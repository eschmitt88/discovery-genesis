---
kind: decision
id: 2
title: Design decisions forced by the pilot
status: accepted
date: "2026-08-23"
---

# 0002 — Design decisions forced by the pilot

## Context

The 15-pair pilot (`experiments/2026-08-22-h1-pilot-bibliometrics/`) and
the three blind coding passes (v0, v1, v1.1; 30 papers × 2 coders each)
produced four findings that change the method, not just the results.

## Decisions

1. **Primary research only.** The raw top 1 % of `type:article` by
   citations is mostly reviews, guidelines and perspectives (≥ 9/15 in
   pilot A). They are excluded from cases *and* twins by the classifier in
   `genesis.sample`, every exclusion is logged with its reason, and the
   per-pool review share is recorded as a finding. Reviews are accretion by
   construction and are not the object of this project.

2. **Citation rank within the topic-year pool, not OpenAlex's percentile.**
   The percentile's tail is unreliable in small topic-years. Pools under
   500 articles are skipped; cases need ≥ 20 citations.

3. **Codebook v1.1 is frozen** (κ = 0.73 on `genesis_model` over 30
   papers with fresh blind coders). Changes from here are versioned v2 and
   require a re-code of a reliability subset; the main sample is coded
   under v1.1 as is.

4. **Pair-blinding.** A coder's batch never contains both members of a
   pair. Dossiers pair up by topic + year, and the recognition asymmetry
   (7/15 cases vs 0/15 twins recognised) means a coder who recognises one
   member learns the other's role.

5. **Memorisation control for H6 is structural, not statistical.** About
   half of the impactful 2010s papers are recognisable to the coder model.
   Excluding recognised cases would bias the retrodiction test toward the
   less famous half of impact. The retrodiction set will therefore be
   drawn from papers published after the generating model's training
   cutoff (MOOSE-Chem's protocol), accepting that their eventual impact is
   not yet known and must be proxied (early citation velocity, venue) and
   re-checked later.

6. **One OpenAlex consumer at a time.** Concurrent list-heavy processes
   trigger multi-hour 429 cooldowns on all list queries. Pipeline stages
   run sequentially; citers are dripped last.

## Consequences

- The project's "impact" is now *primary-research* impact in the top 1 %
  of a topic-year. Findings do not speak to the impact of reviews.
- The skill's evaluation (H6) runs on post-cutoff papers whose impact is
  provisional; the final H6 number should be re-computed when those papers
  are ≥ 3 years old.
- The main sample (60 pairs drawn, 10 held out) is the first set coded
  entirely under a frozen codebook; pilot-B cards under v0/v1 are kept as
  the codebook's development record and are not pooled with it.
