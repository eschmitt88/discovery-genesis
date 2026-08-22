"""Stage 3: bibliometric features per work, computed from the raw bundle.

    uv run python -m genesis.features data/samples/pilot.json --out data/features/pilot.csv

One row per work (case and twin), plus `pair` and `role` columns so the
paired comparison (H1) is a one-liner. Nothing here reads the paper text.

Features
    n_refs, n_authors, n_institutions
    ref_age_median, ref_age_mean, ref_share_le3  (refs published within 3 years before the paper)
    ref_cross_topic, ref_cross_subfield, ref_cross_field, ref_cross_domain
                                                  (share of refs whose primary topic differs
                                                  from the focal paper's at that level)
    ref_n_fields                                   distinct fields among refs
    ref_hot_median                                 median citation count of the refs (hotspot-ness)
    ref_fwci_median                                median field-weighted citation impact of refs
    cd_nok, cd5_nok                                disruption without the k-term:
                                                  (n_i - n_j)/(n_i + n_j), where n_i = citers that cite
                                                  none of the focal paper's refs, n_j = citers that
                                                  cite at least one; cd5 = citers within 5 years
    n_citers, citers_capped
    s2_influential, s2_method_cites, s2_ref_method_share   Semantic Scholar intents if present
    has_text, text_chars
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics as st
import sys
from pathlib import Path

from .fetch import RAW, wid


def level(pt: dict | None, key: str):
    if not pt:
        return None
    if key == "topic":
        return pt.get("id")
    return (pt.get(key) or {}).get("id")


def features_for(w: str) -> dict:
    d = RAW / w
    work = json.load((d / "work.json").open())
    refs = json.load((d / "refs.json").open()) if (d / "refs.json").exists() else []
    citers = json.load((d / "citers.json").open()) if (d / "citers.json").exists() else []
    status = json.load((d / "status.json").open()) if (d / "status.json").exists() else {}
    s2 = json.load((d / "s2.json").open()) if (d / "s2.json").exists() else None
    year = work["publication_year"]
    pt = work.get("primary_topic") or {}
    f = {"id": w, "year": year, "title": work.get("title"), "n_refs": work.get("referenced_works_count"),
         "n_authors": len(work.get("authorships") or []),
         "n_institutions": len({i.get("id") for a in (work.get("authorships") or [])
                                for i in (a.get("institutions") or [])}),
         "pct": (work.get("citation_normalized_percentile") or {}).get("value"),
         "cited_by_count": work.get("cited_by_count"), "fwci": work.get("fwci")}

    ages = [year - r["publication_year"] for r in refs if r.get("publication_year")]
    f["ref_age_median"] = st.median(ages) if ages else None
    f["ref_age_mean"] = round(st.mean(ages), 2) if ages else None
    f["ref_share_le3"] = round(sum(a <= 3 for a in ages) / len(ages), 3) if ages else None
    for lvl in ("topic", "subfield", "field", "domain"):
        mine = level(pt, lvl)
        vals = [level(r.get("primary_topic"), lvl) for r in refs if r.get("primary_topic")]
        f[f"ref_cross_{lvl}"] = round(sum(v != mine for v in vals) / len(vals), 3) if vals else None
    f["ref_n_fields"] = len({level(r.get("primary_topic"), "field") for r in refs if r.get("primary_topic")})
    hot = [r["cited_by_count"] for r in refs if r.get("cited_by_count") is not None]
    f["ref_hot_median"] = st.median(hot) if hot else None
    fw = [r["fwci"] for r in refs if r.get("fwci") is not None]
    f["ref_fwci_median"] = round(st.median(fw), 2) if fw else None

    refset = {wid(r) for r in work.get("referenced_works", [])}
    def cd(cs):
        if not cs:
            return None
        nj = sum(any(wid(x) in refset for x in c.get("referenced_works", [])) for c in cs)
        ni = len(cs) - nj
        return round((ni - nj) / (ni + nj), 3)
    f["n_citers"] = len(citers) if (d / "citers.json").exists() else None
    f["citers_capped"] = status.get("citers_capped", False)
    f["cd_nok"] = cd(citers) if citers else None
    f["cd5_nok"] = (cd([c for c in citers if c.get("publication_year") and c["publication_year"] <= year + 5])
                    if citers else None)

    if s2:
        f["s2_influential"] = s2["paper"].get("influentialCitationCount")
        cits = s2.get("citations", [])
        f["s2_method_cites"] = sum("methodology" in (c.get("intents") or []) for c in cits)
        rr = s2.get("references", [])
        f["s2_ref_method_share"] = round(sum("methodology" in (r.get("intents") or []) for r in rr) / len(rr), 3) if rr else None
    ft = status.get("fulltext") or {}
    f["has_text"] = bool(ft.get("chars"))
    f["text_chars"] = ft.get("chars")
    return f


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.features")
    ap.add_argument("sample")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rec = json.load(open(a.sample))
    rows = []
    for k, p in enumerate(rec["pairs"]):
        for role in ("case", "twin"):
            w = p[role]["id"]
            if not (RAW / w / "work.json").exists():
                print(f"missing bundle {w}", file=sys.stderr); continue
            r = {"pair": k, "role": role, "topic": p["topic"], "domain": p["domain"]}
            r.update(features_for(w)); rows.append(r)
    cols = list(rows[0].keys())
    for r in rows:
        for c in r:
            if c not in cols:
                cols.append(c)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols); wr.writeheader(); wr.writerows(rows)
    print(f"{len(rows)} rows -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
