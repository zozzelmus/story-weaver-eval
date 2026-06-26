# Story Weaver Eval

A no-API-key, runs-entirely-inside-Copilot harness for testing one question:

> **Does grounding + decomposition + critique actually produce better Jira tickets than a single LLM call?**

It does this as an **ablation study** — four generator variants (V0→V3), each adding exactly
one capability, scored by an INVEST judge against tickets your team already wrote by hand.

There is no scripted model call anywhere. Generation and judging both run through **Copilot
agent mode**, so your Copilot subscription is the only model access required. The only Python
in here (`scripts/aggregate.py`) just tallies JSON result files — it never calls a model.

---

## The variant ladder

| Variant | Skill                  | Adds                                              |
|---------|------------------------|---------------------------------------------------|
| **V0**  | `gen-v0-singleshot`    | nothing — "here's the feature, write tickets". This *is* current Story Weaver. The baseline. |
| **V1**  | `gen-v1-grounded`      | retrieval: pulls similar real tickets/epics (Jira MCP, or the `corpus/` folder as fallback) and uses them as exemplars |
| **V2**  | `gen-v2-decomposed`    | an explicit, inspectable epic→story tree before drafting |
| **V3**  | `gen-v3-critic`        | a generate→critique(INVEST + Jira dedup)→revise loop |

The hypothesis is that **V0→V1 is the single biggest jump** — that most of "Story Weaver
output doesn't look like ours" is a *grounding* problem, not an agentic-reasoning problem.
If V1 alone closes most of the gap, that's a genuinely useful negative result: maybe the
rebuild just needs real RAG, not a full pipeline. A cheap finding that saves a quarter of
build is a win.

---

## Prerequisites

- **VS Code 1.120+** with GitHub Copilot, **agent mode** enabled (`chat.agent.enabled`).
- Skills support (1.120 stable). This repo's skills live in `.github/skills/`; Copilot
  also auto-discovers `.claude/skills/` if you'd rather symlink them there.
- **A Jira MCP server connected to Copilot** (for V1 grounding and V3 dedup). This is
  bring-your-own-*tool*, not bring-your-own-model-key — usually a much lighter approval.
  V1/V3 fall back to the `corpus/` files if no Jira MCP is present, so you can still run
  the whole ladder without it (just with weaker grounding).
- **Two models available in the Copilot model picker.** You generate with one and judge
  with another — see "The self-bias problem" below. If you only have one, the experiment
  still runs but the judge numbers are softer.

> The skills reference Jira MCP capabilities generically (e.g. "search issues by JQL",
> "read an epic's children"). Different Jira MCP servers name their tools differently.
> If your agent can't bind a capability, open the relevant `SKILL.md` and replace the
> capability description with your server's actual tool name. This is the one place you'll
> likely need to adjust for your environment.

---

## How to run it (≈ tomorrow morning)

1. **Clone and open** the folder in VS Code. Open the Chat view, select **Agent**.

2. **Populate the test set.** Each test case is a pair:
   - `features/<CASE-ID>.md` — the raw requirement (what goes *into* the tool)
   - `reference-tickets/<CASE-ID>.md` — the tickets your team actually wrote (the ground truth the judge compares against)

   One worked pair (`EXAMPLE-0001-bulk-export`) ships in the repo so you can see the format
   and do a smoke-test immediately. Aim for **~15 pairs** for a directional read.

3. **Populate the grounding corpus.** Drop *well-written past tickets* into `corpus/`.
   **These must be DIFFERENT tickets from `reference-tickets/`** — see the leakage rule below.
   Two example exemplars ship in the repo. If you're grounding against live Jira via MCP,
   the corpus is a supplementary seed; if not, it's the whole grounding pool.

