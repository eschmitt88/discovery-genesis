---
kind: paper
title: "Bias against Novelty in Science: A Cautionary Tale for Users of Bibliometric Indicators"
authors: ["Jian Wang", "Reinhilde Veugelers", "Paula Stephan"]
institutions: ["KU Leuven", "Georgia State University", "Harvard University", "National Bureau of Economic Research", "CEPR", "Bruegel"]
year: 2017
venue: "Research Policy 46(8):1416-1436 (NBER Working Paper 22180, 2016)"
peer_reviewed: true
url: "https://www.nber.org/papers/w22180"
code_url: null
citations: 535
source: "raw/papers/wang2017bias.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: ["2026-08-22-h1-pilot-bibliometrics"]
related_concepts: ["novelty-vs-impact", "atypical-combination"]
tags: ["novelty", "bibliometrics", "h1", "citation-windows"]
---

# Bias against Novelty in Science: A Cautionary Tale for Users of Bibliometric Indicators

## TL;DR

Defines novelty as a paper's *first-ever* combination of two journals in
its reference list (weighted by their prior co-citation distance).
Novel papers are cited *less* in the short run but are more likely to
become a top-1%-cited paper and to be cross-disciplinary in the long run
— so bibliometric indicators that use short citation windows
systematically penalize novelty.

## Claims

- Novelty (first-time journal-pair combination) predicts higher variance
  in eventual impact: more failures, but a disproportionate share of the
  very top-cited papers.
- The novelty penalty is a *timing* artifact of short citation windows,
  not evidence that novel work is lower quality.
- Novel papers are more likely to be published in lower-impact-factor
  journals and to take longer to receive their first citations.

## Methods

- All Web of Science research articles from a single publication year
  (2001), tracked for citations over a long follow-up window.
- Novelty operationalized at the journal-pair level (distinct from
  Uzzi et al.'s topic/journal-pair z-score against a randomized null):
  a paper is "novel" if it makes a combination of two journals in its
  references that has never before co-occurred in any paper's reference
  list, weighted by how distant those journals' typical co-citation
  patterns are.

## Results

- Novel papers are ~26% less likely to be top-1%-cited in the first 3
  years post-publication but ~30% *more* likely to be top-1%-cited over
  a longer horizon.
- Peer reviewers and citers alike appear to discount unfamiliar
  combinations early; recognition catches up only with time.

## Critique / open questions

- A second, independent operationalization of "novelty" alongside Uzzi's
  atypicality proxy — useful for triangulating the project's H1 novelty
  measure, and a direct warning that the plan's 2010-2019 sampling
  window (chosen so impact "has accrued") may still be short enough to
  systematically undercount novel-but-slow-burning cases, i.e. exactly
  the sleeping-beauty concern already flagged in `docs/research-plan.md`
  open questions.

## Trust signals

- **Credibility:** 5 — published in Research Policy (peer-reviewed) after
  circulating as NBER Working Paper 22180; reputable co-authors (Stephan
  is a leading science-of-science economist); 535 citations; the finding
  is now a standard citation in the bibliometrics literature warning
  against short-window citation metrics.

## Follow-up

- **Relevance:** 5 — directly named in the curation brief as a project-
  owned bibliometric source; sharpens `[[novelty-vs-impact]]` with a
  second novelty operationalization and a concrete mechanism (citation-
  window bias) for why novelty and impact "correlate weakly" — not
  because they are unrelated, but because short windows mismeasure the
  novel tail.
- Held file is the 2016 NBER working paper text; the peer-reviewed
  version (Research Policy 2017) is textually near-identical per the
  authors' own citation trail — noted here rather than re-fetched, since
  `raw/` treats a re-fetch of the same content as unnecessary duplication.
