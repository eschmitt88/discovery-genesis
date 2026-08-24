"""Stage 1 of the pipeline: draw case/twin pairs.

    uv run python -m genesis.sample --pairs 20 --seed 123 --out data/samples/pilot.json

Topic draw: the `xpol` sampler from llm-cross-pollination (OpenAlex topic
frame, stratified by domain, OS-entropy or logged seed), filtered to the
STEM domains. Per topic: a random year in YEARS; one impactful paper
(top 1 % by citation rank within the topic-year pool of articles) and one
twin (same pool, rank in the TWIN_BAND fraction), each drawn uniformly by a
seeded RNG over ranks. Pools under MIN_POOL articles are skipped — OpenAlex's
own percentile and topic tags are noisy in small topic-years. Everything needed to
reproduce a draw is in the output record.
"""
from __future__ import annotations

import argparse
import json
import os
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
    "abstract_inverted_index", "primary_location",
])

# ---- primary-research filter -------------------------------------------------
# The top 1 % of `type:article` in a topic-year is mostly reviews, guidelines and
# perspectives (pilot A: >= 8 of 15). OpenAlex's `type:review` catches few of
# them, so we classify from title + abstract + venue and log the share.
import re
TITLE_REVIEW = re.compile(
    r"\b(review|reviews|reviewed|perspective|perspectives|guideline|guidelines|overview|"
    r"update|advances|progress|state[- ]of[- ]the[- ]art|status|roadmap|consensus|"
    r"recommendations|trends|current concepts|primer|tutorial|anniversary|"
    r"challenges and opportunities|opportunities and challenges|where do we stand|"
    r"past, present|lessons learned|what we know|a critical|a comprehensive|"
    r"meta-analysis|systematic|position paper|white paper|handbook|encyclopedia)\b", re.I)
ABSTRACT_REVIEW = re.compile(
    r"\b(this (review|perspective|article|paper|chapter) (reviews|summarizes|summarises|surveys|"
    r"highlights|discusses|provides an overview|gives an overview|focuses on recent)|"
    r"we (review|summarize|summarise|survey|provide an overview|give an overview|highlight recent)|"
    r"(are|is) reviewed|recent (advances|progress|developments) (in|on)|"
    r"(this|the present) (review|overview|survey)|in this review|"
    r"systematic review|meta-analysis|practice guideline|clinical practice guidelines)\b", re.I)
# Review *journals* only — must not match Physical Review, Review of Scientific Instruments, etc.
VENUE_REVIEW = re.compile(r"(annual review|nature reviews|chemical reviews|chemical society reviews|"
                          r"critical reviews|reviews in\b|\breviews$|^trends in|current opinion|"
                          r"^progress in|^advances in|reports on progress|\bsurveys\b|perspectives$)", re.I)


def abstract_text(inv: dict | None) -> str:
    if not inv:
        return ""
    pos = {}
    for word, ps in inv.items():
        for q in ps:
            pos[q] = word
    return " ".join(pos[i] for i in sorted(pos))


def classify(w: dict) -> tuple[str, str]:
    """('primary' | 'review', reason). Conservative: anything that looks like a
    review / guideline / perspective / survey is excluded from both cases and twins."""
    if w.get("type") == "review":
        return "review", "openalex type=review"
    t = w.get("title") or ""
    m = TITLE_REVIEW.search(t)
    if m:
        return "review", f"title:{m.group(0)}"
    ab = abstract_text(w.get("abstract_inverted_index"))
    m = ABSTRACT_REVIEW.search(ab)
    if m:
        return "review", f"abstract:{m.group(0)}"
    venue = (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")
    m = VENUE_REVIEW.search(venue)
    if m:
        return "review", f"venue:{venue}"
    return "primary", ""


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
        "topic_score": pt.get("score"),
        "field": (pt.get("field") or {}).get("display_name"),
        "domain": (pt.get("domain") or {}).get("display_name"),
        "oa_url": (w.get("open_access") or {}).get("oa_url"),
        "is_oa": (w.get("open_access") or {}).get("is_oa"),
        "venue": (((w.get("primary_location") or {}).get("source") or {}).get("display_name")),
    }


MIN_POOL = 500                    # articles in the topic-year; below this the tail is noise
CASE_MIN_CITES = 20               # sanity floor: a "top 1%" paper with fewer is a data artefact


def pool_filter(topic_id: str, year: int) -> str:
    return (f"primary_topic.id:{topic_id},publication_year:{year},type:article,"
            f"is_retracted:false,referenced_works_count:>{MIN_REFS - 1}")


def ranked_page(flt: str, page: int) -> list[dict]:
    """Works sorted by citations desc, 200 per page (basic paging, <= 10k results)."""
    d = openalex({"filter": flt, "sort": "cited_by_count:desc", "per-page": 200,
                  "page": page, "select": SELECT})
    return d["results"]


