---
name: gen-v0-singleshot
description: Generate Jira tickets from a feature requirement in a single shot, with no grounding, no decomposition step, and no critique. This is the BASELINE variant for the Story Weaver ablation eval — it deliberately mimics naive "feature in, tickets out" tools. Use this skill when asked to run V0, the single-shot variant, or the baseline generator for a Story Weaver eval case.
---

# V0 — Single-shot generator (baseline)

This is the **control**. It is intentionally minimal so that V1–V3 can show what each added
capability is worth. Do **not** improve it, ground it, or add reasoning steps — that would
contaminate the experiment. Its whole job is to represent "current Story Weaver".

## Steps

1. Read the feature requirement file the user named (under `features/`).
2. Read `schema/ticket-schema.md` for the output format only.
3. In a single pass, write Jira tickets that cover the requirement.
4. Write the result to the output path the user gave (typically
   `results/<CASE-ID>.v0.tickets.md`), following the schema's Markdown format.

## Constraints (important — keep the baseline honest)

- **No retrieval.** Do not search Jira, do not read `corpus/`, do not look at other tickets.
- **No explicit decomposition.** Don't produce a separate epic→story tree; just write tickets.
- **No self-critique.** Write them once. Do not revise against INVEST or check for duplicates.
- Do not read `reference-tickets/` — that's the answer key.

Produce a reasonable-but-ungrounded result. That's the point: it's the floor we measure from.
