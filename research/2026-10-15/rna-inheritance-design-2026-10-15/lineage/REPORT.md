# Conditional experiment design for F1 retention and inheritance

The six-generation design can distinguish newly generated catalytic competence and parent-dependent state **under the supplied strong-renewal, qualified-assay scenario**. It cannot do so at the small-GUV sample budget, for weak renewal, or for every state threshold. These simulations are experiment-design calculations; no new RNA chemistry, physical inheritance, genetic inheritance or evolution has been observed.

The [protocol](PROTOCOL.md) was frozen after development and independent review, before the 128-experiment campaign. The failed RNA fits supplied no reaction rates. [Research rationale](../research/lineage/REPORT.md) and the [assay design](../research/assays/REPORT.md) provide the component evidence and missing experimental qualifications.

## Distinguishing synthesis from fluorescence and old catalyst

Each 66-nt full-length F1 inventory is represented by origin and active/inactive state. Original founder, earlier newly ligated material, current-generation ligated material and incoming donor catalyst remain separate. Reporter product is inactive and consumes its own precursor plus B. An inactive full-length new molecule is not credited as a catalyst.

The terminal-generation pulse is the crucial provenance intervention. Before g5 incubation, randomly allocate one daughter in each sister pair to a labelled-feed pulse and destructive measurement; its unpulsed sister continues. At g6 its terminal descendants receive the pulse and are destroyed. The proposed analytical codes must distinguish original founder, ordinary feed and terminal pulse. Only current-generation material is assigned to the observer's `new` channel. All earlier F1 is conservatively included in the old-material nuisance bound, regardless of whether it was once newly synthesized. Every pedigree record gives parent and daughter IDs, birth/restored volumes, terminal sample assignment and pulse assignment. Sampled parents never continue.

The shared [assay implementation](../assay/model.py) supplies isotope-resolved amount observations, native/refolded capacity measurements and conservative nuisance subtraction. It receives pooled amounts and simulated capacities; inference receives only their noisy observations and calibration. The lineage decision uses **terminal-new capacity**, not fluorescence or total capacity. All 16 g5 terminal tips and all 32 g6 terminal tips are pooled within their original family. Pooling changes the estimand to family-average competence and preserves root independence.

## Complete simulation surface

Nine worlds cross three hypothetical volume/LOQ platforms, with 128 independent Monte Carlo experiments each. Each experiment has 96 roots per high/low history × intact/reset arm, balanced over four batches. N=24/48/96 comparisons use registered batch-balanced prefixes of the same observations. There are **2,654,208 root-generation observations**, **31,104 joint decisions**, and corresponding whole-root history-shuffle diagnostics. The raw arrays include measurements, response factors, qualification and missingness, inference bounds, and separate labelled truth columns for audit; truth is excluded from decisions.

The three platforms are 0.524 pL with 1-fmol instrumental LOQ, 1000 pL with 1-fmol LOQ, and 1000 pL with 0.01-fmol LOQ. At 1 µM the 16-tip g5 pool contains only 0.008384 fmol in the small platform, versus 16 fmol in the 1-nL platform, before recovery or aliquot allocation. A 1-nL compartment is a different, externally fed platform requiring membrane, delivery and division qualification. These are assumed LOQs, not claimed intact-F1 instrument specifications.

| World | Distinguishing imposed mechanism | Role |
|---|---|---|
| Strong renewal | Four new F1 per active molecule/cycle, substrate-capped, 90% active | Large-effect conditional positive |
| Weak renewal | 0.5 new F1 per active molecule/cycle, 90% active | Low-effect sensitivity |
| Founder-only | Active original founder persists, no new F1 synthesis | Carryover control/no regeneration |
| Inactive-new | New full-length F1 forms but is inactive; founders survive | Identity/function confusion |
| Reporter-only | Inactive founder plus precursor-assisted reporter background | Explicit inactive-founder control |
| No-founder | Neither founder state present, complete precursor feed | Explicit no-founder control |
| Common feed | New active F1 is recreated independently of parental state | Environmental recreation |
| Horizontal | Source-accounted active donors enter; new local F1 is inactive | Import/vertical confusion |
| Shared-history environment | High/low external formation affects both intact and reset arms | Shared environment confounding |

All rates, fractions, volumes and error distributions are planning assumptions. Supply and loss are external interventions, not autonomous growth. Each reaction conserves A, B and reporter moieties exactly in integer molecules. Every physical split uses complementary molecular allocation; fresh feed, reset discard, horizontal donor input, external loss and terminal sampling enter the conservation ledger.

## Power and false positives

The joint decision requires at least 80% of all high-intact roots to show terminal-new native capacity beyond the assay's LOQ, and a positive conservative high-minus-low contrast in intact relative to reset arms, at **both g5 and g6**. Missing or ambiguous states take the entire interval [0,1]. Root and batch uncertainty enter the registered contrast margin. The three state thresholds define separate planning estimands; an any-threshold experimental discovery rule was not tested.

For the strong scenario and the **1-µM terminal-new capacity state threshold**:

