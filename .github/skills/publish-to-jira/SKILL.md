---
name: publish-to-jira
description: The single, gated write path. After a human has reviewed and approved the ticket drafts in tickets-review/<FEATURE-KEY>/, create those tickets in Jira and attach them to the feature (epic link / parent), reusing the components, labels, and estimates from each draft. Requires explicit human approval before any write and is idempotent. Use ONLY when the user has reviewed the drafts and explicitly says to publish/push them to Jira.
---

# publish-to-jira — the gated writer

This is the **only** skill in the repo that writes to Jira. Everything else is read-only by
design. Because there is no SDK-enforced permission gate here (we run in Copilot), the gate is
**procedural and you must honor it**: you do not create anything until the human has explicitly
approved this specific set.

## The gate (do not skip)

1. Read `tickets-review/<FEATURE-KEY>/INDEX.md` and every `NN-<slug>.md`.
2. **Restate the plan back to the user** before writing anything:
   > About to create **N** issues in Jira under **<FEATURE-KEY>**: 1 epic + M stories, with
   > these components/labels/estimates. Tickets flagged `duplicate_of` will be **skipped**.
   > Reply **"publish"** to proceed, or tell me what to change.
3. **Wait for explicit approval.** Do not proceed on implicit or ambiguous replies. If the user
   edited the drafts, re-read them first — the files are the source of truth, not your memory.

## Steps (only after approval)

1. **Resolve the parent.** If the feature/epic already exists in Jira, use its key. If a draft
   epic needs creating, create it first and capture its new key (capability: **"create a Jira
   issue"**).
2. **Create each story**, attaching it to the feature/epic via epic link / parent (capability:
   "create a Jira issue", "set parent / epic link"). For each draft:
   - map the front-matter → real fields: issue type, parent, components, labels, estimate,
     priority,
   - put the description and Given/When/Then AC into the right Jira fields for this server,
   - **skip** any ticket whose `duplicate_of` is set; instead link the feature to the existing
     issue and note it.
3. **Write the result back** for traceability:
   - in each `NN-<slug>.md`, flip front-matter `status: draft` → `status: created: <JIRA-KEY>`,
   - in `INDEX.md`, record the created keys (and any skipped duplicates) as a publish log.

## Idempotency & safety

- **Idempotent.** A ticket whose front-matter already shows `created: <KEY>` is skipped on
  re-run — never create the same story twice. Re-running after a partial failure only creates
  what's still `draft`.
- **Attach, don't restructure.** This skill creates the drafted issues under the feature. It
  does not transition, reassign, or rewrite existing issues.
- **One feature at a time.** Publish a single `tickets-review/<FEATURE-KEY>/` set per run so the
  approval is specific and auditable.
- If any create fails, stop, report which keys were created and which weren't, and leave the
  rest as `draft` for a clean re-run.

## Constraints

- No writes without the explicit approval in the gate above.
- The drafted files are the contract — publish exactly what was approved, not a fresh
  generation. If you think something should change, surface it and re-gate; don't silently
  "improve" during publish.
