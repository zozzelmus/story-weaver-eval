#!/usr/bin/env python3
"""
Aggregate Story Weaver eval results.

Reads results/*.json (written by the invest-judge skill) and prints, per variant:
  - number of cases scored
  - mean case score
  - mean of each INVEST dimension
  - reference-comparison win rate (how often the generated set beat the human one)

No model calls, no third-party deps — stdlib only, so it runs in a locked-down environment
with any Python 3.8+. (If you have pandas and want prettier tables, it's easy to adapt, but
this version deliberately needs nothing.)

Usage:
    python scripts/aggregate.py [results_dir]
Defaults to ../results relative to this script.
"""

import json
import sys
from pathlib import Path
from statistics import mean

INVEST_DIMS = ["independent", "negotiable", "valuable", "estimable", "small", "testable"]
VARIANT_ORDER = ["v0", "v1", "v2", "v3"]


def load_results(results_dir: Path):
    rows = []
    for p in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ! skipping {p.name}: not valid JSON ({e})")
            continue
        if "variant" not in data or "tickets" not in data:
            print(f"  ! skipping {p.name}: missing 'variant' or 'tickets'")
            continue
        rows.append((p.name, data))
    return rows


def case_invest_means(data):
    """Return {dim: mean across this case's tickets} and overall case mean."""
    per_dim = {d: [] for d in INVEST_DIMS}
    for t in data.get("tickets", []):
        inv = t.get("invest", {})
        for d in INVEST_DIMS:
            if d in inv:
                per_dim[d].append(inv[d])
    dim_means = {d: (mean(v) if v else None) for d, v in per_dim.items()}
    present = [m for m in dim_means.values() if m is not None]
    case_mean = round(mean(present), 2) if present else None
    return dim_means, case_mean


def main():
    results_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "results"
    if not results_dir.exists():
        print(f"No results directory at {results_dir}")
        sys.exit(1)

    rows = load_results(results_dir)
    if not rows:
        print(f"No usable result JSON found in {results_dir}.")
        print("Run a variant, then the invest-judge skill, to produce <CASE-ID>.<variant>.json files.")
        sys.exit(0)

    # bucket by variant
    by_variant = {}
    for fname, data in rows:
        by_variant.setdefault(data["variant"], []).append(data)

    print(f"\nStory Weaver eval — {len(rows)} result file(s) across "
          f"{len(by_variant)} variant(s) in {results_dir}\n")

    header = f"{'variant':<8}{'cases':>6}{'case_score':>12}   " + "".join(f"{d[:4]:>6}" for d in INVEST_DIMS) + f"{'gen_win%':>10}"
    print(header)
    print("-" * len(header))

    ordered = [v for v in VARIANT_ORDER if v in by_variant] + [v for v in by_variant if v not in VARIANT_ORDER]
    for v in ordered:
        cases = by_variant[v]
        case_scores, dim_acc, wins, comparisons = [], {d: [] for d in INVEST_DIMS}, 0, 0
        for data in cases:
            dim_means, case_mean = case_invest_means(data)
            if case_mean is not None:
                case_scores.append(case_mean)
            for d in INVEST_DIMS:
                if dim_means[d] is not None:
                    dim_acc[d].append(dim_means[d])
            rc = data.get("reference_comparison", {})
            if rc.get("winner") in ("generated", "human", "tie"):
                comparisons += 1
                if rc["winner"] == "generated":
                    wins += 1

        cs = f"{mean(case_scores):.2f}" if case_scores else "  -"
        dims = "".join(f"{(mean(dim_acc[d]) if dim_acc[d] else 0):>6.2f}" for d in INVEST_DIMS)
        winpct = f"{(100 * wins / comparisons):>9.0f}%" if comparisons else "        -"
        print(f"{v:<8}{len(cases):>6}{cs:>12}   {dims}{winpct}")

    print("\nNotes:")
    print("  - case_score = mean over a case's tickets of the mean of its six INVEST scores.")
    print("  - gen_win% = share of cases where the judge preferred the generated set over the human one.")
    print("  - ~15 cases per variant is directional, not a verdict. Run twice; treat the spread as the error bar.")
    print("  - If V0->V1 is the biggest jump, grounding alone may be most of the fix.\n")


if __name__ == "__main__":
    main()
