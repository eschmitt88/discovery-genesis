---
kind: paper
title: "Chain of Ideas: Revolutionizing Research via Novel Idea Development with LLM Agents"
authors: ["Long Li", "Weiwen Xu", "Jiayan Guo", "Ruochen Zhao", "Xingxuan Li", "Yuqian Yuan", "Boqiang Zhang", "Yuming Jiang", "Yifei Xin", "Ronghao Dang", "Yu Rong", "Deli Zhao", "Tian Feng", "Lidong Bing"]
institutions: ["DAMO Academy, Alibaba Group", "Zhejiang University", "University of Science and Technology of China"]
year: 2024
venue: "EMNLP 2024"
peer_reviewed: true
url: "https://arxiv.org/abs/2410.13185"
code_url: "https://github.com/DAMO-NLP-SG/CoI-Agent"
citations: 114
source: "raw/papers/li2024chain.pdf"
added: "2026-08-22"
relevance: 4
credibility: 5
status: skimmed
related_experiments: []
related_concepts: ["retrodiction-test"]
tags: ["llm-ideation", "h6", "baseline", "agentic"]
---

# Chain of Ideas: Revolutionizing Research via Novel Idea Development with LLM Agents

## TL;DR

Organizes retrieved literature on a topic into a chain that mirrors the
progressive historical development of that research direction, then has an
LLM agent extrapolate the "next" idea in the chain — rather than either
trivially prompting an LLM or dumping unstructured literature into context.
Evaluated with the authors' own "Idea Arena" protocol against human
researcher preferences.

## Claims

- Existing idea-generation methods either trivially prompt LLMs (no
  literature grounding) or expose LLMs to large amounts of literature
  without structure, in both cases limiting idea quality.
- Structuring literature as a chronological chain that "mirrors the
  progressive development" of a subfield gives the LLM agent a better
  causal/historical scaffold from which to extrapolate a next idea, versus
  flat retrieval.

## Methods

- Retrieve literature relevant to a target research direction; organize it
  into a chain structure ordered to reflect the field's progressive
  development (a proxy for the field's own genesis-model history).
- LLM agent (Chain-of-Ideas, "CoI-Agent") extrapolates from the end of the
  chain to propose a next idea.
- "Idea Arena" evaluation protocol: pairwise comparisons against
  human-researcher-generated ideas and/or other systems' ideas, judged for
  preference.

## Results

- CoI-Agent's chain-structured approach reportedly outperforms flat
  retrieval-based and naive-prompting baselines in Idea Arena preference
  comparisons.

## Critique / open questions

- "Progressive development" chains are themselves a genesis-model
  assumption (roughly accretion / incremental extrapolation) baked into
  the generator design — worth noting as a structural contrast to this
  project's four-genesis-model taxonomy, which treats incremental
  extrapolation as only one mode among several.
- Idea Arena, like other LLM-idea evaluation protocols, likely inherits
  some of the judge-reliability concerns documented in
  sinhahajari2026limits; the paper does not test for a novelty-mirage
  effect specifically.

## Trust signals

- **Credibility:** 5 — EMNLP 2024 peer-reviewed, Alibaba DAMO Academy +
  Zhejiang University + USTC, code released
  (DAMO-NLP-SG/CoI-Agent), 114 citations.

## Follow-up

- **Relevance: 4** — A structurally distinct baseline generator
  (progression/chain-based extrapolation, versus SciMON's
  retrieve-and-novelty-check or MOOSE-Chem's background+inspiration
  composition) that broadens the comparison set H6 needs when benchmarking
  the genesis-informed skill against "the idea generators in the
  literature." Its Idea Arena protocol is a reusable evaluation-harness
  reference, though it should be checked against the judge-failure-mode
  warnings in sinhahajari2026limits before reuse.
