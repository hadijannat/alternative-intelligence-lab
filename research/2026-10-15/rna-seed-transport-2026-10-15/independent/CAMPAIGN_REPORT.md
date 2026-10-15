# Independent campaign audit

**Scientific replay passes, with a documented archive difference.** The full fresh-process refit reproduces all numerical campaign outputs exactly. Saved-parameter replay and independently recomputed arithmetic differ by at most **5.68e-14**. All nine held-out adequacy failures remain present.

The reconciled receipt is `campaign-v2/verification.json`. Its explicit dispositions are:

- `archive_identical: false`
- `computational_inputs_identical: true`
- `scientific_outputs_exact: true`
- `status: PASS_WITH_DOCUMENTED_ARCHIVE_DIFFERENCE`

## Verification coverage

| Evidence | Checked |
|---|---:|
| Main calibration fits | 3 |
| Nuisance profile fits | 18 |
| Direct bath profile objectives | 9 |
| Retained optimizer starts replayed | 126; all successful |
| Selected/direct objectives replayed | 30 |
| Calibration / held-out rows | 18 / 72, disjoint |
| Original workbook values | 90 |
| Scenarios | 9 |
| Ordinary / tighter predictions | 810 / 810 |
| Ordinary / tighter trajectory rows | 216 / 216 |
| Ordinary / tighter stage ledger rows | 840 / 840 |
| Seed contrasts | 144 |
| Prior files unchanged | 473 |
| Common scientific files exactly matched | 90, including 44 output files and 46 frozen inputs |

The strict audit performed 235,193 checks. Every numerical, source, preservation, fitting and scoring check passed; two checks detected unequal full archive inventories. The subsequent reconciliation passed 1,350 checks. Six plot files were checked for retained-file integrity but their bytes were excluded from cross-run equivalence. JSON comparison excludes only `elapsed_seconds` and `utc_before_fit`; runtime versions and scientific metrics remain compared.

The audit independently reconstructed the 18/72 partition, training-only profile membership, all starting coordinates and bounds, start budgets, objective values, successful-start selection and agreement qualification. It recalculated replicate RMSE, condition-mean maximum errors, refinement eligibility and adequacy flags. It checked every saved prediction, trajectory and stage against the saved-parameter model, then separately reconstructed source/feed/removal balances, PAGE normalization, founder decay, newly generated competent inventory and seed-contrast subtraction. The prior full-coupled DOP853 transport verification supplies independent equation implementation evidence; replay alone would not establish that.

All nine pooled held-out scenarios still fail. The patch exchange estimate remains at its declared upper boundary, approximately **10 per FT interval**. Numerical qualification does not establish parameter identification.

## Retained strict archive-parity failure

`campaign-v1/verification.json` remains **FAIL** and is hash-linked from the reconciled receipt. It failed `main_refit_same_file_set` and `main_refit:freeze.json`. The main freeze contains 46 source/evidence files; the refit contains those identical 46 files plus five ancillary files finalized between the freezes:

1. The independent numerical-verification report.
2. Four duplicate source snapshots under `independent/results-v2/frozen/`.

The exact five paths, hashes, roles and modification timestamps are retained in `campaign-v2/archive_delta.json`. Their timestamps fall between the main freeze at `2026-10-15T16:26:51.418174+00:00` and the refit freeze at `2026-10-15T16:27:01.702444+00:00`. No common input changed; none was removed. The model, runner, plotting code, protocol, requirements, observations, workbook, condition metadata and fixed chemistry source are identical. The added files have no execution role in the campaign.

Only these exact five additions are reconciled. The original strict failure was not overwritten, and no scientific field was waived. `campaign-v2` inherits the older receipt's `frozen_files_per_run` field, which describes the 46-file main snapshot; its explicit `frozen_input_counts` records the correct main/refit counts of **46/51**.

## Reproduction

Run `campaign_verify.py --output NEW_DIRECTORY` in the pinned Python 3.12.3 / NumPy 2.4.1 / SciPy 1.16.1 / openpyxl 3.1.3 environment. It verifies completed manifests before beginning and reproduces the strict archive-parity failure. `reconcile_campaign.py --output ANOTHER_NEW_DIRECTORY` independently rechecks the exact allowlist, frozen/live hashes, unchanged manifest receipts, prior evidence and scientific equivalence against the retained strict receipt. Both refuse an existing output directory.

Skipped a third refit and physical experiments. Archive identity remains false; validated numerical replay does not establish correct physical transport or functional inheritance.
