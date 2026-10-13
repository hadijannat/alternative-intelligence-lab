# Post-publication corrections — 13 October 2026

These corrections follow a review of commit `e098662` (tag `research-2026-10-13`) that AI language-model agents carried out at the request of the maintainer. It is not an independent peer review. The corrections change wording, add omitted context, add two literature sources that were not read in full, and correct one value in the exported evidence ledger (claim N01, 90 K to 94 K). They change no saved scientific result.

The tag `research-2026-10-13`, the release assets, `data/snapshot.json` and the archived originals are unchanged. No scientific model was rerun and no model was trained. The review recomputed the 480 Mo36 rows with its own code from the published formula and the inputs stored in `data/mo36-encounter-full.json`; that is an independent evaluation of the formula, not arithmetic on saved outputs, and it also produced the value 12.007 quoted in the README for a convention the archived model does not use. The review recounted the CCO percentages from the archived predictions, which is arithmetic on a saved output. Neither reran an archived script, and the review scripts are not part of this repository. The review read the maintainer's local originals, not the release copies; their hashes equal the published index except for the two path-sanitized files named in `docs/REPRODUCIBILITY.md`.

## Corrections

| File | Correction | Source of the corrected statement |
| --- | --- | --- |
| `README.md`, `docs/FINAL_RESULTS.md` | State the three Mo36 geometry conventions: centre at d = a + gap, gap measured from the diffuse-boundary plane to the nearest shell point, shell value as the sphere-surface average. Without them the formula does not reproduce the table. | Archived `encounter/protocol.md` and `encounter/model.py`, `research-0003.tar.gz` |
| `README.md`, `docs/FINAL_RESULTS.md` | Add two undisclosed model choices to the omission lists: the test-charge approximation and potentials held fixed across the salt grid. | Archived `encounter/protocol.md` |
| `README.md`, `docs/FINAL_RESULTS.md` | State that the sign of L equals the sign of the assigned potential difference in all 480 rows. Add literature charge-reversal points for silica and Fe oxides as context. | `data/mo36-encounter-full.json`; README sources 9 and 10, abstract-level reading only |
| `README.md`, `docs/FINAL_RESULTS.md` | Replace “near chance” for the GNN longer-path result with the one-sided counts: 576 of 576 negative and 16 of 576 positive predictions correct (192 queries of each label, pooled over three seeds). | Recount of `cco/artifacts/pilot/evaluation/predictions.jsonl`, `research-0002.tar.gz`, SHA-256 `aed7ab98ad29523be8afbe96807cab4cdb4ff097462318baa87dd2799244d150` |
| `README.md`, `docs/FINAL_RESULTS.md` | Add the CCO test-set sizes, label balance, training budget, descriptive and paired intervals, message-ablation results, and parameter and compute counts. | Archived `cco/REPORT.md`, `research-0002.tar.gz` |
| `docs/FINAL_RESULTS.md` | Replace “matched local storage sometimes achieved the same behavior at lower cost” with the wording of the source report, and name the two digital study folders. | Archived `simulation/acquired-memory-01/report.md` and `simulation/learning-chain-01/report.md`, `research-0004.tar.gz` |
| `docs/FINAL_RESULTS.md` | Explain that the 34 ledger records are 28 for groups C01–C10 and six tagged `CROSS`. | `data/initial-evidence-ledger.json` |
| `data/initial-evidence-ledger.json` | Claim N01: 90 K corrected to 94 K, with a `correction` field. The archived original ledger and `tools/export_snapshot.py` still produce 90 K; a re-export would revert this entry. At the tagged commit this export was byte-identical to the archived original (SHA-256 `37b7e6d40f944c8195b735e6adc9e0c0562d855d59f1bb2c724eef9d82189b16`, recorded in `data/snapshot.json` and in the release index); after this correction it no longer is. | Stevenson, Lunine & Clancy (2015), Methods, <https://doi.org/10.1126/sciadv.1400067> |
| `README.md` | Replace the quoted phrase “genetic effect” with “seed-dependent materials effect”; the quoted phrase does not occur in the cited SAPO-34 paper. | Full-text search of README source 6 |
| `README.md` | State that archive sizes are decimal gigabytes and that 3.04 GB covers the 14 archive parts only. | `data/archive-catalogue.json` |
| `docs/REPRODUCIBILITY.md` | Separate the PySCF runtime diagnostic from the 480-case model, which uses the standard library and NumPy only. | Archived `encounter/model.py` |
| `docs/REPRODUCIBILITY.md` | Name the inputs that the release does not contain: the Mo36 coordinate table read by `model.py` and four inputs of the two export tools. Name the two hashes that refer to unsanitized originals. Define `verified_member_count`. | `data/research-index.csv`, `data/snapshot.json`, `data/archive-catalogue.json`, `tools/export_snapshot.py`, `tools/export_mixed_records.py` |

The table omits the following smaller changes made in the same pass: cross-references to this file in `README.md` and `docs/FINAL_RESULTS.md`; the archived protocol's wording that the point/shell difference is representation sensitivity, not a confidence interval; the path distances of training and longer-path positives and the ID range of the seven non-GNN architectures, both from the archived `cco/REPORT.md`; and the figure alt text in `README.md`, which now says that the GNN failed on longer-path queries. Some added sentences are inferences of the review rather than statements of the sources named above: the reading of the CCO-minus-GNN interval, the reading of the message ablations, and the comparison of the literature values with the assigned potentials, including the 72-row subset.

## Not changed

- The figures and `data/cco-summary.csv`. The figure text already says that the GNN failed on longer paths.
- `docs/RELEASE_NOTES.md` and `CITATION.cff`, which describe the tagged release.
- `docs/publication-review.md`. It is a self-review of an interim state, as its own scope lines say, and it was not repeated on the final tree. No independent external review of this archive exists.

## Open items

- Ledger claim N10 records “seed-dependent lag removal” for Mo36. The main text of the source predicts that preformed Mo36 removes the lag and reports the Mo36 seeding data in its supplement, which the review did not read.
- README source 4 is a secondary source for the Mo36 coordinates: its peer-reviewed version takes the geometry from a 1991 crystal structure. The review did not open the supplement that holds the coordinate tables.
- The size of the test-charge error in L is unknown. No two-body Poisson–Boltzmann solution for the interface and the cluster was computed.
