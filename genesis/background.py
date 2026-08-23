"""Stage 3b: the topic-year background, for two features H1 cannot do without.

    uv run python -m genesis.background data/samples/pilotB.json [--n 150]

For every (primary topic, year) pool that a sample draws from, pull N random
primary-research articles from the same pool (OpenAlex `sample=` with a logged
seed) together with their reference lists, then resolve every referenced
work's year, citations and subfield. From that:

1. **Velocity control.** The pool's own reference-age distribution
   (`pool_ref_age_median`, `pool_ref_share_le3`, `pool_ref_hot_median`). A
   case whose references are "young" may simply sit in a fast subfield; the
   feature that matters is the case's recency *relative to its pool*.

2. **Atypicality null (Uzzi-style, subfield level).** For each pair of
   subfields that a background paper cites together, observed co-citation
   count vs the count expected if subfields were cited independently:
   z = (obs − exp) / sqrt(exp), exp = N · p_i · p_j. A focal paper's reference
   list then maps to a set of subfield-pair z-scores; its *conventionality* is
   the median z and its *atypical tail* the 10th percentile. Uzzi used journal
   pairs and a degree-preserving rewiring null; this is the cheap first
   approximation, and it is labelled as such in every output.

Output: data/background/<topic>-<year>.json (pool stats + pair table) and a
shared cache data/background/_refmeta.json so overlapping references are
resolved once. Reads only OpenAlex. Writes nothing under raw/.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics as st
import sys
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

from .fetch import fetch_batch, wid
from .sample import classify, openalex, pool_filter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "background"
REFMETA = OUT / "_refmeta.json"
REF_SELECT = "id,publication_year,cited_by_count,primary_topic"


def load_refmeta() -> dict:
    return json.load(REFMETA.open()) if REFMETA.exists() else {}


def save_refmeta(m: dict):
    OUT.mkdir(parents=True, exist_ok=True)
    REFMETA.write_text(json.dumps(m))


def resolve_refs(ids: list[str], meta: dict, log) -> None:
    todo = [i for i in ids if i not in meta]
    if not todo:
        return
    log(f"    resolving {len(todo)} reference records ({len(ids) - len(todo)} cached)")
    for i in range(0, len(todo), 500):
        chunk = todo[i:i + 500]
        for r in fetch_batch(chunk, REF_SELECT, log=log):
            pt = r.get("primary_topic") or {}
            meta[wid(r["id"])] = {
                "y": r.get("publication_year"), "c": r.get("cited_by_count"),
                "sf": ((pt.get("subfield") or {}).get("id") or "").rsplit("/", 1)[-1] or None,
                "f": ((pt.get("field") or {}).get("id") or "").rsplit("/", 1)[-1] or None,
            }
        for w in chunk:                         # unresolved ids stay unresolved, not retried forever
            meta.setdefault(w, None)
        save_refmeta(meta)
        time.sleep(0.3)


def pull_pool(topic_id: str, year: int, n: int, seed: int, log) -> list[dict]:
    """n random primary-research articles from the pool, with reference lists."""
    flt = pool_filter(topic_id, year)
    got, page = [], 1
    # OpenAlex sample= returns up to per-page per call and is stable for a seed; over-draw
    # because the primary filter removes ~30 %.
    while len(got) < n and page <= 3:
        d = openalex({"filter": flt, "sample": min(200, n * 2), "seed": seed + page, "per-page": 200,
                      "select": "id,title,publication_year,type,referenced_works,cited_by_count,"
                                "primary_location,abstract_inverted_index"})
        for w in d["results"]:
            if classify(w)[0] == "primary" and w.get("referenced_works"):
                got.append({"id": wid(w["id"]), "refs": [wid(r) for r in w["referenced_works"]],
                            "c": w.get("cited_by_count")})
        page += 1
        time.sleep(0.5)
    seen, uniq = set(), []
    for g in got:
        if g["id"] not in seen:
            seen.add(g["id"]); uniq.append(g)
    return uniq[:n]


def pool_stats(pool: list[dict], year: int, meta: dict) -> dict:
    ages, hot, cross = [], [], []
    for w in pool:
        rs = [meta.get(r) for r in w["refs"]]
        rs = [r for r in rs if r]
        ages += [year - r["y"] for r in rs if r.get("y")]
        hot += [r["c"] for r in rs if r.get("c") is not None]
    return {
        "n_works": len(pool),
        "n_refs_resolved": sum(1 for w in pool for r in w["refs"] if meta.get(r)),
        "pool_ref_age_median": st.median(ages) if ages else None,
        "pool_ref_age_mean": round(st.mean(ages), 2) if ages else None,
        "pool_ref_share_le3": round(sum(a <= 3 for a in ages) / len(ages), 3) if ages else None,
        "pool_ref_hot_median": st.median(hot) if hot else None,
    }


def pair_table(pool: list[dict], meta: dict) -> dict:
    """Subfield-pair z-scores under an independence null."""
    N = len(pool)
    sf_sets = []
    for w in pool:
        s = {meta[r]["sf"] for r in w["refs"] if meta.get(r) and meta[r].get("sf")}
        if len(s) >= 1:
            sf_sets.append(s)
    single = Counter(sf for s in sf_sets for sf in s)
    pair = Counter(tuple(sorted(p)) for s in sf_sets for p in combinations(s, 2))
    n = len(sf_sets)
    z = {}
    for (a, b), obs in pair.items():
        exp = n * (single[a] / n) * (single[b] / n)
        z["|".join((a, b))] = round((obs - exp) / math.sqrt(exp), 3) if exp > 0 else None
    return {"n_works": n, "subfield_freq": dict(single), "pair_z": z,
            "null": "independence (exp = n·p_i·p_j); Uzzi used degree-preserving rewiring on journal pairs"}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.background")
    ap.add_argument("sample", nargs="+")
    ap.add_argument("--n", type=int, default=150, help="background works per topic-year")
    ap.add_argument("--seed", type=int, default=20260823)
    a = ap.parse_args(argv)
    log = lambda s: print(s, file=sys.stderr)
    pools = {}
    for f in a.sample:
        for p in json.load(open(f))["pairs"]:
            pools[(p["topic_id"], p["year"])] = p["topic"]
    meta = load_refmeta()
    OUT.mkdir(parents=True, exist_ok=True)
    for k, (tid, year) in enumerate(sorted(pools), 1):
        out = OUT / f"{tid}-{year}.json"
        if out.exists():
            log(f"[{k}/{len(pools)}] {pools[(tid, year)]} {year}: cached"); continue
        log(f"[{k}/{len(pools)}] {pools[(tid, year)]} {year}")
        pool = pull_pool(tid, year, a.n, a.seed, log)
        resolve_refs(sorted({r for w in pool for r in w["refs"]}), meta, log)
        rec = {"topic_id": tid, "topic": pools[(tid, year)], "year": year, "seed": a.seed,
               "stats": pool_stats(pool, year, meta), "pairs": pair_table(pool, meta),
               "works": [w["id"] for w in pool]}
        out.write_text(json.dumps(rec))
        s = rec["stats"]
        log(f"    {s['n_works']} works, {s['n_refs_resolved']} refs; pool ref-age median {s['pool_ref_age_median']}, "
            f"share≤3y {s['pool_ref_share_le3']}, hot median {s['pool_ref_hot_median']}")


if __name__ == "__main__":
    main()
