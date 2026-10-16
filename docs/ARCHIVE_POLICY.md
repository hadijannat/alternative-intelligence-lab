# Research archive policy

The exact `recursive-compound-2026-10-15/parent-blas-control-audit/sources` subtree contains acquired upstream OpenBLAS source snapshots, including its upstream README. It is excluded as third-party source material; authored report and verification receipts retain URLs and hashes.

One exact-path size exception excludes `recursive-compound-2026-10-15/parent-metric-solve-diagnostic-v2/run-v1/original_metric.npy` (3,077,044,480 bytes), which exceeds GitHub's 100 MiB file limit. The local original remains untouched. Its SHA256, dimensions, finite/symmetry inspection and failed-launch linkage remain in the published launch and postmortem receipts. This does not establish positive definiteness or a successful solve. The separate saved-metric replay completed later; its receipt binds 37 artifacts, with generic logs excluded and all other bindings checked against original source hashes. Its condition estimate is non-certified and its result does not admit physical validity or parent SCF readiness. The explicit-BLAS J follow-up remains prepared and unlaunched. Other binary arrays retain the existing policy.

Three mixed acquisition records also held authored scientific findings. Saved constants, source URLs, inspection extent and original/published hashes are preserved in [qualified-source-constants.json](../data/qualified-source-constants.json). Two negative admission reviews are preserved in [source-admission-findings.json](../data/source-admission-findings.json), including missing inputs and decisions. Raw provider responses are excluded. These projections perform no new scientific calculation; historical execution status is superseded by the current final report.

## Final publication curation

Run `tools/curate_archive.py --source ORIGINAL_RELEASE --output FRESH_FINAL_RELEASE` after the builder finishes. The original generated release remains immutable. This pass reads generated copies only, rejects `source-extract` trees and all TXT except explicitly named `requirements.txt`, `settings.txt`, and own reason notes, and structurally detects tool execution envelopes at any JSON nesting depth (including `native_result`, `actual_native`, and lifecycle wrappers). Scientific keys such as `native`, scalar numeric results and numeric arrays alone remain eligible.

The final curation also excludes every `.legacy-scipy` and `vendor` directory as bundled third-party dependencies, including `resources/vendor` and simulation vendor trees. Retrieve these dependencies from their original sources and follow their licenses. Sibling research sources and results remain eligible.

Provider capture JSON filenames (`provider-*-capture.json` and underscore variants) are excluded as tool acquisition receipts. Structural inspection also excludes an `args` object paired with an `actual` string containing a raw provider return, at any nesting depth and regardless of filename. Standalone scientific JSON with numeric, array or parsed-object `actual` values and `results` keys remains eligible.

Within `.omo/artifacts` and `.omo/evidence`, acquisition filenames containing capture, provider, primary, book, source-return or search-return are also excluded when they pair a request field (`args`, `arguments`, `registered_args`, `request`, `invocation`) with a response field (`actual`, `actual_return`, `provider_return`, `result`, `return`, `actual_visible_return`). Inspection recursively covers `requests`, `calls`, and `provider_operations` arrays. Paired string fields `initial_queries` and `actual_primary_navigation` in these acquisition contexts identify custom navigation captures. The contextual rule exempts protocol, selection, qualified-parameter, bookkeeping and analytical filenames. `web-return.json` in the artifact tree is explicitly excluded as a raw acquisition return. These contextual rules do not reject a scientific `result` field by itself. Standalone qualified constants remain eligible; useful constants embedded in excluded capture envelopes require a separate clean scientific export.

Curation verifies input shard/member/whole-file hashes, scans retained text and decompressed UTF-8 gzip traces for host paths and recognized credentials, and counts retained JSON numeric arrays without asserting scientific validity. It rewrites only affected shards, verifies every retained rewritten member, copies unaffected verified shards unchanged, and rebuilds the manifest, group totals and CSV index. Removed files retain original publication metadata under `prior_publication`; retained files keep their published bytes and hashes. The final manifest records curation evidence and its input-manifest hash. The earlier builder's broad TXT eligibility is superseded by this final curation policy.

The archive packages existing research artifacts. It never imports or executes research engines, historical checkers, or scientific producers. Inclusion and byte-integrity checks do not validate scientific claims. Historical reports retain their original claims and status; the repository README supplies the current interpretation.

## Scope and exclusions

Include own sources, protocols, configurations, reports, figures, numerical results and traces under `alternative-biochemistry-2026-10-06`, `cco`, `claude-run`, `discovery-loop`, `metal-oxide`, `noncarbon`, `simulation`, `virtual-lab`, and root `data`, `results`, `figures`, `src`, `tests`, `docs`, `references`. Root reports, dashboards, bibliography, README and dependency declarations are included. Scientific Markdown, Python, CSV, SQLite and standalone JSON from `.omo/evidence` are eligible. Functional-native Python engines are eligible; the word “native” alone is not an exclusion.

