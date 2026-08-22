---
kind: paper
title: "Accelerating science with human-aware artificial intelligence"
authors: ["Jamshid Sourati", "James A. Evans"]
institutions: ["University of Chicago", "Santa Fe Institute"]
year: 2023
venue: "Nature Human Behaviour"
peer_reviewed: true
url: "https://arxiv.org/abs/2306.01495"
code_url: null
citations: 74
source: "raw/papers/sourati2023accelerating.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: []
related_concepts: ["retrodiction-test", "adjacent-possible", "genesis-models"]
tags: ["h6", "prediction", "evaluation-design"]
---

# Accelerating science with human-aware artificial intelligence

## TL;DR

Models that simulate what a scientist could plausibly infer next from the
literature ("digital doubles" of human expertise, built from co-authorship
and topical-attention distributions) predict actual future discoveries —
and *who* will make them — far better than models that use publication
content alone; the same machinery, tuned to avoid the human-predicted
crowd, generates "alien" hypotheses unlikely to be pursued by anyone for
years.

## Claims

- Incorporating the distribution of human scientific attention (who works
  on what, who collaborates with whom, over time) into a discovery-
  prediction model improves prediction of future discoveries by up to
  400% over content-only baselines, especially where relevant literature
  is sparse.
- The improvement works by predicting *human predictions* — modeling which
  combinations of topics scientists are about to notice and combine,
  not just which combinations are latently plausible in the content.
- The same framework can be inverted to surface "alien" hypotheses:
  scientifically promising combinations that are unlikely to be imagined
  by the current human distribution of attention until much later.

## Methods

- Trains unsupervised link-prediction models over a co-evolving
  bipartite graph of scientists and topics/entities, using simulated
  "digital doubles" — inferences that would be cognitively accessible to
  a working scientist given the literature and collaboration network at
  time t — as an additional signal alongside content embeddings.
- Evaluates on held-out future discoveries (new topic/entity
  combinations that later appear in the literature), scoring both
  *what* will be discovered and *who* will discover it.

## Results

- Human-aware models substantially outperform content-only AI models at
  forecasting future discoveries, with the largest gains in sparse
  (low-precedent) areas — exactly where a content-only model has the
  least signal.
- Tuning the model to predict combinations *far* from the current human
  attention distribution yields candidate hypotheses characterized as
  "alien": plausible from content but not yet within reach of the
  field's collective attention.

## Critique / open questions

- The evaluation is retrodictive on the *combination* (topic pair), not
  on the specific claim/contribution a paper makes — a coarser unit than
  this project's genesis card. Still the closest existing precedent for
  H6's design: hide the future, show the model the prior state, score
  whether it recovers what actually happened.
- "Alien" hypotheses are validated by rarity/lateness of human discovery,
  not by an independent judge of scientific merit — a different
  validation problem than this project's closeness-ladder + usefulness
  judge.

## Trust signals

- **Credibility:** 5 — University of Chicago Sociology + Santa Fe
  Institute authors, published in Nature Human Behaviour (peer-reviewed,
  top venue), 74 citations already accrued since 2023.

## Follow-up

- **Relevance:** 5 — the single closest existing precedent for the
  project's H6 retrodiction test (hide the paper, show the prior state,
  score recovery); its human-aware vs. content-only vs. "alien" framing
  is a ready-made baseline family alongside the plan's SciMON-style
  comparator and a live illustration that *problem-first* discovery
  (the field was already converging on it) and *idea-first* discovery
  ("alien", ahead of the field) are empirically separable rather than
  purely conceptual categories.
- Consider whether the "digital double" attention-distribution signal
  could itself become a card feature: was this paper's move already
  "in the air" per the human-attention model, or was it genuinely alien?
