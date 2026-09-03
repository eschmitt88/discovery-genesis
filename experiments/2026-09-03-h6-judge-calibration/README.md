---
kind: experiment
slug: "h6-judge-calibration"
date: "2026-09-03"
status: done
hypothesis: "Before H6 can be run, the closeness ladder must be shown to rank a paper's real contribution above plausible alternatives given only its prior art."
result: "The ladder works against other papers' contributions (23/23) but FAILS against contributions generated from the same prior art: the judge picks the real one 9/19 and a generated decoy outscores it 53% of the time. Absolute closeness scores cannot serve as H6's metric."
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

| arm | the five decoys are | purpose |
|---|---|---|
| easy | other papers' real contributions (half same-topic) | is the ladder connected to anything? |
| control | *nothing* — the real contribution is removed | does the judge guess confidently when the answer is absent? |
| hard | contributions **generated** from the same prior-art brief | the condition H6 actually faces |

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
p = 1.00. Numbers in `metrics.json`; trials in `results/*.json`.

## Interpretation

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

- intended_effect_confirmed: no — the ladder discriminates on the easy slate (`metrics.json:easy_slate.picked_rate` 1.00) but not on the hard slate (`metrics.json:hard_slate.margin` −0.58).
- leakage_check: prior-art briefs are built by stripping title and abstract from the compact dossier (`genesis/retro.py:prior_art_brief`); judge asked to self-report recognition — 0/23 claimed any. Held-out splits untouched: this ran entirely on `main50` dev works.
- overfitting_signal: n/a — no model fit. The control arm is the analogous guard and it passes (`metrics.json:control_slate.mean_score` 0.23).
- delta_from_prior: first evaluation-side experiment; no prior to compare.
- unexpected_findings: the easy arm was at ceiling (23/23, margin +3.09), which is itself informative — a judge separating same-topic papers' contributions that cleanly is matching on reference vocabulary, so the easy arm mostly measured topic overlap, not closeness.
- next_candidates:
  - Run a **hindsight control**: regenerate decoys with a generator restricted to knowledge before the paper's year (or use a pre-cutoff model), and re-judge. If the real contribution wins under that restriction, reading 1 dominates; if it still loses, reading 2 stands.
  - Replace H6's absolute ladder with a **discrimination metric**: can the judge rank the real contribution above a fixed decoy slate, scored as accuracy against chance? That is measurable even when absolute scores saturate, and matches IdeaBench's rank-based Insight Score (`literature/papers/guo2024ideabench.md`).
  - Have a **human** (the user) judge 10 hard slates blind. If a person also cannot pick the real contribution, reading 2 is much stronger and the judge is exonerated.

## Follow-up

- `docs/research-plan.md` H6 row needs rewriting: the memorisation control was
  the anticipated threat, and it did not fire (0/23 recognised); the actual
  threat is decoy strength.
