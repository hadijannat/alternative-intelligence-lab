# Frozen turnover and transport comparison

Version 1, 15 October 2026; written before any new measured-data fit. This is retrospective development using previously inspected S13 and transport data. Synthetic checks may correct implementation errors before launch. No candidate, bound, fitting budget or decision threshold changes in response to official scores. Failed attempts and negative outcomes remain intact.

## Question and evidence

The previous independent-efficiency/inactivation model improves seeded F1 while worsening Hyper-A validation. Omitting high Hyper-A overpredicts its late endpoint; fitting only early data underpredicts high Hyper-A but overpredicts seeded F1 at late times. Six successful agreeing starts reproduce these fits. A uniform activity reduction alone is not an adequate diagnosis. Transport also loses the observed seed dependence, with seed 2 contributing most squared error. Independent assays at the nominally equivalent first-cycle condition disagree, so some residual may reflect unmodeled preparation/experimental variation.

Finite catalyst-product complexes are supported as topology in related primary ligase work. Their microscopic constants under different sequences, magnesium, temperature and reporter conditions are not Salibi calibrations. Shared release/binding affinities, inactive-state binding and preparation assumptions below are deliberately reduced hypotheses. See research/REPORT.md, diagnosis/REPORT.md and transport_diagnosis/REPORT.md.

## States, reactions and observer

Concentrations are µM; time is minutes. States: A (Hyper-A), R (Cy5-A), B, F (available competent F1), P (ligated inactive fluorescent reporter), D (catalytically inactive full-length RNA), and QFF, QFP, QFD, QDD, QDP, QPP (bound pairs). Complexes occupy binding sites and cannot catalyze another event until release. Competence and physical binding are distinct.

Set s=B/(KB+B). Retain the previous effective initiation and ligation rates:

```text
va = ka F A s                 F-mediated active-fragment ligation
vr = kf F R s                 F-mediated reporter ligation
vh = kh A² s²                 precursor-assisted active initiation
vp = krh A R s²               precursor-assisted reporter ligation
```

The instantaneous comparator produces free F from va+vh and free P from vr+vp, returning the catalytic F. In turnover candidates, va consumes F+A+B and forms QFF; vr consumes F+R+B and forms QFP. Only the F-mediated routes create these complexes. vh consumes A+B and creates free F; vp consumes R+B and creates free P. The catalytic A in precursor-assisted routes is returned. Net ligation releases pyrophosphate, which is not dynamically modeled; these are RNA-moiety balances, not a complete thermodynamic model.

All six complexes release their constituent monomers at krel Q. Rebinding variants add homotypic association 0.5 kbind X² for FF, DD and PP, and heterotypic association kbind X Y for FP, FD and DP. The factor convention makes association independent of competence/reporter labels under the common-affinity assumption. P–P binding is retained for consistency rather than leaving all inactive reporter available to bind F.

Uniform per-competent-strand functional loss is F→D at kd F, QFF→QFD at 2kd QFF, QFD→QDD at kd QFD, and QFP→QDP at kd QFP. It neither automatically protects bound catalyst nor forces dissociation upon loss. D retains the assumed recognition-arm affinity and release rate. These are fixed closures; D does not specify hydrolysis or a measured molecular lesion.

Conserved inventories:

```text
active-origin RNA: A+F+D+2QFF+QFP+2QFD+2QDD+QDP
reporter RNA:      R+P+QFP+QDP+2QPP
B-origin RNA:     B+F+P+D+2(QFF+QFP+QFD+QDD+QDP+QPP)
```

Denaturing PAGE observes 100(P+QFP+QDP+2QPP)/(R+P+QFP+QDP+2QPP). Bound ligated product already counts. Competent full-length inventory is F+2QFF+QFP+QFD; only free F is immediately available. The no-regeneration control sends va into QFD and vh into D, so newly ligated strands never count as competent.

## Fixed candidates and preparation

| Candidate | Free parameters | Choices |
|---|---|---|
| baseline | kf,kh,KB,ka,krh,kd (6) | Prior selected independent/inactivation family; instantaneous products |
| release | baseline+krel (7) | Finite release; kbind=0; initially free strands |
| reversible_free | baseline+krel+kbind (8) | Full pair rebinding; initially free strands |
| reversible_equilibrium | same eight | Same chemistry; initial full-length strands at common-affinity equilibrium |

No other combinations or curve-specific parameters are introduced. For equilibrium, initial total full-length monomers T=Ftotal+Dtotal+Ptotal share a free fraction. Free total u solves T=u+(kbind/krel)u²; free species retain their initial proportions, and pair concentrations follow the association/release convention. This is a limiting preparation scenario, not measured occupancy. No instantaneous re-equilibration follows mixing, dilution or feeding. Sources normally start D=P=0, but the general formula is tested for conservation.

## Data, fitting and holdouts

Reuse the exact 148-row source export and original workbook. S13 has eight complete dose curves and 40 mean observations; fit and score only 32 positive-time means. Time-zero values are displayed and archived but cannot improve the primary score. No duplicate S13d endpoints, fabricated replicates, or incompatible assays enter fitting. Published SD and n=3 are descriptive; unknown replicate covariance prevents calibrated chi-square inference.

Log10 bounds are kf/ka [-4,1], kh/krh [-8,0], KB [-2,2], kd [-6,0], krel [-4,2], kbind [-6,2]. Six deterministic starts use these columns:

