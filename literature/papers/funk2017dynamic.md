---
kind: paper
title: "A Dynamic Network Measure of Technological Change"
authors: ["Russell J. Funk", "Jason Owen-Smith"]
institutions: ["University of Minnesota", "University of Michigan"]
year: 2017
venue: "Management Science 63(3):791-817"
peer_reviewed: true
url: "https://pubsonline.informs.org/doi/10.1287/mnsc.2015.2366"
code_url: null
citations: 480
source: "raw/papers/funk2017dynamic.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: []
related_concepts: ["disruption-index", "novelty-vs-impact"]
tags: ["disruption", "bibliometrics", "cd-index", "method"]
---

# A Dynamic Network Measure of Technological Change

## TL;DR

Introduces the CD index: a focal paper/patent is "disruptive" to the
extent that its later citers tend to cite it *without* also citing its
own references (they treat it as a fresh starting point), and
"consolidating" to the extent the opposite holds. Validated on university
patent data: federal funding is linked to more destabilizing (high-CD)
inventions, commercial ties to more consolidating (low-CD) ones.

## Claims

- Disruption and consolidation are two ends of one measurable spectrum,
  computable purely from citation-network structure (no text needed).
- The index predicts real institutional differences: federally-funded
  university patents disrupt more; patents tied to firms consolidate more.

## Methods

- For a focal work, define: n_i = citers that cite the focal work but not
  its references (disrupting); n_j = citers that cite both the focal
  work and its references (consolidating); n_k = citers that cite the
  focal work's references but not the focal work itself.
- CD = (n_i - n_j) / (n_i + n_j + n_k), bounded in [-1, 1].
- Computable for any paper/patent purely from OpenAlex citer lists and
  their own reference lists — no full text required, matching this
  project's data-sources design.

## Results

- CD index varies systematically with funding source and institutional
  context in the university-patenting sample, supporting construct
  validity beyond just "high CD = more citations."

## Critique / open questions

- The index is known (per later critiques in this same triage — Bentley/
  Petersen et al. 2023, Holst et al. 2024) to be sensitive to reference-
  list length and to citation-network density, both of which have shifted
  secularly over the decades the project's 2010-2019 sample spans. The
  pipeline should treat raw CD5 as one candidate feature, not a ground
  truth, pending the deflated/corrected variants those papers propose.

## Trust signals

- **Credibility:** 5 — top-tier peer-reviewed venue (Management Science),
  480 citations, and this is the primary source that every later CD-index
  application and critique (Park/Leahey/Funk 2023, Bentley/Petersen et
  al. 2023, Holst et al. 2024) cites as the index's origin — the
  foundational reference, not a restatement of it.

## Follow-up

- **Relevance:** 5 — this is the primary source for the exact CD/CD5
  formula the plan's `[[disruption-index]]` concept names; needed to
  implement the metric correctly (the n_i/n_j/n_k definitions) rather
  than relying only on secondary descriptions in the later Nature papers.
- The pipeline's `features` stage should cite this paper's formula
  directly in its docstring/comments, not a paraphrase.
