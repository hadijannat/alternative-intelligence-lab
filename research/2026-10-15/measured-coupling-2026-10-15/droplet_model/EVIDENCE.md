# Droplet model completion evidence

Canonical result: `results-v1/`, identical to `.omo/evidence/run-v1.1/` at acceptance.
The first candidate `.omo/evidence/run-v1/` is preserved. Version 1.1 restricted
retention witnesses to the first two minutes, before observed OD dissolution,
and enabled self-contained frozen replay; no fit data, parameter estimates,
holdout split or conditional transfer criterion changed. README adds the explicit
warning that seeded and accumulated-product transfer is an unvalidated extrapolation.

Runtime prefix used for all scientific invocations:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with scipy==1.16.1 --with numpy==2.4.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python
```

All paths below are relative to `measured-coupling-2026-10-15/droplet_model/`.

| Scenario | Invocation after runtime prefix | Binary observable | Captured artifact |
|---|---|---|---|
| Source provenance and fixed fit/holdout | `run.py --output .omo/evidence/run-v1.1` | 10 training and 6 holdout C3 observations; 126 separate OD observations; input/code SHA256 snapshots present | `results-v1/manifest.json`, `results-v1/frozen/`, `results-v1/fit_residuals.csv` |
| Early fit, fixed temporal extrapolation | same run | Product-dependent holdout RMSE 0.0473179209783 mM <= predeclared 0.084 mM; baseline 0.0956330279542 mM > tolerance | `results-v1/results.json`, `results-v1/fit_residuals.csv` |
| Rate and capacity sensitivity | same run | 101 kcat-profile rows and two fixed-capacity training-only refits; no confidence coverage claimed | `results-v1/rate_profile.csv`, `results-v1/results.json` |
| Joint observation constraint | same run | Inside/outside witnesses have zero bulk prediction difference and opposite retained amount during 0–2 min | `results-v1/observation_witnesses.csv` |
| Conditional passage challenge and controls | same run | 162 cases; 54 per control; 16 conditional regeneration passes and zero passes in each disabled-control arm; no measured-inheritance claim | `results-v1/conditional_transfer_sweep.csv`, `results-v1/results.json` |
| Resource and founder accounting | same run | Maximum numeric chemical balance error 1.7053e-12 nmol < 1e-6; no-regeneration forms zero new product; founder-free arm starts via baseline | `results-v1/results.json`, `.omo/evidence/tests-v1.log` |
| Equations, transfer, negative-input and refinement tests | `-m unittest discover -s measured-coupling-2026-10-15/droplet_model -p 'test_*.py' -v` from repository root | 8 tests pass; all three transfer modes × three controls checked for mass accounting and tighter-tolerance agreement | `.omo/evidence/tests-v1.log`, `test_model.py` |
| Standalone frozen offline replay | `results-v1/frozen/run.py --output .omo/evidence/frozen-replay-v1` | results.json plus all four CSVs byte-identical to canonical outputs | `.omo/evidence/frozen-replay-v1.log`, `.omo/evidence/frozen-replay-comparison.json` |
| Readable scientific figure | view `results-v1/coupling.png` | Four panels inspected: concentrations, OD, bounded witnesses, hypothetical passages; labels visibly readable | `results-v1/coupling.png` |

Refinement is representative plus the nine mode/control unit-test scenarios,
not a tolerance sweep of every fitted conditional parameter combination. Volume
is prescribed half-removal/refill bookkeeping, not inferred phase volume. No
wet-lab replication, active transport measurement or observed inheritance was
performed. The conditional active-fraction and phase-independent-rate closures
are the principal physical risks; no life or intelligence result is claimed.
