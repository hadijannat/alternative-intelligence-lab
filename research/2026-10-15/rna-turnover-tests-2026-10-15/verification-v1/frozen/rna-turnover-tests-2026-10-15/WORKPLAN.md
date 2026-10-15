# RNA turnover and transport investigation

Objective: investigate the remaining high-dose, late-time and transport failures; test a chemistry-grounded revision with held-out validation; preserve negative results.

Scope is this new directory and its independent review receipt. Earlier laboratories and results remain intact. Reuse the existing pinned numerical runtime and grouped-validation machinery. No publication, external messages, paid computation or physical experiments are part of this task. The long-task harness, Karpathy guidelines and frozen-experiment workflow apply. Runtime reasoning settings cannot be inspected; no change to them is claimed.

Completion means a reproducible investigation, not a required positive model result.

| Requirement | Required evidence |
|---|---|
| Diagnose three remaining failures | Replayed dose/time/transport residuals, source/observer checks, parameter drift and structural analysis |
| Ground a bounded revision in chemistry | Primary-source ledger; explicit occupied-catalyst states, stoichiometry, PAGE observer and preparation assumptions |
| Freeze before fitting | Small fixed candidate set, initial states, bounds, starts, budgets, splits, decision rules and source/code hashes |
| Test predictions honestly | Matched refitted prior-best comparator; whole-dose and nested selection validation; late-time and combined high-dose/late-time challenge; all failures retained |
| Investigate transport separately | Chemistry frozen before mixing calibration; historical benchmark untouched by fitting; physical assumptions and sensitivity cases reported separately |
| Check numerical and mechanistic limits | Conservation, nonnegativity, fast-release and zero-rebinding limits, observed-vs-available catalyst distinction, profiles and solver refinement |
| Verify reproduction | Raw records, incremental failures, source snapshots, saved-parameter replay and complete fresh-process refit comparison |
| Deliver reviewable result | Report, figure, commands, checks.md, progress.md and independent code/science review |

All existing measurements and earlier held-out errors have already been seen. This round is retrospective model development. Further cross-validation cannot create a new prospective dataset or establish functional inheritance.

Ownership: diagnosis worker owns diagnosis/; source worker owns research/; transport worker owns transport_diagnosis/. Root owns scope, protocol and integration. Further implementation assignments will use disjoint files. All workers share the workspace and preserve others' edits.
