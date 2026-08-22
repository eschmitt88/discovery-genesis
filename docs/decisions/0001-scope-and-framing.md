---
kind: decision
id: 1
title: Scope and framing of discovery-genesis
status: accepted
date: "2026-08-22"
---

# 0001 — Scope and framing

## Context

The user wants to discover how discoveries are made: look at impactful
research papers and their citations and work out what they did to get
from prior art to the contribution. End product: a `SKILL.md`. The user
flagged a worry — that the natural framing *prior art → novel idea →
impactful paper* might force an intermediate step that is not always real
— and an interest in both novelty and impact.

## Decision

- **The "idea step" is a hypothesis, not the frame.** Every case is coded
  with one of four genesis models (idea-first / means-first /
  problem-first / accretion) and the evidence for it; the authors' own
  narrative is recorded separately. H0 estimates the distribution.
- **Novelty and impact are separate axes** on every case. Sampling is on
  field-normalised impact; novelty is measured, not selected.
- **Matched controls from the start.** Every impactful case has a twin
  from the same topic-year at median impact. No claim about what
  impactful papers do is made without the paired comparison.
- **Random, field-stratified sampling** via the `xpol` sampler from
  `llm-cross-pollination` (OpenAlex topic frame), restricted to the three
  STEM domains. That sampler is already built and tested, so this
  project does not wait on the other one.
- **Unit of analysis** is the paper (with its reference list and
  citation neighbourhood), captured as a genesis card. Whether the
  paper-plus-lineage is the better unit is an open question for the
  pilot.
- **Deliverable** is `skill/genesis/SKILL.md`, evaluated by a
  retrodiction test on a held-out split (HCE) before being proposed to
  `claude-system` via `/elevate`.
- **Order of work:** pipeline + bibliometric H1 on a 20-pair pilot (cheap,
  tests whether the twin design has signal) → open coding → codebook →
  full set → skill → retrodiction.
- **Repo:** public, `agency: standard` for now; `--experiments` linked
  because phases 1–4 are empirical.

## Consequences

- The project may conclude that the skill is mostly about problem
  selection and timing rather than idea generation. That is an acceptable
  outcome and is stated up front.
- Consolidating papers (databases, reviews) will enter the impact sample.
  They are kept, coded as accretion, and reported with/without; if they
  dominate, disruption becomes a second sampling axis.
- LLM coders' prior knowledge of famous papers is a contamination risk
  for both coding and evaluation; mitigations are in the card schema and
  the retrodiction protocol, and are audited rather than assumed.
