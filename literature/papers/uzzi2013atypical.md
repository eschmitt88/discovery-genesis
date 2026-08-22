---
kind: paper
title: "Atypical Combinations and Scientific Impact"
authors: ["Brian Uzzi", "Satyam Mukherjee", "Michael Stringer", "Ben Jones"]
institutions: ["Northwestern University (Kellogg School of Management)", "Northwestern Institute on Complex Systems", "Datascience Analytics", "National Bureau of Economic Research"]
year: 2013
venue: "Science 342(6157):468-472"
peer_reviewed: true
url: "https://www.science.org/doi/10.1126/science.1240474"
code_url: null
citations: 1461
source: "raw/papers/uzzi2013atypical.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: []
related_concepts: ["atypical-combination", "novelty-vs-impact", "matched-control-twin"]
tags: ["novelty", "bibliometrics", "h1", "atypicality"]
---

# Atypical Combinations and Scientific Impact

## TL;DR

Across 17.9M WoS papers, the highest-impact science pairs an exceptionally
*conventional* core of journal-pair reference combinations with a small
*atypical* tail; papers with this "conventional core + atypical tail"
profile are roughly 2x as likely to be a top-cited "hit" as papers that are
uniformly conventional or uniformly novel.

## Claims

- Novelty (atypical journal-pair combinations in the reference list) and
  conventionality are not opposites on one axis; the two matter jointly.
- Teams are 37.7% more likely than solo authors to insert atypical
  combinations, but the *conventional-core-plus-atypical-tail* profile,
  not raw atypicality, is what predicts high citation impact.
- Atypical combinations are rare in absolute terms; most reference pairs
  in most papers are highly conventional.

## Methods

- For each paper, every pairwise combination of the journals in its
  reference list is scored against a randomized-network null (Monte
  Carlo switching of citation links preserving each paper's and each
  journal's citation counts) to get an observed-vs-expected z-score per
  pair, for that publication year.
- Each paper is summarized by two numbers: the median pair z-score
  (conventionality) and the 10th-percentile pair z-score (the atypical
  tail). This is exactly the operationalization behind this project's
  `[[atypical-combination]]` concept.

## Results

- Top-cited papers overwhelmingly combine high conventionality (median
  near or above the field norm) with a low (negative) 10th-percentile
  score — the atypical tail is present but small.
- Uniformly atypical papers (low conventionality *and* a deep atypical
  tail) are not the highest-impact group; the "hit" profile requires the
  conventional core.

## Critique / open questions

- The null model is defined over journal-pairs, a coarse proxy for
  intellectual distance; the project's pipeline substitutes OpenAlex
  topics for journals, which changes the granularity of what counts as
  "atypical" and needs its own background sample per field-year (already
  flagged in `[[atypical-combination]]`).
- Measures the reference list, not what the paper actually *did* with
  the atypical citation — a paper can cite atypically without building on
  it. The project's `ingredients` card field is the intended check.

## Trust signals

- **Credibility:** 5 — top-tier venue (Science), peer-reviewed, extremely
  well cited (1,461 citations per OpenAlex), reputable labs (Northwestern
  Kellogg / NICO, NBER), and the atypicality/conventionality
  operationalization has been independently reused across dozens of
  follow-on science-of-science papers (several of which appear in this
  same triage: Wang et al., Shi & Evans, Lin/Evans/Wu).

## Follow-up

- **Relevance:** 5 — this is the canonical empirical basis for the
  project's `[[atypical-combination]]` bibliometric feature and one of
  H1's two named citations; the plan's feature-block bullet on
  atypicality (10th-percentile / minimum) is modeled directly on this
  paper's method.
- Read the supplementary methods (Science online) before implementing
  the null model in `genesis/features` — the randomization procedure has
  details (fixed marginals) that matter for correctness.
