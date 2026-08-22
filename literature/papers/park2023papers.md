---
kind: paper
title: "Papers and patents are becoming less disruptive over time"
authors: ["Michael Park", "Erin Leahey", "Russell J. Funk"]
institutions: ["University of Minnesota (Carlson School of Management)", "University of Arizona (Department of Sociology)"]
year: 2023
venue: "Nature 613:138-144"
peer_reviewed: true
url: "https://www.nature.com/articles/s41586-022-05543-x"
code_url: "https://doi.org/10.5281/zenodo.7258379"
citations: 872
source: "raw/papers/park2023papers.pdf"
added: "2026-08-22"
relevance: 5
credibility: 4
status: read
related_experiments: []
related_concepts: ["disruption-index", "novelty-vs-impact"]
tags: ["disruption", "bibliometrics", "cd-index", "secular-trend"]
---

# Papers and patents are becoming less disruptive over time

## TL;DR

Using the CD index over 45M papers and 3.9M patents (1945-2010),
disruptiveness (CD5) has declined steadily across nearly all fields and
patent classes even as output volume grew; the authors attribute this to
a narrowing of "attention" per unit of knowledge (papers and patents
increasingly build on, and cite, a narrower slice of prior art) rather
than to a decline in the quality of ideas.

## Claims

- CD5 has fallen roughly monotonically across six decades in essentially
  every field studied, for both papers and patents.
- The decline correlates with growth in reference-list length and with
  narrower citation to "canonical"/highly-cited prior work over time
  ("standing on the shoulders of giants" more narrowly).
- Team size, individual scientists' own career trajectories, and language
  used in abstracts (more "developing/improving" vocabulary, less
  "discover/create" vocabulary over time) move in the same direction.

## Methods

- CD index (Funk & Owen-Smith 2017 formula) computed per paper/patent
  from citation-network structure across six large datasets (WoS,
  APS, USPTO, and others), 1945-2010.
- Secondary analyses: reference-list length over time, career-level CD
  trajectories, text analysis of abstract language.

## Results

- The decline holds "nearly universally" — the headline claim this
  project's `[[disruption-index]]` concept treats as the canonical
  large-scale application the pipeline's CD5 feature is modeled on.

## Critique / open questions

- **This is now a live, unresolved methodological dispute.** A 2026
  Nature Matters Arising (Holst, Algaba, Tori, Wenmackers & Ginis; this
  project's `holst2024dataset` note) argues that a seaborn plotting bug
  hid a spike of maximum-disruption (CD = +1) papers from the published
  histograms, and that dataset artefacts — chiefly zero-backward-citation
  works — account for up to ~93% of the reported decline in the largest
  dataset. Park, Leahey & Funk's simultaneous reply (summarized only via
  secondary coverage here, Nature's reply text itself being paywalled)
  disputes the critique's own data quality and reports the original
  trend survives under the critics' own methods too. Separately, Bentley/
  Petersen et al. (`petersen2023disruption`) argue growing reference-list
  length mechanically drives CD toward zero regardless of any real change
  in disruptiveness ("citation inflation"), a distinct critique from the
  plotting-artefact one.
- **Decision for this project** (per `docs/research-plan.md` open
  questions): treat CD5 as a card *feature*, never a *selection*
  criterion, and compute both raw and a deflated/corrected variant so the
  pipeline's own numbers are legible regardless of how this dispute
  resolves.

## Trust signals

- **Credibility:** 4 — top-tier venue (Nature), massive scale (45M+3.9M
  records), 872 citations, and the code/data are openly deposited on
  Zenodo (unusually good reproducibility signal for a Nature paper). Held
  at 4 rather than 5 because the paper's central empirical claim is
  currently the subject of an active, technically substantive Matters
  Arising dispute (`holst2024dataset`) that this project has not
  independently adjudicated.

## Follow-up

- **Relevance:** 5 — the canonical large-scale application of the
  disruption index the plan's `[[disruption-index]]` feature (CD5,
  computed from OpenAlex citers) is modeled on; sets the secular-trend
  context for any disruption number the `genesis` pipeline computes, and
  its contested status is exactly why the project's CLAUDE.md /
  research-plan flag "document raw vs corrected CD" as a required
  decision before H1 runs.
