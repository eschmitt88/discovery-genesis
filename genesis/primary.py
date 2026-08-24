"""Decide which sampled works are primary research, and which pairs survive.

    uv run python -m genesis.primary data/samples/main50.json --cards cases/main50 \
        --pubtypes data/pubtypes.json --out data/primary-main50.json

Three independent judgements per work:

  coders      each blind coder's `is_primary` (yes / partial / no) from the
              dossier, with no knowledge of the work's impact — the arbiter
              of record, because it is the only signal produced without
              seeing citation counts;
  external    Semantic Scholar / Europe PMC / Crossref publication types
              (`genesis.pubtype`);
  regex       the sampler's own title/abstract/venue classifier, kept only
              to measure how badly it under-called.

A work is `primary` when no coder said `no` and no external signal says
review; `excluded` when both coders say `no` or an external type says review
and at least one coder agrees; otherwise `disputed` and reported as such.
A **pair** survives only if both its members are primary — a twin that turns
out to be a review makes the comparison meaningless in either direction.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def card_is_primary(p: Path) -> str | None:
    m = re.search(r"^is_primary:\s*\"?([a-zA-Z]+)", p.read_text(), re.M)
    return m.group(1).lower() if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.primary")
    ap.add_argument("sample")
    ap.add_argument("--cards", required=True, help="dir holding coderA/ and coderB/")
    ap.add_argument("--pubtypes", default="data/pubtypes.json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rec = json.load(open(a.sample))
    cards = Path(a.cards)
    coders = sorted(d.name for d in cards.iterdir() if d.is_dir() and d.name.startswith("coder"))
    judg = {}
    for c in coders:
        for f in (cards / c).glob("W*.md"):
            judg.setdefault(f.stem, {})[c] = card_is_primary(f)
    ext = json.load(open(a.pubtypes)) if Path(a.pubtypes).exists() else {}

    verdicts, rows = {}, []
    for p in rec["pairs"]:
        for role in ("case", "twin"):
            w = p[role]["id"]
            cs = judg.get(w, {})
            says_no = [c for c, v in cs.items() if v == "no"]
            e = ext.get(w, {})
            ext_review = bool(e.get("is_review_signal"))
            if len(says_no) >= 2 or (ext_review and says_no):
                v = "excluded"
            elif says_no or ext_review:
                v = "disputed"
            elif cs:
                v = "primary"
            else:
                v = "uncoded"
            verdicts[w] = {"verdict": v, "coders": cs, "external_review": ext_review,
                           "external_flags": e.get("review_flags", []),
                           "n_refs": e.get("n_refs"), "role": role,
                           "title": p[role].get("title")}
    keep = []
    for k, p in enumerate(rec["pairs"]):
        vs = [verdicts[p[r]["id"]]["verdict"] for r in ("case", "twin")]
        ok = all(v == "primary" for v in vs)
        keep.append({"pair": k, "keep": ok, "verdicts": vs,
                     "topic": p["topic"], "year": p["year"]})
    out = {"sample": a.sample, "coders": coders, "works": verdicts, "pairs": keep,
           "n_pairs_total": len(keep), "n_pairs_kept": sum(x["keep"] for x in keep)}
    Path(a.out).write_text(json.dumps(out, indent=1))
    c = Counter(v["verdict"] for v in verdicts.values())
    cr = Counter((v["role"], v["verdict"]) for v in verdicts.values())
    print(f"works: {dict(c)}")
    print(f"by role: {dict(sorted(cr.items()))}")
    print(f"pairs kept: {out['n_pairs_kept']}/{out['n_pairs_total']}")
    ex = [(v["n_refs"], w, (v["title"] or "")[:60], v["role"]) for w, v in verdicts.items()
          if v["verdict"] in ("excluded", "disputed")]
    for n, w, t, r in sorted(ex, key=lambda x: -(x[0] or 0))[:15]:
        print(f"  {r:4s} {w} refs={n} {t}")


if __name__ == "__main__":
    main()
