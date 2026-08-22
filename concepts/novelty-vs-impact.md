---
kind: concept
name: "novelty vs impact"
status: seedling
added: "2026-08-22"
sources: ["uzzi2013atypical", "wang2017bias", "fleming2001recombinant", "si2025ideation"]
related_concepts: ["atypical-combination", "disruption-index", "field-normalized-impact", "matched-control-twin", "recombinant-uncertainty"]
related_experiments: []
tags: ["core", "h5"]
---

# Novelty vs impact

## Definition

Two axes kept separate on every card. **Novelty**: did the paper do
something atypical relative to its field that year (reference-pair
atypicality, cross-topic share, disruption)? **Impact**: did the field use
it (field-normalised citations)? They correlate only weakly in the
science-of-science literature; highly novel work is higher-variance, not
higher-mean.

## Why it matters here

The user is interested in both, and they may be produced by different
processes. A skill for novelty (make an atypical move) and a skill for
impact (choose the problem the field is about to need) could be different
skills. H5 is the test: if same-move twins are common, impact is not
explained by the move.

## Connections

- Sampling is on impact; novelty is measured, not selected, so the
  impact-sample's novelty distribution is itself a finding. If
  consolidating (low-novelty, high-impact) papers dominate, a 2×2
  impact × disruption sampling design replaces the 1-D one.
- Fleming (2001) supplies the mechanism for "higher-variance, not
  higher-mean": unfamiliar recombination widens the outcome distribution
  rather than shifting its center, which is why same-move twins should
  exist rather than being a design artifact — see
  [[recombinant-uncertainty]].
- Wang, Veugelers & Stephan (2017) show part of the "weak correlation" is
  a citation-window measurement artifact, not just a real behavioral
  effect: novel work is under-cited early and over-represented in the
  top percentile late.
- `[[si2025ideation]]` (the ideation-execution gap) is a related decoupling
  one level down, at idea rather than paper granularity: LLM-generated
  ideas are judged more "novel" than human ideas before anyone executes
  them, but that apparent-novelty advantage does not survive execution —
  the same shape as novelty and impact correlating only weakly here, but
  observed directly in a controlled human study rather than inferred from
  bibliometrics. See `[[ideation-execution-gap]]`.
