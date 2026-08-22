---
kind: plan
name: research-plan
status: draft
added: "2026-08-22"
updated: "2026-08-22"
---

# Research plan — how discoveries are made

## The question

Take an impactful paper. Behind it is a set of things that already existed —
its references, the state of its subfield, the tools available that year. The
paper did *something* to that prior art. What? And is what it did learnable
as a procedure?

The end product is a `SKILL.md`: a reusable Claude Code skill that, given a
problem and a body of prior art, produces candidate contributions the way
impactful papers actually did — not the way creativity folklore says they
did. Everything below exists to earn the right to write that file.

The closest precedent is TRIZ: Altshuller read ~40 k patents and distilled
the inventive principles that recurred in the good ones ([[triz-lineage]]).
This project does the same for research papers, with three things TRIZ did
not have — random, field-stratified sampling instead of hand-picked
exemplars; matched low-impact controls so we learn what *distinguishes*
impactful work rather than what all work does; and an evaluation of the
resulting procedure instead of a catalogue taken on faith.

## What we are *not* assuming

The naive chain is **prior art → novel idea → impactful paper**. That chain
has an intermediate step that may not exist, may exist only sometimes, or
may be written in after the fact (Medawar's "the scientific paper is a
fraud" — introductions narrate a genesis that did not happen;
[[hindsight-narrative-bias]]). So the intermediate step is a *hypothesis
under test*, not the coding frame. The coding frame admits at least four
[[genesis-models]]:

