# Water assignment and bounded quantum-input feasibility

The primary water-site assignment remains unavailable. No hydrogen coordinates or substituted molecule were generated. The concrete advance is an explicit parent proton-transfer comparison, formula-preserving alternatives, and measured atomic basis construction combined with exact count/storage arithmetic.

## Primary-source access and source limitations

The [IUCr June 1982 issue](https://journals.iucr.org/b/issues/1982/06/00/) identifies Krebs and Paulat-Böschen, pages 1710–1718, [DOI 10.1107/S0567740882007018](https://doi.org/10.1107/S0567740882007018), and links directly to [a21281.pdf](https://journals.iucr.org/b/issues/1982/06/00/a21281/a21281.pdf). The web reader returned HTTP 401 for that PDF and could not resolve the DOI. Direct requests returned HTTP 403 for DOI landing, PDF and issue page. All direct response bodies, hashes, URLs, timestamps and statuses are retained in `acquisition.json` and `raw/`; HTML denials are not paper text. No access restriction was bypassed. The issue-page title renders O12, while the deposited formula and extracted component support O112; the title rendering is not used for chemistry.

The deposited CIF contains no H rows, water-site annotations or bond table, and types every O as O-2. It names sixteen waters at the formula level. O57–O64 and inversion copies remain provisional aqua sites, inferred from sixteen long Mo–O contacts. This pass does not upgrade that inference to a recovered primary assignment. There is no new source-supported protonation or hydrogen-bond direction.

## Explicit hypotheses and discriminating comparison

`hypotheses.json` separates four parent compositions/assignments:

- P0: Mo36O112(H2O)16, H32, charge −8, provisionally water at O57–O64 and their inversion partners.
- PT57: Mo36O111(OH)2(H2O)15, H32, charge −8. Transfer one H from O57@0 to O4@0; keep all 164 heavy atoms. The measured coordinate separation is 2.575820286 Å, the shortest provisional water-to-framework O pair in the extracted component. This proximity selects a falsifiable local test; it does not establish an actual hydrogen bond or favorable transfer.
- PplusH: Mo36O111(OH)(H2O)16, H33, charge −7.
- PminusH: Mo36O112(OH)(H2O)15, H31, charge −9.

P0 and PT57 can be compared with identical nuclei/electron totals, avoiding an unspecified proton chemical potential. External proton addition/removal requires a defined reservoir and cannot be ranked from unmatched raw energies. In particular, target deprotonation H31/−10 is distinct from target one-electron reduction H32/−10.

The next chemically discriminating calculation is **parent-only P0 versus PT57**, using identical heavy atoms, charge −8, a provisional singlet electronic solution, matched PBE/def2-SVP/Mo-ECP and chosen water continuum (epsilon 78.4). Four future starts—two documented water-orientation configurations per arm—would allow H-only relaxation without imposing inversion symmetry. All H placements would be labeled model-built. Compare converged endpoint energies and whether the intended proton stays at its assigned site; retain transfers back, rearrangements, clashes and nonconvergence. A single donor-facing H orientation must not be mistaken for a measured hydrogen position. Def2-SVP is a pilot basis without a demonstrated diffuse-anion adequacy check; an energy ranking needs subsequent basis/environment sensitivity and orbital-stability checks. Frozen-heavy-atom electronic energies are neither free energies nor barriers, pKa values or aqueous populations.

This is a concrete registered future comparison, **not an executed quantum result**. Before full-parent work, qualify the chosen continuum/direct-SCF setup on a small reference. The first parent run should be only a capped performance/convergence pilot: 20 SCF cycles, 900 s wall limit, 8000 MB PySCF memory hint, one requested thread. The memory hint is not an enforced OS ceiling. If it fails to converge, preserve the failure and budget from measured throughput/memory; do not automatically launch four H relaxations or use unconverged energies. The four-start plan is conditional on the pilot and explicit input admission.

## Basis and resource arithmetic

`feasibility.py` uses actual single-atom PySCF 2.14.0 builds with spherical def2-SVP basis functions. Mo/W use def2 ECP; V/O/H are all-electron. Full-cluster AO totals are sums, independent of unknown H orientations. No dummy full-cluster coordinates are invented and no integrals or SCF are evaluated.

| Model | Atoms | All electrons | Removed ECP core | Explicit electrons | Spherical AOs |
|---|---:|---:|---:|---:|---:|
| Mo36O128H32, −8 | 196 | 2576 | 1008 | 1568 | 3068 |
| Mo34WVO128H32, −9 | 196 | 2590 | 1012 | 1578 | 3069 |
| Same target atoms, −10 | 196 | 2591 | 1012 | 1579 | 3069 |

Parity constrains allowed spin but does not identify the ground state or electron localization. Parent singlet and target nominal d0 singlet are hypotheses; the odd-electron reduced target needs an odd 2S, not a forced V-localized spin assignment. Proton addition/removal changes H count and charge together, leaving the explicit electron count unchanged; it changes basis size by five AOs per H with this basis.

For the parent, one dense double-precision AO matrix is 0.07013 GiB. Storing eightfold-packed four-center integrals would require **82,566.66 GiB**. A complete packed-pair × auxiliary tensor with the installed def2-universal-jkfit basis (19,612 auxiliary AOs) would require **687.91 GiB** before workspace. These are exact storage formulas, not allocated arrays or peak-memory observations. Direct integrals, blocked processing or different auxiliary choices avoid those full storage requirements, at a computational cost not measured here. The observed host has 36 GiB physical RAM and 14 logical CPUs; available RAM, reliable parallel speed and full-parent wall time were not measured. No full-array storage strategy above fits physical RAM. No “DFT-ready” admission follows from atomic basis availability.

## Validation and reproduction

Invocation from workspace root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/identity/next-step/feasibility.py
python3 recursive-compound-2026-10-15/identity/next-step/check.py
```

`feasibility.json` and `.omo/evidence/feasibility.log` capture atomic counts, model arithmetic, all sixteen nearest water/framework pairs and host-memory observation. `.omo/evidence/receipt.txt` captures both final invocations and return codes. `check.py` independently checks formulas/charge/electron conservation, integer storage arithmetic, source hashes, hypothesis boundaries and preserved old parent admission. Passing means arithmetic and artifact consistency only. The access failure remains a failed scientific prerequisite, not a passing paper acquisition.

Skipped hydrogen construction, full cluster integrals/SCF and optimization. Risk: all proton arrangements and the target remain hypotheses; the resource numbers do not establish scientific accuracy or feasible runtime.
