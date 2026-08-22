# discovery-genesis

**How discoveries are made: what impactful papers did to their prior art, coded
from random field-stratified samples with matched controls, distilled into a
Claude Code skill.**

📂 **[Browse this repo →](https://eschmitt88.github.io/discovery-genesis/)** —
interactive, always-live view of experiments, concepts, literature, and maps of
content. Served via GitHub Pages from `docs/index.html`; reads the live file
tree, no build step. _(Link is live once the repo is public and Pages is enabled
— `/new-project` does both by default.)_

## What this is

Take an impactful paper. Behind it is a set of things that already existed —
its references, the state of its subfield, the tools available that year.
The paper did *something* to that prior art. What, and is it learnable as a
procedure? This project samples top-1 %-in-their-subfield STEM papers at
random across fields (OpenAlex, via the
[`llm-cross-pollination`](https://github.com/eschmitt88/llm-cross-pollination)
sampler), pairs each with a median-impact twin from the same topic and year,
and codes each pair: the **move** made on the prior art, the **enabler**, and
which **genesis model** fits — idea-first, means-first, problem-first, or
accretion. The "novel idea" step is a hypothesis under test, not an
assumption. Success is a `SKILL.md` that, shown only a paper's prior art,
proposes contributions closer to the real one than a no-skill baseline.
Plan and hypotheses: `docs/research-plan.md`.

## How it's organized

Plain Markdown + flat YAML frontmatter, cross-linked with `[[wikilinks]]`:

- `concepts/` / `mocs/` — atomic ideas; promoted to a map of content when ≥5 cluster.
- `literature/` — processed notes on papers, repos, posts (0–5 relevance scored).
- `experiments/YYYY-MM-DD-<slug>/` — self-contained runs (hypothesis → result, config, metrics, log).
- `raw/` — immutable source captures · `docs/decisions/` — ADRs · `_meta/` — index, log, templates.

## Local use

```sh
make env    # uv sync
make lint   # knowledge-graph / experiment health check
```

Built on the [claude-system](https://github.com/eschmitt88/claude-system)
research framework (upstream attribution — this project is its own repo).
See `CLAUDE.md` for the agent-facing orientation and `~/.claude/CLAUDE.md`
for the framework's durable principles.
