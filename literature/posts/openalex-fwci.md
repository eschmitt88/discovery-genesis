---
kind: post
title: "Field-Weighted Citation Impact (FWCI) — OpenAlex documentation"
author: "OpenAlex"
url: "https://help.openalex.org/hc/en-us/articles/24735753007895-Field-Weighted-Citation-Impact-FWCI"
source: "raw/web/openalex-help-fwci.md"
added: "2026-08-22"
relevance: 5
related_experiments: ["2026-08-22-h1-pilot-bibliometrics"]
related_concepts: ["field-normalized-impact", "matched-control-twin"]
tags: ["methodology", "sampling", "openalex", "documentation"]
---

# Field-Weighted Citation Impact (FWCI) — OpenAlex documentation

## TL;DR

Official OpenAlex methodology page for FWCI and
`citation_normalized_percentile` — the exact field the project's
sampling frame conditions on to draw impactful cases (≥0.99) and matched
twins (0.40-0.60).

## Key points

- FWCI = citations received / citations expected. Received = citations in
  the publication year plus the 3 following years (a 4-year window).
  Expected = the average of that same 4-year count over every work
  matched on type, publication year, and OpenAlex *subfield*.
  `citation_normalized_percentile` expresses the same rank as a
  percentile rather than a ratio (with `is_in_top_1_percent` /
  `is_in_top_10_percent` convenience flags).
- ~68% of OpenAlex works (218M of 322M as of mid-2026) carry an FWCI
  value; work types not expected to accrue citations (e.g. paratext) are
  excluded from the calculation entirely, which matters for anyone
  computing background rates from "all works."
- OpenAlex's implementation differs from narrower databases (e.g.
  Elsevier SciVal) in three ways worth knowing before trusting a raw
  percentile: broader source comprehensiveness (which *raises* FWCI for
  cited works relative to narrower databases), single-subfield
  classification derived from a work's *content* rather than its
  publishing journal, and use of first-online (not official print)
  publication dates.

## Follow-up

- **Relevance:** 5 — this is the literal field
  (`citation_normalized_percentile >= 0.99` / `0.40-0.60`) the plan's
  sampling frame conditions on for both the impactful case and its
  matched twin; needed to know precisely what is being conditioned on
  (a 4-year citation window, content-based single-subfield assignment)
  before treating the percentile as a clean, artifact-free selection
  variable — the 4-year window is short enough that this project's own
  sleeping-beauty concern (Ke et al., flagged in `docs/research-plan.md`
  open questions) applies directly to the sampling frame itself, not
  just to any post-hoc disruption measurement.
- The single-subfield-from-content detail sharpens `[[field-normalized-
  impact]]`'s existing note that "topic assignment is itself a model
  output" — it is specifically a *content-based* classification, not
  journal-based, which changes what a "cross-topic reference" means
  relative to a journal-based novelty measure like Wang et al.'s.
