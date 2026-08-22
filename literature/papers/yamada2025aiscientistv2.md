---
kind: paper
title: "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search"
authors: ["Yutaro Yamada", "Robert Tjarko Lange", "Cong Lu", "Shengran Hu", "Chris Lu", "Jakob Foerster", "Jeff Clune", "David Ha"]
institutions: ["Sakana AI", "University of British Columbia", "Vector Institute", "FLAIR, University of Oxford", "Canada CIFAR AI Chair"]
year: 2025
venue: "arXiv preprint (technical report)"
peer_reviewed: false
url: "https://arxiv.org/abs/2504.08066"
code_url: "https://github.com/SakanaAI/AI-Scientist-v2"
citations: 359
source: "raw/papers/yamada2025aiscientistv2.pdf"
added: "2026-08-22"
relevance: 4
credibility: 4
status: skimmed
related_experiments: []
related_concepts: ["retrodiction-test"]
tags: ["llm-ideation", "full-pipeline", "execution", "ceiling-reference"]
---

# The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

## TL;DR

Sakana AI's end-to-end agentic system (successor to AI Scientist v1):
formulates hypotheses, designs and runs experiments via agentic tree
search, analyzes/visualizes results, and authors a full manuscript with no
human-authored code template required. Three fully autonomous manuscripts
were submitted to a real, peer-reviewed ICLR workshop; one scored above the
average human-acceptance threshold — the first fully AI-generated paper to
pass peer review.

## Claims

- Removing the human-authored code template dependency (present in v1)
  lets the system generalize across diverse ML domains rather than one
  templated setup.
- A progressive agentic tree-search methodology, managed by a dedicated
  experiment-manager agent, replaces a flatter generate-and-check loop.
- Adding a VLM feedback loop over generated figures materially improves
  manuscript quality/aesthetics.
- One of three autonomous submissions to a real ICLR workshop exceeded the
  average human acceptance score.

## Methods

- Pipeline stages: hypothesis formulation -> experiment design ->
  tree-searched experiment execution -> data analysis/visualization ->
  manuscript authoring -> (separately) an AI reviewer with VLM feedback for
  iterative refinement.
- Evaluated by actually submitting three full manuscripts to a real,
  peer-reviewed ICLR workshop and reporting the acceptance-relevant scores
  received.

## Results

- One of three submissions cleared the workshop's average human-acceptance
  score bar under real peer review — the paper's headline result.
- Code fully open-sourced.

## Critique / open questions

- "Exceeded the average human acceptance score" at one workshop, on one
  submission out of three, is a narrow evidentiary base for a strong
  general claim; the paper is explicit this is a first instance, not a
  reliability claim.
- This is the full pipeline including execution — directly relevant to
  the ideation-execution-gap warning (si2025ideation): it is evidence that
  execution-plus-idea, end to end, *can* clear a real bar, which is a
  different (higher, harder) target than H6's closeness-ladder judging of
  ideas alone.

## Trust signals

- **Credibility:** 4 — Sakana AI + Oxford (FLAIR)/UBC/Vector Institute,
  code fully open-sourced, 359 citations (Semantic Scholar); the paper
  itself is an arXiv technical report, not peer-reviewed, though its
  *result* (workshop acceptance of generated papers) was independently
  peer-reviewed.

## Follow-up

- **Relevance: 4** — The most credible existing "full pipeline" precedent
  (idea through execution through review) for what a genesis-informed
  skill could ultimately be judged against beyond the closeness ladder —
  a ceiling reference for what "the idea worked" can mean once execution
  is included, and a direct empirical counterpoint/complement to
  si2025ideation's warning that ideation-stage judgments don't survive
  execution. H6 should cite this as the aspirational (but out-of-scope for
  now) evaluation tier above the retrodiction test, not attempt to
  replicate its execution stage in the pilot.
