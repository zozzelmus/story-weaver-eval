# corpus/ — grounding exemplars

Well-written past tickets used as few-shot exemplars by V1+ (when no Jira MCP is connected,
this is the whole grounding pool; when one is connected, it's a supplementary seed).

These teach the model your project's conventions: summary phrasing, AC style, components, labels.

⚠️ **Leakage rule:** every file here must be a DIFFERENT ticket from anything in
`reference-tickets/`. Never put a held-out answer in the grounding pool.

Two example exemplars ship here — add more of your own good tickets.
