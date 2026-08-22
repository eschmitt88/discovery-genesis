"""Stage 2: build the raw bundle for every work in a sample file.

    uv run python -m genesis.fetch data/samples/pilot.json [--max-citers 3000] [--no-text]

For each case and twin writes raw/cases/<W-id>/ :
    work.json       full OpenAlex record (+ reconstructed abstract)
    refs.json       OpenAlex records of the referenced works (topic, year, citations)
    citers.json     works citing it: id, year, referenced_works (for the disruption index)
    s2.json         Semantic Scholar: references with intents/contexts, citation contexts,
                    influential-citation count  (best effort; skipped on 404)
    fulltext.pdf / fulltext.txt   open-access text if any location yields a real PDF
    status.json     what was fetched, when, from where

raw/ is immutable: an existing file is never overwritten — re-running only
fills gaps. Delete the folder to refetch.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .sample import UA, openalex

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "cases"
S2 = "https://api.semanticscholar.org/graph/v1/paper"
UNPAYWALL = "https://api.unpaywall.org/v2/"
MAILTO = "eschmitt88@gmail.com"
WORK_SELECT = ",".join([
    "id", "doi", "title", "display_name", "publication_year", "publication_date", "type",
    "cited_by_count", "citation_normalized_percentile", "cited_by_percentile_year",
    "referenced_works", "referenced_works_count", "related_works", "primary_topic", "topics",
    "keywords", "concepts", "open_access", "locations", "best_oa_location", "authorships",
    "abstract_inverted_index", "biblio", "ids", "is_retracted", "counts_by_year",
    "primary_location", "language", "fwci",
])
REF_SELECT = ",".join([
    "id", "doi", "title", "publication_year", "type", "cited_by_count", "primary_topic",
    "referenced_works_count", "authorships", "fwci",
])
CITER_SELECT = "id,publication_year,referenced_works,primary_topic,cited_by_count"
CITER_WINDOW = 5                   # years after publication; CD5 is the index we report


# ----------------------------------------------------------------- helpers
def get(url: str, headers: dict | None = None, timeout=60, retries=4, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    if headers and "User-Agent" in headers:
        req.add_header("User-Agent", headers["User-Agent"])
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read() if binary else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 400):
                return None
            if e.code == 429:
                time.sleep(5 * (attempt + 1)); continue
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
        except Exception:                      # noqa: BLE001
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None


def abstract_from_index(inv: dict | None) -> str | None:
    if not inv:
        return None
    pos = {}
    for w, ps in inv.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))


def wid(x: str) -> str:
    return x.rsplit("/", 1)[-1]


def write_once(path: Path, obj, binary=False) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        path.write_bytes(obj)
    else:
        path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) if not isinstance(obj, str) else obj)
    return True


# ------------------------------------------------------------------ stages
def fetch_work(w: str) -> dict:
    d = openalex_one(w, WORK_SELECT)
    d["abstract"] = abstract_from_index(d.pop("abstract_inverted_index", None))
    return d


def openalex_one(w: str, select: str) -> dict:
    return get(f"https://api.openalex.org/works/{w}?select={select}&mailto={MAILTO}")


ENTITY_DELAY = 0.2


def fetch_batch(ids: list[str], select: str, log=None) -> list[dict]:
    """Reference records, 50 at a time. OpenAlex throttles *list* queries
    (`?filter=…`) independently of single-entity GETs (`/works/W…`) and can 429
    every list query for hours while entity lookups stay at 200 — so fall back to
    one GET per id rather than losing the bundle. Slower, but it always finishes."""
    out, i = [], 0
    while i < len(ids):
        chunk = ids[i:i + 50]
        try:
            d = openalex({"filter": f"openalex_id:{'|'.join(chunk)}", "select": select,
                          "per-page": 50})
            out.extend(d["results"])
            i += 50
            continue
        except Exception as e:                 # noqa: BLE001
            if log:
                log(f"    batch list query failed ({str(e)[:40]}); falling back to entity GETs")
        for w in chunk:
            try:
                r = openalex_one(w, select)
            except Exception:                  # noqa: BLE001
                r = None
            if r:
                out.append(r)
            time.sleep(ENTITY_DELAY)
        i += 50
    return out


def fetch_citers(w: str, max_citers: int, until_year: int | None = None) -> list[dict]:
    """Citing works, for the disruption index. `until_year` restricts to citers
    published within the CD window — the 5-year index is what the project uses and
    the restriction cuts request volume several-fold on highly cited papers."""
    flt = f"cites:{w}" + (f",publication_year:<{until_year + 1}" if until_year else "")
    out, cursor = [], "*"
    while cursor and len(out) < max_citers:
        d = openalex({"filter": flt, "select": CITER_SELECT, "per-page": 200, "cursor": cursor})
        out.extend(d["results"])
        cursor = d["meta"].get("next_cursor")
    return out[:max_citers]


# Semantic Scholar's unauthenticated pool is ~1 req/s shared across all users, so a
# 429 is normal, not an error. Pace deliberately and treat an empty reference list
# as a failure worth retrying (that is where the citation *intents* live).
S2_SLEEP = 3.5


def s2_get(url: str, tries: int = 6):
    for i in range(tries):
        try:
            r = get(url, timeout=60, retries=1)
        except Exception:                      # noqa: BLE001
            r = None
        if r is not None:
            return r
        time.sleep(S2_SLEEP * (i + 1))
    return None


def fetch_s2(doi: str | None, w: str) -> dict | None:
    key = f"DOI:{doi.replace('https://doi.org/', '')}" if doi else None
    if not key:
        return None
    base = s2_get(f"{S2}/{urllib.parse.quote(key)}?fields=paperId,title,citationCount,"
                  "influentialCitationCount,referenceCount,tldr,fieldsOfStudy,openAccessPdf")
    if not base:
        return None
    time.sleep(S2_SLEEP)
    refs = s2_get(f"{S2}/{base['paperId']}/references?fields=intents,contexts,isInfluential,"
                  "title,year,externalIds,citationCount&limit=999") or {}
    time.sleep(S2_SLEEP)
    cits = s2_get(f"{S2}/{base['paperId']}/citations?fields=intents,contexts,isInfluential,"
                  "title,year,externalIds&limit=500") or {}
    time.sleep(S2_SLEEP)
    return {"paper": base, "references": refs.get("data", []), "citations": cits.get("data", [])}


def pdf_candidates(work: dict) -> list[str]:
    urls = []
    for loc in ([work.get("best_oa_location")] + (work.get("locations") or [])):
        if not loc:
            continue
        for k in ("pdf_url", "landing_page_url"):
            u = loc.get(k)
            if u and u not in urls:
                urls.append(u)
    arx = (work.get("ids") or {}).get("arxiv") or next(
        (u for u in urls if "arxiv.org" in u), None)
    if arx:
        m = re.search(r"(\d{4}\.\d{4,5}|[a-z\-]+/\d{7})", arx)
        if m:
            urls.insert(0, f"https://arxiv.org/pdf/{m.group(1)}")
    doi = work.get("doi")
    if doi:
        up = get(UNPAYWALL + urllib.parse.quote(doi.replace("https://doi.org/", "")) + f"?email={MAILTO}")
        if up:
            for loc in [up.get("best_oa_location")] + (up.get("oa_locations") or []):
                if loc and loc.get("url_for_pdf") and loc["url_for_pdf"] not in urls:
                    urls.append(loc["url_for_pdf"])
    return urls


CROSSREF = "https://api.crossref.org/works/"


def fetch_abstract(work: dict) -> dict | None:
    """OpenAlex lacks an abstract for ~28 % of works (publisher policy). Try, in
    order: Semantic Scholar, Europe PMC, Crossref, and finally Semantic Scholar's
    machine-written TLDR — which is recorded with `generated: true` so a coder is
    never shown a model summary as if it were the authors' own words."""
    doi = (work.get("doi") or "").replace("https://doi.org/", "")
    if not doi:
        return None
    r = s2_get(f"{S2}/DOI:{urllib.parse.quote(doi)}?fields=abstract,tldr")
    if r and r.get("abstract"):
        return {"text": r["abstract"], "source": "semanticscholar", "generated": False}
    tldr = ((r or {}).get("tldr") or {}).get("text")
    for q in (f"DOI:{doi}", f"EXT_ID:{((work.get('ids') or {}).get('pmid') or '').rsplit('/', 1)[-1]} AND SRC:MED"):
        if q.startswith("EXT_ID: "):
            continue
        try:
            e = get(f"{EPMC}search?query={urllib.parse.quote(q)}&format=json&resultType=core", timeout=40, retries=2)
        except Exception:                      # noqa: BLE001
            e = None
        for hit in ((e or {}).get("resultList") or {}).get("result") or []:
            if hit.get("abstractText"):
                return {"text": hit["abstractText"], "source": "europepmc", "generated": False}
    try:
        c = get(CROSSREF + urllib.parse.quote(doi), timeout=40, retries=2)
    except Exception:                          # noqa: BLE001
        c = None
    ab = ((c or {}).get("message") or {}).get("abstract")
    if ab:
        ab = re.sub(r"<[^>]+>", " ", ab)
        return {"text": " ".join(ab.split()), "source": "crossref", "generated": False}
    if tldr:
        return {"text": tldr, "source": "semanticscholar-tldr", "generated": True}
    return None


BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/126.0 Safari/537.36")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/"


def fetch_epmc_text(work: dict) -> str | None:
    """Europe PMC full-text XML -> plain text, for anything with a PMCID (most OA biomed)."""
    pmcid = (work.get("ids") or {}).get("pmcid")
    if not pmcid:
        # OpenAlex often lacks the PMCID; resolve via Europe PMC search by DOI / PMID.
        doi = (work.get("doi") or "").replace("https://doi.org/", "")
        pmid = ((work.get("ids") or {}).get("pmid") or "").rsplit("/", 1)[-1]
        for q in ([f"DOI:{doi}"] if doi else []) + ([f"EXT_ID:{pmid} AND SRC:MED"] if pmid else []):
            try:
                r = get(f"{EPMC}search?query={urllib.parse.quote(q)}&format=json&resultType=lite", timeout=30, retries=2)
            except Exception:                  # noqa: BLE001
                r = None
            hits = ((r or {}).get("resultList") or {}).get("result") or []
            hit = next((h for h in hits if h.get("pmcid")), None)
            if hit:
                pmcid = hit["pmcid"]; break
        if not pmcid:
            return None
    pmcid = pmcid.rsplit("/", 1)[-1].upper()
    if not pmcid.startswith("PMC"):
        pmcid = "PMC" + pmcid
    try:
        raw = get(f"{EPMC}{pmcid}/fullTextXML", timeout=60, retries=2, binary=True)
    except Exception:                          # noqa: BLE001
        return None
    if not raw or b"<body" not in raw:
        return None
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return None
    body = root.find(".//body")
    if body is None:
        return None
    return "\n".join(t for t in body.itertext())


