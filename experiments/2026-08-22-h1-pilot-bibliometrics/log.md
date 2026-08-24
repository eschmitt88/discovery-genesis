# Log — h1-pilot-bibliometrics

- 2026-08-22 drew 20 pairs (seed 1124470055840796258), 5 held out; fetch started.
- 2026-08-22 19:10 pilot A (15 dev pairs, `type:article`, no review filter) fetched
  and featurised. Paired result in `results/paired-pilotA-alltypes.md`:
  the dominant difference is **reference count** (case median 117 vs twin
  26; 14/15 pairs; Wilcoxon p < 0.001; Cliff δ +0.75). `ref_n_fields` +2
  (p = 0.015) rides on it; cross-field *shares* are identical; recency,
  hotness and team size point the predicted way but do not clear p < 0.05.
- Cause: **≥ 8 of the 15 top-1 % cases are reviews, perspectives or
  guidelines** (trifluoromethylation review, azo-dye review, liver-fibrosis
  pathogenesis, polymer-brush perspective, ASCRS guidelines, NTM
  drug-discovery review, CBD safety review, pharmaceuticals-in-water review).
  The plan's accretion contingency fired immediately: "top 1 % by citations"
  measures consolidation first. Decision: add a primary-research filter to
  `genesis.sample` (title/abstract/venue regex + OpenAlex type; every
  excluded work logged with its reason and the per-pool review share is
  recorded as a finding), redraw as **pilot B**, and keep pilot A as the
  measurement of what the raw top 1 % contains.
- Full text: 1/30 works. PDF hosts (Hindawi, Cell, Elsevier) refuse the
  client; OpenAlex lacks PMCIDs for most biomed OA papers. Fix: resolve PMCID
  via Europe PMC search by DOI and pull `fullTextXML`; retrying.
- 2026-08-22 19:40 pilot B (primary-research filter) drawn, seed 2419655738578421181.
  Review share of the top-1 % band, by the conservative classifier, is logged per
  draw: median ~33 % (range 0/6 to 7/26) — a *lower bound*, since hand-checking
  pilot A put it near 60 %.
- First pilot-B result on the 7 pairs fetched before an OpenAlex 429 killed the
  run (`results/paired-pilotB-partial.md`): the picture inverts relative to
  pilot A. `n_refs` is no longer the story (+14, p = 0.58 — the pilot-A effect
  was entirely the review artefact). What appears instead is **reference
  recency** — `ref_share_le3` +0.15 (6/7 pairs, p = 0.031, Cliff δ +0.73) and
  `ref_age_median` −4 years (δ −0.80) — plus **hotter references**
  (`ref_hot_median` +94, δ +0.55; `ref_fwci_median` +3.45). Cross-field
  *shares* run slightly LOWER in cases at every level (topic/subfield/field/
  domain), which is the direction Uzzi's "conventional core" predicts.
  `cd5_nok` is more negative for cases (−0.68 vs 0.00), i.e. the impactful
  primary papers here are still consolidating rather than disrupting.
- Caveat: n = 7, and the pairs are the first-drawn ones, not a random subset —
  treat as a smoke reading, not the H1 result. Rerunning at n = 15.
- Infrastructure: three concurrent fetch processes tripped OpenAlex 429s and
  starved Semantic Scholar (references empty in 26/40 bundles, which is where
  the citation *intents* live). Fixes: polite-pool `mailto` on every OpenAlex
  call with 429-aware backoff; S2 paced at 3.5 s with 6 retries and a
  `--retry-s2` pass that re-pulls bundles whose stored reference list is empty;
  full text now resolves PMCID via Europe PMC search (OpenAlex often lacks it)
  and falls back to a browser-UA PDF fetch. Publisher PDF hosts (Hindawi, Cell,
  Elsevier) return 403 regardless, so Europe PMC is the main text route.
- 2026-08-22 20:20 coder A finished 14 pilot-B cards (blind). Reported defect:
  6/14 dossiers had **no abstract at all** — OpenAlex omits abstracts for ~28 %
  of works (18/65 bundles here), which is a publisher-policy gap, not a bug in
  the fetch. Fix: `genesis.fetch` now resolves a missing abstract through
  Semantic Scholar → Europe PMC → Crossref, and only as a last resort stores
  Semantic Scholar's machine-written TLDR, flagged `generated: true`; the
  dossier labels it explicitly so a coder never sees a model summary presented
  as the authors' words. `evidence` gains `title+refs-only` and `tldr-only`
  tiers.
