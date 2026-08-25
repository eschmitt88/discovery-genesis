# H3 — does the move distinguish impact? A pre-specified replication test

The pilot (15 pairs, 2026-08-23) produced two move contrasts and I reported
them: impactful papers *first-measure* (10/15 vs 4/15, Fisher p = 0.033) and
median papers *re-apply to the next target* (2/15 vs 7/15, p = 0.054). The
main sample is the independent test of both.

**Test set:** 29 primary-research pairs from `main50`, coded by two blind
coders under frozen v1.1, pair-blinded batches. The pilot's 9 surviving pairs
are reported separately and never pooled into the confirmatory test — they
generated the hypothesis.

## Neither contrast replicates

| move | pilot (generating) | main50 (independent) | verdict |
|---|---|---|---|
| `gap-filling:first-measurement` | 10/15 case vs 4/15 twin, p = 0.033 | 9/29 vs 11/29; discordant 5/7; sign p = 0.77 | **not replicated — direction reverses** |
| `gap-filling:next-target` | 2/15 vs 7/15, p = 0.054 | 16/29 vs 20/29; discordant 3/7; sign p = 0.34 | **not replicated** |

Pooling the two samples makes `next-target` look significant (17 vs 27 papers,
discordant 3/13, sign p = 0.021), but that pool contains the sample the
hypothesis came from, so the number is not a test of anything. It is recorded
here only so nobody recomputes it later and mistakes it for evidence.

## Every other move is null at n = 29

No move reaches p < 0.05 on the paired sign test in the independent sample.
The largest remaining signal is `instrument` — 8/29 cases vs 2/29 twins,
7 case-only discordant pairs against 1, sign p = 0.070 — which points the same
way as the genesis-model result below and is the one contrast worth powering
for. Twelve other labels are flat or too rare to test.

## The one direction that is consistent: means-first

| sample | case | twin | discordant | sign p |
|---|---|---|---|---|
| main50 (independent) | 8/29 | 2/29 | 7 / 1 | **0.070** |
| pilot B | 2/9 | 2/9 | 1 / 1 | 1.00 |
| pooled | 10/38 | 4/38 | 8 / 2 | 0.109 |

`means-first` — the contribution exists because a capability new to the
authors or the field existed — is about 4x more common among impactful papers
in the independent sample, and `instrument` (its move-level counterpart) shows
the same 7-vs-1 discordance. Neither clears 0.05, and with 13 moves tested
neither would survive multiplicity correction if it did. **This is the
project's most promising lead, not a finding.** A power calculation from the
observed 7/1 split says ~90 discordant pairs are needed for 80 % power at
alpha 0.05, which at the observed discordance rate means roughly 300–350
primary-research pairs.

## What H3 says today

**The move a paper makes on its prior art does not, by itself, distinguish
impactful work from ordinary work in a matched comparison at n = 29.** The
move taxonomy is reliable (κ 0.73 on genesis model; every paper shares a move
label between coders) and it describes the corpus well — it simply is not
where the impact difference lives. That is a negative result about the
project's central hypothesis and it changes what the deliverable can be: a
skill built on "make move X" has no evidence behind it, whereas the
bibliometric result (impactful papers build on markedly hotter, more recent
work — `results/pooled-primary.md`) does.
