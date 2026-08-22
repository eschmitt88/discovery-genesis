# NOTES

Running log of work sessions. `/wrap` appends a new dated section at the
end of each session with **Did / Findings / Next** subsections. The
SessionEnd hook backstops this if you forget.

<!-- entries go below this line, newest at bottom -->

## 2026-08-22

### Did

- Scaffolded the project (`/new-project discovery-genesis --experiments`,
  public, Pages enabled).
- Wrote `docs/research-plan.md` (question, four genesis models, H0–H6,
  genesis-card schema v0, sampling design with matched twins, data
  sources, bibliometric feature block, coding protocol, retrodiction
  evaluation, phases) and ADR 0001 (scope; the idea step is a hypothesis,
  not the frame; novelty and impact as separate axes; twins from day one).
- Seeded 12 concepts: genesis-models, genesis-card, move-taxonomy,
  matched-control-twin, novelty-vs-impact, adjacent-possible,
  atypical-combination, disruption-index, field-normalized-impact,
  retrodiction-test, hindsight-narrative-bias, triz-lineage.
- Built `genesis/sample.py` (xpol topic draw → OpenAlex impactful case +
  matched twin, all seeds logged) and smoke-tested it: 5 pairs in
  `data/samples/smoke.json` (seed 20260822).
- Ran three `/discover` triages via Sonnet subagents into
  `raw/_candidates/`: science-of-science metrics; theories of discovery;
  LLM idea generation + evaluation.

### Findings

- No need to wait on `llm-cross-pollination`: its `xpol` sampler is built,
  tested and H1 there is done. We invoke it via `uv run --project`.
- OpenAlex has everything stage 1 needs: `citation_normalized_percentile`
  (field/year-normalised), server-side `sample=&seed=`, reference lists,
  OA URLs, topic ids matching the xpol frame. Impactful pools per
  topic-year are small (6–100 articles at ≥ p99) — fine for uniform draws.
- Smoke draw: 1 of 5 impactful cases is OA. Full text will be missing
  for perhaps half the cases; abstract + references + Semantic Scholar
  citation contexts must carry the coding for those, and the card's
  `evidence` field has to record it.
- One `type:article` case is a review ("Status of Reactive Non-Heme
  Metal–Oxygen Intermediates…") — the accretion/consolidation category
  shows up immediately, as the plan anticipated. Keep, code, report
  with/without.
- Triage (LLM ideation): MOOSE-Chem (2410.07076) already implements a
  hide-the-paper retrodiction with a knowledge-cutoff memorisation control;
  IdeaBench (2411.02429) scores paper + references → real contribution.
  Reuse for H6 rather than rebuild. "Limits of LLM-as-judge for novelty"
  (2606.12071) and the ideation–execution gap (2506.20803) are warnings
  for the H6 judge design.

### Next

- Curate the three triage files: `/fetch-paper` + `/ingest` the top ~10
  and attach them as `sources:` on the 12 seedlings (all sourceless now).
- Pipeline stages 2–3: `genesis/fetch.py` (references, citers, OA text,
  S2 citation intents → `raw/cases/<W-id>/`, DVC) and
  `genesis/features.py` (ref age, cross-topic share, Uzzi atypicality,
  CD₅). Decide the atypicality null-model background sample size.
- Draw the 20-pair pilot with a fresh OS-entropy seed; carve the held-out
  split at draw time; first `/new-experiment`: H1 on the pilot.
- Open-code 4–6 pilot pairs by hand (user + main agent) before any LLM
  coder runs, to draft the coder prompt from real cases.
