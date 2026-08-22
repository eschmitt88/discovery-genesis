---
kind: paper
title: "Semantic TRIZ feasibility in technology development, innovation, and production: A systematic review"
authors: ["Mostafa Ghane", "Mei Choo Ang", "Denis Cavallucci", "Rabiah Abdul Kadir", "Kok Weng Ng", "Shahryar Sorooshian"]
institutions: ["Universiti Kebangsaan Malaysia", "INSA de Strasbourg", "University of Nottingham Malaysia", "University of Gothenburg"]
year: 2023
venue: "Heliyon"
peer_reviewed: true
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10788813/"
code_url: null
citations: 35
source: "raw/papers/triz2023review.pdf"
added: "2026-08-22"
relevance: 3
credibility: 4
status: read
related_experiments: []
related_concepts: ["triz-lineage", "move-taxonomy"]
tags: ["h2", "triz", "systematic-review"]
---

# Semantic TRIZ feasibility in technology development, innovation, and production

## TL;DR

A systematic literature review (2009–2022, 45 studies) of "Semantic
TRIZ" — applying text mining/NLP/AI to automate TRIZ's inventive-problem-
solving tools (patent search, SAO-structure extraction, contradiction
identification) — mapping which TRIZ components have been automated,
which data sources and NLP techniques are used, and what remains
unautomated.

**Correction to the candidate triage file**: the candidate description
characterized this paper as arguing TRIZ's effectiveness "rests mainly on
practitioner case studies and surveys prone to self-selection and
post-hoc rationalization, with little theory-grounded validation" — that
critique is **not what this paper is about**. Its actual scope is a
technical/methods review of AI+NLP tooling built on top of classical
TRIZ, not an epistemic audit of TRIZ's evidence base. It is ingested
regardless (it is a genuine, current, peer-reviewed systematic review of
the TRIZ ecosystem and belongs in `triz-lineage`'s source list), but it
does **not** supply the "catalogue taken on faith" critique the research
plan wanted from this slot — that critique remains an open gap in the
project's TRIZ-lineage sourcing.

## Claims

- TRIZ (40 inventive principles, contradiction matrix, laws of technical
  evolution) derives from Altshuller's analysis of ~40,000 patents and
  remains an active target for AI/NLP automation, not a settled/retired
  method.
- 62% of the 45 reviewed studies focus on refining *existing* TRIZ tools
  (contradiction matrix, SAO extraction) rather than building genuinely
  new ones (e.g., TESE, the laws of technical-system evolution, remain
  comparatively under-automated).
- Patent-derived structured data (function/attribute/action extraction,
  SAO triples) is the dominant substrate for Semantic-TRIZ automation;
  academic literature and general text are secondary sources.

## Methods

- Kitchenham-style systematic literature review protocol; search window
  January 2009–March 2022; 45 included studies (A1–A45), each coded for
  TRIZ component addressed, data source, NLP/AI technique, and
  evaluation method.

## Results

- Maps the current state of AI-TRIZ integration onto a component-by-
  component grid (which of TRIZ's tools/philosophy/methods layers have
  received AI attention and which have not) and flags patent
  classification, contradiction detection, and function-based retrieval
  as the most mature automated sub-areas.
- Notes the shift from keyword/syntactic methods toward transformer-based
  NLP (BERT-era) as an emerging but still nascent trend as of the review
  window.

## Critique / open questions

- Does not address (and was never intended to address) whether TRIZ
  actually improves invention outcomes versus a baseline — its unit of
  evaluation is "has this TRIZ component been automated," not "does using
  TRIZ produce better inventions." The evidentiary-quality critique of
  TRIZ that `triz-lineage` needs (hand-picked exemplars, no controls,
  generic-fit-after-the-fact principles) is still unsourced in this
  project's graph.
- Heavy overlap in author affiliations with prior TRIZ-automation
  literature (multiple co-authors return across the reviewed studies),
  a standard feature of a specialist subfield's own systematic reviews,
  worth noting for interpreting the "which papers get reviewed" scope.

## Trust signals

- **Credibility:** 4 — six-author team across four institutions, open-
  access CC-BY in Heliyon (Elsevier, peer-reviewed), 35 citations,
  transparent PRISMA-style methodology with a full 45-study evidence
  table.

## Follow-up

- **Relevance:** 3 — confirms TRIZ's continued technical currency and
  supplies a ready-made, component-by-component map of the TRIZ toolkit
  (useful when cross-checking `move-taxonomy` entries against TRIZ's own
  categories) but does not supply the epistemic critique of TRIZ's
  evidence base that the research plan's Phase-0 triage wanted from this
  slot. A follow-up `/discover` pass specifically targeting "TRIZ
  effectiveness validity critique" (not "TRIZ automation") is still
  needed to fill that gap; noted in the project's open questions rather
  than silently substituted.
