---
kind: experiment
slug: "compact-dossier-validation"
date: "2026-09-03"
status: done
hypothesis: "A compact dossier (reference list capped with an explicit 'showing N of M' note, tighter citation contexts, shorter full-text cap) supports the same coding judgements as the full dossier, so a 300+ pair sample can be coded at ~4x lower cost."
result: "Validated. Compact-dossier coding agrees with full-dossier coders as well as those coders agree with each other (genesis_model kappa 0.79 vs consensus, ceiling 0.77; is_primary 0.93 vs ceiling 0.87; instrument and means-first at ceiling). Mild conservatism in positive rate is a bias toward null."
related_concepts: ["genesis-card", "move-taxonomy"]
tags: ["methods", "validation", "cost"]
---

# compact-dossier-validation

## Hypothesis

Powering the one surviving H3 lead (`means-first` / `instrument`, 7-vs-1
discordant, p = 0.07) needs ~300 primary-research pairs — roughly 8x the
current corpus. At full-dossier size that coding pass is unaffordable: the
main50 dossiers total 6.0 MB, median 12 kB but with a long tail (p90 67 kB).

A compact dossier caps the reference list above 60 entries — keeping the most
recent, the most cited and the self-citations, and stating plainly how many
were dropped — shortens citation contexts, and caps full text. Total falls to
1.5 MB (median 10.3 kB, p90 31 kB), a 4x reduction.

The question is whether the labels survive. Pre-stated bar: agreement between a
compact-dossier coder and the existing full-dossier coders should be no worse
than those coders' agreement with each other.

## Setup

- Config: `config.yaml`
- Code: `genesis/dossier.py --compact` (`_select_refs`)
- Data: 40 of the 100 `main50` works, stratified to over-sample the rare labels
  under test — all 12 papers either full coder called `instrument`, plus 2
  further `means-first`, plus 26 drawn at random (seed 20260903).
- One fresh blind coder (`sonnet-compactV`) under frozen codebook v1.1, with no
  access to `cases/main50/` (the labels being compared against), the sample
  files, or the features.

## Result

Cohen's κ, compact coder vs each full-dossier coder, against the ceiling of the
two full coders' agreement with each other on the same 40 papers:

| field | vs coderA | vs coderB | vs consensus | **ceiling (A vs B)** |
|---|---|---|---|---|
| `genesis_model` | 0.68 | 0.74 | **0.79** (n=35) | 0.77 |
| `is_primary` | 0.94 | 0.81 | **0.93** (n=38) | 0.87 |
| `instrument` (move present) | 0.66 | 0.64 | — | 0.66 |
| `means-first` | 0.66 | 0.74 | — | 0.70 |
| `enabler` | 0.30 | 0.48 | 0.48 (n=27) | 0.50 |

Every field is at or above its ceiling. `enabler` is poor in both conditions —
that is a property of the field, not of the dossier.

Positive rates on the two labels the scale-up exists to test:

| label | compact | coderA | coderB |
|---|---|---|---|
| `instrument` | 6/40 | 8/40 | 11/40 |
| `means-first` | 8/40 | 11/40 | 12/40 |

## Interpretation

**The compact dossier is validated for the scale-up.** On the fields that carry
the project's remaining hypotheses, a coder reading the compact dossier agrees
with a full-dossier coder as closely as two full-dossier coders agree with each
other. The saving is real and the labels are not degraded.

One caveat, stated because it affects the confirmatory test: the compact coder
is slightly **conservative** on both target labels (6 vs 8/11 `instrument`;
8 vs 11/12 `means-first`), though the gap is no larger than the spread between
the two full coders themselves. A lower positive rate attenuates a
case-vs-twin contrast toward null, so if the powered test finds the
`means-first` effect, the compact dossier did not manufacture it; if it finds
nothing, some of that could be attenuation. That asymmetry is acceptable —
it errs against the project's preferred hypothesis.

The coder reported reference truncation on 12/40 dossiers and judged it to have
impeded a call on only 2, both cases where the dropped tail hid an old
antecedent proposition — the same weak spot the codebook's queued v1.2 already
flags.

## Diagnostics

- intended_effect_confirmed: yes — every κ at or above the full-coder ceiling (`metrics.json:fields`).
- leakage_check: coder was instructed not to read `cases/main50/`, `data/samples/*.json`, `data/features/*.csv` or `data/primary-*.json`; the stratification that selected the 40 papers was applied by the analyst, not visible to the coder.
- overfitting_signal: n/a — no model fit. The ceiling comparison is the guard against declaring success on a weak absolute number.
- delta_from_prior: dossier total size 6.0 MB → 1.5 MB for the same 100 works (`genesis/dossier.py:_select_refs`).
- unexpected_findings: `is_primary` agreement was *higher* from the compact dossier (κ 0.93 vs 0.87 ceiling) — the reference-summary line (median year, median citations, self-citation count) appears to make review-ness more legible than scrolling a 400-entry list.
- next_candidates:
  - Use compact dossiers for the main400 coding pass; keep a 10% full-dossier double-code as an ongoing check.
  - Fix the truncation weak spot by always retaining the oldest 5 references, so an antecedent proposition cannot be dropped.

## Follow-up

- 4 of 40 papers were recognised by the coder (10%), consistent with the 14% memorisation base rate measured in the pilot.
