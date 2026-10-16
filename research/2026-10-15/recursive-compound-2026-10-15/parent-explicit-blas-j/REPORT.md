# Explicit BLAS control: completed diagnostic, repeatability failure

The single approved diagnostic completed two ordinary positive-P0 Coulomb J calls and one factorization, with zero SCFs and zero PCM builds. The unchanged absolute tolerance of 1e-10, with relative tolerance zero, was not met. Completion of the process is distinct from passing the numerical criterion.

| Full-matrix comparison | Maximum absolute difference | Entries above 1e-10 | Verdict |
|---|---:|---:|---|
| B versus A | 6.702407517877873e-10 | 630 | FAIL |
| A versus historical first J | 2.560511802585097e-10 | 80 | FAIL |
| B versus historical first J | 8.22808488010196e-10 | 790 | FAIL |

Both new 3068-by-3068 matrices are finite and exactly symmetric. The historical reference uses the same implementation and is not an independent accuracy oracle. The helper fields `sign_pass:false` and `max_sign_error:null` record the absence of a sign reference; no sign-reversal test was executed. No tolerance was relaxed and no scalar energy contraction replaced the matrix check.

The maximum B-minus-A RHS difference is 2.2282620193436742e-11; the ordinary coefficient difference is 0.0013222289814285304. These descriptive vector comparisons have no acceptance threshold and do not establish physical error. The original metric content digest and factor digest match the saved-metric replay receipts. The two calls retain one factor and return the ordinary solve object unchanged. Newly built metric and factor arrays were not retained for independent elementwise reconstruction. None of these observations proves an exclusive source of the discrepancies or the cause of an earlier native crash.

## Execution and retained evidence

The bound preparation SHA256 is `13cf6df31ebf08fd49d873e96d77843dd1df4cbe8e4039488a0376bf0d90d51e`. A separate approval authorized this one run. The frozen preparation documents retain their original prelaunch wording; terminal evidence is in [run-v1/result.json](run-v1/result.json), [launch-result.json](run-v1/launch-result.json) and [supervisor.json](run-v1/supervisor.json).

```sh
OMP_NUM_THREADS=4 OMP_DYNAMIC=FALSE OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-explicit-blas-j/run.py --launch
```

The child returned zero after 514.0907300410327 seconds, within the 600-second cap; sampled maximum RSS was 3,772,645,376 bytes across 2,414 samples, below the 10,737,418,240-byte guard. There was no monitor error or limit termination. Sampling does not certify unsampled peaks or general runtime safety. Configured getters report OpenBLAS 1 / PySCF 4 through setup and both calls; these are not measurements of executing team sizes. Initial and restored counts are 4/4, and restoring counts does not restore implicit control mode.

The [independent review](INDEPENDENT_REVIEW.md) reproduced all three full-matrix differences using 73-row blocks, verified all 35 recorded output hashes, confirmed the child absent and approved recording the failure. The original review's remaining scope limits are retained. Empty stderr is a valid retained artifact.

## Consequence

Explicit BLAS control did not satisfy the frozen repeatability requirement in this realization. A single pair does not establish a general ranking of runtime configurations. The [prospective accuracy qualification](../explicit-blas-accuracy-qualification/PREREQUISITE_STATUS.json) fails its required parent prerequisite and remains unimplemented and unlaunched. The reserved HMo2O7 case remains unused for operators or SCFs; no held-out validation occurred. Further scientific work requires a separately reviewed discriminating proposal, with the original failures and thresholds preserved.

No parent SCF readiness, exact Mo34WV identity, active catalyst retention, inheritance or intelligent-life function is demonstrated. Aggregate remains 24 assessed roles, zero verified integrated complements, and all twelve requirements I/E/T/B/R/H/V/S/M/A/J/C unmet. Publication records this negative result and does not launch further science.
