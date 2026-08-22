---
kind: concept
name: "ideation execution gap"
status: seedling
added: "2026-08-22"
sources: ["si2025ideation", "si2024can", "yamada2025aiscientistv2"]
related_concepts: ["retrodiction-test", "novelty-vs-impact", "novelty-mirage"]
related_experiments: []
tags: ["evaluation", "h6", "threat"]
---

# Ideation execution gap

## Definition

A research idea's quality *as judged before execution* (novelty,
feasibility, excitement ratings on the idea description alone) does not
reliably predict its quality *after execution* (the outcome once someone
actually builds/runs it). `[[si2025ideation]]` shows this directly: 43
researchers each spent 100+ hours executing a randomly assigned idea
(human- or LLM-authored, blind to origin); LLM-idea review scores dropped
significantly more than human-idea scores after execution across every
metric, closing and in several cases flipping the ideation-stage
advantage LLM ideas held in the companion study, `[[si2024can]]`.

## Why it matters here

H6's retrodiction test is, structurally, an ideation-stage-only
evaluation: it judges closeness of a *proposed* contribution to the real
one, with no execution step. This concept names the specific risk that
finding is good news at H6's own granularity — the skill could look
better than it is if judged only pre-execution, exactly the pattern this
paper demonstrates. It argues for (a) treating the closeness-ladder score
explicitly as a ceiling/proxy, never as "would have worked," in whatever
the skill's own documentation says about its evaluation, and (b) keeping
an eye toward a cheap downstream execution or expert-outcome check if the
project ever has budget for one, rather than trusting the ladder score in
isolation.

## Connections

- `[[novelty-vs-impact]]` is the paper-level analogue of the same
  decoupling — atypicality/novelty and field impact correlate only
  weakly there too. The mechanism is different (bibliometric selection
  and diffusion vs. a controlled execution experiment) but the shape of
  the finding — apparent quality pre-outcome is a poor proxy for quality
  post-outcome — is the same warning at two different grains.
- `[[novelty-mirage]]` is a *judge*-side version of a related risk (the
  judge over-rates novelty); the ideation-execution gap is an *artifact*-
  side version (the idea itself performs worse once tried). Both push in
  the same direction: don't trust a pre-outcome LLM rating of an
  LLM-generated candidate.
- `[[yamada2025aiscientistv2]]` is a counterpoint/ceiling case: a full
  idea-through-execution-through-review pipeline that did clear a real
  peer-review bar on at least one submission — evidence that the gap is
  not unbridgeable, just that ideation-only judging understates it.
- Directly cited in `[[retrodiction-test]]`'s Connections and "Reusable
  protocols" sections as the reason the closeness ladder needs an
  explicit "this is not an execution outcome" caveat.