| model | shape | signature in the record |
|-------|-------|-------------------------|
| **idea-first** | a proposition was stated, then the work tested/built it | the contribution reduces to one sentence the authors could have written before starting; the experiments are designed around it |
| **means-first** | a new instrument / dataset / compute budget / technique was used exploratorily; the "idea" was recognised in the results | the enabling resource is new (cited recently or introduced in the paper); the stated idea post-dates the method section's logic; Dunbar/Hacking/Galison |
| **problem-first** | a recognised open problem met a newly available ingredient; the "idea" was close to forced | the problem is old and widely cited; the ingredient is ≤3 years old; independent near-simultaneous discovery (Merton's multiples) — the move was in the [[adjacent-possible]] |
| **accretion** | no single locatable idea; impact from consolidation, timing, execution, or being the citable reference for what everyone needed | databases, benchmarks, reviews, standards, "the definitive version" of a known method |

Two further things are kept separate throughout: **novelty** (did the paper
do something atypical?) and **impact** (did the field use it?). They
correlate weakly and we want both axes on every case
([[novelty-vs-impact]]).

## Hypotheses

| id | hypothesis | how we would know |
|----|-----------|-------------------|
| H0 | The idea-first model is a minority genesis model for impactful STEM papers; means-first and problem-first together account for more than half. | Blind coding of genesis model on the pilot set; distribution with CIs; test against the authors' own framing (which we expect to over-report idea-first). |
| H1 | Impactful papers differ from matched controls in reference structure — conventional core plus an atypical tail (Uzzi et al. 2013), more cross-topic references, and more *recent* references among the load-bearing ones. | Computed directly from OpenAlex for every case and its twin ([[matched-control-twin]]); paired comparison. Cheap — runs before any reading. |
| H2 | A small finite taxonomy of "moves" (≤ ~15) covers > 80 % of impactful cases, and the taxonomy is stable across STEM fields. | Open-code the pilot; freeze a codebook ([[move-taxonomy]]); closed-code the full set; coverage and per-field distribution; inter-annotator agreement (two LLM coders + human spot checks). |
| H3 | Move frequency differs between impactful papers and their twins. Some moves are impact-enriched (method transfer, instrument, resource creation, simplification), some are impact-neutral or depleted (parameter variation, gap-filling). | Paired move coding; odds ratios per move with CIs. This is the finding the skill is built on. |
| H4 | The load-bearing ingredients of an impactful paper are almost always *in* its references — the contribution is a new *arrangement* of cited prior art, not a de-novo ingredient. | For each case, list the ≤5 ingredients the contribution depends on and whether each is a cited work, an uncited-but-existing work, or new in this paper. Fraction of "all ingredients cited". |
| H5 | Novelty and impact separate: for most impactful papers there exists a twin that made the *same move* and was not impactful. The difference is attributable to problem choice, timing, execution, or community — not to the move. | Among twin pairs sharing a move, code the residual difference. If the move alone explains impact, the skill is a move catalogue; if not, it also needs a problem-selection and timing component. |
| H6 | A skill compiled from H2–H5, given only a paper's prior art (references + subfield state, paper hidden), generates proposals that an LLM judge + human rate as closer to the actual contribution than a no-skill baseline and than the idea generators in the literature (Si et al., SciMON-style). | The [[retrodiction-test]] on the held-out case split. Memorisation control: the model is first probed for whether it can name the paper from its references; any recallable case is excluded or replaced by a post-cutoff paper. |

H0, H2, H4 are about *how* discoveries happen; H1, H3, H5 about what
separates impactful from ordinary; H6 about whether any of it is
operational.

## The unit of analysis: the genesis card

Every sampled paper gets a [[genesis-card]] — one Markdown file with flat
frontmatter under `cases/`, written from the paper text, its reference
list, and its bibliometric neighbourhood. Fields (v0, expected to change
after the pilot):

- `problem` — what was open, in one sentence, and how old it was.
- `ingredients` — the ≤5 prior-art components the contribution depends on;
  each tagged cited / uncited-existing / new-here, with year.
- `move` — from the codebook; free text in the pilot.
- `enabler` — what made it possible *now*: new data / tool / compute /
  theory / collaboration / problem imported from outside / nothing
  identifiable.
- `genesis_model` — idea-first / means-first / problem-first / accretion,
  with confidence and the evidence used.
- `authors_story` — the genesis the introduction narrates, kept separate
  from ours.
- `external_story` — interviews, talks, award lectures, if found (rare;
  strong hindsight bias).
- `novelty` — atypicality proxy, cross-topic reference share, CD index.
- `impact` — field-normalised citation percentile, disruption index.
- `twin` — the matched control's id and the one-paragraph contrast.

## Sampling

- **Frame.** OpenAlex topics, via the `xpol` sampler from
  `llm-cross-pollination` (stratified across domains, OS-entropy seed logged
  in `config.yaml`). Restricted to the three STEM domains (Physical, Life,
  Health Sciences); Social Sciences excluded for now.
- **Impactful case.** Within the drawn topic: `type:article`, year in
  2010–2019 (long enough for impact to accrue, recent enough for OA full
  text), ranked by citations within the topic-year pool (pool ≥ 500
  articles, ≥ 5 references, not retracted), one drawn uniformly from the
  top 1 % of ranks. OpenAlex's own `citation_normalized_percentile` was
  dropped after the first draw — its tail is unreliable in small
  topic-years ([[field-normalized-impact]]).
- **Primary research only (since pilot B).** Pilot A showed the raw top
  1 % is ≥ half reviews, guidelines and perspectives. The sampler
  classifies every work in the band (title / abstract / venue regex +
  OpenAlex type), excludes review-type works from both cases and twins,
  and logs each exclusion and the per-pool review share — which is itself
  the first measured fact about "impact": consolidation dominates raw
  citation impact. Reviews are not studied further in this project; they
  are accretion by construction.
- **Twin.** Same pool, rank in the 0.40–0.60 band, same filter, drawn the
  same way. One twin per case in the pilot; two or three later if H5
  needs them.
- **Sizes.** Pilot 20 pairs; full 150–300 pairs depending on what the pilot
  says about coding cost and agreement.
- **Split.** The held-out `test/` split is drawn at sampling time and never
  read during codebook or skill development (HCE rule applies once
  `cases/` exists). `evaluation_mode: hce` goes into `CLAUDE.md` then.

## Data sources

| source | gives us | notes |
|--------|----------|-------|
| OpenAlex API | works, references, citers, topics, `citation_normalized_percentile`, OA URLs | free, polite pool with mailto; the backbone |
| Semantic Scholar API | citation *intents* (method / background / result) and citation contexts | tells us which references are load-bearing without reading every citer |
| arXiv / Unpaywall / publisher OA | full text | ~half of 2010s STEM has an OA copy; non-OA cases are coded from abstract + references + citing contexts and flagged `text: abstract-only` |
| retrospectives, award talks, interviews | the authors' own account | opportunistic; never the primary evidence |

Raw API responses and PDFs land in `raw/cases/<W-id>/` (DVC-tracked,
immutable); derived cards in `cases/` (git).

## Bibliometric features (computed before any reading)

- Reference-age distribution; share of references ≤ 3 years old.
- Cross-topic share: fraction of references whose primary topic / field
  differs from the paper's.
- Atypicality proxy ([[atypical-combination]]): for each pair of referenced
  topics, how often that pair co-occurs in reference lists of the same
  year's papers in the field vs expectation; report the 10th percentile
  (conventionality) and the minimum (atypical tail), as in Uzzi et al.
- Disruption ([[disruption-index]], CD₅): among the paper's citers, the
  share that cite it *without* citing its references. Computable from
  OpenAlex citers' reference lists.
- Team size, number of institutions, number of distinct fields among
  authors' other works.

## Coding protocol

1. **Open coding (pilot, 20 pairs).** Two independent LLM coders (Sonnet
   subagents, different prompts) write free-text genesis cards. The main
   agent and the user read a subset. Produce codebook v1: move list, enabler
   list, genesis-model decision rules with examples.
2. **Agreement check.** Re-code 10 of the 20 with codebook v1, two coders
   blind to each other; Cohen's κ per field. Revise until κ ≥ 0.6 on
   `move` and `genesis_model`.
3. **Closed coding (full set).** Codebook frozen. Every card records which
   evidence it used (full text / abstract-only / citing contexts /
   external story).
4. **Human spot check.** 10 % of cards, stratified by field, reviewed by the
   user; disagreements logged, not silently fixed.

## Evaluation of the deliverable (H6)

The retrodiction test: hide the paper; show the skill the problem statement
(from the twin's framing of the subfield, or a neutral summary of the
topic that year) and the reference list with abstracts; ask for 3–5
candidate contributions; a judge rates each against the real contribution
on a 0–4 closeness ladder plus a usefulness score. Baselines: no skill;
"be creative"; a SciMON-style literature-inspired generator; the
`/cross-pollinate` skill (which is *one* move — method transfer — so this
doubles as that project's base-rate check). Memorisation is controlled as
in H6. Human rating on a subset calibrates the judge.

## Phases

0. **Framing (now).** This plan, ADR 0001, concept seedlings, three
   literature triages: science-of-science (novelty/impact/disruption
   metrics and findings); theories of discovery (TRIZ, Boden, Simonton,
   Dunbar, literature-based discovery); LLM idea generation and its
   evaluation.
1. **Pipeline.** `genesis` package: `sample` (xpol → OpenAlex pairs),
   `fetch` (records, references, citers, OA text, S2 intents), `features`
   (the bibliometric block), `bundle` (a `raw/cases/<id>/` folder per
   paper). Run it on the pilot sample. Compute H1 on the pilot as the first
   `/new-experiment` — cheap and decisive about whether the twin design
   has signal.
2. **Pilot coding.** 20 pairs, open coding, codebook v1, κ. First look at
   H0, H2, H4. Decide full-set size and whether abstract-only cases are
   codable.
3. **Full set.** 150–300 pairs, closed coding. H1–H5 with statistics.
   Promote the moves to a MoC; each move gets a concept file with its
   worked examples from `cases/`.
4. **Skill v0 and retrodiction.** Compile `skill/genesis/SKILL.md` from
   the H3/H5 findings; run H6 on the held-out split once; iterate on the
   dev split only.
5. **Package.** Propose the skill to `claude-system` via `/elevate`.

## Relationship to `llm-cross-pollination`

- Uses its `xpol` sampler for topic selection (already built and tested;
  H1 there is done). No need to wait for that project's remaining phases.
- That project's core move — import a mechanism from a foreign field — is
  one row of this project's move taxonomy. H3 here measures its base rate
  and impact enrichment among real papers, which is the premise check that
  project cannot run on itself.
- Its transfer-depth ladder and judge harness are reused for H6.

## Findings so far

- **2026-08-22, pilot A (15 pairs, no review filter).** The only strong
  case/twin difference is reference count (117 vs 26, 14/15 pairs,
  p < 0.001) because ≥ 9/15 top-1 % "articles" are reviews, guidelines or
  perspectives. The pipeline now filters to primary research; the review
  share of top-1 % pools (~30 % by the conservative classifier, ~60 % by
  hand on pilot A) is recorded per draw. `experiments/2026-08-22-h1-pilot-bibliometrics/`.

## Open questions

- Is the paper the right unit? Some discoveries are spread over a
  sequence of papers by one group; the sampled "impactful paper" may be
  the *third* in a chain and the genesis happened two papers earlier.
  Pilot check: for each case, does the group's prior work contain the
  move already? If often, the unit becomes the paper-plus-lineage.
- Citation percentile rewards consolidating papers (databases, reviews).
  Do we want them? They are impactful by definition but may have no
  "genesis" to speak of. Decision: keep them, code them as accretion, and
  report findings with and without them. If they dominate, add
  disruption as a second sampling axis (2×2: impact × disruption).
- Can LLM coders read a 2015 paper without already knowing what it became?
  Hindsight contaminates coding as much as it contaminates introductions.
  Mitigation: code from the paper's text and *prior* references only; the
  card's `evidence` field is audited.
- H4 may fail for a reason the reference list cannot show: Tahamtan &
  Bornmann (2018) interviewed authors of landmark papers and found ideas
  traced more often to practical problems and colleague conversations
  than to cited literature. If so, "ingredients" must admit an
  *uncited-social* category, and the twin contrast may live outside the
  bibliographic record entirely. The `external_story` field is the only
  window onto this; its hit rate is itself a pilot outcome.
- The CD/disruption index is contested as of 2026 (Holst/Ginis et al. vs
  Park/Leahey/Funk in *Nature*: much of the reported decline may be a
  zero-reference-works and plotting artefact). Decide and document raw
  vs corrected CD before H1 runs; treat it as a card feature, never a
  selection criterion.
- Is 2010–2019 long enough? Sleeping beauties (Ke et al.) and the 10+
  year convergence of disruption signal (Lin/Evans/Wu) say some
  "twins" are late bloomers. Mitigation: record the percentile's
  snapshot date; re-pull impact at the end of the project and report how
  many twins moved.
- The skill might end up mostly about *problem selection and timing* (H5)
  rather than idea generation. That would be a real finding, and a
  different skill.
