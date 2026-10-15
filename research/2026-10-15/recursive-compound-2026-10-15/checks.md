# Requirement-by-requirement checkpoint

All paths below are relative to this directory. Numerical PASS means only the stated check passed. No required target function is fulfilled by a source-table or software check.

| Requirement | Verdict | Evidence | Correction or remaining work |
|---|---|---|---|
| Larger JKFIT numerical qualification | PASS, fixed small-case screen only | rij-jkfit-qualification/REPORT.md; run-v1/result.json; INDEPENDENT_REVIEW.md | 101/101 checks, six new SCFs, four retrospective cases plus one new external geometry; no target or parent validation |
| Neutral source charge guard | PASS, preparation scope | rij-jkfit-qualification/SOURCE.md; test_rij.py; preparation.json | Pinned output confirms omitted neutral input charge; 14 tests including eight negative charge subcases; 30 pins unchanged |
| In-place factor memory mechanics | PASS, tiny tests only | cpcm-rij-memory/REPORT.md; test_memory.py; evidence/observations.json | Eight tests; factor alias/no global mutation/failure abort; oversized-chunk mutation rejected; Mo equivalence and SCF qualification outstanding |
| Memory qualification preparation | PREPARED, unrun | cpcm-rij-memory-qualification/REPORT.md; preparation.json | 57pins, seven gate tests; independent prelaunch review clear; no operator comparisons or SCF |
| W/V reference selection | ACQUIRED, untested | identity/next-step/wv-reference-selection/SOURCES.md | Six pinned source files; no W/V SCF or target incorporation evidence |
| Parent memory screen after specialization | UNRESOLVED for execution | cpcm-rij-memory/allocation.json | Arithmetic9.89326GiB leaves114.6MB with old allowances; actual peak/native transients unverified; no parent launch |
| Reconcile explicit H and heavy-contact topology | PASS, bounded source/geometry audit | proton-topology/REPORT.md; proton-topology/result.json; proton-topology/guibonds-result.json | 12 synthetic/parser tests; declared H topology agrees with distance assignment; physical framework and site map unresolved |
| Preserve RI-J software failure | PASS, failure retention | rij-qualification/run-v1/result.json; rij-qualification/REPORT.md | ECP bookkeeping initialization falsely triggered strict molecular fingerprint; all original pins retained |
| Qualify repaired RI-J accuracy | FAIL | rij-qualification-v2/run-v1/result.json; rij-qualification-v2/REPORT.md; rij-qualification-v2/INDEPENDENT_REVIEW.md | Neutral MoO3 and external Mo2O7 exceed direct-Fock residual screen; no parent admission despite five converged SCFs |
| Repair initialization without altering chemistry/limits | PASS, software scope | rij-qualification-v2/test_rij.py; PROTOCOL.md | 11 tests pass; same numerical screens, auxiliary basis and caps; post-fix continuation is not newly unseen validation |
| Recover complete parent heavy component | PASS, parent reference only | identity/parent_heavy.xyz; identity/site_mapping.json; identity/check.py | Hydrogen/protonation and target identity unresolved |
| Preserve incomplete extraction | PASS | identity/.omo/evidence/checks.json | 2.0 Å control remains Mo4O11 and rejected |
| Count full-model electrons/basis honestly | PASS, arithmetic/build only | identity/next-step/feasibility.json; parent-pilot-blocked/run-v1/preflight.json | Actual parent build confirmed196atoms/3068AOs/1568electrons; converged SCF/gradients/optimization unresolved |
| Small-reference direct SCF and continuum | PASS, runtime only | identity/next-step/method-qualification/result.json | Four hypothetical reference/control cases; no chemical accuracy or full-parent admission |
| Small-reference analytic nuclear derivative | Original FAIL preserved; corrected diagnostic PASS | identity/next-step/method-qualification/derivative-result.json; identity/next-step/method-qualification/grid-response-result.json | Same 1e-4 Eh/bohr limit and two finite differences; grid response required; no full Hessian or parent derivative |
| Hypothetical parent H inputs | PASS, computational input only | parent-inputs/metadata.json; parent-inputs/checks.json; parent-inputs/REPORT.md | Four inputs; ten malformed controls reject; no measured H or physical admission; short PT57 H-Mo contact retained |
| Original full-parent pilot | RESOURCE PREFLIGHT REJECTED | parent-pilot/run-v1/preflight.json; parent-pilot/run-v1/supervisor.json; parent-pilot/REPORT.md | 14.8437GiB estimate exceeds10GiB; no SCF launched |
| Blocked C-PCM reference equivalence | PASS, numerical implementation only | cpcm-blocked/result.json; cpcm-blocked/INDEPENDENT_REVIEW.md | Three SCFs/261 main checks; no physical admission |
| Blocked full-parent attempt | WALL LIMIT, no energy result | parent-pilot-blocked/run-v1/supervisor.json; parent-pilot-blocked/REPORT.md | Terminated900.208s before first reported cycle; sampled RSS6.6158GiB; matrix/factor built1.8494s; child absent/pins unchanged |
| Additional solution constraints | PASS, source interpretation only | solution-constraints/sources.json; solution-constraints/REPORT.md | Four primary studies; Nb comparator unverified; concentration discrepancy preserved |
| Nd-linked parent architecture | PASS, parent structural analogy only | boundary/nd-linker-proposition.md; solution-constraints/raw/izarova2005-si.pdf | Candidate19; target derivative, retention, transport and renewal unverified; no admission |
| External parent H-reference audit | PASS, computational reference only | published-parent/analysis.json; published-parent/comparison.md; published-parent/INDEPENDENT_REVIEW.md | Different4/24 versus16/0 O-H contact topology; SINGLE POINT provenance; final spectrum unresolved; not held out |
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