| Platform | N=24, accepted/128 (95% Wilson interval) | N=48 | N=96 |
|---|---:|---:|---:|
| 0.524 pL, LOQ 1 fmol | 0 (0–2.91%) | 0 (0–2.91%) | 0 (0–2.91%) |
| 1000 pL, LOQ 1 fmol | 118 (86.22–95.70%) | 128 (97.09–100%) | 128 (97.09–100%) |
| 1000 pL, LOQ 0.01 fmol | 127 (95.71–99.86%) | 128 (97.09–100%) | 128 (97.09–100%) |

The two larger-platform 1-µM scenarios meet the ≥80% planning power target using the lower confidence endpoint. This is conditional power for an intentionally large supplied renewal effect, not an estimate of likely physical F1 performance or a justified final experimental sample size before assay qualification.

The original 0.5-µM threshold gives **0/128** joint acceptance in every platform/N combination. At 1000 pL, LOQ1 fmol and N96, all 128 experiments pass at g5, then none pass at g6: the low/reset bound intervals overlap the state threshold. Lowering the state threshold does not necessarily improve identification of a high/low contrast. The 2-µM threshold also loses g6 discrimination: 0/128 at LOQ1 fmol, and only 1/128 at LOQ0.01 fmol for each N. All weak-renewal combinations give 0/128. These failures remain in the full [summary](results-v1/summary.json).

Every condition in all seven null worlds gives **0/128** false acceptance; each condition's Wilson upper bound is **2.91%**, below the 5% planning target. All history-shuffled diagnostics also give zero acceptance. These are per-condition Monte Carlo intervals, not simultaneous familywise bounds over the complete design surface and not guarantees against unmodeled confounding.

![Conditional design performance](results-v1/design-performance.png)

The first three panels show strong renewal, including every registered state threshold. Weak renewal is zero throughout. The fourth panel retains the largest per-condition null confidence endpoint. Error bars are Wilson intervals across independent simulated experiments; descendants never count as independent replicates.

## Retention and uncertainty

The independent no-feed retention calibration supplies 90% molecular retention and 5% chemical inactivation among retained catalyst, giving nominal native-capacity retention 85.5%. The shared observer measures before/after absolute amounts and native/refolded capacities, while external loss and inactivation remain separately audited. The assay observes whole-family aliquots; it cannot resolve individual-daughter retention.

All 128 small-platform before/after pairs are unresolved because the denominator is censored. At 1 nL/LOQ1 fmol, the mean molecular retention interval is **0.542–1.506**, and the mean native-capacity interval **0.514–1.429**. At LOQ0.01 fmol the corresponding native interval remains broad, **0.518–1.441**. Sensitivity alone does not remove systematic recovery/calibration uncertainty. These intervals cover the supplied truth in all 128 pairs but cannot precisely establish a physical retention percentage or distinguish modest retention differences. Values above one are retained as measurement uncertainty; clipping them would conceal the calibration limitation. [Raw retention observations and bounds](results-v1/retention-1.json).

Every qualified terminal-new capacity interval covers simulated truth in this campaign. Coverage is calculated within each independent experiment, then summarized across experiments; pooled root counts are descriptive. Zero empirical cluster variance gives a t interval of [1,1], which is not certainty. The companion all-covered-experiment Wilson interval is **97.09–100%**. Missing/unqualified observations remain excluded from that conditional coverage estimand but included adversely in inference denominators.

## Reproduction and evidence

Run from the repository root with the pinned runtime:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-inheritance-design-2026-10-15/lineage/run.py --output NEW_DIRECTORY
```

Use `--replay rna-inheritance-design-2026-10-15/lineage/results-v1 --output NEW_DIRECTORY` for the full independent regeneration/comparison. Results directories are never overwritten. [Eight tests](tests.txt) cover stoichiometry and open-system balances in all nine worlds, complementary partition, destructive genealogy, known contrast1/0 behavior, missing/censored observations, blocked controls, shuffled family consistency and seed replay. [Frozen code and source archive](results-v1/sources.zip), [hash manifest](results-v1/freeze.json), [raw-array numerical digests](results-v1/numerical-digests.json), [all decisions](results-v1/decisions.json) and [execution record](results-v1/execution.json) accompany the raw NPZ arrays. A complete illustrative pedigree covers one full root per history/arm for each world/platform; for example [strong/1-nL pedigree](results-v1/pedigree-strong-1.json).

Development-v1 motivated the threshold surface. Development-v2 is explicitly invalid because an accumulator was shadowed when adding that surface; independent review caught it before official execution. Development-v3 reran the repaired implementation with a behavioral contrast regression test. No official-result tuning was performed.

The parent executor completed the [independent integrated replay](../verification-v1/verification.json): **74 checks pass**, with all 27 lineage raw numerical arrays, scientific summaries, decisions and pedigrees reproduced exactly. The integrated suite independently ran all 17 assay/lineage tests (eight lineage tests). Numerical agreement verifies implementation and reproducibility; it does not qualify the assumed chemistry or apparatus. Requirement-level evidence is in [checks.md](checks.md).

Skipped wet experiments, device construction and instrument qualification. Risks: intact-F1 provenance resolution, additive nuisance calibration, native recovery, volume accuracy and repeated compatible division remain unvalidated; simulated parent-dependent fixed-sequence state is not genetic inheritance or evolution.
