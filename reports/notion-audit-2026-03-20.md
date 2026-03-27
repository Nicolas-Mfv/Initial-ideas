# Notion Space Audit Report (Fail/Issue Only)

- Space: https://www.notion.so/2a1ed78da73080c9bc06ca9bf910868b?v=2fded78da7308027b770000cee100c29
- Checklist: https://www.notion.so/FY26-H1-Checklist-CA-Dept-2fbed78da730808e8110f106bb3d1869
- Run at: 2026-03-20T10:05:00Z
- Scope: fail/issue only (PASS entries omitted)

## Summary

- FAIL requirements: 2
- ISSUE requirements: 16
- Notes:
  - `Page Locked` is detectable from page metadata (`<page ... locked>`).
  - Static-vs-dynamic classification is not directly derivable from schema, so rules 3.3/3.4 still need a candidate page set.

## Requirement Results (Fail/Issue Only)

### 1.4 Entry homepage has references/links to all other pages in your team space
- ISSUE: Requires full homepage content/link graph validation across all descendants.
- Note: Root wiki database metadata is available, but this check still needs explicit link-coverage logic against the full page graph.

### 3.2 Every page has a Verification Date
- FAIL: 16 titled pages missing verification.
- https://www.notion.so/329ed78da73080f09c75c8a13054b2b9 — FAIL — `Verification` is null
- https://www.notion.so/319ed78da73080ab941dc6527592432c — FAIL — `Verification` is null
- https://www.notion.so/31bed78da73080479e8efecf2dd00131 — FAIL — `Verification` is null
- https://www.notion.so/2abed78da73080c6abb2ed8bd23125b9 — FAIL — `Verification` is null
- https://www.notion.so/322ed78da73080ba8d78d19dbe591cda — FAIL — `Verification` is null
- https://www.notion.so/319ed78da7308060a604d19cb66b9f1f — FAIL — `Verification` is null
- https://www.notion.so/313ed78da7308005a9efc8a9ca6e3e45 — FAIL — `Verification` is null
- https://www.notion.so/31eed78da730805187ede01584f3f265 — FAIL — `Verification` is null
- https://www.notion.so/309ed78da73080b5b9a0d3f21966ce9d — FAIL — `Verification` is null
- https://www.notion.so/2dfed78da73080e6ae4af121f26b467c — FAIL — `Verification` is null
- https://www.notion.so/2dfed78da73080ee8d62d51383bf0962 — FAIL — `Verification` is null
- https://www.notion.so/2c5ed78da730807eaab3e16635f0422d — FAIL — `Verification` is null
- https://www.notion.so/2ceed78da730804a94c3dae127b8f83c — FAIL — `Verification` is null
- https://www.notion.so/2caed78da73080859659d5c1b727347b — FAIL — `Verification` is null
- https://www.notion.so/2cbed78da73080dda504c9b91321bbb1 — FAIL — `Verification` is null
- https://www.notion.so/2cded78da73080009262dcbc76698dba — FAIL — `Verification` is null

### 3.3 Static documents are Page Locked
- ISSUE: Lock state is detectable, but static-document classification set is not yet defined.
- Example evidence: https://www.notion.so/2cbed78da73080dda504c9b91321bbb1 shows `locked`.

### 3.4 Dynamic documents remain unlocked
- ISSUE: Lock state is detectable, but dynamic-document classification set is not yet defined.

