# Independent terminal review: stage-localization diagnostic

codeQualityStatus: CLEAR
recommendation: APPROVE evidence classification
blockers: []
Execution status: COMPLETED_BOUNDED_STAGE_LOCALIZATION
Scientific status: ordinary repeatability remains NONPASS; fixed-rho contrast passes its specified comparison only.

## Independently replayed outputs

Read nine retained NPY arrays. Recomputed the two J contrasts with a separate seven-row mmap implementation, without calling driver classify/compare. Maxima, first argmax, values at argmax and counts above fixed1e-10 match the original records. Independently recomputed all four vector differences without driver vector_difference. All maximum/RMS/exact-equality results match.

| J comparison | Maximum absolute difference | Entries above1e-10 | Argmax | Verdict |
| --- | ---: | ---: | --- | --- |
| Ordinary B minus ordinary A | 1.1883116712851916e-10 | 2 | [3007,3007] | NONPASS |
| Fixed-rho-A C minus ordinary A | 6.536993168992922e-13 | 0 | [547,547] | PASS |

| Vector comparison | Maximum absolute difference | RMS difference |
| --- | ---: | ---: |
| b_B minus b_A | 1.000444171950221e-11 | 3.6523287976982027e-13 |
| b_C minus b_A | 2.4556356947869062e-11 | 6.515228851992005e-13 |
| ordinary rho_B minus rho_A | 0.00014680086590868058 | 3.108409826546588e-06 |
| ordinary rho_C minus rho_A | 0.000893604225027822 | 1.2897143837667477e-05 |

All four vector pairs are unequal exactly, finite and shaped19612x1. Vector differences have no invented acceptance threshold. J_B and J_fixed_rho_A independently have zero asymmetry; all J inputs to replay were finite. Runtime records also report zero asymmetry for J_A.

## Invariant and provenance audit

Fresh gate matches launch-gate.json, covering the288 grouped preparation pins and exact root approval. The independently computed prelaunch-review hash ac3f85c54bc9f1ade8b2ca4489b836cc9acb0c65dda6c4ec8420da52b84ccd34 matches root approval. The prelaunch review was not modified.

All30 launcher artifact hashes match retained files. Exactly nine numerical arrays exist: three J outputs, three b captures and three ordinary-rho captures. Output hash receipts and launcher worker result agree. Exactly three native metric callback records report Cholesky, finite J and no cached three-index/output tensor. Three factor-state observations are identical in object identity, pointer and content hash; no second factorization is recorded. Raw factor bytes were not saved, so independent content rehash/backward-error analysis is unavailable.

A/B solve receipts report exact original-object return: returned pointer equals ordinary pointer, with independent capture buffers. C reports a distinct returned pointer and ordinary pointer, while retaining ordinary rho_C separately. The frozen hook copies saved rho_A, checks exact equality and nonaliasing, then substitutes that copy. These are checked runtime/source observations; the substituted C return vector itself was not independently serialized as a tenth array. Therefore its exact substitution is not claimed as a separate saved-array replay.

The optimizer baseline was captured after native initialization at the first solve; frozen guards checked optimizer/q_cond/cutoff/molecular state around subsequent calls. There is no runtime failure receipt or invariant rejection. Deferred timestamps represent flush time; they cannot measure actual native factor/pass durations.

Supervisor exit0, no termination reason or monitor error, wall698.8856680409517seconds. Independently recomputed maximum RSS sample3,643,949,056bytes; embedded receipt equals supervisor.json. PID53270 was absent on independent ps lookup. Three calls, zero SCFs, zero PCM builds; sampled memory is not a certified peak or future allocation bound.

## Scientific interpretation

Ordinary same-input repeatability still fails the frozen tolerance. In this one controlled call, reusing rho_A produces a J much closer to J_A and within that tolerance. This supports further investigation at or before the solve/pass2 boundary, while leaving residual pass2 variation observable. It does not prove a unique stage or mechanism causes the ordinary discrepancy.

Small b differences accompanied larger ordinary-rho differences, but their magnitudes or ratios do not establish the metric's condition number. No saved factor, condition estimate or solve backward error is available. There are only two ordinary calls and one later controlled call. Call order, native scheduling, allocation changes from vector copies and rho-dependent pass2 screening remain relevant. C changes the vector and its derived screening consistently; it is not an isolated intervention on pass2 arithmetic.

Independently computed saved-vector Euclidean norms: ||b_A||=43723.32088467428 and ||rho_A||=144.32233127683415. For B, relative b difference is1.1698163034157403e-15 and relative rho difference3.0162385061624005e-06, giving descriptive response ratio2578386450.381399. For C, corresponding values are2.0867838997267213e-15 and1.2514714607599292e-05, ratio5997130133.7135. These are observed relative-change quotients only, not certified condition numbers or backward-error bounds. A frozen rho control cannot respond correctly to a changing density and is not an operator repair.

No exclusive causality, allocator-trap explanation, parent SCF readiness or chemical/life admission follows. Earlier signed and repeatability nonpasses remain preserved, and the new ordinary NONPASS is not erased by the controlled PASS. Diagnostic completion means the prescribed experiment finished, not numerical qualification of ordinary J(P0).

## Evidence binding and review scope

Launch-result SHA256:6c7ce531a0f06fd8e2a4cf643be2f69a68b6a1cfc7356709016d8da3e16b7344.

- J_A SHA256:28b843c19419dd786ecec760b711fabde588319a7eb199050c3af0b4a997f46a
- J_B SHA256:1ed3f4bd876306b270a28cd6ac182de8979392db517b5bfd8c72fa4baa63c5c8
- J_fixed_rho_A SHA256:b5d16ee7357b5676a8e9a425c2a569b91e72fb55ab0478df18248c4239607659

No CRITICAL/HIGH/MEDIUM evidence mismatch found. Programming/remove-ai-slops perspectives were applied during prelaunch review; this terminal pass introduced no production code or tests. No native operator, SCF or synthetic test rerun occurred. Only this report and its evidence receipt were written.
