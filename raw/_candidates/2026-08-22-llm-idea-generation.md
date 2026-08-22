---
kind: candidates
topic: "LLM research-idea generation and its evaluation"
discovered: 2026-08-22
source: discover
n_requested: 14
n_returned: 14
curated: 2026-08-22
---

## 1. Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers

- url: https://arxiv.org/abs/2409.04109
- type: paper
- summary: Si, Yang & Hashimoto (2024) run a blinded head-to-head where 100+ NLP researchers write ideas and separately judge LLM-generated vs. human expert ideas, finding LLM ideas rated more novel but slightly weaker on feasibility.
- reason: The named anchor paper for this topic and the H6 baseline generator/evaluator design (blind human rating, novelty vs. feasibility axes) the retrodiction test should benchmark against.

## 2. The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas

- url: https://arxiv.org/abs/2506.20803
- type: paper
- summary: The 2025 execution follow-up to #1: 43 researchers each spend 100+ hours executing a randomly assigned expert- or LLM-written idea; LLM-idea scores drop significantly more after execution, flipping some rankings in humans' favor.
- reason: Directly warns H6 that closeness-to-idea judging without execution can overstate LLM idea quality — motivates keeping the retrodiction judge's closeness ladder honest and not treating "sounds good" as "would have worked."

## 3. MOOSE-Chem: Large Language Models for Rediscovering Unseen Chemistry Scientific Hypotheses

- url: https://arxiv.org/abs/2410.07076
- type: paper
- summary: Gives an LLM only the "background" of 51 high-impact 2024+ chemistry papers (with a pre-2024 knowledge-cutoff model) and asks it to retrieve inspirations and compose/rank hypotheses that rediscover the paper's actual contribution, reporting high recovery similarity.
- reason: This is the closest existing implementation of the project's own retrodiction test — hide-the-paper, show-the-background-and-inspirations, judge recovery — with an explicit knowledge-cutoff contamination control; H6's evaluation harness should study and likely reuse its task decomposition (retrieve/compose/rank) and cutoff-date memorization control rather than rebuild from scratch.

## 4. On the Limits of LLM-as-Judge for Scientific Novelty Assessment

- url: https://arxiv.org/abs/2606.12071
- type: paper
- summary: Introduces RQ-Bench, which reconstructs author-anchored research questions from a paper's cited background/gaps/contributions (a retrodiction-style construction), and finds LLM judges rate model-generated research questions as highly novel ("novelty mirage") where domain experts do not.
- reason: A direct, credible negative result on LLM-as-judge for exactly the kind of novelty/closeness judgment H6's evaluation depends on — argues for human calibration of the judge on a subset, which the plan already specifies but this paper gives concrete failure-mode evidence for.

## 5. SciMON: Scientific Inspiration Machines Optimized for Novelty

- url: https://arxiv.org/abs/2305.14259
- type: paper
- summary: Wang, Downey, Ji & Hope (ACL 2024) generate literature-grounded research directions by retrieving "inspiration" papers and iteratively updating ideas against prior work until a novelty threshold is met, finding GPT-4 alone produces low-novelty, low-depth ideas.
- reason: Named explicitly in the research plan as a baseline family ("a SciMON-style literature-inspired generator") that H6's retrodiction test must run against; also documents the low-novelty failure mode of naive LLM ideation that motivates the project's move-taxonomy approach.

## 6. Accelerating science with human-aware artificial intelligence

- url: https://arxiv.org/abs/2306.01495
- type: paper
- summary: Sourati & Evans train unsupervised models on simulated expert inference (not just literature content) and show this improves prediction of future discoveries by up to 400%, especially where literature is sparse, and can also be tuned to surface "alien" hypotheses unlikely to be pursued by humans.
- reason: Frames prediction of future research as a modeling target distinct from idea generation itself — relevant to whether the skill should model "what the community would try next" (problem/timing, H5) versus "what move is available" (H3), and gives a credible prior-art baseline for forecasting-style evaluation.

## 7. SciMuse: Interesting Scientific Idea Generation Using Knowledge Graphs and LLMs — Evaluations with 100 Research Group Leaders

- url: https://arxiv.org/abs/2405.17044
- type: paper
- summary: Gu & Krenn build a co-occurrence knowledge graph from ~58M papers and combine it with GPT-4 to generate personalized research ideas, evaluated for interest by over 100 real research group leaders across 4,400+ ideas.
- reason: A large, credible human-evaluation precedent (real domain-expert raters, not crowdworkers) for judging whether a generated idea is any good — directly informs how H6's human-rating calibration subset should be recruited and scored.

