# Why the RNA model failed, and what a revised model can establish

15 October 2026. **A more explicit, chemistry-grounded model family has been implemented and tested, but it has not resolved the RNA model's predictive failure.** The data support a modest retrospective ranking change, not a validated replacement mechanism. New public datasets strengthen the measurement design; active-F1 retention and physical functional inheritance remain unidentified.

## Diagnosis established by the audit

The old failure begins in homogeneous bulk chemistry, before any compartment transport is modeled. Its 40-point bulk RMSE is reproduced exactly at **7.866 percentage points**: **5.253** for F1-only curves and **9.806** for Hyper-A curves. All **148 previously extracted measurements match the source workbook**, so the audit found no unit conversion, duplicate endpoint or source-cell mistake. [Exact diagnostic replay](diagnosis-v1/diagnosis.json); [source audit](sources/salibi/audit.md).

The strongest discrepancies are interpretable. At 1 µM initial Hyper-A, measured reporter formation after 60 minutes is 14.401%, while the old model gives 0.961%. At 2.5 µM it instead overshoots: 78.974% predicted versus 59.730% observed. Fitting a different retention coefficient cannot fix these bulk errors.

Three assumptions warrant testing; they are not established causes of all residual errors:

1. **The precursor-assisted reporter route was omitted.** Salibi's SI13b depicts Hyper-A promoting Cy5-A+B ligation. The old model required active F1 to form first through its background reaction. The source supports the additional route topology, while leaving its elementary rate law and contribution unresolved.
2. **The rate law imposed unsupported reaction orders.** The old `A²B²` background law was inferred from a proposed tetramer drawing, not measured reaction orders. Its F1-catalysed reporter term was proportional to unbound B throughout the reaction. With B falling from 7.5 to about 2.74 µM in the high-yield F1-only assay, that law forces a strong depletion effect. Saturating substrate occupancy is a chemically plausible alternative; only the comparison can show whether it improves these data.
3. **Product inhibition was not identified.** The fitted inhibition scale reached its 1,000 µM upper bound and the high-value profile was nearly flat. That fit does not establish an inhibitory mechanism. The revision removes this term and examines other constrained hypotheses.

