# Open coding — genesis card v0 (pilot)

You are coding one research paper for a study of how contributions arise
from prior art. You will see a dossier: bibliographic header, abstract,
the reference list (with each reference's year, topic and — where known —
how the paper uses it: method / background / result), and the full text if
an open-access copy exists. You will NOT be told how impactful the paper
turned out to be, and you must not try to infer or recall it. If you
recognise the paper and know what it became, say so in `recognised:` and
code only from what the dossier shows.

Write the card as Markdown with flat YAML frontmatter, exactly these keys:

```yaml
---
kind: genesis-card
id: <OpenAlex id>
codebook: v0-open
coder: <your model name>
recognised: <no | yes — what you recall, one line>
evidence: <full-text | abstract+contexts | abstract-only | title+refs-only | tldr-only>
is_primary: <yes | no — review / guideline / perspective / survey | partial — e.g. methods paper, dataset, framework>
problem: "<one sentence: what was open or unsatisfactory before this paper>"
problem_age: "<new (<3 y) | established (3–15 y) | old (>15 y) | n/a>"
ingredients:
  - what: "<component the contribution depends on>"
    status: <cited | uncited-existing | new-here | uncited-social>
    year: <year of the ingredient or null>
    role: <method | data | theory | instrument | problem | result>
move: "<free text, one line: what the paper DID to the prior art — verb first>"
move_candidates: [<1–3 short labels from: transfer, recombination, scale, instrument, resource, simplification, inversion, unification, relaxation, reformulation, anomaly, consolidation, gap-filling, formalisation, other:<label>>]
enabler: "<what made it possible now: new data | new tool | new compute | new theory | new collaboration | imported problem | nothing identifiable — plus one line>"
genesis_model: <idea-first | means-first | problem-first | accretion>
genesis_confidence: <low | medium | high>
genesis_evidence: "<the two or three observations in the dossier that decided it>"
authors_story: "<the genesis the introduction narrates, in one sentence — keep separate from yours>"
contribution: "<one sentence: what the paper adds, stated neutrally>"
---
```

Then three short sections:

## Reasoning
Why this move and this genesis model. Point at specific references (year +
short title) and at sentences in the abstract or text. Say what evidence
would have changed your mind.

## Alternative reading
The second-most-likely genesis model and why it is less likely.

## Notes for the codebook
Anything the v0 labels could not express — a move that fits no label, an
ambiguity between two labels, a field-specific pattern.

Rules
- Code from the dossier only. No web search, no recall of the paper's later reception.
- Some dossiers have no authors' abstract. If the Abstract section is labelled a
  machine-generated summary, set `evidence: tldr-only` and lower
  `genesis_confidence` accordingly; if there is no abstract at all, use
  `title+refs-only`. A reference list plus citation intents still supports a
  defensible `problem` and `ingredients`; it rarely supports a confident
  `genesis_model` — say so rather than guessing.
- `is_primary`: institutional surveillance or trend reports (MMWR, ESPAD) and
  essays/commentaries are `no — <kind>`; code them as accretion unless the
  dossier shows otherwise.
- `move_candidates`: list up to 3, **most central first**. Co-listing
  "transfer, gap-filling" is expected and fine.
- Code the *contribution*, not the topic: "applied X to Y" is a move only if
  the paper does it; a paper that cites foreign-field work decoratively has not transferred.
- `genesis_model` decision guide:
  - idea-first: the paper states a proposition and its design follows from it;
    the proposition could have been written before the work began.
  - means-first: a new instrument / dataset / compute / technique is the
    starting point and the result is what it revealed; the idea is recognised in the data.
  - problem-first: an established problem meets a recently available ingredient
    (≤ 3 y old among the references) — the move was close to forced.
  - accretion: no single locatable idea — consolidation, standardisation,
    the definitive version, a resource, a review-like survey, a large trial of an established question.
- Be literal and brief. The card is data, not an essay.
