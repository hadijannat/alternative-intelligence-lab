# Testing alternative RNA reaction mechanisms

This laboratory investigates why the previous RNA model fails against Salibi's measured S13 dose curves. It compares six fixed candidate conditions, holds out entire doses, nests model selection inside each outer holdout, and separately tests prediction beyond 30 minutes. All measurements were inspected in earlier work, so the validation is retrospective.

**Result:** separate active/reporter efficiencies plus F1 inactivation improve whole-dose RMSE from 10.631 to 3.145 pp. Nested selection gives 3.551 pp and later-time prediction 4.148 pp. Every candidate still fails the fixed accuracy screen; both historical transport closures also fail. The [completed report](REPORT.md), [comparison figure](comparison.png), [checks](checks.md) and [independent verification](independent-verification.json) preserve these outcomes.

The [protocol](PROTOCOL.md) fixes chemistry, optimization and decision rules before the official run. The [diagnosis](diagnosis/REPORT.md) reproduces the earlier failure and derives a dose–time restriction contradicted by the data. The [source review](research/REPORT.md) distinguishes literature support from proposed rate laws and records why other datasets cannot be pooled into this assay.

## Reproduce

From this directory, use Python 3.12.3 with [requirements.txt](requirements.txt). The existing offline environment is available through:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python -m unittest discover -p 'test*.py' -v
```

Use the same `uv run` prefix for these Python commands:

```sh
python diagnosis/diagnose.py
python research/verify.py
python run.py --output results-new
python run.py --replay results-new
python run.py --output verification-new
python verify_results.py --result results-new --replicate verification-new
```

The run refuses an existing output directory. Four independent worker processes execute the dose-subset fits; each fit retains all six starts and the same evaluation budget. Full source/code snapshots, raw predictions, parameter profiles, model state inventories, numerical checks and figures are retained. Failed starts and unresolved folds remain visible. No network access or external service is required for reproduction from the retained inputs.

The saved official and full-repeat directories are `results-v1` and `verification-v1`. Each complete campaign took about 18 minutes on this host. All 30 tests pass, and 262 scientific files match across the complete refits. The separate `render_report.py` reuses the frozen plotting code with smaller titles to produce the report's `comparison.png`; it leaves the official figure and manifest unchanged.

## Scope

F1-mediated reporter ligation, active-RNA production, precursor-assisted reactions, loss of catalytic competence, and nonproductive substrate complexes have separate state and observation definitions. The PAGE reporter is inactive product. A better fit to its yield does not establish active catalyst abundance, functional retention, inheritance, or creation of life. No physical experiment is performed here.

Synthetic runtime checks are in `development-v1` and `development-v2`. The interrupted first check exposed a missing start-table entry; it was corrected to the already specified protocol before any new measured-data fit. In v2, the trapping model recovered its own synthetic curves to 8.32e-10 pp RMSE. The revised comparator's `known_mechanism_curve_recovered` field is vacuously true in that historical timing record and is not a recovery claim; its synthetic RMSE was 2.040 pp.
