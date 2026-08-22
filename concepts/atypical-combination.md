---
kind: concept
name: "atypical combination"
status: seedling
added: "2026-08-22"
sources: []
related_concepts: ["novelty-vs-impact", "move-taxonomy", "adjacent-possible"]
related_experiments: []
tags: ["metric", "h1"]
---

# Atypical combination

## Definition

Uzzi et al.'s bibliometric novelty measure: for each pair of journals (here,
topics) a paper cites together, how unusual that pairing is relative to a
randomised null for the same year. A paper is summarised by its
conventionality (median pair z-score) and its atypical tail (10th
percentile). The headline finding: highest-impact papers combine a
conventional core with a small atypical tail.

## Why it matters here

It is the one novelty measure computable for every case and twin from
OpenAlex alone, before any reading, so H1 can run on day one of the
pipeline. It is also a prior about what the *transfer* and *recombination*
moves should look like in the references: mostly home-field, with a few
far citations that do the work.

## Connections

- The null model needs a background sample of reference lists per
  field-year; size that in the pipeline, not per case.
- Measures the *reference list*, not the contribution — a paper can cite
  atypically and do nothing with it. The card's `ingredients` field is
  the check.
