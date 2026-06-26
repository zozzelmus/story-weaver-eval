# Jira Ticket Schema

`draft-tickets` outputs tickets in **this shape**, and `publish-to-jira` maps this shape onto
real Jira fields. Keeping the schema in one file means changing the target ticket format is a
one-place edit.

> **Drafts first, write behind a gate.** `draft-tickets` only ever produces Markdown — one file
> per ticket in `tickets-review/<FEATURE-KEY>/` — that a human reviews. Reads against Jira
> (search, read epics, read components/labels, dedup) are read-only. The **only** write path is
> `publish-to-jira`, and it runs only after explicit human approval of the reviewed files.

## Issue types

- **Epic** — a body of work spanning multiple stories. One feature usually maps to 1–2 epics.
- **Story** — a vertically-sliced, independently valuable, testable unit. The main output.
- **Sub-task** — only when a story genuinely needs decomposition; don't manufacture these.

(Use the issue types the team profile says this project actually uses — don't introduce a type
the team doesn't.)

## Fields per ticket

| Field                | Required | Notes |
|----------------------|----------|-------|
| Issue Type           | yes      | Epic / Story / Sub-task |
| Summary              | yes      | In the team's voice (profile). Specific, not "User login" — "Allow returning users to sign in with email + password". |
| Description          | yes      | Context + the *what* and *why*. Match the team's typical depth. No restating the whole feature. |
| Acceptance Criteria  | yes (Story/Sub-task) | In the team's AC format (Given/When/Then or their checklist). This is where naive output is thin. |
| Epic Link / Parent   | yes (Story) | Which epic this rolls up to. Use the real epic key when grounding surfaced one. |
| Components           | when known | Reuse existing project components from the profile — don't invent new ones. |
| Labels               | when known | Reuse existing labels from the profile; don't coin novel ones. |
| Story Point Estimate | optional | Only on the team's scale, only if a comparable exemplar implies one. Never guess into a vacuum. |
| Priority             | optional | Only if the requirement or the team's convention signals it. |

## Output format (Markdown `draft-tickets` writes)

Each ticket is its own file, `tickets-review/<FEATURE-KEY>/NN-<slug>.md`, with a front-matter
block the publisher reads, then the human-readable ticket:

````markdown
---
issue_type: Story
parent: <epic summary or JIRA-KEY>
components: [case-explorer, exports]
labels: [analyst-tools]
estimate: 3
status: draft        # publisher flips to "created: <KEY>" after pushing
duplicate_of:        # set if dedup flagged an existing issue
---

### Story: <summary>
**Epic Link:** <epic summary or JIRA-KEY>
**Description:** ...
**Acceptance Criteria:**
- **Given** ... **When** ... **Then** ...
- **Given** ... **When** ... **Then** ...
**Components:** ...  **Labels:** ...  **Estimate:** ...
````

`INDEX.md` in the same directory carries the decomposition tree, the critique log, and the
approval checklist (see `draft-tickets`).

## What "good" means — INVEST

The quality bar `draft-tickets` self-checks against:

- **Independent** — minimal dependence on other unfinished stories.
- **Negotiable** — describes the need, leaves room for implementation discussion; not a spec dump.
- **Valuable** — delivers observable value to a user or the business; a vertical slice, not a layer.
- **Estimable** — clear enough that the team could size it.
- **Small** — fits comfortably in a sprint; if it can't, it should have been split.
- **Testable** — the acceptance criteria are concrete and verifiable.

A recurring failure to watch for: **horizontal slicing** (a "DB ticket", an "API ticket", a "UI
ticket") instead of **vertical slices** by deliverable user value — it fails Independent +
Valuable. Slice the way the team profile shows this team slices.
