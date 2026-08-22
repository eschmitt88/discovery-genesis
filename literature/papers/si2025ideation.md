---
kind: paper
title: "The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas"
authors: ["Chenglei Si", "Tatsunori Hashimoto", "Diyi Yang"]
institutions: ["Stanford University"]
year: 2025
venue: "arXiv preprint"
peer_reviewed: unknown
url: "https://arxiv.org/abs/2506.20803"
code_url: "https://github.com/NoviScl/AI-Researcher"
citations: 5
source: "raw/papers/si2025ideation.pdf"
added: "2026-08-22"
relevance: 5
credibility: 4
status: skimmed
related_experiments: []
related_concepts: ["retrodiction-test", "ideation-execution-gap"]
tags: ["llm-ideation", "h6", "execution-gap", "human-study"]
---

# The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas

## TL;DR

The direct execution follow-up to si2024can: 43 expert researchers each
spend 100+ hours executing an idea (randomly assigned, either LLM-generated
or human-expert-written, blind to origin), write a short paper on the
result, and the resulting papers are blind-reviewed. LLM-idea scores drop
significantly more than human-idea scores after execution on every metric
(novelty, excitement, effectiveness, overall) — closing, and in several
metrics flipping, the gap observed at the ideation stage alone.

## Claims

- Ideation-stage novelty/feasibility ratings (as in si2024can) do not
  reliably predict post-execution quality.
- LLM ideas look relatively better *before* anyone tries to build them and
  relatively worse *after* — the ideation-execution gap is directional and
  consistent across raters and metrics.
- Judging "closeness to a good idea" without any execution signal
  systematically overstates LLM idea quality relative to human ideas.

## Methods

- 43 researchers recruited, each executes exactly one idea (assignment
  randomized and blind to whether it was LLM- or human-authored) over
  100+ hours, producing a 4-page short paper.
- Executed papers blind-reviewed by a separate pool of expert NLP
  researchers on the same axes as the ideation-stage study (novelty,
  excitement, effectiveness, overall), enabling a paired
  before/after comparison on the *same* ideas.

## Results

- Post-execution scores for LLM-generated ideas fall significantly more
  than for human ideas across all four metrics (p < 0.05); rankings flip
  in humans' favor on several.
- This directly falsifies the assumption that a static novelty/feasibility
  judgment (no execution) is a safe proxy for "would this idea have been a
  good contribution."

## Critique / open questions

- 43 pairs is a modest sample for a claim this strong; the paper is explicit
  that this is a first empirical demonstration, not a general law.
- The mechanism behind the drop (LLM ideas underspecified? harder to debug
  during execution? less robust to the researcher's own judgment calls
  mid-project?) is not isolated.

## Trust signals

- **Credibility:** 4 — same Stanford group as si2024can, an unusually
  expensive and rigorous execution study (43 researchers x 100+ hours each),
  data/code released; citation count (5) is low only because the paper is
  ~2 months old at ingest time, not a quality signal.

## Follow-up

- **Relevance: 5** — This is the single most important methodological
  warning for H6: it is direct, empirical evidence that a closeness-to-idea
  judge (exactly what the retrodiction test's 0-4 ladder is) can rank LLM
  output favorably relative to human output in a way that inverts once
  outcomes are known. H6 already treats this as a risk in
  `concepts/retrodiction-test.md`; this paper is the citable evidence for
  why the closeness ladder must not be read as "would have worked," and
  motivates keeping a genuine execution or expert-outcome check (even a
  cheap one) somewhere downstream of the ladder score, not just a bigger n
  on the judge.
