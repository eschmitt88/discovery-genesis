"""Stage 1 of the pipeline: draw case/twin pairs.

    uv run python -m genesis.sample --pairs 20 --seed 123 --out data/samples/pilot.json

Topic draw: the `xpol` sampler from llm-cross-pollination (OpenAlex topic
frame, stratified by domain, OS-entropy or logged seed), filtered to the
STEM domains. Per topic: a random year in YEARS; one impactful paper
(field-normalised citation percentile >= CASE_PCT) and one twin (same
topic/year/type, percentile in TWIN_BAND), each drawn uniformly by
OpenAlex's server-side `sample=` with a logged seed. Everything needed to
reproduce a draw is in the output record.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

XPOL_PROJECT = Path("~/projects/research/llm-cross-pollination").expanduser()
STEM_DOMAINS = ("Physical Sciences", "Life Sciences", "Health Sciences")
YEARS = (2010, 2019)
CASE_PCT = 0.99
TWIN_BAND = (0.40, 0.60)
MIN_REFS = 5                      # need prior art to study
OPENALEX = "https://api.openalex.org/works"
UA = "discovery-genesis (research; mailto:eschmitt88@gmail.com)"
SELECT = ",".join([
    "id", "doi", "title", "publication_year", "type", "cited_by_count",
    "citation_normalized_percentile", "referenced_works_count",
    "primary_topic", "open_access", "authorships", "is_retracted",
])


# ----------------------------------------------------------------- helpers
def openalex(params: dict) -> dict:
    url = OPENALEX + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:                      # noqa: BLE001
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def slim(w: dict) -> dict:
    pt = w.get("primary_topic") or {}
    return {
        "id": w["id"].rsplit("/", 1)[1],
        "doi": w.get("doi"),
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "type": w.get("type"),
        "cited_by_count": w.get("cited_by_count"),
        "pct": (w.get("citation_normalized_percentile") or {}).get("value"),
        "n_refs": w.get("referenced_works_count"),
        "n_authors": len(w.get("authorships") or []),
        "topic_id": (pt.get("id") or "").rsplit("/", 1)[-1],
        "topic": pt.get("display_name"),
        "field": (pt.get("field") or {}).get("display_name"),
        "domain": (pt.get("domain") or {}).get("display_name"),
        "oa_url": (w.get("open_access") or {}).get("oa_url"),
        "is_oa": (w.get("open_access") or {}).get("is_oa"),
    }


def draw_work(topic_id: str, year: int, pct_filter: str, seed: int) -> tuple[dict | None, int]:
    """One uniformly-sampled work from the filtered pool, plus the pool size."""
    flt = (f"primary_topic.id:{topic_id},publication_year:{year},type:article,"
           f"is_retracted:false,referenced_works_count:>{MIN_REFS - 1},"
           f"citation_normalized_percentile.value:{pct_filter}")
    pool = openalex({"filter": flt, "per-page": 1, "select": "id"})["meta"]["count"]
    if pool == 0:
        return None, 0
    d = openalex({"filter": flt, "sample": 1, "seed": seed, "per-page": 1, "select": SELECT})
    return (slim(d["results"][0]) if d["results"] else None), pool


def xpol_topics(k: int, seed: int | None) -> tuple[list[dict], dict]:
    cmd = ["uv", "run", "--project", str(XPOL_PROJECT), "xpol", "sample",
           "-k", str(k), "--level", "topic", "--stratify", "domain", "--json"]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    out = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=XPOL_PROJECT).stdout
    d = json.loads(out)
    return d["seeds"], d["record"]


def topic_id_for(name: str) -> str:
    """xpol reports topic names; map back to the OpenAlex id via its frame file."""
    frame = json.load((XPOL_PROJECT / "data" / "openalex_topics.json").open())
    for t in frame:
        if t["name"] == name:
            return t["id"]
    raise KeyError(name)


# -------------------------------------------------------------------- main
def sample_pairs(n_pairs: int, seed: int | None, years=YEARS, verbose=True) -> dict:
    rng = random.Random(seed)
    # Over-draw topics so that dropping Social Sciences and empty pools still leaves n_pairs.
    seeds, xrec = xpol_topics(n_pairs * 3, seed)
    topics = [s for s in seeds if s["stratum"] in STEM_DOMAINS]
    pairs, skipped = [], []
    for t in topics:
        if len(pairs) >= n_pairs:
            break
        tid = topic_id_for(t["name"])
        yrs = list(range(years[0], years[1] + 1))
        rng.shuffle(yrs)
        done = False
        for year in yrs[:3]:                       # three tries per topic, then give up
            s_case, s_twin = rng.randrange(1 << 30), rng.randrange(1 << 30)
            case, n_case = draw_work(tid, year, f">{CASE_PCT - 1e-9:.4f}", s_case)
            if not case:
                continue
            twin, n_twin = draw_work(tid, year, f"{TWIN_BAND[0]}-{TWIN_BAND[1]}", s_twin)
            if not twin:
                continue
            pairs.append({"topic": t["name"], "topic_id": tid, "path": t["path"],
                          "domain": t["stratum"], "year": year,
                          "pools": {"case": n_case, "twin": n_twin},
                          "draw_seeds": {"case": s_case, "twin": s_twin},
                          "case": case, "twin": twin})
            done = True
            if verbose:
                print(f"[{len(pairs):2d}] {t['name']} ({year})  case={case['id']} p{case['pct']:.4f} "
                      f"c={case['cited_by_count']}  twin={twin['id']} p{twin['pct']:.3f} "
                      f"c={twin['cited_by_count']}  pools={n_case}/{n_twin}", file=sys.stderr)
            break
        if not done:
            skipped.append(t["name"])
    return {
        "kind": "sample",
        "date": date.today().isoformat(),
        "seed": seed,
        "xpol_record": xrec,
        "params": {"years": list(years), "case_pct": CASE_PCT, "twin_band": list(TWIN_BAND),
                   "min_refs": MIN_REFS, "domains": list(STEM_DOMAINS), "type": "article"},
        "n_pairs": len(pairs),
        "skipped_topics": skipped,
        "pairs": pairs,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.sample")
    ap.add_argument("--pairs", type=int, default=5)
    ap.add_argument("--seed", type=int, default=None, help="RNG seed (default: OS entropy, logged)")
    ap.add_argument("--out", default=None, help="JSON output path (default: stdout)")
    a = ap.parse_args(argv)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 62)
    rec = sample_pairs(a.pairs, seed)
    txt = json.dumps(rec, indent=1, ensure_ascii=False)
    if a.out:
        p = Path(a.out); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(txt)
        print(f"{rec['n_pairs']} pairs, seed {seed} -> {p}", file=sys.stderr)
    else:
        print(txt)


if __name__ == "__main__":
    main()