- Coder A's first read (14 papers, blind, v0 codebook): idea-first 2, means-first
  4, problem-first 3, accretion 5. Unused v0 move labels: scale, simplification,
  inversion, and `resource` (used only as an *enabler*, never as a move) —
  candidate cuts for v1. No label had to be invented.
- Schema friction reported: `problem_age` is single-valued but papers often have
  an old broad problem and a recent narrow one; `role` has no slot for a
  formalism/substrate (RDF); problem-first's "≤3 y ingredient" rule fits
  resource-repurposing (secondary analysis of a 5-year-old trial) badly.
- 2026-08-22 20:35 coder B finished; agreement computed
  (`results/agreement-pilotB.md`). **Cohen κ = 0.714 on `genesis_model`**
  (raw 0.79), above the protocol's 0.6 gate on the first attempt with the v0
  codebook. `move_candidates` Jaccard 0.70, and every paper shared at least one
  move label between coders. Weak fields: `enabler_head` κ = 0.16 (free text —
  needs a closed vocabulary in v1) and `problem_age` κ = 0.44 (the
  old-broad-problem / recent-narrow-problem conflation coder A flagged).
  Confusion is concentrated in accretion↔problem-first (3 of 3 disagreements).
- Both coders independently recognised the same 2 of 14 papers
  (`W2078338131` band-convergence, `W2149161770` zebrafish gata4+) — a 14 %
  recall rate on randomly drawn 2010s STEM papers, which is the memorisation
  base rate the H6 retrodiction protocol has to handle.
- **First unblinded contrast (H0/H3 smoke reading; 7 pairs × 2 coders = 14
  codings per role):**
  - genesis model, case vs twin: means-first **6 vs 2**, accretion 3 vs 5,
    problem-first 3 vs 4, idea-first 2 vs 3.
  - moves, case vs twin: `transfer` **0 vs 8**, `unification` 4 vs 0,
    `recombination` 6 vs 3, `anomaly` 1 vs 0, `gap-filling` 7 vs 5.
  Read with care at this n, but two directions are worth stating: impactful
  primary papers in this batch lean **means-first** (a new tool/screen/
  instrument produced the finding), and **`transfer` appears only on the
  twins** — every coded instance of "imported a method or frame from another
  field" landed on the median-impact member of its pair. If that survives
  n = 150, it is a direct challenge to the premise of `llm-cross-pollination`
  (that foreign-mechanism import is the high-value move) and to any skill built
  on transfer alone.
  Confounds to rule out first: `transfer` may be coded more readily when a
  paper is thin (less method detail → the import is the only visible move);
  and 3 of the 7 twins here are essay/report genres where framing imports are
  the whole contribution.
- 2026-08-22 21:05 OpenAlex 429 diagnosis. Single work lookups return 200 while
  **every** `filter=cites:` query returns 429 — at per-page 200, 100, 50 and 25,
  with and without `select`, and with a publication-year window. So it is not a
  global block or a query-shape problem: OpenAlex throttles the citation-lookup
  endpoint class far harder than work/reference lookups, and our earlier
  three-process burst put it in a cooldown. Fix: citers are decoupled from the
  bundle (`--no-citers` for the main pass, `--citers-only --citer-delay` for a
  slow drip afterwards); a citer failure now records `citers_error` in
  `status.json` instead of aborting the run, and `features.py` emits null CD
  rather than 0 when citers are absent. H1's primary signals (reference recency,
  hotness, cross-field share) do not depend on citers, so the analysis is not
  blocked by the cooldown.
- 2026-08-22 21:45 **H4 first look**, from the 28 blind cards (117 ingredients
  parsed, all 28 cards usable):
  - `cited` 105 · `uncited-existing` 11 · `new-here` **1**.
  - 90 % of the components a contribution depends on were already in its own
    reference list; **19 of 28 cards have *every* ingredient cited**.
  - Case vs twin: 52/60 cited vs 53/57 cited. Ingredient provenance is
    **identical across roles** — H4 looks broadly true and is *not* a
    discriminator between impactful and ordinary work.
  - Ingredient roles: theory 48, method 40, data 11, instrument 8, result 7.
  **Caveat that limits this**: coders were handed the reference list and asked
  to name ingredients, which anchors hard toward citing what is visible. The v0
  prompt also lacked the `uncited-social` status (added in codebook v1 after
  Tahamtan & Bornmann), so a conversation- or practice-derived ingredient had no
  slot to be recorded in. Read this as "the reference list is *sufficient* to
  reconstruct a plausible ingredient set in 90 % of cases", not as "the ideas
  came from the references". Distinguishing those needs the `external_story`
  field and full text, which this batch mostly lacked.
