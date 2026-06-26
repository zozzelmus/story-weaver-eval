---
name: gen-v3-critic
description: Generate Jira tickets with the full pipeline — ground, decompose, draft, then run a critique loop that scores each ticket against INVEST and checks for duplicates in the existing Jira backlog, revising once. This is the V3 variant for the Story Weaver ablation eval — it adds a CRITIQUE-AND-REVISE loop on top of the decomposed V2 variant. Use this skill when asked to run V3, the critic generator, or the full pipeline for a Story Weaver eval case.
---

# V3 — Critic generator (full pipeline)

V3 = V2 (grounded + decomposed) **plus a critique loop**. Generate → critique against INVEST
and check for backlog duplicates → revise once. This is the cheapest large quality jump and
the thing naive tools never do.

Add the critique loop. Keep grounding (V1) and the decomposition tree (V2).

## Steps

1. **Ground** (as V1) and **decompose** (as V2): produce the epic→story tree, then draft an
   initial set of tickets per `schema/ticket-schema.md`. Don't write the file yet.

2. **Critique.** For every drafted ticket, evaluate:

   **INVEST** — score each 1–5 and note the weakest dimension:
   - *Independent* — does it depend on other unfinished stories? (Horizontal slices fail here.)
   - *Negotiable* — is it a need, or an over-specified implementation dump?
   - *Valuable* — does it deliver observable user/business value as a vertical slice?
   - *Estimable* — could the team size it as written?
   - *Small* — does it fit in a sprint? If not, split it.
   - *Testable* — are the Given/When/Then criteria concrete and verifiable?

   **Acceptance-criteria completeness** — are the main happy path AND the obvious edge/error
   cases covered, or only the happy path?

   **Duplicate check** — does this story already exist in the backlog?
   - With a Jira MCP connected: search the backlog by summary keywords / JQL for near-duplicates
     (capability: "search Jira issues by JQL"). If a strong match exists, flag it and prefer
     referencing the existing issue over creating a near-twin.
   - Without a Jira MCP: check against `corpus/` for an obvious existing equivalent.

3. **Revise once.** Rewrite any ticket scoring ≤3 on any INVEST dimension, or with thin AC, or
   flagged as a likely duplicate. Split stories that fail *Small*. Targeted fixes — not a blind
   regenerate. Do exactly one revision pass (the eval measures the loop, not infinite polish).

4. Write the result to `results/<CASE-ID>.v3.tickets.md`. At the top, include:
   - the decomposition tree (from V2), then
   - a short **critique log**: per ticket, the weakest INVEST dimension found and what the
     revision changed (or "no change needed"), and any duplicate flags.

   The critique log is part of what V3 is demonstrating — keep it.

## Constraints

- Exactly one revision pass.
- Keep grounding and the decomposition tree.
- Duplicate checks are **read-only**; never create or modify Jira issues.
- Never read `reference-tickets/`.
