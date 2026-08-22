---
kind: paper
title: "MOOSE-Chem: Large Language Models for Rediscovering Unseen Chemistry Scientific Hypotheses"
authors: ["Zonglin Yang", "Wanhao Liu", "Ben Gao", "Tong Xie", "Yuqiang Li", "Wanli Ouyang", "Soujanya Poria", "Erik Cambria", "Dongzhan Zhou"]
institutions: ["Nanyang Technological University", "Shanghai Artificial Intelligence Laboratory", "University of Science and Technology of China", "Wuhan University", "University of New South Wales", "GreenDynamics", "Singapore University of Technology and Design"]
year: 2024
venue: "ICLR 2025"
peer_reviewed: true
url: "https://arxiv.org/abs/2410.07076"
code_url: "https://github.com/ZonglinY/MOOSE-Chem"
citations: 66
source: "raw/papers/yang2024moose.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: []
related_concepts: ["retrodiction-test", "genesis-card", "move-taxonomy"]
tags: ["llm-ideation", "h6", "retrodiction", "memorisation-control"]
---

# MOOSE-Chem: Large Language Models for Rediscovering Unseen Chemistry Scientific Hypotheses

## TL;DR

Gives an LLM only the *background* (question + optional survey) of 51
high-impact 2024+ chemistry/materials papers (Nature/Science-tier) and asks
it to retrieve "inspiration" papers and compose/rank hypotheses that
rediscover the paper's actual contribution — using a model with a
pre-2024 knowledge cutoff so the rediscovery cannot be attributed to
memorising the target paper. Reports high similarity between rediscovered
and ground-truth hypotheses, especially on inspiration retrieval.

## Claims

- A hypothesis can be decomposed as h = f(b, i1, ..., ik): background b
  plus k ∈ [1,3] inspirations composes into hypothesis h. This
  decomposition is grounded in both domain-expert interviews and the
  cognitive-science finding that creative ideas often come from associating
  two previously unrelated pieces of knowledge (Koestler).
- The decomposition factors P(h|b) into a per-step product of
  P(inspiration_j | b, h_{j-1}, corpus) x P(h_j | b, h_{j-1}, i_j) — an MDP
  over (retrieve inspiration, update hypothesis) steps, making an
  intractable single-shot generation task into a sequence of tractable
  retrieval/composition steps.
- LLMs are surprisingly accurate at inspiration retrieval — an
  out-of-distribution task — suggesting LLMs may encode latent scientific
  associations not yet recognized as such by humans.

## Methods

- **Benchmark construction (TOMATO-Chem):** 51 chemistry/materials papers,
  published and put online *after January 2024*, restricted to top venues
  (27 Nature/Science, 20 Nature subjournals, 4 other top journals),
  annotated by chemistry PhD students into: background question (+ strict
  variant), background survey (+ strict variant), 1-3 inspiration paper
  titles + reason, hypothesis, experiments, reasoning process linking
  background+inspirations to hypothesis.
- **Contamination control:** the generating LLM's training-data cutoff
  predates the papers' publication date (post-Jan-2024), so any successful
  rediscovery cannot be explained by the model having seen the target paper
  during training — the paper states this explicitly as the reason
  rediscovery "is not because of data contamination."
- **Expert QA on constructed cards:** annotators re-check that (1)
  inspirations are correctly identified and complete, (2) the background
  contains no leaked information from inspirations/hypothesis, (3) the
  background + inspirations can plausibly, logically lead to the
  hypothesis.
- **Method:** an agentic pipeline directly implementing the 3-subtask
  decomposition — retrieve inspirations, compose hypothesis from
  background + inspirations, rank candidate hypotheses.

## Results

- High similarity between LLM-composed hypotheses and ground truth across
  the 51-paper benchmark; notably strong performance specifically on the
  inspiration-retrieval subtask.
- Framework generalizes the same recipe across polymer, organic, inorganic,
  and analytical chemistry.

## Critique / open questions

- 51 papers, hand-annotated by domain PhDs — not cheaply scalable to other
  fields without similar annotation investment.
- "Rediscovery similarity" is itself judged by an LLM/similarity metric;
  the paper does not deeply interrogate whether *that* judge has the same
  novelty-mirage failure mode documented in sinhahajari2026limits.
- The "strict" background variant (excluding hint-y phrasing) is the more
  honest test; results on the non-strict variant likely overstate
  difficulty reduction.

## Trust signals

- **Credibility:** 5 — peer-reviewed at ICLR 2025, multi-institution
  (NTU, Shanghai AI Lab, USTC, Wuhan, UNSW, STUD), code + benchmark
  released, 66 citations, benchmark hand-built and QA'd by domain PhD
  chemists rather than crowdworkers.

## Follow-up

- **Relevance: 5** — This is the closest existing implementation of this
  project's own H6 retrodiction test: hide-the-paper, show only the
  background, retrieve inspirations from prior art, compose and rank
  hypotheses, judge recovery similarity to ground truth — with an explicit,
  citable knowledge-cutoff contamination control (post-cutoff paper dates
  rather than a recall-probe exclusion). H6's evaluation harness should
  study and largely reuse its (a) task decomposition into
  retrieve/compose/rank, (b) post-cutoff-date memorisation control, and
  (c) expert QA protocol on constructed background/inspiration splits,
  rather than rebuilding from scratch. See the "Reusable protocols" note
  added to `concepts/retrodiction-test.md`.
