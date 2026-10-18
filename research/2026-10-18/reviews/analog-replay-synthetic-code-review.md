# Analog replay synthetic code review

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

Scope: `documented-scaffold-2026-10-18/analog-learning-replay/replay.py` and `test_replay.py`, reviewed as newly added files against `REPLAY_PROTOCOL.md`. This is approval of the synthetic computational implementation only. Native response values were not opened and the real replay entry point was not executed. No implementation files were edited.

The requested review concerns structural snapshot eligibility, native-to-logical mapping, units, overlap/conflicts, train-only conventional fits and chronological endpoints. Parent clarified that raw/stored mapping is compared only on structurally complete snapshots; a mismatch on any such snapshot stops that run's numerical interpretation. This clarification was applied. No separate notepad was supplied; the frozen protocol and task messages provided the acceptance criteria.

`omo-agent-toolkit ulw-loop status --json` returned `ULW_LOOP_PLAN_MISSING`, so this report uses the required fallback evidence path.

## Evidence

- Independently executed `/USER_HOME/.codex/worktrees/mat-io-runtime-302efd/bin/python -B -m unittest -v test_replay.py` from the experiment directory: 8 tests passed, 0.011 seconds.
- Reviewed source SHA256: `9f953db04fe7fad3c014b42e9b02cae6313e976a7aac34ec56b77f8640c18c0b`.
- Reviewed test SHA256: `0a0767c18b917e15409f988874ed7852633f2474401fdb06958e63b571fdc25a`.
- Reviewed protocol SHA256: `d5e2411412b68f50b3f8f1bd96fda33eba3276a9b21ccb0c401f1124e62ce4e9`.

## Findings by severity

### CRITICAL

None.

### HIGH

None. No scientifically material correctness omission was found within the synthetic review scope.

### MEDIUM

- `replay.py:20–70`: analysis helpers expose untyped array/dictionary contracts. The programming perspective calls for typed boundaries and result contracts; these functions provide neither. The explicit runtime shape checks and meaningful synthetic tests reduce immediate scientific risk, but result-schema changes cannot be checked statically. This is a maintainability concern, not a demonstrated incorrect result.
- `replay.py:237`: the per-file `except Exception` also catches programming errors and classifies them as failed records. Failures remain visible in saved records and status counts, so they are not silently discarded; nevertheless, the programming/remove-ai-slops perspectives favor separating expected decode/validation failures from unexpected implementation defects. No evidence of a presently triggered defect was found.

### LOW

- Tests do not directly exercise rank-deficient affine design, differential native-target conflict with equal logical labels, or capacitor endpoint selection when the first/final native rows are invalid. Inspection found the relevant implementations consistent with the protocol. These are focused optional coverage opportunities, not requests for blanket test expansion.

## Skill-perspective check

Loaded `omo:programming`, its Python reference, and `omo:remove-ai-slops`. Both perspectives ran over production and test code. The typing and exception concerns above violate the programming perspective; the broad exception also triggers the slop perspective. No deletion-only, removal-verification, tautological, implementation-constant-mirroring or prompt-prose tests were found. Tests assert calculable outputs, eligibility, failure behavior and TEST-label independence. No unnecessary scientific response extraction, normalization chosen to force agreement, speculative model, or needless abstraction was found. Schema and finite-value checks occur at the external array boundary and are justified by the frozen protocol.

## Verified and unverified scope

Verified synthetically: asymmetric axes, differential sign, single-ended outputs, full-grid finiteness, structural placeholders versus legitimate zeros, complete-only mapping, run-level stop on measured mismatch, chronological endpoints, source-boundary overlap, target conflicts, train-only constant/affine fits, learning-time failures, zero-denominator handling and nonfinite capacitor state.

Not checked: native data outcomes, main-entry integration, runtime decoding equivalence, publication/export, static typing/lint, or scientific conclusions from physical observations. The source hash and native-file inventory guards were read but not executed. Synthetic approval does not establish generalization, causal physical adaptation or integrated goal completion.

## Schedule amendment re-review

The preceding review is preserved as historical evidence for its exact hashes. This section supersedes its binary-DOTEST interpretation and LOW coverage observations. Read `REPLAY_SCHEDULE_AMENDMENT.md`; reviewed the current implementation diff against preserved `replay_flag_assumption.py`, the new synthetic tests, and current mapping/provenance/output handling. The source-method conclusion in the amendment was accepted as the review input; this synthetic review did not independently open native MATLAB/source response data.

Current decision: codeQualityStatus WATCH; recommendation APPROVE; blockers []. CRITICAL: none. HIGH: none. MEDIUM: the previously documented untyped contracts and broad per-file exception handling remain. LOW: the three prior coverage opportunities are now covered. No new scientifically material issue found.

- Current `replay.py` SHA256: `8056b774b9d6af35f04fff57fa617ce65a709c44bebb41df81b47d957cbdbeb1`.
- Current `test_replay.py` SHA256: `21a232e21799fff4e87bf421e31676cb70fd50d9183b2cf3cad7219d5b1dab54`.
- Schedule amendment SHA256: `32b49b8b7f768cdace259da5dc24614dc23fc05afaff2dfdd7e84cd8ab05ceb5`.
- Independently reran the same qualified-runtime unittest command: 12 tests passed in 0.016 seconds.

The amended code requires finite positive integral strictly increasing scheduled steps, records them verbatim, and accepts gaps without altering cumulative LearnTimes or introducing extra observations. Raw-state completeness remains separate. Synthetic tests reject zero, negative, nonfinite, duplicate, fractional and decreasing steps. They also now cover rank deficiency, different native targets with equal logical differential labels, source drift, no-complete-snapshot failure, and capacitor RMS at selected endpoints when native edge rows are invalid.

The fresh JSON basename is constrained to the results directory; slash/backslash traversal and existing files are rejected. The final exclusive-create open remains in place, protecting against a file appearing after the early existence check. The amendment hash is included in output provenance. The narrow diff does not alter scoring, fitting or endpoint rules.

Both skill perspectives were reapplied to the amended code/tests. The remaining MEDIUM concerns above persist; tests remain behavioral and boundary validation is justified. Native replay/result files were neither opened nor executed by this reviewer. Main-entry integration, static typing/lint and physical/scientific conclusions remain outside this review.