The primary chemistry involves substrate association, ligation and product-complex release, with possible nonproductive substrate association. [Ferretti and Joyce](https://doi.org/10.1021/bi301646n) and [Robertson and Joyce](https://doi.org/10.1016/j.chembiol.2013.12.004) motivate those distinctions. Their rates were measured under other conditions and are not inserted as constants into Salibi's sucrose-containing assay.

The precursor-assisted route also changes interpretation of the observer: newly formed inactive Cy5-F1 reporter is not uniquely attributable to newly generated active F1. A reporter signal can therefore support ligation without identifying which catalytic species caused it. The proposed route's existence and its quantitative contribution must be distinguished.

## Revised chemistry and measured outcome

The [frozen protocol](model/PROTOCOL.md) compares the old model with four reduced chemical alternatives. The new rate laws use substrate occupancy `sB = B/(KB+B)`:

```text
active ligation:    va = kF F A sB + kH A² sB²
reporter ligation:  vr = kF F R sB + h kH A R sB²
```

Here A is Hyper-A, R is accessible Cy5-A, B is the second fragment, F is active F1, and h is fixed to zero or one. An optional common accessible fraction q puts the remaining reporter into an explicit inactive reservoir, included in the PAGE denominator. Each ligation consumes one matching fragment plus B. The [implementation](model/model.py) separately tracks inactive reporter product, active catalyst, ablation product, material losses and feed. These are effective binding/assembly hypotheses; binding intermediates and elementary rate constants are not measured.

Five models received the same fixed optimization budget and eight whole-dose-held-out folds. All **40 folds resolved**. Selection used only those dose folds and a prespecified simplicity rule; former transfer holdouts were treated as historical development benchmarks.

| Chemistry candidate | Fitted parameters | Bulk fit RMSE, pp | Whole-dose CV RMSE, pp |
|---|---:|---:|---:|
| Original model, matched refit | 3 | 7.866 | 9.798 |
| Substrate-occupancy candidate, selected | 3 | 7.893 | 9.509 |
| Plus direct precursor-assisted reporter route | 3 | 7.890 | 9.517 |
| Plus accessible reporter fraction | 4 | 7.893 | 9.509 |
| Both additions | 4 | 7.890 | 9.517 |

The selected candidate lowers CV RMSE by **2.95%**, while slightly worsening the full-data fit. This small retrospective ranking is not a statistical significance claim. Its `KB≈100 µM` reaches the imposed upper bound, well above the assay's initial B concentration of 7.5 µM; the profile improves toward that boundary and the rate law approaches the original unsaturated limit. Strong substrate saturation is therefore **not identified**. The q variants fit q=1, providing no support for an inaccessible reporter pool within this family. The source-supported direct route does not materially improve the fit under the tested shared-coefficient constraint; its omission is not demonstrated to be the main cause of failure, and the comparison does not rule out the physical route. [All fits](model/results-v2/full_fits.json); [CV and convergence](model/results-v2/cross_validation.json); [binding-scale profiles](model/results-v2/profiles.json).

Two conservative exchange models were then calibrated on the same 18 Figure 2 observations. Fractional exchange partially mixes every cohort; contact exchange mixes a fraction of each cohort and leaves the remainder separate. Neither simulates division or creates offspring. On the 72 historical benchmark observations:

| Coupled model | RMSE, pp | Maximum absolute group-mean error, pp | Declared accuracy screen |
|---|---:|---:|---|
| Original model | 3.322 | 6.890 | Fail |
| Revised chemistry, fractional exchange | 3.280 | 6.945 | Fail |
| Revised chemistry, contact exchange | 3.594 | 7.089 | Fail |

The screen requires RMSE≤2 pp and maximum group-mean error≤4 pp. **All eight active-catalyst retention scenarios also fail**, spanning 0.30, 0.55, 0.80 and 0.95 retention over three cycles for each exchange model, with fragment retention held at 0.55. These are scenarios, not measured retention estimates or confidence intervals. No transport or retention choice is selected from these benchmark outcomes. [Predictions](model/results-v2/predictions.csv); [all scenarios](model/results-v2/sensitivity.json).

![Measured RNA curves, candidate comparison and historical serial benchmarks](<PROJECT_ROOT/rna-mechanism-2026-10-15/model/results-v2/comparison.png>)

Points are measured yields; curves are model outputs. The upper panels show the selected candidate's full-data fit, not held-out predictions. The persistent Hyper-A dose mismatch and serial-transfer discrepancies remain visible. The lower panels show separate replicate measurements. No prospective unseen validation is claimed.

Numerical checks pass: maximum material-balance discrepancy is approximately **6.3×10⁻¹⁵ µM**, and tightening integration tolerance changes reporter predictions by less than **3.8×10⁻⁶ pp**. Those results verify calculation, not physical adequacy. Disabling regeneration or exchange further degrades the serial benchmark within the supplied model; this is a model ablation, not an experimental demonstration of inheritance. Bulk-to-GUV transfer still extrapolates membrane effects and Hyper-A concentration: calibration covers 1–2.5 µM, whereas fresh substrate cohorts contain 10 µM.

## Additional observations from the original study

The expanded [workbook export](sources/salibi/observations.csv) contains **529 rows: 148 previously used and 381 additional**. These span serial transfers, membrane-effect assays, freeze–thaw chemistry, tracer-intensity histograms, size histograms and negative controls. They give useful challenges, but most do not match the original kinetic recipe.

- S18 shows substantial bulk chemistry during a longer freeze–thaw protocol, challenging the zero-reaction cycling assumption without supplying a calibrated rate for the shorter vesicle protocol.
- S15 shows membrane-associated changes in reporter yield, under a different substrate recipe and uncertain post-addition dilution. It cannot be used as an exact intravesicular rate multiplier.
- S9's tracer-intensity ratio is about 0.782 after one cycle. It measures a labelled 26-nt tracer, not active F1 survival. Size changes in S17 make amount, concentration and volume especially important to distinguish.
- S12 tests active-precursor versus inactive-product propagation. A nominal intermediate sample does not match a simple instantaneous tenfold-dilution observer. This could reflect timing, normalization or recipe details; it is not established experimental error. The values are preserved without tuning the revised chemistry to them.

The new S13 negative controls are an exact-condition zero-activity check, but offer little discrimination between the competing mechanisms. No newly acquired dataset provides a fresh, comprehensive same-condition validation of the original active-F1 transfer model.

## New public datasets and what they constrain

| Primary dataset | Acquired and checked | Useful constraint | Boundary |
|---|---|---|---|
| [Ghosh et al. 2025](https://doi.org/10.1038/s41467-025-63656-z), [EDMOND data](https://doi.org/10.17617/3.G6KSU2) | 77 representative hammerhead-cleavage points and seven phase-composition rows | Catalyst-species partition can be compared with catalytic function across peptide coacervates | Concentrations use charge equivalents; fluorescent RNA amount is not active fraction; pellet contains both phases. Different chemistry from R3C/POPC. |
| [Le Vay et al. 2023](https://elifesciences.org/articles/83543) | 16 active/inactive-system exchange rows | Reaction-dependent concatenation changes population mixing | Labels track substrate/concatemer rather than catalytic RNA; fusion and diffusion are confounded. |
| [Ameta et al. 2021](https://doi.org/10.1038/s41467-021-21000-1) | 1,837 network compositions and 20,039 droplet records; measured/model tables separated | Noncovalent background assembly can erase memory of initial covalent catalyst composition | Droplet barcodes identify samples, not multigeneration physical parent–daughter pedigrees. |
| [Mizuuchi et al. 2022](https://doi.org/10.1038/s41467-022-29113-x) | Clone/genotype data and 182 functional-replication entries, including a preserved missing-value label | Links inherited RNA sequence variants to different replication interactions | Requires encoded Qβ protein replicase and supplied translation machinery; no active-R3C retention coefficient. |
| [Gianni et al. 2026, QT45](https://doi.org/10.1126/science.adt2760), [Zenodo](https://doi.org/10.5281/zenodo.13891380) | Fidelity archive, 14 FASTA files; integrity and inventory verified | Separates copied sequence, newly produced RNA and functional-product assays | Fidelity not re-estimated here. Separate low-yield strand-synthesis reactions, external interventions and no compartment inheritance assay. |

These data constrain model structure and future measurements. They are not interchangeable numerical calibration sets. In particular, the hammerhead coacervate study shows why sequestration cannot be assumed to preserve catalysis, and the Azoarcus network study shows why regeneration cannot be assumed to preserve a distinct inherited state.

Two close membrane studies remain useful with limitations. [DasGupta et al.](https://doi.org/10.1002/chem.202301376) measure retention of the ligase species and separately test activity, but the retention and activity assays use different buffer concentrations and a fluorophore changes activity. [Peter et al.](https://doi.org/10.1002/anie.202218507) use internal coacervates to aid exchange/retention in vesicles, but their modified ligation product is inactive. Neither supplies the missing active, self-regenerated descendant measurement. The [Lai sequence/activity dataset](https://doi.org/10.1073/pnas.2025054118) was reviewed; Dryad numeric downloads failed with HTTP401/403 and are not claimed as analyzed.

Source URLs, download hashes, conditions, missing data and access failures are retained in the [retention report](sources/retention/REPORT.md) and [inheritance report](sources/inheritance/REPORT.md). This is a targeted review, not an exhaustive literature census.

## What still needs measurement

The fluorescent PAGE observer is `P/(R+P)` (including an inaccessible reporter reservoir in models that use it). A common loss of all fluorescent material can leave this ratio unchanged. Kinetic assumptions may indirectly constrain loss, but the ratio is not an absolute recovery measurement. Likewise, population measurements contain no parent identities and cannot recover a physical pedigree by better fitting alone.

To discriminate the remaining chemistry hypotheses, the next data should vary B independently of F1 and Hyper-A, resolve early reaction times, and measure active F1 as well as fluorescent product. Those observations would separate substrate occupancy, precursor-assisted ligation, nonproductive complex formation and loss of activity more effectively than another fit to the same reporter curves. Matched bulk/GUV measurements immediately after cycling and after warm incubation would also separate chemistry during freeze–thaw from subsequent catalysis. These are proposed measurements, not experiments performed here.

The decisive experiment should measure inside/outside original and newly formed F1, then directly assay their catalytic activity after recovery. In parallel, track compartment volume, parent–daughter identity and horizontal exchange. Vary parent composition at fixed feed composition, using inactive-catalyst, founder-only, no-regeneration and shuffled-parent controls. That design distinguishes renewed chemistry from maintenance of an inherited functional state.

## Verification and disposition

The complete offline suite passed **10 model tests**, **14 numerical artifact comparisons**, the **529-row source extraction** and its independent **148-value prior-data comparison**, **16 retention-data checks** and **23 inheritance-data checks**. A separate saved-parameter replay reproduced all **216 predictions exactly**. The full independent refit repeated model selection, fits, profiles, transport, controls and sensitivity; only elapsed time was excluded when comparing scientific JSON. All 71 recorded inputs and 264 non-cache files in the preceding laboratory remained unchanged. [Verification receipt](verification-v1/verification.json); [commands and scope](checks.md).

The first numerical attempt is preserved after an output-serialization failure. Its repair only converts the observer scalar to a native Python float; candidate definitions, fitting budgets and criteria stayed frozen. The completed run is `model/results-v2`. Five chemical-fit artifacts match the first attempt byte-for-byte, and common numerical outputs differ by less than 10⁻⁸ pp. [Repair record](model/RUN_REPAIR.md).

The [independent review](review-independent.md) approves the bounded computational investigation with no blockers. Its two low-priority notes concern future unresolved-score plotting and interface annotations; neither changes these completed results. **Do not adopt this revision as a validated physical replacement.** It documents which small chemical changes were insufficient and which additional measurements are needed to identify a defensible model.

No wet experiments, author correspondence or full sequencing reanalysis were performed. Inaccessible source files and incompatible chemical conditions remain explicit in the ledgers.
