# Inter-coder agreement — cases/pilotB/v11

Coders: coderA vs coderB; 30 papers coded by both (30 / 30 total).

| field | raw agreement | Cohen κ |
|---|---|---|
| genesis_model | 0.83 | 0.73 |
| is_primary | 0.90 | 0.818 |
| problem_age_specific | 0.83 | 0.712 |
| enabler_head | 0.73 | 0.549 |
| move_primary | 0.57 | 0.49 |
| move_candidates (Jaccard) | 0.639 mean; 0.77 share with ≥1 shared label | – |

## genesis_model confusion (rows = coderA)

| | accretion | idea-first | means-first | problem-first |
|---|---|---|---|---|
| accretion | 4 | 1 | 0 | 1 |
| idea-first | 0 | 4 | 0 | 0 |
| means-first | 0 | 0 | 2 | 1 |
| problem-first | 0 | 0 | 2 | 15 |

## label distributions

- **coderA** genesis_model: {'problem-first': 17, 'means-first': 3, 'idea-first': 4, 'accretion': 6}
  moves: {'gap-filling:first-measurement': 10, 'gap-filling:next-target': 7, 'consolidation': 4, 'instrument': 3, 'gap-filling:bigger-n': 3, 'unification': 2, 'gap-filling:other': 2, 'formalisation': 2, 'recombination': 2, 'transfer': 2}
- **coderB** genesis_model: {'problem-first': 17, 'means-first': 4, 'idea-first': 5, 'accretion': 4}
  moves: {'gap-filling:first-measurement': 13, 'gap-filling:next-target': 7, 'consolidation': 4, 'instrument': 2, 'transfer': 2, 'gap-filling:bigger-n': 2, 'formalisation': 2, 'recombination': 2, 'unification': 2, 'inversion': 1}

Papers either coder reported recognising: 7 — ['W2078338131', 'W2127780961', 'W2134599653', 'W2136608905', 'W2149161770', 'W2783667606', 'W2837320447']

## Unblinded: move and genesis model by role

(computed after agreement, per the coding protocol)

- **case** genesis_model: {'idea-first': 4, 'problem-first': 18, 'means-first': 4, 'accretion': 4}
  moves: {'gap-filling:first-measurement': 17, 'consolidation': 5, 'gap-filling:bigger-n': 3, 'gap-filling:other': 2, 'formalisation': 2, 'instrument': 2, 'gap-filling:next-target': 2, 'unification': 2, 'recombination': 2, 'inversion': 1, 'transfer': 1}
- **twin** genesis_model: {'problem-first': 16, 'means-first': 3, 'idea-first': 5, 'accretion': 6}
  moves: {'gap-filling:next-target': 12, 'gap-filling:first-measurement': 6, 'instrument': 3, 'transfer': 3, 'consolidation': 3, 'unification': 2, 'recombination': 2, 'formalisation': 2, 'gap-filling:bigger-n': 2}
