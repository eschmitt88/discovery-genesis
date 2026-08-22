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
