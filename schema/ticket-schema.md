# Jira Ticket Schema

Every generator variant outputs tickets in **this shape**, and the judge scores against it.
Keeping the schema in one file means changing the target ticket format is a one-place edit.

> **Drafts only.** No variant in this repo ever *creates* Jira issues. The output is Markdown
> that a human reviews. Even when a Jira MCP is connected, the generators use it **read-only**
> (search, read epics, read components/labels). The only write path in a real Story Weaver v2
> would sit behind a human approval gate — deliberately out of scope for an eval harness.

## Issue types

- **Epic** — a body of work spanning multiple stories. One feature usually maps to 1–2 epics.
- **Story** — a vertically-sliced, independently valuable, testable unit. The main output.
- **Sub-task** — only when a story genuinely needs decomposition; don't manufacture these.

## Fields per ticket

| Field                | Required | Notes |
|----------------------|----------|-------|
| Issue Type           | yes      | Epic / Story / Sub-task |
| Summary              | yes      | Imperative, specific. Not "User login" — "Allow returning users to sign in with email + password". |
| Description          | yes      | Context + the *what* and *why*. 2–5 sentences. No restating the whole feature. |
| Acceptance Criteria  | yes (Story/Sub-task) | One or more **Given / When / Then** scenarios. This is where most single-shot output is thin. |
| Epic Link / Parent   | yes (Story) | Which epic this rolls up to. Use the real epic key if grounding via Jira MCP surfaced one. |
| Components           | when known | Match existing project components — don't invent new ones. |
| Labels               | when known | Reuse existing labels from grounding; don't coin novel ones. |
| Story Point Estimate | optional | Only if a comparable exemplar implies a scale. Never guess into a vacuum. |
| Priority             | optional | Only if the requirement signals it. |

## Output format (Markdown the generators write to `results/`)

````markdown
# <CASE-ID> — <variant>

## Epic: <summary>
**Description:** ...
**Components:** ...  **Labels:** ...

### Story 1: <summary>
**Epic Link:** <epic summary or JIRA-KEY>
**Description:** ...
**Acceptance Criteria:**
- **Given** ... **When** ... **Then** ...
- **Given** ... **When** ... **Then** ...
**Components:** ...  **Labels:** ...  **Estimate:** ...

### Story 2: <summary>
...
````

## What "good" means (this is also the judge's rubric — INVEST)

- **Independent** — minimal dependence on other unfinished stories.
- **Negotiable** — describes the need, leaves room for implementation discussion; not a spec dump.
- **Valuable** — delivers observable value to a user or the business; a vertical slice, not a layer.
- **Estimable** — clear enough that the team could size it.
- **Small** — fits comfortably in a sprint; if it can't, it should have been split.
- **Testable** — the acceptance criteria are concrete and verifiable.

A recurring single-shot failure to watch for: **horizontal slicing** (a "DB ticket", an "API
ticket", a "UI ticket") instead of **vertical slices** by deliverable user value. The judge
penalizes this under Independent + Valuable.
