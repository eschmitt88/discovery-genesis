---
kind: experiment
slug: "h6-judge-calibration"
date: "2026-09-03"
status: done
hypothesis: "Before H6 can be run, the closeness ladder must be shown to rank a paper's real contribution above plausible alternatives given only its prior art."
result: "The UNSUPERVISED ladder fails: asked which candidate best fits the prior art, the judge prefers a generated proposal to the real contribution (9/19, and 5/23 when the generator is denied hindsight). The SUPERVISED redesign works: shown the real contribution and asked how close each proposal comes, anchors land 4.00/0.04 in 23/23 papers and unaided proposals score 1.80 (best-of-3: 2.43) — H6 is measurable, with a baseline to beat."
related_concepts: ["retrodiction-test", "novelty-mirage", "hindsight-narrative-bias", "adjacent-possible"]
related_literature: ["sinhahajari2026limits", "si2024can", "guo2024ideabench", "yang2024moose"]
tags: ["h6", "evaluation", "calibration", "negative-result"]
---

# h6-judge-calibration

## Hypothesis

H6 plans to score a skill's proposals against a paper's real contribution on a
0–4 closeness ladder. That presupposes the ladder can *tell them apart*. This
experiment tests the ruler before anything is measured with it: hide a paper,
show a judge only its prior art (field, year, reference list), and ask it to
score a slate of candidate contributions, one of which is real.

Pre-stated expectation: the judge should rank the real contribution top well
above chance. If it cannot, the H6 design has to change before a skill is
written.

## Setup

- Config: `config.yaml`
- Code: `genesis/retro.py` (`calibrate` and `hard` stages)
- Data: 24 primary-research works from `data/samples/main50.json`
  (`data/primary-main50.json` verdicts), contributions taken from the coded
  cards in `cases/main50/`, prior-art briefs derived from
  `data/dossiers/main50-compact/` with title and abstract stripped.
- Judge and generator: `claude-sonnet-5`, pinned, run from a neutral cwd.

Three arms, in increasing difficulty:

