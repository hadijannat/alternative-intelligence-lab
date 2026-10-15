# Measured droplet coupling laboratory

The two matched Cys/PSS assays constrain bulk C3 production and a separate OD
window. The model tests how far those measurements constrain joint regeneration,
retention and transmitted catalytic function. The answer is limited by missing
active C3 transport and lineage measurements; conditional simulations are not
measured inheritance.

Run offline, from the repository root, with installed matching packages:

```sh
python measured-coupling-2026-10-15/droplet_model/run.py --output /tmp/droplet-replay-new
python -m unittest discover -s measured-coupling-2026-10-15/droplet_model -p 'test_*.py' -v
```

Verified package versions: Python 3.12.3, numpy 2.4.1, scipy 1.16.1,
matplotlib 3.10.8. The scoped runtime command used here was:

```sh
uv run --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with scipy==1.16.1 --with numpy==2.4.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python measured-coupling-2026-10-15/droplet_model/run.py --output /tmp/droplet-replay-new
```

After the packages are cached, add `--offline` to uv. The simulation itself uses
no network. Output paths must not exist. An accepted evidence directory includes
a self-contained `frozen/` snapshot: its `run.py` can also replay using its frozen
observations.csv and conditions.json. Compare results.json and the four CSVs;
manifest paths differ for frozen versus source replay. No timestamp or path is
included in scientific results.

Read PROTOCOL.md before interpreting results. Version 1 evidence is preserved;
the final evidence directory is linked in EVIDENCE.md. A post-fit reporting fix
restricts the observation-equivalent compartment witnesses to 0–2 minutes, before
observed dissolution; it changes no fitted parameters or holdout predictions.

The fitted timecourse starts with zero C3 and spans roughly 0–0.84 mM total C3.
Supplied-seed serial cycles, changed active fractions, and accumulated product
(especially complete retention q=1) extrapolate beyond this measured training
chemistry. Their effective rates and retained-function scores have no direct
experimental validation. The sweep establishes conditional behavior and missing
constraints; it does not establish physical feasibility across its parameter grid.
