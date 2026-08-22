---
kind: paper
title: "Recombinant Uncertainty in Technological Search"
authors: ["Lee Fleming"]
institutions: ["Harvard University (Graduate School of Business)"]
year: 2001
venue: "Management Science 47(1):117-132"
peer_reviewed: true
url: "https://pubsonline.informs.org/doi/10.1287/mnsc.47.1.117.10671"
code_url: null
citations: 2854
source: "raw/papers/fleming2001recombinant.pdf"
added: "2026-08-22"
relevance: 5
credibility: 5
status: read
related_experiments: []
related_concepts: ["novelty-vs-impact", "matched-control-twin", "recombinant-uncertainty"]
tags: ["recombination", "theory", "h4", "h5", "patents"]
---

# Recombinant Uncertainty in Technological Search

## TL;DR

Using patent citation data, shows inventions combining *unfamiliar*
components (or unfamiliar component-combinations) have higher *variance*
in outcome quality than familiar recombinations — more failures, but also
more breakthroughs — because what "belongs together" is a social
convention scientists/inventors have learned, not a fixed constraint on
the underlying knowledge space.

## Claims

- Technological uncertainty is largely a *search* phenomenon: it comes
  from experimenting with unfamiliar components and combinations, not
  from some intrinsic unpredictability of the technology itself.
- Unfamiliar recombination increases the *variance*, not the *mean*, of
  invention quality — most unfamiliar recombinations are worse, a few are
  much better, and the distribution is what matters, not the average.
- "Familiarity" is a property of the inventor/community's prior search
  history, so the same recombination can be familiar to one lab and
  unfamiliar (hence high-variance) to another.

## Methods

- Patent citation networks used to classify each patent's components and
  component-combinations as familiar or unfamiliar to the inventor
  (based on the inventor's own prior patenting history) and to the field.
- Outcome quality measured via forward citations; variance and mean
  compared across familiar vs. unfamiliar recombination patent cohorts.

## Results

- Unfamiliar-component and unfamiliar-combination patents show
  significantly higher variance in forward-citation outcomes than
  familiar recombinations, holding mean impact roughly constant or lower.

## Critique / open questions

- This is the mechanism-level explanation for why H5 should expect
  same-move twins to exist: if recombination raises variance rather than
  mean, then for any given atypical/novel "move" there should be a
  population of papers that made the same move and landed in the low-
  variance tail (the unsuccessful twin), not just the successful case
  the impact-percentile sampling frame surfaces. This is a genuinely new
  angle the atomic concepts didn't yet carry explicitly — see the new
  `[[recombinant-uncertainty]]` seedling.

## Trust signals

- **Credibility:** 5 — Management Science (top-tier, peer-reviewed),
  2,854 citations, foundational status: this is the paper Uzzi, Wang,
  and Shi & Evans's recombination/novelty framings all build on or cite
  as the origin of "novel recombination raises variance" as a testable
  claim rather than a folk intuition.

## Follow-up

- **Relevance:** 5 — the foundational recombinant-search theory paper
  behind the entire novelty/atypicality literature this project draws on
  (Uzzi, Wang, Shi & Evans all build on this framing); directly relevant
  to H4 (contribution as new arrangement of cited ingredients) and gives
  a mechanism for H5's novelty/impact separation: novelty predicts
  variance, not impact, so impact needs a second explanation (problem
  choice, timing, execution, community) beyond the move itself.
