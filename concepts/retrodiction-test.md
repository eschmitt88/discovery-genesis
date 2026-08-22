---
kind: concept
name: "retrodiction test"
status: seedling
added: "2026-08-22"
sources: ["si2024can", "si2025ideation", "yang2024moose", "sinhahajari2026limits", "wang2023scimon", "li2024chain", "yamada2025aiscientistv2", "guo2024ideabench"]
related_concepts: ["genesis-card", "move-taxonomy", "hindsight-narrative-bias", "novelty-mirage", "ideation-execution-gap"]
related_experiments: []
tags: ["evaluation", "h6"]
---

# Retrodiction test

## Definition

The evaluation of the deliverable: hide the paper, show the skill only the
problem framing and the reference list (with abstracts), ask for 3–5
candidate contributions, and judge how close the best one lands to the
real contribution on a 0–4 closeness ladder plus usefulness. Baselines: no
skill, "be creative", a SciMON-style literature-inspired generator, and
`/cross-pollinate`.

## Why it matters here

A catalogue of moves that feels insightful but does not help a model (or
a person) get from prior art to contribution is folklore. Retrodiction is
the cheapest honest test available before the expensive one (does it help
with the user's own problems).

## Connections

- Memorisation is the threat: the model may know the 2015 paper. Control
  by probing recall from the reference list first and excluding
  recallable cases, or by using post-cutoff papers (whose impact is not
  yet known — a trade-off to decide in the pilot). `[[yang2024moose]]`
  is the strongest citable precedent for the post-cutoff-date route: it
  benchmarks on papers published after its generator LLM's training
  cutoff, so no recall-probing is needed at all.
- Runs once on the held-out `test/` split (HCE rule); iteration on dev only.
- Reuses `llm-cross-pollination`'s transfer-depth ladder and judge harness.
- `[[sinhahajari2026limits]]` is a direct warning about the closeness-ladder
  judge itself: LLM judges rate model-generated research questions as more
  novel than domain experts do (a "novelty mirage"), and the bias gets
  *stronger* under comparative/pairwise judging — so H6 should not assume
  head-to-head judging is safer than standalone scoring, and must keep the
  planned human-calibration subset. See `[[novelty-mirage]]`.
- `[[si2025ideation]]` shows empirically that closeness-to-idea judgments
  (exactly the 0–4 ladder here) do not survive execution: LLM-generated
  ideas score relatively better than human ideas before execution and
  relatively worse after. The ladder score is therefore a proxy for "looks
  like a good contribution," not "would have worked" — worth stating
  explicitly in the skill's own limitations. See `[[ideation-execution-gap]]`.
- `[[guo2024ideabench]]`'s rank-based "Insight Score" (rank the real
  contribution among n generated candidates, read off its position) is a
  candidate alternative or supplement to a fixed 0–4 ladder — it may be
  more robust to judge miscalibration since it is relative, not absolute.
- `[[wang2023scimon]]` and `[[li2024chain]]` are the two required baseline
  generator families (retrieval + iterative novelty-boosting; chain/
  progression extrapolation) H6 must run alongside the genesis-informed
  skill. `[[yamada2025aiscientistv2]]` is a ceiling reference: a full
  idea-through-execution-through-review pipeline that cleared a real peer
  review bar, well beyond what H6's closeness-ladder retrodiction attempts.

## Reusable protocols

What this project should copy from the closest published precedents,
rather than reinvent for H6:

- **Task decomposition (from `[[yang2024moose]]`).** Don't ask for a
  contribution in one shot. MOOSE-Chem factors hypothesis generation as
  h = f(b, i1, ..., ik) — background plus k retrieved inspirations — and
  turns the single hard generation task into three tractable subtasks:
  retrieve inspirations, compose a hypothesis from background +
  inspirations, rank candidate hypotheses. The genesis-card's own
  `ingredients` field is close to "inspirations" already; H6's prompt to
  the skill should make the retrieve/compose/rank split explicit rather
  than asking for "3-5 candidate contributions" as an undifferentiated
  blob.
- **Knowledge-cutoff control (from `[[yang2024moose]]`).** Prefer
  benchmarking on papers published after the generator LLM's training
  cutoff over a recall-probe-and-exclude approach where possible — it is a
  cleaner, harder-to-argue-with contamination control, at the cost of not
  yet knowing those papers' eventual impact (a real trade-off against this
  project's impact-stratified sampling; may require a held-back "recent"
  slice sampled without the impact filter, purely for H6).
- **Scoring ladder vs. rank-based scoring (from `[[guo2024ideabench]]`).**
  IdeaBench's Insight Score presents the real contribution alongside n
  generated candidates to a judge and reads off the real one's rank,
  rather than scoring each independently on a fixed scale. Pilot both: the
  planned 0–4 closeness ladder (absolute, human-interpretable) and a
  rank-based score (relative, may be more judge-robust) on the same dev
  cases, and see whether they disagree in informative ways.
- **Judge-failure-mode audit (from `[[sinhahajari2026limits]]` and
  `[[si2024can]]`).** Before trusting the retrodiction judge: (a) run it in
  both standalone and comparative/pairwise modes and check whether
  comparative mode inflates apparent quality (the RQ-Bench finding); (b)
  check whether the judge favors generated contributions that are narrow
  or source-bound without flagging them as such; (c) do not rely on the
  same LLM self-evaluating its own generations (si2024can's finding that
  LLM self-evaluation of idea quality is unreliable applies directly to a
  judge built from the same model family as the generator).
