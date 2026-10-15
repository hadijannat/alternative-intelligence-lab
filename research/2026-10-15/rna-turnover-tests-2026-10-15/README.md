# RNA turnover, high-dose prediction and transport

This laboratory investigates the remaining errors of the earlier independent-efficiency/inactivation model. It tests explicit catalyst–product complexes, finite release and reversible full-length binding. All earlier laboratories and negative results remain intact.

Both frozen campaigns are complete and independently verified. The [report](REPORT.md) preserves a negative result: finite release reduces held-dose RMSE from 3.145 to 3.012 percentage points, while all four candidates still fail dose, late-time and combined high-dose/late-time screens. All sixteen transport scenarios fail. The registered simplicity rule retains the earlier baseline, which remains inadequate. [Progress](progress.md) and [checks](checks.md) record completion and review.

The [protocol](PROTOCOL.md) fixes four chemistry candidates, six optimizer starts, whole-dose and nested validation, late-time prediction, a combined high-dose/late-time challenge, and all transport sensitivities before fitting. These are retrospective holdouts from previously inspected data. No fresh prospective validation dataset was acquired.

The [dose/time diagnosis](diagnosis/REPORT.md), [transport diagnosis](transport_diagnosis/REPORT.md) and [primary-source review](research/REPORT.md) explain the revision. Bound ligated reporter counts in the PAGE observer. Available catalyst, competent full-length RNA and chemically ligated material remain separate quantities. Related literature motivates the reaction topology; its rate constants are not imported as measurements under the Salibi assay conditions.

## Reproduce

From this directory, use Python 3.12.3 and the four packages in [requirements.txt](requirements.txt). The pinned offline environment on this host is:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python -m unittest discover -p 'test*.py' -v
```

Use the same `uv run` prefix for the following Python commands:

```sh
python run.py --output results-new
python run.py --replay results-new
python run.py --output verification-new
python verify_results.py --result results-new --replicate verification-new
```

Each run refuses an existing output directory and freezes source data, code, protocol and research ledgers. Four processes execute independent fits. Every fit retains six start records, including unsuccessful finite starts and capped budgets. Raw predictions, nested split identifiers, parameter profiles, state inventories, numerical checks, transport calibration receipts and figures are retained. The separately hashed verifier cannot affect the fits. Reproduction uses retained inputs without network access.

`results-v1/` is the official run and `verification-v1/` the complete fresh-process refit. `development-v1/` contains synthetic tests only: the reversible model recovers its generating curves to 6.15e-9 percentage-point RMSE, with six successful starts. This verifies implementation recovery, not the physical mechanism or unique parameter identification.

Each complete campaign contains 161 fits, 966 optimizer starts, 3,288 prediction rows and sixteen transport scenarios. One combined-challenge fit retains a start-agreement flag. The official run took about 93 minutes on this host. The [saved-parameter replay](saved-parameter-replay.json) passes. An independently written five-state DOP853 bulk solver agrees with the twelve-state LSODA implementation on 1,800 comparisons; `python reduction_check.py` replays that check against the retained `results-v1` full fits and writes [reduction-verification.json](reduction-verification.json). It does not independently implement transport.

The [independent verification receipt](independent-verification.json) confirms all scientific values and identities across 193 complete-refit files match exactly, excluding clocks and plot bytes. All 268 audited previous-laboratory hashes remain unchanged. The current 50-test suite also passes in independent review.

## Scope

No physical experiment, publication or external message is performed. Shared pair affinities, uniform competence loss, initially free/equilibrated seed, and transport content-loss/dissociation closures are explicit hypotheses. Aggregate RNA retention does not measure active-catalyst retention. These simulations do not demonstrate functional inheritance, life or intelligence.
