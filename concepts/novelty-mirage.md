---
kind: concept
name: "novelty mirage"
status: seedling
added: "2026-08-22"
sources: ["sinhahajari2026limits", "si2024can"]
related_concepts: ["retrodiction-test", "hindsight-narrative-bias"]
related_experiments: []
tags: ["evaluation", "h6", "threat", "judge-failure"]
---

# Novelty mirage

## Definition

An LLM judge asked to rate the novelty of an LLM-generated research
artifact (a research question, hypothesis, or contribution) systematically
rates it as more novel than a domain expert would — and the bias gets
*stronger*, not weaker, under comparative/pairwise judging rather than
standalone scoring. Coined as "novelty mirage" by
`[[sinhahajari2026limits]]` (RQ-Bench), which reconstructs author-anchored
research questions from a paper's own cited background/gaps/contributions
and shows LLM judges prefer generated alternatives that domain experts
reject.

## Why it matters here

H6's retrodiction test hinges entirely on an LLM judge rating how close a
generated contribution is to the real one. If the judge has a novelty
mirage — over-crediting the generated candidate for looking novel/original
— the closeness ladder is biased in exactly the direction that would make
the skill look better than it is. This is a sharper, more mechanistic
version of the generic "calibrate the judge against humans" caution
already in the research plan: it says *how* the judge fails (over-rates
novelty, worse under pairwise comparison, misses narrow/source-bound
answers) rather than just that it might.

## Connections

- `[[si2024can]]` independently documents a related failure: LLM
  self-evaluation of idea quality is unreliable, and LLM-generated ideas
  get rated more novel than expert ideas by human reviewers even before
  any judge-specific bias is introduced — so some of the "novelty"
  overrating is a real property of the artifacts, and some is a property
  of the judge. RQ-Bench isolates the judge-specific component by using
  the *same* generated content across standalone vs. comparative judging
  and finding the comparative mode makes the bias worse.
- Directly threatens `[[retrodiction-test]]`'s 0-4 closeness ladder; see
  that concept's "Reusable protocols" note for the specific audit steps
  (standalone vs. comparative judging, narrowness/source-boundedness
  checks, avoiding same-model-family judge/generator pairs).
- Distinct from `[[hindsight-narrative-bias]]`: that concept is about a
  *coder* (human or LLM) narrating a genesis that didn't happen; this one
  is about a *judge* over-crediting novelty of a candidate it is scoring.
  Both are hindsight-adjacent contamination risks but act on different
  pipeline stages (coding vs. evaluation).
