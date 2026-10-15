# Frozen retrospective reaction-mechanism comparison

Protocol v1, 15 October 2026. This protocol is written before new mechanism fitting. Numerical development may profile runtime and check synthetic invariants, but may not tune chemistry, bounds or selection using candidate scores. Any necessary implementation correction preserves the failed attempt and is documented. The existing measured data have already been inspected; all validation below is retrospective.

## Evidence and chemistry

The previous model fails before transport. F1-only dynamics have the restriction `dP/dt = F0 g(P)`, so reporter yield depends only on `F0*t`. Actual equal-exposure observations differ by approximately 13.9 percentage points. A common substrate saturation factor or common inaccessible fraction cannot repair this invariant. Hyper-A reporter activity also appears too early and the high-dose trajectory accelerates too strongly relative to the old fit. These discrepancies motivate the bounded candidates below; they do not identify a unique cause.

Concentrations are µM and time is minutes. States are A (Hyper-A), R (Cy5-A), B, F (active F1), P (inactive Cy5-F1), D (inactive F1-equivalent material), CA (nonproductive A+B complex) and CR (nonproductive R+B complex). Set `s = B/(KB+B)` using free B. Rates:

```text
active ligation       va = ka F A s + kh A² s²
reporter ligation     vr = kf F R s + krh A R s²
functional loss      vd = kd F
off-path association ua = kon A B - koff CA
                     ur = kon R B - koff CR
```

Each ligation consumes one matching precursor and one B. P, D, CA and CR do not catalyse. Functional loss F→D conserves RNA moieties; it is not a chemically explicit hydrolysis model. CA and CR are coarse nonproductive complexes, not structurally identified Salibi intermediates. They dissociate during denaturing analysis and count as unligated reporter. The PAGE observer is `100 P/(R+P+CR)`. Conserved inventories are `A+F+D+CA`, `R+P+CR`, and `B+F+P+D+CA+CR`.

| Identifier | Free parameters | Fixed choices |
|---|---|---|
| revised | kf, kh, KB (3) | ka=kf; krh=kd=kon=koff=0; matched prior selected family |
| independent | kf, kh, KB, ka, krh (5) | kd=kon=koff=0; separate active/reporter efficiencies and precursor reporter route |
| inactivation | kf, kh, KB, kd (4) | ka=kf; krh=kon=koff=0 |
| independent_inactivation | kf, kh, KB, ka, krh, kd (6) | kon=koff=0; one prespecified combination |
| trapping_free | kf, kh, KB, kon, koff (5) | ka=kf; krh=kd=0; initially free substrates |
| trapping_equilibrium | same five | same chemistry, initial CA/CR in equilibrium at Kd=koff/kon |

This is three proposed mechanistic changes, one prespecified combination and two fixed preparation scenarios, not unrestricted model expansion. Primary sources support exploring distinct reaction efficiencies and nonproductive binding. Their conditions do not calibrate these rates. Salibi starts incubation by Mg²⁺ addition after preparation on ice; zero preexisting complex is not established. The equilibrium variant solves the shared-substrate mass balances with the same initial total A/R/B and no added fitted initial fractions. After initialization, both trapping variants evolve finite-rate ODEs. Every tested preparation remains reported.

Units: kf, ka, kh and krh are µM⁻¹ min⁻¹; KB is µM; kd and koff are min⁻¹; kon is µM⁻¹ min⁻¹. Source-supported identity/topology and hypothetical reductions are separated in `research/REPORT.md`.

## Data and score

Use the exact eight S13c dose trajectories: F1=0.1/0.25/0.5/1 µM with A=0; Hyper-A=1/1.5/2/2.5 µM with F=0. All have Rtotal=5 µM, Btotal=7.5 µM, 20 mM MgCl₂, 50 mM EPPS pH 8.5, 900 mM sucrose, 42°C. There are 40 means at 0/15/30/45/60 min, with published SD and n=3. Do not duplicate S13d endpoints or fabricate replicate trajectories.

Fit unweighted percentage-point residuals at t>0. The primary metric uses 32 informative means. Record the old 40-row RMSE for comparability, but deterministic time-zero points do not improve the primary score. Descriptive SD-scaled residuals are permitted; unknown within-curve covariance and unavailable replicates preclude a chi-square significance interpretation. Complete dose curves, never randomly selected timepoints, define held-out groups.

## Frozen optimization

Log10 bounds: kf and ka [-4,1]; kh and krh [-8,0]; KB [-2,2]; kd [-6,0]; kon and koff [-6,1]. They are broad declared scenarios, not confidence limits. Exactly six deterministic starts use columns from this table for each fitted parameter; fixed parameters remain fixed.

