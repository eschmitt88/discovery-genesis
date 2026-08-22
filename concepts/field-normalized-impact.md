---
kind: concept
name: "field-normalized impact"
status: seedling
added: "2026-08-22"
sources: []
related_concepts: ["matched-control-twin", "novelty-vs-impact"]
related_experiments: []
tags: ["metric", "sampling"]
---

# Field-normalized impact

## Definition

OpenAlex's `citation_normalized_percentile`: a work's citation count ranked
against works of the same type, year and primary topic. Sampling on it
means "top 1 % in its own subfield", so a 2014 mycology paper and a 2014
deep-learning paper compete on equal terms.

## Why it matters here

Raw citation counts would make the impact sample mostly biomedicine and
computer science. Normalising lets the `xpol` sampler's field-stratified
topic draw do its job — the sample spans STEM — and makes the twin design
well-defined (same topic-year, different percentile band).

## Connections

- Threshold ≥ 0.99 for cases, 0.40–0.60 for twins, years 2010–2019 so
  impact has accrued and OA text exists.
- Topic assignment is itself a model output; a case whose primary topic
  looks wrong is flagged, not silently kept.
