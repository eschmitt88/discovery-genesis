"""H6 stage 0: can the judge tell a real contribution from a plausible decoy?

    uv run python -m genesis.retro calibrate --cards cases/main50 \
        --sample data/samples/main50.json --n 24 --out experiments/<slug>/results/

Before asking "does the skill's proposal land near the real contribution?" we
have to know the ruler works. This stage hides a paper, shows a judge its prior
art (problem framing + reference list), and offers a shuffled slate: the paper's
real contribution plus decoys — contributions of *other* papers, half drawn from
the same OpenAlex topic (hard) and half from elsewhere (easy). The judge scores
each on the same 0-4 closeness ladder H6 would use.

If the real contribution does not come out on top well above chance, the ladder
cannot measure what H6 needs and the evaluation has to be redesigned (rank-based
scoring, or a different judge) before any skill is written. That is the point of
running this first: it is a cheap way to find out the instrument is broken.

Two failure modes this is designed to expose, both documented in the literature
notes: the judge scoring fluency rather than fit ([[novelty-mirage]]), and the
judge simply recognising the famous paper ([[hindsight-narrative-bias]]) — so
every trial records whether the judge names the source, and `--decoys-only`
runs a control slate with the real contribution removed, where a confident
"the real one is #3" is proof of guessing.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEUTRAL_CWD = Path("~/projects/.claude-p-cwd").expanduser()
MODEL = "claude-sonnet-5"          # pinned: an unattended job must not inherit the session default

LADDER = """0 — unrelated to this prior art.
1 — plausible in this area but not what this prior art most sets up.
2 — the right area and the right kind of move, wrong specifics.
3 — close: the same move on the same problem, differing in detail.
4 — this is what the prior art was setting up; it names the same contribution."""


def read_card(p: Path) -> dict:
    t = p.read_text()
    m = re.search(r"^---\n(.*?)\n---", t, re.S)
    fm = m.group(1) if m else ""
    g = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip().strip('"').strip("'")
    return {"id": p.stem, "contribution": g("contribution"), "problem": g("problem"),
            "is_primary": g("is_primary").split()[0].lower() if g("is_primary") else "",
            "genesis_model": g("genesis_model")}


def prior_art_brief(w: str, dossier_dir: Path, max_refs: int = 45) -> str | None:
    """The paper's own title and abstract are removed; what remains is the state of
    the art it was standing on."""
    p = dossier_dir / f"{w}.md"
    if not p.exists():
        return None
    t = p.read_text()
    head = re.search(r"^- year: (\d{4})", t, re.M)
    topic = re.search(r"^- primary topic: (.*)$", t, re.M)
    refs = re.search(r"^## References.*?$(.*?)(?=^## |\Z)", t, re.S | re.M)
    lines = [l for l in (refs.group(1).splitlines() if refs else []) if l.startswith("- [")]
    if not lines:
        return None
    return (f"Field: {topic.group(1) if topic else '?'}\n"
            f"Year the work was published: {head.group(1) if head else '?'}\n\n"
            f"Reference list of the (hidden) paper — this is the prior art it built on:\n"
            + "\n".join(lines[:max_refs])
            + (f"\n… and {len(lines) - max_refs} further references." if len(lines) > max_refs else ""))


def build_slate(target: dict, pool: list[dict], same_topic: list[str], rng: random.Random,
                n_decoys: int = 5, include_real: bool = True) -> tuple[list[dict], int | None]:
    near = [c for c in pool if c["id"] in same_topic and c["id"] != target["id"] and c["contribution"]]
    far = [c for c in pool if c["id"] not in same_topic and c["id"] != target["id"] and c["contribution"]]
    k_near = min(len(near), n_decoys // 2)
    picks = rng.sample(near, k_near) + rng.sample(far, min(len(far), n_decoys - k_near))
    slate = [{"text": c["contribution"], "src": c["id"], "real": False} for c in picks]
    if include_real:
        slate.append({"text": target["contribution"], "src": target["id"], "real": True})
    rng.shuffle(slate)
    real_ix = next((i for i, s in enumerate(slate) if s["real"]), None)
    return slate, real_ix


GEN_PROMPT_ERA = """Below is the prior art a research paper built on: its field, its year,
and its full reference list. The paper itself is hidden.

