# Checks and boundaries

2026-10-15, completed.

- PASS: official archive size 40,811,489 bytes and MD5 `fb3e1eb80339a70ff313af1c644c1777` match downloaded file. SHA256 `d4c64660e9e1fa45c82bd8868a96ec10162195eed69636445972c05550d8d0d6`.
- PASS: retained protocol SHA256 `0fabca6410b7e92d192a9239d1fda9316dbaad4b4d6b717281c3fbdb1e2a20cc` remains unchanged.
- PASS: eight standard-library unit tests covering exact carbon-token exclusion, missing/nonfinite/boolean numbers, stratum precedence, property-blind and order-independent selection, quota shortage and duplicate exclusion, classification thresholds, reduced compositions, malformed identities and elemental structures.
- PASS: 1000 unique carbon-free compound structure IDs, 923 distinct reduced compositions. All exact quotas filled; no fallback redistribution required.
- RECORDED EXECUTION ORDER: the separate `select` process wrote and hashed IDs before the `screen` process read numerical properties. Independent inspection verifies that selection uses composition and identity only. The selection manifest lacks a pre-property code hash and independent timestamp, so exact historical code freeze is not independently verified; the later artifact-manifest code hash does not establish earlier timing.
- PASS: full fresh-process selection and screening into `verification-v1` reproduced all six scientific output files byte-for-byte, including all 71,739 eligible structure inventory rows and all 1000 retained source records. Machine-readable evidence: `verification-v1/verification.json`.
- PASS: all five life-related columns are `UNMEASURED` for every row. All 88 positive formation-energy results, 320 above-threshold hull results and 751 missing MBJ bandgaps retained; no row replacement.
- PASS: independent read-only scalar/source verification, without importing `screen.py`: 1000 IDs/formulas/element sets and 4000 scalar cells match retained source records; nine independently recomputed counts/hash checks passed, zero mismatches.
- CLEAR: independent read-only specialist code/source audit found no concrete selection-leakage, parsing or evidence-claim blocker. It separately confirmed official version, download registry, property meanings and license.

Numerical-property screen results are descriptive. The fixed 0.1 eV/atom hull screen is a heuristic, and formation energy does not prove competing-phase stability. Composition flags do not prove activity or transport. Source data are computed bulk crystal properties from the explicitly selected 2022 snapshot, not solution kinetics, a synthesis record, or a model of life. Newer dataset versions were not compared.

No ML model, new DFT, held-out biological validation, synthesis or wet experiment was performed. No supported novel-compound or non-carbon life claim emerged.
