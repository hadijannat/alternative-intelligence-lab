# Requirement-by-requirement checkpoint

All paths below are relative to this directory. Numerical PASS means only the stated check passed. No required target function is fulfilled by a source-table or software check.

| Requirement | Verdict | Evidence | Correction or remaining work |
|---|---|---|---|
| Recover complete parent heavy component | PASS, parent reference only | identity/parent_heavy.xyz; identity/site_mapping.json; identity/check.py | Hydrogen/protonation and target identity unresolved |
| Preserve incomplete extraction | PASS | identity/.omo/evidence/checks.json | 2.0 Å control remains Mo4O11 and rejected |
| Count full-model electrons/basis honestly | PASS, arithmetic only | identity/next-step/feasibility.json; identity/next-step/check.py | No full-cluster build, SCF, gradients or optimized structure |
| Small-reference direct SCF and continuum | PASS, runtime only | identity/next-step/method-qualification/result.json | Four hypothetical reference/control cases; no chemical accuracy or full-parent admission |
| Small-reference analytic nuclear derivative | Original FAIL preserved; corrected diagnostic PASS | identity/next-step/method-qualification/derivative-result.json; identity/next-step/method-qualification/grid-response-result.json | Same 1e-4 Eh/bohr limit and two finite differences; grid response required; no full Hessian or parent derivative |
| Hypothetical parent H inputs | PASS, computational input only | parent-inputs/metadata.json; parent-inputs/checks.json; parent-inputs/REPORT.md | Four inputs; ten malformed controls reject; no measured H or physical admission; short PT57 H-Mo contact retained |
| Full-parent pilot | NOT RUN | parent-pilot/PROTOCOL.md; parent-pilot/pilot.py; parent-pilot/test_pilot.py | Fixed P0_A input and bounded supervisor prepared; no full-parent electronic result |
| Primary fixed-geometry site calculation | PASS, mismatch only | site_chemistry/evaluate.py; site_chemistry/site_scores.csv; site_chemistry/.omo/evidence/validation.json | No strain or energy; Mo7 parent discrepancy and all V deficits retained |
| Sequential energy alternatives | PASS, bounded evidence assessment | energy/candidates.json; energy/checks.py | Four roles evaluated; no target energy-maintenance cycle |
| Boundary feed inventory and identity distinction | PASS, accounting only | boundary/checks.py; boundary/REPORT.md | Five roles evaluated; no active-cluster permeability or wall renewal |
| Restricted founder-capacity bound | PASS, conditional bound | heredity/check.py; heredity/.omo/evidence/checks.json | Replaced two tautological tests; six actual calls and eleven invalid-input tests; new-material inheritance unverified |
| Memory evidence and SI-unit handling | PASS, source fit/accounting only | adaptation/checks/run.py; adaptation/REPORT.md | Four roles evaluated; no target learning, causal resource control or renewal |
| Speciation source rows and limits | PASS, published-table evidence | compatibility/selected_rows.csv; compatibility/check.py; compatibility/raw/table-page-*.png | No raw-FID replay; source zero/100 not absolute recovery; mean discrepancy preserved |
| Nominal-versus-final medium distinction | PASS | compatibility/REPORT.md; compatibility/.omo/evidence/checks.json | Matched starting buffers have different final pHs; no joint mixture observed |
| Independent quantitative review | PASS with repaired test concern | review/; ../.omo/evidence/recursive-quantitative-review-code-review.md | Six original quantities and later NMR/BVS results independently checked |
| Final executable checks | PASS: eight commands, all exit 0 | ../.omo/evidence/recursive-integration-verification.json | Does not validate chemistry; command outputs and scope retained |
| Root synthesis and links | PASS, documentation scope | review/root-synthesis-addendum.md | Abbreviated evidence paths subsequently qualified; this review predates the later quantum qualification |
| Exact target in operating medium (I) | UNRESOLVED | identity/identity_admission.json | Measured structure/speciation/oxidation/protonation absent |
| Energy coupled to target function (E) | UNRESOLVED | energy/REPORT.md | Complete useful regeneration cycle unmeasured |
| Resource and waste transport (T) | UNRESOLVED | boundary/REPORT.md | Species/flux/active-fraction joint measurements absent |
| Maintained renewing boundary (B) | UNRESOLVED | boundary/REPORT.md | Formation and persistence are not demonstrated renewal |
| Active renewal and repair (R) | UNRESOLVED | heredity/REPORT.md; energy/REPORT.md | New active material after perturbation unmeasured |
| Functional inheritance and variation (H,V) | UNRESOLVED | heredity/REPORT.md | Founder-bound, serial function and variant selection missing |
| Sensing/state/adaptive action (S,M,A) | UNRESOLVED | adaptation/REPORT.md | No local causal target mechanism under unseen conditions |
| Integration and intelligent behavior (J,C) | UNRESOLVED | REPORT.md; PROTOCOL.md | No characterized system demonstrates all functions; no broad intelligence inference |
| Held-out target validation | NOT PERFORMED | WORKPLAN.md; REPORT.md | No target dataset; current tables are retrospective, not untouched tests |
| Full goal achieved | NO | All unresolved rows above | Goal remains ACTIVE; zero verified integrated complements |

Previous publication-verification turn: no substantive chemical-goal progress. Current turn: progress through new primary speciation evidence, corrected candidate decision, structural mismatch calculation and verified artifacts. A repeated three-turn impasse has not occurred; no blocked or complete status is justified.
