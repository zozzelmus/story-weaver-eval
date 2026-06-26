---
name: gen-v2-decomposed
description: Generate Jira tickets by first producing an explicit, inspectable epic-to-story decomposition tree with rationale, then drafting grounded tickets from that tree. This is the V2 variant for the Story Weaver ablation eval — it adds an EXPLICIT DECOMPOSITION step on top of the grounded V1 variant. Use this skill when asked to run V2, the decomposed generator, or to test whether a visible decomposition step improves ticket quality for a Story Weaver eval case.
---

# V2 — Decomposed generator

V2 = V1 (grounded) **plus an explicit decomposition step**. Single-shot tools skip the
reasoning where feature → epics → stories actually happens; V2 makes it a real, visible stage.

Add the decomposition tree. Keep grounding from V1. Do not add the critique loop (that's V3).

## Steps

1. Read the feature requirement (under `features/`) and `schema/ticket-schema.md`.
2. **Ground** exactly as V1 does — Jira MCP preferred, `corpus/` fallback. (Read
   `.github/skills/gen-v1-grounded/SKILL.md` if you need the grounding detail; don't duplicate it.)
3. **Decompose — emit the tree first.** Before drafting any ticket, produce an explicit tree:

   ```
   Feature: <name>
   ├── Epic A: <summary>   — rationale: <why this is a coherent epic>
   │   ├── Story A1: <summary>   — rationale: <the user value this slice delivers>
   │   └── Story A2: <summary>   — rationale: ...
   └── Epic B: <summary>   — rationale: ...
       └── Story B1: <summary>   — rationale: ...
   ```

   Rules for the tree:
   - **Slice vertically, by deliverable user value** — not horizontally by layer
     (avoid a "database story", an "API story", a "UI story"). Each story should be
     demonstrable on its own.
   - Each node carries a one-line **rationale**. The rationale is the "reasoning" that
     single-shot tools lack — make it real, not decorative.
   - Prefer fewer, well-formed stories over many thin ones.

4. **Draft from the tree.** Expand each leaf into a full ticket per the schema (description,
   Given/When/Then acceptance criteria, epic link, grounded components/labels).
5. Write the result to `results/<CASE-ID>.v2.tickets.md`. **Include the tree at the top of the
   output**, above the tickets — its visibility is part of what V2 is testing.

## Constraints

- The tree must precede the tickets and must show rationale per node.
- Keep V1 grounding; don't drop it.
- No critique/revision/dedup pass yet — that's V3.
- Never read `reference-tickets/`.
