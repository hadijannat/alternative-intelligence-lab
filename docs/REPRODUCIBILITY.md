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

The catalogue records each asset SHA-256 and size. The full manifest records source and published hashes, transformations, excluded inputs and member locations. Verification must use the hash for the exact bytes being checked.

Historical relative links can point to an excluded acquisition payload or private native receipt. Consult the membership/exclusions manifest and source URL instead of treating such a path as a published file.

## Scientific reruns

Each study's archived protocol and environment record controls its rerun. Do not use one repository-wide dependency environment to imply that all studies share a validated runtime.

Examples of saved environments include Python 3.12.3; the Mo36 runtime used PySCF 2.14.0, while the CCO pilot used PyTorch 2.9.1. Original code, seeds, configurations and outputs are archived where eligible. The original source/geometry dependencies may require separately retrieving their authorized originals.

This snapshot makes no promise that a historical script can run unchanged on another host: private path sanitization, external source dependencies, absent native tools and old absolute paths are explicitly recorded. Original source hashes are useful for traceability; they are not the hashes of a sanitized copy.

## Rebuild publication figures

The chart inputs are rounded saved report summaries in `data/mo36-encounter-illustrative.csv` and `data/cco-summary.csv`. `tools/render_figures.py` redraws these figures; it does not recompute chemistry, train models or regenerate inference intervals. The displayed figures were produced with Python 3.12.3 and matplotlib 3.10.8. The plotting requirements are pinned in `requirements-figures.txt`.

```sh
python3 -m pip install -r requirements-figures.txt
python3 tools/render_figures.py
```

## Cite exactly the version used

Use the tagged snapshot, asset checksum and study version in a reproducibility record. `CITATION.cff` identifies the archive without fabricating a DOI. Citation of this archive does not replace citation of the primary papers for their experimental findings.
