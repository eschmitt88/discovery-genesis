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
