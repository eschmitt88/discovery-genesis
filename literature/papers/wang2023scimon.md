---
kind: paper
title: "SciMON: Scientific Inspiration Machines Optimized for Novelty"
authors: ["Qingyun Wang", "Doug Downey", "Heng Ji", "Tom Hope"]
institutions: ["University of Illinois at Urbana-Champaign", "Allen Institute for Artificial Intelligence (AI2)", "The Hebrew University of Jerusalem"]
year: 2023
venue: "ACL 2024"
peer_reviewed: true
url: "https://arxiv.org/abs/2305.14259"
code_url: "https://github.com/eaglew/clbd"
citations: 211
source: "raw/papers/wang2023scimon.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: skimmed
related_experiments: []
related_concepts: ["retrodiction-test"]
tags: ["llm-ideation", "h6", "baseline", "literature-grounded"]
---

# SciMON: Scientific Inspiration Machines Optimized for Novelty

## TL;DR

Given a background context (problem, motivation, focus points), retrieve
"inspiration" papers from past literature and generate a natural-language
research idea grounded in them, then iteratively compare the idea against
prior work and update it until a novelty threshold is met. Moves beyond
prior literature-based-discovery work's binary link prediction to
free-text idea generation. Finds naive GPT-4 prompting alone produces
low-novelty, shallow ideas — motivating the iterative-novelty-boosting loop.

## Claims

- Prior literature-based hypothesis generation was limited to binary link
  prediction between concepts, severely limiting the expressivity of what
  could be proposed as a "new idea."
- A dedicated iterative loop that retrieves inspirations and explicitly
  checks/boosts novelty against prior papers outperforms single-pass
  generation, including naive GPT-4 prompting, which the paper finds
  produces low-novelty, low-depth ideas.

## Methods

- Pipeline: background context -> inspiration retrieval (from a corpus of
  prior (background, idea) pairs) -> idea generation grounded in retrieved
  inspirations -> iterative novelty-boosting loop that compares the
  candidate idea against prior literature and revises until a novelty
  criterion is satisfied.

## Results

- Comprehensive evaluation (automatic + human) shows the retrieval +
  iterative-novelty-boosting pipeline produces more novel, more
  literature-grounded ideas than single-pass LLM prompting baselines.

## Critique / open questions

- Novelty is operationalized as difference from retrieved prior
  (background, idea) pairs — a proxy that, like the judges in
  sinhahajari2026limits, could reward superficial rephrasing over genuine
  novelty if not carefully validated against human judgment.
- Predates the current generation of strong instruction-tuned LLMs (GPT-4
  era baseline); the "naive GPT-4 is low-novelty" finding may or may not
  hold with newer models.

## Trust signals

- **Credibility:** 5 — ACL 2024 peer-reviewed, UIUC + AI2 + Hebrew
  University, code released, 211 citations (Semantic Scholar); this is a
  well-established reference point in the LLM-ideation literature.

## Follow-up

- **Relevance: 5** — Named explicitly in this project's own research plan
  ("a SciMON-style literature-inspired generator") as one of the required
  H6 baselines. Also documents the specific failure mode — naive LLM
  prompting yields low-novelty, low-depth ideas — that motivates why this
  project bets on a move-taxonomy/genesis-model approach rather than
  retrieval-plus-novelty-check alone. H6's baseline suite must include a
  SciMON-style generator (retrieve inspirations + iterative novelty
  boosting) as a comparison point for the genesis-informed skill.
