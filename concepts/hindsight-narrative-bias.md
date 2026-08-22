---
kind: concept
name: "hindsight narrative bias"
status: seedling
added: "2026-08-22"
sources: ["yang2024moose", "medawar1963fraud", "dunbar1997scientists", "simonton2010bvsr"]
related_concepts: ["genesis-models", "genesis-card", "retrodiction-test"]
related_experiments: []
tags: ["method", "threat"]
---

# Hindsight narrative bias

## Definition

A paper's introduction narrates the genesis the authors wish had happened:
motivation → hypothesis → test. Medawar called the form a fraud. Award
lectures and interviews do the same with more distance. LLM coders add a
third layer: they may already know what the paper became.

## Why it matters here

It is the main threat to H0. Mitigations built into the card: the
`authors_story` field is kept separate from our `genesis_model`; coders are
instructed to code from the paper's *prior* references and its methods
section logic, not its introduction; the `evidence` field is audited;
external stories are opportunistic corroboration, never the primary
source.

## Connections

- Means-first genesis is the one most likely to be rewritten as
  idea-first, so any idea-first estimate from introductions is an upper
  bound.
- `[[medawar1963fraud]]` (Howitt & Wilson's 2014 revisit of Medawar's
  1963 argument) is the source of "Medawar called the form a fraud"
  above, and adds that the distortion is *trained in*: students learn to
  write, and to expect, the tidy hypothesis-then-confirmation narrative
  from textbook exemplars, which primes them to misremember their own
  research the same way later.
- `[[dunbar1997scientists]]` supplies a rare direct counter-example: one
  discovery was captured live, on tape, during a lab meeting — evidence
  that a genuinely means-first genesis can be documented as it happens,
  which is what makes it possible to detect when a later introduction
  rewrites it as idea-first.
- `[[simonton2010bvsr]]`'s BVSR theory gives the theoretical mechanism:
  a creator can be genuinely blind with respect to the ultimate success
  criterion while still reporting (truthfully, from their own vantage)
  a partially-sighted, idea-first-sounding process — narrative bias need
  not be dishonest to be systematic.
- `[[yang2024moose]]` (MOOSE-Chem) is the cleanest external precedent for
  controlling the LLM-coder-already-knows-the-outcome variant of this
  bias: rather than probing and excluding recallable cases, it benchmarks
  only on papers published *after* the generating LLM's training cutoff,
  so hindsight contamination is structurally impossible rather than
  merely audited. Worth weighing against this project's `evidence`-field
  audit approach for the LLM-coder pipeline itself, not just for H6.
