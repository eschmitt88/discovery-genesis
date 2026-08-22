---
kind: concept
name: "genesis card"
status: seedling
added: "2026-08-22"
sources: ["tahamtan2018creativity"]
related_concepts: ["genesis-models", "move-taxonomy", "matched-control-twin", "novelty-vs-impact"]
related_experiments: []
tags: ["core", "method"]
---

# Genesis card

## Definition

The unit of analysis: one Markdown file per sampled paper under `cases/`,
recording the problem, the ≤5 prior-art ingredients (cited / uncited-existing
/ new-here), the move, the enabler, the genesis model with evidence, the
authors' own story, bibliometric novelty and impact measures, and the
contrast with the paper's twin.

## Why it matters here

Every hypothesis is a statement about the distribution of some card field,
or the paired difference between a card and its twin's card. The card
schema is therefore the project's real instrument; v0 lives in
`docs/research-plan.md` and is expected to change after the pilot's open
coding.

## Connections

- `evidence` field records what the coder saw (full text / abstract-only /
  citing contexts / external story) so hindsight contamination can be
  audited.
- Cards are written by two independent LLM coders in the pilot; agreement
  on `move` and `genesis_model` gates the move to closed coding.
- `[[tahamtan2018creativity]]` is direct interview evidence that the
  `ingredients` field's cited/uncited-existing/new-here scheme can still
  miss the load-bearing influence entirely: landmark scientometrics
  papers' own authors (Hirsch on the h-index, Small on co-citation)
  trace their ideas to a practical problem or a colleague conversation,
  not to any reference, cited or not — the risk the research plan's open
  questions flag for H4. This is the concrete case for treating
  `external_story` as load-bearing, not opportunistic.