## 8. Predicting the Future of AI with AI: High-Quality Link Prediction in an Exponentially Growing Knowledge Network

- url: https://arxiv.org/abs/2210.00881
- type: paper
- summary: Krenn et al. build the Science4Cast benchmark (100k+ papers, 64k+ concept nodes) and show curated network features beat end-to-end learned approaches at forecasting which concept pairs will be combined in future AI research.
- reason: The clearest prior instance of a "predict future research combinations from the prior-art graph" task with a fixed evaluation benchmark — a structural precedent for treating retrodiction as link/combination prediction over a paper's reference graph rather than free-text idea generation.

## 9. Chain of Ideas: Revolutionizing Research via Novel Idea Development with LLM Agents

- url: https://arxiv.org/abs/2410.13185
- type: paper
- summary: Organizes retrieved literature into a chain mirroring a research topic's progressive development, then has an LLM agent extrapolate the next idea in the chain, evaluated via the authors' "Idea Arena" protocol against human-researcher preferences.
- reason: A second, structurally different baseline generator (progression-based rather than retrieval-and-novelty-check like SciMON) that H6 should include for diversity, plus its Idea Arena protocol is a reusable evaluation-harness reference.

## 10. ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models

- url: https://arxiv.org/abs/2404.07738
- type: paper
- summary: Baek et al. augment a seed paper with an academic knowledge graph and a concept store, then iteratively refine problem/method/experiment proposals using human-preference-aligned LLM reviewer agents.
- reason: A third baseline architecture (iterative self-review rather than single-pass generation) broadening the comparison set H6 needs against "the idea generators in the literature," and its reviewer-agent design is a candidate component for the retrodiction judge itself.

## 11. The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

- url: https://arxiv.org/abs/2504.08066
- type: paper
- summary: Sakana AI's end-to-end system (successor to AI-Scientist v1, arXiv:2408.06292) that formulates hypotheses, runs experiments via agentic tree search, and authors manuscripts — one autonomous submission exceeded the average human acceptance score at a real ICLR workshop.
- reason: The most credible existing "full pipeline" precedent (idea through execution through review) for what a genesis-informed skill could ultimately be judged against beyond the closeness ladder — a ceiling reference for what "the idea worked" can mean once execution is included, echoing entry #2's warning.

## 12. IdeaBench: Benchmarking Large Language Models for Research Idea Generation

- url: https://arxiv.org/abs/2411.02429
- type: paper
- summary: Builds a dataset of influential papers' titles/abstracts plus their reference lists and a standardized framework for scoring LLM-generated ideas against the real paper's contribution.
- reason: Structurally the closest published benchmark to the project's own genesis-card unit (paper + its references as input, real contribution as the target) — worth checking directly for reusable data/scoring before building H6's held-out split from scratch.

## 13. LiveIdeaBench: Evaluating LLMs' Scientific Creativity and Idea Generation with Minimal Context

- url: https://arxiv.org/abs/2412.17596
- type: paper
- summary: Tests 40+ LLMs on single-keyword scientific ideation across 1,180 keywords and 22 domains using a dynamic multi-model judge panel, finding idea-generation quality is poorly predicted by general-intelligence benchmarks; the authors report explicit measures against contamination/overfitting via the rotating judge ensemble.
- reason: A recent (2025), large-scale creativity benchmark with an explicit contamination-mitigation design and a multi-judge-ensemble approach — a concrete alternative to single-LLM-judge scoring that H6's judge design should consider to reduce the novelty-mirage failure mode documented in entry #4.

## 14. Large Language Models for Scientific Idea Generation: A Creativity-Centered Survey

- url: https://arxiv.org/abs/2511.07448
- type: paper
- summary: A November 2025 (revised Feb 2026) survey organizing LLM-driven scientific ideation methods into five families (knowledge augmentation, prompt-based steering, inference-time scaling, multi-agent collaboration, parameter-level adaptation) through Boden's and Rhodes' creativity frameworks.
- reason: The most recent dedicated survey of this exact literature; its five-family taxonomy is a useful cross-check against this project's own move-taxonomy (H2) to see whether "how ideas get generated" and "how papers actually arose" categorize similarly or reveal a mismatch worth noting.
