# Completed computational verification

The [full offline receipt](verification-v1/verification.json) reports `passed`. Its commands, logs, source hashes, dependency versions and code/ledger snapshot are retained in `verification-v1/`. The tested command is in [README.md](README.md).

| Check | Observed result | Scope |
|---|---|---|
| Original-study extraction | 529 source cells and 148 previously used values match | 529 includes the original 148; these counts are not independent new observations |
| New retention sources | 16 checks pass; 100 normalized rows | Source hashes, units, 77 reconstructed cleavage values, phase and exchange exports |
| New inheritance sources | 23 checks pass; six exports | Source hashes, workbook exports/missingness, QT45 archive integrity and FASTA inventory; no fidelity re-estimation |
| Chemical and event tests | 10 pass | Moieties, nonnegativity, inactive reporter, zero B, saturation limit, inaccessible reservoir, both exchange closures, species-specific loss, founder bounds, feed accounting, refinement and input rejection |
| Full refit | All 40 dose folds resolve; all 14 compared artifacts match | 12 scientific JSON/CSV artifacts plus two original-model diagnostic artifacts |
| Saved-parameter replay | 216 predictions reproduced exactly | Current/frozen source and output hashes also match |
| Preservation | 71 recorded inputs and 264 prior non-cache files unchanged | Source audit separately counts 269 old files including caches |
| Numerical refinement | Maximum reporter difference 3.784×10⁻⁶ pp | Six mode/seed checks; threshold 10⁻⁴ pp |
| Material accounting | Maximum discrepancy 6.301×10⁻¹⁵ µM | Chemical moieties plus feed, transfer and losses |
| Figure review | Rendered and inspected | Axes, units, measured points, fitted curves, model comparison and evidence labels readable |

JSON comparisons exclude only top-level `elapsed_seconds`; CSV comparisons use exact hashes. Timestamp-bearing `freeze.json` and its dependent `manifest.json` are not compared across runs, but the saved-run replay verifies their content hashes and all retained artifacts. The runtime used Python 3.12.3, NumPy 2.4.1, SciPy 1.16.1, matplotlib 3.10.8, openpyxl 3.1.3 and PyMuPDF 1.27.2.3. The global SciPy installation was not altered.

The first attempt failed while serializing a NumPy boolean in the refinement output. [Repair details](model/RUN_REPAIR.md) preserve the failure and limit the fix to native scalar output plus a regression assertion. The completed `results-v2` run and independent refit use the same repaired code and frozen scientific protocol. [Repair comparison](model/repair-comparison.json) preserves common-output agreement within 10⁻⁸ pp; five chemical-fit artifacts are byte-identical.

[Independent review](review-independent.md): APPROVE, no blockers, code-quality WATCH. Two LOW notes concern a future unresolved-candidate bar being displayed as zero and incomplete type annotations. All current candidates resolved; neither affects this figure or these calculations.

Passing these checks establishes computational reproducibility, source fidelity and accounting. Both transport models and all eight retention scenarios still fail the scientific accuracy screen. No active-F1 retention, physical pedigree or functional inheritance was independently measured. Dedicated lint/type/security scans, physical experiments and full sequencing reanalysis were not performed.
