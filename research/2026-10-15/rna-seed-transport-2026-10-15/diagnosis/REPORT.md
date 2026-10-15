# Why the previous transport models lose seed dependence

The previous equations erase seed differences through repeated withdrawal, irreversible removal of leaked cargo, competence loss, and insufficient seed-dependent production after replenishment. Global-mean exchange also removes spatial correlations. Removing competence loss or cargo loss alone does not repair the failure. Removing replenishment preserves a PAGE percentage mainly by retaining old reporter product in a dwindling inventory; that is not sustained catalytic function. The source recheck below identifies a distinct unsupported assumption: treating extracellular material as an irreversible sink.

This fixed-parameter investigation is explanatory and retrospective. It does not fit a new model or validate a transport mechanism. All twelve predeclared interventions and both chemistry families are retained, including failures and counterfactuals that contradict the experimental protocol.

## The experimental seed was supplied only initially

The [original article](https://www.nature.com/articles/s41467-023-36940-z), its Figure 3 caption, and its Methods describe initial F1 followed by substrate-only replenishment (`salibi.txt`, lines 45, 47 and 111). Supplementary Figure 19 corroborates half-volume transfer (`salibi_si.txt`, lines 444–449). The earlier implementation correctly omitted repeated exogenous F1 and used the stated transfer/incubation sequence. This verifies those schedule elements only.

Crucially, SI S19 describes washing the collected PAGE aliquots. Methods line 111 specifies an initial supernatant discard, then centrifugation in later generations without specifying another discard. Under the described half-sample transfer, continued-culture exterior is carried with the sample unless an additional supernatant removal is assumed. Thus loss from vesicles need not mean irreversible loss from the continuing culture. The previous instantaneous-discard closure excludes subsequent extracellular reaction and re-entry; the source does not establish that closure. Washing before PAGE instead distinguishes the observation compartment from the material available during culture. [source_interpretation.json](source_interpretation.json) records this corrected scope without changing diagnostic outputs.

The approximate 45% cargo loss after three FT cycles and tracer fluorescence shifts in SI S9 do not identify active-F1 survival, permeability, or exterior fate. A fresh web request was blocked by the publisher's identity redirect; this audit used the previously retrieved, hashed article and supplement.

## Quantitative reference failure

The measured seed-2 minus seed-0 yield contrast is 8.242 pp at G1 and 9.82833 pp at G7. Under the frozen fractional/uniform reference transport, the baseline predicts 6.52720 → 0.008277 pp and release predicts 11.75033 → 0.022562 pp. The complete set of 16 earlier transport scenarios gives G7 contrasts from −0.000764 to 0.022975 pp. All thus lose the measured separation, including the earlier contact and all-or-none closures.

The stage decomposition identifies where the competent-catalyst contrast contracts in the previous irreversible-sink model. Every post-G1 feed multiplies the difference between seed arms by 0.5; exchange plus equal material retention multiplies it by 0.55. The reaction then multiplies the remaining competent contrast by 0.25–0.52 for the baseline and 0.54–0.66 for release over G1–G7. Maintaining the contrast after transfer and material loss would require a net reaction multiplier of 1/(0.5 × 0.55) = 3.636, conditional on those assumptions. These ratios compare two complete trajectories, not a local linear stability eigenvalue or universal chemical reproduction number. A finite exterior bath can return leaked material, so this contraction formula cannot simply be imposed on that revised system.

| Generation | Baseline seed contrast, pp | Release seed contrast, pp | Measured mean contrast, pp |
|---|---:|---:|---:|
| 1 | 6.52720 | 11.75033 | 8.24200 |
| 2 | 3.43757 | 6.74162 | 10.74100 |
| 3 | 1.24487 | 2.64383 | 9.80600 |
| 4 | 0.38610 | 0.88231 | 10.47833 |
| 5 | 0.11094 | 0.27085 | 11.17500 |
| 6 | 0.03063 | 0.07930 | 9.31133 |
| 7 | 0.00828 | 0.02256 | 9.82833 |

Raw observations and descriptive replicate SDs are preserved in [observed_seed_contrasts.csv](observed_seed_contrasts.csv). The earlier fitted model scenarios are in [previous_seed_contrasts.csv](previous_seed_contrasts.csv); every reaction-stage ratio is in [reaction_contrast_gains.csv](reaction_contrast_gains.csv). No significance test is inferred from three replicates.

## Which assumptions matter

The following are G7 seed-2 minus seed-0 contrasts. All other constants, including the previously calibrated mixing scalar, remain fixed. Values are diagnostic model outputs, not estimates of the consequences of changing an actual experiment.

| Intervention | Baseline PAGE, pp | Release PAGE, pp | Baseline competent F1, µM | Release competent F1, µM |
|---|---:|---:|---:|---:|
| Reference | 0.008277 | 0.022562 | 5.17e-7 | 5.91e-6 |
| Zero competence loss | 0.095473 | 0.356013 | 3.78e-4 | 1.25e-3 |
| Perfect cargo retention | 0.002051 | −0.037101 | −6.56e-4 | −1.18e-3 |
| Zero competence and cargo loss | 0.163452 | 0.023144 | 0.02365 | 0.01258 |
| No transfer and no fresh feed | 10.604135 | 18.652632 | 5.20e-5 | 7.66e-5 |
| Both Hyper-A background paths removed | 0.014365 | 0.025031 | 2.79e-6 | 7.72e-6 |
| Unseeded active initiation removed | 0.013354 | 0.024588 | 2.75e-6 | 7.71e-6 |
| Direct background reporter ligation removed | 0.008643 | 0.022957 | 4.51e-7 | 5.91e-6 |
| No regeneration | 0.007863 | 0.012490 | 6.90e-7 | 8.30e-7 |
| Fresh substrate replaced by empty volume | 8.210625 | 14.679518 | 7.53e-7 | 1.04e-6 |
| Complete global mixing | 0.056548 | 1.331405 | −4.25e-5 | 1.84e-3 |
| No further mixing after G1 | 0.002962 | 0.005680 | 7.34e-7 | 1.02e-6 |

Competence loss accelerates forgetting, but setting it to zero gives less than 0.36 pp separation. Perfect cargo retention raises the common background substantially and can invert the small final contrast because the seeded reaction depletes substrates differently. Removing Hyper-A initiation eliminates background generation while leaving insufficient seed-driven production to counter the sinks. Disabling regeneration confirms that some new active catalyst exists in the reference; its production is insufficient to preserve the difference between seed arms. Neither “add more retention” nor “remove all background” is a sufficient explanation within this chemistry.

Stopping mixing after G1 blocks replenishment of productive local combinations. Complete global mixing increases reaction and gives at most 1.33 pp of contrast, while its G7 yields are 42.5–42.6% for the baseline and 16.8–18.2% for release. It does not reproduce the observed seed-specific pattern. These limits support investigating local productive encounters, not simply increasing a common exchange rate.

The transfer and feed interventions reveal an observer trap. With empty-volume feed, seed-2 G7 total reporter inventory is only 0.000198234 µM instead of 0.474131 µM in the reference. New reporter production during G7 is 1.82e−10 µM (baseline) or 4.06e−11 µM (release), despite apparently substantial final yields of 12.18% and 15.35%. The retained historical product dominates that percentage. No-transfer/no-feed also retains a large fraction but produces only 3.26e−7 or 1.54e−7 µM new reporter at G7. Both counterfactuals remove the experimental replenishment requirement. [generation_production.csv](generation_production.csv) separates inherited reporter from new product in every generation and seed arm.

## Analytic checks on transport and founder persistence

Under the previous irreversible exterior sink, common material retention and uniform competence hazard, the expected competent founder concentration is

`C_founder(g) = (seed/3) × retention^g × 0.5^(g−1) × exp(−60 kd g)` for g ≥ 1.

The post-G1 generation multiplier is 0.126466 for baseline and 0.129844 for release. With initial seed 2 µM, G7 competent founder is 6.90e−7 or 8.30e−7 µM. If competence is ignored, G7 retained founder material is 0.000158587 µM for either model. These are conditional expectations, not measured founder survival, lineage tracing, or free-F1 concentrations. Total competent F1 includes competent strands inside complexes. The diagnostic subtracts founder only from total competent inventory, never from free F1.

For fractional exchange `x_i'=(1−m)x_i+m mean(x)`, the weighted mean is unchanged and each deviation from the mean contracts by `1−m`. A variance or covariance therefore contracts by `(1−m)^2` per FT before uniform material loss. Three FT plus 0.55 retention multiply local concentration variances by `0.55^2 (1−m)^6`: 0.24090 for baseline and 0.19732 for release. This is a within-population mixing identity. It does not directly multiply the mean difference between separately seeded experiments. Every species obtains a positive contribution from the population mean for any positive m, irrespective of its distance or encounter history.

The earlier contact model changes which fraction receives the mean, but the newly added mixed cohort still has the composition of the whole population. It therefore does not represent sparse pair encounters. Equal species retention also forces full catalyst, substrates, inactive products and bound complexes to share a loss law. That closure is particularly important because molecular size, folding and complexes can influence exchange; the aggregate retention datum does not identify a separate rate for each.

## Implication for the next transport model

A minimal defensible next comparison retains the legacy model as its reference and tests a finite common exterior bath and deterministic effective patch exchange, all with the same frozen selected bulk chemistry. The finite bath explicitly conserves material that leaves vesicles and allows its subsequent fate to differ from the washed PAGE observation. Effective patches test limited exchange while preserving local substrate–catalyst correlations; they are not a resolved microscopic lattice or lineage graph. The comparison retains the source-defined half-volume substrate feed and explicitly accounts for exterior carryover. It introduces no selective-mobility hypothesis. All candidates should use the same held-out groups and retain every negative result.

Finite exterior persistence and effective patch exchange have not been tested in this diagnostic. The results motivate testing both assumptions, while leaving open the possibility that frozen bulk chemistry remains inadequate. Increased seed memory is not by itself a successful model: current-generation reporter production, active catalyst, total material, and held-out residuals must all remain visible.

“Seed memory” denotes dependence of later observations on the initial dose. “Founder persistence” denotes survival of molecules already supplied initially. “New synthesis” denotes material formed from supplied precursors; the reporter is catalytically inactive. “Physical inheritance” requires passage of functional material into subsequent compartments or populations. The deterministic cohort means and PAGE fractions here do not demonstrate ancestry-resolved functional inheritance or autonomous life.

## Reproducibility and checks

Run `audit.py` with Python 3.12.3, NumPy 2.4.1 and SciPy 1.16.1, then `python3 summarize.py`. The [protocol](PROTOCOL.md) was written before execution. All 72 trajectories were repeated at tighter tolerances: 1,584 rows in [stage_states.csv](stage_states.csv), 1,584 in [refined_stage_states.csv](refined_stage_states.csv), and 528 contrasts in [seed_contrasts.csv](seed_contrasts.csv). Species, source/removed/retained inventories, active founders, local variance and covariance remain available.

[verification.json](verification.json) records PASS: reference yields exactly reproduce the previous implementation; maximum tolerance-refinement change is 1.70e−6 pp or 8.33e−9 µM; maximum moiety imbalance is 6.70e−11 µM. The no-background zero-seed and no-regeneration founder identities passed. Input hashes were unchanged. The first launch failed at Python parsing before any trajectory ran; its log remains in `execution.log`, followed by the successful `execution-v2.log`. This was a syntax correction, not a response to a scientific score.

No measured parameter was fitted, no earlier artifact was edited, and no new experimental validation was obtained. Numerical checks reuse the earlier chemistry implementation and do not constitute an independent chemical solver.
