# Explicit-BLAS ordinary-J prelaunch review

- codeQualityStatus: CLEAR
- recommendation: APPROVE (bounded diagnostic design only; separate root launch authorization required)
- blockers: []
- Date: 2026-10-16
- Reviewed preparation SHA256: `13cf6df31ebf08fd49d873e96d77843dd1df4cbe8e4039488a0376bf0d90d51e`

## Scope and evidence

Reviewed the complete new `recursive-compound-2026-10-15/parent-explicit-blas-j/run.py`, `test_run.py`, protocol, preparation and qualification artifacts, plus the actual inherited saved-metric explicit controller, stage-localization setup/capture, repeatability runtime/storage guards and comparison, signed-operation restrictions, memory specialization, and process supervisor. The new directory is untracked; its complete contents, rather than an empty git diff, were the review input. No separate notepad was supplied. `omo-agent-toolkit ulw-loop status --json` returned ULW_LOOP_PLAN_MISSING; this report uses the specifically assigned fallback evidence path.

Independently verified preparation SHA and 428 of 429 grouped pins, with zero mismatches. The only skipped grouped pin is `parent-metric-solve-diagnostic-v2/run-v1/original_metric.npy` (3,077,044,480 bytes), assigned to root for full hashing. Checked pins include the new source/tests/protocol/qualification, all inherited controller/setup sources, qualification records, prior J matrices, prior replay outputs and independent replay review. Hash verification establishes byte identity, not scientific validity.

At inspection, neither `parent-explicit-blas-j/independent-root-review.json` nor `parent-explicit-blas-j/run-v1` existed. No approval file or run directory was created by this review.

## Findings by severity

CRITICAL: none.

HIGH: none.

MEDIUM: none.

LOW — `parent-explicit-blas-j/run.py:181-183`: the final gate catches every Exception and discards its reason. This violates the programming/remove-ai-slops error-transparency perspective. It is not a launch blocker: `same` stays false, `completed` becomes false, and launch returns 1. It cannot turn an integrity failure into success, but diagnosis of a final-only missing/changed artifact is weaker. Preserve this caveat rather than editing frozen inputs during review.

LOW — the new driver follows the inherited untyped script style, and the tests use unittest rather than the programming skill's preferred typed/pytest style. No strict typecheck claim is made. This is maintainability debt, without a demonstrated failure in this bounded, frozen single-use flow; broad modernization would exceed the current scope.

## Bounded-execution checks

The new launch is exclusive (`mkdir(exist_ok=False)`) and starts one fresh interpreter through the inherited supervisor with 600 seconds and a 10 GiB sampled RSS guard. The supervisor fails closed on unavailable RSS monitoring and terminates its owned process group. Sampling and termination grace permit unsampled memory peaks and wall-time overshoot; these are not hard OS resource ceilings.

The unchanged explicit controller verifies environment, binary hashes and common dpotrf symbol identity; checks initial configured getters 4/4; sets BLAS1 while retaining PySCF4; snapshots before/after setup and each J; and records getter restoration without claiming restoration of implicit mode or measured team sizes.

The inherited setup builds the frozen Mo36 parent dimensions (196 atoms, 3068 AO, 1568 electrons, charge -8), method and auxiliary basis. Runtime/molecule checks run before and after each call. SCF/initial-guess/PCM-build entry points are forbidden; PCM state is checked unbuilt. Storage checks enforce one factor, aliasing, immutable Fortran layout, stable factor contents, metric-call count, no retained ERI/three-index data, and unchanged method settings. The new wrapper hashes and writes the original metric before destructive factorization; the second-factor attempt fails before execution. Unequal saved/new metric hashes are descriptive and do not claim a matched causal comparison.

`OrdinaryCapture` rejects C before the inherited capture executes, and A/B return the original ordinary solve object unchanged. Exactly two positive P0 requests run on the same object and factor. P0 digest and call/capture counts are checked. Each returned full J and each b/rho copy is saved, closed and hashed before post-return runtime/storage checks. Both calls precede numerical classification. Structural/native failures remain incomplete with available arrays retained; finite numerical tolerance failures remain completed diagnostic outcomes.

Classification uses the inherited full-matrix absolute 1e-10, relative-zero comparison, unchanged symmetry threshold, and separate historical-first-J comparisons. No energy scalar replaces the full matrices, no rho substitution, tolerance relaxation or retry is introduced. Historical output is explicitly not an independent accuracy oracle. Vector differences are descriptive, without a new threshold.

## Independent test execution

Command (no --record):

```text
recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python3.12 -B recursive-compound-2026-10-15/parent-explicit-blas-j/test_run.py
```

Observed exit 0; six tests passed in 0.006 seconds:

- ordinary return identity and C rejection;
- first arrays retained on storage failure;
- missing approval and changed-pin gate rejection;
- one child, exact resource arguments and exclusive output;
- original metric receipt before destructive factorization and rejection of a second factor;
- two full outputs before nonpass classification, extra-call rejection and exclusive array save.

These tests exercise behavioral seams and failure handling. None is deletion-only, prose-pinning, tautological, or merely a mirror of implementation constants: the resource arguments are the external protocol contract. Classification is mocked in sequencing tests, so these six tests do not establish native numerical accuracy or directly retest the inherited matrix arithmetic. Source inspection verified the unchanged threshold and comparison path.

## Skill-perspective check and limits

Loaded `omo:programming`, its Python reference, and `omo:remove-ai-slops`; applied both to production and test code. The LOW findings above are the identified perspective deviations. No unnecessary parsing, normalization, data extraction, speculative abstraction, deletion-only test, or implementation-mirroring test was found. Pin and array validation serve actual evidence/native boundaries and should remain. The inherited temporary patch seams provide mockability and preserve frozen native behavior; a new abstraction layer is unnecessary for this task.

No native parent integrals, J, factorization, solve, SCF or PCM build was executed. No source or frozen artifact was edited. No lint/typecheck/security-suite result is claimed; this was a bounded prelaunch review with six mock tests and direct source/pin inspection. Root must complete its assigned whole-metric/full-manifest audit and issue separately bound launch approval. Numerical parent repetition is only a prerequisite diagnostic: exact Mo34WV target chemistry, independent accuracy, retention, inheritance, life/intelligence functions and scientific admission remain unverified.
