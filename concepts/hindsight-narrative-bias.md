---
kind: concept
name: "hindsight narrative bias"
status: seedling
added: "2026-08-22"
sources: []
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
