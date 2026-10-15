# Measured chemistry coupling laboratory

Question: can catalyst regeneration, compartment retention and functional inheritance operate together under one experimentally specified condition?

This continuation replaces selected generic rates with fits to primary chemical observations and tests the remaining transport/lineage assumptions explicitly. The earlier [computational suite](../alternative-entity-lab-2026-10-15/REPORT.md) remains a separate, conditional construction. Neither package establishes a living or intelligent physical entity.

Two independent chemistry branches are retained:

- `droplet_sources/`, `droplet_model/`: fuel-dependent autocatalyst/droplet experiments, numerical formation kinetics and turbidity. Source DOI [10.1016/j.chempr.2025.102816](https://doi.org/10.1016/j.chempr.2025.102816).
- `rna_sources/`, `rna_model/`: R3C ligase chemistry in externally temperature-cycled POPC vesicles, numerical kinetic/transfer observations and inactive reporter. Source DOI [10.1038/s41467-023-36940-z](https://doi.org/10.1038/s41467-023-36940-z). The separately reviewed coacervate study [10.1038/s42004-023-00887-5](https://doi.org/10.1038/s42004-023-00887-5) supplies context only; its incompatible chemistry is not imported.

Read the frozen model protocols and source condition ledgers before interpreting results. Source measurements, fitted effective parameters, approximate estimates and hypothetical transfer scenarios are different evidence classes. Unknown transport or lineage parameters are not filled with measurements from a different system.

The completion requirements are in [WORKPLAN.md](WORKPLAN.md). [NEXT_EXPERIMENT.md](NEXT_EXPERIMENT.md) specifies the missing joint measurement and matched controls. Current execution status is in [progress.md](progress.md).

Read [REPORT.md](REPORT.md) for results, [checks.md](checks.md) for verification and reproduction, and [review.md](review.md) for independent review. Accepted verification: 15 tests, 90 source/extraction checks, 13 numerical replay comparisons. The droplet bulk fit meets its engineering tolerance; the RNA model fails its held-out adequacy screen. Neither establishes functional offspring inheritance.

Run a new offline replay from this directory with the cached pinned environment:

```sh
uv run --offline --no-project \
  --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 \
  --with numpy==2.4.1 --with scipy==1.16.1 \
  --with matplotlib==3.10.8 --with openpyxl==3.1.3 \
  python run_suite.py --output verification-new
```

Use an unused output directory. Models and raw source data are preserved; numerical results are compared with results-v1 in each branch. The accepted top-level receipt is verification-v2/verification.json; verification-v1 is retained because a simultaneous README edit correctly failed its input-stability guard despite matching numerical outputs.
