# Verification record

- Fixed-parameter diagnosis: PASS. Twelve interventions × two chemistries × three seed doses; 1,584 stage records and tighter replay retained. See `diagnosis/verification.json`.
- Prelaunch scientific review: CLEAR, by independent `seed_validation_design` agent after reading PROTOCOL.md, model.py and run.py. Confirmed conservative mean/deviation equations, half-transfer exterior carryover, sample-only observer, unchanged calibration across fixed sensitivities, 18/72 split and 126-start plus nine-direct-objective budget. Review executed no tests or fits. Launch conditional on the required synthetic/numerical checks.
- Prelaunch tests: 35/35 PASS in pinned environment (root executed unittest discovery). Covers model invariants and validation/failure handling.
- Synthetic recovery: all three six-start fits qualified, maximum prediction RMSE 1.28e-12 pp. Parameter truths recovered; no measured outcomes used. See `development-v1/timing.json`.
- Independent numerical implementation: PASS on final model, `independent/results-v2/verification.json`. 2,688 transport quantities and 19,440 short-serial quantities; maximum transport discrepancy 8.38e-13 µM, serial inventory 1.52e-9 µM, PAGE 9.62e-8 pp. Prior verification v1 is retained; v2 captures a subsequent zero-generation argument-validation check, with unchanged equations.
- Primary-source review: PASS, 18 hashes, six bath identities, nine conservation cases, seven new workbook sheets. See `research/verification.json`.
- Official measured run: complete, `results-v1/`, 22.43 seconds before plotting/manifest finalization. 21 optimized fits, 126/126 successful starts, nine direct profile objectives. Every fit/profile qualified numerically. All nine held-out accuracy screens FAIL and remain retained.
- Run refinement: maximum PAGE change 2.14e-7 pp; maximum all-stage source/removal moiety residual 1.34e-14 µM. Saved coarse/refined predictions, trajectories and stage ledgers.
- Preservation: 473 prior/source file hashes match before/after. Frozen code, protocol and source ledgers precede fitting. No official-run code or parameter changes after seeing scores.
- Complete fresh-process refit: `independent/campaign-v2/verification.json` reports PASS_WITH_DOCUMENTED_ARCHIVE_DIFFERENCE. All 44 scientific output files and 46 common frozen input files match exactly after excluding elapsed/UTC fields; zero scientific numerical difference. Saved-parameter replay/arithmetic discrepancy is at most 5.69e-14. Both sets of 810 predictions, all 126 starts, 90 source workbook cells, 840 stages, 144 contrasts and 473 immutable prior/source hashes independently checked.
- Archive qualification: `independent/campaign-v1/verification.json` retains the initial strict-parity FAIL. The refit snapshot adds exactly five ancillary verification files finalized between freezes. There are no removed files and no changed common input hashes. `independent/campaign-v2/verification.json` explicitly states archive_identical=false, computational_inputs_identical=true and scientific_outputs_exact=true; original failure receipt is hash-linked. This was a packaging race, not a changed experiment or numerical mismatch.
- Figures: root visually inspected serial-validation, seed-contrast and training-profile PNGs; readable labels, observed values and all failed scenarios retained. PDF exports also present. All 27 local Markdown links in report/README checked; none missing.
- Final independent code/science review: APPROVE / WATCH, no blockers. Reviewer reran all 35 tests, verified 97 main and 102 refit manifest entries, checked exact source passages and scientific claims, and inspected the reconciled campaign receipt. See [review](../.omo/evidence/rna-seed-transport-review.md).
- Nonblocking maintenance finding retained: the frozen runner recursively captures nested verification snapshots. Future experiment versions should use an explicit computational-input inventory. Current runs remain unchanged; their five-file ancillary difference is fully disclosed.

## Requirement closure

| Requirement | Final disposition |
|---|---|
| Diagnose seed-dependence erasure | COMPLETE: twelve fixed interventions, stagewise contrasts, source correction and retained negatives |
| Implement chemistry-grounded transport | COMPLETE: legacy, finite bath and effective patch models with explicit material ledgers and observer |
| Review sources and additional data | COMPLETE: condition ledger and new seven-sheet Qβ/DMSO workbook; incompatible data excluded from calibration |
| Frozen held-out validation | COMPLETE: disjoint 18/72 rows, 126 starts, 27 profile points, nine fixed scenarios; all accuracy screens FAIL |
| Numerical qualification and refit | COMPLETE: synthetic recovery, 35 tests, independent ODE checks and exact scientific reproduction; archive asymmetry explicitly retained |
| Preserve prior evidence | COMPLETE: 473 prior/source hashes unchanged, no score-driven code changes, all old negative results retained |
| Deliver artifacts and review | COMPLETE: report, source/diagnostic reports, code, plots/PDFs, reproduction commands, checks and independent approval |

Final computational investigation: COMPLETE. Chemical adequacy: FAIL within this protocol. Actual seed-maintenance mechanism, active-catalyst retention and functional inheritance: UNRESOLVED.

Completion is assessed for the reproducible computational investigation. Chemical adequacy and functional inheritance have separate dispositions.
