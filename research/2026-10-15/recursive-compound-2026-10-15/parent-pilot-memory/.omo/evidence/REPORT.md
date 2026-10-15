# Parent MemoryRI pilot preparation evidence

Scope: only parent-pilot-memory. No parent launch, publishing or commit. No active ulw attempt: toolkit status returned ULW_LOOP_PLAN_MISSING, so artifacts are in this folder's .omo/evidence.

## Executed acceptance scenarios

1. Standard-library unit/synthetic suite. Invocation: `python3 -B recursive-compound-2026-10-15/parent-pilot-memory/test_pilot.py`. Binary observable: exit0, six tests OK. Artifact: `.omo/evidence/tests.txt`. Exercises exact allocation arithmetic and dimension rejection, 57-pin count/content rejection, all six failed-child variants, terminal flags, independent-review missing/stale/failed variants, exclusive run folder rejection, supervisor success and wall timeout.
2. Synthetic supervisor child success. Invocation is recorded exactly in `.omo/evidence/synthetic-success/supervisor.json`. Binary observable: returncode0, no termination reason, all five requested thread variables equal1. Artifacts: supervisor.json and stdout.txt in that directory.
3. Synthetic supervisor wall cap. Invocation is recorded exactly in `.omo/evidence/synthetic-timeout/supervisor.json`. Binary observable: nonzero returncode and WALL_LIMIT. Artifact: supervisor.json in that directory. These synthetic children do not import chemistry.
4. Live read-only qualification verification. Invocation: load pilot.py using importlib, call `qualification_manifest()` and `original_pins()`. Binary observable: no exception, 57 unchanged pins, all six terminal supervisor/result receipts accepted. Artifact: `.omo/evidence/terminal-qualification-verification.json`, including hashes of33 terminal artifacts. This also records `parent_run_exists:false` and `pyscf_imported:false`.
5. Preparation freeze. Invocation: `python3 -B recursive-compound-2026-10-15/parent-pilot-memory/pilot.py --prepare`. Binary observable: exit0 and pending preparation record; artifact: `preparation.json`.
6. Independent launch gate closure. Invocation: import pilot.py and call `validate_gate()` before any approval exists. Binary observable: FileNotFoundError specifically for independent-root-review.json, SCFs_launched0. Artifact: `.omo/evidence/launch-gate-pending.json`.

## Prepared runtime requirements, not executed evidence

Driver contains chemistry/dimension/configuration guards, metric-before-PCM stage, actual alias receipts, storage checks, original supervisor reuse, initial and per-cycle partial checkpoint, native checkpoint/log, failure and terminal receipts. These parent-size paths are deliberately unexecuted and require independent code review plus a later authorized bounded run. Synthetic tests do not establish actual parent aliasing, convergence, peak memory, checkpoint performance, or scientific validity.

## Risks

9.893259406GiB arithmetic leaves about0.107GiB below the10GiB sampled guard. Unbounded native/allocator transients can exceed it between samples.900second limit includes initialization/checkpoint IO. Kills before initial density yield no array checkpoint; latest completed stages/native output survive. All physical, target, optimization and stability claims remain false/unverified. Approval file is an auditable attestation, not authenticated reviewer identity.
