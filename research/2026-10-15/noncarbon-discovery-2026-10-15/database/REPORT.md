# A frozen screen of 1000 carbon-free crystal structures

**Result: 1000 existing database structures screened; no novel compound or non-carbon living system discovered.** All life-related properties remain unmeasured. This screen provides an auditable materials inventory for follow-up hypotheses.

The official NIST JARVIS registry supplied a 2022-12-12 snapshot containing 75,993 structures. We excluded 3,455 carbon-containing structures and 799 elemental structures. The executed workflow selected 1000 structures from 71,739 eligible structure records using composition strata and salted JID hashes before its separate property-screening step. The retained code permits independent verification that selection uses only composition and identity, and replay reproduces the selected IDs. The 71,739 eligible records are structures, not 71,739 distinct compounds. The sample contains **923 distinct reduced compositions**, because polymorphs remain distinct structure candidates. It is not a random sample representative of all inorganic chemistry; the strata deliberately emphasize oxygen, sulfur, nitrogen and phosphorus compositions.

The current Figshare article also offers a 2025 snapshot. We retained the official registry's explicitly pinned 2022 snapshot and do not call it the latest data. Source license is CC BY 4.0; [SOURCES.md](SOURCES.md) contains attribution, exact URLs and hashes.

| Composition stratum | Selected | Formation <= 0 eV/atom | Hull <= 0.1 eV/atom | Hull > 0.1 eV/atom |
|---|---:|---:|---:|---:|
| Phosphorus and oxygen | 150 | 149 | 129 | 21 |
| Silicon and oxygen, after prior stratum | 150 | 147 | 101 | 49 |
| Sulfur without oxygen | 200 | 183 | 130 | 70 |
| Nitrogen without oxygen or sulfur | 100 | 65 | 48 | 52 |
| Other oxygen-containing | 300 | 292 | 206 | 94 |
| Other carbon-free compounds | 100 | 76 | 66 | 34 |
| **Total** | **1000** | **912** | **680** | **320** |

All selected records have formation energy, hull distance and OptB88vdW bandgap; only 249 have MBJ bandgap. The 88 positive formation-energy cases, all 320 above-threshold hull cases and all 751 missing MBJ values remain in the output. The categories overlap and must not be added as independent exclusions.

Negative formation energy indicates favorability relative to the dataset's elemental references. Hull distance considers competing phases in the reference set. The 0.1 eV/atom cutoff is an explicitly chosen broad screen, not a universal stability criterion and not a necessary or sufficient condition for life. Neither calculation describes solution stability, reaction barriers, chemical maintenance, catalyst retention or functional inheritance under a particular environment.

439 structures contain at least one listed redox-relevant element; 515 contain at least one listed candidate ion species. These are **element-presence flags**, not measurements of reversible redox, catalytic activity, ionic mobility or memory. No oxidation-state assignment, material ranking or combined life score was made. Electronic bandgaps do not establish cognition. Carbon-free formulae also do not establish carbon-free synthesis or operation.

Every row explicitly labels autonomous maintenance, replication, functional inheritance, learning and intelligence **UNMEASURED**, and novelty **existing_database_structure**. Database membership does not prove experimental synthesis. A novel compound would need a separate novelty search and structural/chemical validation; a living system would need reaction-network and inheritance measurements beyond static crystal data.

## Reproducibility

Historical-freeze limitation: the selection manifest hashes the protocol and selected IDs, but it does not contain a pre-property `screen.py` hash or independent timestamp. The later artifact manifest hashes the retained code and is not evidence of an earlier code freeze. Independent audit verifies the inspectable composition/ID-only selection and deterministic replay; it does not independently verify the exact historical code freeze.

- [PROTOCOL.md](PROTOCOL.md): recorded selection and screening rules; its hash matches the selection manifest.
- [results-v1/selected_1000.csv](results-v1/selected_1000.csv): frozen structure IDs and composition-only selection.
- [results-v1/screened_1000.csv](results-v1/screened_1000.csv): every selected result, including unfavorable and missing values.
- [results-v1/eligible_inventory.csv](results-v1/eligible_inventory.csv): all 71,739 eligible structure records.
- [results-v1/selected_source_records.json](results-v1/selected_source_records.json): unchanged source rows for the 1000 candidates, including structures.
- [checks.md](checks.md): tests, integrity and fresh-process replay evidence.

Run from the repository root with Python 3, no extra packages:

```sh
python3 -m unittest discover -s noncarbon-discovery-2026-10-15/database -p 'test_screen.py'
python3 noncarbon-discovery-2026-10-15/database/screen.py select --out /tmp/noncarbon-replay
python3 noncarbon-discovery-2026-10-15/database/screen.py screen --out /tmp/noncarbon-replay
python3 noncarbon-discovery-2026-10-15/database/screen.py verify --out /tmp/noncarbon-replay --reference noncarbon-discovery-2026-10-15/database/results-v1
```

The output directory must not already exist for `select`; completed screens cannot be overwritten. The archive must already be available at the pinned local path.

No new DFT, ML training, synthesis or wet experiments were performed. This deterministic data screen is not held-out biological validation, and no life claim is supported by it.
