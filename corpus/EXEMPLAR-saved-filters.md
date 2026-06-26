# EXEMPLAR — Saved search filters (grounding corpus)

> A well-written past ticket used as a GROUNDING exemplar. It teaches the model how this
> project writes summaries, AC, components, and labels. It is intentionally a DIFFERENT
> feature from anything in `reference-tickets/` — keep it that way (leakage rule).

## Story: Let analysts save and reuse Case Explorer search filters
**Epic Link:** Case Explorer search
**Description:** Analysts re-run the same searches daily. Let them save a configured set of
search filters under a name and re-apply it later, so they don't rebuild common searches by hand.
**Acceptance Criteria:**
- **Given** an analyst has configured search filters **When** they choose Save Search and name it **Then** the named search appears in their saved-search list.
- **Given** a saved search **When** the analyst selects it **Then** the grid re-runs with exactly the saved filters applied.
- **Given** a saved search the analyst owns **When** they rename or delete it **Then** the change is reflected in their list and does not affect other analysts.
**Components:** case-explorer, search  **Labels:** analyst-tools
