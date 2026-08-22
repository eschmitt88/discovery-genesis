"""Inter-coder agreement on genesis cards, and the case-vs-twin move contrast.

    uv run python -m genesis.agree cases/pilotB --sample data/samples/pilotB.json

Reports, for every card field two coders both filled:
  * raw agreement and Cohen's kappa on the categorical fields
    (`genesis_model`, `enabler` head, `is_primary`, and set-overlap on
    `move_candidates`);
  * the confusion table for `genesis_model`, so disagreement has a shape;
  * per-coder label distributions — a coder that always says "means-first"
    agrees with nobody for an uninteresting reason.

With `--sample`, it *then* unblinds (the sample file names which member of
each pair is the impactful case) and reports the move/genesis-model
distribution split by role. That contrast is H0/H3's first look; it must be
computed after agreement, never before, so a poor codebook cannot be tuned
against the outcome.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = ("genesis_model", "is_primary", "problem_age", "enabler_head")


def parse_card(p: Path) -> dict:
    txt = p.read_text()
    m = re.search(r"^---\n(.*?)\n---", txt, re.S)
    fm = m.group(1) if m else ""
    d = {"id": p.stem}
    for key in ("coder", "genesis_model", "genesis_confidence", "is_primary",
                "problem_age", "enabler", "move", "recognised", "evidence"):
        mm = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
        if mm:
            d[key] = mm.group(1).strip().strip('"').strip("'")
    mm = re.search(r"^move_candidates:\s*\[(.*?)\]", fm, re.M | re.S)
    d["move_candidates"] = [x.strip().strip('"').strip("'")
                            for x in (mm.group(1).split(",") if mm else []) if x.strip()]
    # enabler is free text after a category word; take the head before any dash/colon
    e = d.get("enabler", "")
    d["enabler_head"] = re.split(r"[—\-:|]", e)[0].strip().lower()[:24] if e else ""
    d["is_primary"] = (d.get("is_primary", "") or "").split()[0].rstrip("—-").strip().lower()
    return d


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if not n:
        return None
    labels = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if (sa | sb) else 1.0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.agree")
    ap.add_argument("cards_dir", help="directory holding coderA/ and coderB/")
    ap.add_argument("--sample", default=None, help="unblind roles from this sample file")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    root = Path(a.cards_dir)
    coders = sorted(d.name for d in root.iterdir() if d.is_dir() and d.name.startswith("coder"))
    if len(coders) < 2:
        raise SystemExit(f"need two coder dirs in {root}, found {coders}")
    A, B = ({p.stem: parse_card(p) for p in (root / c).glob("W*.md")} for c in coders[:2])
    ids = sorted(set(A) & set(B))
    L = [f"# Inter-coder agreement — {root}", "",
         f"Coders: {coders[0]} vs {coders[1]}; {len(ids)} papers coded by both "
         f"({len(A)} / {len(B)} total).", ""]
    out = {"n": len(ids), "coders": coders[:2], "fields": {}}
    L += ["| field | raw agreement | Cohen κ |", "|---|---|---|"]
    for f in FIELDS:
        va, vb = [A[i].get(f, "") for i in ids], [B[i].get(f, "") for i in ids]
        raw = sum(x == y for x, y in zip(va, vb)) / len(ids) if ids else 0
        k = kappa(va, vb)
        out["fields"][f] = {"raw": round(raw, 3), "kappa": k}
        L.append(f"| {f} | {raw:.2f} | {k if k is not None else '–'} |")
    jac = [jaccard(A[i]["move_candidates"], B[i]["move_candidates"]) for i in ids]
    any_overlap = sum(j > 0 for j in jac) / len(ids) if ids else 0
    out["move_jaccard_mean"] = round(sum(jac) / len(jac), 3) if jac else None
    out["move_any_overlap"] = round(any_overlap, 3)
    L.append(f"| move_candidates (Jaccard) | {out['move_jaccard_mean']} mean; "
             f"{any_overlap:.2f} share with ≥1 shared label | – |")
    L += ["", "## genesis_model confusion (rows = " + coders[0] + ")", ""]
    conf = defaultdict(Counter)
    for i in ids:
        conf[A[i].get("genesis_model", "?")][B[i].get("genesis_model", "?")] += 1
    cols = sorted({c for r in conf.values() for c in r})
    L.append("| | " + " | ".join(cols) + " |")
    L.append("|---" * (len(cols) + 1) + "|")
    for r in sorted(conf):
        L.append(f"| {r} | " + " | ".join(str(conf[r][c]) for c in cols) + " |")
    L += ["", "## label distributions", ""]
    for name, C in ((coders[0], A), (coders[1], B)):
        gm = Counter(C[i].get("genesis_model") for i in ids)
        mv = Counter(m for i in ids for m in C[i]["move_candidates"])
        L.append(f"- **{name}** genesis_model: {dict(gm)}")
        L.append(f"  moves: {dict(mv.most_common())}")
    rec = [i for i in ids if not (A[i].get("recognised", "no").startswith("no")
                                  and B[i].get("recognised", "no").startswith("no"))]
    L += ["", f"Papers either coder reported recognising: {len(rec)} — {rec}", ""]
    out["recognised"] = rec

    if a.sample:
        rec_s = json.load(open(a.sample))
        role = {p[r]["id"]: r for p in rec_s["pairs"] for r in ("case", "twin")}
        L += ["## Unblinded: move and genesis model by role", "",
              "(computed after agreement, per the coding protocol)", ""]
        by = {"case": Counter(), "twin": Counter()}
        gby = {"case": Counter(), "twin": Counter()}
        for i in ids:
            r = role.get(i)
            if not r:
                continue
            for coder in (A, B):
                for m in coder[i]["move_candidates"]:
                    by[r][m] += 1
                gby[r][coder[i].get("genesis_model")] += 1
        for r in ("case", "twin"):
            L.append(f"- **{r}** genesis_model: {dict(gby[r])}")
            L.append(f"  moves: {dict(by[r].most_common())}")
        out["by_role"] = {r: {"genesis_model": dict(gby[r]), "moves": dict(by[r])} for r in by}
    txt = "\n".join(L) + "\n"
    print(txt)
    if a.out:
        Path(a.out).write_text(txt)
        Path(a.out).with_suffix(".json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
