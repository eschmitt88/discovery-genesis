"""H1 pilot: paired case-vs-twin comparison of bibliometric features.

    uv run python experiments/2026-08-22-h1-pilot-bibliometrics/analyze.py

Reads data/features/pilot.csv (dev split only), writes metrics.json and
results/paired.md in this folder. Wilcoxon signed-rank (exact, two-sided) on
the paired differences; sign counts; median paired difference; Cliff's delta
on the pairs as an effect size that does not assume anything.
"""
from __future__ import annotations

import csv
import json
import math
import statistics as st
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
import sys
NAME = sys.argv[1] if len(sys.argv) > 1 else "pilotB"
FEATURES = ROOT / "data" / "features" / f"{NAME}.csv"

PREDICTED = {                      # feature -> predicted sign of (case - twin); 0 = measured only
    "ref_share_le3": +1, "ref_age_median": -1, "ref_age_mean": -1,
    "ref_cross_topic": 0, "ref_cross_subfield": 0, "ref_cross_field": +1, "ref_cross_domain": 0,
    "ref_n_fields": +1, "ref_hot_median": +1, "ref_fwci_median": +1,
    "n_authors": +1, "n_institutions": +1, "n_refs": 0,
    "cd_nok": 0, "cd5_nok": 0, "s2_ref_method_share": 0,
}


def wilcoxon_exact(d: list[float]) -> float | None:
    """Exact two-sided signed-rank p-value (n <= 25); ties in |d| get average ranks."""
    d = [x for x in d if x != 0]
    n = len(d)
    if n < 5:
        return None
    absd = sorted(abs(x) for x in d)
    ranks = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and absd[j + 1] == absd[i]:
            j += 1
        for k in range(i, j + 1):
            ranks[absd[k]] = (i + j) / 2 + 1
        i = j + 1
    w_plus = sum(ranks[abs(x)] for x in d if x > 0)
    r = [ranks[abs(x)] for x in d]
    # distribution of W+ over all 2^n sign assignments (n <= 25 -> fine)
    from collections import Counter
    dist = Counter({0.0: 1})
    for rk in r:
        new = Counter()
        for w, c in dist.items():
            new[w] += c
            new[w + rk] += c
        dist = new
    total = 2 ** n
    mean = sum(r) / 2
    dev = abs(w_plus - mean)
    p = sum(c for w, c in dist.items() if abs(w - mean) >= dev - 1e-9) / total
    return min(1.0, p)


def cliffs_delta(a: list[float], b: list[float]) -> float:
    gt = sum((x > y) - (x < y) for x in a for y in b)
    return gt / (len(a) * len(b))


def main():
    rows = list(csv.DictReader(FEATURES.open()))
    pairs = {}
    for r in rows:
        pairs.setdefault(int(r["pair"]), {})[r["role"]] = r
    pairs = {k: v for k, v in pairs.items() if "case" in v and "twin" in v}
    out, lines = {"n_pairs": len(pairs), "features": {}}, []
    lines.append(f"# H1 {NAME} — paired differences (case − twin), n = {len(pairs)} pairs\n")
    lines.append("| feature | predicted | case median | twin median | median Δ | case>twin | case<twin | Wilcoxon p | Cliff δ |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for feat, sign in PREDICTED.items():
        cs, ts, ds = [], [], []
        for p in pairs.values():
            try:
                c, t = float(p["case"][feat]), float(p["twin"][feat])
            except (ValueError, KeyError):
                continue
            cs.append(c); ts.append(t); ds.append(c - t)
        if len(ds) < 5:
            continue
        pval = wilcoxon_exact(ds)
        rec = {"n": len(ds), "predicted_sign": sign, "case_median": st.median(cs), "twin_median": st.median(ts),
               "median_diff": st.median(ds), "n_pos": sum(d > 0 for d in ds), "n_neg": sum(d < 0 for d in ds),
               "wilcoxon_p": pval, "cliffs_delta": round(cliffs_delta(cs, ts), 3)}
        rec["direction_as_predicted"] = (sign == 0) or (math.copysign(1, rec["median_diff"]) == sign if rec["median_diff"] else None)
        out["features"][feat] = rec
        ps = f"{pval:.3f}" if pval is not None else "–"
        star = "**" if (pval is not None and pval < 0.05) else ""
        lines.append(f"| {feat} | {'+' if sign > 0 else '−' if sign < 0 else '·'} | {rec['case_median']:.3g} | {rec['twin_median']:.3g} "
                     f"| {star}{rec['median_diff']:+.3g}{star} | {rec['n_pos']} | {rec['n_neg']} | {star}{ps}{star} | {rec['cliffs_delta']:+.2f} |")
    # Benjamini-Hochberg FDR across the features tested in this run. 15 correlated
    # features on 15 pairs: without it, one or two "significant" cells are expected
    # by chance alone.
    tested = [(f, r["wilcoxon_p"]) for f, r in out["features"].items() if r["wilcoxon_p"] is not None]
    tested.sort(key=lambda x: x[1])
    m = len(tested)
    prev = 1.0
    for i in range(m - 1, -1, -1):
        f, pv = tested[i]
        q = min(prev, pv * m / (i + 1))
        out["features"][f]["bh_q"] = round(q, 4)
        prev = q
    lines.append("")
    lines.append(f"Benjamini-Hochberg FDR over the {m} features tested "
                 f"(q < 0.05 survives): " +
                 ", ".join(f"{f} q={out['features'][f]['bh_q']:.3f}"
                           for f, _ in tested if out["features"][f]["bh_q"] < 0.05) or "none")
    lines.append("")
    # text availability, for the coding-protocol decision
    has = [p["case"]["has_text"] == "True" for p in pairs.values()], [p["twin"]["has_text"] == "True" for p in pairs.values()]
    out["fulltext_cases"] = sum(has[0]); out["fulltext_twins"] = sum(has[1])
    lines.append(f"\nFull text available: cases {sum(has[0])}/{len(pairs)}, twins {sum(has[1])}/{len(pairs)}.")
    out["sample"] = NAME
    (HERE / "metrics.json").write_text(json.dumps(out, indent=1))
    (HERE / "results" / f"paired-{NAME}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
