# Provenance and reproducibility

## Publication checks

Run `python3 tools/verify_publication.py` from the repository root. It verifies key saved data counts, relative links used by the publication, the final scientific status and archive catalogue structure. It neither imports nor executes the scientific producers.

The publication process packages existing results. Historical checks remain historical evidence; new packaging checks do not independently validate those experiments.

## Recover the bulk record

Download the assets from the `research-2026-10-13` release and the archive manifest. Each archive is an independent gzip-compressed tar file. Files larger than the shard budget are represented as ordered chunks; the manifest gives the original path and chunk order. Reassemble those chunks before using the file.

The included helper verifies the downloaded archives and reconstructs split files into a new directory:

```sh
python3 tools/extract_research.py --archives /path/to/downloads --output /path/to/new/research
```

Add `--group cco` or another top-level group to recover a subset. Download every archive referenced by that group's files in the manifest. See the [archive policy](ARCHIVE_POLICY.md) for validation and selection details.

The catalogue records each asset SHA-256 and size. Its `verified_member_count` counts tar members per archive, so a file split across archives is counted once per chunk; the member counts sum to 23,931 for 23,926 files because one database is split across six archives. The full manifest records source and published hashes, transformations, excluded inputs and member locations. Verification must use the hash for the exact bytes being checked.

Historical relative links can point to an excluded acquisition payload or private native receipt. Consult the membership/exclusions manifest and source URL instead of treating such a path as a published file.

## Scientific reruns

Each study's archived protocol and environment record controls its rerun. Do not use one repository-wide dependency environment to imply that all studies share a validated runtime.

Examples of saved environments include Python 3.12.3; the Mo36 quantum-runtime diagnostic (H2 and water only) used PySCF 2.14.0, the 480-case Mo36 encounter model uses only the Python standard library and NumPy, and the CCO pilot used PyTorch 2.9.1. Original code, seeds, configurations and outputs are archived where eligible. The original source/geometry dependencies may require separately retrieving their authorized originals.

This snapshot makes no promise that a historical script can run unchanged on another host: private path sanitization, external source dependencies, absent native tools and old absolute paths are explicitly recorded. Original source hashes are useful for traceability; they are not the hashes of a sanitized copy. Two recorded hashes are of this kind: `cco/REPORT.md` in `data/snapshot.json` and `protocol_sha256` in `data/mo36-encounter-full.json` refer to original bytes, and the published copies of those two files hash differently.

### Inputs that the public release does not contain

The 480-case Mo36 model (`discovery-loop/experiments/mo36-interface-resume-2026-10-13/encounter/model.py`, in `research-0003.tar.gz`) reads `discovery-loop/sources/e850-mo36-structure-browser-capture-v2/published-coordinate-tables.json` and checks its SHA-256, `9836944e329c98956b478b036fd2fbce5866ec6eca82b38a0fa390b0e4e5fb48`. That coordinate table is not in the release index, so the archived script cannot run as published. The saved rows can still be recomputed from the formula and conventions in the README together with the shell radius, the thermal voltage and the screening constant of each bath (`baths[].kappa_nm_inverse`) stored in `data/mo36-encounter-full.json`; the README does not define `kappa`.

`tools/export_snapshot.py` and `tools/export_mixed_records.py` are maintainer-side exporters. They read four inputs that `data/research-index.csv` does not list: `.omo/evidence/mo36-resume-encounter-native-2026-10-13.json` (SHA-256 `7a724f37cf50eb7dcab0a00d3b910dbc1ec432dbfa94cf3af2c66d4635652a67`, the source of `data/mo36-encounter-full.json`), `.omo/artifacts/Mg-charge-budget-next/constant-captures.json` (SHA-256 `118dac6e05148a006380a139701459c1e9eb77275d16f5394c048f48bcb57fe4`), `.omo/evidence/e878-primary-route-packet.json` (original SHA-256 `83160f02101c858b21ac9ced59c0876573a19e721d3bb1d2706a3169aca373ab`) and `.omo/evidence/e910-mo248-primary.json` (SHA-256 `33776c48835cbef4a9f795deb5156f924460ea386c9a13f344666c75386b90f0`); the last three hashes are recorded in `data/qualified-source-constants.json` and `data/source-admission-findings.json`. The two tools document how the `data/` projections were made; they cannot be rerun from the public release.

## Rebuild publication figures

The chart inputs are rounded saved report summaries in `data/mo36-encounter-illustrative.csv` and `data/cco-summary.csv`. `tools/render_figures.py` redraws these figures; it does not recompute chemistry, train models or regenerate inference intervals. The displayed figures were produced with Python 3.12.3 and matplotlib 3.10.8. The plotting requirements are pinned in `requirements-figures.txt`.

```sh
python3 -m pip install -r requirements-figures.txt
python3 tools/render_figures.py
```

## Cite exactly the version used

Use the tagged snapshot, asset checksum and study version in a reproducibility record. `CITATION.cff` identifies the archive without fabricating a DOI. Citation of this archive does not replace citation of the primary papers for their experimental findings.
