#!/usr/bin/env python3
"""
Run a fail/issue-only Notion space audit from command line.

This script is intentionally conservative:
- Emits only FAIL / ISSUE entries.
- Treats unverifiable checks as ISSUE (never PASS output).
- Names output files per space slug so different spaces do not overwrite.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


DEFAULT_CHECKLIST_URL = (
    "https://www.notion.so/FY26-H1-Checklist-CA-Dept-2fbed78da730808e8110f106bb3d1869"
)
NOTION_VERSION = "2022-06-28"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "space"


def extract_notion_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    uuid_re = re.compile(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
    matches = uuid_re.findall(s)
    if not matches:
        raise ValueError(f"Could not extract Notion ID from: {url_or_id}")
    raw = matches[-1].replace("-", "").lower()
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"


def request_json(
    token: str,
    method: str,
    path: str,
    data: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    base = f"https://api.notion.com{path}"
    if query:
        base += "?" + urllib.parse.urlencode(query)
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(base, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {method} {path} failed: {e.code} {raw}") from e


def fetch_page(token: str, page_id: str) -> Dict[str, Any]:
    return request_json(token, "GET", f"/v1/pages/{page_id}")


def fetch_database(token: str, database_id: str) -> Dict[str, Any]:
    return request_json(token, "GET", f"/v1/databases/{database_id}")


def fetch_block_children(token: str, block_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while True:
        payload: Dict[str, Any] = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        chunk = request_json(token, "GET", f"/v1/blocks/{block_id}/children", query=payload)
        out.extend(chunk.get("results", []))
        if not chunk.get("has_more"):
            break
        cursor = chunk.get("next_cursor")
    return out


def query_database_pages(token: str, database_id: str, max_pages: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while len(out) < max_pages:
        body: Dict[str, Any] = {"page_size": min(100, max_pages - len(out))}
        if cursor:
            body["start_cursor"] = cursor
        chunk = request_json(token, "POST", f"/v1/databases/{database_id}/query", data=body)
        out.extend(chunk.get("results", []))
        if not chunk.get("has_more"):
            break
        cursor = chunk.get("next_cursor")
    return out


def get_title_from_properties(props: Dict[str, Any]) -> str:
    for _, p in props.items():
        if p.get("type") == "title":
            parts = p.get("title", [])
            return "".join((it.get("plain_text") or "") for it in parts).strip() or "Untitled"
    return "Untitled"


def find_property_name_by_casefold(properties: Dict[str, Any], target: str) -> Optional[str]:
    tgt = target.casefold()
    for name in properties.keys():
        if name.casefold() == tgt:
            return name
    return None


def property_is_empty(value: Dict[str, Any]) -> bool:
    ptype = value.get("type")
    if ptype == "title":
        return len(value.get("title", [])) == 0
    if ptype == "rich_text":
        return len(value.get("rich_text", [])) == 0
    if ptype == "people":
        return len(value.get("people", [])) == 0
    if ptype == "relation":
        return len(value.get("relation", [])) == 0
    if ptype == "multi_select":
        return len(value.get("multi_select", [])) == 0
    if ptype in ("select", "status"):
        return value.get(ptype) is None
    if ptype == "date":
        return value.get("date") is None
    if ptype == "checkbox":
        return not bool(value.get("checkbox"))
    if ptype in ("url", "email", "phone_number"):
        return not bool(value.get(ptype))
    if ptype == "number":
        return value.get("number") is None
    if ptype == "files":
        return len(value.get("files", [])) == 0
    if ptype == "verification":
        verification = value.get("verification")
        if verification is None:
            return True
        # Best-effort: treat "verified" as present.
        if isinstance(verification, dict):
            return verification.get("state") != "verified"
        return False
    # Unknown types default to "not empty" to avoid false FAIL.
    return False


def crawl_blocks(
    token: str,
    block_id: str,
    max_blocks: int = 5000,
) -> Tuple[str, Set[str], Set[str]]:
    """Return (flattened_text, urls, child_database_ids)."""
    text_parts: List[str] = []
    urls: Set[str] = set()
    child_db_ids: Set[str] = set()
    seen = 0

    def walk(current_id: str) -> None:
        nonlocal seen
        if seen >= max_blocks:
            return
        children = fetch_block_children(token, current_id)
        for block in children:
            seen += 1
            if seen >= max_blocks:
                return

            # Plain text extraction from rich_text arrays.
            block_type = block.get("type")
            typed = block.get(block_type, {}) if block_type else {}
            if isinstance(typed, dict):
                rt = typed.get("rich_text")
                if isinstance(rt, list):
                    for item in rt:
                        pt = item.get("plain_text")
                        if pt:
                            text_parts.append(pt)
                        href = item.get("href")
                        if href:
                            urls.add(href)
                        tdict = item.get("text", {})
                        if isinstance(tdict, dict):
                            link = tdict.get("link")
                            if isinstance(link, dict) and link.get("url"):
                                urls.add(link["url"])

            # Child database blocks.
            if block_type == "child_database":
                dbid = block.get("id")
                if dbid:
                    child_db_ids.add(dbid)

            # Catch URL-looking substrings from serialized block.
            raw = json.dumps(block, ensure_ascii=False)
            for u in re.findall(r"https?://[^\s\"'<>)+]+", raw):
                urls.add(u.rstrip(".,);]"))
            for m in re.findall(r"mailto:[^\s\"'<>)+]+", raw):
                urls.add(m.rstrip(".,);]"))

            if block.get("has_children"):
                walk(block.get("id"))

    walk(block_id)
    return "\n".join(text_parts), urls, child_db_ids


def normalize_external_urls(urls: Iterable[str]) -> List[Tuple[str, str]]:
    out: Set[Tuple[str, str]] = set()
    notion_hosts = {"notion.so", "www.notion.so", "notion.site", "calendar.notion.so"}
    for url in urls:
        if not url:
            continue
        if url.startswith("mailto:"):
            out.add(("mailto", url))
            continue
        try:
            p = urllib.parse.urlparse(url)
        except Exception:
            continue
        if p.scheme not in ("http", "https"):
            continue
        host = (p.netloc or "").lower()
        if any(host == h or host.endswith("." + h) for h in notion_hosts):
            continue
        # Remove huge querystrings for signed URLs in report readability.
        clean = f"{p.scheme}://{p.netloc}{p.path}"
        if p.query and "amazonaws.com" not in host:
            clean += "?" + p.query
        out.add((host, clean))
    return sorted(out, key=lambda x: (x[0], x[1]))


def build_markdown_report(
    space_url: str,
    checklist_url: str,
    run_at: str,
    fail_items: Dict[str, List[str]],
    issue_items: Dict[str, List[str]],
    external_links: List[Tuple[str, str]],
    evidence_notes: List[str],
) -> str:
    lines: List[str] = []
    lines.append("# Notion Space Audit Report (Fail/Issue Only)")
    lines.append("")
    lines.append(f"- Space: {space_url}")
    lines.append(f"- Checklist: {checklist_url}")
    lines.append(f"- Run at: {run_at}")
    lines.append("- Scope: fail/issue only (PASS entries omitted)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- FAIL requirements: {len(fail_items)}")
    lines.append(f"- ISSUE requirements: {len(issue_items)}")
    lines.append("")
    lines.append("## Requirement Results (Fail/Issue Only)")
    lines.append("")

    for req_id, items in fail_items.items():
        lines.append(f"### {req_id}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    for req_id, items in issue_items.items():
        lines.append(f"### {req_id}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## External Links Inventory (for Manual Investigation)")
    lines.append("")
    if not external_links:
        lines.append("- ISSUE: No external links extracted from available content.")
    else:
        lines.append("| Domain | URL |")
        lines.append("|---|---|")
        for domain, url in external_links:
            lines.append(f"| {domain} | {url} |")
    lines.append("")

    if evidence_notes:
        lines.append("## Evidence Notes")
        lines.append("")
        for n in evidence_notes:
            lines.append(f"- {n}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def run_audit(args: argparse.Namespace) -> Tuple[Dict[str, Any], str]:
    token = args.notion_token or os.getenv("NOTION_TOKEN")
    if not token:
        raise SystemExit(
            "Missing Notion token. Set NOTION_TOKEN env var or pass --notion-token."
        )

    space_id = extract_notion_id(args.space_url)
    run_at = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    fail_items: Dict[str, List[str]] = {}
    issue_items: Dict[str, List[str]] = {}
    evidence_notes: List[str] = []

    root_obj: Dict[str, Any]
    root_type = "page"
    try:
        root_obj = fetch_page(token, space_id)
    except RuntimeError:
        root_obj = fetch_database(token, space_id)
        root_type = "database"

    if root_type == "page":
        root_title = get_title_from_properties(root_obj.get("properties", {}))
        page_text, urls, child_dbs = crawl_blocks(token, space_id, max_blocks=args.max_blocks)
    else:
        root_title = root_obj.get("title", [{}])[0].get("plain_text", "space")
        page_text, urls, child_dbs = "", set(), {space_id}

    lower_text = page_text.casefold()
    external_links = normalize_external_urls(urls)

    # Structure checks (only emit when failing).
    if "stock zone" not in lower_text:
        fail_items.setdefault("2.1 Stock Zone exists", []).append(
            "FAIL — Could not find 'Stock Zone' in available page content."
        )
    if "flow zone" not in lower_text and "flow/drafts zone" not in lower_text:
        fail_items.setdefault("2.2 Flow Zone exists", []).append(
            "FAIL — Could not find 'Flow Zone' in available page content."
        )
    if "archive zone" not in lower_text:
        fail_items.setdefault("2.3 Archive Zone exists", []).append(
            "FAIL — Could not find 'Archive Zone' in available page content."
        )

    # Discover candidate database.
    db_id: Optional[str] = None
    if child_dbs:
        db_id = sorted(child_dbs)[0]
        if len(child_dbs) > 1:
            evidence_notes.append(
                f"Multiple child databases found ({len(child_dbs)}); used first database id: {db_id}"
            )
    else:
        issue_items.setdefault("Data access", []).append(
            "ISSUE — No child database found from fetched blocks. Per-page metadata checks are limited."
        )

    if db_id:
        try:
            db = fetch_database(token, db_id)
            props = db.get("properties", {})
            owner_prop = find_property_name_by_casefold(props, "Owner")
            date_prop = find_property_name_by_casefold(props, "Date")
            verification_prop = find_property_name_by_casefold(props, "Verification")
            rows = query_database_pages(token, db_id, args.max_db_pages)

            if owner_prop:
                missing_owner = []
                for row in rows:
                    p = row.get("properties", {}).get(owner_prop)
                    if p is not None and property_is_empty(p):
                        missing_owner.append(
                            f"{row.get('url', 'unknown-url')} — FAIL — `{owner_prop}` is empty"
                        )
                if missing_owner:
                    fail_items["3.1 Every page has a designated Owner assigned"] = missing_owner
            else:
                issue_items.setdefault("3.1 Every page has a designated Owner assigned", []).append(
                    "ISSUE — Owner property not found in selected database schema."
                )

            if verification_prop:
                missing_verif = []
                for row in rows:
                    p = row.get("properties", {}).get(verification_prop)
                    if p is not None and property_is_empty(p):
                        missing_verif.append(
                            f"{row.get('url', 'unknown-url')} — FAIL — `{verification_prop}` is empty"
                        )
                if missing_verif:
                    fail_items["3.2 Every page has a Verification Date"] = missing_verif
            else:
                issue_items.setdefault("3.2 Every page has a Verification Date", []).append(
                    "ISSUE — Verification property not found in selected database schema."
                )

            if date_prop:
                missing_date = []
                for row in rows:
                    p = row.get("properties", {}).get(date_prop)
                    if p is not None and property_is_empty(p):
                        missing_date.append(
                            f"{row.get('url', 'unknown-url')} — FAIL — `{date_prop}` is empty"
                        )
                if missing_date:
                    fail_items["3.5 No documents are past their review date"] = missing_date
            else:
                issue_items.setdefault("3.5 No documents are past their review date", []).append(
                    "ISSUE — Date property not found in selected database schema."
                )

        except Exception as e:  # noqa: BLE001
            issue_items.setdefault("Data access", []).append(
                f"ISSUE — Could not query selected database `{db_id}`: {e}"
            )

    # Known manual/semantic checks.
    for req in [
        "1.4 Entry homepage has references/links to all other pages",
        "3.3 Static documents are Page Locked",
        "3.4 Dynamic documents remain unlocked",
        "4.1 Finalized docs moved to Stock with Owner + Date",
        "4.2 Abandoned docs moved to Archive",
        "4.3 Personal notes are in Private spaces",
        "5.1 Archive contains only completed/deprecated content",
        "5.2 All pages in Archive zone are Page Locked",
        "5.3 Documents in Archive are not being edited anymore",
        "5.4 No active projects/current specs are in Archive",
        "6.1 Primary documentation lives in Notion (Single Source of Truth)",
        "6.2 Technical docs in Notion are indexed/linked in Backstage product pages",
        "6.3 No unauthorized Google Docs/Confluence/external tools",
        "6.4 Exceptions are justified and properly indexed",
        "7.1 Stock information is properly maintained",
        "7.2 Flow information is in designated areas or Private spaces",
    ]:
        issue_items.setdefault(req, []).append(
            "ISSUE — Requires semantic/manual adjudication or additional data mapping."
        )

    if "locked" in lower_text:
        evidence_notes.append("Found 'locked' policy text in available content.")
    if external_links:
        evidence_notes.append(f"Extracted {len(external_links)} unique external links.")
    else:
        evidence_notes.append("No external links extracted from available content.")

    report_markdown = build_markdown_report(
        space_url=args.space_url,
        checklist_url=args.checklist_url,
        run_at=run_at,
        fail_items=fail_items,
        issue_items=issue_items,
        external_links=external_links,
        evidence_notes=evidence_notes,
    )

    json_report: Dict[str, Any] = {
        "meta": {
            "run_at": run_at,
            "space_url": args.space_url,
            "checklist_url": args.checklist_url,
            "root_type": root_type,
            "root_title": root_title,
            "mode": "fail_issue_only",
        },
        "summary": {
            "fail_requirements": len(fail_items),
            "issue_requirements": len(issue_items),
        },
        "fails": fail_items,
        "issues": issue_items,
        "external_links": [{"domain": d, "url": u} for d, u in external_links],
        "evidence_notes": evidence_notes,
    }
    return json_report, report_markdown


def write_reports(
    output_dir: str,
    run_date: dt.date,
    slug: str,
    json_report: Dict[str, Any],
    markdown_report: str,
) -> Tuple[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    stem = f"notion-audit-{run_date.isoformat()}-{slug}"
    md_path = os.path.join(output_dir, f"{stem}.md")
    json_path = os.path.join(output_dir, f"{stem}.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return md_path, json_path


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fail/issue-only Notion space audit.")
    parser.add_argument("--space-url", required=True, help="Notion space/home URL or page ID.")
    parser.add_argument(
        "--checklist-url",
        default=DEFAULT_CHECKLIST_URL,
        help="Checklist page URL (stored in report metadata).",
    )
    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory to write report files into.",
    )
    parser.add_argument(
        "--notion-token",
        default=None,
        help="Notion API token (if omitted, uses NOTION_TOKEN env var).",
    )
    parser.add_argument(
        "--max-db-pages",
        type=int,
        default=300,
        help="Max number of database pages to inspect.",
    )
    parser.add_argument(
        "--max-blocks",
        type=int,
        default=5000,
        help="Max blocks to crawl when scanning page content.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    json_report, md_report = run_audit(args)
    title = json_report.get("meta", {}).get("root_title") or args.space_url
    slug = slugify(str(title))
    md_path, json_path = write_reports(
        output_dir=args.output_dir,
        run_date=dt.date.today(),
        slug=slug,
        json_report=json_report,
        markdown_report=md_report,
    )
    print(f"Wrote markdown report: {md_path}")
    print(f"Wrote json report:     {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