| Start | kf | kh | KB | ka | krh | kd | kon | koff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | -1 | -5 | 0 | -1 | -4 | -2 | -2 | -2 |
| 2 | -0.5 | -3 | 1 | -0.5 | -2 | -1 | 0 | -1 |
| 3 | -1.5 | -6 | -1 | -1.5 | -6 | -3 | -4 | 0 |
| 4 | 0.2 | -4 | 1.8 | -2 | -3 | -4 | -1 | -4 |
| 5 | -2 | -2 | -1.8 | 0.5 | -1 | -0.3 | 0.7 | 0.7 |
| 6 | 0.8 | -7 | 0.5 | -0.2 | -7 | -5 | -5 | -5 |

All fits use least_squares, max_nfev=160 and xtol=ftol=gtol=1e-8. Use three-point numerical derivatives with diff_step=1e-3, declared before fitting to keep perturbations above integration noise; SciPy applies its default three-point step at zero log coordinates. Batch curves into one integration where feasible; LSODA rtol=1e-8, atol=1e-10. Schedule independent dose-subset fits across four worker processes, preserving the same per-fit budget and deterministic result order; never run LSODA concurrently in threads. Numerical failures are recorded. A fit resolves if at least one start terminates successfully with finite predictions. Select the smallest SSE among successful starts. Record every start's termination, evaluations, SSE and active bounds; report whether two successful starts agree within `max(1e-4, 1e-4*best_SSE)`. A failed fold is unresolved, not omitted or assigned a favourable score. No selective retry or budget escalation follows official results.

## Held-out analysis

1. **Fixed-family dose validation.** Leave each entire dose trajectory out. Fit seven and predict the eighth. Report all eight positive-time errors, pooled RMSE, maximum absolute error and historical 40-point score for every family.
2. **Nested model-selection validation.** For each outer held-out dose, compare families through seven inner held-dose folds within the remaining seven curves. Fit six curves in each inner fold. Cache fits by unordered omitted pair: 28 unique inner training subsets per family. Select only families with all inner folds resolved, within 0.25 pp of minimum inner RMSE; prefer fewer parameters, then lexicographic identifier. Refit the selected family on the seven outer-training curves and predict the outer curve. Outer observations never choose the family. Preserve fit-training IDs, inner/outer IDs and all choices.
3. **Late-time challenge.** For every fixed family, fit only 15/30-minute means and predict 45/60-minute means. No winner is chosen using the late-time outcome. This is a separate retrospective extrapolation, not independent experimental replication.
4. **Final development choice.** Apply the same simplicity rule to all eight ordinary dose folds, then fit that family to all positive-time means for profiles and the historical transport challenge. Its ordinary CV score is selection data; the nested score describes the selection procedure.

Predictive improvement is lower held-dose RMSE than the matched revised comparator, with all per-dose errors displayed; it is not proof of mechanism. A new pragmatic bulk adequacy screen requires positive-time held-dose RMSE≤2 pp and maximum absolute held-out error≤4 pp. Apply the same screen to the nested predictions and late-time challenge, reporting each separately. These thresholds are planning criteria, not a source-derived noise model. Never redefine them after seeing results.

## Profiles, refinement and historical transport

For the final development choice, profile KB at log10 values [-2,-1,0,1,2] and each introduced free parameter at five equally spaced values across its registered log bounds. Refit nuisance parameters with the same six starts and evaluation budget, clipping starts only to valid free-parameter bounds. Report the full objective profile, bound optima and Jacobian singular values. These are identifiability diagnostics, not calibrated confidence intervals. Retain differences in state inventories among similarly fitting models; reporter data do not directly identify active F1.

At every resolved full-data fit, compare predictions at rtol=1e-10 against the registered integration tolerance; require maximum difference<1e-4 pp and moiety discrepancy<1e-7 µM. Compare batched with separate-curve integration. Numerical failure prevents adequacy claims.

Freeze all chemistry before fitting transport. Reuse both previous fractional/contact cohort exchange rules and 0.55 three-cycle retention for all material classes, explicitly hypothetical for active catalyst and complexes. Fit only mixing m on Figure2 seed0/1 with FT1/2/3 (18 observations); do not fit chemistry or preparation to these observations. Report both closures on Figure2 seed2 and all Figure3 positive generations (72 historical benchmark values), including failures. Retain the old benchmark screen RMSE≤2 pp and maximum absolute group-mean error≤4 pp. These data were already inspected and are not a fresh external validation set. No physical division, parent–daughter inheritance or parameter transplant across incompatible buffers is inferred.

## Retention of evidence

Save protocol, source data/workbook, code, dependency versions and hashes before fitting. Retain individual fits incrementally, every fixed/nested/time prediction, full fits, profiles, transport predictions/trajectories, numerical checks, figures and convergence failures. Refuse existing output directories. Preserve interrupted/invalid attempts. Tests precede official execution. Fresh-process saved-parameter replay and independent complete refit must reproduce scientific numbers within absolute 1e-8 plus relative 1e-8 tolerance in the same pinned runtime; discrete choices and training/evaluation IDs must match exactly. Timestamps and runtime are excluded. Solver-tolerance refinement has the separate limits declared above. No assertion of unique reaction mechanism, active-F1 retention or life follows from passing software tests.
