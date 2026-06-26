# reference-tickets/ — ground truth

For each `features/<CASE-ID>.md`, the tickets your team **actually wrote and was happy with**.
The judge compares generated output against these.

⚠️ **Leakage rule:** these tickets must NOT also appear in `corpus/`. The grounding pool and
the held-out answers must be disjoint, or V1+ will look good for the wrong reason and your
conclusion is invalid.
