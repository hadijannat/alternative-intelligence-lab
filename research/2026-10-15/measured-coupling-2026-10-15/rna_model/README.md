# Measured R3C/POPC coupling laboratory

Read `REPORT.md` for the result and `PROTOCOL.md` for the frozen analysis design. Source observations and conditions are in `../rna_sources/`; all original source files are retained there. `results-v1/` is the first numerical run, not a successful physical demonstration. The coupled model fails its prediction criterion and functional compartment inheritance is unidentifiable.

Run from this directory. uv isolates dependencies from the broken pre-existing global SciPy installation:

```sh
uv run --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with openpyxl==3.1.3 --with matplotlib==3.10.8 python -m unittest -v test_model.py
uv run --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with openpyxl==3.1.3 --with matplotlib==3.10.8 python run.py --output results-reproduction
uv run --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with openpyxl==3.1.3 --with matplotlib==3.10.8 python run.py --replay results-v1
```

`--output` refuses an existing directory. It freezes source hashes before fitting, refits only calibration observations, executes all predictions/controls/sensitivity/profile cases, and writes explicit chemical inventories. `--replay` verifies frozen-source and output hashes and regenerates108 predictions at saved parameters; it does not refit parameters.

Deterministic numerical artifacts are `predictions.csv`, `trajectories.csv`, `controls.json`, `sensitivity.json`, `profile.json`, `passive_carryover.csv`, and `inheritance_witness.json`. `summary.json` is deterministic except `elapsed_seconds`. `freeze.json` includes a run timestamp; the manifest hashes this timestamp and all outputs, so manifests differ across full re-runs. `prediction.png` is the standalone figure. The source files and model are not modified by runs.

The solver preserves three RNA moieties and distinguishes inactive reporter from active catalyst. Reactions are coarse effective laws fitted to a matched buffer, with membrane effects and transport identities unmeasured. No author rate from the unrelated Azoarcus coacervate study is imported.