{brief}

IMPORTANT — answer as if you were a researcher working in this field in that year
and no later. You must not use any knowledge of what this field went on to do
afterwards. Do not propose a contribution because you know it later succeeded, and
do not name methods, datasets, models or results that did not exist by then. If a
proposal only makes sense with hindsight, replace it.

Propose {k} DIFFERENT contributions that a strong paper could plausibly have made
from exactly this prior art, in this field, in this year, using only what was
available then. Each should be specific enough to be a paper's one-sentence
contribution statement — name the method, the system and the claim, not a research
direction. Make them genuinely different from one another and each as plausible as
you can.

Reply with ONLY a JSON array of {k} strings, no prose."""


GEN_PROMPT = """Below is the prior art a research paper built on: its field, its year,
and its full reference list. The paper itself is hidden.

{brief}

Propose {k} DIFFERENT contributions that a strong paper could plausibly have made
from exactly this prior art, in this field, in this year. Each should be specific
enough to be a paper's one-sentence contribution statement — name the method, the
system and the claim, not a research direction. Make them genuinely different from
one another, and make each one as plausible as you can.

Reply with ONLY a JSON array of {k} strings, no prose."""


GRADED_PROMPT = """A research paper made this contribution:

REFERENCE CONTRIBUTION: {truth}

Below are {n} proposals that were written *without* seeing it, from the paper's
prior art alone. Score how close each proposal comes to the reference
contribution above — not how good or plausible it is on its own.

0 — a different contribution altogether.
1 — same broad area, different problem and different move.
2 — same problem OR same kind of move, not both.
3 — same problem and same kind of move, differing in specifics.
4 — the same contribution, in different words.

Proposals:
{candidates}

Reply with ONLY a JSON object, no prose:
{{"scores": [<one integer 0-4 per proposal, in the order shown>],
  "why": "<one sentence>"}}"""


PROMPT = """You are judging how well each candidate contribution fits a body of prior art.

{brief}

Below are {n} candidate contributions. Exactly one of them may or may not be the
contribution the hidden paper actually made — do not assume one of them is.
Score EVERY candidate independently on this ladder:

{ladder}

Then say which single candidate you think is most likely the hidden paper's own
contribution, and how confident you are.

Candidates:
{candidates}

