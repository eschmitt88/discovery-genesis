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


def build(w: str, with_citers: bool, max_chars: int) -> str:
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
    L += ["## Abstract", "", work.get("abstract") or "(no abstract in OpenAlex)", ""]

    # S2 intents keyed by DOI or title
    intents = {}
    if s2:
        for r in (s2.get("references") or []):
            cp = r.get("citedPaper") or {}
            key = ((cp.get("externalIds") or {}).get("DOI") or "").lower() or (cp.get("title") or "").lower()
            if key:
                intents[key] = {"intents": r.get("intents") or [], "influential": r.get("isInfluential"),
                                "contexts": r.get("contexts") or []}
    L += ["## References (by year)", ""]
    for r in sorted(refs, key=lambda r: (r.get("publication_year") or 0, r.get("title") or "")):
        rt = (r.get("primary_topic") or {})
        key = (r.get("doi") or "").replace("https://doi.org/", "").lower() or (r.get("title") or "").lower()
        it = intents.get(key, {})
        tag = ""
        if it.get("intents"):
            tag = f"  «{'/'.join(it['intents'])}{'; influential' if it.get('influential') else ''}»"
        L.append(f"- [{r.get('publication_year')}] {r.get('title')}  — *{rt.get('display_name')}* "
                 f"({(rt.get('field') or {}).get('display_name')}); cited {r.get('cited_by_count')}×{tag}")
        for c in it.get("contexts", [])[:2]:
            L.append(f"    > {c.strip()[:300]}")
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
    a = ap.parse_args(argv)
    rec = json.load(open(a.sample))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in rec["pairs"]:
        for role in ("case", "twin"):
            w = p[role]["id"]
            if not (RAW / w / "work.json").exists():
                print(f"missing bundle {w}", file=sys.stderr); continue
            (out / f"{w}.md").write_text(build(w, a.with_citers, a.max_chars)); n += 1
    print(f"{n} dossiers -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
