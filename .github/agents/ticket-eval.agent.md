---
name: ticket-eval
description: Orchestrates a full Story Weaver ablation run for one eval case — runs the V0–V3 generators, then judges each output against the human reference, pausing for a model switch before judging.
tools:
  - codebase
  - editFiles
---

# Story Weaver Eval Orchestrator

Runs one complete eval case end to end. Use this **after** you've smoke-tested the individual
generator and judge skills and trust them. Drive it with a case ID, e.g.
"run the eval for EXAMPLE-0001-bulk-export".

## What you do, given a CASE-ID

### Phase 1 — Generate (run with the GENERATOR model)

For the given case, run each generator variant in turn, writing each to `results/`:

1. Apply the **gen-v0-singleshot** skill → `results/<CASE-ID>.v0.tickets.md`
2. Apply the **gen-v1-grounded** skill → `results/<CASE-ID>.v1.tickets.md`
3. Apply the **gen-v2-decomposed** skill → `results/<CASE-ID>.v2.tickets.md`
4. Apply the **gen-v3-critic** skill → `results/<CASE-ID>.v3.tickets.md`

Input for all four is `features/<CASE-ID>.md`. Do **not** read `reference-tickets/` during
generation — it's the answer key.

### Phase 2 — Pause for model switch

Stop and tell the user, in these words:

> Generation done for **<CASE-ID>** (v0–v3 in `results/`). **Switch the Copilot model picker
> to your judge model now**, then say "judge it" so the scoring uses a different model than
> generation. (If you only have one model, say "judge anyway" — but the scores will be softer.)

Wait for the user. Do not proceed to judging on your own.

### Phase 3 — Judge (run with the JUDGE model)

For each variant v0–v3, apply the **invest-judge** skill, comparing
`results/<CASE-ID>.<variant>.tickets.md` against `reference-tickets/<CASE-ID>.md`, writing
`results/<CASE-ID>.<variant>.json`.

### Phase 4 — Wrap up

Tell the user to run `python scripts/aggregate.py` once they've done enough cases, and remind
them ~15 cases gives a directional read, not a verdict.

## Rules

- Never read `reference-tickets/` during Phase 1.
- Keep the model-switch pause real — it's the main bias control.
- Don't create or modify Jira issues; any Jira MCP use here is read-only.
