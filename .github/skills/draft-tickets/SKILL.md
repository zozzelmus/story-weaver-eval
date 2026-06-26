---
name: draft-tickets
description: Draft Jira tickets for a feature, matched to the team's learned conventions. Reads the gathered context and the persisted team profile, decomposes the feature into a vertical epic-to-story tree, drafts each ticket in the team's house style, runs a light INVEST self-check and read-only backlog dedup, and writes ONE markdown file per ticket into a review directory for a human to approve. This skill never writes to Jira. Use whenever asked to draft, generate, or write tickets/stories for a feature.
---

# draft-tickets — feature → reviewable ticket drafts

Turn one feature into a set of tickets that **look like this team wrote them**, and lay them out
as **one markdown file per ticket** in a review directory so a human can read, edit, and approve
them before anything is pushed to Jira.

This skill **produces drafts only**. It does not touch Jira except read-only (dedup). Writing is
`publish-to-jira`'s job, behind the gate.

## Inputs

```
/draft-tickets feature=<JIRA-FEATURE-KEY>
```

Reads:
- `tickets-review/<FEATURE-KEY>/_context.md` — the brief from `gather-context`.
- `profile/team-profile.md` — the learned conventions (the whole point: imitate this).
- `schema/ticket-schema.md` — the ticket shape and the INVEST quality bar.

If the team profile is missing, stop and tell the user to run `/learn-team` first — drafting
without it produces generic tickets, which is the exact thing we're trying to beat.

## Steps

### 1. Decompose — vertical slices, in the team's pattern

Produce an explicit epic→story tree before drafting any ticket:

```
Feature: <name>
├── Epic A: <summary>            — rationale: <why this is a coherent epic>
│   ├── Story A1: <summary>      — rationale: <the user/business value this slice delivers>
│   └── Story A2: <summary>      — rationale: ...
└── Epic B: <summary>            — rationale: ...
```

- **Slice vertically by deliverable value**, not horizontally by layer (no "DB story / API story
  / UI story"). Each story should be demonstrable on its own.
- Match the **granularity** the profile observed on this team — don't over-split into thin
  tasks or under-split into sprint-busting epics.
- Each node carries a one-line rationale. That rationale is the reasoning naive tools skip.

### 2. Draft each ticket in the team's voice

Expand each leaf into a full ticket per `schema/ticket-schema.md`, **styled to the profile**:

- summary phrasing in the team's preferred voice,
- AC in the team's format (Given/When/Then or their checklist style) — cover the happy path
  **and** the obvious edges/errors the context brief surfaced,
- **reuse real components and labels** from the profile; link each story to a real epic,
- estimate only on the team's scale and only when a comparable exemplar implies one,
- use the **domain glossary** from the profile so it reads like an insider wrote it.

### 3. Self-check — INVEST + dedup (one pass)

For each ticket, quickly check the six INVEST dimensions (see schema) and AC completeness;
revise anything weak **once**. Then a **read-only** dedup pass: search the backlog for near-
duplicates (capability: "search Jira issues by JQL"); if a strong match exists, flag it in the
ticket and prefer referencing the existing issue over creating a near-twin. Never create issues
here.

### 4. Write the review directory — one file per ticket

Into `tickets-review/<FEATURE-KEY>/`, write:

- `NN-<slug>.md` per ticket (`01-export-csv-small-sets.md`, …), each a complete, self-contained
  ticket in the schema's Markdown shape, with a small front-matter block the publisher reads:

  ```
  ---
  issue_type: Story
  parent: <epic summary or JIRA-KEY>
  components: [case-explorer, exports]
  labels: [analyst-tools]
  estimate: 3
  status: draft        # publisher flips this to "created: <KEY>" after pushing
  duplicate_of:        # set if dedup flagged one
  ---
  ```

- `INDEX.md` — the human's review cockpit:
  - a one-line banner: **"Nothing here is in Jira yet. Review, then approve to publish."**
  - the decomposition tree from step 1,
  - a per-ticket **critique log** (weakest INVEST dimension found + what the one revision
    changed, or "no change needed"; any duplicate flags),
  - an **approval checklist** the human ticks before `publish-to-jira` runs.

## Constraints

- **Never write to Jira.** Dedup is read-only; publishing is gated and lives in another skill.
- One revision pass — targeted fixes, not infinite polish.
- One ticket per file. The separated-files layout *is* the review mechanism — keep it.
- If the profile is thin or low-confidence on something, draft conservatively and note the
  assumption in the ticket rather than inventing team process.
