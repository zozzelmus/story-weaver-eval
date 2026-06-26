# profile/ — the team's learned conventions (persisted memory)

This directory is the agent's **self-learning memory**. `learn-team` writes
`team-profile.md` here; `draft-tickets` reads it back so generated tickets imitate how *this*
team actually writes them — without re-scanning Jira every run.

Because we run in Copilot agent mode (no API key, no SDK runtime), there's no built-in
cross-run memory. This file **is** the memory: a committed, human-readable, editable record of
what the agent has learned. That's a feature — you can read it, correct it, and see exactly why
the drafter does what it does.

## Files

- `team-profile.template.md` — the shape `learn-team` fills in. Don't edit the template to
  record real conventions; let `learn-team` produce `team-profile.md` from it.
- `team-profile.md` — the live profile (created on first `/learn-team` run). Edit it freely to
  correct or augment what the agent learned; `learn-team` merges rather than clobbers on
  refresh.

## Keeping it honest

- **Provenance matters.** The profile records what was scanned and when. A profile learned from
  40 closed stories is worth more than one inferred from 3 — the confidence notes say which.
- **Refresh deliberately.** Conventions drift. Re-run `/learn-team` when the team changes how it
  works, not every drafting run.
- **You can hand-write it.** If you already know your conventions, you can fill in
  `team-profile.md` by hand and skip the scan. The drafter doesn't care how the knowledge got
  there — only that it's accurate.