- 2026-08-23 citers dripped for all 40 pilot-B works (3 s spacing, 0 failures;
  5-year window). **Disruption is a null at n = 15**: `cd5_nok` case −0.64 vs
  twin −0.33, 7 pairs one way and 8 the other, p = 0.30, δ −0.23. The 7-pair
  reading of 2026-08-22 ("cases more consolidating", p = 0.078) does not
  survive; it was the first-drawn pairs, not a random subset. Both members of
  a pair are mildly consolidating, which is what CD-nok looks like for most
  primary research. Novelty measured on the *outputs* (citers) therefore does
  not distinguish impact here; novelty on the *inputs* (reference structure)
  does — recency, hotness, and a *lower* cross-boundary share.
- Background pools (`genesis.background`, 150 primary works per topic-year)
  are being pulled for the velocity control and the atypicality null.
- 2026-08-23 **pilot-B coding complete: 30 papers × 2 blind coders** (14 under
  codebook v0, 16 under v1). `results/agreement-pilotB-v1.md`,
  `results/agreement-pilotB-all.md`.
  - Agreement, all 30: `genesis_model` κ = 0.63 (v0 batch 0.71, v1 batch
    0.52); `is_primary` 0.64; `enabler_head` 0.50 overall but **0.79 on the
    v1 batch** (the closed vocabulary fixed the worst field, 0.16 → 0.79);
    `problem_age_specific` 0.72, `problem_age_broad` 0.55 (0.08 on v1 alone —
    the "broad" question is not codable reliably and should go).
    `move_candidates` Jaccard 0.56; 97 % of papers share ≥ 1 label.
  - Why `genesis_model` κ fell under v1: the decision order
    (accretion → means-first → problem-first → idea-first, first match wins)
    made problem-first a catch-all for coder A (10/16) while coder B split the
    same papers means/problem (5/7). All v1 disagreements are problem-first ↔
    means-first. Both coders independently named the same unresolved case:
    *an established assay or platform applied to the next target* (next gene,
    next cancer type, next lattice geometry, next species) — means-first by
    the "capability → observation" signature, problem-first by the paper's
    own gap framing. That is ~5 of 16 papers and it is a real category, not a
    coding failure. v1.1 needs a named label for it, or a rule that routine
    reuse of a mature platform is problem-first and means-first is reserved
    for a capability that is *new to the authors or the field*.
  - **`transfer` is coded only on twins, at the full pilot.** Paper level:
    0/15 cases vs 7/15 twins by ≥ 1 coder (3/15 by both); Fisher one-sided
    p = 0.003; 7 discordant pairs, all twin-only, sign test p = 0.008. The
    v1 `transfer` definition (source in a *different primary field*) is
    stricter than v0's and the result survived the tightening. Both coders
    noted that animal→human translation and same-field method reuse do *not*
    count as transfer under v1; those went to gap-filling/recombination.
  - **Genesis model by role is not stable across batches.** v0 batch: cases
    means-first 6 vs 2; v1 batch: cases problem-first 12 vs 5 and twins
    means-first 7 vs 1. At paper level with both coders agreeing: cases
    problem-first 6, means-first 3, accretion 2, idea-first 1; twins
    means-first 3, accretion 3, problem-first 2, idea-first 2. The only thing
    stable is **idea-first is rare on both sides** (1/12 agreed cases, 2/10
    agreed twins) — H0 holds; the means/problem split is codebook-sensitive
    and cannot be read at this n.
  - Recognition: 3 of 30 papers recognised by ≥ 1 coder (10 %).
- 2026-08-23 **H5 first pass** (30 cards, primary move = first listed):
  5/15 pairs share the same primary move across case and twin; 9/15 share at
  least one move label. In those pairs the move cannot be what separates
  impact from non-impact — the residual is problem choice, timing, execution
  or community, exactly what H5 predicts. Caveat: `gap-filling` is the
  primary move on 12 of 30 papers, so label coarseness inflates sharing; a
  v1.1 codebook that splits gap-filling (see below) is needed before H5 is
  read quantitatively. The shared-move pairs (Smoking, Liver/TIPS,
  Interferon/CIN, Cervical, Insect) are the first candidates for the
  `twin` contrast paragraph on the card.
- Main sample (60 pairs, 10 held out) draw failed at 0 pairs on an OpenAlex
  list-query 429; a retry loop probes every 5 min and draws when list queries
  return 200. Rule from here: **one OpenAlex consumer at a time** — the
  background pull and the citer drip running together is what tripped the
  long cooldown twice today.
