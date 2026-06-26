# Self-Learning Ticket Agent

A no-API-key, runs-entirely-inside-Copilot agent that **learns how your team writes tickets**,
then breaks a feature down into draft tickets that look like your team wrote them — for you to
review and approve before anything is pushed to Jira.

> **learn → gather → draft → [you review] → publish**

There is no model key and no separate runtime. Learning, drafting, and (gated) publishing all
run through **Copilot agent mode** with Markdown *skills*, so your Copilot subscription is the
only model access required. The agent reaches Jira, Confluence, and your source through tools
(MCP + the repo) — it never calls a model itself.

---

## What it does

| Step | Skill | What happens |
|------|-------|--------------|
| **Learn** | `learn-team` | Deep self-learning: read the team's **working agreement** (a Confluence page), scan the **whole Jira project** (epics, stories, components, labels, estimation, glossary), and study **one existing feature's** decomposition. Persist it all to `profile/team-profile.md`. |
| **Gather** | `gather-context` | Read the target **feature from Jira** (description, AC, comments, links, attachments) and the relevant **source code**, into a context brief. |
| **Draft** | `draft-tickets` | Decompose the feature into vertical slices and draft tickets **in the team's voice**, one Markdown file per ticket in `tickets-review/<FEATURE>/`. A light INVEST self-check + read-only backlog dedup. Nothing is in Jira yet. |
| **Publish** | `publish-to-jira` | **The single gated write path.** After you review and approve the files, create the tickets in Jira **attached to the feature**, reusing components/labels/estimates. Idempotent. |

The `ticket-agent` orchestrator **chains these skills like tools** and stops at the review gate.

---

## Why Copilot (and not the Claude Agent SDK)

The SDK would give you enforced write-gating, subagents-as-tools, and a place to persist
learning — but it needs Anthropic **API access** (a key, or Amazon Bedrock / Google Vertex /
Azure). With no token, the SDK can't run, so we stay in **Copilot agent mode** and emulate the
two things that matter:

- **The write-gate is procedural.** Only `publish-to-jira` writes, and only after you explicitly
  approve the reviewed files. Everything else is read-only by construction.
- **Learning is persisted to a file.** `profile/team-profile.md` *is* the memory — committed,
  human-readable, and editable.

The skill *content* is model-agnostic. If you later get Bedrock/Vertex access, the same skills
drop onto a thin Agent SDK harness with a real enforced gate — this isn't a dead end.

---

## Prerequisites

- **VS Code 1.120+** with GitHub Copilot, **agent mode** enabled (`chat.agent.enabled`), and
  Skills support (1.120 stable). Skills live in `.github/skills/`; Copilot also auto-discovers
  `.claude/skills/` if you prefer to symlink them.
- **A Jira MCP server connected to Copilot** — used read-only for learning, gathering, and
  dedup, and read-write only by `publish-to-jira` behind the gate. Without it, the agent falls
  back to local files (`corpus/`, `features/`) and can't publish.
- **A Confluence MCP (or any "fetch this page" tool)** for `learn-team` to read the working
  agreement. Optional — you can also paste the agreement into the profile by hand.

> The skills reference MCP capabilities generically (e.g. "search Jira issues by JQL", "create a
> Jira issue", "fetch a Confluence page"). Different MCP servers name their tools differently. If
> a capability won't bind, open the relevant `SKILL.md` and swap in your server's actual tool
> name — that's the one place you'll likely adjust for your environment.

---

## How to run it

1. **Clone and open** the folder in VS Code. Open the Chat view, select **Agent**.

2. **Teach it your team (once).** This is the deep self-learning step — give it your working
   agreement and project key:
   ```
   /learn-team confluence=https://your.wiki/working-agreement project=TM exemplar=TM-77
   ```
   It writes `profile/team-profile.md`. **Read it** — correct anything it got wrong; it's the
   memory every draft is built from. Re-run it when the team changes how it works, not every time.

3. **Break down a feature.** Point the orchestrator at a Jira feature:
   ```
   Use ticket-agent to break down TM-128. Code is in src/transport/**.
   ```
   It gathers the feature + code, then drafts to `tickets-review/TM-128/` — one file per ticket,
   plus `INDEX.md` with the decomposition tree, critique log, and an approval checklist.

4. **Review the gate.** Open `tickets-review/TM-128/`. Edit the files freely — they are the
   source of truth. Nothing is in Jira yet.

5. **Publish when happy.**
   ```
   publish TM-128
   ```
   `publish-to-jira` restates exactly what it will create, waits for your go, then creates the
   tickets under the feature and writes the new Jira keys back into the files.

You can also run the skills individually (`/gather-context`, `/draft-tickets`, …) instead of the
orchestrator.

---

## The review gate (the one rule that matters)

Drafting writes **files**, not Jira issues. `publish-to-jira` is the only skill that writes, and
it will not create anything until you explicitly approve the reviewed set. The separated
one-file-per-ticket layout exists so the review is a real, line-by-line read (review it like a
PR diff). Don't wire any other skill to write to Jira — keep the single gated path.

---

## Honest caveats

- **The profile is the whole game.** A profile learned from a broad scan of real, closed stories
  produces drafts that sound like your team; a thin profile produces generic tickets. Invest in
  the first `learn-team` run, and read what it wrote.
- **Reproducibility.** Chat is less reproducible than a script. The skills are committed (fixed
  instructions = fixed behavior), and the profile is committed (fixed grounding) — together
  that's most of the determinism you can get in Copilot.
- **Model drift.** Copilot's underlying model can change under you. Nothing here pins it.
- **Gate discipline.** The write-gate is procedural, not enforced by a runtime. The skills are
  written to honor it, but *you* are the actual gate — review before you say "publish".

---

## Layout

```
.
├── README.md                       ← you are here
├── .github/
│   ├── agents/
│   │   └── ticket-agent.agent.md    ← orchestrator: chains the skills, stops at the gate
│   └── skills/
│       ├── learn-team/SKILL.md      ← deep self-learning → profile/team-profile.md
│       ├── gather-context/SKILL.md  ← read the Jira feature + source code
│       ├── draft-tickets/SKILL.md   ← feature → one md per ticket (review dir)
│       └── publish-to-jira/SKILL.md ← the single gated write path
├── profile/
│   ├── team-profile.template.md     ← the shape learn-team fills in
│   └── team-profile.md              ← the persisted learned conventions (created on first run)
├── schema/ticket-schema.md          ← the ticket shape; INVEST quality bar
├── tickets-review/                  ← drafted tickets land here, one dir per feature
├── features/                        ← optional local feature briefs (offline / worked examples)
├── samples/                         ← representative data payloads for the worked example
└── corpus/                          ← optional offline exemplars (fallback grounding)
```
