---
kind: paper
title: "Long-run patterns in the discovery of the adjacent possible"
authors: ["Josef Taalbi"]
institutions: ["Lund University"]
year: 2022
venue: "Industrial and Corporate Change (arXiv preprint; accepted 2025)"
peer_reviewed: true
url: "https://arxiv.org/abs/2208.00907"
code_url: null
citations: 2
source: "raw/papers/tria2022adjacent.pdf"
added: "2026-08-22"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["adjacent-possible", "genesis-models"]
tags: ["h4", "problem-first", "quantitative-adjacent-possible"]
---

# Long-run patterns in the discovery of the adjacent possible

## TL;DR

A quantitative test of Kauffman's "adjacent possible" against a century
of Swedish product-introduction data (1908–2016): innovation modeled as a
search-and-recombination process over a constantly-restructuring
reachable space. Innovation rate depends *linearly* on cumulative past
innovations (explaining incumbent-firm advantage while ruling out
winner-take-all dynamics), new-product-type discovery follows Heaps' law
(a declining share of genuinely new types as organizations mature), and
the topology of the product space itself carries predictive information
about what gets discovered next — the adjacent possible is not wholly
"unprestatable."

**Correction to the candidate triage file**: the candidate list attributed
this paper to "Tria, Loreto, et al." — the actual, sole author is **Josef
Taalbi** (Dept. of Economic History, Lund University); there is no Tria/
Loreto co-authorship on this specific arXiv ID (2208.00907). Citekey and
authorship corrected accordingly; the candidate file's `## Curation`
entry below flags this.

## Claims

- The rate of introduction of qualitatively new product types is well
  described by a generalized Heaps'-law-style relationship: the *share*
  of novel types declines as an organization's (or economy's) cumulative
  output grows, mirroring vocabulary-growth laws in text.
- Aggregate innovation rate depends linearly on cumulative past
  innovations — an organization's history of past innovation predicts its
  future rate, which explains why incumbents keep innovating (they sit
  closer to more of the current adjacent possible) without producing
  extreme winner-take-all concentration.
- The product space's topology (which product types are "close" to
  which) carries real predictive signal about which new types will be
  discovered next — the adjacent possible has *structure*, not just size.

## Methods

- Long-run empirical dataset: Swedish product/technology introductions,
  1908–2016 (SWINNO database), coded by organization and product type.
- Fits combinatorial/search-theoretic models of the adjacent possible
  (rate of discovery as a function of the reachable-combination space)
  against the empirical introduction and diversification patterns; tests
  Heaps'-law and preferential-attachment-style predictions.

## Results

- Empirical support across a century of data for: (a) linear dependence
  of innovation rate on cumulative innovations; (b) Heaps'-law decline in
  novel-type share; (c) product-space topology predicting future
  diversification direction, i.e., some of the adjacent possible is
  foreseeable from where an organization currently sits.

## Critique / open questions

- Single national economy (Sweden), and "innovation" here is
  commercial-product introduction, not scientific-paper contribution —
  the mapping from firm/product adjacent-possible dynamics to a single
  paper's ingredient-arrangement move is an analogy this project must
  earn, not assume.
- Long-run, aggregate/statistical patterns do not by themselves identify
  the *move* an individual actor made to reach a specific new
  combination — complements rather than substitutes for this project's
  case-level `genesis_model` coding.

## Trust signals

- **Credibility:** 4 — Lund University (Dept. of Economic History), a
  century-scale purpose-built historical dataset (SWINNO), accepted at a
  peer-reviewed journal (Industrial and Corporate Change, 2025); citation
  count still low (2) reflecting recency of the arXiv preprint relative
  to formal publication.

## Follow-up

- **Relevance:** 4 — gives problem-first / adjacent-possible genesis a
  quantitative, falsifiable empirical form (rather than only the
  Kauffman/Johnson metaphor) and a directly reusable methodology (Heaps'
  law on novel-type share; topology-based predictability of the next
  reachable combination) for the project's own H1/H4 feature pipeline —
  e.g., is a case's contribution predictable from the topology of its
  subfield's citation/topic space before reading it?
