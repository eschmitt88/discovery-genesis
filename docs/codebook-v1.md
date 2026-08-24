---
kind: codebook
name: codebook
version: v1.1
status: frozen   # v1.1 — κ 0.73 on genesis_model over 30 papers, 2026-08-23
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

## Blinding rule for batches (added 2026-08-23)

A coder's batch must never contain both members of a pair: dossiers pair up
by topic + year, and recognising one member reveals the other's role.
Shuffle pairs across coders and batches.

## v1.1 — applied 2026-08-23 (from the second blind batch, 16 papers); FROZEN after the 30-paper re-code

The rules below **are in force**; the numbered issues they answer follow.

- **Means-first requires a capability new to the authors or the field.**
  Serial reuse of the authors' own established platform on a new target
  (next gene, next cancer type, next lattice geometry, next species) is
  **problem-first**. Tell: the same method cited 4–8 times in the authors'
  own prior work → problem-first. Tell for means-first: the capability is
  introduced in this paper, or first cited ≤ 2 years before it, or the
  authors' own prior work does not use it.
- **`problem_age_broad` is dropped.** Keep `problem_age_specific`.
- **`abstract-only` caps `genesis_confidence` at `low`** whenever the
  decision is means-first vs idea-first.
- **`gap-filling` is split.** It was the primary move on 12/30 papers and is
  too coarse for H3/H5. Use exactly one of:
  `gap-filling:next-target` (established method, new target/population/
  species/material — includes animal→human translation),
  `gap-filling:bigger-n` (same question, larger or longer sample — a
  trial, a cohort, a survey wave),
  `gap-filling:first-measurement` (a quantity or effect measured for the
  first time in this system),
  `gap-filling:other`.
- **Second labels only if removing them would make the card false.** The
  "default second label" habit (`recombination`, `consolidation`) is what
  drove move Jaccard from 0.70 to 0.43.
- **Framework papers with no data**: `is_primary: partial — framework`;
  `idea-first` if the stated structure organises the design.
- **Reviews with an embedded unsignposted dataset**: follow the abstract's
  framing; note the dataset in `contribution`.

1. **Problem-first became a catch-all under the decision order** (κ on
   `genesis_model` fell 0.71 → 0.52; every disagreement is problem-first ↔
   means-first). Both coders named the same unresolved case: *a mature
   assay/platform applied to the next target* — next gene, next cancer type,
   next lattice geometry, next species. Proposed rule: **means-first requires
   a capability new to the authors or the field**; serial reuse of one's own
   established platform on a new target is **problem-first**, and the
   dossier signature (the same method cited 4–8 times in the authors' own
   prior work) is named explicitly as the tell. A worked example each way.
2. **Drop `problem_age_broad`** (κ 0.08 on v1). Keep `problem_age_specific`
   (κ 0.49 → reliable enough).
3. **`abstract-only` also caps `genesis_confidence` at `low`** when the
   means/idea distinction is what is at stake — the rule currently names only
   `title+refs-only` and `tldr-only`.
4. **Evidence labels**: "(via semanticscholar/europepmc/crossref)" marks the
   authors' real abstract from another index and is `abstract-only`; only
   "machine-generated summary" is `tldr-only`. (Prompt already updated.)
5. **Cross-species translation** (animal → human) is neither `transfer`
   (same primary field) nor obviously `recombination`. Add a worked example
   under recombination, or a sub-tag `translation`, so biomedicine's most
   common move is not coded inconsistently.
6. **Framework-proposing papers with no data** (a stated model, e.g. COM-B):
   `is_primary: partial — framework` and `genesis_model: idea-first` when the
   proposition organises the design; distinguish from essay/perspective
   (`no`) by whether a testable or applicable structure is delivered.
7. **Reviews with an embedded unsignposted dataset**: default to the paper's
   own abstract-level framing; note the dataset in `contribution`.
8. **Label preference drift**: coder B used `recombination` 11×, coder A
   `consolidation` 8×, on the same 16 papers (move Jaccard 0.70 → 0.43).
   Both are being used as the "default second label". Rule: a second label
   is listed only if removing it would make the card false.

## Dossier support for the means-first rule (added 2026-08-24)

Three coders independently reported that the v1.1 means-first test — *is
the capability new to the authors?* — was the rule they most often had to
guess at, because the dossier's reference list did not say which references
the authors wrote themselves. `genesis.dossier` now marks every reference
sharing an author with the focal paper (**SELF**) and prints the count in
the section heading. Validated against a coder's manual count: 15 of 92 on
the Krische reductive-coupling paper, where the coder had estimated
"~15–20 self-citations on the same strategy".

Use it directly: **≥ 4 self-citations of the same method/platform →
problem-first** (serial reuse); **0–1, or the capability first cited ≤ 2
years before the paper → means-first**. Cards coded before this change
(pilot B, main50) inferred self-citation from author names in titles and
should be treated as noisier on this axis.


## v1.2 — queued (from the H0 order-sensitivity audit, 2026-08-24)

The cascade suppresses one real pattern: a comprehensive modern study
organised around **someone else's** long-standing published proposition
(trisomy-21 interferon-receptor dosage, proposed 1974–78, tested
comprehensively in 2016). The cascade stops at problem-first — old question,
existing tools — and never weighs the antecedent claim.

Fix: ask of every paper, independently of the cascade, and record as its own
field:

    antecedent_proposition: <none | authors' own prior claim | third-party claim>
    antecedent_year: <year the proposition was first stated, or null>
    antecedent_evidence: "<the cited work stating it>"

This keeps the cascade's reliability (κ 0.73) while making the suppressed
pattern visible and countable instead of silently folded into problem-first.
