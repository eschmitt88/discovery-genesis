---
kind: candidates
topic: "science-of-science findings and metrics on novelty, impact, disruption, recombination"
discovered: 2026-08-22
source: discover
n_requested: 14
n_returned: 17
---

## 1. Atypical Combinations and Scientific Impact (Uzzi, Mukherjee, Stringer, Jones, 2013)

- url: https://www.science.org/doi/10.1126/science.1240474
- type: paper
- summary: Across 17.9M papers, the highest-impact work pairs an exceptionally conventional core of journal-pair combinations in its references with an atypical tail; papers with this "hit" profile are ~2x more likely to be highly cited than uniformly novel or uniformly conventional ones.
- reason: Direct empirical basis for H1's atypicality proxy (10th-percentile conventionality + minimum/atypical-tail measure); the plan's feature block cites this design explicitly.

## 2. Papers and patents are becoming less disruptive over time (Park, Leahey, Funk, 2023)

- url: https://www.nature.com/articles/s41586-022-05543-x
- type: paper
- summary: Using the CD index over 45M papers and 3.9M patents (1945-2010), disruptiveness (CD5) has declined steadily across nearly all fields and patent classes even as output volume grew, attributed to narrowing "attention" per unit of knowledge rather than declining quality of ideas.
- reason: The canonical large-scale application of the disruption index the plan's `[[disruption-index]]` feature (CD5, computed from OpenAlex citers) is modeled on; sets up the secular-trend context for any disruption number the pipeline computes.

## 3. Matters Arising: dataset artefacts partially drive the measured decline in disruption, and reply (Holst, Ginis et al.; Park, Leahey, Funk reply; Nature, 2026)

- url: https://www.nature.com/articles/s41586-026-10787-y
- type: paper
- summary: A 32-month-delayed Nature Matters Arising argues a seaborn plotting bug hid a spike of maximum-disruption (CD=+1) papers in Park et al.'s histograms, and that dataset artefacts (esp. zero-backward-citation works) account for up to 93% of the reported decline in the largest dataset; Park/Leahey/Funk's simultaneous reply disputes the critique's own data quality and reports the original trend holds under the critics' methods too.
- reason: The single most load-bearing 2024-2026 update on this exact thread — an unresolved, live methodological dispute over the very index (CD/CD5) the project's bibliometric feature block depends on. Content verified via WebSearch result snippets and secondary coverage (arXiv companion pieces below); direct Nature fetch was paywalled (403), so treat citation details as search-verified, not full-text-verified.

## 4. A Dynamic Network Measure of Technological Change (Funk & Owen-Smith, 2017)

- url: https://pubsonline.informs.org/doi/10.1287/mnsc.2015.2366
- type: paper
- summary: Introduces the original CD index — a paper/patent is "disruptive" if later work citing it tends not to also cite its own references, and "consolidating" if the opposite — validated on university patenting data linking federal funding to more destabilizing inventions and commercial ties to more consolidating ones.
- reason: The primary source for the CD/CD5 formula the plan cites directly under `[[disruption-index]]`; needed to implement the metric correctly rather than only via secondary description.

## 5. The disruption index is biased by citation inflation (Bentley, Kyriakou, Mackay, Petersen et al., 2023/2024)

- url: https://arxiv.org/abs/2306.01949
- type: paper
- summary: Shows growing reference-list lengths mechanically drive the CD index toward zero over time (citation inflation), a bias correlated with team size and other confounds; a weighted/deflated CD variant reverses or mutes the apparent decline in disruptiveness.
- reason: Core critique of the CD index for H1/H5 — the project must decide whether to use raw CD5 or a deflated variant before treating "disruption" as a clean impact-adjacent feature; directly relevant to the twin-pair comparison design.

## 6. Bias against novelty in science: a cautionary tale for users of bibliometric indicators (Wang, Veugelers, Stephan, 2017)

