# EXAMPLE-0001 — Bulk export of saved search results (REFERENCE / human-written)

> This is the ground truth the judge compares generated output against. These are the tickets
> the team would actually be happy shipping. Note the vertical slicing, the Given/When/Then
> AC, the reuse of existing components/labels, and that nothing here is a bare "build the API"
> horizontal layer.
>
> ⚠️ Leakage rule: do NOT also place these in `corpus/`. The grounding pool must be different
> tickets from these references.

## Epic: Saved-search bulk export
**Description:** Let Case Explorer analysts export the full result set of a saved search to
CSV or XLSX, running large exports in the background and delivering them via expiring,
permission-checked download links.
**Components:** case-explorer, exports  **Labels:** analyst-tools, q3-roadmap

---

### Story 1: Export a saved search to CSV synchronously for small result sets
**Epic Link:** Saved-search bulk export
**Description:** For result sets small enough to generate quickly, let an analyst export the
current saved search to CSV directly from the result grid, using their current column config.
**Acceptance Criteria:**
- **Given** a saved search returning ≤ 5,000 rows **When** the analyst selects Export → CSV **Then** a CSV of the full result set downloads, containing only the columns currently shown in the grid, in the grid's column order.
- **Given** the export is generating **When** the analyst waits **Then** a progress indicator is shown and the grid stays interactive.
- **Given** a column is hidden in the analyst's grid config **When** they export **Then** that column is omitted from the file.
**Components:** case-explorer, exports  **Labels:** analyst-tools

### Story 2: Export to XLSX with headers and basic formatting
**Epic Link:** Saved-search bulk export
**Description:** Offer XLSX as an export format, preserving column headers and basic cell
formatting so the file is presentation-ready for non-Case-Explorer recipients.
**Acceptance Criteria:**
- **Given** a saved search result **When** the analyst selects Export → XLSX **Then** an .xlsx file downloads with a header row matching the grid columns and date/number cells formatted appropriately.
- **Given** the same data **When** exported as XLSX vs CSV **Then** both contain identical rows and columns.
**Components:** case-explorer, exports  **Labels:** analyst-tools

### Story 3: Run large exports in the background with notify-on-ready
**Epic Link:** Saved-search bulk export
**Description:** For result sets too large to generate inline, run the export as a background
job and notify the analyst when the file is ready, so the UI never blocks or times out.
**Acceptance Criteria:**
- **Given** a saved search returning more than 5,000 rows **When** the analyst exports **Then** the export is queued as a background job and the analyst is told it will be delivered when ready, without blocking the UI.
- **Given** a background export completes **When** the file is ready **Then** the analyst receives an in-app toast and an email via the existing notification mechanism, each linking to the download.
- **Given** a background export fails **When** the job errors **Then** the analyst is notified of the failure and can retry.
**Components:** case-explorer, exports, notifications  **Labels:** analyst-tools

### Story 4: Deliver exports via expiring, permission-checked download links
**Epic Link:** Saved-search bulk export
**Description:** Store export files in existing object storage and serve them through signed
URLs that expire and re-check the requester's case-level permissions, since exports can carry
sensitive case data.
**Acceptance Criteria:**
- **Given** a completed export **When** the file is stored **Then** it is written to object storage and accessed only through a signed URL with a finite expiry.
- **Given** a download link **When** it is opened after expiry **Then** access is denied and the analyst is prompted to regenerate the export.
- **Given** an analyst whose case permissions changed after export **When** they open the link **Then** access is re-checked against current case-level permissions before the file is served.
**Components:** exports, security  **Labels:** analyst-tools, security
