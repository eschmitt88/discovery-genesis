---
kind: paper
title: "Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers"
authors: ["Chenglei Si", "Diyi Yang", "Tatsunori Hashimoto"]
institutions: ["Stanford University"]
year: 2024
venue: "arXiv preprint (COLM-style topics; no confirmed peer-reviewed venue found in-text)"
peer_reviewed: unknown
url: "https://arxiv.org/abs/2409.04109"
code_url: "https://github.com/NoviScl/AI-Researcher"
citations: 432
source: "raw/papers/si2024can.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: skimmed
related_experiments: []
related_concepts: ["retrodiction-test", "ideation-execution-gap"]
tags: ["llm-ideation", "h6", "baseline", "human-study"]
---

# Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers

## TL;DR

A controlled, blinded head-to-head: 100+ NLP researchers each write a novel
research idea on a specified topic, an LLM ideation agent generates ideas on
the same topics, and a separate pool of expert reviewers blind-rates both
pools. LLM ideas are judged statistically significantly more novel than
human-expert ideas, but slightly weaker on feasibility.

## Claims

- With careful experimental controls (matched topics, standardized idea
  format, blind review, style normalization to defeat "LLM tells" in
  writing), LLM-generated ideas score higher on novelty than human expert
  ideas (p < 0.05).
- LLM self-evaluation of idea quality is unreliable and LLM idea generation
  lacks diversity (near-duplicate ideas across many samples).
- Human novelty/feasibility judgments are themselves noisy — inter-reviewer
  agreement on "is this idea novel" is not high even among experts.

## Methods

- Recruited 79 expert researchers to write ideas, 100+ to review, across a
  fixed set of NLP research topics.
- Standardized idea format (title, problem, motivation, proposed method,
  experiment plan) and an LLM-based style normalizer to strip
  distinguishing tells between human and LLM prose before blind review.
- Reviewers rate novelty, feasibility, excitement, expected effectiveness
  on Likert scales, blind to authorship.

## Results

- LLM ideas: higher novelty (statistically significant), lower feasibility,
  reviewers occasionally flag LLM ideas as vague or infeasible at
  implementation detail.
- The paper explicitly stops short of claiming the ideas are *good* in any
  outcome sense — it only measures novelty/feasibility *as judged*, and
  proposes the follow-up execution study (see si2025ideation) as the
  necessary next test.

## Critique / open questions

- Novelty/feasibility ratings are subjective proxies for whether an idea
  would actually work; the paper itself flags this and designed the
  execution follow-up specifically to test it (si2025ideation).
- The reviewer pool judges idea *descriptions*, not idea outcomes — the
  same category of risk H6's closeness-ladder judge faces.

## Trust signals

- **Credibility:** 5 — Stanford, extremely widely discussed/cited (432,
  Semantic Scholar) within under two years, rigorous blinded human-study
  design with real domain experts (not crowdworkers), code and review data
  released.

## Follow-up

- **Relevance: 5** — This is the named anchor paper for the whole
  LLM-idea-generation literature and the direct methodological precedent
  for H6's retrodiction-test design: blind expert judging, novelty vs.
  feasibility as separate axes, and — critically — an explicit admission
  that novelty/feasibility judgments alone can be misleading, which its own
  2025 follow-up (si2025ideation) then demonstrates empirically. H6's judge
  design should borrow the blinding and style-normalization protocol and
  heed the self-evaluation-unreliability finding when designing the
  retrodiction judge.
