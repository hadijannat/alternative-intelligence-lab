# Remaining RNA transport failure: source and residual audit

The saved `independent_inactivation` transport failure is reproduced exactly. The strongest discrepancy is the disappearance of seed-dependent behavior in the model: by generation 7 it predicts practically the same yield for seeds 0, 1, and 2 µM, whereas observed means remain 2.133%, 4.591%, and 11.961%. No initial-mixture, dilution-count, unit, or incubation-clock implementation mistake was found in the audited baseline. The source does not identify the transport and active-catalyst assumptions needed to assign this failure uniquely to membrane exchange, content loss, or chemistry.

The [audit script](audit.py) independently checks 108 Figure 2/3 observations and metadata against source-workbook cells, reproduces all 216 saved predictions and every saved trajectory value with maximum difference **0**, verifies the original calibration/benchmark separation, and checks moiety balance (maximum error **5.01×10⁻¹⁵ µM**). The 14 [input hashes](input_hashes.json) remain unchanged. [Verification](verification.json) records the pinned runtime and output hashes. No parameter was fitted in this audit. Figures 2/3 have already been inspected, so the benchmark is untuned retrospective evaluation, not fresh experimental validation.

## Residual structure

Errors below are prediction minus the mean of three source replicates, in percentage points. RMSE by seed uses the individual positive-time observations: nine per Figure 2 seed and 21 per Figure 3 seed. Structural zeros are excluded. [Every condition and its SD](residuals_by_condition.csv) and [seed summaries](dynamic_residuals_by_seed.csv) are retained.

| Figure / seed µM | Fractional RMSE | Fractional bias | Contact RMSE | Contact bias |
|---|---:|---:|---:|---:|
| 2 / 0 | 1.432 | +1.336 | 1.277 | +1.224 |
| 2 / 1 | 1.396 | −0.997 | 1.007 | −0.606 |
| 2 / 2 | 5.922 | −5.706 | 6.524 | −6.418 |
| 3 / 0 | 2.151 | +1.947 | 1.347 | +1.029 |
| 3 / 1 | 1.499 | −0.715 | 2.128 | −1.459 |
| 3 / 2 | 6.848 | −6.316 | 7.763 | −7.330 |

The calibrated arms already show a compromise: both closures overpredict zero-seed background and underpredict the seeded first FT response. Increasing one common rate or mixing scalar therefore cannot be assumed to solve both errors.

| Figure 2 seed | FT count | Observed mean % | Fractional error | Contact error |
|---|---:|---:|---:|---:|
| 0 | 1 | 0.284 | +0.734 | +1.338 |
| 0 | 2 | 0.585 | +1.631 | +1.420 |
| 0 | 3 | 0.823 | +1.643 | +0.915 |
| 1 | 1 | 4.082 | −2.007 | −1.268 |
| 1 | 2 | 5.437 | −0.684 | −0.374 |
| 1 | 3 | 6.554 | −0.300 | −0.175 |
| 2 | 1 | 10.238 | −7.372 | −7.326 |
| 2 | 2 | 12.344 | −5.795 | −6.742 |
| 2 | 3 | 12.943 | −3.950 | −5.184 |

The high-seed serial arm shows the failure developing after the first generation. Its errors do not resemble a constant observer offset.

| Generation, seed 2 µM | Observed mean % | Fractional prediction % | Fractional error | Contact prediction % | Contact error |
|---|---:|---:|---:|---:|---:|
| 1 | 10.115 | 8.993 | −1.122 | 7.759 | −2.356 |
| 2 | 12.300 | 7.060 | −5.239 | 5.954 | −6.345 |
| 3 | 11.442 | 5.209 | −6.233 | 4.213 | −7.229 |
| 4 | 12.092 | 4.450 | −7.641 | 3.497 | −8.595 |
| 5 | 13.413 | 4.206 | −9.207 | 3.266 | −10.147 |
| 6 | 11.058 | 4.136 | −6.922 | 3.199 | −7.859 |
| 7 | 11.961 | 4.117 | −7.844 | 3.181 | −8.780 |

