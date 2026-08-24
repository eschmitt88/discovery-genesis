# H1 pooled — 38 primary-research pairs (pilot B 9 + main50 29)

Both members of every pair were called primary research by two blind coders
(`genesis.primary`; verdicts in `data/primary-{pilotB,main50}.json`). Reviews,
guidelines, consensus statements and trend reports are excluded — 16 of 50
main50 **cases** but only 2 of 50 twins, so the contamination was almost
entirely on the impactful side.

| feature | median Δ (case − twin) | pairs + / − | p | BH q |
|---|---|---|---|---|
| `ref_hot_median` | **+140 citations** | 32 / 6 | 0.00001 | **0.0000** |
| `n_refs` | **+13.5** | 31 / 7 | 0.00001 | **0.0001** |
| `ref_fwci_median` | **+2.7** | 30 / 8 | 0.0001 | **0.0004** |
| `ref_share_le3` | **+0.072** | 29 / 9 | 0.0004 | **0.0011** |
| `n_authors` | **+2** | 25 / 9 | 0.0028 | **0.0067** |
| `n_institutions` | **+1.5** | 24 / 9 | 0.0067 | **0.0134** |
| `ref_age_median` | **−2 years** | 10 / 24 | 0.028 | **0.0481** |
| `ref_cross_subfield` | −0.083 | 16 / 22 | 0.105 | 0.157 |
| `ref_cross_topic` | −0.095 | 16 / 22 | 0.154 | 0.205 |
| `ref_n_fields` | 0 | 18 / 14 | 0.300 | 0.359 |
| `ref_cross_domain` | 0 | 14 / 18 | 0.329 | 0.359 |
| `ref_cross_field` | −0.068 | 17 / 21 | 0.407 | 0.407 |

## What replicates

**Reference hotness is the strongest and most consistent signal.** The median
reference of an impactful primary paper has ~140 more citations than the
median reference of its twin, in 32 of 38 pairs. `ref_fwci_median` says the
same thing field-normalised. This held at n = 15 (δ +0.68) and at n = 29
(δ +0.58) independently.

**Reference recency holds but is smaller than the pilot suggested.** The
share of references ≤ 3 years old is +0.072 pooled (the pilot's 15 pairs gave
+0.15). Median reference age is −2 years pooled, and only just clears FDR;
the pilot's −4 years was an overestimate.

**Team size and reference count are real, modest effects** that the pilot was
too small to see: +2 authors, +1.5 institutions, +13.5 references.

## What does NOT replicate

**The breadth reversal.** At n = 15 I reported that impactful papers cite
*less* across topic, subfield and domain (cross-domain q = 0.050). Pooled
over 38 pairs every cross-boundary feature is null: the direction is still
negative at topic and subfield level (16 / 22 pairs) but nowhere near
significance, and cross-domain and `ref_n_fields` are flat. **The claim that
impactful papers are more local was over-read from 15 pairs and does not
survive.** What survives is the weaker statement: breadth of citation does
not distinguish impactful from ordinary work in either direction.

This also removes the bibliometric leg of the "crossing fields does not pay"
story. The coding leg has weakened too: `transfer` under the strict v1.1
definition was 2 codings in 130 papers.
