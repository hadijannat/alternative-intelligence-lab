# Verification checkpoint

Process checks below concern acquisition, audit and publication preparation. They do not close the scientific goal.

| Requirement | Verdict | Evidence | Correction or limit |
|---|---|---|---|
| Correct publication baseline | pass | Local HEAD and live remote main both `0685c45ad68429040d82cfa593a511d2c546ba74`; exact GitHub `verify` check completed successfully | No inference about a later commit |
| Preserve unrelated files | pass | Original untracked duplicates left untouched; `execution_failures.md` | Original checkout integrity check still fails on extras |
| Isolated committed snapshot | pass | Fresh remote clone: `PASS_OCTOBER18_PUBLICATION_ONLY`, 236 included files, 11,154,032 bytes | Integrity only; scientific reruns zero |
| Exporter baseline tests | pass | `python3 -m unittest discover -s tests -p test_export_october18.py`: 6 tests OK in clean clone | Original duplicate-contaminated checkout: 1/6 failed, preserved |
| Reuse Wei evidence and preserve access limit | pass | Existing SI independently rehashed; current published source audit; normal Chrome abstract-only access | Main body and label mapping unresolved |
| Distinct primary acquisition | pass | Ou main, SI, metadata and figure workbook HTTP200; SHA256/MD5/size in `sources/receipt.json` | DFT workbook not needed/downloaded |
| Source identity and inventory | pass | `python3 sources/verify_sources.py`: all 18 checks true; 12/35 PDF pages, 21 workbook sheets | Native payloads remain local, full text extracted |
| Eligibility before modeling | pass | `PROTOCOL.md`, SHA256 `45b71ca66ad444a71586a53bb6174fd51fc3c9d81eb56b58e72314ae904908b2`; source audit | No response points selected for new analysis; no rate fit/holdout |
| Acquisition failure preservation | pass | `python3 -B test_acquire.py`: 2 tests OK, including malformed JSON/wrong DOI and interrupted body | No live failure injection or new network rerun; use `-B` inside the frozen publication tree |
| Independent source/code review | pass | `.omo/evidence/origin-function-followup-code-review.md`: initial findings retained, corrections reviewed, APPROVE with no blockers | Formal lint/typecheck, live-network failure tests and Ag40 source verification outside review scope |
| Full objective and prior negatives retained | pass | `REPORT.md` all twelve rows unclosed; `negative_results.json`; parent continuation ledger | Zero integrated complements added |
| Origin-resolved active repair | unresolved | Same-film analytical linkage and S29 function recovery improve component evidence | Missing quantitative founder/new-material function bound and joint stock/function observations |
| Founder-bounded serial inheritance | unresolved | No qualifying recipient/variant/serial assay acquired | Ag40 architecture depends on structural organic ligands |
| Same-system integration and intelligence | unresolved | No maintained characterized integrated system | Physical verification unavailable through simulation/literature alone |
| New curated checkpoint | pass | Exporter verifier passes 251 included authored files, no missing reviews; hash comparison finds no deleted file or changed prior scientific result | Only new iteration/review, three continuation documents, manifest and review allowlist change |
| Publication of this checkpoint | unresolved | Local preparation only at this checkpoint | A local export/commit is not remote publication; verify exact remote SHA/checks if authorized and pushed |

Commands for this iteration run from `documented-scaffold-2026-10-18/origin-function-followup/` unless their paths explicitly name the publication repository. Use `python3 -B` for offline tests inside the curated snapshot so Python does not add a bytecache to its exact-file manifest. Do not rerun acquisition in place: the script refuses to overwrite the existing receipt and native files. Reacquisition requires a fresh directory so old successes and failures survive.
