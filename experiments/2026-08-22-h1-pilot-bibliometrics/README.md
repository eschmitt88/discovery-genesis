---
kind: experiment
slug: "h1-pilot-bibliometrics"
date: "2026-08-22"
status: done     # running | done | abandoned
hypothesis: "Impactful papers differ from matched topic-year twins in reference structure: more recent references, a conventional (within-topic) core, more cross-field tail, hotter references (H1)."
result: "H1 partly confirmed on 15 pairs: impactful primary papers cite markedly more RECENT and more HIGHLY-CITED work, with larger multi-institution teams — but they cite LESS across topic/subfield/domain, not more. Five features survive BH-FDR."
related_concepts: ["matched-control-twin", "atypical-combination", "disruption-index", "field-normalized-impact", "novelty-vs-impact"]
related_literature: []
tags: ["h1", "pilot", "bibliometrics"]
# members: only set when kind: ensemble — list parent experiment slugs.
# parent:  only set when this experiment was produced via /propose --expand.
---

# h1-pilot-bibliometrics

## Hypothesis

H1 from `docs/research-plan.md`: on 15 dev pairs (top-1 %-by-rank case vs
rank-0.40–0.60 twin, same OpenAlex primary topic × year × `type:article`,
pool ≥ 500), the case has — relative to its twin —

- **more recent references** (`ref_share_le3` higher, `ref_age_median` lower);
- **a within-topic core** (`ref_cross_topic` not higher; possibly lower);
- **a wider tail** (`ref_n_fields` higher, `ref_cross_field` ≥ twin);
- **hotter references** (`ref_hot_median`, `ref_fwci_median` higher);
- **larger teams** (`n_authors`, `n_institutions` higher — Wu/Wang/Evans);
- disruption (`cd5_nok`) is *not* predicted in a direction: it is being
  measured for the novelty-vs-impact question.

Expectation before running: with n = 15 pairs only the strongest effects
(reference recency, reference hotness, team size) will clear p < 0.05 on a
Wilcoxon signed-rank test; the rest give direction and effect size for the
full-set power calculation. Uzzi-style atypicality is **not** in this run —
it needs the field-year background sample (stage `features --atypicality`,
not yet built).

## Setup

- Config: `config.yaml` (sample seed, bands, pool floor)
- Code: `genesis/sample.py` → `genesis/fetch.py` → `genesis/features.py` → `analyze.py` (this folder)
- Data: pilot A `data/samples/pilot.json` (all article types; 15 dev pairs) and
  pilot B `data/samples/pilotB.json` (primary research only; 15 dev pairs) →
  `raw/cases/<W-id>/` (DVC) → `data/features/pilot{,B}.csv`. The 5 held-out pairs in `test/samples/` are
  fetched by the same mechanical stage but **never** featurised or read here.

## Result

Two runs. **Pilot A** (`results/paired-pilotA-alltypes.md`, all `type:article`)
is a measurement of what the raw top 1 % contains, not a test of H1: its only
strong effect is reference count (117 vs 26, p < 0.001) because ≥ 9 of 15
"impactful articles" are reviews, guidelines or perspectives.

**Pilot B** (`results/paired-pilotB.md`, primary research only, n = 15 pairs)
is the H1 test. Surviving Benjamini-Hochberg FDR across the 15 features:

| feature | case median | twin median | median Δ | pairs | p | BH q | Cliff δ |
|---|---|---|---|---|---|---|---|
| `ref_hot_median` | 309 | 124 | **+162** | 12/14 | 0.002 | 0.025 | +0.68 |
| `ref_share_le3` | 0.35 | 0.20 | **+0.15** | 13/15 | 0.003 | 0.025 | +0.62 |
| `ref_age_mean` | 7.9 | 11.3 | **−4.5 y** | 12/15 | 0.005 | 0.027 | −0.62 |
| `ref_age_median` | 5 | 8 | **−4 y** | 13/15 | 0.011 | 0.040 | −0.60 |
| `ref_cross_domain` | 0.12 | 0.25 | **−0.13** | 11/14 | 0.017 | 0.050 | −0.35 |

