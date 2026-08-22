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

### Next (superseded — see the 2026-08-22 evening entry)

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

## 2026-08-22 (evening)

### Did

- Set `agency: max`; headroom verdict GO/high all session.
- Curated all three triage files via parallel Sonnet subagents: **26 papers
  ingested** with trust-signal frontmatter, 13 declined with reasons, all
  archived to `raw/_candidates/_done/`. Graph is now 26 literature notes,
  18 concepts, 2 MoCs (`measuring-novelty-and-impact`,
  `how-contributions-arise`).
- Built the pipeline end to end: `genesis.sample` (rank-based draws with a
  primary-research filter) → `genesis.fetch` (refs, citers, S2 intents,
  abstracts, OA text) → `genesis.features` → `genesis.dossier` (blinded coder
  packets) → `genesis.agree` (κ, confusion, unblinded role contrast).
- Ran the H1 experiment twice: pilot A (all article types) and pilot B
  (primary research only, 15 dev pairs + 5 held out).
- Open-coded 14 papers with two independent blind Sonnet coders; measured
  agreement; wrote **codebook v1** from their friction reports.

### Findings

- **The top 1 % by citations is mostly reviews and guidelines.** ≥ 9/15 in
  pilot A. This produced a spurious "impactful papers have 4× more
  references" effect that vanished under the filter (+92 → +8).
- **H1 partly confirmed, breadth reversed.** Recency (q = 0.025) and
  reference hotness (q = 0.025) are large and robust; cross-domain,
  cross-subfield and cross-topic shares are all *lower* for impactful
  papers. Impact here looks like working at the live edge of a hot local
  literature, not like crossing fields.
- **H0: idea-first is the minority genesis** (κ = 0.714). Means-first,
  problem-first and accretion together dominate. Both coders reached this
  independently.
- **H4: 90 % of ingredients are cited prior art** (1/117 new-here) — and
  identical for cases and twins, so it is not a discriminator.
- **`transfer` appeared only on twins** (8 vs 0). If it survives n = 150 it
  challenges `llm-cross-pollination`'s premise directly.
- 14 % of randomly drawn 2010s papers were recognised by both coders — the
  memorisation floor H6 must design around.
- Infrastructure: OpenAlex omits abstracts for ~28 % of works (now backfilled
  S2 → EPMC → Crossref, TLDR labelled); OpenAlex throttles *list* queries
  (`?filter=…`) independently of entity GETs and can 429 every list query for
  hours — reference fetching now falls back to per-entity GETs, and citers are
  decoupled entirely.

### Next

- Build the **Uzzi atypicality null model** (field-year reference-pair
  background). It is the highest-value missing feature: the conventional-core
  hypothesis predicts a thin atypical *tail*, which a mean share cannot see,
  and it is the direct test of whether the reversed breadth result is the
  whole story.
- Add a **subfield-velocity control** — median reference age of the whole
  topic-year pool — to test whether reference recency is a field-tempo
  artefact.
- Code the remaining pilot-B pairs with **codebook v1** and re-measure κ
  (target: `enabler` κ from 0.16 to > 0.6 on the closed vocabulary).
- Drip the missing citers (`--citers-only --citer-delay`) once the OpenAlex
  cooldown lifts; recompute CD5 at n = 15.
- Then scale: 150–300 pairs, closed coding, H3/H5.
