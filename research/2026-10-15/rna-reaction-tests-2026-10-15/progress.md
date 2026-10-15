State: complete.

Objective: diagnose the revised RNA model's failure and test alternative reaction mechanisms with held-out validation, retaining negative results.

Completed: all six candidate conditions fitted and tested; all 248 fits resolved under the frozen rule, with 22 unsuccessful starts and six fits without two-start agreement retained. Combined independent efficiencies/inactivation wins ordinary dose validation (3.145 pp vs 10.631 baseline); nested score 3.551 pp, late score 4.148 pp. Every accuracy screen fails, including both historical transport closures (4.479/4.975 pp). All full-fit and transport numerical checks pass. All 30 software tests pass. Saved-parameter replay reproduces all 2,512 prediction rows exactly. A complete fresh-process refit matches 262 scientific files; the independent audit verifies 392 splits, 20 profiles, 240 state rows and prior-source preservation. REPORT, README and checks document negative results and limits.

Implementation ownership: model worker writes only model.py/test_model.py. Root owns protocol and integration. Existing laboratories remain unchanged. No new compatible numerical external validation dataset has been acquired; cross-validation is retrospective.

Outputs: results-v1/ and verification-v1/ contain frozen sources, fits and full outputs. independent-verification.json and saved-parameter-replay.json hold verification receipts. comparison.png is a separately rendered presentation figure with corrected title spacing; the original frozen figure is preserved.

Open issues: physical mechanism, active-F1 retention and functional inheritance remain unestablished. No new compatible external numerical holdout was acquired. Six bounded optimizations lack multistart agreement; no global-optimum claim is made.

Final review: APPROVE with no blockers; WATCH only for low-priority interface typing. All eight presentation documents and local links checked; corrected figure visually reviewed. Every WORKPLAN completion requirement has an evidence row in checks.md.

Next action: no implementation work remains for this investigation. Further mechanistic claims need the matched activity, binding and inheritance measurements described in REPORT.md. Do not reinterpret software acceptance as a passed chemistry or inheritance claim.