| arm | the decoys are | purpose |
|---|---|---|
| easy | other papers' real contributions (half same-topic) | is the ladder connected to anything? |
| control | *nothing* — the real contribution is removed | does the judge guess confidently when the answer is absent? |
| hard | contributions **generated** from the same prior-art brief | the condition H6 actually faces |
| hard-era | the same, with the generator forbidden to use hindsight | is the judge's preference for decoys a hindsight artefact? |
| graded | *supervised*: the judge is **shown** the real contribution and grades proposals against it, with a known-answer positive anchor (the contribution itself) and negative anchor (another paper's) | does the redesigned metric work? |

## Result

| | easy (n=23) | hard (n=19) |
|---|---|---|
| judge picked the real contribution | **23/23 (100%)** | **9/19 (47%)** |
| chance | 17% | 17% |
| real score, mean | 3.83 | 2.89 |
| best decoy, mean | 0.74 | **3.47** |
| margin (real − best decoy) | **+3.09** | **−0.58** |
| a decoy outscored the real one | 0% | **53%** |

Control arm: with the real contribution removed, mean score collapses to 0.23
and 20/24 slates are judged "low confidence" — the judge does *not* confabulate
a winner when there isn't one. The judge never claimed to recognise a paper.

Sign test, hard arm, real vs best decoy: 9 up, 10 down of 19 discordant,
p = 1.00.

**Denying the generator hindsight made it worse, not better** (hard-era, n=23):
the judge picked the real contribution 5/23 (22%, indistinguishable from the 17%
chance rate, p = 0.34), the margin widened to −1.48, and a generated decoy
outscored the real contribution in 18/23 (sign test p = 0.011). On the 18 papers
run both ways the margin fell from −0.50 to −1.22. Period-appropriate decoys are
*stronger* competitors, not weaker — which rules out the hindsight explanation.

**The supervised redesign works** (graded, n=23 papers, 4 proposals each):

| | mean score | detail |
|---|---|---|
| positive anchor (the real contribution) | **4.00** | 4 in 23/23 |
| negative anchor (another paper's contribution) | **0.04** | 0 in 22/23 |
| unaided generated proposals | **1.80** | 0:2 1:22 2:33 3:12 (n=69) |
| best of 3 generated, per paper | **2.43** | reached ≥3 on 10/23 papers |

Anchors correct in 23/23. Numbers in `metrics.json`; trials in `results/*.json`.

## Interpretation

**The unsupervised question is the wrong question, and the fix is cheap.**
Asking "which of these fits the prior art best?" cannot work, because the decoys
are *generated from that very reference list* while the real paper was not
written to fit its own bibliography. Derivability-from-the-references is exactly
what the generator optimises and exactly what the judge scores, so the decoys
win — and win harder when they are era-matched. That is a property of the task
framing, not of the judge.

Shown the real contribution and asked to grade distance from it, the same judge
becomes a usable instrument: it pins the truth at 4.00 and a foreign
contribution at 0.04 in every one of 23 papers, and spreads unaided proposals
across the middle. **H6 is therefore measurable, but only in its supervised
form**, and the number a skill has to beat is now known: an unaided model given
the reference list alone scores 1.80 per proposal and 2.43 on its best of three.
That is a demanding baseline — on 10 of 23 papers an unaided proposal already
reached "same problem, same kind of move".

**The ladder is real but not sharp enough for H6 as designed.** The judge is
far from random — 47% against a 17% chance rate is p = 0.0018, and the control
arm shows it recognises absence. What it cannot do is separate the real
contribution from the *best* thing a competent model invents from the same
references. In more than half of cases the invented contribution scored higher.

This kills the planned H6 metric. "Did the skill's proposal score close to the
real contribution?" is unanswerable when an unaided generator's proposal
already scores *above* the real contribution. Any skill would look successful.

Two readings, and they are not exclusive:

1. **A measurement artefact.** LLM judges are known to over-rate generated text
   ([[literature/papers/sinhahajari2026limits]]'s "novelty mirage"), and the
   generator is a 2026 model proposing for a 2010s literature — some decoys may
   be describing what the field actually did *next*, which hindsight makes look
   better-supported than the paper under test.
2. **A fact about discovery.** The prior art *underdetermines* the
   contribution: many different contributions are about equally well-supported
   by the same reference list. That is [[concepts/adjacent-possible]] measured
   directly, and it sits comfortably with this project's other negative
   results — if the move does not distinguish impact (`results/h3-replication.md`)
   and the ingredients are the same cited prior art for cases and twins, then
   "what the prior art set up" is a wide set, not a point.

Reading 2 is the more interesting claim and it is *not* established here;
distinguishing the two requires the hindsight control below.

## Diagnostics

- intended_effect_confirmed: partial — the unsupervised ladder fails (`metrics.json:hard_slate.margin` −0.58; `metrics.json:hard_era_slate.margin` −1.48) but the supervised redesign passes its anchor test (`metrics.json:graded_supervised.anchors_correct` 23/23).
- leakage_check: prior-art briefs are built by stripping title and abstract from the compact dossier (`genesis/retro.py:prior_art_brief`); judge asked to self-report recognition — 0/23 claimed any. Held-out splits untouched: this ran entirely on `main50` dev works.
- overfitting_signal: n/a — no model fit. The control arm is the analogous guard and it passes (`metrics.json:control_slate.mean_score` 0.23).
- delta_from_prior: first evaluation-side experiment; no prior to compare.
- unexpected_findings: the easy arm was at ceiling (23/23, margin +3.09), which is itself informative — a judge separating same-topic papers' contributions that cleanly is matching on reference vocabulary, so the easy arm mostly measured topic overlap, not closeness.
- next_candidates:
  - **Done, and it reversed the expected direction**: the hindsight control (hard-era) made decoys stronger, so reading 1 is out. Reading 3 — proposals generated from a reference list are trivially more derivable from it than the real paper is — now looks like the explanation, and it is a framing artefact rather than a fact about discovery.
  - **Done**: the supervised metric replaces the unsupervised one; `genesis.retro graded` is the H6 harness, with 1.80 / best-of-3 2.43 as the no-skill baseline.
  - Have a **human** (the user) grade one set of graded slates, to check the judge's 0-4 distances against a person's. The anchors make this cheap: 23 papers, each with the real contribution and four proposals.
  - Re-run the graded baseline with the *generator* also given the project's H1 findings (build on recent, highly-cited work) — the cheapest possible test of whether the bibliometric result is actionable, before any SKILL.md is written.

## Follow-up

- `docs/research-plan.md` H6 row rewritten: the anticipated threat was
  memorisation, which did not fire (0/23 recognised); the real threat was the
  unsupervised framing, now replaced.
- The 2.43 best-of-3 baseline is the bar for any `skill/genesis/SKILL.md`. It is
  high enough that a skill which merely restates "look at the references" will
  not clear it.
