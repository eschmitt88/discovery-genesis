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
