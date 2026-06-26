# 0002 — Secure transport of conduct cases from VIBES to ServiceNow, with in-network redaction and enrichment before egress

> A real candidate feature for the transport-middleware platform. Written in business-ask voice:
> the requirement states the outcome and value; the mechanism lives under refinement notes.

## Requirement

We operate the **transport middleware** that moves conduct cases between systems. Cases
originate in **VIBES**, an *external* conduct case intake feed, and must end up in **ServiceNow**,
a *public (cloud)* application where investigators work them. Our system is the controlled
crossing point: it brings cases in from the external feed, processes them inside our private
network, and egresses the result out to public ServiceNow.

The problem is the sensitive data making that crossing. Raw cases carry payment card data (PCI)
and personally identifiable information (PII) in free-text narrative fields and in fields VIBES
has flagged as sensitive. Because ServiceNow sits outside our private network, **none of that
sensitive data can leave our network un-masked** — and today getting a case into a compliant,
sendable state means manual scrubbing and manual account lookups before anyone can move it on.
That is slow, inconsistent, and every manual touch of unredacted PCI/PII inside the boundary is
a compliance and data-exposure risk.

We want our middleware to move each new VIBES case to ServiceNow **automatically and safely** —
sensitive data masked and customer account context attached while the case is still inside our
network, so that only sanitized, enriched cases ever egress to the public destination.

## What they want

- **Automatic pickup** of every new case from the external VIBES feed — no manual import.
- **In-network masking** of all PCI/PII in free-text fields, and in the fields VIBES flagged as
  sensitive, performed before the case is sent anywhere outside our network.
- **In-network enrichment**: the case is enriched with the customer's account details, looked up
  from the **ECN** on the case, using account data that lives inside our network.
- **Egress to ServiceNow ready to work**: the masked, enriched case is delivered to the existing
  public ServiceNow application in the shape investigators expect.
- **Nothing sensitive crosses the boundary un-sanitized.** If masking or enrichment can't
  complete, the case must be held inside the network and surfaced — never egressed half-processed
  or with sensitive data exposed.

## Scope note

Our deliverable is the **transport and transformation layer** — the secure pipe that moves and
shapes the case across the boundary. It does not own the masking capability (that's NOVA) or the
case management system (that's ServiceNow); it orchestrates them and is accountable for what
crosses the boundary.

## Notes / constraints heard in refinement

- New cases arrive from the external VIBES feed over **Kafka**, into our private network.
- Masking is performed by **NOVA**, our in-network AI orchestration platform: an API call whose
  result is returned over NOVA's **streaming API**.
- "Flagged fields" = fields VIBES has already confirmed contain sensitive data; masked in
  addition to anything detected within free text.
- Account enrichment is keyed off the **ECN** field, resolved against account data inside our
  network.
- **ServiceNow is a public (cloud) destination**; sending the mapped payload to it is the egress
  point out of our private network.
- The masked-and-enriched data must be mapped into ServiceNow's expected request payload.
- Both the NOVA and ServiceNow calls are fronted by **Apigee**, already configured for these
  services from prior work — no new gateway setup expected.

## Sample inbound record

A representative VIBES record as it arrives on the queue lives at
`samples/0002-vibes-case.kafka.json`, annotated in `samples/README.md`. It exercises both
masking paths (confirmed flagged fields *and* PCI/PII embedded in free text) and includes a few
intentional scope ambiguities (raw ECN egress, attachments, employee data) for the decomposition
to surface.
