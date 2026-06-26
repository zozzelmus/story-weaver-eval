# tickets-review/ — drafted tickets land here (the review gate)

`draft-tickets` writes one subdirectory per feature, `tickets-review/<FEATURE-KEY>/`, containing:

- `_context.md` — the brief `gather-context` produced (the feature + the source it touches).
- `NN-<slug>.md` — **one file per ticket**, each with a front-matter block (`issue_type`,
  `parent`, `components`, `labels`, `estimate`, `status`, `duplicate_of`) and the human-readable
  ticket below it.
- `INDEX.md` — the review cockpit: the decomposition tree, the per-ticket critique log, and an
  approval checklist.

**Nothing in here is in Jira until you approve it.** Review and edit the files — they are the
source of truth — then tell the agent `publish <FEATURE-KEY>`. `publish-to-jira` reads exactly
what's here, creates the issues under the feature, and writes the new Jira keys back into the
front-matter (`status: created: <KEY>`), so a re-run never double-creates.

Committing these dirs is handy — your review becomes a PR diff, and the published keys give you
a permanent record of what was created from what.
