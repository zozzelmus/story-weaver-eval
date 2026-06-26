# features/ — optional local feature briefs

Normally the feature you're breaking down **lives in Jira**, and `gather-context` reads it from
there (description, AC, comments, links, attachments) via the Jira MCP. You don't need anything
in this folder for the live flow.

This folder is for the cases where it's useful to have the requirement **as a local file**:

- the ask isn't fully written up in Jira yet, or
- you want to run the agent **offline** (no Jira MCP), or
- you want a worked example to smoke-test the skills.

Format: one file per feature, in **pre-ticket voice** — a requirement, not tickets. Pass it to
`gather-context` as `brief=features/<file>.md`.

Two worked examples ship here:

- `EXAMPLE-0001-bulk-export.md` — a small, self-contained feature (saved-search bulk export).
- `0002-vibes-conduct-case-intake.md` — a richer, real-shaped feature (secure VIBES→ServiceNow
  transport), with a representative inbound payload in `samples/`.
