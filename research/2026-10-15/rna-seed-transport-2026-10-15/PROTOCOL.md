# Frozen retrospective seed-transport comparison

Version 1. Written before any new measured-data fitting. Implementation and synthetic checks may expose bugs before launch; any such correction must be recorded before the frozen run manifest. Old results remain immutable. Completion does not require a model to pass.

## Question and evidence boundary

Does separating extracellular exchange, subsequent reaction, serial sampling and PAGE preparation improve predictions of seed dependence? The previous selected bulk chemistry remains fixed and inadequate on some bulk challenges. Changing transport cannot certify that chemistry. All experimental outcomes have been inspected in previous work: this is retrospective, analysis-design held-out validation, not prospective validation or new experimental replication.

The source distinguishes washing collected PAGE aliquots from the continuing culture. Initial-only F1, equal suspension-volume transfer and substrate-only feed are retained. Continuing exterior carryover is the primary interpretation; complete extracellular discard is an explicitly unmeasured sensitivity. The model assumes equal effective encapsulated volume per suspension volume. It does not infer physical pedigree, Darwinian inheritance, life or intelligence.

## Chemical states and fixed parameters

Intracellular and extracellular concentrations are in micromolar. Species are Hyper-A `A`, labelled inactive precursor `R`, substrate `B`, competent F1 `F`, labelled ligated reporter `P`, and inactive F1 `D`. Passive tag `H` counts competent founder F1 and is a subset of F, not an additional molecular inventory.

Use the exact six parameters from `../rna-turnover-tests-2026-10-15/results-v1/fits/baseline__omit-none.json`, hash recorded at freeze:

| Parameter | Value |
|---|---:|
| ka | 0.01571930404353992 |
| kf | 0.14700614279831425 |
| kh | 0.0006836756169276764 |
| krh | 0.000708265067441493 |
| KB | 1.3611955373989844 |
| kd | 0.012946670134460872 |

For `s=B/(KB+B)`, define `va=ka F A s`, `vr=kf F R s`, `vh=kh A² s²`, `vp=krh A R s²`.

```text
A' = -va-vh             R' = -vr-vp
B' = -va-vh-vr-vp       F' = va+vh-kd F
P' = vr+vp              D' = kd F
H' = -kd H
```

`ka,kf,kh,krh` have units µM⁻¹ min⁻¹ under these effective rate laws; KB is µM, kd is min⁻¹. The independent conserved inventories are `A+F+D`, `R+P`, and `B+F+P+D`. This reuses a phenomenological precursor reaction and irreversible competence loss; these mechanisms remain uncertain. No turnover, reactivation, selective active retention or new bulk fitting enters this comparison.

## Three fixed transport families

Weights `w_i` sum to one and represent internal volume fractions. Each FT cycle is one dimensionless transport interval τ; chemistry during that interval is neglected. All seven quantities have the same permeability. This is a common-cargo closure, not a measured claim that 14-, 52- and 66-nt RNAs have equal mobility.

1. **legacy**: each cycle applies `c_i ← r[(1-m)c_i+m sum(w c)]`, with `r=.55^(1/3)`. Removed cargo enters an irreversible loss ledger. Fit m in [0,1]. This preserves the failed historical comparator.
2. **bath**: a shared finite exterior of relative volume ν obeys `dc_i/dτ=κ(e-c_i)`, `ν de/dτ=κ(sum(w c)-e)`. Fit ν in [1,30].
3. **patch**: each cohort has an exterior patch of volume `ν w_i`, with `dc_i/dτ=κ(e_i-c_i)` and `de_i/dτ=(κ/ν)(c_i-e_i)+D_e(sum(w e)-e_i)`. Fit ν in [1,30] and D_e in [.001,10] per FT interval. This is effective patch exchange, with no measured physical spacing or diffusion coefficient.

Finite models conserve `sum_i w_i(c_i+ν e_i)`. Means obey the two-state bath solution; patch deviations obey the matrix exponential of `[[-κ,κ],[κ/ν,-κ/ν-D_e]]`. Bath intracellular deviations decay as `exp(-κτ)`. Exterior is retained between successive FT intervals. D_e=0 prevents transfer between initially separate substrate patches; the large-D_e limit approaches the common bath. Those limits are numerical tests, not additional fitted candidates.

For both finite families:

```text
κ(ν) = -log(.55-.45/ν) / [3(1+1/ν)]
R3 = [1+ν exp(-3κ(1+1/ν))]/(1+ν) = .55
```

This relation is exact only for a nonreacting, initially uniform internal reference tracer with an initially empty exterior. The source's approximate gel-based RNA retention is not such a tracer experiment. Imposing this relation is a declared parameter-reduction assumption. ν>9/11 is required; fitted bounds are analyst choices, not measured volume limits. A preloaded exterior will not enforce 55% retention in later generations.

## Schedule, observer and fixed sensitivities

Initial cohorts have weights 1/3: F1/H at seed dose 0, 1 or 2 µM; A=10 and R=2.5 µM; B=15 µM. Exterior starts empty. Figure 2 applies 1, 2 or 3 FT intervals followed by 60 minutes at 42 °C. G1 applies 3 FT then 60 minutes. G0 is recorded as an initial control.

At warm-stage entry, exterior patches are homogenized to their weighted mean, conserving exterior inventory. Membranes then close. Each intracellular cohort reacts separately; the exterior reacts separately. Homogenization before warm incubation is a well-mixed exterior approximation and resets exterior patch differences, not intracellular contents. It is not measured vesicle motion or a spatial simulation.

