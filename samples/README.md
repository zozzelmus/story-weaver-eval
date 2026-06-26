# samples/ — VIBES inbound case fixture

`0002-vibes-case.kafka.json` is a representative record as it would arrive on the VIBES topic,
for feature `0002`. It exists so the feature is concrete — the ticket generators (and, later, a
real implementation) have an actual payload shape to reason about.

**All values are synthetic.** Canonical test PAN (`4111111111111111`), placeholder SSN
(`123-45-6789`), reserved fictional phone range (`555-01xx`), and `example.com`. Safe to commit.

## What the record represents

A sales-practice conduct complaint raised in VIBES (external), keyed by `ecn` for in-network
account enrichment, destined for public ServiceNow after masking. The envelope (`topic`, `key`,
`headers`, `value`) mirrors a consumed Kafka record so consumer code has the metadata it needs
(`schemaVersion`, `eventType`, `correlationId`, `producedAt`).

## The two masking paths (this is the point of the fixture)

The requirement says mask both *flagged fields* and *free text* — this record exercises both:

1. **Confirmed flagged fields** (`dataFlags[].status == "CONFIRMED"`) — VIBES has already
   asserted these structured fields hold sensitive data. NOVA masks them by field path:
   - `customer.ssn` (PII / SSN)
   - `customer.cardNumber` (PCI / PAN)
   - `customer.cardExpiry` (PCI / card expiry)
   - `customer.accountNumber` (PII / financial account)
   - `customer.dateOfBirth` (PII / DOB)

2. **Free text requiring detection** (`status == "REQUIRES_DETECTION"`) — the same SSN, PAN,
   DOB, phone and email are *also* embedded inline in `complaint.detailedNarrative` and
   `complaint.summary`. These aren't structured; NOVA has to detect and mask them in place.
   This is where naive field-level masking leaks — a good implementation (and a good ticket
   set) treats free text as a distinct path.

## Open design questions worth a ticket / a decision (not yet settled here)

- **Does the raw `ecn` egress to ServiceNow?** It's an internal customer identifier and the
  enrichment key. Whether the un-tokenized ECN should cross the boundary is a real decision —
  a good decomposition surfaces it rather than silently passing it through.
- **Attachments.** `attachments[].containsSensitiveData == true` — the PDF excerpt is flagged
  sensitive, but this flow as described only masks the case record's fields/text. Whether
  attachments are in scope, stripped, or separately handled is unspecified on purpose; it's
  the kind of gap V3's critic should flag against the "nothing sensitive crosses un-sanitized"
  guarantee.
- **`subjectEmployee`** is internal employee data, not customer PCI/PII. Decide whether it
  egresses as-is (investigators likely need it) — it's a scope call, not an automatic mask.

These ambiguities are intentional. They're exactly the places where a single-shot generator
quietly assumes the happy path and a reasoning pipeline asks the question.
