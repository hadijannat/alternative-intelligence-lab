# RI-J repair campaign: two numerical failures retained

**The proposed Coulomb approximation does not pass the frozen qualification and is not admitted for a parent calculation.** All five SCFs converged, but neutral MoO3 and the external Mo2O7 challenge exceeded the direct-Fock residual limit. Small total-energy errors alone did not establish adequate orbitals under the direct reference operator. No threshold, auxiliary basis or chemical setting was adjusted after seeing results.

| Fixed case | Absolute total-energy difference per Mo, Eh | Direct-Fock residual at RI solution, Eh | Limit, Eh | Numerical disposition |
|---|---:|---:|---:|---|
| Hypothetical MoO4(2-), water dielectric | 0.000134120181 | 0.000651886558 | 0.001 | Pass in this case |
| Hypothetical MoO3, water dielectric | 0.000117862233 | 0.001151565935 | 0.001 | Fail |
| Hypothetical MoO4(2-), epsilon1 | 0.000133650107 | 0.000635401713 | 0.001 | Pass in this case |
| External fixed Mo2O7(2-), water dielectric | 0.000112274219 | 0.001096362264 | 0.001 | Fail |

Across81 recorded checks,79 satisfied their thresholds and these two did not. Aggregate status is FAIL_NUMERICAL_SCREEN; the tally is not a chemical success rate. Maximum absolute Coulomb matrix error was0.000527555087Eh and maximum absolute Coulomb energy difference perMo0.000182648928Eh, each within its own unchanged screen. Electron trace errors were at most about1e-13. All recorded native RI-J calls used Cholesky factors, returned finite matrices and left three-index caches/output unset. The direct full solvent-aware Fock at each RI density supplies the residual; it is not the already-small RI self-consistency residual.

The new external direct and RI calculations both took24cycles, at energies−662.834329575359 and−662.8345541237971Eh. Recorded kernel times were53.479 and26.078seconds. These are diagnostics, not a controlled cold-start speed benchmark: direct SCF preceded the comparison calls, while the RI metric was already initialized before RI SCF. No parent throughput is inferred. Every child finished within180seconds and sampled RSS2GiB, with no timeout or monitor error; maximum sampled RSS across the campaign was615,055,360bytes. This is sampled RSS, not a hard or certified peak bound.

## Repair and held-out scope

Original sibling `rij-qualification/run-v1` remains a software failure with partial arrays and complete exception/supervisor records. Its strict environment guard rejected PySCF's lazy initialization of ECP routing fields18/19. V2 first initializes the core Hamiltonian, then installs the unchanged guard. Eleven synthetic/mocked tests, including the real ECP initialization regression, passed without launching SCFs. Both original and repaired source pins remain unchanged after their runs.

All geometries, thresholds, the def2-universal-jfit basis and resource limits were declared before v1 results. The external Mo2O7 geometry was a predeclared numerical holdout. Its direct baseline became visible during v1; v2 is a documented post-fix continuation with no changed scientific method, not newly unseen validation. In v1 no RI matrix was produced for this external case and no RI SCF completed in any case. The retained source is a computational geometry with incomplete minimum evidence; its original PBE/TZP/ZORA/COSMO energy was never compared to PySCF absolute energy. Experimental target validation remains false.

## Consequence for the requested compound

Do not launch the parent with this approximation based on the two passing molybdate controls. A separately frozen alternative must improve the failed cases and use a new uninspected numerical challenge if claiming fresh held-out evidence. The parent resource calculation also remains open:9828 auxiliary functions require772,716,672bytes for one dense metric; allowing metric plus factor adds1,545,433,344bytes to the earlier allocation screen, bringing it above10GiB. Qualification would not by itself authorize a parent launch.

The installed two-pass Coulomb implementation and auxiliary-basis choice follow the [PySCF density-fitting documentation](https://pyscf.org/user/df.html). The external geometry and attribution are pinned in PROTOCOL.md to [ICIQ item100/28779](https://iochem-bd.iciq.es/browse/handle/100/28779). No chemical function, target structure, new complement or intelligent-life claim is admitted.

## Reproduction record

Executed once: `./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/rij-qualification-v2/run.py --launch`. This existing run must not be overwritten or repeated automatically. Inspect `run-v1/result.json`, each case's `result.json`, `arrays.npz`, `metric-calls.jsonl`, native log and supervisor receipt. The driver rejects an existing campaign directory. Unit tests can be rerun with the same interpreter and `-m unittest discover -s recursive-compound-2026-10-15/rij-qualification-v2 -p test_rij.py`.
