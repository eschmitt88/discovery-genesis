---
kind: concept
name: "disruption index"
status: seedling
added: "2026-08-22"
sources: []
related_concepts: ["novelty-vs-impact", "field-normalized-impact"]
related_experiments: []
tags: ["metric"]
---

# Disruption index

## Definition

Funk & Owen-Smith's CD index: among papers citing a focal paper, the share
that cite it *without* also citing its references (disrupting) minus the
share that cite both (consolidating), in [-1, 1]. Computable from OpenAlex
by pulling the focal paper's citers and their reference lists.

## Why it matters here

Citation impact alone cannot distinguish a paper that replaced its prior
art from one that summarised it. CD separates them, and is the second axis
if consolidating papers dominate the impact sample. Known problems: it is
sensitive to reference-list length and to database coverage, and the
"science is getting less disruptive" result built on it is contested —
use it as a card feature, not a selection criterion, until the pilot shows
it is stable on this sample. As of 2026 the decline result is under open
dispute in *Nature* (Holst/Ginis et al. Matters Arising vs the Park/Leahey/
Funk reply); the pipeline must document raw vs corrected CD.

## Connections

- Complements [[atypical-combination]]: one measures the inputs, the other
  the downstream effect.
