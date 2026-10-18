# Native test-schedule semantics, before task-error computation

The first replay is preserved as `results/replay.json`:191runs stopped on the predeclared binary-DOTEST rule, before any task errors/baseline scores were computed. All404archive rows remain recorded. The exact old program is preserved as `replay_flag_assumption.py`, with the SHA256 recorded for `replay.py` in that result. This is a failed observation-encoding assumption, not failed physical learning.

The subsequent control-only `results/control-schema.json` finds positive finite nonbinary DOTEST values, with no nonfinite flags. This motivated acquisition of the native MIT-licensed helper ZIP, independently hash-checked against the Zenodo file table. Its receipt is `sources/attachment-receipt.json`; no MATLAB code was executed.

New primary evidence in `Experiment2.m` resolves the field:

- Line69 calls DOTEST the indices of the testing schedule with shape1xMES.
- Lines425–427 check that this schedule has one row; line724 uses DOTEST(m)-1 in training-step cycling; lines1280–1290 locate a requested step by matching DOTEST.
- Lines138–140 declare stored target tensors and LearnTimes. Lines172–175 describe every TEST example measured at each recorded measurement step.
- Lines4140–4162 (`checkMeasurements`) and4198–4218 (`measurementConsistency`) directly compare TestMeasurements with the TestFreeState values selected by TLOC+1, with the same snapshot index. This supports the fixed raw/stored mapping check.
- CalcError lines781–787 uses first-minus-second for both differential labels and predictions, while the Figure3/classification convention uses second-minus-first. Applying one consistent sign to both leaves squared errors unchanged. The frozen Figure3 convention stays second-minus-first.

Before any new numerical errors are computed, replace only the contradicted control-encoding rule: require DOTEST to be finite positive integer scheduled training-step indices, strictly increasing with MES entries. Record each scheduled step. It is not a per-snapshot truth flag and cannot supply a DOTEST_false exclusion. Actual measurement completeness still requires finite raw free-state observations and rejects an entire-zero initialized grid when specified inputs are nonzero. Zero complete snapshots remain failed records. Raw/stored agreement is checked on every structurally complete snapshot.

All191-run inclusion, old failures, first/final available endpoints, fixed1e-12mapping/overlap tolerances, voltage conversion, train-only constant/affine fits, frozen earliest observed comparison and causal/generalization limits remain unchanged. The replacement is supported by newly acquired source methods, not chosen to improve a known learning score. Source outcomes already seen remain consumed; no blind-validation claim is made.

Run the amended implementation only into a fresh result name. No old result/protocol is overwritten. Preserve original code hashes separately from any sanitized publication hashes.