| Start | kf | kh | KB | ka | krh | kd | krel | kbind |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | -1 | -5 | 0 | -1 | -4 | -2 | -1 | -2 |
| 2 | -0.5 | -3 | 1 | -0.5 | -2 | -1 | 0 | 0 |
| 3 | -1.5 | -6 | -1 | -1.5 | -6 | -3 | -3 | -4 |
| 4 | 0.2 | -4 | 1.8 | -2 | -3 | -4 | 1 | 1 |
| 5 | -2 | -2 | -1.8 | 0.5 | -1 | -0.3 | 0.5 | -5 |
| 6 | 0.8 | -7 | 0.5 | -0.2 | -7 | -5 | -2 | 0.5 |

Use least_squares with max_nfev=160 per start, jac='3-point', diff_step=1e-3, xtol=ftol=gtol=1e-8; derivative evaluations are additional. LSODA rtol=1e-8, atol=1e-10; batch paired curves. Schedule independent fits across four processes, never concurrent LSODA threads. Retain every start, message, nfev/njev, finite objective and bounds. A fit resolves with at least one finite successful start; choose its smallest SSE. Flag whether two successful starts agree within max(1e-4,1e-4*best_SSE). A failed held prediction or unresolved fit invalidates its pooled score. No selective retries or budget increases.

1. Fixed-family whole-dose validation: eight folds, seven complete training doses, all five points of the omitted dose predicted; primary score uses its four positive times.
2. Nested selection: each outer dose omitted throughout; seven inner held-dose folds use six training curves. Cache the 28 unordered omitted pairs per family. Among fully resolved families within 0.25 pp of best inner RMSE, prefer fewer free parameters, then lexical identifier. Refit seven outer-training curves and predict the outer dose. Retain all IDs and inner scores.
3. Late-time challenge: fit 15/30 minutes across all eight doses; predict 45/60 minutes for each fixed family. No selection from these outcomes.
4. Joint high-dose/later-time challenge: exclude F1=1 and Hyper-A=2.5 µM entirely; fit only 15/30-minute means at the six remaining doses (12 values), and predict 45/60 minutes at the two excluded high doses (four values). Apply to every family, with no selection from this severe extrapolation challenge.
5. Final development choice: apply the same 0.25 pp simplicity rule to ordinary eight-dose validation, then use its full-data fit. Its ordinary CV score is selection data; the nested score estimates the selection procedure.

For every bulk challenge retain the earlier pragmatic limits: positive-time RMSE≤2 pp AND maximum absolute error≤4 pp, plus numerical qualification. Lower RMSE than the matched baseline is improvement, not adequacy or proof of mechanism.

## Profiles and numerics

Profile KB and each introduced free parameter (krel/kbind when present) for the final development choice, at five equally spaced values across its registered log10 bounds. Refit nuisance parameters with the same starts and budget. Retain objectives, boundaries, Jacobian singular values and active/available/reporter inventories. These are coarse objective profiles, not confidence intervals. Preserve inventories for every full-fit family.

At every resolved full fit, refine rtol to 1e-10 and compare batched with separate integrations: observer discrepancies must each be <1e-4 pp and moiety error <1e-7 µM. Test rapid-release recovery of the comparator, zero-rebinding behavior, occupied-catalyst availability, per-strand loss, no-regeneration bookkeeping, pair statistical factors, equilibrium, transport and observer conservation. Numerical failure prevents an adequacy claim; do not claim separate tolerance certification of every fold.

## Transport diagnosis and fixed sensitivity cases

Freeze chemistry separately for all four full-data families. For each, test fractional and contact mixing crossed with uniform and all_or_none content loss: sixteen main scenarios, all with no complex reset. Both loss closures retain the same aggregate 0.55 RNA fraction after three FT cycles, using r=0.55^(1/3) per cycle. Uniform loss scales local concentrations. All-or-none content emptying preserves retained concentrations, multiplies cohort weights by r and assigns lost volume weight to empty cohorts. Merge identical empty cohorts to bound state size. This is an unmeasured limiting distribution, not observed vesicle survival or death.

For the bulk-selected family, if it has turnover, additionally cross both mixing and loss closures with instantaneous stoichiometric complex dissociation after each FT. These four fixed sensitivity scenarios bracket unresolved thermal-complex history. They conserve every RNA inventory and the PAGE signal; they are not a measured freeze/thaw mechanism. If the comparator is selected, the reset is identical and is not duplicated.

Fit only mixing m∈[0,1] using Figure2 seeds0/1, FT1/2/3 (18 observations), bounded scalar minimization xatol=1e-7. Chemistry, release, rebinding, loss rate, preparation, loss-distribution and reset assumptions cannot be fitted to the historical challenge. Report all scenarios on Figure2 seed2 plus all positive Figure3 generations (72 values). No transport winner is selected from these scores. Retain RMSE≤2 pp and maximum absolute group-mean error≤4 pp screen, qualified by serial refinement <1e-4 pp and moiety error <1e-7 µM.

All material classes share the stated retention. Under uniform per-strand competence loss, equal retention and no reactivation, founder TOTAL competent expectation is seed/3 ×0.55^g×0.5^(g−1)×exp(−60kd g) at g≥1. This is conditional and includes bound founders; it must never be subtracted from free F alone. Parent–daughter inheritance is not measured. Cross-assay first-cycle discrepancies and seed-history loss remain reported even if a sensitivity case fits better.

## Evidence retention and reproduction

Freeze model, runner, tests, protocol, source export/workbook, relevant ledgers and dependency versions before measured fitting. Refuse existing output directories. Retain every raw prediction, start, failed scenario, profile, state inventory and frozen source; record development mistakes separately. Independent verification code cannot influence fits and is separately hashed. Saved-parameter replay preserves original evaluation batches. A complete fresh-process refit must match scientific numbers within abs1e-8+rel1e-8 and discrete choices/IDs exactly; clocks and plot bytes are excluded. Report physical uncertainty separately from successful software verification.
