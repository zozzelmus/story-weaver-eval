---
name: invest-judge
description: Score a generated set of Jira tickets against the INVEST rubric and compare them to the human-written reference tickets, emitting a structured JSON result. This is the JUDGE for the Story Weaver ablation eval — it produces the quantitative scores that let you compare V0/V1/V2/V3. Use this skill whenever asked to judge, score, grade, or evaluate generated tickets for a Story Weaver eval case, or to compare a variant's output against the reference tickets.
context: fork
---

# INVEST Judge

Scores one variant's output for one case, against the human reference, and writes a JSON
result file that `scripts/aggregate.py` can tally. This skill runs in a **forked context**
(see frontmatter) so the generator's reasoning never leaks into the scoring.

This rubric is the single source of truth for "good" — the same definition the V3 critic
loop uses. Generate and measure off one bar.

## Before you score — guard against bias

1. **Judge with a different model than generated**, if available. (Switch the Copilot model
   picker before invoking this skill.) Record both model IDs in the output.
2. **Anchor to the reference.** You are always comparing the generated tickets to the
   human-written ones — not rating in a vacuum.
3. If the user is calibrating you, they may hand-score a case too; expect your numbers to be
   checked against theirs. Score honestly, not generously.

## Inputs

- The generated tickets file (e.g. `results/<CASE-ID>.v1.tickets.md`).
- The human reference (`reference-tickets/<CASE-ID>.md`) — the ground truth.
- `schema/ticket-schema.md` for the field/format expectations.

## Steps

1. Read the generated file and the reference file.
2. For **each generated ticket**, score the six INVEST dimensions 1–5 using the anchors below,
   plus AC completeness, epic-link correctness, and a duplicate flag.
3. Make the **reference comparison**: holistically, are the generated tickets better than,
   worse than, or about equal to the human set for this feature? This is the most important
   single signal — anchor it to concrete differences, not vibes.
4. Compute the case score (mean of per-ticket means).
5. Write the JSON below to the output path (e.g. `results/<CASE-ID>.v1.json`). Emit **only**
   valid JSON in the file — no prose, no Markdown fences.

## INVEST scoring anchors (1–5)

- **5** — exemplary; a senior PM would ship as-is.
- **4** — solid; minor nits.
- **3** — usable but flawed on this dimension.
- **2** — clearly deficient; needs rework.
- **1** — fails the dimension outright.

Specific failure cues:
- *Independent* ≤2 if the story is a horizontal layer (DB-only / API-only / UI-only) that
  can't be demonstrated alone.
- *Valuable* ≤2 if no observable user/business value, or it's a technical task masquerading
  as a story.
- *Testable* ≤2 if acceptance criteria are missing, vague, or not Given/When/Then-shaped.
- *Small* ≤2 if it plainly can't fit in a sprint and wasn't split.

## Output JSON schema

```json
{
  "case_id": "EXAMPLE-0001-bulk-export",
  "variant": "v1",
  "model_generator": "<model that produced the tickets, or 'unknown'>",
  "model_judge": "<model running this judge>",
  "tickets": [
    {
      "ticket_index": 1,
      "summary": "<the generated ticket's summary>",
      "invest": {
        "independent": 4,
        "negotiable": 3,
        "valuable": 5,
        "estimable": 4,
        "small": 3,
        "testable": 5
      },
      "ac_completeness": 4,
      "epic_link_correct": true,
      "duplicate_of": null,
      "weakest_dimension": "small",
      "notes": "<1-2 sentences: the most important strength or flaw>"
    }
  ],
  "reference_comparison": {
    "winner": "generated | human | tie",
    "margin": "slight | clear",
    "rationale": "<what concretely made the difference>"
  },
  "case_score": 4.0
}
```

`case_score` = mean across tickets of (mean of the six INVEST scores). Round to one decimal.
`duplicate_of` is null or the key/summary of the existing ticket it duplicates.