### 3.5 No documents are past their review date
- FAIL: 22 titled pages missing `Date` review field, so review-date governance cannot be validated.
- https://www.notion.so/329ed78da73080f09c75c8a13054b2b9 — FAIL — `Date` missing
- https://www.notion.so/319ed78da73080ab941dc6527592432c — FAIL — `Date` missing
- https://www.notion.so/2e8ed78da730806e950bf567ea6656cf — FAIL — `Date` missing
- https://www.notion.so/2bfed78da7308030a84ef646832b9954 — FAIL — `Date` missing
- https://www.notion.so/2e8ed78da73080c5b240f646e3784358 — FAIL — `Date` missing
- https://www.notion.so/31bed78da73080479e8efecf2dd00131 — FAIL — `Date` missing
- https://www.notion.so/2abed78da73080c6abb2ed8bd23125b9 — FAIL — `Date` missing
- https://www.notion.so/322ed78da73080ba8d78d19dbe591cda — FAIL — `Date` missing
- https://www.notion.so/319ed78da7308060a604d19cb66b9f1f — FAIL — `Date` missing
- https://www.notion.so/313ed78da7308005a9efc8a9ca6e3e45 — FAIL — `Date` missing
- https://www.notion.so/31eed78da730805187ede01584f3f265 — FAIL — `Date` missing
- https://www.notion.so/309ed78da73080b5b9a0d3f21966ce9d — FAIL — `Date` missing
- https://www.notion.so/ce911be39dcb44c09f04d9dab2356e9c — FAIL — `Date` missing
- https://www.notion.so/2a2ed78da73080a3ac41df1e097c6b46 — FAIL — `Date` missing
- https://www.notion.so/2d3ed78da7308070a8fefbac92ff0f22 — FAIL — `Date` missing
- https://www.notion.so/2dfed78da73080e6ae4af121f26b467c — FAIL — `Date` missing
- https://www.notion.so/2dfed78da73080ee8d62d51383bf0962 — FAIL — `Date` missing
- https://www.notion.so/2c5ed78da730807eaab3e16635f0422d — FAIL — `Date` missing
- https://www.notion.so/2ceed78da730804a94c3dae127b8f83c — FAIL — `Date` missing
- https://www.notion.so/2caed78da73080859659d5c1b727347b — FAIL — `Date` missing
- https://www.notion.so/2cbed78da73080dda504c9b91321bbb1 — FAIL — `Date` missing
- https://www.notion.so/2cded78da73080009262dcbc76698dba — FAIL — `Date` missing

### 4.1 Finalized documents moved to Stock Zone with Owner + Date assigned
- ISSUE: Zone transitions and completion state require manual/semantic review.

### 4.2 Abandoned documents moved to Archive
- ISSUE: Requires archive intent/content classification review.

### 4.3 Personal notes not relevant to team are in Private spaces
- ISSUE: Requires ownership/privacy intent validation.

### 5.1 Archive contains only completed/deprecated content
- ISSUE: Requires semantic review of archive contents.

### 5.2 All pages in Archive zone are Page Locked
- ISSUE: Lock can be detected; archive membership list still needed for deterministic check.

### 5.3 Documents in Archive are not being edited anymore
- ISSUE: Needs archive page list + edit recency threshold.

### 5.4 No active projects or current specs are in Archive
- ISSUE: Requires semantic classification of archived documents.

### 6.1 Primary documentation lives in Notion (Single Source of Truth)
- ISSUE: Requires policy and source-of-truth validation against external systems.

### 6.2 Technical docs in Notion are indexed/linked in Backstage product pages
- ISSUE: Backstage references exist in content, but end-to-end coverage is not yet proven.

### 6.3 No unauthorized Google Docs, Confluence, or other external tools
- ISSUE: External links detected; authorization cannot be inferred automatically.
- See inventory below for manual review.

### 6.4 Any exceptions are justified and properly indexed
- ISSUE: Requires explicit exception records/policy mapping.

### 7.1 Stock information is properly maintained
- ISSUE: Requires semantic quality review.

### 7.2 Flow information is in designated areas or Private spaces
- ISSUE: Requires zone mapping + semantic review.

## External Links Inventory (for Manual Investigation)

Note:
- Source: fetched content from all 22 titled pages.
- Query strings removed from very long signed URLs where appropriate.
- Notion URLs excluded.

