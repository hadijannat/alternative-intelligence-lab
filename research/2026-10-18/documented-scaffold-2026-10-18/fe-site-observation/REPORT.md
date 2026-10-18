# Fe-redox counting adds an observation, but does not identify repaired material

The Qian2022 source adds a useful observable missing from the earlier voltage-only model: a reported Fe-redox density alongside separate current curves. A frozen test finds a nominal constant-competence relationship that predicts later figure midpoints, but that result is not robust to the public figure's resolution and extraction ambiguity. No new-material functional contribution, universal founder activity ceiling or verified integrated complement is established.

The original Mo34WV-plus-complements objective and all12requirements remain intact. This is an assay/model assessment toward R, not a replacement of the goal with an electrode fit. Exact Mo34WV identity, functional heredity and same-system integration remain unverified.

## Primary source and actual data boundary

Haitao Qian et al., [*In Situ Quantification of the Active Sites, Turnover Frequency, and Stability of Ni–Fe (Oxy)hydroxides for the Oxygen Evolution Reaction*](https://doi.org/10.1021/acscatal.2c03898), ACS Catalysis12 (2022),14280–14289. The native [public SI](https://ndownloader.figshare.com/files/38122559) is the sole file in [publisher Figshare record21509957](https://acs.figshare.com/articles/journal_contribution/In_Situ_Quantification_of_the_Active_Sites_Turnover_Frequency_and_Stability_of_Ni_Fe_Oxy_hydroxides_for_the_Oxygen_Evolution_Reaction/21509957), 644572bytes and11pages, with matching deposited MD5 and saved SHA256. [Source audit](<SOURCE_AUDIT.md>) records rights, routes, methods and limitations. Main-body acquisition returned403; an author institutional bibliography confirms identity but supplies no manuscript. No raw numeric trace, spreadsheet or analysis code is deposited in this record.

SI FigureS8 follows seven cycling labels in1M KOH plus2µM Fe3+, from−0.4 to1.6V versus RHE. Panel a contains separate current-density curves; panel d contains a derived Fe-density proxy and TOF. Methods count Fe using corrected reduction charge, assuming one electron per accessible Fe. The axis is mol/cm2, so its areal charge conversion uses **Faraday's constant**, not elementary charge times moles.

The source's apparent TOF is current divided by four times that same redox charge. Density and TOF therefore cannot be treated as independent confirmations. Here the response comes only from panel a at1.52V. Panel d's left-axis density is an input proxy; the TOF bars are never used to reconstruct current or fit a response. S8's scan rate, exact integration window and background uncertainty are not fully specified, so independent redox reintegration is not claimed. The source refers toS6 for a pure-Ni background that is actually pictured inS5.

## Extraction limitations govern interpretation

The PDF embeds FigureS8 as a **540×412 JPEG**, with no vector curves. [The extractor](<extract_figS8.py>), native/annotated pixels (dependency not included: `documented-scaffold-2026-10-18/fe-site-observation/data/figS8_calibration.png`), [point provenance](<data/point_provenance.csv>) and [seven-row table](<data/figS8_points.json>) preserve the reading process. The current curves merge into only **four distinguishable color groups**: cycles1/2,3/4 and6/7 share broad color-compatible intervals; cycle5 is separate. Sweep branches are not labeled. No response ranking or fit was used to invent distinct values for the ambiguous pairs.

Nominal currents are interval midpoints, not seven resolved raw measurements. The bounds include the horizontal calibration band because the steep OER slope amplifies a one-pixel horizontal error. Density points are more readable, but baseline cycle1 has overlapping symbols and a wider interval. These are deliberately loose manual extraction envelopes, not experimental error bars, likelihoods or confidence intervals. Shared colors, axes and baseline induce correlations that the independent interval box does not model.

Two extraction failures were caught before fitting: a floating-point self-check and preliminary current envelopes too narrow for the declared horizontal pixel band. They remain in `extraction_failures.txt`; source data and evaluator were not adjusted to obtain a model pass.

## Predeclared test and observed result

[The protocol](<PROTOCOL.md>) fixes cycle1 as baseline, cycles2–4 for fitting, and cycles5–7 as reserved responses. Qualitative source conclusions were already known; the extraction agent is response-exposed. This is retrospective, paper-informed conditional prediction from a published figure. Reserved Fe density is supplied as an observation, so density evolution itself is not forecast.

M0 fits added current proportional to added redox-accessible Fe density with a fixed host baseline. M1 adds an exponential cycle-dependent competence coefficient. It is an empirical two-parameter diagnostic, not an identified chemical mechanism. Both models constrain the apparent scale k to be nonnegative; M1 gamma ranges from −ln(10) to +ln(10). M0 is nested in M1. B1 andB4 carry forward the baseline or last training current, respectively. They do not bound adaptive founder activity.

The fixed operational screen requires normalized RMSE≤10% and maximum fractional error≤20%. At nominal raster midpoints:

| Model | Early-cycle normalized RMSE | Reserved RMSE,mA/cm2 | Reserved normalized RMSE | Reserved maximum fractional error | Nominal reserved screen |
|---|---:|---:|---:|---:|---|
|M0 constant incremental competence|about13.6%|1.485|3.93%|5.40%|Pass|
|M1 changing incremental competence|about10.7%|14.032|37.13%|43.81%|Fail|
|B1 constant cycle1 current|—|19.363|51.24%|52.78%|Fail|
|B4 constant cycle4 current|—|10.393|27.50%|29.63%|Fail|

Both fitted models already exceed the10% normalized-error criterion during calibration. A later nominal pass does not establish a correct mechanism. M1 has smaller training SSE but worse reserved predictions; no parameter range, extraction point or model was changed after those outcomes. The fitted coefficients are apparent incremental response parameters under host/background assumptions, not measured intrinsic Fe-site turnover constants.

All16384corners of the deliberately independent14-dimensional extraction box were then evaluated with training-only refitting. M0 passes848corners and fails the others; M1 passes554and fails the others. B1 passes1024. These counts are **not probabilities, independent replicates or likelihoods**. The broad ranges prevent a decisive preference between constant and changing competence from this public raster alone.

B4 has no passing corner, which does not reject the model throughout the continuous box. As a post-hoc illustration,35mA/cm2 lies inside each interval for cycles4–7; assigning that value to those four entries makes B4's reserved error zero inside the loose box. This hypothetical interior is not a new extraction or an observed current trajectory, and source correlations could exclude it. It demonstrates why corner evaluation cannot certify a continuous bound. No nominal data or reported fit was replaced by it.

![Figure-derived conditional current test](<results/models.png>)

[Machine-readable results](<results/models.json>) retain every nominal prediction/residual, exact fit parameters, sensitivity summaries, origin witness and frozen-input hashes. [The implementation](<test_models.py>) checks molar/charge units, synthetic recovery, zero/leverage limits, nesting and exclusion of reserved current **and** density from fitting. Numerical checks passed; scientific inference remains qualified by the data.

## Why origin-specific repair is still unidentifiable

Two measurements can improve state estimation without identifying atom age. If redox density observes `N_old+N_new`, and shared catalytic coefficients make current depend on the same sum, different origin partitions remain indistinguishable. The executed finite-inventory witness uses identical initial pools and two hypothetical mechanisms: exposing previously inaccessible founder Fe versus adding fresh Fe to the accessible population. Both conserve each origin, give identical total count/charge/current and end with different origin-specific accessible populations. This is a conditional mathematical counterexample, not an estimate of what happened in Qian's electrode.

The source does not supply the initial founder inventory/functional upper bound needed to exclude such alternatives. Current can also change through Ni activity, background subtraction, morphology, redox accessibility or restructuring during the wide diagnostic scan. A redox-visible Fe atom is not automatically a proven OER-active atom. The SI does not provide matched gas/Faradaic-efficiency or origin-specific product measurements for these cycles.

Adsorption activation on retained Ni material is not automatically damage repair. The measured electrode contains Vulcan carbon black, Nafion and glassy carbon as functional components. It is an assay comparator, not an admitted noncarbon complement. A coefficient from this preparation cannot be transferred to bare Ni wire, Ni felt, PMo12 or hypothetical Mo34WV. No same-medium coupled test is supplied.

## Recursive decision

Retain **Fe-redox charge plus independently read current** as a better observation design than voltage alone. Reject circular current reconstruction from density×TOF as independent validation. Leave per-site activity selection and new-material repair unresolved under the acquired data; preserve the nominal M0 success, M1 failure, calibration errors and uncertainty reversals together. No full-system function is closed and no integrated complement is added.

The next discriminating evidence is native matched current/redox data with an explicit scan/background protocol and same-preparation controls, followed by origin-resolved functional attribution. An additional public lead, DOI10.1021/acscatal.6c01228, concerns dissolution detection/accumulation controls and was only abstract-screened previously. Its SI is not acquired here; any next step must first verify its actual observations and source access. Neither another fitted rate nor an undetected dissolution signal supplies missing functional heredity or exact target identity.

This turn is **progress**: a new primary assay is acquired, a noncircular conditional test is executed, and the public data's resolving power changes the next action. The full original objective remains active and unachieved.
