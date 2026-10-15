# Why the revised bulk RNA model still fails

The revised model retains a structural restriction that the measured F1 dose curves violate: with no Hyper-A present, it predicts the same reporter yield whenever initial F1 concentration times incubation duration is the same. The workbook gives materially different yields at several such matched exposures. Substrate saturation or a common inaccessible-reporter fraction cannot remove that restriction. The Hyper-A series has a second failure: the model builds too little reporter early, followed by excessive high-dose acceleration. Neither discrepancy involves membrane transport.

This diagnosis independently reads the original workbook and replays the prior saved parameters. It does not refit, select a new mechanism, or modify the prior laboratory. All numerical results below are recomputed in [summary.json](summary.json), with every full-fit and held-dose residual in [residuals.csv](residuals.csv).

## Verified data and numerical reproduction

Run from the workspace root:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-reaction-tests-2026-10-15/diagnosis/diagnose.py
```

The script checks 120 numerical workbook cells: 40 means, 40 SDs, and 40 sample sizes. It checks metadata, residual arithmetic, and all 400 predictions from five previous candidates under full fitting and eight whole-dose holdouts. Forward replay at retained parameters reproduces every prediction exactly in the pinned runtime. All input hashes are unchanged. [Verification receipt](.omo/evidence/verification.json) captures those binary checks and source/output hashes. No previous report is accepted as proof of these computations.

S13 comprises eight separate dose curves, five times each, with n=3 summaries. Concentrations are µM; time is minutes; response and errors are percent and percentage points. Buffer is 50 mM EPPS pH 8.5, 20 mM MgCl2, 900 mM sucrose at 42 °C; Cy5-A=5 µM and B=7.5 µM. The F1 curves contain no Hyper-A. Cy5-F1 is inactive reporter product. The observer therefore measures reporter ligation, not newly active F1 directly. See the retained [source audit](../../rna-mechanism-2026-10-15/sources/salibi/audit.md) and [conditions](../../rna-mechanism-2026-10-15/sources/salibi/conditions.json).

## Residual structure

| Dose curve | Revised full-fit RMSE, pp | Revised held-dose RMSE, pp | Full-fit mean error, pp |
|---|---:|---:|---:|
| F1 0.1 µM | 1.019 | 1.031 | −0.296 |
| F1 0.25 µM | 2.361 | 2.937 | −1.482 |
| F1 0.5 µM | 7.244 | 9.604 | −5.833 |
| F1 1 µM | 6.976 | 8.078 | −4.472 |
| Hyper-A 1 µM | 7.388 | 7.425 | −5.420 |
| Hyper-A 1.5 µM | 8.330 | 11.706 | −6.656 |
| Hyper-A 2 µM | 10.032 | 10.621 | −3.030 |
| Hyper-A 2.5 µM | 12.885 | 15.849 | +2.387 |

Errors are prediction minus observed mean. These RMSEs include the supplied t=0 zeros. The revised overall full-fit RMSE is 7.892929 pp; original was 7.866012. Revised held-dose RMSE is 9.508726 pp; original was 9.797886. Excluding the eight structural zeros, revised full-fit and held-dose RMSE are respectively **8.824562** and **10.631079** pp. Keeping both summaries prevents trivial initial conditions from obscuring dynamic errors.

At 15, 30, 45, and 60 minutes, full-fit mean errors across all eight curves are −4.395, −8.058, −3.927, and +0.879 pp. The nearly unbiased endpoint average conceals underprediction at low Hyper-A doses and overprediction at high doses. Held-dose maximum absolute error is 23.093 pp. All 16 nonzero Hyper-A observations exceed twice their reported SD; across both seed types 24/32 do so, for both full fitting and held-dose validation. The maximum descriptive residual/SD is about 72 at Hyper-A 1 µM, 45 minutes.

These ratios use the reported SD, not SD/√3. They are descriptive discrepancies, **not p values**: individual replicates, repeated-time covariance, gel/batch covariance, and systematic uncertainty are unavailable. Precision of a mean does not establish assay accuracy.

## A model restriction exposed without fitting

For the selected saturation model with A=0, F remains F0, R=5−P, B=7.5−P, and

`dP/dt = kF F0 (5−P)(7.5−P)/(KB+7.5−P)`.

Setting exposure τ=F0t removes F0 from this equation. Thus all F1 curves must collapse onto one P(τ), regardless of kF or KB. A common accessible fraction q changes the initial R inventory but preserves the same collapse. Direct Hyper-A catalysis is absent in these A=0 curves, so its addition cannot repair this restriction either.

| Matched F1 exposure | First condition/yield | Second condition/yield | Difference, pp | Difference / combined reported SD |
|---|---|---|---:|---:|
| 7.5 µM·min | 0.25 µM × 30 min: 51.188% | 0.5 µM × 15 min: 55.229% | 4.041 | 0.746 |
| 15 µM·min | 0.25 µM × 60 min: 67.698% | 0.5 µM × 30 min: 81.306% | 13.608 | 8.583 |
| 15 µM·min | 0.25 µM × 60 min: 67.698% | 1 µM × 15 min: 81.550% | 13.852 | 5.777 |
| 15 µM·min | 0.5 µM × 30 min: 81.306% | 1 µM × 15 min: 81.550% | 0.244 | 0.086 |
| 30 µM·min | 0.5 µM × 60 min: 89.346% | 1 µM × 30 min: 93.509% | 4.163 | 2.040 |

Combined SD is √(SD1²+SD2²), used as a descriptive scale; the three exposure-15 comparisons share observations and are not independent tests. The revised predictions differ by less than 6×10^-8 pp at every pair, verifying the restriction numerically. Not every pair disagrees: preserving the near-equalities is important. The diagnostic establishes incompatibility of this shared autonomous catalyst-linear law with the mean pattern, subject to unmeasured assay/systematic effects; it does not prove a unique microscopic mechanism.

Time-dependent activity loss could produce less conversion in a longer, lower-dose incubation at fixed F0t. Catalyst-concentration-dependent productive assembly or concentration-dependent sequestration could also break collapse. Substrate-only saturation with a constant active catalyst cannot do so. A uniform slow activation process from an initially inactive state would tend to favor the longer incubation at matched exposure, opposite to the largest observed discrepancy, although richer folding pathways could behave differently.

## Curvature and parameter-boundary evidence

The F1 1 µM curve produces 81.550 pp in its first 15 minutes but only 0.666 pp in its last interval. The revised model gives 68.285 and 3.397 pp. F1 0.25 µM's final increment is 3.651 pp versus 8.361 predicted. These are finite-window flattening observations, not measured infinite-time plateaus or direct proof of irreversible inactivation. F1 0.5 µM has a small final reacceleration (2.938 then 5.102 pp), retained in the data rather than forced into a smooth mechanistic narrative.

Every Hyper-A mean curve has positive successive 15-minute second differences. At Hyper-A 2.5 µM, observed increments are 6.421, 12.864, 17.282, and 23.163 pp. Revised increments are 0.082, 4.311, 45.738, and 29.199 pp: a delayed burst and subsequent flattening that disagree with the smoother measured acceleration. At Hyper-A 1 µM, predicted endpoint is only 0.953% versus 14.401% observed. This pattern challenges the assumed initiation/amplification balance rather than simply its overall rate multiplier.

The revised KB optimum reaches its 100 µM upper bound in every full-fit variant, far above the 2.5–7.5 µM B range possible in F1-only reactions. Profiling KB at 0.01, 0.1, 1, 10, and 100 µM yields refitted RMSE 9.180, 9.105, 8.703, 8.091, and 7.893 pp. Thus the available fit favors the unsaturated limiting direction; it has not identified a finite B-saturation scale. In that limit kF/KB and kH/KB² are the effective combinations. Moving the bound upward might change numerical scores but would not remove F1 exposure collapse.

Allowing a common accessible-reporter fraction returns q=1 at its bound. Adding direct Hyper-A-assisted reporter ligation changes training RMSE only from 7.892929 to 7.889656 pp and slightly worsens held-dose RMSE (9.508726 to 9.517363 pp). Crucially, that direct route shares the tiny initiation coefficient kH and the squared B-occupancy factor. It is a restricted tied-rate alternative; its failure does **not** exclude an independently parameterized productive Hyper-A reporter route. The original product-inhibition Ki likewise reaches its 1000 µM upper bound; no observed finite inhibition scale was established. Parameter-boundary evidence is not a confidence interval.

## Small alternative set and validation recommendations

1. **Finite active lifetime.** Add a single shared active→inactive catalyst process with explicit inactive inventory and conserved RNA moieties. This directly tests time-dependent loss of active catalyst against the equal-exposure discrepancy. Keep common parameters across all doses; do not substitute per-dose active fractions.
2. **Independent direct Hyper-A reporter route.** Separate productive Hyper-A reporter catalysis from its initiation of new F1. Retain explicit A/B consumption in active ligation and R/B consumption in reporter ligation. This tests whether early reporter formation can occur without forcing equally rapid new-F1 autocatalysis. The reporter curves alone may still leave active F1 formation weakly identified.
3. **Constrained catalytic-complex turnover.** Represent conserved free/substrate-bound/product-bound catalyst, or an explicitly justified reduced law that reflects those inventories. A small shared binding/release model tests finite-turnover or sequestration effects. Avoid fitting every microscopic forward/backward/folding rate: 32 nonzero summary observations do not independently constrain them all. Retain the prior simple models as negative comparators.

Test individual changes and a prespecified limited combination; preserve every failed model and fit. The first two address distinct residual structures and are not mutually exclusive. Binding/product-release topology is motivated by the primary studies already collected in the source audit; no microscopic rate from a different buffer/temperature should be imported as a measured Salibi parameter.

Use **whole-dose holdouts** as the primary retrospective comparison, so a held curve contributes no fitted points. Explicitly identify the lowest/highest held doses as concentration extrapolation and interior doses as interpolation. Add a frozen **late-time challenge** (train through 30 minutes; predict 45/60) to expose burst/flattening behavior that whole-dose averaging can hide. Retain separate F1 and Hyper-A scores, every fold, zero-excluded dynamic RMSE, maximum error, boundary status, and numerical convergence. If model selection uses cross-validation, its winning score is selection-conditioned; nested outer-dose validation or a separately frozen late-time assessment is needed for an honest selection-performance estimate. All source values were already examined, so even nested validation remains retrospective development evidence, never fresh unseen experimental validation.

Do not merge S12, S15, or S18 into the same numeric holdout: sucrose, concentrations, cycle duration, dilution, or observer timing differ or remain unresolved. Transport parameters cannot repair membrane-free S13 discrepancy. A later membrane model should inherit the surviving chemical uncertainty rather than treat the best available failed bulk candidate as calibrated truth.

No new mechanism was fitted in this diagnostic subtask, and no wet experiment was performed. The principal remaining risk is non-identifiability: a better reporter fit can still give the wrong active-catalyst inventory.
