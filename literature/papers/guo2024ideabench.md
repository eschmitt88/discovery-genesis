---
kind: paper
title: "IdeaBench: Benchmarking Large Language Models for Research Idea Generation"
authors: ["Sikun Guo", "Amir Hassan Shariatmadari", "Guangzhi Xiong", "Albert Huang", "Eric Xie", "Stefan Bekiranov", "Aidong Zhang"]
institutions: ["University of Virginia"]
year: 2024
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2411.02429"
code_url: "https://anonymous.4open.science/r/IdeaBench-2747/"
citations: 14
source: "raw/papers/guo2024ideabench.pdf"
added: "2026-08-22"
relevance: 5
credibility: 3
status: read
related_experiments: []
related_concepts: ["retrodiction-test", "genesis-card"]
tags: ["llm-ideation", "h6", "benchmark", "retrodiction"]
---

# IdeaBench: Benchmarking Large Language Models for Research Idea Generation

## TL;DR

Builds a dataset of 2,374 influential target papers' titles/abstracts plus
their reference papers, profiles an LLM as a domain-specific researcher
grounded in the same references a human author would have had, and scores
the LLM's generated idea against the real paper's idea using a
"personalized quality ranking" metric ("Insight Score") rather than
similarity alone.

## Claims

- Idea generation should be evaluated the way a human researcher actually
  generates ideas: target a topic, review recent related literature,
  identify gaps, propose an idea addressing the gap — and the benchmark's
  dataset/prompting is built to emulate exactly that sequence.
- A single similarity-to-ground-truth score is not sufficient to capture
  idea quality (novelty, feasibility, etc., can trade off); the paper
  proposes ranking generated ideas together with the real target idea on a
  user-specified quality indicator, then reading off a relative-rank-based
  score.

## Methods

- **Dataset construction:** curate influential target papers (title +
  abstract) plus their reference-paper abstracts, filtered for quality;
  2,374 target papers after filtering.
- **Idea generation:** prompt LLMs, given the target paper's references
  (not the target paper itself), to generate a candidate research idea —
  mirroring this project's own genesis-card setup (prior art in, real
  contribution held out).
- **Insight Score:** for a target paper and n LLM-generated ideas, present
  all n+1 ideas (n generated + 1 real) to a ranking judge (GPT-4o) with a
  user-specified quality indicator (e.g. novelty, feasibility), obtain the
  rank r_target of the real idea in that list, and compute
  I(LLM, q) = (r_target - 1) / n, averaged over target papers. I=0 means
  the real idea always ranks best (LLM cannot beat it on q); I=1 means the
  real idea always ranks last (LLM ideas always judged superior on q).
  This directly extends similarity scoring into a scalable, user-defined
  quality-ranking framework instead of a single novelty/feasibility number.
- Code and dataset released via an anonymized repository
  (anonymous.4open.science/r/IdeaBench-2747).

## Results

- Reports Insight Scores across several LLMs and quality indicators (e.g.
  novelty, feasibility), demonstrating the metric differentiates models
  and indicators where plain similarity scoring would not.

## Critique / open questions

- The ranking judge (GPT-4o) is itself an LLM judge for a novelty-adjacent
  quality indicator — the same class of instrument flagged as unreliable
  in sinhahajari2026limits; IdeaBench does not test its judge against
  human experts for the novelty-mirage failure mode.
- Dataset construction and evaluation both lean on the paper's own
  abstract/reference structure rather than full text — coarser-grained
  than MOOSE-Chem's hand-annotated background/inspiration/hypothesis
  splits, but far more scalable (2,374 papers vs. 51).
- Not yet peer-reviewed; single-institution (UVA); no external
  replication.

## Trust signals

- **Credibility:** 3 — single institution (UVA), arXiv preprint with no
  confirmed peer-reviewed venue at ingest, moderate citations (14), but
  code + dataset released and the ranking-metric design is coherent and
  reused-worthy regardless of venue status.

## Follow-up

- **Relevance: 5** — Structurally the closest published benchmark to this
  project's own genesis-card unit: paper's references in, real
  contribution as the held-out target, and a formal scoring framework
  (Insight Score) instead of ad hoc similarity. H6's retrodiction test
  should check IdeaBench's exact dataset-construction and ranking-based
  scoring approach directly for reuse before building the held-out split
  and closeness ladder from scratch — the rank-based Insight Score
  (present ground truth alongside generated candidates and read off its
  rank, rather than scoring each independently) is a distinct alternative
  to a fixed 0-4 closeness ladder and may be more robust to judge
  miscalibration.
