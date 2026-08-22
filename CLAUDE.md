# Project: discovery-genesis

Short orientation only. User-level `~/.claude/CLAUDE.md` holds the durable
principles; this file refines them for this project.

## What this project is about

How discoveries are made: sample impactful STEM papers at random
(field-stratified), pair each with a matched median-impact twin, and code
what each did to its prior art — the **move**, the **enabler**, and which
**genesis model** fits (idea-first / means-first / problem-first /
accretion). The idea step is a hypothesis, not the frame. End product: a
Claude Code skill for going from prior art to a contribution, evaluated by
retrodiction on held-out cases.
Plan + hypotheses: `docs/research-plan.md`. Scope: `docs/decisions/0001-*`.

## Layout (see user CLAUDE.md for the full rationale)

- `raw/` — immutable source material. Read only.
- `literature/` — processed notes on papers, repos, posts.
- `concepts/` — atomic ideas. Promote to `mocs/` when ≥5 cluster.
- `experiments/YYYY-MM-DD-<slug>/` — self-contained runs.
- `docs/decisions/` — lightweight ADRs.
- `journal/` — daily session files (hook-written).
- `_meta/` — index, log, templates.

## Scoped rules

Detailed conventions live in `.claude/rules/` and are auto-loaded when you
touch matching paths:

@.claude/rules/experiments.md
@.claude/rules/notebooks.md
@.claude/rules/data.md

Framework rules load here (per-project, not globally — they only cost
context where they can apply):

@~/claude-system/claude/rules/evaluation.md
@~/claude-system/claude/rules/agency.md

## Budget & compute

Autonomous runs read `budget.yaml` at this project's root for hard
ceilings (wall time, tokens, disk) and model roles (ideator vs
implementer). Before proposing anything with non-trivial resource
demands — multi-hour training, large downloads, many seeds — read
`budget.yaml` and make sure the ask fits under the remaining headroom.
If it doesn't fit, say so in the proposal's `risks:` and either scope
down or explicitly flag the need to raise a ceiling.

@budget.yaml

## Project-specific facts

- Primary language: Python (`genesis/` package: sample → fetch → features →
  bundle); cards and codebook as Markdown.
- Sampling frame + RNG: the `xpol` sampler in
  `~/projects/research/llm-cross-pollination` (invoked via
  `uv run --project`, never re-implemented here). Seeds are logged.
- Data: OpenAlex (polite pool, mailto set), Semantic Scholar citation
  intents, OA full text. Raw API responses and PDFs go to
  `raw/cases/<W-id>/` (DVC); derived genesis cards go to `cases/` (git).
- LLM coders run as Sonnet subagents; `claude -p` on the subscription with
  `--model` pinned in any unattended job. Never a raw API key.
- Evaluation: HCE applies once `cases/` has a `test/` split; the
  retrodiction test runs on it once.
- Environment: managed by `uv`; run `make env` to sync.
- Data: tracked by DVC. Large artifacts on SN850X via `~/projects/`.

## Housekeeping

- End sessions with `/wrap`. The SessionEnd hook backstops this.
- Use `/new-experiment <slug>` — don't hand-roll experiment folders.
- Run `/lint` weekly.
