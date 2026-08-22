---
kind: paper
title: "On the Limits of LLM-as-Judge for Scientific Novelty Assessment"
authors: ["Soumitra Sinhahajari", "Navonil Majumder", "Soujanya Poria"]
institutions: ["DeCLaRe Lab, Nanyang Technological University"]
year: 2026
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2606.12071"
code_url: "https://huggingface.co/datasets/declare-lab/rq-bench"
citations: 3
source: "raw/papers/sinhahajari2026limits.pdf"
added: "2026-08-22"
relevance: 5
credibility: 3
status: read
related_experiments: []
related_concepts: ["retrodiction-test", "novelty-mirage"]
tags: ["llm-ideation", "h6", "judge-failure", "novelty-mirage"]
---

# On the Limits of LLM-as-Judge for Scientific Novelty Assessment

## TL;DR

Introduces RQ-Bench: for a set of recent arXiv papers, reconstruct
author-anchored research questions (RQs) from each paper's own cited
background, gaps, and stated contributions — a retrodiction-style
construction. Model-generated RQs (from the same background) are then
compared against these author-anchored reference RQs by standalone LLM
judges, comparative LLM judges, and human domain experts. LLM judges
consistently rate model-generated RQs as highly novel — a "novelty
mirage" — while domain experts reach the opposite conclusion and prefer
the author-anchored questions.

## Claims

- LLM-as-judge for scientific novelty is unreliable in a specific,
  reproducible direction: it systematically over-rates novelty of
  LLM-generated research questions relative to what a domain expert
  would say, and the effect gets *stronger*, not weaker, under comparative
  (pairwise) judging.
- Many generated RQs are narrow or "source-bound" (they hew closely to the
  cited background rather than genuinely extending it) — a defect LLM
  judges tend not to catch unless explicitly probed for it.
- The RQ-Bench construction method (reconstruct an author-anchored RQ from
  a paper's own background/gaps/contributions) is itself close to this
  project's retrodiction-test unit, just one level upstream (research
  question rather than full hypothesis/contribution).

## Methods

- Build RQ-Bench from recent arXiv papers: for each, reconstruct the
  "author-anchored" RQ from the paper's stated background, gap, and
  contribution (not from the full paper) — a retrodiction-style label.
- Generate comparison RQs from the same background using LLMs.
- Evaluate three ways: standalone LLM judging (rate one RQ), comparative
  LLM judging (rate a pair head-to-head), and human domain-expert
  evaluation — allowing a direct LLM-judge-vs-human-judge contrast on the
  same items.

## Results

- Standalone LLM judges rate generated RQs as highly novel.
- Comparative LLM judging makes the LLM-favoring bias *stronger*.
- Human experts prefer the author-anchored reference RQs over the
  generated ones — the opposite conclusion from the LLM judges.
- Narrowness/source-boundedness of generated RQs is under-detected by LLM
  judges unless the evaluation explicitly tests for it.

## Critique / open questions

- Focuses on research-question novelty, one step removed from full
  hypothesis/contribution judging (MOOSE-Chem, IdeaBench, H6's own ladder)
  — the failure mode may compound or partially cancel at that further
  remove; untested here.
- Very recent (June 2026) and not yet peer-reviewed; single lab's finding,
  though the direction (LLM judges over-rate LLM-flavored novelty) is
  consistent with community discussion elsewhere in this space.
- Small citation count reflects recency, not a credibility problem per se,
  but also means no independent replication yet exists.

## Trust signals

- **Credibility:** 3 — reputable group (DeCLaRe Lab, NTU, same lab as
  yang2024moose's Soujanya Poria co-author), dataset released on
  HuggingFace (declare-lab/rq-bench), but arXiv-only preprint as of
  ingest, very recent (3 citations), single-institution, no independent
  replication yet.

## Follow-up

- **Relevance: 5** — This is the sharpest, most direct negative result on
  exactly the mechanism H6's retrodiction judge depends on: an LLM judge
  scoring "closeness"/novelty of a generated idea against a real one. Its
  finding that comparative judging *worsens* the bias is a specific,
  actionable warning — H6 should not assume pairwise/tournament judging is
  safer than standalone scoring. Directly supports the research plan's
  existing commitment to calibrate the judge against human ratings on a
  subset, and gives that plan concrete failure-mode evidence rather than
  a generic worry. Seeds the `novelty-mirage` concept (see below).
