Task: investigate seed-dependence loss and test a chemistry-grounded transport model with held-out prediction and retained negatives.

State: COMPLETE. Official comparison, full fresh-process refit, independent numerical/campaign verification and final review completed. Earlier laboratories untouched.

Completed: prior results and code inspected; independent fixed-parameter diagnostic completed; source recheck identifies washing of PAGE aliquots rather than demonstrated removal of the continuing extracellular pool. Removing decay/leakage separately does not rescue seed dependence. Apparent reporter-ratio rescue under no fresh feed is largely historical product in a shrinking denominator.

Decision: model an explicit exterior pool carried through FT, incubation and serial sampling. Frozen prior baseline chemistry; compare irreversible sink/global mean, finite common bath and finite patch exchange. No geometric Monte Carlo without measured geometry. Retain uncertainty in exterior activity and bulk-to-exterior rate transfer.

Protocol written: three fixed families, deterministic finite patches, nine fixed exterior scenarios, 18 calibration/72 held-out rows, six starts with 120 evaluations, training-only profiles, no benchmark selection. Main and independent implementations are being checked using synthetic inputs. Source review acquired a 2026 Qβ/DMSO dataset; its different chemistry excludes it from fitting.

Completed: 35 tests, synthetic recovery, 600 independent ODE/event checks, prelaunch review, frozen comparison, all 126 measured optimization starts and nine direct profile objectives, nine scenarios and tighter replay, full fresh-process refit, report and figures. All nine held-out accuracy screens fail. Primary RMSE legacy4.479/bath13.564/patch14.331 pp; observed G7 seed contrast9.828 pp versus .0083/.2448/.2504 predicted. No score-driven changes made.

Final verification: 44 scientific outputs and 46 common frozen inputs reproduce exactly. Two strict archive-parity failures are preserved because the refit captured five additional ancillary verification files. The reconciled receipt explicitly distinguishes nonidentical archives from identical computational inputs/results. All473 prior/source hashes unchanged. Independent final review APPROVE/WATCH, no blockers; recursive evidence freezing is a documented nonblocking maintenance issue.

Required work remaining: none. Chemical adequacy fails all nine screens. Conditional transport assumptions, actual maintenance of seed dependence and functional inheritance remain unresolved scientific questions; no further fitting was performed after viewing scores.
