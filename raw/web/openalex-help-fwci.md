---
source_url: https://help.openalex.org/hc/en-us/articles/24735753007895-Field-Weighted-Citation-Impact-FWCI
fetched: 2026-08-22
title: "Field-Weighted Citation Impact (FWCI)"
kind: documentation
---

# Field-Weighted Citation Impact (FWCI) — OpenAlex help article

Fetched via WebFetch on 2026-08-22 from the URL above (OpenAlex official
documentation, not a paper).

## Definition

Field-Weighted Citation Impact (FWCI) is a normalized citation metric that
accounts for differences in citation patterns across research types,
publication years, and academic subfields.

## Formula

citations received / citations expected

- 1.0 = world average
- 2.0 = twice the expected citation count
- 0.5 = half the expected count

**Citations received (numerator):** citations in the publication year plus
the three following years (a 4-year window).

**Citations expected (denominator):** the average of that same 4-year
received count over every work with the same year, type, and subfield
(articles split journals vs. conference proceedings).

`citation_normalized_percentile` (and the `is_in_top_1_percent` /
`is_in_top_10_percent` flags) express the same underlying rank as a
percentile rather than a ratio-to-average.

## Coverage & exclusions

Approximately 218 million of 322 million works (68%) carry an FWCI value
as of mid-2026. The metric excludes work types not expected to accumulate
citations — e.g. paratext — to avoid distorting institutional averages.

## Notable caveats

OpenAlex's implementation differs from standard databases (e.g. Elsevier's
SciVal) in three ways:

1. Broader comprehensiveness — increases FWCI for cited works relative to
   narrower databases.
2. Single-subfield classification derived from work *content*, not the
   publishing journal.
3. Reliance on first-online publication dates rather than official
   (print) publication dates.