Exclude every symbolic link, multiply linked file, dependency/environment directory, cache, session/tooling directory, and the publication tree. Own scientific `.md`, `.py`, `.csv`, `.sqlite`, and `.json` artifacts under `.omo/artifacts` are eligible, including unique research outputs; duplicates are retained for provenance. Excluded directories have one subtree record; their contents are deliberately not enumerated. Credential filenames and `.env` files are excluded. Protected workbook names are checked before filesystem metadata or content reads. Copies in acquired spreadsheet formats are excluded; hard links and symlinks are excluded without reading targets. Renamed, unrelated-format copies cannot be identified without opening them and are outside what this policy can certify.

Acquired `supplementary` and `cache` directories and document/archive/sequence payload formats (including PDF, DOCX, XLSX, ZIP and FASTA) are excluded. In `sources` and `source`, authored Markdown and Python remain eligible, as do JSON/CSV explicitly named analysis, summary, metadata, provenance, license, audit, or result. This naming filter is a candidate-selection policy, not authorship proof; review that subset before release. Bibliographies and source metadata supply citations instead of redistributing primary datasets. Generic logs and raw web-response bodies are excluded. Scientific `.txt` is eligible only in own `models`, `experiments`, or `results` directories; `requirements.txt` is allowed. Unknown formats are excluded.

JSON/JSONL native tool receipts are excluded after structural inspection of typed tool-envelope fields; this version does not extract nested numerical outputs. A scientific field called `native` or a `content` array alone is permitted. Pure standalone numerical JSON remains eligible. Binary arrays, model checkpoints, databases, figures and UTF-8 gzip traces are eligible. Binary artifacts are preserved byte-for-byte and cannot be certified free of embedded private metadata; inspect the manifest and review such assets before public release.

## Transformations and integrity

UTF-8 text replaces the current project prefix with `PROJECT_ROOT`, user home paths with `/USER_HOME`, recognized credential strings and literal credential assignments with redaction markers. Every transformation is counted in the manifest. Gzip traces are decoded, sanitized and deterministically recompressed. Undecodable text/traces and invalid JSON are excluded with reasons. Text redaction is conservative and can affect example literals; original and published hashes expose every byte change.

The manifest records source and published SHA256, sizes, inclusion/exclusion reasons, transformations, group totals and archive member locations. Files split across shards have ordered offsets, chunk hashes and the whole published-file hash; concatenate their member contents in offset order to reconstruct them. Excluded unopened entries have no content hash. The CSV index lists included artifacts for path/group/format searching.

Archives use stable order, fixed timestamps, permissions and owner metadata. Gzip compression level 1 is recorded in the manifest and used for shards and transformed traces. Each tar member is recovered and hashed after writing; the manifest is written only after these checks and a final source-stat check. Any detected source mutation aborts publication. A fresh output directory is required and appears only after successful completion. Determinism applies to identical inputs and the same Python/compression runtime. SHA256 checks establish byte integrity, not scientific validity, provenance or license clearance.

## Invocation

To recover downloaded release files, place `manifest.json` and the selected group's referenced `research-*.tar.gz` assets in one directory. Run:

```sh
python3 tools/extract_research.py --archives /path/to/downloads --output /path/to/NEW/research
python3 tools/extract_research.py --archives /path/to/downloads --output /path/to/NEW/simulation --group simulation
```

Repeat `--group` to select several top-level groups; omit it for all included files. The helper checks every required archive SHA256, each selected member SHA256, contiguous chunk offsets, and each reconstructed whole-file SHA256. Split SQLite files and other large results are reassembled automatically. It rejects unsafe paths, links and existing output directories, and exposes the output only after all selected files pass verification. It does not execute scientific code.

```sh
python3 publication/alternative-intelligence-lab/tools/build_archive.py \
  --source . --output /path/to/fresh/release-assets --dry-run
python3 publication/alternative-intelligence-lab/tools/build_archive.py \
  --source . --output /path/to/fresh/release-assets --max-shard-mib 512
```

Dry run only inventories paths, sizes and policy decisions; it writes nothing and defers content inspection, transformations and hashes. Binary files are copied through temporary disk storage and read in bounded chunks. Gzip UTF-8 traces stream line by line, preserving original logical newline bytes; peak text memory scales with the largest line. Other text processing can require several times the size of the largest JSON. Tar shards are bounded by the requested compressed size; a file larger than the member budget is split, never silently omitted.