4. **Run a variant for a case.** In agent chat:
   ```
   /gen-v0-singleshot  using features/EXAMPLE-0001-bulk-export.md, write the result to results/EXAMPLE-0001-bulk-export.v0.tickets.md
   ```
   Then the same for `/gen-v1-grounded`, `/gen-v2-decomposed`, `/gen-v3-critic`.
   (Or use the orchestrator agent — see below — to run all four for a case in one go.)

5. **Switch the model**, then judge. Change the model in the picker to your *judge* model, then:
   ```
   /invest-judge  compare results/EXAMPLE-0001-bulk-export.v1.tickets.md against reference-tickets/EXAMPLE-0001-bulk-export.md, write scores to results/EXAMPLE-0001-bulk-export.v1.json
   ```
   The judge runs in a **forked context** (set in its frontmatter) so the generation
   reasoning doesn't leak into the scoring.

6. **Tally.** When you've got JSON results in `results/`:
   ```
   python scripts/aggregate.py
   ```
   It prints mean case score per variant, mean per-INVEST-dimension, and the
   reference-comparison win rate per variant. Stdlib only — no pip, no key.

### Or let the orchestrator drive it

`.github/agents/ticket-eval.agent.md` is an agent that, given a case ID, runs all four
generators and then judges each — pausing for you to switch the model before the judging
phase. Use it once you've smoke-tested the skills individually and trust them.

---

## ⚠️ The leakage rule (read this or your numbers lie)

A ticket used as a **grounding exemplar** (`corpus/`) must **never** also be a **held-out
reference** (`reference-tickets/`). If the model is shown the answer as an exemplar, V1+ will
look brilliant for the wrong reason and your whole conclusion is invalid. Keep the two folders
strictly disjoint. The folder split is the mechanism that enforces this — don't defeat it.

---

## The self-bias problem (the one real wound of running this in Copilot)

Generator and judge would normally be the same underlying model, and a model tends to like
its own output. Three mitigations, in order of strength:

1. **Generate with one model, judge with another.** 1.120's model picker makes this a two-click
   switch. This is the strongest fix and costs nothing — do it.
2. **Judge reference-based, not reference-free.** The judge always sees the human ticket as the
   anchor and answers "which is better"; anchoring to ground truth is far harder to game than a
   bare 1–5.
3. **Calibrate the judge yourself.** Before trusting any number, hand-score 3–4 tickets and
   confirm the judge agrees with you. A miscalibrated judge makes the whole run worthless.

## Other honest caveats

- **Small n.** ~15 cases is *directional*, not gospel. Run each case twice and treat the
  spread as the error bar. Don't present a 0.2-point gap as a finding.
- **Reproducibility.** Chat is less reproducible than a script. The skills are committed
  (fixed instructions = fixed behavior); also **record which model backed each run** — the
  judge writes `model_generator` / `model_judge` into each result JSON for exactly this reason.
- **Model drift.** Copilot's underlying model can change under you. The recorded model IDs are
  your audit trail.

---

## What this gets you

The repo is simultaneously the **proof-of-concept** and the **regression bar**. The same
INVEST rubric drives both the V3 critic loop and the judge — one definition of "good," used
to build *and* to measure. And you produced it without filing a single model-key request.

## Layout

```
story-weaver-eval/
├── README.md                  ← you are here
├── .github/
│   ├── agents/
│   │   └── ticket-eval.agent.md
│   └── skills/
│       ├── gen-v0-singleshot/SKILL.md
│       ├── gen-v1-grounded/SKILL.md
│       ├── gen-v2-decomposed/SKILL.md
│       ├── gen-v3-critic/SKILL.md
│       └── invest-judge/SKILL.md
├── schema/ticket-schema.md    ← the Jira ticket shape every variant targets
├── features/                  ← held-out raw requirements (test inputs)
├── reference-tickets/         ← human-written tickets (ground truth)
├── corpus/                    ← grounding exemplars (MUST be disjoint from reference-tickets)
├── results/                   ← generated tickets + judge JSON land here
└── scripts/aggregate.py       ← tallies results/*.json (no model calls)
```
