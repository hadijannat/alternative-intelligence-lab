# F1 retention and inheritance experiment laboratory

This laboratory designs and simulates experiments for new active-F1 attribution, catalyst retention and functional inheritance through tracked compartment generations.

- [Experiment specification](EXPERIMENTS.md)
- [Integrated report](REPORT.md)
- [Earlier RNA failure analysis, revised chemistry and acquired datasets](../rna-mechanism-2026-10-15/REPORT.md)
- [Completion requirements](WORKPLAN.md)
- [Assay identities, source evidence and qualification gates](research/assays/REPORT.md)
- [Physical lineage design and sources](research/lineage/REPORT.md)
- [Assay simulation protocol](assay/PROTOCOL.md)
- [Assay and retention results](assay/REPORT.md)
- [Lineage simulation protocol](lineage/PROTOCOL.md)
- [Lineage results](lineage/REPORT.md)
- [Completion audit](checks.md)
- [Independent full replay receipt](verification-v1/verification.json)
- [Progress](progress.md)

The simulations evaluate prospective measurements under explicit planning assumptions. They do not use the preceding failed kinetic fit as calibrated chemistry, and no physical assay or division system has been qualified here.

Run the complete offline verification and independent numerical replay from the workspace root, choosing a new output directory:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-inheritance-design-2026-10-15/run_suite.py --output rna-inheritance-design-2026-10-15/NEW_VERIFICATION
```

The suite checks current scientific files against their frozen hashes, tests both laboratories in separate processes, verifies source identities and exact counterexamples, then reruns both complete campaigns. Assay replay extracts the official source snapshot so later report files do not alter source discovery. Lineage replay compares scientific JSON and the numerical contents of compressed arrays. ZIP timestamps and execution times are excluded; scientific values are exact comparisons. Existing output directories are refused.
