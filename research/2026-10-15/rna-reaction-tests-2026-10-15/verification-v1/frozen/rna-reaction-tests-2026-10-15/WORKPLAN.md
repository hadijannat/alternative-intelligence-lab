# Revised RNA failure and alternative reaction mechanisms

Objective: investigate why the revised RNA model still fails and test alternative reaction mechanisms against measured data, using held-out validation and preserving negative results.

Scope: this new directory and an independent review record in the workspace `.omo/evidence/`. All previous laboratories, data and failed fits remain unchanged. No wet experiments, external messages, publication, paid computation or changes to shared Python installations are needed. The existing pinned numerical environment is used. The long-task harness and frozen-experiment workflow apply; runtime reasoning settings are not inspectable and no change to them is claimed.

## Completion requirements

| Requirement | Evidence required |
|---|---|
| Diagnose remaining failure | Exact source-cell checks, independently replayed residuals, analytical structural restriction and measured counterexample, optimization and parameter-bound assessment |
| Chemistry-grounded alternatives | Primary-source mechanism ledger; explicit equations, units, state/observer definitions, moiety balance, initial-preparation assumptions and cross-condition exclusions |
| Fair frozen comparison | Candidate list, start/bound/evaluation budgets, split definitions and scoring rules frozen before official fits; failures retained rather than selectively retried |
| Held-out evaluation | Every fixed family's whole-dose predictions; nested grouped evaluation of model selection; independent late-time challenge with no late-time fitting; disjoint fit/selection/evaluation records |
| Interpretation of remaining transfer failure | Chemistry frozen before transport calibration; both existing transport closures; same historical benchmark and no tuning to benchmark outcomes |
| Identifiability and numerical checks | Convergence and multistart agreement, boundaries/Jacobian diagnostics, fixed-grid profiles of selected new parameters, moiety/nonnegativity/observer/split tests and tolerance refinement |
| Negative results and reproducibility | All candidate scores, failed starts/folds, unsupported and unresolved results; raw predictions, immutable source/config snapshots, saved-parameter replay and independent full-refit comparison |
| Delivery and review | Final report, runnable commands, figures, source ledgers, checks.md, progress.md and independent code/science review |

Completion is a verified investigation, not a required positive result or identification of a unique physical mechanism. Reporter predictions alone cannot establish active F1 abundance or inheritance.

## Evidence boundary

All existing S13 and transfer values have already been inspected in earlier work. Holding them out of each numerical fit provides retrospective predictive validation. It does not erase prior design knowledge or create prospective unseen experiments. No compatible new numerical validation dataset has been acquired. Condition differences in other papers and supplementary assays are retained explicitly.

## Ownership

Diagnosis worker owns `diagnosis/`; research worker owns `research/`; chemistry worker owns `model.py` and `test_model.py`; numerical comparison worker owns `run.py`, `test_validation.py` and `plot.py`. Root owns protocol, integration, verification and final reporting. Review is independent and read-only except its review record. Workers share the workspace and preserve others' changes.
