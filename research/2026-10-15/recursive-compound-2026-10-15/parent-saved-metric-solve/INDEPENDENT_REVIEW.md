# Independent saved-metric replay result review

Date: 2026-10-16. Reviewer: metric_v2_prelaunch_review.

- codeQualityStatus: CLEAR
- recommendation: APPROVE, limited to recording this completed diagnostic and its observed results
- blockers: []
- Scientific admission: none. No SCF readiness, exact-target identity, seed dependence, inheritance or life/intelligence claim is supported.

## Terminal evidence

Read the saved launch/supervisor/result, matrix-factor and error receipts; independently recomputed all 37 artifact hashes in launch-result.json with streaming reads. All matched. PID 83941 has no process row. Child returncode 0, completed=true, wall 66.03815049992409 s, sampled maximum RSS 6,496,583,680 B, no timeout, RSS-limit termination or monitor error. This is sampled memory evidence, not a hard peak bound.

Receipt SHA256 values independently computed:

- launch-result.json: `1b12b619c3491182c6eb0e8dfb557905e1c73c2afda12c5c3e477ae20e88a730`
- result.json: `6f4f2b4e2755d9dbba32242dc8cef5420d77a94280a7e15c0b37254b205cb22a`
- supervisor.json: `294593effe798add8a31ebc6275195a6173e9f9cc289f3a711d267681702fb5e`

The launch used the reviewed preparation SHA `75aae4c3937ccfd774246a10be98661ad848df2edc349a0b54df17267361c99f`. Root reports full gate verification including the 3,077,044,480-byte original metric; this reviewer did not repeat that whole-file hash. The saved original matrix was opened readonly only for selected residual rows. No factorization, solve, J call, SCF, PCM or integral build was executed by the reviewer. Bound prelaunch documents and scientific artifacts were not edited.

## Findings by severity

CRITICAL: none. HIGH: none. MEDIUM: none.

LOW: residual summaries depend materially on float64 accumulation order at sampled rows. Existing records correctly call them non-certified diagnostics; do not relabel them exact residuals or certified backward errors. Independent selected-row sums below demonstrate why that qualifier matters.

## Independently reproduced numerical observations

A1 and A2 saved coefficient arrays are bitwise identical. This establishes one identical-RHS repeated pair in this realization, not general determinism across runs, platforms, or all RHS vectors. B and C were each solved once.

| Comparison with A1 | max absolute coefficient difference | relative infinity-norm coefficient difference | RHS max absolute difference from A | relative infinity-norm RHS difference |
|---|---:|---:|---:|---:|
| B | 0.00020332596854455431 | 1.9856152879395542e-5 | 1.000444171950221e-11 | 2.353419153170805e-15 |
| C | 0.0009639826773497617 | 9.413941343331941e-5 | 2.4556356947869062e-11 | 5.776574285055613e-15 |

All values above were recomputed directly from saved arrays. Relative quantities divide by the respective A infinity norms; they are not condition estimates or physical error measures. They support strong coefficient sensitivity to the small saved RHS changes under this fixed factor/execution setting.

The saved DPOCON receipt gives reciprocal one-norm estimate 4.004423558640322e-14, condition estimate 2.4972383299521492e13, info=0 and certified_bound=false. The estimator was reviewed before launch; it was not rerun here. High estimated conditioning is compatible with sensitive coefficients and small backward residuals. It neither proves the old crash cause nor supplies a certified forward-error bound.

The new factor hash `261d6cbcbe2d0ee2b42f3dfb064570df01ca831676e968591518f6083c242c0e` differs from prior `15f8e083a4b323de758bf30b03438e1c0da0d80604b577208cc708b6c2f1a31c`. Factors are not stored, so no independent elementwise factor comparison is possible. Different execution controls and factor realization prevent attributing old/new coefficient differences exclusively to a prior solve operation. Completing this one controlled factorization also does not establish that threading caused the earlier SIGBUS.

Every saved configured-count receipt was checked: OpenBLAS1/PySCF4 around this calculation; initial/restored getters 4/4. These are configured getters, not observed executing team sizes. Explicit mode restoration is correctly disclaimed.

## Independent selected-row residual arithmetic

