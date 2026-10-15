# Independent W/V prelaunch review

Prelaunch status: CLEAR
codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

Reviewed PROTOCOL.md, SOURCES.md, sources.py, run.py, test_gate.py, test_sources.py, preparation.json and the original JKFIT numerical thresholds. No scientific operator, PCM surface, molecule construction or SCF was invoked by this reviewer. No approval or launch record was written.

Fresh verification recomputed all 30 preparation pins and the authoritative six source digests. The ledger requires exactly six expected unique filename/digest pairs and exactly six acquired records. The selected WO4 and VO4 XYZ records exactly equal CML finalization geometry and element order. Explicit input charge and scoped adf.runtype/symmetry output charge match -2 and -3; sole Restricted spin evidence maps to spin 0. Unrelated logfile charge records are deliberately excluded. Prepared metadata agrees: WO4 88 AOs, 535 auxiliary AOs, 48 explicit electrons, 60 W ECP core electrons; VO4 87 AOs, 572 auxiliary AOs, 58 electrons, all-electron V. No run-v1 existed at inspection.

The four unit-test methods passed independently in 0.028 seconds. Their malformed source/ledger and rejected campaign-result cases exercise relevant boundary behavior rather than requested-removal or phrase-matching checks. They import no scientific operators or SCFs.

Launch checks frozen hashes, validates sources, reserves run-v1 without overwrite, and runs exactly two ordered 180-second/2-GiB sampled-RSS children through the unchanged supervisor. Each worker has one direct and one RI kernel from identical saved initial density, at most four SCFs total, with no retry path. The exact-case/status/two-SCF/nonempty-check gate rejects missing or failed child results; clean receipt and unchanged-pin checks are required. Parent termination is an orchestration prerequisite in PROTOCOL.md and must be enforced by root before launch; the W/V driver does not implement a parent-process lock.

RKS PBE, def2-SVP/W ECP, JKFIT, grid2, SCF thresholds and solvent settings match the frozen plan. Max AO J error, per-metal Coulomb and total-energy error limits remain 1e-3; direct orbital-gradient threshold remains 1e-3, RI gradient 1e-5 and electron trace 1e-8. Exactly one metal per case makes the energy normalization explicit. Initial J comparisons build the RI metric before either PCM surface. Direct-J uses the intentional direct comparator, not a silent RI fallback. Qualified memory sources retain their existing fail-closed guards and are unchanged/pinned.

Initial/perturbed/converged densities and J matrices, orbital data, overlap, solvent-aware Focks and solvent data are saved for independent postrun checks. Checks/results flush incrementally; failure tracebacks and supervisor receipts retain errors. The two SCFs must converge and all numerical checks pass. No optimization, ADF-energy comparison, target incorporation, experimental holdout or physical admission is claimed.

Findings by severity:
- CRITICAL: none.
- HIGH: none.
- MEDIUM: none affecting the frozen launch.
- LOW: untyped dictionaries and compressed statements remain in the driver, consistent with nearby scientific scripts. The programming and remove-ai-slops perspectives were loaded earlier in this session and applied here. Strict typing/style expectations are not fully met; no material needless production parsing, abstraction or overfit test was identified. Source parsing is necessary boundary validation.

No full-repository lint/typecheck/security scan or numerical support validation was performed. Approval covers preparation only. Actual W/V convergence and approximation errors remain unknown; sampled RSS is not a certified peak. Wait for the actual terminal parent handle before root launches W/V.
