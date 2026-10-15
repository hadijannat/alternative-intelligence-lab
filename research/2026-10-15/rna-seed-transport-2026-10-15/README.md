# Seed dependence and finite exterior transport

The laboratory separates membrane exchange, extracellular chemistry, serial sampling/feed and washed PAGE observation. It preserves the earlier failed sink model and evaluates two conservative transport closures with unchanged bulk chemistry. **All nine scenarios fail the held-out accuracy screen.** Read the [results report](REPORT.md), [frozen protocol](PROTOCOL.md), [diagnosis](diagnosis/REPORT.md), and [source review](research/REPORT.md).

Run from this repository's root. The pinned interpreter and packages were already available locally:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python -m unittest discover -s rna-seed-transport-2026-10-15 -p 'test_*.py' -v
```

Complete fresh-process calibration, profiles, held-out predictions, refinement and plots:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-seed-transport-2026-10-15/run.py --output rna-seed-transport-2026-10-15/NEW_OUTPUT_DIRECTORY
```

The runner refuses existing output directories. `--development` runs only synthetic recovery and timing, without measured calibration. Exact scientific outputs, failed starts, unresolved fits and threshold failures remain in each run. Frozen snapshots and SHA256 manifests support auditing; elapsed time and plot bytes are not scientific refit-equivalence criteria. The frozen runner also captures nested verification evidence, so archive file sets can grow as audit documents are added. The official main/refit scientific outputs match exactly; their documented five-file ancillary archive difference remains in the verification receipts.

No wet experiments, author correspondence or publication are performed. Reporter prediction does not identify active-catalyst retention or functional inheritance.
