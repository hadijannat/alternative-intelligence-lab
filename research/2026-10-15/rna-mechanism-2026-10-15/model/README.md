# RNA mechanism revision

`PROTOCOL.md` fixes the five chemistry candidates, whole-dose cross-validation, controls and transport comparisons before fitting. The previous experiment is preserved unchanged. All model comparisons are development evidence because the published data were already inspected.

Use the installed isolated runtime; global SciPy failed to import with a Mach-O PROPACK error. From this directory:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python -m unittest -v test_model.py
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python run.py --output results-reproduction
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python run.py --replay results-v2
```

The output directory must not exist. `results-v2` is the complete run; the first run is retained as a partial serialization-failure artifact explained in `RUN_REPAIR.md`. Every run freezes complete local code/data copies and hashes before fitting. `cross_validation.json` contains every candidate, fold and optimizer start, including failed starts and boundary hits. `full_fits.json` and `profiles.json` describe calibration and identifiability. `predictions.csv` contains both transport models' historical benchmarks; neither is selected on those outcomes. `trajectories.json`, `controls.json` and `sensitivity.json` preserve chemical inventories, inactive reporter reservoir, source/sink balances and active-catalyst retention alternatives. `refinement.json` checks integration accuracy; `new_assay_checks.json` records the same-condition negative control and the scope of incompatible-buffer assays. `comparison.png` is the standalone figure.

Scientific JSON/CSV outputs are deterministic. `summary.json` has one nondeterministic field, `elapsed_seconds`; `freeze.json` contains a timestamp and runtime versions. `manifest.json` hashes all output files and frozen copies, so its hash changes with timestamps. `--replay` verifies the manifest and all source hashes and regenerates 216 benchmark predictions at saved parameters; it does not repeat fitting. A full independent refit uses `--output` instead.

No active-catalyst retention measurement or parent-daughter lineage data are inferred from inactive fluorescent reporter yields. A better statistical fit cannot establish physical functional inheritance.
