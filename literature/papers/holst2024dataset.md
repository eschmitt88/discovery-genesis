---
kind: paper
title: "Dataset Artefacts are the Hidden Drivers of the Declining Disruptiveness in Science"
authors: ["Vincent Holst", "Andres Algaba", "Floriano Tori", "Sylvia Wenmackers", "Vincent Ginis"]
institutions: ["Vrije Universiteit Brussel", "KU Leuven", "University of Massachusetts Boston"]
year: 2024
venue: "arXiv preprint 2402.14583; published as Nature Matters Arising \"Dataset artefacts can partially drive the measured decline in disruption\" (2026), DOI 10.1038/s41586-026-10787-y"
peer_reviewed: true
url: "https://arxiv.org/abs/2402.14583"
code_url: null
citations: 8
source: "raw/papers/holst2024dataset.pdf"
added: "2026-08-22"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["disruption-index"]
tags: ["disruption", "bibliometrics", "cd-index", "critique", "dispute"]
---

# Dataset Artefacts are the Hidden Drivers of the Declining Disruptiveness in Science

## TL;DR

Argues that Park, Leahey & Funk's (2023) reported decline in
disruptiveness (CD5) is substantially a dataset/plotting artefact: a bug
in seaborn's histogram rendering silently dropped the largest data
points, hiding a spike of maximum-disruption (CD = +1) papers — these are
overwhelmingly zero-backward-citation works ("pure dataset artefacts"),
whose relative decline over time drives most of the apparent trend.

## Claims

- The apparent secular decline in CD5 largely disappears once
  zero-backward-reference works are handled correctly / excluded.
- The original paper's own published histograms are internally
  inconsistent with the underlying data due to a plotting-library
  default that clips outliers rather than binning them.
- Up to ~93% of the reported decline in the largest dataset the original
  paper used is attributable to this artefact.

## Methods

- Re-obtains the same six datasets as Park, Leahey & Funk (2023) (or
  their nearest available reconstructions) and recomputes CD-index
  histograms without the plotting truncation, isolating the
  zero-reference-work subpopulation's contribution to the trend.

## Results

- The recomputed distributions show a previously-hidden mass of CD=+1
  papers; their declining share over time (not a genuine shift in the
  disruptiveness of "normal" papers) explains most of the headline trend.

## Critique / open questions

- Published as a Nature "Matters Arising" after a 32-month editorial
  delay (per the authors' own public statement); Park, Leahey & Funk
  filed a simultaneous reply disputing the critique's own data handling
  and reporting that the original trend survives under the critics'
  methods too. This project holds only the arXiv preprint's full text —
  the final peer-reviewed Nature exchange (both pieces) was paywalled at
  fetch time (403 on direct request), so the reply's specifics here are
  drawn from secondary search coverage, not primary text. Flagged as a
  genuinely **unresolved, live dispute** rather than a settled correction.
- Directly actionable for this project: the pipeline should compute CD5
  both with and without zero-backward-citation works isolated, and
  report both, rather than picking a side in a dispute that is still in
  print.

## Trust signals

- **Credibility:** 4 — peer-reviewed (Nature Matters Arising track),
  technically concrete and falsifiable claim (a specific plotting-library
  bug with a specific consequence), but a single critique still actively
  contested by the original authors and not yet independently
  replicated by a third party as of this writing.

## Follow-up

- **Relevance:** 4 — this is the single most load-bearing 2024-2026
  update on the disruption-index thread this project's
  `[[disruption-index]]` concept depends on; the concept file already
  anticipated exactly this kind of dispute ("the decline result is
  under open dispute in Nature... document raw vs corrected CD") and
  this note is the primary citation backing that sentence.
- Follow the resolution: if a third-party replication settles the
  dispute before the pipeline's H1 experiment runs, update
  `[[disruption-index]]`'s recommended raw-vs-corrected default
  accordingly.
