---
kind: concept
name: "retrodiction test"
status: seedling
added: "2026-08-22"
sources: []
related_concepts: ["genesis-card", "move-taxonomy", "hindsight-narrative-bias"]
related_experiments: []
tags: ["evaluation", "h6"]
---

# Retrodiction test

## Definition

The evaluation of the deliverable: hide the paper, show the skill only the
problem framing and the reference list (with abstracts), ask for 3–5
candidate contributions, and judge how close the best one lands to the
real contribution on a 0–4 closeness ladder plus usefulness. Baselines: no
skill, "be creative", a SciMON-style literature-inspired generator, and
`/cross-pollinate`.

## Why it matters here

A catalogue of moves that feels insightful but does not help a model (or
a person) get from prior art to contribution is folklore. Retrodiction is
the cheapest honest test available before the expensive one (does it help
with the user's own problems).

## Connections

- Memorisation is the threat: the model may know the 2015 paper. Control
  by probing recall from the reference list first and excluding
  recallable cases, or by using post-cutoff papers (whose impact is not
  yet known — a trade-off to decide in the pilot).
- Runs once on the held-out `test/` split (HCE rule); iteration on dev only.
- Reuses `llm-cross-pollination`'s transfer-depth ladder and judge harness.
