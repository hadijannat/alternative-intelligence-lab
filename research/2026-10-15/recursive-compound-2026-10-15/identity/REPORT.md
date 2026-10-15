# Parent heavy-atom identity admission

A complete connected potassium-salt parent component was extracted from unchanged COD 2107026: **36 Mo + 128 O = 164 heavy atoms**. Admission is limited to a crystallographic parent heavy-atom reference. The complete hydrated molecule, its solution identity, the Mo34WV derivative and noncarbon life/intelligence remain unverified. No substitution, coordinate repair, added hydrogen, energy or experimental result was generated.

Source: `noncarbon-discovery-2026-10-15/research/structure/raw/cod2107026.cif`, SHA256 `9a2275df1f08e8160b95d7139356e4b790d57ee97caafff321c0c4d7846be799`; deposited parent study DOI 10.1107/S0567740882007018. The existing parser's pure functions are reused via AST selection to avoid executing its writes. Its hash is in `.omo/evidence/extraction.json`. This retains its documented single-line-loop and monoclinic-cell scope; it is not a general CIF parser.

## Extraction and unresolved chemistry

The extractor expands all deposited Mo/O sites through four symmetry operations, constructs periodic Mo–O adjacency at 2.6 Å, selects the component containing Mo1 under the identity operation and unwraps it by graph traversal. Every cycle must give the same integer cell translation; a periodic network is rejected. No Cartesian coordinates are adjusted. `site_mapping.json` records source label, symmetry expression/index, wrapped fractional coordinate, integer translation, occupancy, Cartesian coordinate and neighboring Mo labels for every retained atom. Indices are zero-based for symmetry operations and one-based for XYZ atoms.

The component comprises two copies of Mo1–Mo18 and O1–O64. All occupancies are 1. Partially occupied oxygen and potassium source rows are recorded and excluded by component membership, without deleting them from the source. Mo coordination at the declared cutoff is 32 six-neighbor and four seven-neighbor sites. Minimum interatomic separation is 1.664453262 Å. This is a geometry audit, not bond-order assignment. The identical component and coordinates survive 2.5 and 2.7 Å cutoffs. A deliberately too-short 2.0 Å cutoff returns only Mo4O11 and is retained as a rejected extraction control.

O57–O64 and inversion-related copies provide sixteen long-contact oxygen sites, nearest Mo approximately 2.320–2.441 Å, consistent with the formula's sixteen coordinated waters. This is an **inferred site assignment**, not a resolved protonation measurement. O57 and O64 each contact two Mo at the cutoff, so “one Mo neighbor means water” would misassign them. All deposited oxygen type labels are O-2, including putative waters; these labels cannot resolve oxide/aqua chemistry. Hydrogen coordinates are absent. The formula supports nominal 112 oxide + sixteen neutral water accounting and parent charge −8, but individual proton positions, possible hydroxo alternatives and solution protonation remain unresolved. `identity_admission.json` therefore blocks admission of a full hydrated quantum input. `parent_heavy.xyz` is labeled accordingly and omits charge/multiplicity rather than inventing them.

The earlier sodium-parent 1.335 Å anomaly remains in the immutable prior dataset. No source was repaired or substituted to hide it. The new cutoff failure is preserved in `.omo/evidence/checks.json`.

## Runtime and smallest next atomistic step

The prior `discovery-loop/experiments/mo36-interface-resume-2026-10-13/runtime/REPORT.md` and diagnostic source were inspected as historical claims; its old SCF results are not counted as fresh validation here. A fresh import/build-only check in the existing borazine-water venv observes PySCF 2.14.0 and successful def2-SVP atomic basis/ECP construction: Mo 31 AOs/14 explicit electrons/28 core electrons; W 32/14/60; V 31/23/0. No SCF was executed, no electronic energy was evaluated and no optimizer was launched. These are availability checks; they do not qualify a Hamiltonian for the cluster.

The smallest defensible next step is to recover the primary atom/water assignment, then define explicit parent-only hydrogen/protonation hypotheses with provenance, inspect clashes and water geometry, and build the resulting documented input to count electrons and basis size before budgeting a bounded parent calculation. Multiple plausible H configurations must remain alternatives. Only after a parent method check should single substitutions and defined double-substitution isomers be compared using balanced reactions and the same environment. A stable geometry, if later found, would still not verify assembly, aqueous lifetime, functional heredity, adaptive behavior or intelligence.

## Reproduction and evidence

Run from the workspace root:

```sh
python3 recursive-compound-2026-10-15/identity/extract.py
python3 recursive-compound-2026-10-15/identity/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/identity/runtime_check.py
```

| Scenario | Binary observable | Captured artifact |
|---|---|---|
| Parent extraction and periodic unwrapping, first invocation | exit 0; 36 Mo/128 O, occupancy 1, no cycle conflict | `.omo/evidence/extraction.json`, `run.log`, `site_mapping.json`, `identity_admission.json` |
| Independent Cartesian connectivity, site counts/uniqueness, XYZ serialization, 2.5–2.7 Å sensitivity, second invocation | exit 0; `checks_pass=true` | `.omo/evidence/checks.json`, `check.log` |
| Deliberate 2.0 Å incomplete-component control, second invocation | `full_parent_rejected=true`; only Mo4O11 | `.omo/evidence/checks.json` |
| Fresh Mo/W/V build-only availability, third invocation | exit 0; expected core counts; `scf_run=false` | `.omo/evidence/runtime.json`, `receipts.json` |

`receipts.json` records exact invocations, return codes and raw outputs of the final full run. No active ulw-loop attempt exists; evidence is under this owned folder's `.omo/evidence/`.

Skipped hydrogen construction, large DFT, substitution screening and physical validation. Main risk: the parent heavy-atom XYZ is incomplete molecular input and must not be treated as a validated target or solution species.
