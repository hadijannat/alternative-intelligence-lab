# Salibi RNA mechanism and source-data audit

The previous model fails its **bulk kinetic calibration before membrane transport is involved**. Replaying its retained parameters against the independently reread workbook reproduces 7.866012 percentage-point RMSE. Its numerical source extraction is correct: all 148 previous observations match the cited cells. The problem established by this audit is the kinetic model's dose/time shape, plus unmeasured transport assumptions. A specific physical cause remains to be tested.

This audit owns only this source directory. It does not fit a revised model or modify the previous laboratory. The data have been inspected; a future split of these data is retrospective cross-validation, not a blinded experimental test.

## Evidence and reproduction

Run from the workspace root:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-mechanism-2026-10-15/sources/salibi/extract.py
```

`verification.json` records 529 exact new numerical cell checks, 148 prior extraction checks, unchanged hashes for 269 existing laboratory files, and successful replay of the 40 bulk predictions. `observations.csv` includes the sheet and cell for every value, units, conditions, and whether it was used previously. `v1_calibration_residuals.csv` records the actual replay, with no refitting.

The shared pyenv installation's SciPy 1.15.3 failed to import because its `_spropack` Mach-O binary has an invalid thread-bss offset. The command above uses the already cached isolated SciPy 1.16.1 runtime. No shared installation was repaired or altered. The replay exactly reproduces the original aggregate RMSE in that runtime.

Primary source: [Salibi et al. 2023](https://doi.org/10.1038/s41467-023-36940-z), [source workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-36940-z/MediaObjects/41467_2023_36940_MOESM8_ESM.xlsx), [SI](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-36940-z/MediaObjects/41467_2023_36940_MOESM1_ESM.pdf). The retained workbook SHA256 is `d39d7b0b9a30091fe848e1bb12737030da043025a5b96ab54b577444f37b7fc7`.

## Demonstrated model discrepancies

| Source coordinate | Condition | Observed reporter % | Old prediction % | Error, percentage points |
|---|---|---:|---:|---:|
| S13 L8 | F1 0.5 µM, 30 minutes | 81.30633 | 68.16908 | -13.13725 |
| S13 O7 | F1 1 µM, 15 minutes | 81.55033 | 68.15510 | -13.39523 |
| S13 T10 | Hyper-A 1 µM, 60 minutes | 14.40133 | 0.96083 | -13.44050 |
| S13 AC10 | Hyper-A 2.5 µM, 60 minutes | 59.73033 | 78.97443 | +19.24410 |

The F1-only series contains no active substrate Hyper-A, so these errors cannot be assigned to autocatalytic production or membrane retention. The model treats both substrates as unsaturated factors in `k*F*R*B`. Reporter ligation consumes B from 7.5 µM toward about 2.7 µM in high-yield conditions, enforcing a strong decline in the B-dependent rate. A saturating B occupancy factor is a plausible alternative, not a demonstrated unique cause.

In the Hyper-A series, the model permits reporter formation only after an assumed `kb*A²*B²` route first makes F1. It misses early low-dose reporter production and then overshoots high-dose endpoints. That pattern argues against rescuing the old model by changing one transport parameter. The fitted inhibition concentration reaches its 1000 µM upper bound, far above observed concentrations. This fit provides no affirmative evidence for the imposed product-inhibition denominator.

No mismatched percent/fraction conversion, micromolar unit error, substituted active reporter, or duplicate S13d endpoint was found. S13 contains summary means, SD and n=3, not the underlying three replicate values. Zeros at t=0 are real supplied summaries. S13 negative controls at 0 and 60 minutes were unused previously and both equal zero.

## Chemical interpretation

Hyper-A is a 52-nt active precursor; B supplies the complementary fragment. Full-length F1 is catalytic. Cy5-A has the G38A substitution and its ligated Cy5-F1 product is inactive. Consequently, a fluorescent product trace reports ligation and does not directly measure the amount, folding state, or retained catalytic activity of new F1. The paper's estimate of newly made active material uses additional equivalence assumptions about reporter and active substrates.

The physically motivated reaction sequence is substrate association, ligation, then product-complex dissociation. A+B association can also sequester substrates off the productive path. [Ferretti and Joyce 2013](https://doi.org/10.1021/bi301646n) analyze these distinctions for related R3C enzymes. [Robertson and Joyce 2014](https://doi.org/10.1016/j.chembiol.2013.12.004) study optimized F1 and distinguish improved catalytic turnover from product release and substrate sequestration. These primary papers motivate topology; their microscopic rate constants are not Salibi's 42 °C, 20 mM MgCl2, 900 mM sucrose calibration.

Salibi SI Figure 11 is a proposed 2A2B secondary structure, **not a measured fourth-order rate law**. Its existence does not establish that every such complex is productive. SI Figure 13b explicitly depicts Hyper-A as the catalyst in a cycle ligating Cy5-A and B; the image was inspected directly and is retained as `SI13-page17.png`. A direct effective Hyper-A-assisted reporter route therefore follows the authors' proposed topology. Its exact concentration order and transient molecular state are not measured, and the reporter trace alone does not independently quantify how much Hyper-A first becomes F1. Likewise, a common reactive-substrate fraction can model a plateau but is not an experimentally determined inactive fraction. These additions need prediction checks and parameter identifiability analysis rather than mechanistic certainty from a better fit.

The F1 concentration series can constrain an effective rate response; the Hyper-A concentration series can constrain the shape of delayed initiation. They do not independently identify every association, dissociation, ligation, inactivation, and leakage rate. A model with all these elementary rates freely fitted would exceed the information in the data. Whole-dose-group cross-validation is more informative than randomly withholding points from each fitted curve.

## Additional numerical data and their limits

| Sheet | Exact export | Appropriate use | Limit |
|---|---:|---|---|
| S13 negative | 2 summaries | Same-condition structural zero check | Trivial zero baseline, not a strong independent kinetic challenge |
| S12 | 126 replicate values | Distinguish active-precursor propagation from inactive-product dilution | 30-minute bulk cycles; sucrose not stated; half-generation observer ambiguity |
| S15 | 18 replicate values | Challenge membrane-independent activity assumption | Different substrate concentrations; possible 2× post-addition dilution; sucrose not stated |
| S18 | 48 replicate values | Challenge zero chemistry during the cycling interval | Bulk, 10+10-minute FT protocol, versus GUV 5+5 minutes; sucrose not stated |
| S9 | 102 histogram values + 3 summaries | Fluorescent tracer content-loss proxy | Atto655-(CA)13, not F1 activity; no paired before/after objects |
| S17 | 82 histogram values | GUV fragmentation/size-distribution constraint | Fluorescent dye assay, no catalytic cargo or paired parent/daughter identity |

The rest of the 529 rows re-extract the 148 already used Figure 2, Figure 3 and S13 observations. Full recipes and incompatibilities are in `conditions.json`; no source rates or retention factors have been silently pooled.

S9 gives an ensemble mean intensity ratio of 0.781951 after one FT. Applying that as an active-F1 survival probability would confound tracer concentration, sampling, compartment volume, fluorophore effects, and catalytic competence. S17 independently demonstrates that size changes occur, making unchanged-volume concentration assumptions especially important to test. Neither histogram can identify individual compartment ancestry.

S18's three-cycle bulk means are approximately 18.21% reporter without initial F1 and 18.14% with F1 before the additional 42 °C stage. That is not zero, but these longer cycles and bulk conditions cannot calibrate the GUV cycling interval directly. S15's mean reporter yields are 22.72%, 38.57%, and 41.98% for increasing GUV suspension fraction; they motivate a membrane-effect challenge while remaining insufficient to identify an intravesicular correction factor.

S12 has a specific unresolved observer issue: in the unseeded Hyper-A arm, the first endpoint mean is 59.483%, while the published next half-generation mean is 15.002%. An instantaneous 10-fold transfer into an identical fresh labelled-substrate concentration would predict 5.9483% before further reaction. Possibilities include reaction before the nominal initial sample, gel/background normalization, or recipe details. These are hypotheses, not demonstrated experimental errors. Preserve the values and do not tune a chemical model to the discrepancy without clarification. Actual terminal zeros are retained exactly; they are not silently recoded as missing.

## What remains unmeasured

The existing GUV assay constrains population ligation after mixing, loss, warming, sampling and washing. It does not separately constrain species-specific retention of active F1, its post-cycle active fraction, Hyper-A/Cy5-A relative ligation efficiencies inside GUVs, or de novo catalyst activity in identified daughter compartments. Functional inheritance requires direct active-catalyst assays and compartment identity tracking, with founder carryover and horizontal transfer separated. These quantities cannot be recovered merely by improving a bulk-curve fit.

Online searches reached the primary Robertson and Ferretti records and indexed primary text. Direct Europe PMC full-text XML acquisition returned HTTP 500 for both; `mechanism_retrieval.json` preserves those failures. No unavailable supplementary measurement or digitized curve is claimed as acquired.
