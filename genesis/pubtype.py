"""Independent review/primary signals, because the title+abstract+venue regex in
`genesis.sample.classify` has poor recall.

    uv run python -m genesis.pubtype data/samples/main50.json [--out data/pubtypes.json]

The regex was built on pilot A, where reviews announced themselves ("… : A
Review", *Chemical Reviews*). At n = 50 it flagged 0 of 100 works while the
sample's own reference counts show obvious reviews at the top (489, 401, 294
references, none with "review" in the title or venue). Precision was fine;
recall is the problem.

Three signals, none of them the feature under test (reference count):

  s2_types      Semantic Scholar `publicationTypes` — carries "Review" for
                many works OpenAlex types as `article`.
  epmc_type     Europe PMC `pubTypeList` — the biomedical authority.
  crossref_type Crossref `type` plus its `subtype`.

Writes one record per work id. Nothing here filters; the sampler and the
analysis decide what to do with the flags, and the coders' blind `is_primary`
field remains the arbiter of record.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

from .fetch import EPMC, ROOT, S2, get, s2_get

OUT = ROOT / "data" / "pubtypes.json"
REVIEW_WORDS = ("review", "meta-analysis", "systematic", "editorial", "comment",
                "letter", "news", "guideline", "practice guideline", "consensus")


def signals(w: str, work: dict) -> dict:
    doi = (work.get("doi") or "").replace("https://doi.org/", "")
    rec = {"id": w, "openalex_type": work.get("type"), "n_refs": work.get("referenced_works_count")}
    if not doi:
        return rec
    r = s2_get(f"{S2}/DOI:{urllib.parse.quote(doi)}?fields=publicationTypes,title")
    if r:
        rec["s2_types"] = r.get("publicationTypes")
    time.sleep(3.5)
    try:
        e = get(f"{EPMC}search?query={urllib.parse.quote('DOI:' + doi)}&format=json&resultType=core",
                timeout=40, retries=2)
    except Exception:                          # noqa: BLE001
        e = None
    for hit in ((e or {}).get("resultList") or {}).get("result") or []:
        pt = (hit.get("pubTypeList") or {}).get("pubType")
        if pt:
            rec["epmc_types"] = pt if isinstance(pt, list) else [pt]
        break
    try:
        c = get("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=40, retries=2)
    except Exception:                          # noqa: BLE001
        c = None
    m = (c or {}).get("message") or {}
    if m:
        rec["crossref_type"] = m.get("type")
        rec["crossref_subtype"] = m.get("subtype")
    flags = []
    for key in ("s2_types", "epmc_types"):
        for t in (rec.get(key) or []):
            if any(word in str(t).lower() for word in REVIEW_WORDS):
                flags.append(f"{key}:{t}")
    if str(rec.get("crossref_type", "")).lower() in ("review", "peer-review") or \
       any(word in str(rec.get("crossref_subtype", "")).lower() for word in REVIEW_WORDS):
        flags.append(f"crossref:{rec.get('crossref_type')}/{rec.get('crossref_subtype')}")
    if rec.get("openalex_type") == "review":
        flags.append("openalex:review")
    rec["review_flags"] = flags
    rec["is_review_signal"] = bool(flags)
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.pubtype")
    ap.add_argument("sample", nargs="+")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--from-sample", action="store_true",
                    help="type works straight from the sample record (doi/type/n_refs are all "
                         "signals() needs) instead of requiring a fetched bundle — lets a large "
                         "draw be screened BEFORE paying to fetch it")
    a = ap.parse_args(argv)
    from .fetch import RAW
    out = Path(a.out)
    store = json.load(out.open()) if out.exists() else {}
    ids, from_sample = [], {}
    for f in a.sample:
        for p in json.load(open(f))["pairs"]:
            for role in ("case", "twin"):
                ids.append(p[role]["id"])
                from_sample[p[role]["id"]] = {
                    "doi": p[role].get("doi"), "type": p[role].get("type"),
                    "referenced_works_count": p[role].get("n_refs")}
    if a.from_sample:
        todo = [w for w in ids if w not in store]
    else:
        todo = [w for w in ids if w not in store and (RAW / w / "work.json").exists()]
    print(f"{len(todo)} works to type ({len(ids) - len(todo)} cached)", file=sys.stderr)
    for i, w in enumerate(todo, 1):
        work = (from_sample[w] if a.from_sample
                else json.load((RAW / w / "work.json").open()))
        store[w] = signals(w, work)
        if i % 5 == 0 or i == len(todo):
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(store, indent=1))
        f = store[w]["review_flags"]
        print(f"[{i}/{len(todo)}] {w} refs={store[w]['n_refs']} "
              f"{'REVIEW ' + ','.join(f)[:60] if f else 'primary'}", file=sys.stderr)
    out.write_text(json.dumps(store, indent=1))
    n = sum(1 for v in store.values() if v.get("is_review_signal"))
    print(f"{n}/{len(store)} flagged as review by an external signal", file=sys.stderr)


if __name__ == "__main__":
    main()
