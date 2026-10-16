# Independent terminal review

codeQualityStatus: CLEAR
recommendation: APPROVE evidence classification and publication
blockers: []
Scientific status: COMPLETED_WITH_NUMERICAL_NONPASS

The bounded diagnostic completed all three prescribed requests. Five of six numerical comparisons failed the unchanged absolute 1e-10 criterion (rtol 0). This is a retained negative numerical result, not parent SCF readiness or chemical validation.

## Independent array replay

Read saved J1/J2/J3 and original Jold with read-only mmaps. A separate seven-row implementation, rather than the driver's sixteen-row comparison function, independently recomputed all maxima, first row-major argmax locations, counts above tolerance, values at maxima and operand magnitudes. Every value matched comparisons.json exactly. All three output arrays are finite and exactly symmetric under the independent check.

| Comparison | Maximum absolute error | Entries above 1e-10 | First argmax | Verdict |
| --- | ---: | ---: | --- | --- |
| J2-J1 | 4.844054046770907e-10 | 284 | [2972,2972] | NONPASS |
| J3+J1 | 4.420286359163583e-10 | 231 | [2972,2972] | NONPASS |
| J3+J2 | 4.142748366575688e-10 | 31 | [3022,3022] | NONPASS |
| J1-Jold | 4.718572199635673e-10 | 304 | [1882,1882] | NONPASS |
| J2-Jold | 9.484324436925817e-11 | 0 | [3007,3007] | PASS |
| J3+Jold | 3.2159164220502134e-10 | 14 | [3022,3022] | NONPASS |

Same-sign, sign-reversal and external-run categories are therefore all NONPASS. The passing J2-Jold pair does not override the other failures. The per-array matrix_checks sign_pass=false/max_sign_error=null fields are the helper's no-reference sentinel, not additional evaluated sign tests; the six comparisons above supply the sign/repeat evidence.

## Execution and integrity audit

- Fresh frozen manifest and approval gate match launch-gate.json. All 24 artifact hashes in launch-result.json match current files; no missing artifacts or artifact errors.
- Independently loaded original cycle-zero P0 and reproduced its positive/negative byte digests. Input records match the fixed [+1,+1,-1] sequence and prepared positive digest.
- Exactly three native J callback records, one Cholesky factor creation, zero SCFs. Stage sequence records save/close/hash, post-call close and array release before each subsequent request.
- Recorded factor identity, pointer and content digest are equal across all three states and match the creation digest. No raw factor is retained for independent content rehash; this part is verified from runtime observations and the frozen checked code, not a saved-factor replay.
- Supervisor exit0, no termination reason or monitor error, wall696.6868703749496 seconds, sampled maximum RSS3,655,090,176 bytes. Recomputed sample maximum matches. Embedded launcher receipt equals standalone supervisor.json. PID37763 was absent on independent ps check.
- All three buffered checkpoints closed; no recorded allocator trap occurred in this diagnostic. The sampled memory observation is not a hard peak or future allocation guarantee.

## Interpretation and limits

Identical positive inputs on the same object produced different outputs beyond the frozen tolerance. This establishes a repeatability limitation in the observed configuration without requiring sign reversal to explain every discrepancy. It does not identify OpenMP reductions, screening, allocator behavior, or any other mechanism as the cause. Sign and call order remain confounded. Jold uses the same algorithm and is not an independent numerical oracle.

The old signed-run failure remains unchanged. No threshold was relaxed, simulation restarted, native operator rerun, or previously passed synthetic test repeated by this reviewer. No physical admission or parent SCF readiness follows. A future causal investigation requires a separately reviewed control design; this audit authorizes no new native execution.

## Evidence binding

Launch-result SHA256: 86caecf4eafd9ab8d3d6212466f4e79d87dbaa5ea64ed69e6c063b6735982fce

- J1.npy: 8bacd08c2f8e852b9dd164bd33aa6518d872dd87b65cce2ffeabab7d6f861bb6
- J2.npy: de18f44800b2fa29fe36b171fedfcefd3d01cf0f38fd55b937616744d890c831
- J3.npy: a152f67d3cea79974e826aac9fd39ff2b9f33712ce1577fd1759bd5f2d5101ee

Programming/remove-ai-slops perspectives were applied during the exact-preparation review. This terminal audit found no mismatch requiring production changes; no new code/tests were introduced.
