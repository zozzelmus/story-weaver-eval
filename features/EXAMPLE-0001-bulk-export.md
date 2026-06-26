# EXAMPLE-0001 — Bulk export of saved search results

> This is a worked example so the repo runs out of the box. Replace it (and add ~14 more)
> with real features your team has already ticketed well. Keep the raw, pre-ticket voice —
> this should read like a requirement, not like tickets.

## Requirement

Analysts using the Case Explorer can run a saved search and get back a result grid of cases.
Right now they can only read results on screen, page by page. They've asked to be able to
**export the full result set** of a saved search so they can work with it offline and share
it with people who don't have Case Explorer access.

They want:

- Export the **entire** result set of the currently selected saved search, not just the
  visible page.
- Two formats: **CSV** and **XLSX**. XLSX should preserve column headers and basic formatting;
  CSV is for downstream tooling.
- Only the columns currently shown in the grid (respect the analyst's column config).
- Some saved searches return tens of thousands of rows, so the export can't block the UI or
  time out. A large export should run in the background and notify the analyst when it's ready
  to download.
- Exports may contain sensitive case data, so a download link should expire and access should
  respect the same permissions as viewing the cases.

## Notes / constraints heard in refinement

- The grid already has the column config and the saved-search query; reuse them.
- We have an existing notification mechanism (in-app toast + email) — don't build a new one.
- Files should land in our existing object storage with signed, expiring URLs.
- No new permission model — exports inherit the viewer's case-level permissions.
