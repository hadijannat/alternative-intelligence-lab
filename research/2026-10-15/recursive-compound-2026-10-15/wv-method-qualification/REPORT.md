# W/V numerical comparison: bounded screen passes

The two previously selected WO4(2-) and VO4(3-) geometries pass all40fixed numerical checks after four converged SCFs. The launcher is terminal exit0, PASS_NUMERICAL_SCREEN_ONLY. Thirty preparation pins still match. The original preparation and unrun reports remain preserved, including [REPORT-before-first-run.md](REPORT-before-first-run.md). No threshold, implementation or source was changed after observing results.

Basis metadata: WO4 has88orbital functions,535auxiliary functions,48explicit electrons and60Wcore electrons removed by the ECP; VO4 has87orbital functions,572auxiliary functions and58explicit electrons with all-electronV. These counts are preparation evidence, not chemical predictions.

The frozen protocol's two sequential180second/2GiB children ran only after the parent pilot's terminal receipt and absent processes were verified. Each completed one direct and one MemoryRI SCF, from identical saved initial densities. Both child receipts are clean, with no resource termination or monitor error. The largest sampled RSS was514,736,128bytes; sampled RSS is not a certified peak.

| Numerical observable | WO4 | VO4 |
|---|---:|---:|
| Direct / RI SCF cycles | 15 / 15 | 17 / 16 |
| Total energy difference, Eh per metal | 4.853319285e-5 | 6.001044926e-5 |
| Largest absolute AO J difference over four densities, Eh | 5.944924980e-5 | 3.766002609e-5 |
| Largest Coulomb energy difference, Eh per metal | 1.374620297e-4 | 6.170984699e-5 |
| Direct full-Fock residual at RI orbitals | 7.845565631e-5 | 7.774269395e-5 |
| RI full-Fock gradient norm | 3.534453613e-7 | 5.893230551e-8 |
| Child wall time, seconds | 14.589 | 17.652 |

The [independent review](INDEPENDENT_REVIEW.md) recomputed all eight saved density/J comparisons, energy differences, solvent-aware orbital gradients, traces, orbital reconstruction/orthonormality, seeded perturbations and source pins. It checked the native energy logs and45metric-call receipts without launching new operators or SCFs. Saved arrays are numerical evidence only; no experimental source energies were compared across different methods.

These are external fixed-geometry numerical challenges for the W/V method gap, not experimental held-out validation or proof of incorporation into the target. Source method differences, target identity, basis/cavity sensitivity, reduced spin states and integration remain unresolved. All earlier RI and parent failures remain intact, including the MemoryRI parent's900second wall limit. No target complement or life function is admitted by this pass.
