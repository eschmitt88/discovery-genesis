---
kind: concept
name: "move taxonomy"
status: seedling
added: "2026-08-22"
sources: ["dunbar1997scientists", "sternberg1999propulsion"]
related_concepts: ["triz-lineage", "genesis-card", "atypical-combination", "novelty-vs-impact"]
related_experiments: []
tags: ["core", "h2", "h3"]
---

# Move taxonomy

## Definition

The codebook of operations a paper performs on its prior art. Derived
bottom-up by open coding the pilot, then frozen. A *prior* list, to be
overwritten by the data, not imposed on it:

transfer (method imported from another field) · recombination (two cited
components never previously combined) · scale (same method, far more
data / compute / resolution) · instrument (a quantity becomes observable)
· resource (dataset / benchmark / database that becomes the shared
reference) · simplification (remove a part; it still works) · inversion
(negate a standing assumption) · unification (two things shown to be one)
· relaxation (lift a constraint) · reformulation (recast X as a Y problem)
· anomaly (explain a noticed discrepancy) · consolidation (review /
standard that crystallises) · gap-filling (the obvious next experiment,
done first or best) · formalisation (folklore made rigorous).

## Why it matters here

H2 asks whether a short list like this covers most impactful work and is
stable across fields; H3 asks which entries are impact-enriched relative
to twins. The enriched entries, with worked examples from `cases/`, become
the body of the skill. An orthogonal *enabler* axis (new data / tool /
compute / theory / collaboration / imported problem) is coded alongside.

## Connections

- TRIZ's 40 principles are the precedent and the warning
  ([[triz-lineage]]): a catalogue is only useful if it beats a baseline.
- "Transfer" is the whole of `llm-cross-pollination`; its base rate here is
  that project's premise check.
- `[[dunbar1997scientists]]` supplies worked examples for two entries:
  "anomaly" (18 of 70 tracked findings were unexpected and drew more
  reasoning than expected ones) and a *distance* sub-feature on any
  analogy-based move (99 observed analogies were overwhelmingly local —
  40 within-organism, 57 other-organism, only 2 non-biological — so
  "transfer" should be coded with how far the import travelled, not just
  whether it occurred).
- `[[sternberg1999propulsion]]` is an independent, previously-published
  ~8-type taxonomy (sorted by paradigm-acceptance/rejection) that
  cross-checks this list's plausible size and suggests
  paradigm-relationship as a candidate orthogonal coding axis alongside
  `move` and `enabler`.
