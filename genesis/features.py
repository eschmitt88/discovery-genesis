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


BG = ROOT / "data" / "background"


def load_background(topic_id: str, year: int) -> dict | None:
    p = BG / f"{topic_id}-{year}.json"
    return json.load(p.open()) if p.exists() else None


def atypicality(refs: list[dict], bg: dict) -> dict:
    """Map the focal paper's referenced subfield pairs onto the pool's pair z-table.
    A pair both of whose subfields occur in the background but which never
    co-occur there gets the z of obs = 0 (−sqrt(exp)); a pair involving a
    subfield absent from the background is unscorable and dropped (counted)."""
    from itertools import combinations
    import math
    sfs = sorted({((r.get("primary_topic") or {}).get("subfield") or {}).get("id", "").rsplit("/", 1)[-1]
                  for r in refs if (r.get("primary_topic") or {}).get("subfield")})
    sfs = [x for x in sfs if x]
    zt, freq, n = bg["pairs"]["pair_z"], bg["pairs"]["subfield_freq"], bg["pairs"]["n_works"]
    zs, unscorable = [], 0
    for a, b in combinations(sfs, 2):
        key = "|".join(sorted((a, b)))
        if key in zt and zt[key] is not None:
            zs.append(zt[key])
        elif a in freq and b in freq and n:
            exp = n * (freq[a] / n) * (freq[b] / n)
            zs.append(round(-math.sqrt(exp), 3) if exp > 0 else 0.0)
        else:
            unscorable += 1
    if not zs:
        return {"atyp_n_pairs": 0, "atyp_unscorable": unscorable}
    zs.sort()
    return {"atyp_n_pairs": len(zs), "atyp_unscorable": unscorable,
            "atyp_median_z": round(st.median(zs), 3),
            "atyp_p10_z": round(zs[max(0, int(0.1 * len(zs)) - 1)] if len(zs) >= 10 else zs[0], 3),
            "atyp_share_novel": round(sum(z < 0 for z in zs) / len(zs), 3)}


def features_for(w: str, topic_id: str | None = None, year_hint: int | None = None) -> dict:
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

    bg = load_background(topic_id, year) if topic_id else None
    if bg:
        ps = bg["stats"]
        f["pool_ref_age_median"] = ps.get("pool_ref_age_median")
        f["pool_ref_share_le3"] = ps.get("pool_ref_share_le3")
        f["pool_ref_hot_median"] = ps.get("pool_ref_hot_median")
        if f["ref_age_median"] is not None and ps.get("pool_ref_age_median") is not None:
            f["ref_age_vs_pool"] = round(f["ref_age_median"] - ps["pool_ref_age_median"], 2)
        if f["ref_share_le3"] is not None and ps.get("pool_ref_share_le3") is not None:
            f["ref_share_le3_vs_pool"] = round(f["ref_share_le3"] - ps["pool_ref_share_le3"], 3)
        if f["ref_hot_median"] is not None and ps.get("pool_ref_hot_median"):
            f["ref_hot_vs_pool"] = round(f["ref_hot_median"] / ps["pool_ref_hot_median"], 3)
        f.update(atypicality(refs, bg))
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
            r.update(features_for(w, p.get("topic_id"), p.get("year"))); rows.append(r)
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
