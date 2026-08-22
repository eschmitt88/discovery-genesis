---
kind: concept
name: "matched control twin"
status: seedling
added: "2026-08-22"
sources: ["openalex-fwci", "fleming2001recombinant"]
related_concepts: ["field-normalized-impact", "novelty-vs-impact", "genesis-card", "recombinant-uncertainty"]
related_experiments: []
tags: ["core", "method", "h1", "h3", "h5"]
---

# Matched control twin

## Definition

For each impactful case, a paper drawn at random from the same OpenAlex
primary topic, the same year and the same document type, with
field-normalised citation percentile in the 0.40–0.60 band. Coded with the
same card schema.

## Why it matters here

Without a twin, reading impactful papers teaches what *all* papers do —
survivorship bias dressed as insight (the failure mode of most
"habits of great scientists" writing, and arguably of TRIZ). Every
comparative claim in the project (H1, H3, H5) is a paired case-vs-twin
difference. H5 specifically hunts for twins that made the *same move*
and did not land, to separate the move from problem choice, timing and
execution.

## Connections

- Drawn with OpenAlex `sample=` and a logged seed, like the case.
- One twin per case in the pilot; more if H5's same-move twins are rare.
- The 0.40–0.60 percentile band is defined by the same
  `citation_normalized_percentile` / FWCI methodology as the case's ≥0.99
  threshold — see [[field-normalized-impact]] for its exact window and
  classification caveats.
- Fleming's (2001) recombination-variance finding
  ([[recombinant-uncertainty]]) is the theoretical reason to expect
  same-move, non-impactful twins to be common rather than a rare
  edge case H5 might struggle to find.
