"""Stage 4: build a coder dossier — everything a genesis-card coder may see,
and nothing it may not.

    uv run python -m genesis.dossier data/samples/pilot.json --out data/dossiers/pilot

One Markdown file per work. Contents, in order: bibliographic header,
abstract, the reference list (title, year, topic, citations — sorted by the
paper's own reference order is unknown, so by year), Semantic Scholar
citation *intents* for each reference where present (which refs the paper
uses as method / background / result), and — only if --with-citers — the
contexts in which later papers cite this one (what the field took from it).
Full text is appended when present, truncated to --max-chars.

The dossier deliberately omits: citation counts of the focal paper, its
percentile/rank, and the twin's identity. Coders must not know which member
of a pair is the impactful one. The file name is the OpenAlex id only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .fetch import RAW, wid


REF_CAP = 60                       # show every reference up to this many
REF_KEEP_RECENT = 22               # beyond it: the most recent ...
REF_KEEP_CITED = 22                # ... plus the most cited, deduped


def _select_refs(refs: list[dict], compact: bool) -> tuple[list[dict], str]:
    """Long reference lists dominate dossier size (p90 is 67 kB, max 3 MB) without
    adding coding signal: what a coder needs is what the paper builds on *recently*
    and what it leans on *heavily*. Above REF_CAP, keep the most recent and the most
    cited and say plainly what was dropped, so the omission is visible rather than
    silent."""
    if not compact or len(refs) <= REF_CAP:
        return refs, ""
    recent = sorted(refs, key=lambda r: (r.get("publication_year") or 0), reverse=True)[:REF_KEEP_RECENT]
    cited = sorted(refs, key=lambda r: (r.get("cited_by_count") or 0), reverse=True)[:REF_KEEP_CITED]
    selfc = [r for r in refs if r.get("_self")][:10]
    keep, seen = [], set()
    for r in recent + cited + selfc:
        k = r.get("id") or r.get("title")
        if k not in seen:
            seen.add(k); keep.append(r)
    years = [r["publication_year"] for r in refs if r.get("publication_year")]
    cites = [r["cited_by_count"] for r in refs if r.get("cited_by_count") is not None]
    import statistics as _st
    note = (f"\n**Showing {len(keep)} of {len(refs)} references** — the most recent and the most "
            f"cited (plus self-citations). Whole list: median year "
            f"{int(_st.median(years)) if years else '?'}, median citations "
            f"{int(_st.median(cites)) if cites else '?'}, "
            f"{sum(1 for r in refs if r.get('_self'))} self-cited.\n")
    return keep, note


def build(w: str, with_citers: bool, max_chars: int, compact: bool = False) -> str:
    d = RAW / w
    work = json.load((d / "work.json").open())
    refs = json.load((d / "refs.json").open()) if (d / "refs.json").exists() else []
    s2 = json.load((d / "s2.json").open()) if (d / "s2.json").exists() else None
    status = json.load((d / "status.json").open()) if (d / "status.json").exists() else {}
    pt = work.get("primary_topic") or {}
    auth = [a.get("author", {}).get("display_name") for a in work.get("authorships") or []]
    inst = sorted({i.get("display_name") for a in (work.get("authorships") or []) for i in (a.get("institutions") or []) if i.get("display_name")})
    L = [f"# {work.get('title')}", "",
         f"- id: {w}", f"- year: {work.get('publication_year')}",
         f"- venue: {((work.get('primary_location') or {}).get('source') or {}).get('display_name')}",
         f"- authors ({len(auth)}): {', '.join(a for a in auth if a)}",
         f"- institutions: {'; '.join(inst)}",
         f"- primary topic: {pt.get('display_name')}  [{(pt.get('subfield') or {}).get('display_name')} / {(pt.get('field') or {}).get('display_name')}]",
         f"- all topics: {', '.join(t.get('display_name') for t in (work.get('topics') or []))}",
         f"- references: {work.get('referenced_works_count')}", ""]
    ab, ab_note = work.get("abstract"), ""
    ab_p = d / "abstract.json"
    if not ab and ab_p.exists():
        rec = json.load(ab_p.open())
        ab = rec["text"]
        ab_note = (" — **machine-generated summary (Semantic Scholar TLDR), not the authors' abstract**"
                   if rec.get("generated") else f" (via {rec['source']})")
    L += [f"## Abstract{ab_note}", "",
          ab or "(no abstract available from OpenAlex, Semantic Scholar, Europe PMC or Crossref — "
                "code from the title, reference list and citation contexts)", ""]

    # S2 intents keyed by DOI or title
    intents = {}
    if s2:
        for r in (s2.get("references") or []):
            cp = r.get("citedPaper") or {}
            key = ((cp.get("externalIds") or {}).get("DOI") or "").lower() or (cp.get("title") or "").lower()
            if key:
                intents[key] = {"intents": r.get("intents") or [], "influential": r.get("isInfluential"),
                                "contexts": r.get("contexts") or []}
    # Self-citation marking. The v1.1 codebook's means-first / problem-first rule
    # turns on whether a capability is new to the AUTHORS, and coders reported that
    # the dossier gave them no way to see it. Mark any reference sharing an author
    # (OpenAlex author id, or normalised surname+initial as a fallback) with the
    # focal paper, and summarise the count per author cluster.
    def author_keys(rec):
        ids, names = set(), set()
        for a in (rec.get("authorships") or []):
            au = a.get("author") or {}
            if au.get("id"):
                ids.add(au["id"].rsplit("/", 1)[-1])
            dn = (au.get("display_name") or "").strip().lower()
            if dn:
                parts = dn.replace(".", " ").split()
                if len(parts) >= 2:
                    names.add(parts[-1] + "|" + parts[0][:1])
        return ids, names

    focal_ids, focal_names = author_keys(work)
    self_cited = 0
    for r in refs:
        rid, rname = author_keys(r)
        r["_self"] = bool((focal_ids & rid) or (focal_names & rname))
        self_cited += r["_self"]
    shown, note = _select_refs(refs, compact)
    L += [f"## References (by year) — {self_cited} of {len(refs)} share an author with this paper "
          f"(marked **SELF**)", note, ""]
    for r in sorted(shown, key=lambda r: (r.get("publication_year") or 0, r.get("title") or "")):
        rt = (r.get("primary_topic") or {})
        key = (r.get("doi") or "").replace("https://doi.org/", "").lower() or (r.get("title") or "").lower()
        it = intents.get(key, {})
        tag = ""
        if it.get("intents"):
            tag = f"  «{'/'.join(it['intents'])}{'; influential' if it.get('influential') else ''}»"
        L.append(f"- [{r.get('publication_year')}]{' **SELF**' if r.get('_self') else ''} {r.get('title')}"
                 f"  — *{rt.get('display_name')}* "
                 f"({(rt.get('field') or {}).get('display_name')}); cited {r.get('cited_by_count')}×{tag}")
        for c in it.get("contexts", [])[:(1 if compact else 2)]:
            L.append(f"    > {c.strip()[:(160 if compact else 300)]}")
    L.append("")
    if with_citers and s2 and (s2.get("citations") or []):
        L += ["## How later papers cite this one (Semantic Scholar contexts; sample)", ""]
        n = 0
        for c in s2["citations"]:
            for ctx in (c.get("contexts") or [])[:1]:
                cp = c.get("citingPaper") or {}
                L.append(f"- [{cp.get('year')}] «{'/'.join(c.get('intents') or [])}» {ctx.strip()[:300]}")
                n += 1
            if n >= 40:
                break
        L.append("")
    txt_p = d / "fulltext.txt"
    if txt_p.exists():
        t = txt_p.read_text(errors="replace")
        L += ["## Full text (open-access copy; may be truncated)", "", t[:max_chars]]
        if len(t) > max_chars:
            L.append(f"\n[... truncated at {max_chars} of {len(t)} characters]")
    else:
        L += ["## Full text", "", f"(not available — {json.dumps(status.get('fulltext'))}; code from abstract, references and citation contexts)"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.dossier")
    ap.add_argument("sample")
    ap.add_argument("--out", required=True)
    ap.add_argument("--with-citers", action="store_true", help="include how later papers cite it (hindsight risk — use for impact coding only)")
    ap.add_argument("--max-chars", type=int, default=120_000)
    ap.add_argument("--compact", action="store_true",
                    help="cap the reference list and full text so a large sample can be coded "
                         "affordably; validate against full dossiers before trusting it")
    a = ap.parse_args(argv)
    rec = json.load(open(a.sample))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in rec["pairs"]:
        for role in ("case", "twin"):
            w = p[role]["id"]
            if not (RAW / w / "work.json").exists():
                print(f"missing bundle {w}", file=sys.stderr); continue
            (out / f"{w}.md").write_text(
                build(w, a.with_citers, a.max_chars, compact=a.compact)); n += 1
    print(f"{n} dossiers -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