- url: https://www.nber.org/papers/w22180
- type: paper
- summary: Defines novelty as a paper's first-ever combination of two journals in its reference list (weighted by their prior co-citation distance); novel papers are cited less in the short run but more likely to be top-1%-cited and cross-disciplinary in the long run — bibliometric indicators using short citation windows penalize novelty.
- reason: A second, independent novelty operationalization (new journal pairs) complementing Uzzi's atypicality proxy — useful for triangulating H1's novelty measure and directly warns against short citation windows, which matters for the plan's 2010-2019 sampling window and long-tail impact (sleeping beauties, entry 12).

## 7. Tradition and Innovation in Scientists' Research Strategies (Foster, Rzhetsky, Evans, 2015)

- url: https://journals.sagepub.com/doi/abs/10.1177/0003122415601618
- type: paper
- summary: Modeling millions of biomedical abstracts as a chemical-relationship hypothesis network, most published work consolidates known entities/relationships (tradition) rather than testing novel combinations (innovation); innovative work is riskier but pays off more in citations when institutional structures reward it, and the innovation deficit is more severe as fields mature.
- reason: Direct precedent for the plan's move taxonomy (H2/H3) — distinguishes exploration vs. consolidation strategies at the level of individual research choices, which is close to the "move" unit the genesis cards need to code.

## 8. Surprising combinations of research contents and contexts are related to impact and emerge with scientific outsiders from distant disciplines (Shi & Evans, 2023)

- url: https://www.nature.com/articles/s41467-023-36741-4
- type: paper
- summary: A hypergraph model predicts expected combinations of article keywords (contents) and cited-journal contexts; "surprising" realized combinations — more common when authors publish into audiences from distant fields — predict outsized (top-10%) citation impact across life sciences, physical sciences, and patents.
- reason: Extends Uzzi/Wang-style novelty from reference-pair atypicality to content x context surprise, and its "outsiders from distant disciplines" finding bears directly on H3 (which moves are impact-enriched) and H5 (novelty vs. impact separated by who does the combining, not just what is combined).

## 9. Large teams develop and small teams disrupt science and technology (Wu, Wang, Evans, 2019)

- url: https://www.nature.com/articles/s41586-019-0941-9
- type: paper
- summary: Across 65M papers, patents, and software products (1954-2014), small teams disproportionately produce disruptive, question-raising work built on older/less-popular ideas, while large teams disproportionately produce consolidating, paradigm-stabilizing work built on recent/prominent ideas — the pattern holds within-author across a career.
- reason: Grounds the plan's "team size, number of institutions" bibliometric feature directly in a disruption-index finding, and is a strong H3 candidate (team-size-as-move-correlate) with a very large, well-cited empirical base.

## 10. The nearly universal link between the age of past knowledge and tomorrow's breakthroughs in science and technology: the hotspot (Mukherjee, Romero, Jones, Uzzi, 2017)

- url: https://www.science.org/doi/10.1126/sciadv.1601315
- type: paper
- summary: Papers/patents citing references with low mean age but high age variance ("hotspot" referencing) are about twice as likely to become top-5%-cited hits; this pattern holds nearly universally across scientific and technological fields.
- reason: Directly operationalizes the plan's "reference-age distribution; share of references <=3 years old" feature and gives it a validated functional form (mean age + variance, not just recency share) worth adopting or testing against.

## 11. New directions in science emerge from disconnection and discord (Lin, Evans, Wu, 2022)

- url: https://arxiv.org/abs/2103.03398
- type: paper
- summary: Atypical (novel-combination) papers are ~2x as likely to eventually disrupt their field as conventional papers, but the disruption signal takes 10+ years to converge, and many such papers pass through a "sleeping beauty" phase of delayed recognition before their disruptive impact is legible in citation data.
- reason: Directly links atypicality (H1) to disruption (CD index) and to delayed-recognition dynamics (entry 12), which matters for the plan's choice of a 2010-2019 window (a decade may still be short for slow-converging disruption signal) and is itself an H3-relevant "move" (atypical combination -> disruption) with a documented lag.

## 12. Defining and identifying Sleeping Beauties in science (Ke, Ferrara, Radicchi, Flammini, 2015)