At G7, the model's three seed arms span only 0.00828 pp under fractional mixing or 0.00791 pp under contact mixing; the observed span is 9.82833 pp. Active F1 converges to approximately 0.012337 µM or 0.008630 µM, respectively. Disabling new active-F1 production yields only 0.859–0.867% or 0.449–0.457% reporter at G7; this computational ablation shows that the model includes regeneration, yet its regeneration does not preserve the measured seed separation. It is not a new experimental ablation.

Figure 2 FT3 and Figure 3 G1 have identical nominal inputs and sequence in the model and exactly equal predictions. Their observed means differ by +1.050, −1.320, and −2.828 pp for seeds 0, 1, and 2 respectively (Figure 3 minus Figure 2). Combined descriptive SDs are 0.664, 1.596, and 1.369 pp. These differences expose independent-experiment variation or unrecorded preparation effects; they do not justify fitting dataset-specific offsets. SD comparisons are descriptive, not p values, and the source does not establish all covariance or systematic-error terms.

## Source conditions and what the implementation actually assumes

The primary record is [Salibi et al.](https://www.nature.com/articles/s41467-023-36940-z), with retained [article text](../../measured-coupling-2026-10-15/rna_sources/raw/salibi.txt), [SI](../../measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt), and [workbook](../../measured-coupling-2026-10-15/rna_sources/raw/salibi_data.xlsx). Local source line references below refer to these hashed files. An online search reached the primary article; direct initial open encountered the publisher login redirect. Numerical evidence was read from the local workbook, not scraped from plots.

| Quantity | Source and baseline interpretation | Audit finding |
|---|---|---|
| Initial mixture | Article Methods, lines 107/111: equal seed, A, B GUV preparations | Three cohort weights 1/3; local contents F1=seed, A=10 plus Cy5-A=2.5, B=15 µM. Correct nominal recipe; equal internal-volume weights remain a closure. |
| Fresh feed | Article line 111: half previous suspension plus equal-volume fresh A/B feed | Old cohort weights ×0.5; new A and B weights each 0.25. No F1 feed. Correct nominal volume schedule. |
| Transfer count | G0 before incubation; G1 follows first FT/incubation; subsequent generations fed | G7 has seven 60-min incubations and six half-volume transfers. No extra pre-G1 dilution. |
| FT and incubation | Article lines 107/111; Figure 3 caption | Figure 2: n consecutive FT then one 60-min incubation. Figure 3: three FT then one 60-min incubation per generation. Correct sequencing. |
| Content loss | Article line 45; SI lines 396–404 | Approximately 45% loss after three FT inferred from gels. SI notes 20% extra sample volume loaded per additional FT; this loading correction is not an independent species-specific retention measurement. |
| Recoverable observable | Article lines 89–91 and Figure 2 description | Samples washed to remove leaked molecules, lysed, heat-denatured, and PAGE analyzed. Ratio counts recovered labelled product relative to all recovered reporter strands, including carried product. |
| Additional retention proxy | SI lines 294–299 | S9 uses Atto655-(CA)13 tracer, not F1; its microscopy protocol and fluorophore/cargo differ. It cannot supply active-F1 survival. |
| Thermal comparison | SI S18, lines 573–581 | Bulk experiment uses 10+10-min FT, with optional 60 min at 42 °C. It cannot calibrate the GUV 5+5-min FT clock directly. |

The baseline population means at G0 are A=3.333, Cy5-A=0.833, B=5, F1=seed/3 µM. Each later feed adds 2.5, 0.625, and 3.75 µM of A, reporter, and B in the fixed total-volume convention, after halving old inventory. Under equal 0.55 retention, total reporter follows `Rtot[g]=0.55*(0.5*Rtot[g−1]+0.625)` after G1. Its limit is 0.474138 µM. The corresponding supplied A-plus-reporter moiety tends to 2.370690 µM, close to the paper's approximate 2.4 µM bookkeeping estimate. Agreement validates this nominal accounting, not local concentrations or catalyst activity.

Fifty-five percent belongs to **three FT**, not each FT and not the serial-transfer step. The implemented per-FT factor is `0.55^(1/3)=0.819321`; applying 0.55 per FT would incorrectly leave 0.166375 after three cycles. The cube-root law assumes identical multiplicative loss per cycle. Neither active-F1 retention nor differential product/fragment loss is measured. RNA quantity retention also differs from retained catalytic competence.

Both transport closures conserve the weighted pre-loss inventory. Fractional transport moves every cohort partway toward the population mean; contact transport leaves a fraction unchanged and introduces a mixed cohort. Neither represents measured encounter pairs, vesicle size changes, or tracked daughters. The G7 cohort counts (15 fractional, 36 contact) are numerical mixture components, not observed vesicle counts. Equal preparation volumes need not imply equal internal aqueous volumes, particularly after fragmentation, pelleting and sampling.

The 55% loss operator scales every local concentration. A synthetic check exposes the assumption: starting from the same homogeneous mixture, uniform concentration thinning versus complete content loss in 45% of equal-volume cohorts leaves exactly the same total inventory, but the unchanged chemistry predicts 90.982% versus 99.957% reporter after 60 min. This is an identifiability counterexample, not evidence that either map describes the experiment. Aggregate loss cannot determine the spatial distribution that drives nonlinear reactions.

## Activity clock and reporter interpretation

The selected fitted inactivation coefficient is 0.01294667 min⁻¹, corresponding to a model half-life of 53.539 min and active fraction 0.459875 after each 60-min reaction. The baseline applies it only during the 42 °C incubation. One generation contains an additional 30 minutes of freeze/thaw. Extending the same coefficient to that interval would impose an extra factor 0.678141 without source support; frozen, thawing and warm-stage rates require separate evidence. Treating the entire 90 minutes as 42 °C reaction time is also unsupported. A source-motivated zero-FT-chemistry approximation is not proof that all FT-period catalysis or deactivation is exactly zero.

After G1, founder active F1 decreases per generation by `0.5*0.55*exp(−60 kd)=0.126466` in this model. At G7, the 2-µM seed leaves 6.898×10⁻⁷ µM active founder. This number depends on the inherited effective inactivation law and equal retention; it is not measured founder survival. Reversible sequestration could explain an apparent activity decline without destroying all future catalytic availability. If complexes gain different survival or protection, this analytic founder formula ceases to apply. If every competent F1 strand instead has exactly the same irreversible hazard whether free or bound, all cargo shares retention, and there is no reactivation, the formula remains valid for **total competent founder** in expectation. Subtract it from total competent F1, never free F1 alone; check that a two-F1 complex loses competence per constituent rather than losing both at an incorrectly doubled whole-complex hazard.

Cy5-A contains the inactivating mutation; Cy5-F1 is the inactive labelled ligation product. The measured reporter fraction does not directly count active new F1. In the selected model, active and reporter ligation rates are explicitly independent (`ka=0.0157193` versus `kf=0.1470062`), so multiplying a reporter yield by the unlabelled precursor inventory does not recover its predicted new active-F1 pool. The paper's approximate 0.3 µM estimate makes additional reporter-to-active-product equivalence assumptions; it is not an independent observed target for this model.

For a finite-complex model, count all labelled strands in the denominator, and only covalently ligated labelled strands in the numerator. Denaturing PAGE releases product held in a catalyst–product complex. A preligation catalyst–reporter–B complex contributes unligated reporter; a postligation F1·Cy5-F1 complex contributes labelled product. Both contain one unlabelled F1 moiety and one reporter moiety. F1·F1 contains two F1 equivalents. These distinctions must survive transport, loss and mass-balance accounting.

## Implementation issues versus unmeasured closure

No baseline error was found in the audited source extraction, prediction replay, inventory arithmetic, dilution schedule, or source-clock sequencing. This conclusion is limited to those checks; it is not a claim that the model is physically correct.

One latent **retention classification assumption** matters for future tests: the current vector assigns `F1` and `inactive_F1` to `retention_f`, but assigns full-length `Cy5F1` to `retention_fragments`. With synthetic settings 0.8/0.55, the three-cycle retained fractions are F1=0.8, inactive_F1=0.8, Cy5-F1=0.55. Equal retention in the saved baseline makes this harmless there. If the knob means generic full-length RNA retention, Cy5-F1 needs the same class; if it means unlabelled-specific retention, name and justify that distinction. The source does not identify either split. Existing A–B complexes also inherit fragment retention by explicit shortcut; this does not justify assigning future catalyst–product complexes the same value.

Physically unmeasured closures remain: concentration loss versus selective cohort loss; internal-volume weights; exchange/contact distribution; preparation heterogeneity; membrane modulation of chemistry; differential retention and activity; complex survival; and temperature-dependent activity clocks. The data do not identify one unique correction. Adding several fitted retention, mixing, activity, and observer factors would make the high-seed discrepancy easier to fit while weakening what the model establishes.

## Minimal next tests, with the benchmark left untuned

1. **Freeze the surviving chemistry using bulk data only.** If finite catalyst–product complexes are investigated, select and check them with whole-dose/late-time bulk validation first. Retain independent inactivation as the comparator. No GUV observation may select a chemistry candidate or rate bound.
2. **Reuse both existing transport closures and the source schedule.** Fit only their one common mixing scalar to the same 18 positive Figure 2 seed-0/seed-1 observations. Retain all seed-2 Figure 2 and all Figure 3 points as the 72-row untuned benchmark. Report both closures, every seed and generation, and the original thresholds; do not select whichever benchmark score is smaller.
3. **Use fixed limiting treatments for complexes only if the surviving chemistry contains them.** Compare intact-complex transport with instantaneous, moiety-conserving dissociation after every FT, keeping common molecular retention 0.55 per three cycles. Neither limit is measured. Preserve both outcomes and the original intact-complex choice even if it fails. Do not fit a separate complex-retention or protection coefficient to the benchmark. A bound catalyst should not simultaneously be counted as free, and products released by denaturation must remain in the observer.
4. **Retain simple conservation and observer checks.** Zero mixing must leave the initially separated system unreacted under the zero-FT-reaction approximation; complete mixing must make both closures agree; the no-regeneration control must not create active catalyst; 50% transfer must halve every retained molecule and complex moiety; and changing binding occupancy alone must not change denatured reporter ligation. For mixed-origin complexes, track founder origin explicitly, use the conditional total-competence formula above only when its assumptions hold, or report the separation as unresolved.
5. **Treat other transport changes as prospective hypotheses.** Measure paired active-F1 activity and total full-length RNA before/after FT, separate labelled/unlabelled product and fragment recoveries, and measure internal-volume/encounter distributions. Those measurements can fix differential retention and loss location before a fresh serial experiment. The existing totals cannot turn free retention/activity parameters into calibrated physical quantities.

The parent campaign has proposed a finite sensitivity set: four bulk-fit chemistry candidates through two mixing closures and two equal-aggregate-loss closures, followed by fixed complex-dissociation variants only for the bulk-selected turnover chemistry (up to 20 variants). This is acceptable as prespecified retrospective sensitivity if every outcome is retained, mixing alone is fitted on the same 18 calibration rows, and benchmark scores never select the chemistry, loss closure, dissociation treatment, or rate bounds. The [assumption ledger](assumption_ledger.json) records the physical limits.

For the all-or-none map, multiply each retained cohort's weight by `r=0.55^(1/3)` and transfer the remaining weight to an empty-content cohort, preserving total volume weight. Merging identical zero-content cohorts is exact. This represents nonselective content emptying of a fraction of equal-volume cohorts, retaining concentration in the rest. It does not establish vesicle death or measured survival probability. The aggregate PAGE loss does not exclude this limiting map. S9's microscopy tracer intensity-distribution shift could challenge pure all-or-none loss under its different protocol; it neither directly measures the F1/PAGE distribution nor validates the closure. If cargo destruction, vesicle-volume loss, or selective wash recovery is intended instead, the empty fixed-volume replacement and observer normalization need rederivation.

Reproduce from the workspace root:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-turnover-tests-2026-10-15/transport_diagnosis/audit.py
```

No new mechanism was fitted and no wet experiment was performed. The remaining risk is non-identifiability: matching a recovered reporter curve can still give the wrong retained active-catalyst inventory or compartment history.
