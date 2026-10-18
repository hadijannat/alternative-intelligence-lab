# Fe-site observations: fixed conditional-current test

Full objective remains the original Mo34WV plus missing functions for a maintained, inherited and intelligent system. Exact target identity and all12integrated requirements remain unverified. Previous goal turn is progress: new KTiOPO4 primary evidence and executed observation checks changed the functional-carrier assessment. This step follows the identified public Fe-site assay lead; it does not redefine the full goal as an electrochemical fit.

## Exposure and primary source

DOI10.1021/acscatal.2c03898, SI Figshare21509957/file38122559. One public11page PDF, not raw numeric data. The source auditors have viewed figures to audit methods/series and are response-exposed, but no numerical response points have been extracted, fitted or communicated. Root knows qualitative article conclusions and the methods, cycle labels and axes only. This is a retrospective, paper-informed analysis of figure-derived data; no prospective/blinded or independent-specimen validation is claimed.

FigS8 contains cycles1–7. Panel a provides current density in mA/cm2 versus potential; panel d provides reported Fe density in10^-9mol/cm2 and TOF. Native Methods define an electron-charge-based redox count and TOF using current divided by four times charge. In molar units the density proxy corresponds to areal charge `Q/A=F*n_mol/A`, not elementary charge times moles. Panel c cannot supply independently reintegrated charge without a qualified scan rate/window/background; S8 does not specify these completely. Do not silently transfer another figure's scan rate.

## Fixed extraction and split

1. Verify native SI DOI/title/file integrity, formats, geometry/current normalization, carbon support/binder and source-reference errors. Preserve absence of main full text or raw files rather than inventing Methods.
2. Extract seven current densities at E=1.52V_RHE from **panel a**, using native vector curve/legend associations if available. Match cycles by explicit legend, never by activity rank or best fit. For multiple intersections use the rising-potential branch only if documented; otherwise retain the full intersection interval and midpoint nominal value, without choosing a favorable branch.
3. Extract seven Fe-density points from the **left axis of panel d**. Use them as a reported derived-charge proxy; do not claim independent replication of its integration/background correction. **Do not reconstruct current from n×TOF**, and do not fit the TOF curve as an independent response.
4. Cycle1 supplies baseline j1,n1. Fit using cycles2,3,4 only; reserve cycles5,6,7. Baseline values and extraction uncertainties remain shared, not extra independent samples. Reserved Fe density is a measured input to conditional current prediction, not a forecast of density evolution. No random point split or adjustment after reserved outcomes.
5. Save points, path/legend metadata, axis calibration and extraction uncertainty/ambiguities before fitting. Native vector stroke/marker resolution is a digitization limit, not a measurement CI. If source branches/normalization or error bars are not recoverable, retain that limitation explicitly. No absent errors become zero experimental uncertainty.

## Models and fixed evaluator

Let `Delta n = (n_c - n1)*10^-9 mol/cm2`, `Delta j = (j_c-j1)*10^-3 A/cm2`, and F=96485.33212C/mol.

- M0: `Delta j = 4*F*k*Delta n`, k≥0. Fit the single apparent competence parameter by constrained least squares on cycles2–4. It tests whether added current is proportional to added reported redox-accessible Fe under a fixed host baseline.
- M1: `Delta j = 4*F*k*exp(gamma*(c-1)/3)*Delta n`. Fix gamma to1001 evenly spaced values from−ln(10) to+ln(10). Solve k≥0 analytically for each gamma using training only, select minimum SSE. M0 is included at gamma0. This is a two-parameter empirical changing-competence diagnostic, not an identified chemical reaction or material-origin model. Record boundary solutions and training-equivalent ambiguity.
- B1: constant j1. B4: constant final-training current j4. Neither is a universal maximum founder activity; founders can change state.

For all models report individual residuals, training/reserved RMSE, and reserved normalized RMSE=`RMSE/sqrt(mean(j_observed^2))`. Operational screen: normalized RMSE≤0.10 and every reserved error divided by max(|j_observed|,0.1mA/cm2)≤0.20. Both required. These are analyst tolerances, not a statistical confidence test. No new comparator, parameter bounds or scan assumptions are added to rescue a failure.

Retain digitization sensitivity separately: perturb the seven nominal current and density readings over their documented extraction intervals, including shared baseline, and report a deterministic envelope if tractable. A numerical sampling of that box is not an exhaustive bound or experimental confidence interval. Do not select extracted branches or offsets against fit success.

## Causality, origin and full-system limits

This assay observes total redox-accessible Fe and total electrochemical current. An apparent per-site coefficient need not be an individual Fe site's OER turnover: Ni background, redox accessibility, morphology and assay-induced restructuring can vary. Shared-quantity coupling in n and TOF must remain explicit. Check algebraically/numerically that `n=F_old+F_new` and current depending on their equal-competence sum cannot identify origin partitions without an origin-specific functional observation or valid founder ceiling. Do not turn a successful total-current prediction into active new-material repair.

The source uses carbon black, Nafion and glassy carbon. It is an assay/mechanism comparator, not a verified noncarbon integrated complement. Adsorption activation is not automatically damage repair. No Fe-site coefficient transfers to Ni felt, Ni wire, PMo12 or Mo34WV without matching measurements. No full gas/Faradaic balance, isotope lineage, serial inheritance, cognition or target integration is inferred.

Completion: native acquisition/audit, reproducible extraction, executed frozen models and checks, negative-result ledger, independent review, report/checks/progress. Check units, charge conversion, analytic least-squares limits, M0 nesting, synthetic recovery, fit-mask separation and origin-sum invariance. Preserve every source/access/extraction/model failure. No wet-lab experiment or full-goal completion is claimed.
