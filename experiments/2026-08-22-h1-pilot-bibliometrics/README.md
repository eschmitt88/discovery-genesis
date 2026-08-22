---
kind: experiment
slug: "h1-pilot-bibliometrics"
date: "2026-08-22"
status: running     # running | done | abandoned
hypothesis: "Impactful papers differ from matched topic-year twins in reference structure: more recent references, a conventional (within-topic) core, more cross-field tail, hotter references (H1)."
result: ""
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
- Data: `data/samples/pilot.json` (15 dev pairs) → `raw/cases/<W-id>/` (DVC) →
  `data/features/pilot.csv`. The 5 held-out pairs in `test/samples/` are
  fetched by the same mechanical stage but **never** featurised or read here.

## Result

Fill in after the run. Point at `metrics.json` (validation split — this
is the search signal and the file every other skill reads). A separate
`final_metrics.json` holds held-out test-split numbers and is written
only by the `dvc repro final_eval` pass at chain end. See
`~/claude-system/claude/rules/evaluation.md`.

## Interpretation

What did you actually learn? What surprised you?

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

- intended_effect_confirmed: <yes | no | partial> — <one-line evidence with anchor>
- leakage_check: <method used> — <finding>
- overfitting_signal: train=<x> val=<y> gap=<z> — <interpretation> (from metrics.json)
- delta_from_prior: vs <related_prior_slug>, <metric_delta> attributed to <cause> (metrics.json)
- unexpected_findings: <one or two sentences, or "none">
- next_candidates:
  - <one-sentence proposal 1>
  - <one-sentence proposal 2>

## Follow-up

- ...
