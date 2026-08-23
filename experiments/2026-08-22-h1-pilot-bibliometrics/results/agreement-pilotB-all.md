# Inter-coder agreement — cases/pilotB

Coders: coderA vs coderB; 30 papers coded by both (30 / 30 total).

| field | raw agreement | Cohen κ |
|---|---|---|
| genesis_model | 0.73 | 0.627 |
| is_primary | 0.83 | 0.643 |
| problem_age | 0.93 | 0.88 |
| problem_age_broad | 0.70 | 0.553 |
| problem_age_specific | 0.80 | 0.717 |
| enabler_head | 0.57 | 0.502 |
| move_primary | 0.67 | 0.582 |
| move_candidates (Jaccard) | 0.556 mean; 0.97 share with ≥1 shared label | – |

## genesis_model confusion (rows = coderA)

| | accretion | idea-first | means-first | problem-first |
|---|---|---|---|---|
| accretion | 5 | 0 | 0 | 2 |
| idea-first | 0 | 3 | 0 | 0 |
| means-first | 0 | 0 | 6 | 1 |
| problem-first | 0 | 2 | 3 | 8 |

## label distributions

- **coderA** genesis_model: {'means-first': 7, 'problem-first': 13, 'idea-first': 3, 'accretion': 7}
  moves: {'gap-filling': 17, 'consolidation': 12, 'instrument': 5, 'transfer': 4, 'recombination': 4, 'unification': 3, 'formalisation': 3, 'anomaly': 2, 'reformulation': 1, 'resource': 1}
- **coderB** genesis_model: {'means-first': 9, 'problem-first': 11, 'idea-first': 5, 'accretion': 5}
  moves: {'gap-filling': 17, 'recombination': 17, 'transfer': 6, 'consolidation': 6, 'formalisation': 4, 'unification': 4, 'instrument': 3, 'scale': 1}

Papers either coder reported recognising: 3 — ['W2078338131', 'W2136608905', 'W2149161770']

## Unblinded: move and genesis model by role

(computed after agreement, per the coding protocol)

- **case** genesis_model: {'idea-first': 3, 'problem-first': 15, 'means-first': 7, 'accretion': 5}
  moves: {'gap-filling': 19, 'recombination': 11, 'consolidation': 10, 'unification': 6, 'formalisation': 4, 'instrument': 3, 'scale': 1, 'anomaly': 1, 'resource': 1}
- **twin** genesis_model: {'means-first': 9, 'problem-first': 9, 'idea-first': 5, 'accretion': 7}
  moves: {'gap-filling': 15, 'recombination': 10, 'transfer': 10, 'consolidation': 8, 'instrument': 5, 'formalisation': 3, 'anomaly': 1, 'reformulation': 1, 'unification': 1}
