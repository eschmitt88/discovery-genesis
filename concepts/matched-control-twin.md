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
primary topic, the same year and the same document type, with citation
rank within that topic-year pool in the 0.40–0.60 band (the case is in
the top 1 % of the same ranking). Coded with the
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

- Drawn by a seeded RNG over ranks in the topic-year pool, like the case
  (`genesis/sample.py`); the OpenAlex `sample=` + percentile approach was
  dropped after the pilot redraw — see [[field-normalized-impact]].
- One twin per case in the pilot; more if H5's same-move twins are rare.
- The 0.40–0.60 band and the case's top-1 % are fractions of the same
  citation ranking, so the two are defined identically — see
  [[field-normalized-impact]] for why OpenAlex's own percentile was not used.
- Fleming's (2001) recombination-variance finding
  ([[recombinant-uncertainty]]) is the theoretical reason to expect
  same-move, non-impactful twins to be common rather than a rare
  edge case H5 might struggle to find.
