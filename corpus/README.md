# corpus/ — optional offline exemplars

Well-written past tickets used as **fallback grounding** when no Jira MCP is connected. When a
Jira MCP *is* connected, `learn-team` learns conventions directly from the live project and
these are just a supplementary seed.

They teach the agent your project's conventions: summary phrasing, AC style, components, labels.

> No leakage rule anymore — there's no held-out answer key in this repo (it's a ticket-drafting
> agent, not an eval harness). Drop in any good real tickets you'd like the agent to imitate.
> The richer the live Jira scan or this corpus, the more your drafts sound like your team.

A couple of example exemplars ship here — add more of your own good tickets, or rely on the live
Jira scan via `learn-team`.
