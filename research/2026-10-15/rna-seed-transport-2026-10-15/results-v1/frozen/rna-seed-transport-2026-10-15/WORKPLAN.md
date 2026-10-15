# Seed dependence and extracellular transport

Task: investigate which assumptions erase seed dependence, implement a chemistry-grounded transport revision, and evaluate held-out predictions while preserving negative results.

Scope: this new laboratory and its independent review receipt. Earlier laboratories are immutable. Use the existing pinned Python numerical environment and source data. No publication, external messages, paid services or physical experiments. Runtime reasoning settings cannot be inspected; no change is claimed.

Completion means a verified computational investigation, not a required positive result.

| Requirement | Required evidence |
|---|---|
| Diagnose memory loss | Source schedule recheck, stagewise seed contrasts, bounded interventions, conservation and numerical replay |
| Model the transport boundary | Explicit intracellular/extracellular RNA, exchange and reuptake, serial sampling/feed, warm chemistry and washed PAGE observer |
| Ground assumptions | Primary-source ledger; distinguish measured procedures, approximations and unmeasured quantities |
| Freeze comparison | Equations, small fixed family set, parameters/bounds, fitting budget, calibration/test IDs and error criteria before fitting |
| Test held-out behavior | Original Figure 2 seed-0/1 calibration; held seed-2 and all positive serial-generation observations; no benchmark-selected winner |
| Preserve negatives | All fits, starts, residuals, sensitivity scenarios, profiles and scientific failure flags retained |
| Verify computation | Conservation/limits tests, synthetic recovery, tighter numerical check, saved-model replay, independent transport implementation and complete fresh-process refit |
| Deliver | Report, figures, reproduction commands, checks.md, progress.md and independent final review |

Current design decision: retain the earlier selected instantaneous chemistry unchanged. Compare the prior irreversible-loss/global-mixing model with an explicit common exterior bath and an effective finite exterior-patch exchange model. Use source-supported serial exterior carryover as the primary closure. Treat exterior chemistry and whole-culture exterior discard as fixed sensitivities, without new fit parameters. The final protocol will specify the mathematical closure after source and implementation checks; no measured fits are authorized before that freeze.

Ownership: diagnosis worker owns diagnosis/; source worker owns research/; model worker will own model.py and test_model.py; runner worker will own run.py, plot.py and test_validation.py after interface agreement; root owns protocol and integration. All workers share the workspace and preserve each other's work.
