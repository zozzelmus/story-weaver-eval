---
name: gather-context
description: Gather everything needed to draft tickets for one feature — read the target feature from Jira (description, acceptance criteria, comments, linked issues, attachments) and pull the relevant source code and local samples that ground it in technical reality. This is the agent's information-gathering tool, chained before draft-tickets. Use whenever asked to gather context for a feature, pull a Jira feature plus its code, or prepare grounding for ticket drafting.
---

# gather-context — grab the feature and its code

The drafter is only as good as what it's grounded in. This skill is the **tool the agent
chains** to go out and collect the two things drafting needs: **what the feature is** (from
Jira) and **the technical reality it lands in** (from the source code). Read-only.

## Inputs

```
/gather-context feature=<JIRA-FEATURE-OR-EPIC-KEY> [code=<path-or-glob>...] [brief=<local-file>]
```

- `feature` — the Jira feature/epic to break down. The primary input.
- `code` — repo paths/globs that the feature touches (optional but strongly preferred — it's
  what makes the tickets technically real).
- `brief` — optional local requirement file (e.g. under `features/`) if the ask isn't fully in
  Jira yet, or for offline runs.

## Steps

### 1. Read the feature from Jira

Capability: **"get a Jira issue"**, **"list an issue's links / children / comments"**,
**"read an issue's attachments"**. Capture:

- The full **description** and any acceptance criteria already on the feature.
- **Comments** — refinement discussion often holds the real constraints and decisions.
- **Linked issues / children** — what already exists, what this depends on or blocks (so the
  drafter doesn't re-create existing work).
- **Attachments / samples** — payloads, mockups, or data shapes referenced by the feature.

### 2. Pull the relevant source code

For each `code` path/glob, read enough to answer:

- What **components/modules** does this feature actually touch? (These should map to the Jira
  components the profile knows about.)
- What are the existing **patterns, names, and seams** the work will extend — so stories
  reference real modules, not invented ones?
- Are there obvious **technical constraints or edges** (auth boundaries, queues, external
  systems, data contracts) the AC must cover?

Use the repo's own samples too when present (e.g. `samples/` holds representative payloads for
the worked example) — concrete data shapes make AC specific instead of hand-wavy.

### 3. Produce a context brief

Write a short, structured **context brief** to `tickets-review/<FEATURE-KEY>/_context.md`:

- the feature's intent and scope (and explicit out-of-scope),
- the technical surfaces it touches (with `path:line` references to real code),
- known constraints, edges, and dependencies,
- open questions / scope ambiguities to flag for the drafter (and ultimately the human).

This brief is the hand-off to `draft-tickets`. Keep it factual — gather, don't decide the
decomposition here.

## Constraints

- **Read-only** everywhere — Jira, the repo, samples. This skill never writes to Jira.
- Don't invent technical detail. If the code doesn't show something, record it as an open
  question rather than guessing.
- Stay scoped to the feature. Pulling the entire codebase is noise; pull what the feature
  touches.
