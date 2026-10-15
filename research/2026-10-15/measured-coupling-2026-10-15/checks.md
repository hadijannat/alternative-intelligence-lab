# Verification and scientific acceptance

15 October 2026. Accepted computational verification: [verification-v2/verification.json](verification-v2/verification.json).

The research implementation is complete. Scientific support for an integrated living or intelligent entity is not established. Numerical correctness and repeatability do not change that distinction.

| Requirement | Verdict | Evidence and limits |
|---|---|---|
| Inspect primary numerical sources and conditions | Pass | 7,104 normalized droplet rows and 148 exact RNA workbook cells; source audits and condition ledgers. Counts describe extracted observations across assays, not independent experiments. |
| Use coherent chemical conditions | Pass for bounded analysis | Figure1 droplet assays share nominal formulation but are unpaired; RNA bulk buffer matches vesicle interior, with membrane extrapolation explicit. Incompatible source parameters excluded. |
| Separate observed, fitted and assumed processes | Pass | Frozen protocols; active transport, phase kinetics, retention estimate, reporter activity and lineage identity caveats retained. |
| Implement coupled chemistry and transfer accounts | Pass | Both models track resources and loss/transfer; droplet original/new chemical labels and RNA founder bound distinguish carryover. |
| Test held-out observations and simpler controls | Pass for execution | Droplet temporal fit passes declared engineering tolerance; RNA fails its frozen prediction screen and all nine sensitivity cases. No holdout rescue performed. |
| Test simultaneous retention and inherited function | Unresolved scientifically; constraint test completed | Droplet conditional retained-function envelope and observation-identical opposite-retention witnesses; RNA analytical lineage-observer invariance. Actual functional variants and parent/daughter assays absent. |
| Meaningful implementation tests | Pass | Eight droplet plus seven RNA tests, executed in separate fresh processes. See verification-v2/*-tests.log. |
| Chemical accounting | Pass within models | Droplet maximum residual 1.7053e-12 nmol; RNA maximum moiety residual 5.3934e-15 µM. Prescribed volume bookkeeping is not a physical phase-volume validation. |
| Numerical refinement | Pass within stated scenarios | Droplet representative endpoint difference 2.5662e-9 nmol plus nine transfer/control test combinations; RNA maximum reported-yield difference 1.7685e-7 percentage points. Not exhaustive convergence across all parameter combinations. |
| Source integrity | Pass | 88 retained-source hash comparisons plus two extraction row-count checks; same checks before and after replay. All 148 RNA workbook coordinates are also checked in tests. |
| Full offline refit/replay | Pass | 13 scientific output comparisons: five droplet and eight RNA CSV/JSON files. CSV byte equality; JSON equality excluding top-level elapsed_seconds only. Plots/timestamps/provenance are not numerical replay comparisons. |
| Stable inputs and retained snapshot | Pass | verification-v2 input SHA256 list and code-and-ledger-snapshot.zip. Droplet also retains a standalone frozen runnable snapshot. |
| Visual inspection | Pass | Both scientific figures opened and inspected. They distinguish fitted/held-out observations, reporter versus catalyst, and hypothetical transfers. |
| Independent scientific/code review | Recorded separately | See review.md and the linked independent reviewer artifact. |
| Physical replication, living entity or intelligence | Unresolved / not performed | No physical laboratory work, evolution or intelligence benchmark was executed in this continuation. |

## Corrections and preserved unsuccessful checks

- Review caught an RNA inhibition term that reset its treatment of active product at every incubation. It was removed before fitting; no held-out parameter tuning followed.
- Review caught a droplet disabled-control score using the full catalytic coefficient and an algebraic volume identity that could look like a measured conservation result. Both were corrected before the first fit.
- The first droplet candidate allowed compartment-retention witnesses beyond observed dissolution. A retained reporting/snapshot revision restricts them to 0–2 minutes and makes frozen replay standalone; fitted parameters, holdout split and transfer criterion are unchanged. See droplet_model/EVIDENCE.md and preserved .omo/evidence/run-v1.
- verification-v1 passed all 15 tests and 13 numerical comparisons but correctly failed its input-stability guard because droplet_model/README.md changed during verification. That failed receipt and snapshot are preserved. No numerical mismatch occurred. The runner was also extended to verify the droplet SI PDF hash stored separately in its manifest; verification-v2 passes with stable inputs and all 90 checks.
- The original SciPy binary failed to load its `_spropack` extension with a Mach-O section error. The runs use isolated SciPy 1.16.1 through uv; the global environment was not repaired or replaced. Temporary uv interpreter paths are not treated as durable reproduction commands.

## Tested runtime and command

Python 3.12.3; NumPy 2.4.1; SciPy 1.16.1; matplotlib 3.10.8; openpyxl 3.1.3. These versions are pinned in requirements.txt.

From this directory, choose an unused output path:

```sh
uv run --offline --no-project \
  --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 \
  --with numpy==2.4.1 --with scipy==1.16.1 \
  --with matplotlib==3.10.8 --with openpyxl==3.1.3 \
  python run_suite.py --output verification-new
```

The offline command uses already cached packages. On a new machine, provision those packages first or omit `--offline` for the initial environment setup, and select an available Python 3.12 interpreter. The analysis and replay make no network requests. Fresh computation demonstrates reproducibility, not independent physical replication.
