---
kind: codebook
name: codebook
version: v1
status: active
added: "2026-08-22"
supersedes: v0-open (prompts/open-code.md, pilot B open coding)
derived_from: 28 blind codings (14 papers × 2 coders), cases/pilotB/
---

# Genesis card codebook v1

Built from the v0 open-coding pass: 14 pilot-B papers coded independently by
two Sonnet coders (κ = 0.714 on `genesis_model`, 0.70 mean Jaccard on
`move_candidates`, but κ = 0.16 on the free-text `enabler`). Every change
below answers a specific disagreement or a friction point both coders
reported. Changes are marked **[why]**.

## 1. `genesis_model` — four values, with a tiebreaker

Unchanged in definition; κ was already acceptable. What was missing is a rule
for the one place disagreement concentrated: **accretion ↔ problem-first**
(3 of 3 confusions). **[why: coder A read "old gap closed with existing
method on new material" as problem-first; coder B read the same papers as
accretion.]**

Decision order — take the first that applies:

1. **accretion** if the contribution is the *aggregate itself*: a survey wave,
   a trend report, a review, a database, a standard. Test: could the authors
   have written the conclusion's *form* before collecting anything, with only
   the numbers left blank? If yes → accretion.
2. **means-first** if a capability (instrument, screen, assay, dataset,
   compute budget) is the reason the finding exists, and the paper's logic
   runs capability → observation → claim.
3. **problem-first** if the paper names a specific open question, and the
   ingredient that closes it already existed. The ingredient need **not** be
   ≤ 3 years old — a 5-year-old completed trial or an existing biobank counts.
   **[why: both coders hit resource-repurposing cases the v0 "≤3 y" rule
   mis-sorted.]** What matters is that the *question*, not the ingredient, is
   what is new.
4. **idea-first** only if a proposition is stated that could have been written
   *before* the work began and the design follows from it. A gap statement is
   not a proposition. **[why: v0 let "we hypothesised that…" boilerplate
   count.]**

If the dossier is `title+refs-only` or `tldr-only`, cap
`genesis_confidence` at `low` — the means-first/idea-first distinction turns
on the introduction's logic, which is exactly what is missing.
**[why: both coders named this pair as underdetermined without full text.]**

## 2. `move_candidates` — 14 labels, attestation marked

List up to 3, most central first; co-listing is expected.

**Attested in the pilot** (count over 28 codings): gap-filling 12,
recombination 9, transfer 8, consolidation 7, unification 4, instrument 4,
formalisation 4, anomaly 1.

**Unattested so far** — retained, not cut, until n ≈ 50: scale,
simplification, inversion, relaxation, reformulation, resource.
**[why: absence in 14 papers is weak evidence; but if still unattested at
n = 50 they are dead labels and the taxonomy is really ~8 wide, which is
itself an H2 result.]**

Two labels needed sharper boundaries — both were stretched by both coders:

- **unification** — two *previously separate literatures or phenomena* are
  shown to be one mechanism. Not "the paper cites two fields".
- **formalisation** — an informal construct is given a formal/computable
  representation (an ontology, an equation, a metric). Not "the paper is
  mathematical".
- **transfer** vs **recombination** — transfer is import *across a field
  boundary* (the source has a different primary field); recombination is
  joining two things *within* reach of the same field. When the source is
  the same field, it is recombination. **[why: the largest single source of
  Jaccard loss.]**

## 3. `enabler` — closed vocabulary (was free text)

Pick exactly one head term, then one clause of detail. κ = 0.16 on free text
makes this the biggest single fix. **[why: coders wrote the same enabler in
incompatible words — "screen (triple mutant + Tn5)" vs "new tool".]**

`new-instrument` · `new-assay-or-method` · `new-dataset-or-resource`
· `existing-resource-repurposed` · `new-compute-or-scale`
· `new-theory-or-formalism` · `new-collaboration-or-team`
· `imported-problem` · `routine-data-wave` · `none-identifiable`

## 4. `problem_age` — split in two

Replace the single field with:

- `problem_age_broad` — how old is the general question the paper situates
  itself in? `new (<3 y)` / `established (3–15 y)` / `old (>15 y)`
- `problem_age_specific` — how old is the precise question it answers?
  same scale, plus `opened-by-this-paper`

**[why: κ = 0.44; both coders reported papers with an old broad problem and a
recent narrow one, and split their answers differently.]**

## 5. `ingredients.role` — two new values

`method` · `data` · `theory` · `instrument` · `problem` · `result`
· **`framework-or-formalism`** (RDF, a critical-theory frame, a modelling
formalism) · **`prior-finding`** (a specific published result the
contribution builds on, as distinct from a whole theory)

**[why: both coders forced formalisms into `instrument`; theory/humanities
papers depend on frames and specific prior results, which the v0 roles could
not express.]**

## 6. `is_primary` — three values, with genre list

- `yes` — primary research (empirical, theoretical, or methodological).
- `no — <genre>` — review, guideline, consensus statement, editorial, essay,
  commentary, **surveillance/trend report** (MMWR, ESPAD and similar routine
  monitoring bulletins). **[why: coder A had no slot for these and used
  `yes`; coder B used `no`; this was 2 of the 3 `is_primary` disagreements.]**
- `partial — <what>` — dataset/resource papers, tool papers, protocol papers:
  primary work whose contribution is an artefact rather than a finding.

## 7. `problem` when there is no problem

Accretion cases may have no unsatisfactory prior state. Write
`problem: "none stated — <what the paper aggregates>"` rather than
manufacturing a gap. **[why: both coders reported inventing a problem
sentence for the surveillance bulletins.]**

## 8. Fields unchanged

`recognised`, `evidence` (now five tiers), `authors_story`, `contribution`,
`genesis_evidence`. Recognition rate in the pilot was 2/14 papers, and
*both* coders recognised the same two — treat ~14 % as the working
memorisation base rate for randomly drawn 2010s STEM papers
([[concepts/retrodiction-test]] must handle it structurally, not by hoping).
