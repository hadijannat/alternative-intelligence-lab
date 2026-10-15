# Verification record

This record separates completion of the investigation from adequacy of its model. Both measured campaigns and independent numerical verification are complete. Every predictive adequacy screen fails; those failures are retained as results.

| Requirement | Verdict | Evidence | Correction or limit |
|---|---|---|---|
| Diagnose high-dose and late-time failures | pass | diagnosis/REPORT.md; verification.json; residuals.csv | Independent DOP853 replay; conflicting branch errors retained |
| Diagnose transport failures | pass | transport_diagnosis/REPORT.md; verification.json | Schedule/accounting checked; seed dependence and cross-assay mismatch remain |
| Ground candidate topology in primary sources | pass | research/REPORT.md; sources.json; verification.json | No compatible new numerical holdout; external rates not treated as same-condition calibration |
| Freeze design and scientific inputs before fitting | pass | PROTOCOL.md; results-v1/freeze.json; frozen/ | Retrospective development on previously inspected data |
| Implement conservation, occupancy, PAGE and transport limits | pass | test-results.log; ../.omo/evidence/rna-turnover-tests-review.md | 50 tests passed; 36 core and 14 independent-verifier tests; final reviewer reran current suite |
| Recover known synthetic curves | pass | development-v1/timing.json | 6.15e-9 pp curve RMSE; not experimental validation or unique parameter recovery |
| Independently implement and check bulk chemistry | pass | reduction_check.py; reduction-verification.json | Five-state DOP853 versus twelve-state LSODA; 1,800 comparisons; not an independent transport implementation |
| Whole-dose and nested validation | pass: executed; fail: adequacy | results-v1/validation.json | All four fixed families fail; nested RMSE 3.226 pp; simplicity rule retains baseline |
| Late-time and joint high-dose/late-time validation | pass: executed; fail: adequacy | results-v1/late_time.json; joint_challenge.json | Every family fails both challenges; all held predictions retained |
| Transport sensitivities with frozen bulk chemistry | pass: executed; fail: adequacy | results-v1/transport.json; transport_refinement.json | All sixteen scenarios fail; 48 refinement checks pass; no benchmark-selected winner |
| Preserve all failures and earlier results | pass | independent-verification.json; results-v1/manifest.json | 161 fits/966 starts retained; one start-agreement warning; all 268 audited previous hashes unchanged |
| Independent accounting and saved-parameter replay | pass | independent-verification.json; saved-parameter-replay.json | 3,288 predictions, 264 splits, 5 profiles, 200 profile states and 160 full states checked |
| Complete fresh-process refit | pass | verification-v1/; independent-verification.json | 63,917 scientific numbers across 193 files match exactly; identities exact; clocks and plot bytes excluded |
| Report and figures | pass | REPORT.md; README.md; results-v1/comparison.png; transport_comparison.png | Both official figures visually inspected; all local report links resolve |
| Independent final review | pass | ../.omo/evidence/rna-turnover-tests-review.md | CLEAR / APPROVE; no blockers; independently reran 50 tests and complete verifier; approval covers investigation, not model adequacy |

No wet experiments, active-retention measurement, prospective validation, publication or functional-inheritance demonstration are claimed.