def draw_by_rank(topic_id: str, year: int, band: tuple[float, float], rng: random.Random,
                 primary_only: bool = True) -> tuple[dict | None, dict]:
    """Uniform draw among PRIMARY-research works whose citation rank (within the
    topic-year pool of articles) falls in `band` (fractions of the pool, 0 = most
    cited). Own ranking — OpenAlex's citation_normalized_percentile is unreliable in
    the tail of small topic-years. Reviews/guidelines/perspectives in the band are
    counted and logged, then excluded. Basic paging caps at 10k results."""
    flt = pool_filter(topic_id, year)
    n = openalex({"filter": flt, "per-page": 1, "select": "id"})["meta"]["count"]
    info = {"pool": n}
    if n < MIN_POOL:
        return None, info
    lo, hi = int(band[0] * n), max(int(band[1] * n) - 1, int(band[0] * n))
    hi = min(hi, 9999)
    works = []
    for page in range(lo // 200 + 1, hi // 200 + 2):
        works += [(rank, w) for rank, w in enumerate(ranked_page(flt, page), start=(page - 1) * 200)
                  if lo <= rank <= hi]
    eligible, reviews = [], []
    for rank, w in works:
        kind, why = classify(w)
        (eligible if (kind == "primary" or not primary_only) else reviews).append((rank, w, why))
    info.update({"band_ranks": [lo, hi], "n_band": len(works), "n_review": len(reviews),
                 "review_share": round(len(reviews) / len(works), 3) if works else None,
                 "reviews": [{"rank": r, "title": (w.get("title") or "")[:80], "why": why}
                             for r, w, why in reviews][:30]})
    if not eligible:
        return None, info
    rank, w, _ = rng.choice(eligible)
    out = slim(w); out["rank"] = rank; out["pool"] = n
    info["rank"] = rank
    return out, info


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
            case, ci = draw_by_rank(tid, year, (0.0, 1 - CASE_PCT), rng)
            if not case or (case["cited_by_count"] or 0) < CASE_MIN_CITES:
                continue
            twin, ti = draw_by_rank(tid, year, TWIN_BAND, rng)
            if not twin:
                continue
            flags = []
            if (case.get("topic_score") or 1) < 0.7:
                flags.append("case_topic_score<0.7")
            if (twin.get("topic_score") or 1) < 0.7:
                flags.append("twin_topic_score<0.7")
            pairs.append({"topic": t["name"], "topic_id": tid, "path": t["path"],
                          "domain": t["stratum"], "year": year, "pool": ci["pool"],
                          "ranks": {"case": ci.get("rank"), "twin": ti.get("rank"),
                                    "case_band": ci.get("band_ranks"), "twin_band": ti.get("band_ranks")},
                          "review_filter": {"case_band": {k: ci.get(k) for k in ("n_band", "n_review", "review_share", "reviews")},
                                            "twin_band": {k: ti.get(k) for k in ("n_band", "n_review", "review_share")}},
                          "flags": flags, "case": case, "twin": twin})
            done = True
            if verbose:
                print(f"[{len(pairs):2d}] {t['name']} ({year}) pool={ci['pool']} reviews_in_top1%={ci['n_review']}/{ci['n_band']}  "
                      f"case={case['id']} r{ci['rank']} c={case['cited_by_count']} oa={case['is_oa']}  "
                      f"twin={twin['id']} r{ti['rank']} c={twin['cited_by_count']}  {' '.join(flags)}\n"
                      f"      {case['title'][:100]}", file=sys.stderr)
            break
        if not done:
            skipped.append(t["name"])
    return {
        "kind": "sample",
        "date": date.today().isoformat(),
        "seed": seed,
        "xpol_record": xrec,
        "params": {"years": list(years), "case_band": [0.0, 1 - CASE_PCT], "twin_band": list(TWIN_BAND),
                   "min_refs": MIN_REFS, "min_pool": MIN_POOL, "case_min_cites": CASE_MIN_CITES,
                   "ranking": "own cited_by_count rank within primary_topic × year × type:article",
                   "primary_only": True, "review_filter": "title/abstract/venue regex + openalex type (genesis.sample.classify)",
                   "domains": list(STEM_DOMAINS), "type": "article"},
        "n_pairs": len(pairs),
        "skipped_topics": skipped,
        "pairs": pairs,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.sample")
    ap.add_argument("--pairs", type=int, default=5)
    ap.add_argument("--seed", type=int, default=None, help="RNG seed (default: OS entropy, logged)")
    ap.add_argument("--out", default=None, help="JSON output path (default: stdout)")
    ap.add_argument("--holdout", type=int, default=0,
                    help="move the LAST N pairs to test/samples/<name>-heldout.json (HCE split, never read during search)")
    a = ap.parse_args(argv)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 62)
    rec = sample_pairs(a.pairs, seed)
    if not a.out:
        print(json.dumps(rec, indent=1, ensure_ascii=False)); return
    p = Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    if a.holdout:
        held = dict(rec, pairs=rec["pairs"][-a.holdout:], n_pairs=a.holdout, split="test")
        rec = dict(rec, pairs=rec["pairs"][:-a.holdout], n_pairs=len(rec["pairs"]) - a.holdout, split="dev")
        hp = Path("test/samples") / (p.stem + "-heldout.json"); hp.parent.mkdir(parents=True, exist_ok=True)
        hp.write_text(json.dumps(held, indent=1, ensure_ascii=False))
        print(f"{a.holdout} pairs held out -> {hp}", file=sys.stderr)
    p.write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(f"{rec['n_pairs']} pairs, seed {seed} -> {p}", file=sys.stderr)


if __name__ == "__main__":
    main()