For each A1/A2/B/C, independently verified the saved residual infinity norm from the residual NPY. Opened the original metric readonly and sampled rows 0, 9806, 19611, plus each arm's row with the largest saved residual. Formed individual Python float products from the saved binary64 matrix/coefficient values, then used `math.fsum([b_i, -product_1, ...])`. This changes summation, but products are still rounded binary64 and the sample is not a full residual audit or certified bound.

| Arm and sampled maximum-residual row | Saved row residual | fsum of rounded-products residual |
|---|---:|---:|
| A1, row 7405 | -2.955857780762017e-11 | 1.216077059050053e-12 |
| A2, row 7405 | -2.955857780762017e-11 | 1.216077059050053e-12 |
| B, row 7915 | 4.638422979041934e-11 | 1.4769304001178836e-12 |
| C, row 10 | 2.7284841053187847e-11 | 4.1048767556970547e-13 |

Other sampled fsum residuals ranged from roughly 3.15e-16 to 3.87e-14 in absolute value. At all sampled rows, ratios to fsum(|b_i| + sum|a_ij*x_j|) were approximately 5.06e-18 to 1.50e-16. These sampled ratios do not replace the full saved componentwise maxima. In particular, the sign and scale change at row 7405 show accumulation effects; a successful factor/solve and tiny computed residual alone do not prove coefficient accuracy.

At root's request, a further independent check used Fraction.from_float for every matrix, coefficient and RHS value in exactly those three worst-saved rows. All 19,612 products and their sum were evaluated as exact rational arithmetic. This establishes the exact dot residual for the stored binary64 inputs at those rows only. It does not certify underlying molecular integrals, the full residual norm, solution forward error or physical accuracy. The three-row computation took approximately 0.185 s and performed no factorization or solve.

| Arm/row | Exact rational residual, numerator / denominator | Rounded decimal rendering |
|---|---|---:|
| A1/7405 | 51088270918292795005172184873081901183 / 46768052394588893382517914646921056628989841375232 | 1.092375420880339e-12 |
| B/7915 | 1175311528459555727846710951960289896803 / 748288838313422294120286634350736906063837462003712 | 1.5706655883156099e-12 |
| C/10 | 8605929024799425911305655696397225185585 / 23945242826029513411849172299223580994042798784118784 | 3.59400365547532e-13 |

The fsum residuals of rounded products differ from these exact stored-input values by approximately +1.2370e-13, -9.3735e-14 and +5.1087e-14 respectively. Both product rounding and summation order therefore matter; neither the ordinary residual nor the fsum check should be relabeled an exact full-matrix residual.

## Next discriminating diagnostic

Separate three questions in a newly frozen protocol before authorizing additional native work:

1. Coefficient sensitivity: use the existing coefficient deltas and original metric to assess a metric-weighted quantity such as delta-rho^T A delta-rho, with compensated/higher-precision accumulation and explicit treatment of cancellation. This measures the fitted-density Coulomb metric under the model; it is not established physical target chemistry. Do not use unweighted coefficient magnitude alone to rank scientific error.
2. Observable effect: evaluate fixed-density Coulomb-matrix changes from controlled coefficient alternatives through the same documented contraction/screening convention. Keep input density P0 fixed, preserve the historical absolute J tolerance 1e-10, and assess both elementwise J error and the fixed-density energy contraction. Scalar energy cancellation cannot excuse a matrix-level failure. A selected-element check cannot establish the full-matrix gate.
3. Numerical intervention: if testing stabilization/refinement or basis truncation, separate the numerical model change from runtime controls, preregister acceptance against the original operator, and use untouched validation cases. This replay used already examined arrays and is not held-out validation. No intervention is justified merely because it reduces coefficient differences.

No new diagnostic was launched by this review. The appropriate recorded outcome is a completed saved-input numerical experiment with strong coefficient sensitivity, a large estimated condition number, and preserved prior failures. All compound-level functions remain unverified.

## Review perspectives and limits

Programming and remove-ai-slops skill perspectives were consulted in the prelaunch review and applied to this result audit. No new production/test code was written; no implementation-mirroring or prose-pinning tests were added. The new independent arithmetic check samples actual output behavior and does not claim full-matrix certification. The earlier low-severity streaming-documentation caveat remains in the bound prelaunch review.
