---
kind: paper
title: "The disruption index is biased by citation inflation"
authors: ["Alexander M. Petersen", "Felber Arroyave", "Fabio Pammolli"]
institutions: ["University of California, Merced", "Politecnico di Milano"]
year: 2023
venue: "arXiv preprint 2306.01949; published in Quantitative Science Studies (2024), DOI 10.1162/qss_a_00333"
peer_reviewed: true
url: "https://arxiv.org/abs/2306.01949"
code_url: null
citations: 25
source: "raw/papers/petersen2023disruption.pdf"
added: "2026-08-22"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["disruption-index"]
tags: ["disruption", "bibliometrics", "cd-index", "critique", "citation-inflation"]
---

# The disruption index is biased by citation inflation

## TL;DR

Shows the CD index is mechanically biased toward 0 over time by
"citation inflation": ever-growing reference-list lengths increase
citation-network density and push CD toward zero regardless of any real
change in disruptiveness; a second driver is rising self-citation /
triadic closure in reference-list construction. A weighted/deflated CD
variant mutes or reverses the apparent secular decline.

## Claims

- Reference-list-length growth alone, holding "true" disruptiveness
  fixed, drives CD toward 0 in a simulated citation network — i.e. the
  bias exists even in a null model with no real behavioral change.
- Self-citation and rising triadic closure in citation-network
  construction confound CD, since CD is itself a measure of a network's
  triadic-closure structure.
- This systematic time-dependent bias also confounds any attempt to
  correlate CD with other time-varying quantities (team size, citation
  counts) — a direct warning for this project's planned team-size feature.

## Methods

- Three complementary lines of critique: (1) deductive/analytic argument
  from the CD formula's structure; (2) empirical analysis of real
  citation-network reference-list-length trends; (3) computational
  modeling using an ensemble of synthetic citation networks with known,
  fixed ground-truth disruptiveness, released for others to test
  alternative indices against.

## Results

- The synthetic-network experiments show CD trending toward 0 purely
  from reference-list-length growth, with no change in the generative
  process's "true" disruptiveness — a clean identification of the bias
  mechanism, independent of the Holst et al. plotting-artefact critique.

## Critique / open questions

- This is a *distinct* critique from `holst2024dataset`'s plotting-bug
  argument — one is about database/rendering artefacts, this one is
  about a structural bias inherent to the CD formula itself as reference
  lists lengthen. Both point the same direction (raw CD5 secular decline
  is at least partly artefactual) but via different, non-overlapping
  mechanisms; the pipeline should be aware it may need to correct for
  both independently.
- Released a synthetic-network test suite — worth using directly to
  validate whichever CD implementation (raw or deflated) the `genesis`
  `features` stage ships, rather than trusting the implementation on
  faith.

## Trust signals

- **Credibility:** 4 — peer-reviewed (Quantitative Science Studies, MIT
  Press), reputable authors/institutions (UC Merced, Politecnico di
  Milano), a testable synthetic-network methodology with released
  materials referenced in-text. Held at 4 rather than 5 as a single
  critique paper (25 citations) rather than an established, widely
  replicated correction.

## Follow-up

- **Relevance:** 4 — a second, independent, mechanistically distinct
  critique of the CD index the plan's `[[disruption-index]]` concept
  needs to weigh alongside `holst2024dataset` before the pipeline commits
  to a raw-vs-corrected CD default; also a direct caution against the
  plan's planned team-size/CD correlation analysis (Wu/Wang/Evans-style),
  since team size and CD may both be confounded by reference-list-length
  trends over the same period.