Nominally significant but not surviving FDR: `ref_cross_subfield` (−0.11,
p = 0.026), `ref_cross_topic` (−0.14, p = 0.035), `n_institutions` (+3,
p = 0.035), `n_refs` (+8, p = 0.034). `n_authors` +2 (p = 0.051).
Null: `ref_n_fields` (±0), `ref_cross_field` (−0.07, n.s.).
Disruption is unavailable for most pairs (OpenAlex `cites:` throttle) —
on the 7 pairs with citers, `cd5_nok` runs *more negative* for cases
(−0.68 vs 0.00, p = 0.078).

Numbers: `metrics.json`. Full tables: `results/paired-pilotB.md`,
`results/agreement-pilotB.md`.

## Interpretation

**Recency and hotness are the signal; breadth is not.** An impactful primary
paper's reference list is ~4 years younger than its twin's and points at work
that is itself far more cited (median reference: 309 citations vs 124). That is
one coherent picture: these papers are working at the live edge of an active
literature, on problems the field is already converging on.

**The surprise is the sign on breadth.** Every cross-boundary share runs
*lower* for the impactful member — topic (−0.14), subfield (−0.11), domain
(−0.13, the one that survives FDR). The naive "impact comes from crossing
fields" story is not merely unsupported here, it is inverted. This is the
direction Uzzi's conventional-core result predicts, and it agrees with the
open-coding pass, where `transfer` (import from another field) was coded 8
times on twins and 0 times on cases.

Two things this does **not** show. (1) Uzzi's actual claim is a conventional
core *plus an atypical tail*; a mean share cannot see a tail. The atypicality
null model (`features --atypicality`, unbuilt) is what would test it, and it is
now the highest-value missing feature. (2) Reference recency is partly
mechanical: a paper with more citations tends to have been read more, and
fast-moving subfields produce both young reference lists and high citation
counts. A within-subfield-velocity control is needed before calling this causal.

**What it means for the deliverable.** If it holds at n = 150, the skill's
advice is not "import a mechanism from a distant field". It is closer to:
work where the literature is young and hot, stay inside the field's core, and
put the unusual move in a small part of the argument rather than the frame.

## Diagnostics

Fill in after the run. One line per field; leave `n/a` rather than
blank. `next_candidates` must list ≥2 concrete one-sentence proposals.
Every concrete claim below needs a **citation anchor** — a code
reference like `train.py:42-58`, a metrics file path like
`metrics.json:val_acc`, or a wikilink into `literature/`. Unanchored
assertions are flagged by `/lint` (Kosmos, arXiv 2511.02824).

Unless otherwise noted, metric numbers here reference `metrics.json`
(validation split). Cite `final_metrics.json` only if this experiment
is itself the final-scoring pass.

- intended_effect_confirmed: partial — recency and hotness confirmed with FDR-surviving effects (`metrics.json:features.ref_share_le3`, `ref_hot_median`); the predicted *breadth* effect is reversed (`metrics.json:features.ref_cross_domain`, δ −0.35).
- leakage_check: held-out split carved at sampling time (`genesis/sample.py:--holdout`, `splits.yaml`); `test/samples/pilotB-heldout.json` was fetched by the mechanical stage but never featurised or read here — no test/ access during analysis.
- overfitting_signal: n/a — no model is fit; this is a paired comparison. Multiplicity is the analogous risk and is handled by BH-FDR over the 15 features (`analyze.py:106-121`).
- delta_from_prior: vs pilot A (`results/paired-pilotA-alltypes.md`), `n_refs` collapses from +92 (p<0.001, δ+0.75) to +8 (p=0.034, δ+0.39), attributed to the primary-research filter removing reviews (`genesis/sample.py:classify`).
- unexpected_findings: cross-boundary citation shares are *lower* for impactful papers at topic, subfield and domain level — the opposite of the predicted sign, and consistent with the open-coding result that `transfer` was coded only on twins (`results/agreement-pilotB.md`).
- next_candidates:
  - Build the Uzzi atypicality null model (field-year reference-pair background) — a mean cross-field share cannot detect the atypical *tail* that the conventional-core hypothesis actually predicts.
  - Add a subfield-velocity control (median reference age of the whole topic-year pool) to test whether reference recency is a field-tempo artefact rather than a property of the paper.
  - Drip the missing citers (`--citers-only`) and recompute CD5 at n=15; the 7-pair reading (cases more consolidating) is the only disruption evidence so far.

## Follow-up

- ...