- 2026-08-23 **codebook v1.1 re-code, all 30 pilot-B papers, two fresh blind
  coders** (`results/agreement-pilotB-v11.md`; cards in `cases/pilotB/v11/`).
  - **κ = 0.73 on `genesis_model`** (v1 batch 0.52; v0 0.71), `is_primary`
    0.82, `problem_age_specific` 0.71, `enabler_head` 0.55, move Jaccard
    0.64. The gate (≥ 0.6) is cleared on the field that matters; **v1.1 is
    frozen as the codebook for the main sample.**
  - **The gap-filling split is the sharpest contrast in the pilot.** Paper
    level, ≥ 1 coder: `gap-filling:first-measurement` on 10/15 cases vs 4/15
    twins (both coders: 7 vs 2; Fisher p = 0.033); `gap-filling:next-target`
    on 2/15 cases vs 7/15 twins (both coders: 0 vs 5; Fisher p = 0.054).
    Sign tests on discordant pairs do not reach 0.05 at n = 15 (8–2,
    p = 0.11; 1–6, p = 0.125). Reading: the impactful primary paper
    *measures something for the first time in its system*; the median paper
    *applies an established method to the next target*.
  - **`transfer` attenuates under the strict v1.1 definition**: 1/15 cases
    vs 2/15 twins (was 0 vs 7 under v0/v1). The earlier contrast was partly
    animal→human and cross-context reuse being labelled transfer; v1.1 sends
    those to `next-target`, where the contrast reappears. So the stable
    finding is not "twins import from other fields" but "twins re-apply;
    cases first-measure". The bibliometric breadth reversal stands on its own.
  - `genesis_model` **does not discriminate roles**: problem-first 18 vs 16
    codings, means-first 4 vs 3, idea-first 4 vs 5, accretion 4 vs 6. H0
    holds (idea-first ≈ 13 % of codings either side); the v1.1 rule makes
    problem-first the modal model for primary research on both sides.
  - **Recognition is asymmetric: 7/15 cases vs 0/15 twins** recognised by
    ≥ 1 coder in this pass (earlier passes: 2/14, 1/16 — recognition varies
    by run). The memorisation floor for the retrodiction test is ~half of
    *impactful* 2010s papers, not 14 % of papers. Excluding recognised cases
    would bias H6 toward the less famous half; post-cutoff papers
    (MOOSE-Chem style) are the cleaner control.
  - **Blinding leak**: coder A noted the 30 dossiers resolve into 15 pairs
    by topic + year. A coder who recognises one member can infer the other
    is the twin. Mitigation for the main sample: each coder gets a shuffled
    batch that never contains both members of a pair.
- 2026-08-24 **main sample drawn and fetched**: 50 dev pairs + 10 held out
  (seed 1729883731402988666), 120/120 bundles, 88/100 abstracts. Domains:
  Life 19, Physical 18, Health 13. Median review share of the top-1 % band
  by the sampler's classifier: 25 %.
- **H1 at n = 50 is NOT reportable yet — the review filter has a recall
  problem.** `n_refs` returns as the largest effect (+24.5, 43/50 pairs,
  q < 0.001, δ +0.59), the pilot-A signature. But a post-hoc rerun of the
  sampler's own regex flags **0 of 100** works, while the top cases by
  reference count are plainly reviews: *Galectin-3: One Molecule for an
  Alphabet of Diseases* (489 refs), *Remediation of heavy metal(loid)s
  contaminated soils* (401), *The Growing Impact of Catalysis in the
  Pharmaceutical Industry* (294), *Teleost intestinal immunology* (211).
  13 cases have > 100 references; 0 twins do. The regex was built on pilot
  A, where reviews announced themselves in the title or the venue
  (*Chemical Reviews*, *Annual Review of…*). Its precision is fine and its
  recall is poor: a review that is simply titled after its subject evades
  every pattern.
- Fix: `genesis.pubtype` pulls three independent signals — Semantic
  Scholar `publicationTypes`, Europe PMC `pubTypeList`, Crossref
  `type`/`subtype`. Spot check: S2 and EPMC both return "Review" for the
  Galectin-3 and teleost papers that the regex missed. Reference count is
  deliberately *not* used as a filter — it is the feature under test.
- The arbiter of record stays the coders' blind `is_primary` field: two
  independent coders judge each paper from its dossier without knowing its
  impact. H1 at n = 50 will be recomputed on the subset both coders call
  primary, with the external signals as a cross-check.
- Also to repair before the n = 50 analysis: full text reached only 3/100
  works (pilot B got 20/40) — the fast sequential fetch appears to have
  been rate-limited on Europe PMC; and 46 of 50 background pools are
  missing, so the velocity control and atypicality null are unavailable at
  n = 50.
