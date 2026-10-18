# Reproduction and verification

Environment actually used: Python 3.12.3, NumPy 2.4.1, Matplotlib 3.10.8. PyMuPDF version is retained in the extraction receipt. No dependency installation or system-library patch was performed.

From the workspace root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/extract_plots.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/model.py
```

Observed checks:

- Extraction passed source SHA256, 1038-vector inventory, tick orientation/linearity, marker color/shape/geometry and uniqueness checks; 29 points retained. Initial negative GC marker and separate time-coordinate offsets were preserved.
- Source hash: `cba5ee525fdfba67185b30180dae2b3ae201cb89e2bed40e66b42e831dd9d9a6`.
- SI hash: `55af718552d17d3c260d530d9b25d26a8019468ed345f5318d752649bb33e981`.
- Frozen protocol: `97d9721694d1af68a3d9218b5980c607f5e459293ab224a6252366ca2d18aa5c`.
- Plot table: `9cadaee99b5c763b455a11c1a5b89a633e36cfa9666f5a634902c863116df119`.
- Model run passed optimizer quadratic self-check, analytic detector step, zero-stock current, finite inventory, no-drive, no-buffer, explicit no-charge oxidized state, reduced-stock positive control and constant-current stock-excess assertions.
- The 3064-row trajectory closes mediator, hydrogen-equivalent and electron balances. Largest recorded charge residual is 5.684e-14 C. All JSON files parsed; negative-ledger numbers and result status agree.
- Re-extraction and model rerun after the control fix reproduced all held-out metrics. No split, equation or screening threshold changed after outcome inspection.
- Independent reviewer rendered and checked the primary vector plot, independently reproduced fitted parameters and held-out RMSE, tested the detector against an analytic ramp, and integrated discharge separately by one-second RK4. Final Red agreed with the implicit solution within 5.93e-21 mol.
- Independent control re-review resolved the duplicate-control coverage finding: oxidized/no-charge with discharge enabled gives zero mediator-supported H2, while initial Red with no charging gives 0.000497180230090813 mol H2 and no O2/charging input. Review status CLEAR / APPROVE, no blockers: `../.omo/evidence/documented-scaffold-code-review.md`.
- The four-panel generated result figure was inspected visually for axes, labels and failed-model visibility.
- Historical exact-target candidate ledger remains SHA256 `e4098ad3639df1c88a75aa5076c3f79d0ff22ac00df9c472aa534ab2304b0771`, unchanged from the prior branch.

Execution failures are retained in `negative_results.json`: the initial SciPy native PROPACK binary could not load, the existing cco virtual environment resolved to the same failed library, and Homebrew Python lacked SciPy. The working code instead uses deterministic NumPy grid refinement and an implicit analytic discharge solution. No failed import was represented as a chemical outcome.

No wet-lab experiment, independent new experimental dataset, uncertainty propagation from individual current replicates, native GC transfer-function measurement, immersed-mesh-area calibration, material-renewal measurement or functional-inheritance test was performed. The transport pass is a two-point retrospective voltage extrapolation screen; the geometry and detector tests fail. Conservation is a numerical property, not chemical validation.

Claude's completed consultation, selected Opus 5.5 Max model, transcript capture and the claim audit are recorded in `consultation/`. The primary-supported recommendation was retained, while unsupported numerical loss/speciation/proton constraints were rejected. No second prompt was submitted; the temporary unsent capture draft was cleared. Its output is AI advice and is not an independent experiment or a primary source.

The separate scientific narrative review corrected the balance units (mol versus C) and the mesh citation location (SI-6 pS11). These reporting corrections did not alter equations, thresholds or numerical outcomes. The model and extraction checks are complete; no broader project tests were needed for this isolated branch and README link.
