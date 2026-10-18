# Analog learning outcome review

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

## Findings by severity

- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: `documented-scaffold-2026-10-18/analog-learning-replay/input_overlap.py:18` and `replay.py:25` retain the workspace's unannotated numerical-script style. The programming skill prefers typed function contracts and structured result types. This is a maintainability limitation, not an observed wrong result or a reason to refactor frozen historical code. No `Any` cast or type-ignore escape was introduced.

## Scope and independent evidence

Reviewed the full pasted objective, REPLAY_PROTOCOL, REPLAY_CLARIFICATIONS, REPLAY_SCHEDULE_AMENDMENT, INPUT_OVERLAP_PROTOCOL, REPLAY_REPORT, replay.py, preserved replay_flag_assumption.py, input_overlap.py, test_replay.py, test_sources.py, native helper methods, extended methods, source receipts and result artifacts. The exact replay amendment diff changes the schedule interpretation, preserves the fixed mapping tolerances, records schedule indices and permits a fresh output filename. The progress/notepad is `documented-scaffold-2026-10-18/analog-learning-replay/progress.md`; final publication/export is outside this review.

Independent read-only execution used `/USER_HOME/.codex/worktrees/mat-io-runtime-302efd/bin/python -B`. It hash-checked the native Dryad archive against `f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c`, checked each included MAT against its schema hash, and decoded all 191 qualified records. Direct NumPy array equality, without calling the submitted overlap function, confirms TRAIN and TEST are entirely identical within each record, including labels and ordering. There are 1,524 TEST columns and no duplicate source vectors within a run. Exact equality also establishes the frozen 1e-12 overlap conclusion. This did not inspect or score response tensors.

Independent artifact checks confirm:

- `results/replay.json`: 404 rows, 191 failed and 213 excluded. Its recorded original replay.py hash matches the retained replay_flag_assumption.py bytes.
- `results/replay-schedule.json`: 404 rows, 191 failed_mapping and 213 excluded; 8,041 structurally complete snapshots. All recorded provenance hashes match current original files.
- Neither replay contains derived task MSE fields, endpoints or fitted baselines. Stored TestMSE diagnostics remain expressly distinguished from independent recomputation.
- `results/input-overlap.json` provenance hashes match current originals.
- `python -B -m unittest discover -s documented-scaffold-2026-10-18/analog-learning-replay -p 'test_*.py'`: 17 tests passed (12 replay, five source boundaries).

Native Experiment2.m declares DOTEST as test-schedule indices and directly compares TestMeasurements to same-snapshot TLOC-selected TestFreeState. Its measurementConsistency method returns a discrepancy rather than asserting identity. This supports the schedule correction while leaving the frozen identity criterion failed. No new score or tolerance adjustment was used to rescue it.

The retained helper ZIP's SHA256/MD5 and CRC check pass. DataCite software metadata explicitly identifies MIT. An attempted read of `attempt1/zenodo-record.json` raised JSONDecodeError because that preserved unsuccessful response is not JSON; the valid DataCite metadata supplied the license evidence. This reviewer did not overwrite that failure or rerun downloads.

The extended-methods HTML matches the receipt's 293,048 bytes and SHA256 `cd33786e55e8895d11d9b583c2c514042f41eae3142e482887ea03ce79d76b4b`. Its title is “Machine Learning Without a Processor: Emergent Learning in a Nonlinear Electronic Metamaterial.” Appendix E.3/E.4 describes 8-bit conversion and repeated measurements with averages. It supplies no calibrated deterministic difference bound between the two deposited tensor fields. The report's decision to retain the mapping failure is justified.

## Skill-perspective review

Loaded omo:programming, its Python reference, and omo:remove-ai-slops before judging tests and maintainability. The overfit/slop pass found no deletion-only tests, prose pins, tautological requested-removal tests or unnecessary response fitting/extraction. Synthetic asymmetric mapping, conflict/duplicate inputs, train-only baselines, missing snapshots, invalid schedules and immutable output behavior are meaningful behavioral checks. Source-boundary tests exercise corrupted inputs and preservation after partial failure. The separate input audit is required to answer a frozen endpoint independently of response failure; it is not speculative production parsing. The low typing limitation above is the programming-perspective deviation; no material slop-perspective violation was found. No new dependency or abstraction is needed for this review.

## Scientific disposition and limits

Approve the bounded conclusion: the deposited evaluation uses trained inputs. It neither proves nor refutes generalization beyond them. No physical replication, causal held-out adaptation, material renewal, functional inheritance or same-system integration is credited. All twelve original integrated requirements remain open and zero integrated complements are added. Acquisition/integrity and synthetic tests are not scientific validation.

No response replay was rerun and no new errors, fits or baselines were computed. No native MATLAB source was executed. Full publication manifest, export fidelity, remote commit/CI, and a project-wide lint/typecheck were not checked here. Existing frozen results and source bytes were left unchanged. `omo-agent-toolkit ulw-loop status --json` reported ULW_LOOP_PLAN_MISSING, so this report uses the required fallback evidence location.

## Subsequent prepared-publication delta review

Reviewed `/USER_HOME/.codex/worktrees/oct18-state-learning-export-audit` and the clean clone's exporter delta after the scientific review above. This adds publication-scope verification; the earlier scientific and typing verdict remains WATCH / APPROVE with no blockers. No new CRITICAL, HIGH, MEDIUM or LOW finding arises from this delta.

Independent manifest comparison against committed `HEAD:research/2026-10-18/manifest.json` confirms 333 included records, 66 additions, zero removals, and only three modified prior payloads: CONTINUATION_LEDGER.md, progress.md and NEXT_SESSION_PROMPT.md. Every included prepared file matches its published SHA256 and size. The inspected stage contains 20,630,347 payload bytes. Those counts describe this prepared stage before this review append is exported; they are not a claim about the later self-inclusive final manifest.

All previously published scientific payload hashes remain unchanged. The exporter delta adds specific review names and exact authored metadata filenames, plus a browser-native subtree exclusion. Inspection confirms no newly included PDF, XLSX, ZIP, HTML, XML or MATLAB source file, and no browser-native payload (including its README). Native source bytes remain local; acquisition and exclusion provenance remains in the curated snapshot. Authored source-audit prose and acquisition/verifier scripts remain included. Six exporter tests independently passed.

The manifest preserves separate source and published hashes. In particular, replay.json and replay-schedule.json receive declared host-home-path sanitization and consequently different published hashes; input-overlap.json is byte-identical. Frozen hashes inside research results remain original-source references rather than rewritten claims about sanitized bytes. The parent handoff expressly explains omitted native assets, reacquisition, original-versus-published hashes, unpushed local work and the absence of checkout-only scientific reproduction.

Read the new parent-ledger/progress entries and next-session prompt. They preserve the failed binary-DOTEST stage, unchanged 1e-12 mapping failures, trained-input-only overlap conclusion, incomplete inheritance evidence, all twelve integrated requirements and zero new integrated complements. The old acquisition-active progress entry is explicitly superseded by the later outcome entry. Local preparation is not described as remote delivery or CI success.

This review does not establish a final commit, remote push, CI result, final post-append manifest or scientific rerun. Root must regenerate the final export after this append and verify that actual final artifact separately.
