# Independent terminal review: signed parent RI-J

Evidence review status: CLEAR
Scientific classification: FAIL_FIXED_FIRST_SIGN_CRITERION; SECOND_PROBE_NOT_EXECUTED
Recommendation: retain the negative result; do not promote it to a passing campaign or rerun this frozen attempt.

## Verified terminal state

Read the original run-v1 first checks, failure traceback, stage log, metric receipt, factor records, supervisor and launcher result. Independently invoked only the read-only gate check under the qualified env-aligned interpreter with OMP4/BLAS1: current frozen pins and approval match launch-gate.json. The launch result embeds exactly the standalone supervisor receipt. PID 25053 was absent from `ps -p 25053 -o pid=,stat=,command=` (exit 1, no process row). No numerical work was launched during this review.

Child exit code 1, wall time 243.2830698749749 seconds, no termination reason and no monitor error. Independently recomputing the maximum over 1136 RSS samples gives 3,742,777,344 bytes, equal to the receipt. This was an application-level failed numerical check, not a recorded signal, timeout, RSS termination or monitor failure. The sampled maximum is not a hard peak bound.

The first returned J is recorded finite and exactly symmetric under the implemented comparison (maximum asymmetry 0). Maximum sign residual is 5.282743131829193e-10 against fixed absolute 1e-10 and rtol 0, about 5.28 times the allowed tolerance. Therefore the first sign test failed. The code preserves the check before raising ValueError at run.py:261. No tolerance reinterpretation or relaxed acceptance is justified after observing this result.

One native J callback and one 19612-square metric factor are recorded. Factor aliasing used the same pointer, with read-only Fortran storage. There is only one factor-state observation, so reuse across a second call or oracle was not tested. The first callback records finite J and absent cached three-index/tensor output.

Stages show the native call beginning at 9.11247645795811 seconds and returning at 242.22937583294697 seconds. The first buffered-file checkpoint begins at 242.27792695804965 and closes at 242.27825079101603 seconds; the file exists with 48 bytes. The failure occurs after that close. This particular first signed-density return and bounded buffered close completed without the earlier allocator trap. That observation neither rules out latent corruption nor establishes why a different earlier process failed.

No first_full_arrays_released stage, second native call, second density/check file, selected oracle, second post-call file or final worker result exists. The first criterion stopped the run as specified. The launcher retained INCOMPLETE_OR_FAILED_SIGNED_J, gate_unchanged true, empty worker result, and the missing-second-check artifact exception. Its empty artifact_sha256 map results from the all-artifact comprehension aborting at the missing second file; existing raw artifacts are still present and were independently hashed below.

## Replay limitation

No NPY, NPZ, H5 or HDF5 numerical output exists anywhere under this run-v1. The driver never saves its computed negative-density J, metric or residual matrix. Thus the failing J and residual cannot be independently recomputed from retained arrays. The original positive saved J and cycle-zero density remain upstream, but they cannot recover the negative output. The scalar maximum cannot identify the offending AO pair, residual distribution, relative scale, or whether a common metric matched across processes. This review verifies the recorded failure and code/evidence consistency; it does not independently replay the numerical residual.

## What is not established

- The fixed indefinite D01 probe and its ten selected shell-pair oracle checks were not executed.
- No same-sign repeatability or same-process positive/negative control was measured.
- OpenMP reduction variability is a possible hypothesis, not an inferred cause. Numerical summation, screening effects, cross-process differences and other implementation behavior remain unseparated.
- No parent SCF, PCM, functional inheritance, chemical stability or intelligent-life requirement is validated.
- RSS below the guard does not refute the native requested-allocation audit or certify future runs.

## Next discriminating action

First design and review a separate campaign that retains returned arrays (or a fully specified sufficient residual record) before any acceptance abort. Preserve this campaign unchanged. A matched same-sign repeat control alongside a sign-reversed request, using a common fixed metric and unchanged numerical method, can compare same-sign variability against sign-reversal residuals. Saving the numerical outputs permits independent replay, maxima coordinates and residual distributions. Thread-count comparisons should be a separately frozen follow-up if needed, not an assumed explanation or a retroactive threshold adjustment. Any new protocol must explicitly budget its additional calls and decide in advance which failed checks stop execution; no such native execution is authorized or performed by this review.

## Evidence hashes

- first-checks.json: 7aff4f413c90c6a767b5c57a549022fc01af3518814ca8ac00594010ca567e6b
- supervisor.json: dfe5519055541e6879e7e45fd5e09821908d36c02bfcf49289bc9b2a6550b74b
- launch-result.json: 7f3e86c1c59103a0d8ee23b65a06a4dcd5cc8262776df43202cecdd7f2916b42
- failure.json: 0f11f095269472e5a00a4da55b7830690c2f86e265bed0a21b5a3382604bcbe4
- stages.jsonl: eb8f33ec04ef752992c5cd212745e149138582eae640c4629ef8c6f18ec73e9f
- metric-calls.jsonl: cb5ebdae378c02ef70b78e5c9741f9700a0fa38bfdb0d7a87dea2f4ff516abaa
- factor-aliases.json: c744cc93a6b77ca628c8e1f1dccd6cae5e9d4c78168957a7321ae63b0fe9be56
- factor-states.json: 65a1d4c9c85a40bec4fe03b0c6bdd036f1269925f1fa52e667e31747b6283d3c
- post-call-1.bin: 56765fcab9aece972242aec2ad517d26b46b89c6a9954e3ca80d1885602db418

No frozen implementation, preparation, threshold or original failure file was modified. No rerun or additional operator was performed.
