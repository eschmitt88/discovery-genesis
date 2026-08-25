"""H3: does move frequency differ between impactful papers and their twins?

    uv run python -m genesis.moves cases/main50 --sample data/samples/main50.json \
        --primary data/primary-main50.json --out results/h3-main50.md

Counts each move at the level that matters — the **paper**, not the coding —
so a paper both coders label `instrument` counts once, not twice. Three
strengths of evidence per move:

    any     at least one coder used the label
    both    both coders used it (the conservative count)
    primary the label a coder put first (most central)

For each move: a 2x2 (has move x case/twin) with a two-sided Fisher exact
test, and the paired view (discordant pairs only) with an exact sign test —
the paired test is the one that respects the matched design.

Restricted to pairs both of whose members two blind coders called primary
research, unless --no-primary-filter is passed. Reviews are excluded because
`consolidation` on a review is a tautology, not a finding.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from math import comb
from pathlib import Path


def parse(p: Path) -> dict:
    fm = p.read_text().split("---")[1]
    g = lambda k: (re.search(rf"^{k}:\s*\"?([^\"\n]*)", fm, re.M) or [None, ""])[1].strip()
    m = re.search(r"^move_candidates:\s*\[(.*?)\]", fm, re.M | re.S)
    moves = [x.strip().strip("\"'") for x in (m.group(1).split(",") if m else []) if x.strip()]
    return {"moves": moves, "primary_move": moves[0] if moves else None,
            "genesis": g("genesis_model"), "enabler": g("enabler").split()[0] if g("enabler") else ""}


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    n = a + b + c + d
    r1, c1 = a + b, a + c
    if not n or not r1 or not c1:
        return 1.0
    def h(k):
        return comb(r1, k) * comb(n - r1, c1 - k) / comb(n, c1)
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    p0 = h(a)
    return min(1.0, sum(h(k) for k in range(lo, hi + 1) if h(k) <= p0 + 1e-12))


def sign_two_sided(x: int, y: int) -> float:
    n = x + y
    if not n:
        return 1.0
    k = min(x, y)
    return min(1.0, 2 * sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.moves")
    ap.add_argument("cards", help="dir with coderA/ and coderB/")
    ap.add_argument("--sample", required=True)
    ap.add_argument("--primary", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-primary-filter", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.cards)
    coders = sorted(d.name for d in root.iterdir() if d.is_dir() and d.name.startswith("coder"))
    cards = defaultdict(dict)
    for c in coders:
        for f in (root / c).glob("W*.md"):
            cards[f.stem][c] = parse(f)
    rec = json.load(open(a.sample))
    keep = None
    if a.primary and not a.no_primary_filter:
        keep = {p["pair"] for p in json.load(open(a.primary))["pairs"] if p["keep"]}
    pairs = [(k, p) for k, p in enumerate(rec["pairs"]) if keep is None or k in keep]
    pairs = [(k, p) for k, p in pairs
             if len(cards.get(p["case"]["id"], {})) == 2 and len(cards.get(p["twin"]["id"], {})) == 2]

    L = [f"# H3 — move frequency, case vs twin ({len(pairs)} pairs, "
         f"{'primary research only' if keep else 'all pairs'})", ""]
    labels = sorted({m for k, p in pairs for r in ("case", "twin")
                     for c in cards[p[r]["id"]].values() for m in c["moves"]})
    for strength, fn in (("any", lambda cs, m: any(m in c["moves"] for c in cs.values())),
                         ("both", lambda cs, m: all(m in c["moves"] for c in cs.values())),
                         ("primary", lambda cs, m: any(c["primary_move"] == m for c in cs.values()))):
        L += [f"## Coded by **{strength}** coder(s)", "",
              "| move | cases | twins | Fisher p | case-only pairs | twin-only pairs | sign p |",
              "|---|---|---|---|---|---|---|"]
        rows = []
        for m in labels:
            ca = sum(fn(cards[p["case"]["id"]], m) for _, p in pairs)
            tw = sum(fn(cards[p["twin"]["id"]], m) for _, p in pairs)
            if ca + tw == 0:
                continue
            n = len(pairs)
            fp = fisher_two_sided(ca, n - ca, tw, n - tw)
            co = sum(1 for _, p in pairs if fn(cards[p["case"]["id"]], m) and not fn(cards[p["twin"]["id"]], m))
            to = sum(1 for _, p in pairs if fn(cards[p["twin"]["id"]], m) and not fn(cards[p["case"]["id"]], m))
            rows.append((m, ca, tw, fp, co, to, sign_two_sided(co, to)))
        for m, ca, tw, fp, co, to, sp in sorted(rows, key=lambda r: r[6]):
            star = "**" if sp < 0.05 else ""
            L.append(f"| `{m}` | {ca}/{len(pairs)} | {tw}/{len(pairs)} | {fp:.3f} "
                     f"| {co} | {to} | {star}{sp:.3f}{star} |")
        L.append("")
    L += ["## Genesis model and enabler by role", ""]
    for field in ("genesis", "enabler"):
        for role in ("case", "twin"):
            c = Counter(cards[p[role]["id"]][cd][field] for _, p in pairs for cd in coders)
            L.append(f"- **{role}** {field}: {dict(c.most_common())}")
        L.append("")
    txt = "\n".join(L) + "\n"
    print(txt)
    if a.out:
        Path(a.out).write_text(txt)


if __name__ == "__main__":
    main()
