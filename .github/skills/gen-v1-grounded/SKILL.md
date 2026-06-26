---
name: gen-v1-grounded
description: Generate Jira tickets from a feature requirement, grounded in similar real tickets, epics, components and labels retrieved from Jira (via MCP) or the local corpus folder. This is the V1 variant for the Story Weaver ablation eval — it adds RETRIEVAL on top of the V0 baseline and nothing else. Use this skill when asked to run V1, the grounded generator, or to test whether grounding alone improves ticket quality for a Story Weaver eval case.
---

# V1 — Grounded generator

V1 = V0 **plus retrieval**. The hypothesis under test is that most of "the output doesn't
look like ours" is a grounding problem. So this variant's only addition is: before drafting,
gather real exemplars and conventions, and use them as few-shot context.

Add retrieval. Add nothing else (no separate decomposition tree, no critique loop).

## Steps

1. Read the feature requirement file the user named (under `features/`).
2. Read `schema/ticket-schema.md` for the output format.
3. **Ground.** Gather exemplars and conventions, preferring Jira MCP, falling back to `corpus/`:

   **If a Jira MCP server is connected (preferred):**
   - Search for issues similar to the feature using JQL on keywords / summary terms
     (capability: "search Jira issues by JQL"). Pull the 5–10 most relevant Stories.
   - For the most relevant matches, read the issue to capture how summaries, descriptions,
     and acceptance criteria are actually written on this project (capability: "get a Jira issue").
   - Capture the **epics**, **components**, and **labels** in use, so drafted tickets link to
     real epics and reuse real labels rather than inventing them (capability: "list/read epics
     and project components").

     > If your Jira MCP names these tools differently, replace the capability phrases above
     > with your server's actual tool names. The intent is: find similar tickets, read a few,
     > learn the project's epics/components/labels.

   **If no Jira MCP is connected (fallback):**
   - Read the files in `corpus/`. Select the 5–10 exemplars most similar to the feature.
   - Treat their structure, acceptance-criteria style, components, and labels as the conventions.

4. **Draft, grounded.** Write tickets that imitate the *form* of the retrieved exemplars —
   their summary phrasing, AC granularity, the components/labels/epics they use — while
   covering the new feature's content. Link stories to a real epic when grounding surfaced one.
5. Write the result to the output path (typically `results/<CASE-ID>.v1.tickets.md`).

## Constraints

- Imitate the *form and conventions* of exemplars; never copy an exemplar's *content*.
- Do **not** read `reference-tickets/` — that's the answer key, and reading it is leakage.
- No explicit epic→story tree step (that's V2). No critique/dedup loop (that's V3).
