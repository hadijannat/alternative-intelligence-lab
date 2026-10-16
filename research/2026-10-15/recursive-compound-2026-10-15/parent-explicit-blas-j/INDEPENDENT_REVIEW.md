# Independent explicit-BLAS ordinary-J result review

Date: 2026-10-16.

- codeQualityStatus: CLEAR
- recommendation: APPROVE for recording the completed diagnostic and its numerical failure
- blockers to recording: []
- Numerical repeatability: FAIL at unchanged absolute1e-10/relative0
- Downstream conditional accuracy-qualification prerequisite: FAIL; no launch authorized

## Terminal and integrity audit

`ps -p 94290 -o pid=,stat=,command=` returned no row and exit1. The supervisor and embedded launch receipt are identical: PID94290, returncode0, no termination reason or monitor error, wall514.0907300410327s against600s cap, sampled maximum RSS3,772,645,376 bytes against10,737,418,240-byte guard. Independently checked the maximum over2414 retained samples. This is sampled memory evidence, not a certified peak or general runtime-safety result.

Independently recomputed all35 artifact hashes in launch-result.json, with zero mismatches and no unlisted files other than launch-result.json itself. All six complete arrays exist, and result.json, per-call and closed-output hash records agree with independently computed file hashes. `stderr.txt` is legitimately empty. The worker and metric receipts record two J calls, one factorization, zero SCFs and zero PCM builds. Both call captures report ordinary solve object returned unchanged and no aliasing of captured b/rho copies. No C/sign-reversal call occurred.

Rechecked428/429 grouped preparation pins, all matching; only the3,077,044,480-byte original saved metric file was left to root's full hash audit. Verified preparation/review/launch-gate bindings and the separately approval-bound original prelaunch-review hash; that review was not modified. Bound preparation SHA256:
`13cf6df31ebf08fd49d873e96d77843dd1df4cbe8e4039488a0376bf0d90d51e`.
Approval SHA256: `22fadb8296b639a3859ac79de7dbf2b93e68224c80a6df077846efd80d4b3892`.

Terminal file SHA256 values:

- launch-result.json: `e896086b360363a1c527911142bee762b39f20b3c16b073a6235cebd30987c6f`
- result.json: `cd35669af12ff030145d3f8afdf51ed8a53343c809929783f0ec121589221d1f`
- supervisor.json: `e23b1b2509b975826e47493f4822ee114bc9192e58bfd4d867e9d51c33dafc89`

## Independent full-array recomputation

Read the two new3068x3068 float64 J arrays and historical first-J matrix from `parent-openmp-first-j-v2/run-v1/J.npy` as readonly mappings. Independently calculated elementwise absolute differences in73-row blocks, instead of the production16-row helper; did not import/call that helper. Checked finite values, full-array maxima, row/column argmax and all entries exceeding1e-10. All recorded values agree exactly.

| Comparison | Maximum absolute difference | Entries above1e-10 | Argmax, zero-based | Result |
|---|---:|---:|---|---|
| B versus A | 6.702407517877873e-10 |630|2972,2972|FAIL|
| A versus historical first J |2.560511802585097e-10|80|3061,3061|FAIL|
| B versus historical first J |8.22808488010196e-10|790|2987,2987|FAIL|

Both new matrices are finite and exactly symmetric (independently recomputed max asymmetry0). Symmetry does not rescue the failed repeatability criterion. `sign_pass:false` with `max_sign_error:null` is the helper's no-reference default in these symmetry checks: no sign-reversal test was executed, so this is not a failed executed sign test.

Both19612x1 b/rho pairs are finite and unequal. Independent delta maxima and RMS using math.fsum of squared stored differences:

| Vector B minus A | Maximum absolute difference | RMS |
|---|---:|---:|
| b |2.2282620193436742e-11|6.08576192478926e-13|
| ordinary rho |0.0013222289814285304|1.7296552618145334e-05|

The rho RMS differs from the recorded last digit only through summation order; agreement is within1e-15 relative. Neither vector has a new acceptance threshold. These arithmetic checks do not rerun a solve, factorization, integral or J calculation.

## Configured control and metric/factor evidence

Independently read every thread receipt. Initial/restored getters are4/4. Explicit setter, before/after setup and before/after both J calls all report OpenBLAS1/PySCF4. Identity receipt reports shared dpotrf symbol; independently rehashed every listed binary and _flapack file, all matching. Symbol identity itself is a saved child observation, not re-executed here. Counts are configured getters, not measured executing teams. Restoration explicitly reports implicit control mode not restored; the child has exited.

The original metric content hash recorded before destruction is `f972103f0d3473f6b899e0a77aa1206a783b68ba97a550707e5fea80edbc7d6f`, matching the saved replay's metric content receipt. Factor content hash is `261d6cbcbe2d0ee2b42f3dfb064570df01ca831676e968591518f6083c242c0e`, matching the saved replay and both new post-call states. New factor identity/pointer are the same in both states; readonly/Fortran flags are true. The one alias receipt records same input/factor pointer and shared storage. This validates consistency of the saved receipts; factors and the newly built original metric were not retained, so independent elementwise reconstruction is unavailable. Hash equality does not prove a causal explanation of earlier failures.

Stage-localization receipts defer Python stage logging until return, so apparent closely spaced factor start/completion timestamps are buffered logging times, not an independent factorization timing measurement. No timing claim is inferred from them.

## Findings by severity and interpretation

CRITICAL: none. HIGH: none. MEDIUM: none.

LOW: the prelaunch final-gate exception-detail limitation remains; here the terminal gate is unchanged and all checked bindings pass. No misleading success finding: completed=true and process exit0 denote completion of the diagnostic, while the numerical pass fields explicitly remain false. Any external report must preserve that distinction.

The explicit controller did not satisfy the frozen parent repeatability requirement in this realization. Both historical comparisons also fail, but the historical matrix is the same implementation and not an independent accuracy oracle. Do not relax1e-10, replace it with energy cancellation or reinterpret vector deltas as a new pass. This result blocks the separately drafted qualification's parent prerequisite; it does not authorize a retry, SCF, PCM build or consumption of the prospective case. No cause of the discrepancies or earlier crash is proved, and no general safety, numerical accuracy, Mo34WV identity, chemistry, retention, inheritance or life/intelligence claim follows. Zero physical admissions.

Programming and remove-ai-slops perspectives were loaded and applied to the preceding source review and this evidence audit. No new code/tests or unnecessary production complexity were introduced. Only this report was written. No native J/SCF/solve/factorization/PCM/integral was rerun. Skipped the large metric rehash assigned to root and independently unrepeatable factor/metric elementwise checks; these limits do not erase the directly reproduced full-J failure.
