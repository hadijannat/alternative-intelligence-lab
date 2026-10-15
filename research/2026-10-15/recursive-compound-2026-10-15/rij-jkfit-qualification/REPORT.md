# Larger-basis RI-J numerical qualification

**PASS_NUMERICAL_SCREEN_ONLY.** The fixed def2-universal-jkfit proposal passed all 101 checks across four retrospective cases and one newly selected external geometry. This advances the numerical prerequisite for a parent calculation. It adds no verified chemical complement and does not demonstrate target existence, stability, heredity or intelligence.

| Fixed case | Absolute energy error per Mo, Eh | Direct full-Fock residual at RI solution | RI cycles | Auxiliary functions |
|---|---:|---:|---:|---:|
| MoO4(2-), water dielectric | 0.000074199188 | 0.000111037607 | 16 | 563 |
| MoO3, water dielectric | 0.000063655337 | 0.000096235629 | 14 | 486 |
| MoO4(2-), epsilon1 | 0.000074059769 | 0.000110611067 | 17 | 563 |
| Previous external Mo2O7(2-) | 0.000067709913 | 0.000145781706 | 24 | 1049 |
| New external H2Mo2O7, neutral | 0.000075443496 | 0.000186795344 | 32 | 1085 |

The unchanged energy-error and direct-Fock residual screens are each0.001 in their declared units. Previous jfit residual failures were0.001151565935 for MoO3 and0.001096362264 for Mo2O7. Those failed campaigns and their pins remain intact. All five new RI SCFs converged. The four earlier direct energies/densities were reused exactly, without new direct SCFs. Only the new external case required a direct calculation:32cycles, energy−663.7139243400396Eh; its RI energy was−663.7140752270326Eh. Total new SCFs:6.

Worst discrepancies across the saved arrays were maximum J error0.000279110802Eh, absolute Coulomb energy error perMo0.000174251053Eh, total-energy error perMo0.000075443496Eh and direct-Fock residual0.000186795344. Maximum RI residual was2.65740e-7, trace error6.39488e-14 and additivity error1.65201e-12. Symmetry error and zero-density J were zero. All148 native metric receipts report Cholesky factors, finite J and absent three-index caches; no four-center ERI cache was retained. Independent recomputation of the arrays confirmed these results.

All five children returned0 with no termination reason or monitoring error. The slowest was the new external case at150.6173seconds, within180seconds. Maximum sampled RSS was624,345,088bytes, within2GiB; sampling does not certify the instantaneous peak. All30 frozen source/code pins still match. Session2782 is terminal, exit0. The old parent runs were not restarted.

## Source selection and validation scope

[SOURCE.md](SOURCE.md) records the new neutral H2Mo2O7 geometry, primary URLs, attribution, hashes and charge evidence. It was the first available case in the prescribed H2-before-H1 order, selected before its direct or RI calculation. The deposited input omits Charge while its output explicitly confirms zero charge and restricted spin; a prelaunch guard correction and eight negative subcases address this representation. Fourteen unit tests passed before the preparation freeze. This changes no scientific threshold or method.

The four earlier cases are retrospective. The neutral external case is a fresh fixed-geometry numerical challenge relative to the prior RI campaigns, not experimental validation or a target holdout. The source uses ADF PBE/TZP/ZORA/COSMO, while the new direct and RI comparisons both use the fixed PySCF PBE/def2-SVP/ECP/BlockedPCM method. The original ADF energy is not a comparison target. One geometry cannot establish chemical accuracy, transferability to Mo36 or substituted W/V sites, an optimized minimum, or orbital stability.

Kernel timing remains diagnostic. The new direct and RI times were84.5904 and50.0177seconds, but RI's metric was initialized before its SCF and execution order was fixed. No controlled speedup claim follows.

## Parent feasibility and next gate

The ordinary dense storage plan remains unsuitable for the prior10GiB screen:19,612 parent auxiliary functions require3,077,044,352bytes for one metric, before a separate factor. A separately prepared memory specialization uses shared-buffer factorization, bounded finite checks, factor-only PCM storage and AO block1. Its eight tiny tests pass, including an injected destructive factorization failure that must abort before native fallback. That implementation has not yet been qualified on these Mo references or through an SCF.

Its conservative arithmetic sum is10,622,806,400bytes (9.893259406GiB), retaining4GiB scratch and32AO-matrix allowances. Only114,611,840bytes remain below10GiB. Actual native transients, parent buffer aliasing and RSS remain unverified. This is not parent launch clearance.

Next: freeze and run retained-density J/PCM equivalence checks for the memory specialization, then a bounded small-reference SCF comparison. Only after those results and an independently reviewed parent resource protocol should a new parent attempt be considered. Keep W/V, basis/cavity sensitivity, proton-topology alternatives and physical identity as separate unfulfilled requirements.

Executed once with the existing environment: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/rij-jkfit-qualification/run.py --launch`. The driver refuses an existing run directory. Inspect `preparation.json`, `run-v1/result.json`, per-case arrays/checks/metric receipts and supervisor records. No threshold relaxation or retry occurred.