For G2–G7, halve weights of old cohorts and append fresh A/R and B cohorts with weights .25 each. Intracellular concentrations of surviving cohorts stay unchanged. Half the exterior amount is transferred, and the fresh exterior contains no RNA: its concentration is halved and assigned uniformly to all exterior patches. ν remains constant, an unmeasured volume closure. Sampling, feed and any discard are explicitly ledgered.

The PAGE observer is `100 sum(w P)/sum(w(R+P))`, using internal RNA only. Washing an assay aliquot does not reset the simulated continuing culture. Record reporter denominator, internal/external competent F1, competent founders H, newly generated competent F−H, and new reporter production during each warm interval. Historical reporter percentage is not a measure of new function.

Report **nine scenarios**, without held-out selection: legacy plus each finite family under the 2×2 crossing below. All finite scenarios reuse that family's calibration fit.

| Assumption | Primary | Fixed alternative |
|---|---|---|
| Exterior warm chemistry | Same six rates as interior | All exterior chemistry frozen, including F/H decay |
| Exterior at serial transfer | Carry the sampled half | Discard entire exterior after each measured generation |

Applying sucrose-calibrated rates to the glucose exterior is unmeasured. The inert alternative is an optimistic protection limit, not known absence of catalysis. Whole-culture discard is not asserted to be the source's aliquot wash. Neither alternative is chosen by benchmark performance.

## Data partition and fitting

Use the unchanged 148-row observation table and stable IDs `observation_000` onward. Freeze the concrete ID lists in output before fitting. Bulk S13 rows and zero-time controls do not enter transport calibration or scored validation.

| Partition | Conditions | Rows |
|---|---|---:|
| Calibration | Figure 2 seeds 0/1, FT 1/2/3 | 18 |
| Held seed | Figure 2 seed 2, FT 1/2/3 | 9 |
| Serial holdout | Figure 3 seeds 0/1/2, G1–G7 | 63 |

The 18 calibration rows represent six conditions with three reported replicates. Do not treat them as 18 distinct mechanistic conditions. Fit unweighted replicate residuals in percentage points. No Figure 3 value or held seed enters fitting, profiles, bounds or model selection. Cross-figure G1 differences remain a limitation; no dataset offset is fitted.

Each family uses six fixed starts at normalized bound fractions (.05,.2,.4,.6,.8,.95). m is linear; ν and D_e are log10 transformed. The patch D_e start order is reversed relative to ν. Use SciPy least_squares, three-point numerical Jacobian, diff_step=1e-3, max_nfev=120, ftol=xtol=gtol=1e-8. Every attempted start is retained with status, objective, evaluations, elapsed time and boundary indicators. No selective budget extensions. Choose the lowest-SSE successful start; if none succeeds retain an unresolved fit. At least two successful starts must have SSE agreement within `max(1e-4,1e-4*best_SSE)` for computational qualification. Agreement does not prove a global optimum or parameter identification.

Training-only objective profiles: nine geometrically spaced ν values from 1 to 30 for bath (direct objective) and patch (refit D_e); nine D_e values .001 to 10 for patch (refit ν). Nuisance fits use the same six starts and budget. These are objective profiles, not confidence intervals. Retain boundary optima, weakly varying profiles and unresolved points. Total: 3 main fits, 18 nuisance profile fits, 126 bounded optimization starts, plus 9 direct bath objectives.

## Evaluation and qualification

Report all scenarios' calibration, held-seed, serial and pooled-heldout errors, including per-condition residuals. RMSE uses individual reported replicate rows. Maximum absolute error uses condition means (dataset, seed, FT/generation); display both definitions. Seed contrasts 1−0 and 2−0 are reported for every generation, with measured contrasts and predicted inventories/new production. No benchmark winner or post-score model refinement.

Adequacy screen: heldout RMSE ≤2 percentage points AND maximum absolute condition-mean error ≤4 points, plus qualified numerical checks and a qualified calibration fit. This is a pragmatic inherited tolerance, not an experimentally derived uncertainty interval. Report accuracy failure separately from numerical failure. A lower error alone does not establish adequacy.

Use LSODA chemistry with rtol=1e-8 and atol=1e-10; repeat all saved-parameter predictions at rtol=1e-10 and atol=1e-12. Require maximum PAGE change ≤1e-4 pp and total source/removal moiety residual ≤1e-6 µM. Independently compare analytic transport against a full coupled ODE implementation. Require concentration nonnegativity and H≤F within numerical tolerances. Numerical errors remain recorded and block physical-adequacy claims.

Before launch, test conservation, nonempty-bath reuptake, reference retention, no transport, isolated/global patch limits, sample observation versus whole-culture discard, serial source bookkeeping, prior baseline chemical equivalence and synthetic recovery. A full fresh-process refit must reproduce scientific outputs; clocks and plot bytes are not numerical equivalence criteria.

## Reproducibility and preservation

Pin Python3.12.3, NumPy2.4.1, SciPy1.16.1, Matplotlib3.10.8 and openpyxl3.1.3. Refuse existing output directories. Copy code/protocol/source ledgers and input hashes into the run before fitting. Save all starts, profiles, predictions, state ledgers, seed contrasts, refinements and screening flags. Compare previous laboratory/source hashes before and after. Preserve diagnostic negative interventions and all historical failed models. No new source dataset enters this frozen fit.

Remaining uncertainty includes unknown exterior volumes, RNA-dependent permeability, pore timing, spatial correlations, glucose-exterior kinetics, active-state reversibility and assay recovery. Computational approval is separate from chemical validation.
