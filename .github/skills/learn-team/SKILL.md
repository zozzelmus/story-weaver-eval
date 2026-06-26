---
name: learn-team
description: Deep self-learning step. Learn how a specific team works by reading their working agreement (a Confluence page), scanning an entire Jira project's epics and stories, and observing how one existing feature was decomposed — then persist everything into profile/team-profile.md so later drafting runs imitate the team's real conventions. Use this whenever asked to learn a team/project, ingest a working agreement, study how a team writes tickets, refresh the team profile, or before drafting tickets for a project the agent hasn't learned yet.
---

# learn-team — deep self-learning

This is the **self-learning core**. Everything the drafter does later is only as good as the
profile this skill produces. The goal is not to draft anything here — it is to *learn how this
team works* and write that knowledge down so it persists across runs.

You learn from three sources, in order, and merge them into one **team profile**:

1. the team's **working agreement** (a Confluence page the user gives you),
2. the team's **whole Jira project** (scan the backlog broadly — epics, stories, conventions),
3. **one existing feature**, observed end-to-end (how was it actually decomposed?).

Everything you do here is **read-only**. This skill never creates or edits Jira issues.

## Inputs (the user's initial `/prompt`)

Invoked like:

```
/learn-team confluence=<working-agreement-URL> project=<JIRA-PROJECT-KEY> [exemplar=<FEATURE-OR-EPIC-KEY>]
```

- `confluence` — URL of the working agreement / team norms page. Required for a first run.
- `project` — the Jira project key to scan (e.g. `TM`, `CASE`).
- `exemplar` — optional: a feature/epic the team already broke down well, to study closely.
  If omitted, pick the most complete-looking recent epic yourself during the scan.

## Steps

### 1. Read the working agreement (Confluence)

Fetch the page the user linked (capability: **"fetch/read a Confluence page by URL or page ID"**).
Extract and note:

- **Definition of Ready** and **Definition of Done**.
- Story conventions — preferred summary voice ("As a… I want…" vs imperative), AC format
  (Given/When/Then vs checklist), required fields.
- Estimation scheme (story points / Fibonacci / t-shirt) and what a "1" vs a "5" means here.
- Workflow states and any required ceremonies (refinement, sizing rules, sprint length).
- Any explicit rules about slicing, splitting, spikes, or what *not* to do.

> If the working agreement spans multiple linked pages, follow the obviously-relevant child
> links (e.g. "Definition of Done", "Estimation guide") — but don't crawl the whole wiki.

### 2. Scan the whole project (Jira) — this is the deep part

Using the Jira MCP (capability: **"search Jira issues by JQL"**, **"get a Jira issue"**,
**"list project components / labels / issue types"**):

- Pull a broad, representative sample of the project's **Stories** — recent ones, and a few
  older well-regarded ones. Aim for ~20–40 issues so conventions are statistically real, not
  one person's style. Prefer Done/closed stories (they reflect what "good" converged to).
- Read enough of them in full to learn the **house style**: how summaries are phrased, how
  thick the descriptions are, the exact AC shape, how many AC per story is normal.
- Capture the project's **epics** (the real structure work rolls up into), **components**, and
  **labels** actually in use — with rough frequencies, so the drafter reuses common ones and
  doesn't invent new ones.
- Note the **estimation distribution** (what point values actually appear) and any **priority**
  usage pattern.
- Build a small **domain glossary** of recurring project-specific terms and systems (e.g. the
  names of internal services, feeds, gateways) — these are how you'll later sound like an
  insider rather than a generic generator.

> Different Jira MCP servers name these tools differently. If a capability won't bind, open this
> file and replace the capability phrase with your server's actual tool name. The intent is
> fixed: search the backlog, read a representative sample, learn epics/components/labels/scale.

### 3. Observe one feature end-to-end

Take the `exemplar` (or the best epic you found) and study **how it was decomposed**:

- What were its child stories, and how was the feature sliced — vertically by user value, or
  some house pattern? How big was each slice?
- How did AC granularity, components, and labels flow from epic down to story?
- What's the *shape* of a good decomposition on this team? This is the template the drafter
  will imitate.

### 4. Persist the profile (the self-learning output)

Write everything to `profile/team-profile.md`, following `profile/team-profile.template.md`.

- If the file already exists, **update it incrementally** — merge new observations, refresh
  stale lists, and bump the "Last learned" provenance block (what you scanned, project, date,
  issue count). Don't blindly overwrite hard-won notes; reconcile.
- Record **provenance and confidence**: which conventions you saw consistently (high
  confidence) vs inferred from few examples (low confidence). The drafter should know what's
  solid.
- Keep 2–3 links to genuinely exemplary real tickets you observed, as touchstones.

The profile is the memory. A good profile means the next `draft-tickets` run produces tickets
that look like the team wrote them — without re-scanning every time.

## Constraints

- **Read-only.** Never create, edit, transition, or comment on Jira issues here.
- Learn *conventions and structure*, not content to copy. You are learning the team's voice,
  not memorizing specific stories to regurgitate.
- If no Jira MCP is reachable, fall back to the offline exemplars in `corpus/` and say so in the
  profile's provenance block (the profile will be weaker — note that honestly).
- Don't fabricate a Definition of Done or estimation scale you didn't actually find. Mark
  unknowns as unknown so the drafter doesn't invent process.
