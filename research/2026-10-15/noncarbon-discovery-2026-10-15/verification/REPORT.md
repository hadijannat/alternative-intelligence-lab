# Independent numerical and claims audit

Date: 2026-10-15. Ownership is restricted to this `verification/` directory; no database outputs, research reports or prior laboratories were changed.

**Numerical disposition: PASS, with a freeze-provenance limitation.** The independent `verify.py` imports no production screening code. All 22 checks passed, with zero source-value or classification mismatches. This verifies the descriptive inventory and bookkeeping; it does not validate a novel molecule, life, intelligence or a predictive biological model.

## Dataset and reproducibility

An independent HTTP fetch of the [official Figshare metadata](https://api.figshare.com/v2/articles/6815699) confirmed file 38521619, its 40,811,489-byte size and MD5 `fb3e1eb80339a70ff313af1c644c1777`. The downloaded archive matches all three. Its SHA256 is `d4c64660e9e1fa45c82bd8868a96ec10162195eed69636445972c05550d8d0d6`. The [NIST registry at the recorded commit](https://github.com/usnistgov/jarvis/blob/3b0c9d0f0c15759135de857dbc93e010db01eb29/jarvis/db/figshare.py) was fetched independently and is byte-identical to the retained registry. Dataset attribution and CC BY 4.0 license are supported. The archive is the explicitly chosen 2022-12-12 snapshot; version 11 metadata also lists a 2025 snapshot. The analysis must not describe the chosen archive as the latest release.

The audit decompressed the original archive and independently reconstructed composition-stratified selection from the salted JID hashes. It verified:

- 75,993 unique source IDs, 3,455 carbon-containing exclusions and 799 elemental exclusions; 71,739 eligible records.
- The exact 1,000 selected IDs, their order in the screened file, all six quotas and all selected original source rows.
- 923 distinct **reduced compositions**, allowing multiple structure records per composition. This should not be described as 1,000 chemically distinct novel compounds.
- Exact-token carbon exclusion, avoiding confusion with calcium, cobalt or chlorine.
- All 4,000 scalar cells against the original archive, including 751 unavailable MBJ bandgaps.
- 912 nonpositive and 88 positive formation energies; 680 hull distances at or below 0.1 eV/atom and 320 above. No unfavorable selected record was replaced.
- Redox-element and ion-element flags of 439 and 515 respectively. These are composition flags, with no measured redox kinetics, ion mobility or life score.
- Five life-related fields explicitly marked `UNMEASURED` in every row, and novelty marked `existing_database_structure`.

All six scientific files in `database/results-v1/` and the completed fresh-process `database/verification-v1/` replay are byte-identical. No fields or files were excluded from this comparison. The audit rechecked the existing replay rather than launching a redundant third complete screening pipeline; its separate archive-based reconstruction is recorded in `verification.json`.

The selection manifest verifies the protocol hash and selected-ID hash. The two-stage implementation prevents numerical properties from determining selection, and that property independence is directly reconstructible. However, the manifest has no pre-property code hash or independently timestamped immutable execution receipt. Thus the audit supports **property-blind deterministic selection**, while the stronger historical claim that the exact code was frozen before all property inspection is not independently established. Adding a hash now would not repair that historical limit. The reviewed current code hash is retained in `verification.json` for future reproduction.

## Proposed compound and primary evidence

The proposed `[Mo(VI)34 W(VI) V(V) O112(H2O)16]9−` passes formal charge arithmetic: `34×6 + 6 + 5 − 112×2 = −9`. A formal V(IV) counterpart gives −10; the parent all-Mo(VI) anion gives −8. Water is neutral in this accounting. These checks do not establish a substitution site, atomic geometry, protonation state, solution identity or the location of an added electron. A full carbon-free salt and operating system also require counterion, solvent, interface and reagent accounting.

The retained [Miras et al. primary paper](https://doi.org/10.1073/pnas.1921536117) supports seed-dependent parent Mo36 assembly under its acidic aqueous conditions, including removal of the kinetic lag with added parent cluster. Its Figure 1 identifies the parent formula. The proposed derivative cannot inherit that kinetic evidence by analogy. The reported strongly reducing regime is a decomposition warning; it does not establish that a single electron at V destroys the proposed derivative.

The retained [Sanchez Sanchez et al. primary manuscript and SI](https://pure.mpg.de/rest/items/item_1849723/component/file_1854326/content) reports Mo36−xNbx solution assignments and tentative V-substitution interpretation during mixed-oxide formation. This is relevant positive prior art against broad claims of first heterometal Mo36 chemistry. It is not a characterized Mo34WV molecule. The novelty report appropriately treats absent exact-formula search hits as a bounded search result, not global scientific novelty or patentability.

The primary-source dossiers also correctly separate physical conductance/retained material state, templated assembly and compartment growth from functional inheritance and autonomous cognition. Their operating media and auxiliary carbon dependencies matter. The known-compound Mo36/hydrated-WO3 coupling is an untested architecture; the proposed derivative is a hypothesis requiring identity and compatibility measurements. Neither is a demonstrated life compound.

## Evidence boundaries

Formation energy compares a calculated periodic solid with elemental references; hull distance concerns competing phases included in the database. Neither establishes aqueous stability, reaction rates, active catalyst retention, renewal or inheritance. The 0.1 eV/atom threshold is a declared descriptive heuristic. The screen is not held-out validation: no predictive model, relevant endpoint labels or new biological test data exist here.

The count of materials is not an agent count. The final live-inventory audit records **24 participating subagents: 15 direct specialists and nine children**, plus the root coordinator separately. The count includes the first restricted patent-check attempt, which performed arithmetic but could not browse. The requested 1,000-agent execution was not performed. A simultaneous concurrency limit does not establish that 1,000 sequential agents are impossible. `agents.json` retains every name, role and observed status; this auditor remains running at the final pre-response snapshot.

## Final integrated-claims review

**Disposition: APPROVE for bounded reporting; no blocking claim defect found.** The reviewed root `REPORT.md` SHA256 is `af39c60ff75edb4844eb41e69650de4b3454563939867ff44c4a840892e458f2`; the reviewed `candidate.json` SHA256 is `d4793fb6dd8c88a7d414817d8229134f0895c5929e710bb7c65595db3a4d21db`. `claims_review.json` records these hashes, participation and local-link checks, and the remaining provenance limitation. Subsequent edits require renewed review rather than inheriting this receipt silently.

The report preserves positive inorganic structural transmission and physical-learning evidence without requiring reproduction to acknowledge learning. It also preserves NaClO3 founder-fragment uncertainty and four source aggregate discrepancies; parent Mo36's all-seeded 480-row table and limited within-trace forecasts; adverse old B–N numerical results; and the parent sodium CIF anomaly. Parent coordinates are not represented as target coordinates. The common-medium audit retains both HER discharge and favorable morphology evidence, without inventing potential conversions or shared kinetic constants. None of these separate subsystem observations is promoted into an integrated living compound.

The proposed Mo34WV formula is consistently labeled an unverified composition hypothesis. Novelty, structure, aqueous identity, active retention, functional inheritance and intelligent behavior remain unestablished. The 1,000-record screen is explicitly descriptive, separate from that molecular target, and not a held-out biological validation. The reviewed report accurately retains the historical code-freeze provenance limit identified above.

Reproduce this independent audit with `python3 noncarbon-discovery-2026-10-15/verification/verify.py` from the workspace root. The locally retained independently fetched metadata and registry are required; `acquisition.json` records their URLs, hashes and HTTP results.

Skipped a third full pipeline, synthesis, new DFT and exhaustive patent/structure searching. Molecular existence, same-medium integration, functional inheritance and intelligence remain unverified.