def fetch_pdf(urls: list[str]) -> tuple[bytes | None, str | None]:
    for u in urls:
        try:
            b = get(u, headers={"Accept": "application/pdf,*/*", "User-Agent": BROWSER_UA},
                    timeout=90, retries=1, binary=True)
        except Exception:                      # noqa: BLE001
            b = None
        if b and b[:5] == b"%PDF-" and len(b) > 10_000:
            return b, u
        time.sleep(0.5)
    return None, None


def pdf_text(pdf: Path) -> str:
    from pypdf import PdfReader
    return "\n\n".join((p.extract_text() or "") for p in PdfReader(str(pdf)).pages)


def bundle(w: str, max_citers: int, want_text: bool, log=print, retry_text: bool = False,
           retry_s2: bool = False, want_citers: bool = True) -> dict:
    d = RAW / w
    status_p = d / "status.json"
    status = json.load(status_p.open()) if status_p.exists() else {"id": w}
    t0 = time.time()

    if not (d / "work.json").exists():
        work = fetch_work(w); write_once(d / "work.json", work)
    else:
        work = json.load((d / "work.json").open())

    if not (d / "refs.json").exists():
        refs = fetch_batch([wid(r) for r in work.get("referenced_works", [])], REF_SELECT, log=log)
        write_once(d / "refs.json", refs); status["n_refs_fetched"] = len(refs)

    # Citers are fetched separately: OpenAlex throttles the `cites:` filter far more
    # aggressively than work/reference lookups, and a 429 there must not block the
    # rest of a bundle. `--citers-only` drips them in afterwards.
    if want_citers and not (d / "citers.json").exists():
        try:
            citers = fetch_citers(w, max_citers, until_year=work["publication_year"] + CITER_WINDOW)
        except Exception as e:                 # noqa: BLE001
            status["citers_error"] = str(e)[:120]
        else:
            write_once(d / "citers.json", citers)
            status["n_citers_fetched"] = len(citers)
            status["citers_capped"] = len(citers) >= max_citers
            status["citer_window_years"] = CITER_WINDOW

    ab_p = d / "abstract.json"
    if not work.get("abstract") and not ab_p.exists() and "abstract" not in status:
        ab = fetch_abstract(work)
        status["abstract"] = ab["source"] if ab else "missing"
        if ab:
            write_once(ab_p, ab)

    s2_p = d / "s2.json"
    s2_thin = s2_p.exists() and not (json.load(s2_p.open()).get("references") or [])
    if (not s2_p.exists() and "s2" not in status) or (retry_s2 and s2_thin):
        s2 = fetch_s2(work.get("doi"), w)
        if s2 and (s2.get("references") or not s2_p.exists()):
            if s2_p.exists():
                s2_p.unlink()                  # only ever replaces an empty-reference stub
            write_once(s2_p, s2)
            status["s2"] = "ok"
            status["s2_n_refs"] = len(s2.get("references") or [])
        elif not s2_p.exists():
            status["s2"] = "missing"

    if want_text and not (d / "fulltext.txt").exists() and ("fulltext" not in status or retry_text):
        txt = fetch_epmc_text(work)
        if txt and len(txt) > 5000:
            write_once(d / "fulltext.txt", txt)
            status["fulltext"] = {"source": "europepmc", "chars": len(txt)}
            urls, pdf, src = [], None, None
        else:
            urls = pdf_candidates(work)
            pdf, src = fetch_pdf(urls)
        if pdf:
            write_once(d / "fulltext.pdf", pdf, binary=True)
            try:
                txt = pdf_text(d / "fulltext.pdf")
                write_once(d / "fulltext.txt", txt)
                status["fulltext"] = {"source": src, "chars": len(txt)}
            except Exception as e:             # noqa: BLE001
                status["fulltext"] = {"source": src, "error": str(e)[:200]}
        else:
            status["fulltext"] = {"source": None, "tried": len(urls)}

    status["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    status["seconds"] = round(time.time() - t0, 1)
    status_p.write_text(json.dumps(status, indent=1))
    ft = status.get("fulltext") or {}
    s2n = json.load(s2_p.open()).get("references") if s2_p.exists() else None
    log(f"  {w}  refs={work.get('referenced_works_count')}  citers={status.get('n_citers_fetched')}"
        f"  s2_refs={len(s2n) if s2n is not None else '-'}  text={'yes' if ft.get('chars') else 'no'}"
        f"  {status['seconds']}s")
    return status


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.fetch")
    ap.add_argument("sample", help="sample JSON from genesis.sample")
    ap.add_argument("--max-citers", type=int, default=3000)
    ap.add_argument("--no-text", action="store_true")
    ap.add_argument("--only", nargs="*", help="restrict to these W-ids")
    ap.add_argument("--retry-text", action="store_true", help="retry full text even if a previous attempt failed")
    ap.add_argument("--no-citers", action="store_true", help="skip the citer pull (OpenAlex throttles `cites:` hard); fill later with --citers-only")
    ap.add_argument("--citers-only", action="store_true", help="fetch only missing citers, slowly")
    ap.add_argument("--citer-delay", type=float, default=3.0, help="seconds between citer pulls")
    ap.add_argument("--retry-s2", action="store_true", help="re-pull Semantic Scholar when the stored reference list is empty (rate-limited first time)")
    a = ap.parse_args(argv)
    rec = json.load(open(a.sample))
    ids = []
    for p in rec["pairs"]:
        ids += [p["case"]["id"], p["twin"]["id"]]
    if a.only:
        ids = [i for i in ids if i in set(a.only)]
    print(f"{len(ids)} works -> {RAW}", file=sys.stderr)
    if a.citers_only:
        for i, w in enumerate(ids, 1):
            d = RAW / w
            if (d / "citers.json").exists() or not (d / "work.json").exists():
                continue
            work = json.load((d / "work.json").open())
            try:
                citers = fetch_citers(w, a.max_citers, until_year=work["publication_year"] + CITER_WINDOW)
            except Exception as e:             # noqa: BLE001
                print(f"[{i}/{len(ids)}]  {w}  citers FAILED: {str(e)[:60]}", file=sys.stderr)
                time.sleep(a.citer_delay * 5)
                continue
            write_once(d / "citers.json", citers)
            st_p = d / "status.json"
            st = json.load(st_p.open()) if st_p.exists() else {"id": w}
            st.update({"n_citers_fetched": len(citers), "citers_capped": len(citers) >= a.max_citers,
                       "citer_window_years": CITER_WINDOW})
            st.pop("citers_error", None)
            st_p.write_text(json.dumps(st, indent=1))
            print(f"[{i}/{len(ids)}]  {w}  citers={len(citers)}", file=sys.stderr)
            time.sleep(a.citer_delay)
        return
    for i, w in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}]", file=sys.stderr, end="")
        bundle(w, a.max_citers, not a.no_text, log=lambda s: print(s, file=sys.stderr),
               retry_text=a.retry_text, retry_s2=a.retry_s2, want_citers=not a.no_citers)


if __name__ == "__main__":
    main()
