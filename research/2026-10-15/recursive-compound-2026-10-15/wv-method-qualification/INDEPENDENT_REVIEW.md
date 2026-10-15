# Independent W/V numerical audit

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []
Numerical audit: PASS_NUMERICAL_SCREEN_ONLY for both fixed geometries.

Root confirmed launcher session 37378 terminated with exit 0 before this audit. Read-only scientific-artifact inspection followed; no new operator, molecule, PCM surface, SCF, retry or scientific-source edit was performed. The reproducible audit script and output are at .omo/evidence/wv-numerical-audit/check_arrays.py and array-audit.json. Run the script from the repository root using the pinned environment interpreter. An initial inline audit command had a syntax typo and never executed; the saved corrected script executed successfully.

All 30 current SHA256 pins match preparation.json and run-v1/pins.json. Both case receipts match supervisor.json, exited zero without termination or monitor error, and used the frozen 180-second/2-GiB guards. Both result records have 20 passing checks and exactly two SCFs; the final record reports four total. No physical admission or experimental validation is claimed. The independent source/geometry/charge/spin checks are documented in PRELAUNCH_REVIEW.md and remain covered by unchanged pins.

## Recomputed saved-array results

| Metric | WO4 | VO4 | Frozen limit |
|---|---:|---:|---:|
| Largest AO J error over four densities (Eh) | 5.944925e-5 | 3.766003e-5 | 1e-3 |
| Largest absolute Coulomb error per metal (Eh) | 1.374620e-4 | 6.170985e-5 | 1e-3 |
| Total SCF energy difference per metal (Eh) | 4.853319e-5 | 6.001045e-5 | 1e-3 |
| Direct full Fock gradient at RI orbitals | 7.845566e-5 | 7.774269e-5 | 1e-3 |
| RI full Fock gradient | 3.534454e-7 | 5.893231e-8 | 1e-5 |
| Direct electron trace | 48.000000000000014 | 58.00000000000002 | target 48 / 58, error <=1e-8 |
| RI electron trace | 48.000000000000014 | 58.00000000000003 | target 48 / 58, error <=1e-8 |

The audit recomputed each initial, perturbed, direct-converged and RI-converged J difference and 0.5 Tr[P(Jri-Jdirect)] directly from arrays, rather than trusting recorded check values. All arrays are finite; both direct and RI J matrices and densities are symmetric within 1e-10. RI J asymmetry is exactly zero. Direct and RI initial densities are identical. The perturbation exactly reconstructs from seed7392016 with the frozen symmetric norm0.01 procedure.

Both converged densities reconstruct from saved orbitals/occupations within1e-12, and overlap orthonormality holds within1e-10. Fock gradients were recomputed as the Euclidean norm of 2*C_virtual.T*F*C_occupied. Energy differences match saved results; each native log contains exactly two convergence-energy lines agreeing with the two saved total energies within1e-10. Full total energies were not reconstructed from integrals or DFT quadrature because that would require new scientific work.

The iteration records have exactly sequential cycles consistent with both results: WO4 direct15/RI15; VO4 direct17/RI16. Sequential metric-call receipts number22 and23, respectively, all CD, finite-J, no cached three-index tensor and no tensor output. Worker storage checks record no retained S, no ERI and no three-index cache. Those are saved process observations, not independent reconstruction of the finished process heap.

WO4 wall14.5890seconds / sampled maximum RSS495779840bytes; VO4 wall17.6522seconds / sampled maximum RSS514736128bytes. These maxima are samples, not certified peaks or hard OS limits.

## Findings by severity and skill review

CRITICAL: none.
HIGH: none.
MEDIUM: none affecting this fixed-geometry numerical screen.
LOW: run.py's untyped record dictionaries and compressed statements fall short of the strict programming style perspective, as already documented in prelaunch review. No demonstrated numerical failure follows from that style in these artifacts.

Programming and remove-ai-slops skills were loaded during this review session and applied to production/tests. The four relevant tests independently passed during prelaunch review. No deletion-only/removal-verification, brittle prompt or tautological tests were found; source mutation tests exercise actual admission boundaries. No needless parsing/abstraction was identified. Full-repository lint/typecheck/security scans were not performed. No committed baseline diff or notepad path was supplied; review scope is the complete new qualification files and saved run artifacts.

These are fixed-geometry numerical challenges for the selected W/V monomers, not experimental holdouts, target-incorporation proof, Mo36 stability evidence or chemical admission. Passing these small cases does not change the parent pilot's preserved WALL_LIMIT result or establish parent-scale feasibility. No failure was removed or rerun.