- url: https://arxiv.org/abs/1505.06454
- type: paper
- summary: Introduces a "beauty coefficient" quantifying both the length of a paper's citation dormancy and the intensity of its eventual awakening; sleeping beauties are common, not exceptional, across the literature, undermining short-window citation metrics as a complete impact signal.
- reason: A direct challenge to the plan's sampling design — drawing on `citation_normalized_percentile` for 2010-2019 papers could systematically miss or mis-rank genuinely impactful-but-delayed work, which is exactly the open question the plan already flags about the paper being "the right unit" and impact accruing over time.

## 13. The Diversity-Innovation Paradox in Science (Hofstra, Kulkarni, Munoz-Najar Galvez, He, Jurafsky, McFarland, 2020)

- url: https://www.pnas.org/doi/10.1073/pnas.1915378117
- type: paper
- summary: Analyzing 1.2M US doctoral dissertations (1977-2015), underrepresented-gender/race scholars produce higher rates of novel topical combinations than majority peers, yet their novel contributions are taken up (cited, converted into careers) at systematically lower rates — diversity breeds novelty but not proportional recognition.
- reason: Squarely an H5 case study — same "move" (novel combination), different impact outcome, attributable to who made the move and how the community received it rather than to the move's content; a concrete mechanism candidate for the "residual difference" H5 asks twin-pair coders to identify.

## 14. Recombinant Uncertainty in Technological Search (Fleming, 2001)

- url: https://pubsonline.informs.org/doi/10.1287/mnsc.47.1.117.10671
- type: paper
- summary: Using patent citation data, shows that inventions combining unfamiliar components/component-combinations have higher variance in outcome quality than familiar recombinations — more failures, but also more breakthroughs — because what "belongs together" is a social convention, not a fixed constraint on the knowledge space.
- reason: The foundational recombinant-search theory paper behind the entire novelty/atypicality literature (Uzzi, Wang, Shi & Evans all build on this framing); directly relevant to H4 (contribution as new arrangement of cited ingredients) and to why novelty alone should predict variance in impact, not impact itself — a mechanism for H5's novelty/impact separation.

## 15. OpenAlex Field-Weighted Citation Impact (FWCI) / citation_normalized_percentile documentation

- url: https://help.openalex.org/hc/en-us/articles/24735753007895-Field-Weighted-Citation-Impact-FWCI
- type: post
- summary: Official methodology page: FWCI = citations received (publication year + 3 following years) / citations expected (same-window average for works matched on type, year, and OpenAlex subfield); `citation_normalized_percentile` expresses the same underlying rank as a percentile with `is_in_top_1_percent`/`is_in_top_10_percent` flags; ~68% of works carry an FWCI value as of mid-2026.
- reason: This is the exact field (`citation_normalized_percentile >= 0.99` / `0.40-0.60`) the plan's sampling frame uses to draw impactful cases and matched twins — needed to know precisely what the sampler is conditioning on (subfield-normalized, 4-year window, single-subfield assignment) and its known gaps (uncited/paratext exclusions).

## 16. A review on the novelty measurements of academic papers (Zhao & Zhang, 2025)

- url: https://arxiv.org/abs/2501.17456
- type: paper
- summary: A 2025 systematic review distinguishing novelty from originality/creativity/breakthrough, taxonomizing novelty measures by data type (text, references, topics/keywords), and surveying validation approaches and available tools/datasets across the literature this triage file covers.
- reason: The most recent (2025) synthesis of the whole novelty-measurement landscape named in this topic; useful as a map of alternatives and validation methods when the project has to pick and justify a specific novelty operationalization for the bibliometric feature block.

## 17. Structural Scaffolds for Citation Intent Classification in Scientific Publications (Cohan, Ammar, van Zuylen, Cady, 2019)

- url: https://arxiv.org/abs/1904.01608
- type: paper
- summary: A multitask scaffold model classifies why a citation was made (background / method / result-comparison) and introduces SciCite, a dataset 5x larger and more domain-diverse than prior citation-intent corpora; code and data at https://github.com/allenai/scicite.
- reason: This is the Semantic Scholar citation-intent classifier the plan's data-sources table names explicitly ("citation intents... tells us which references are load-bearing without reading every citer"); needed to know what "method" vs "background" citation labels actually mean before using S2 intents to identify a genesis card's load-bearing ingredients (H4).
