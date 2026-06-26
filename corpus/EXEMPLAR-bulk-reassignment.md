# EXEMPLAR — Bulk case reassignment (grounding corpus)

> A well-written past ticket used as a GROUNDING exemplar. Different feature from anything in
> `reference-tickets/`. Teaches the project's background-job + notification conventions, which
> are useful context for any feature with long-running work.

## Story: Reassign a batch of cases to a new owner with audit and notify
**Epic Link:** Case workload management
**Description:** Team leads occasionally need to move many cases from one analyst to another
(e.g. when someone goes on leave). Let a lead select multiple cases and reassign them in one
action, with an audit trail and notifications to the affected analysts.
**Acceptance Criteria:**
- **Given** a lead has selected multiple cases **When** they choose Reassign and pick a new owner **Then** all selected cases are reassigned and each change is recorded in the case audit log.
- **Given** a reassignment of many cases **When** the batch is large **Then** it runs as a background job and the lead is notified via the existing in-app + email mechanism when complete.
- **Given** cases were reassigned **When** the job completes **Then** the previous and new owners are notified of the change.
**Components:** case-explorer, notifications  **Labels:** lead-tools