| Domain | URL | Found in page |
|---|---|---|
| docs.google.com | https://docs.google.com/document/d/1Lzdn8jLdFmREOFXy4E7CahGk5V5Gyve17_0gnOC8HvE/edit | CA Dev Leaders’ Meeting |
| biz.moneyforward.com | https://biz.moneyforward.com/support/account/guide/others/ot03.html | ScanSnap連携処理説明 / CA: Scansnap Integration memo |
| accounting.moneyforward.com | https://accounting.moneyforward.com/accounts/co_scansnap/oauth?country=ja_JP | ScanSnap連携処理説明 |
| accounting-stg1-test.ebisubook.com | https://accounting-stg1-test.ebisubook.com/accounts/co_scansnap/oauth?country=ja_JP | ScanSnap連携処理説明 |
| api-jp.cloud.scansnap.com | https://api-jp.cloud.scansnap.com/ | ScanSnap連携処理説明 / CA: Scansnap Integration memo |
| isv-api.cloud.scansnap.com | https://isv-api.cloud.scansnap.com/ | ScanSnap連携処理説明 / CA: Scansnap Integration memo |
| auth-jp.cloud.scansnap.com | https://auth-jp.cloud.scansnap.com/oauth2/authorize | ScanSnap連携処理説明 |
| accounting.moneyforward.com | https://accounting.moneyforward.com/auth/scansnap/callback | ScanSnap連携処理説明 |
| accounting-stg1-test.ebisubook.com | https://accounting-stg1-test.ebisubook.com/auth/scansnap/callback | ScanSnap連携処理説明 |
| drive.google.com | https://drive.google.com/file/d/1KkW9PsiVrsUeRkW68vcxu1anmNfOSxDy/view | CA: Scansnap Integration memo |
| drive.google.com | https://drive.google.com/file/d/1wm4BwXoXUGn2Ks7WR6xgRzwoWr6nvcB7/view | CA: Scansnap Integration memo |
| github.com | https://github.com/moneyforward/ca_web/pull/38384/files | CA: Scansnap Integration memo |
| biz.moneyforward.com | https://biz.moneyforward.com/support/account/faq/linkage/l06.html | CA: Scansnap Integration memo |
| docs.google.com | https://docs.google.com/spreadsheets/d/1p8ulAjXhuBVMZAzh2X7-nb0pg27sBgFa5REcGWSud_s/edit | Standardization of CA Onboarding document |
| docs.google.com | https://docs.google.com/spreadsheets/d/18oNg-2jla2oPIGjiOpA4G-oEv3Qmlr63Xv-wJWQMLyA/edit | Standardization of CA Onboarding document |
| moneyforward.slack.com | https://moneyforward.slack.com/team/U08L3T302TX | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| moneyforward.slack.com | https://moneyforward.slack.com/team/U07UXBNJ3AL | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| moneyforward.slack.com | https://moneyforward.slack.com/team/U06S7NECACU | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| attendance.moneyforward.com | https://attendance.moneyforward.com/my_page/settings/integrations | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| github.com | https://github.com/integrations/slack | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| circleci.com | https://circleci.com/ | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| figma.com | https://figma.com/ | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| launcher.myapps.microsoft.com | https://launcher.myapps.microsoft.com/api/signin/432fae38-9496-4fdf-87d1-8949c067b4e1 | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| myapplications.microsoft.com | https://myapplications.microsoft.com/ | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| analytics.google.com | https://analytics.google.com/analytics/web | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| lookerstudio.google.com | https://lookerstudio.google.com/navigation/reporting | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| chromewebstore.google.com | https://chromewebstore.google.com/detail/esakibela-to-notion-redir/ihegohkilecklemmoldidoobmiaccchk | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| moneyforward.cybozu.com | https://moneyforward.cybozu.com/o/ag.cgi?page=WorkFlowForm&id=21588 | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| moneyforward.cybozu.com | https://moneyforward.cybozu.com/o/ag.cgi?page=WorkFlowForm&id=1978142 | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| moneyforward.cybozu.com | https://moneyforward.cybozu.com/o/ag.cgi?page=WorkFlowForm&id=1367 | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| sites.google.com | https://sites.google.com/moneyforward.co.jp/onboardingsite-eng/work | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| docs.google.com | https://docs.google.com/spreadsheets/d/1i4IYawEqzApsqDHWe6fNxtxLiEHFBZw1yhsSKpXJyZo/edit | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| miro.com | https://miro.com/app/board/uXjVOcD9v-U=/ | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) / Documents to read |
| miro.com | https://miro.com/app/board/o9J_llqGzgw=/ | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) / Documents to read |
| github.com | https://github.com/moneyforward/ca_web | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
| sites.google.com | https://sites.google.com/moneyforward.co.jp/onboardingsite/home | Documents to read |
| docs.google.com | https://docs.google.com/presentation/d/1roN4n3do9_SxeNGYZhja6DPRbl3ONg42/edit | Documents to read |
| miro.com | https://miro.com/app/board/uXjVOrTLe0M=/ | Documents to read |
| moneyforward.kibe.la | https://moneyforward.kibe.la/notes/286088 | Documents to read |
| docs.google.com | https://docs.google.com/spreadsheets/d/1Z6g7a5eVn9G0wsylmMAFaoDV7wVBEMBp37Fpd7I6tzw/edit | Documents to read |
| prod-files-secure.s3.us-west-2.amazonaws.com | https://prod-files-secure.s3.us-west-2.amazonaws.com/... | ScanSnap連携処理説明 / CA: Scansnap Integration memo / 作業中tmp... / How to create the individual GGI Page |
| mailto | mailto:kamezaki.yuto@moneyforward.co.jp | 作業中tmp mugima working Cloud Accounting Department Intern Onboarding Overview (1) |
