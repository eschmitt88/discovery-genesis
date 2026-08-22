---
kind: moc
name: "measuring novelty and impact"
status: active
added: "2026-08-22"
concepts: ["[[concepts/novelty-vs-impact]]", "[[concepts/atypical-combination]]", "[[concepts/disruption-index]]", "[[concepts/field-normalized-impact]]", "[[concepts/matched-control-twin]]", "[[concepts/recombinant-uncertainty]]"]
tags: ["moc", "measurement", "h1", "h3", "h5"]
---

# Measuring novelty and impact

**Question this map answers:** how do we tell, from the bibliographic
record alone and before reading a word, whether a paper *did something
unusual* with its prior art and whether the field *used* what it did —
and why those two questions need separate instruments.

The project samples on impact and measures novelty, so every comparative
claim (H1, H3, H5) rests on the measures here and on the twin design
that makes them comparable. The concepts fall into three layers.

## 1. The distinction that organises everything

- [[concepts/novelty-vs-impact]] — two axes, weakly correlated. Novelty is
  atypicality relative to the field that year; impact is uptake. Anchored by
  [[literature/papers/uzzi2013atypical]] (conventional core + atypical tail
  is the high-impact signature) and
  [[literature/papers/wang2017bias]] (novel work is under-cited early,
  over-represented in the top percentile late — part of the "weak
  correlation" is a citation-window artefact).
- [[concepts/recombinant-uncertainty]] — the mechanism behind the weak
  correlation: unfamiliar recombination widens the *variance* of outcomes,
  not the mean ([[literature/papers/fleming2001recombinant]]). Predicts
  that same-move, non-impactful twins are common — which is what H5 needs
  to find.

## 2. Measuring novelty from the inputs and from the outputs

- [[concepts/atypical-combination]] — novelty of the *reference list*:
  how unusual the paper's pairings of cited topics are against a
  field-year null. Computable before reading; needs a background sample
  of reference lists per field-year (not yet built — stage
  `features --atypicality`).
- [[concepts/disruption-index]] — novelty seen in the *citers*: do later
  papers cite this one instead of, or together with, its references
  (CD; [[literature/papers/funk2017dynamic]]). Contested on two
  independent grounds — a zero-reference/plotting artefact
  ([[literature/papers/holst2024dataset]] vs
  [[literature/papers/park2023papers]]) and reference-list inflation
  ([[literature/papers/petersen2023disruption]]). The pipeline computes
  `cd_nok` and `cd5_nok` as card features only; never a selection axis
  until the pilot shows stability.

## 3. Measuring impact and making pairs comparable

- [[concepts/field-normalized-impact]] — why raw citation counts would
  make the sample mostly biomedicine and CS, and what normalising by
  topic × year does. OpenAlex's own percentile/FWCI
  ([[literature/posts/openalex-fwci]]) uses a 4-year window and is noisy
  in small topic-years; the sampler therefore ranks works by citations
  *within the topic-year pool itself* and requires a pool ≥ 500.
- [[concepts/matched-control-twin]] — the design that turns a measure
  into a comparison: same topic, year and type, rank in the 0.40–0.60
  band. Without the twin, reading impactful papers teaches what all
  papers do.

## Open thread

The impact sample's *novelty* distribution is itself a finding. If
consolidating papers (high impact, negative CD, low atypicality) dominate
the p99 pool, sampling becomes 2-D (impact × disruption) and the skill
splits into "make an unusual move" and "choose the problem the field is
about to need". The 15-pair pilot (`experiments/2026-08-22-h1-pilot-bibliometrics/`)
is the first look.
