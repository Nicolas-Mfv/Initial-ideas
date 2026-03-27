# Notion Space Audit Report (Fail/Issue Only)

- Space: https://www.notion.so/SMB-Cloud-Accounting-Home-309ed78da73080ccb621d75d6ecbb642
- Checklist: https://www.notion.so/FY26-H1-Checklist-CA-Dept-2fbed78da730808e8110f106bb3d1869
- Run at: 2026-03-27T00:00:00Z
- Scope: fail/issue only (PASS entries omitted)

## Summary

- FAIL requirements: 0
- ISSUE requirements: 17
- Notes:
  - The provided URL resolves as a page (`SMB Cloud Accounting Home`), not a directly queryable wiki data source.
  - Search evidence confirms the home page contains "Stock Zone", "Flow Zone", "Archive Zone", and policy text about owner/date and page locking.
  - Child page/database inventory is not retrievable from current fetch output (`<content><empty-block/></content>`), which blocks per-page PASS/FAIL checks.

## Requirement Results (Fail/Issue Only)

### 1.4 Entry homepage has references/links to all other pages in your team space
- ISSUE: Cannot validate link coverage because child page graph is not available from current page fetch output.

### 3.1 Every page has a designated Owner assigned
- ISSUE: Home page policy text exists ("Designated owner ... required"), but per-page owner values are not retrievable without child inventory/data source.

### 3.2 Every page has a Verification Date
- ISSUE: Per-page verification values cannot be checked without child inventory/data source.

### 3.3 Static documents are Page Locked
- ISSUE: Policy text found ("Static documents ... must be page locked"), but lock-state verification across static pages is blocked by missing page list.

### 3.4 Dynamic documents remain unlocked
- ISSUE: Dynamic-page lock-state verification is blocked by missing page list and static/dynamic classification set.

### 3.5 No documents are past their review date
- ISSUE: Review-date values cannot be checked without child inventory/data source.

### 4.1 Finalized documents moved to Stock Zone with Owner + Date assigned
- ISSUE: Requires zone membership + per-page metadata for descendants.

### 4.2 Abandoned documents moved to Archive
- ISSUE: Requires archive membership/content classification for descendants.

### 4.3 Personal notes not relevant to team are in Private spaces
- ISSUE: Requires ownership/privacy intent validation for descendants.

### 5.1 Archive contains only completed/deprecated content
- ISSUE: Requires archive page list and semantic classification.

### 5.2 All pages in Archive zone are Page Locked
- ISSUE: Requires archive page list and lock-state checks.

### 5.3 Documents in Archive are not being edited anymore
- ISSUE: Requires archive page list and edit-recency threshold.

### 5.4 No active projects or current specs are in Archive
- ISSUE: Requires archive page list and semantic classification.

### 6.1 Primary documentation lives in Notion (Single Source of Truth)
- ISSUE: Requires policy adjudication and broader evidence set.

### 6.2 Technical docs in Notion are indexed/linked in Backstage product pages
- ISSUE: No backstage evidence surfaced in scoped search; cannot conclude without descendant pages.

### 6.3 No unauthorized Google Docs, Confluence, or other external tools
- ISSUE: At least one external link was detected in scoped search (Slack URL in home page highlight), but full external-links inventory cannot be generated without full page content/descendants.

### 6.4 Any exceptions are justified and properly indexed
- ISSUE: Requires explicit exception records.

### 7.1 Stock information is properly maintained
- ISSUE: Requires semantic quality review of stock descendants.

### 7.2 Flow information is in designated areas or Private spaces
- ISSUE: Requires semantic review of flow descendants/private pages.

## Available Evidence (Scoped Search Highlights)

- "🗂️ Stock Zone (Official & Active)" found on `SMB Cloud Accounting Home`.
- "📝 Flow Zone (Draft)" found on `SMB Cloud Accounting Home`.
- "📦 Archive Zone" found on `SMB Cloud Accounting Home`.
- "✅ Designated owner and next review date required for all top-level pages" found on `SMB Cloud Accounting Home`.
- "✅ Static documents ... must be page locked" found on `SMB Cloud Accounting Home`.
- External link evidence found in highlight:
  - https://moneyforward.slack.com/archives/C089A6PF1HQ

## Blocking Gap to Resolve Next Iteration

To produce page-level FAIL rows (your preferred format), we need one of:
1) a queryable child data source (`collection://...`) for this home space, or  
2) full descendant page listing + full content fetch access for each child page.