Reply with ONLY a JSON object, no prose:
{{"scores": [<one integer 0-4 per candidate, in the order shown>],
  "best": <1-based index of your pick>,
  "confidence": "<low|medium|high>",
  "recognised_paper": "<the paper's title if you actually recognise it from the references, else 'no'>",
  "why": "<one sentence>"}}"""


def judge(brief: str, slate: list[dict], model: str, timeout: int = 300) -> dict | None:
    cands = "\n".join(f"{i+1}. {s['text']}" for i, s in enumerate(slate))
    prompt = PROMPT.format(brief=brief, n=len(slate), ladder=LADDER, candidates=cands)
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", model],
                           capture_output=True, text=True, timeout=timeout, cwd=NEUTRAL_CWD)
    except subprocess.TimeoutExpired:
        return None
    out = r.stdout.strip()
    m = re.search(r"\{.*\}", out, re.S)
    if not m:
        return {"error": (out or r.stderr)[:300]}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"error": m.group(0)[:300]}


def generate_decoys(brief: str, k: int, model: str, timeout: int = 300,
                    era_restricted: bool = False) -> list[str]:
    """Plausible on-topic contributions for the *same* prior art. These are the
    decoys H6 actually has to survive: the easy calibration used other papers'
    contributions, which a judge can separate on topic vocabulary alone."""
    try:
        tmpl = GEN_PROMPT_ERA if era_restricted else GEN_PROMPT
        r = subprocess.run(["claude", "-p", tmpl.format(brief=brief, k=k), "--model", model],
                           capture_output=True, text=True, timeout=timeout, cwd=NEUTRAL_CWD)
    except subprocess.TimeoutExpired:
        return []
    m = re.search(r"\[.*\]", r.stdout, re.S)
    if not m:
        return []
    try:
        out = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    return [str(x) for x in out][:k]


def judge_graded(truth: str, proposals: list[str], model: str, timeout: int = 300) -> dict | None:
    """Supervised scoring: the judge is *shown* the real contribution and grades each
    proposal's distance from it. The unsupervised variant — 'which of these fits the
    prior art best?' — was shown not to work (`hard` stage): proposals generated from
    a reference list are by construction more derivable from it than the real paper
    is, so the judge prefers them. Grading against a revealed ground truth removes
    that asymmetry."""
    cands = "\n".join(f"{i+1}. {p}" for i, p in enumerate(proposals))
    prompt = GRADED_PROMPT.format(truth=truth, n=len(proposals), candidates=cands)
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", model],
                           capture_output=True, text=True, timeout=timeout, cwd=NEUTRAL_CWD)
    except subprocess.TimeoutExpired:
        return None
    m = re.search(r"\{.*\}", r.stdout, re.S)
    if not m:
        return {"error": (r.stdout or r.stderr)[:300]}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"error": m.group(0)[:300]}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genesis.retro")
    ap.add_argument("stage", choices=["calibrate", "hard", "graded"])
    ap.add_argument("--cards", required=True)
    ap.add_argument("--sample", required=True)
    ap.add_argument("--dossiers", default="data/dossiers/main50-compact")
    ap.add_argument("--primary", default=None, help="primary-verdict json; restrict to primary works")
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--decoys", type=int, default=5)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--era-restricted", action="store_true",
                    help="hard stage: forbid the generator from using post-publication hindsight — "
                         "the control that separates 'the judge over-rates generated text' from "
                         "'the prior art genuinely underdetermines the contribution'")
    ap.add_argument("--control", action="store_true",
                    help="run the no-real-contribution control slate as well")
    ap.add_argument("--hard-name", default="hard-raw.json", help="output filename for the hard stage")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    cards_dir = Path(a.cards)
    coders = sorted(d.name for d in cards_dir.iterdir() if d.is_dir() and d.name.startswith("coder"))
    cards = {}
    for c in coders:                            # first coder that produced a contribution wins
        for p in (cards_dir / c).glob("W*.md"):
            rec = read_card(p)
            if rec["contribution"] and rec["id"] not in cards:
                cards[rec["id"]] = rec
    sample = json.load(open(a.sample))
    topic_of = {p[r]["id"]: p["topic_id"] for p in sample["pairs"] for r in ("case", "twin")}
    ok = set(topic_of)
    if a.primary:
        pv = json.load(open(a.primary))
        verd = pv.get("works", pv)
        ok = {w for w in ok if str(verd.get(w, {}).get("verdict", "primary")) == "primary"}
    pool = [c for c in cards.values() if c["id"] in ok]
    rng = random.Random(a.seed)
    targets = rng.sample(pool, min(a.n, len(pool)))
    out_dir = Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, t in enumerate(targets, 1):
        brief = prior_art_brief(t["id"], Path(a.dossiers))
        if not brief:
            print(f"[{i}/{len(targets)}] {t['id']} no brief — skipped", file=sys.stderr); continue
        if a.stage == "graded":
            # Anchors with known answers, so the ruler itself is under test:
            #   positive  — the paper's own contribution, restated by the judge's own
            #               standard (should score 4)
            #   generated — proposals from the prior art alone (the quantity of interest)
            #   negative  — another paper's real contribution (should score 0-1)
            gen = generate_decoys(brief, 3, a.model, era_restricted=True)
            if len(gen) < 2:
                print(f"[{i}/{len(targets)}] {t['id']} generator failed — skipped", file=sys.stderr)
                continue
            others = [c for c in pool if c["id"] != t["id"] and c["contribution"]]
            neg = rng.choice(others)["contribution"]
            props = [{"kind": "positive", "text": t["contribution"]}] + \
                    [{"kind": "generated", "text": g} for g in gen] + \
                    [{"kind": "negative", "text": neg}]
            rng.shuffle(props)
            res = judge_graded(t["contribution"], [p["text"] for p in props], a.model)
            sc = (res or {}).get("scores") or []
            row = {"id": t["id"], "arm": "graded", "kinds": [p["kind"] for p in props],
                   "result": res}
            if len(sc) == len(props):
                by = {}
                for p, s2 in zip(props, sc):
                    by.setdefault(p["kind"], []).append(s2)
                row["by_kind"] = by
            rows.append(row)
            print(f"[{i}/{len(targets)}] {t['id']} graded: {row.get('by_kind')}", file=sys.stderr)
            (out_dir / "graded-raw.json").write_text(json.dumps(rows, indent=1))
            continue
        if a.stage == "hard":
            gen = generate_decoys(brief, a.decoys, a.model, era_restricted=a.era_restricted)
            if len(gen) < 2:
                print(f"[{i}/{len(targets)}] {t['id']} generator failed — skipped", file=sys.stderr)
                continue
            slate = [{"text": g, "src": "generated", "real": False} for g in gen]
            slate.append({"text": t["contribution"], "src": t["id"], "real": True})
            rng.shuffle(slate)
            real_ix = next(j for j, s2 in enumerate(slate) if s2["real"])
            res = judge(brief, slate, a.model)
            row = {"id": t["id"], "arm": "hard", "n_candidates": len(slate),
                   "real_index": real_ix + 1, "slate": [s2["text"][:200] for s2 in slate],
                   "result": res}
            sc = (res or {}).get("scores") or []
            if len(sc) == len(slate):
                row["real_score"] = sc[real_ix]
                row["decoy_max"] = max(s2 for j, s2 in enumerate(sc) if j != real_ix)
                row["decoy_mean"] = round(sum(s2 for j, s2 in enumerate(sc) if j != real_ix) / (len(sc) - 1), 2)
                row["real_is_top"] = sc[real_ix] > row["decoy_max"]
                row["real_tied_top"] = sc[real_ix] == row["decoy_max"]
                row["picked_real"] = res.get("best") == real_ix + 1
            rows.append(row)
            print(f"[{i}/{len(targets)}] {t['id']} hard: real={row.get('real_score')} "
                  f"decoy_max={row.get('decoy_max')} picked_real={row.get('picked_real')} "
                  f"conf={(res or {}).get('confidence')}", file=sys.stderr)
            (out_dir / a.hard_name).write_text(json.dumps(rows, indent=1))
            continue
        same = [w for w, tp in topic_of.items() if tp == topic_of[t["id"]]]
        for arm in (["real"] + (["control"] if a.control else [])):
            slate, real_ix = build_slate(t, pool, same, rng, a.decoys, include_real=(arm == "real"))
            res = judge(brief, slate, a.model)
            row = {"id": t["id"], "arm": arm, "n_candidates": len(slate),
                   "real_index": None if real_ix is None else real_ix + 1,
                   "slate_sources": [s["src"] for s in slate], "result": res}
            if res and "scores" in res and real_ix is not None:
                sc = res["scores"]
                if len(sc) == len(slate):
                    row["real_score"] = sc[real_ix]
                    row["decoy_max"] = max(s for j, s in enumerate(sc) if j != real_ix)
                    row["decoy_mean"] = round(sum(s for j, s in enumerate(sc) if j != real_ix)
                                              / (len(sc) - 1), 2)
                    row["real_is_top"] = sc[real_ix] > row["decoy_max"]
                    row["real_tied_top"] = sc[real_ix] == row["decoy_max"]
                    row["picked_real"] = res.get("best") == real_ix + 1
            rows.append(row)
            print(f"[{i}/{len(targets)}] {t['id']} {arm}: real={row.get('real_score')} "
                  f"decoy_max={row.get('decoy_max')} picked_real={row.get('picked_real')} "
                  f"conf={(res or {}).get('confidence')}", file=sys.stderr)
            (out_dir / "calibration-raw.json").write_text(json.dumps(rows, indent=1))
    name = {"hard": a.hard_name, "graded": "graded-raw.json"}.get(a.stage, "calibration-raw.json")
    (out_dir / name).write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} trials -> {out_dir/name}", file=sys.stderr)


if __name__ == "__main__":
    main()
