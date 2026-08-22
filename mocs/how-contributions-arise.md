---
kind: moc
name: "how contributions arise"
status: active
added: "2026-08-22"
concepts: ["[[concepts/genesis-models]]", "[[concepts/adjacent-possible]]", "[[concepts/literature-based-discovery]]", "[[concepts/hindsight-narrative-bias]]", "[[concepts/genesis-card]]", "[[concepts/move-taxonomy]]", "[[concepts/triz-lineage]]"]
tags: ["moc", "genesis", "h0", "h2", "h4"]
---

# How contributions arise

**Question this map answers:** when a paper turns prior art into a
contribution, what actually happened — and how can we code it from the
record without believing the story the paper tells about itself?

This is the project's core question. The naive chain *prior art → idea →
paper* is treated as one hypothesis among four, and the concepts below
are the theory, the threats to reading it off the record, and the
instrument that does the reading.

## 1. Four shapes of genesis, and the theory behind each

- [[concepts/genesis-models]] — idea-first / means-first / problem-first
  / accretion. Means-first has the strongest direct evidence:
  [[literature/papers/dunbar1997scientists]] watched four labs in vivo and
  found unexpected findings common (18/70) and *more* reasoned-about
  than expected ones. [[literature/papers/simonton2010bvsr]] gives the
  theoretical reason sincere idea-first reports can still be
  reconstructions (blind variation, selective retention).
  [[literature/papers/sourati2023accelerating]] operationalises the
  problem-first/idea-first boundary computationally — predictable-from-
  attention vs "alien" hypotheses.
- [[concepts/adjacent-possible]] — problem-first made concrete: the
  ingredients exist, only the arrangement is new. Fingerprint: Merton's
  multiples ([[literature/papers/merton1961singletons]]); quantitative
  form: innovation rate and diversification are predictable from the
  current combinatorial space ([[literature/papers/taalbi2022adjacent]]).
- [[concepts/literature-based-discovery]] — the zero-new-ingredient
  limit case: Swanson's A→B, B→C ⇒ test A→C
  ([[literature/papers/swanson1986fishoil]]). If H4 holds, discovery is
  often a search problem of this shape with fuzzier connectors.

## 2. Why the record lies, and how to read it anyway

- [[concepts/hindsight-narrative-bias]] — introductions narrate the
  genesis that should have happened
  ([[literature/papers/medawar1963fraud]]), the habit is trained in, and
  an LLM coder adds a third layer by knowing what the paper became
  ([[literature/papers/yang2024moose]]'s post-cutoff benchmarking is the
  structural fix). Consequence: idea-first estimates from introductions
  are upper bounds; means-first is the model most often rewritten.
- The H4 threat that no reference list can see:
  [[literature/papers/tahamtan2018creativity]] — landmark-paper authors
  trace the idea to a practical problem or a conversation, not to any
  citation. Hence the card's `uncited-social` ingredient status and the
  `external_story` field.

## 3. The instrument and its precedent

- [[concepts/genesis-card]] — one file per paper: problem, ingredients
  (cited / uncited-existing / new-here / uncited-social), move, enabler,
  genesis model with evidence, authors' story kept separate, twin
  contrast. Two independent coders in the pilot; agreement gates closed
  coding. Prompt: `prompts/open-code.md`.
- [[concepts/move-taxonomy]] — the codebook of operations on prior art;
  a prior list (transfer, recombination, scale, instrument, resource,
  simplification, …) to be overwritten by open coding. Dunbar adds a
  *distance* sub-feature to any analogy move (99 observed analogies were
  overwhelmingly local); [[literature/papers/sternberg1999propulsion]]
  suggests paradigm-relationship as an orthogonal axis.
- [[concepts/triz-lineage]] — the precedent and the warning: patents →
  principles worked as a catalogue but was never sampled, controlled, or
  evaluated. The TRIZ-efficacy critique is still unsourced in this graph
  ([[literature/papers/ghane2023semantictriz]] maps automation, not
  validity) — an open `/discover` target.

## Open thread

H0 predicts idea-first is the minority model. The sources here lean the
same way — but every one of them is either lab-ethnography, theory, or
authors' retrospection. The pilot's 15 coded pairs are the first test on
randomly sampled papers with a twin to compare against.
