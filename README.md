# Initial-ideas

## Run Notion audit from command line

Use the CLI script to run a fail/issue-only audit against any Notion space URL.

### 1) Export a Notion API token

```bash
export NOTION_TOKEN="secret_xxx"
```

The token must have access to the target page/database.

### 2) Run the audit

```bash
python3 scripts/notion_audit_cli.py \
  --space-url "https://www.notion.so/SMB-Cloud-Accounting-Home-309ed78da73080ccb621d75d6ecbb642"
```

Optional checklist override:

```bash
python3 scripts/notion_audit_cli.py \
  --space-url "https://www.notion.so/<your-space>" \
  --checklist-url "https://www.notion.so/<your-checklist>"
```

### 3) Output files

Reports are written in `reports/` with a filename based on:

- run date
- audited space title/URL slug

Example:

- `reports/notion-audit-2026-03-27-smb-cloud-accounting-home.md`
- `reports/notion-audit-2026-03-27-smb-cloud-accounting-home.json`

This avoids overwriting reports when auditing different spaces.
