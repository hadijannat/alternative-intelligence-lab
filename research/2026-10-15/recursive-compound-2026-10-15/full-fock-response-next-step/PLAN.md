# Next integration test: full fixed-geometry Fock response

Status: **DRAFT_NOT_IMPLEMENTED_OR_AUTHORIZED**. This plan follows the independently reviewed C-PCM response component pass. It authorizes no run and does not replace the nominal Mo34WV target with its small numerical reference.

The next necessary numerical question is whether the RI Coulomb, PBE exchange-correlation and solvent response contributions combine into the derivative of the same full Fock matrix. The standalone solvent pass cannot answer that question. Proposed candidate:

R(deltaP) = J_RI(deltaP) + f_xc[P0](deltaP) + R_PCM(deltaP).

Use a dedicated bare real RKS object with the existing parent memory-specialized JKFIT installation, PBE/grid2 and the v2 standalone MemoryPCM response at epsilon 78.4. Production GroundStateOnly guards stay unchanged. PySCF's ordinary RKS response with singlet=None, hermi=1 combines the cached PBE kernel and mf.get_j; pass an explicit bounded max_memory rather than its implicit minimum of 2000 MB. The precise implementation, memory value and pins must be fixed before approval.

Independently evaluate full ordinary Fock matrices F(P) = hcore + J_RI(P) + V_xc(P) + V_PCM_stock(P), without using fxc in the oracle. Compare the candidate action with central differences. Use stock ground-state PCM explicitly so its tagged Fock contribution cannot be omitted. Exclude DIIS, damping, level shifts, frozen solvent and SCF iteration. The oracle shares integral/runtime/RI libraries and tests derivative consistency, not independent chemical accuracy.

## Retrospective inputs and directions

Use only rij-jkfit-qualification/run-v1/anion-water/arrays.npz, with the existing anion-water geometry/basis provenance. Root confirmed these saved keys exist: RI_mo_coeff (87x87), RI_mo_occ (87), RI_converged_P (87x87), overlap (87x87). The saved case is marked converged and not held out. Validate orbital orthonormality under overlap, occupations, reconstructed density and electron count. Record the current full-Fock orbital residual descriptively; derivative consistency alone does not establish stationarity.

Freeze zero, HOMO-LUMO and deterministic mixed occupied-virtual rotation directions, mixed seed 7392016. Construct exactly symmetric AO tangents and normalize nonzero tangents to Frobenius norm 0.01. Generate displaced densities through orthogonal orbital rotations preserving occupations and electron count, rather than arbitrary AO perturbations. With antisymmetric rotation K and occupation matrix N, C(h)=C exp(hK), P(h)=C(h)N C(h)^T and deltaP=C(KN-NK)C^T. Numerical symmetrization conventions must be specified before results.

Build the integration grid once at P0; require identical grid coordinates and weights for response and all finite differences. No grid rebuilding/pruning-dependent target should be silently compared with a fixed-grid kernel. Preserve source guards, factors, geometry and response-owned caches; distinguish expected updates to the oracle's own ground-state cache.

## Proposed acceptance, to freeze before execution

- Central steps 0.001 and 0.0005; maximum absolute action/FD discrepancy <=1e-8 at both, relative tolerance zero.
- FD step-to-step discrepancy <=1e-8; finite symmetric outputs, zero response and reciprocity within 1e-10.
- Electron-trace error <=1e-8, validated fixed geometry/grid/inputs/factors, no SCF or holdout consumption.
- Retain orbitals, density, baseline Fock/residual, generators, tangents, displaced densities/Focks, decomposed J/XC/PCM responses, all errors, source/runtime hashes and supervisor observations before final classification. Preserve every failed comparison.
- One separately reviewed fresh child, proposed 120 seconds and 2-GiB sampled RSS, one requested/verified thread, no automatic retry. Prove fresh-process full-import pin equality before launch.

A pass would support fixed-geometry full-Fock derivative consistency on this retrospective reference. It would not establish the complete orbital-Hessian action, stability eigenvalue convergence, external complex/spin channels, nuclear derivatives, parent accuracy or exact-target identity. The parent's full-J failure and unchanged 1e-10 criterion remain; the prospective HMo2O7 holdout remains unused. All twelve integrated functions and 24-role/zero-complement status remain open.

Source basis: parent-openmp/env-aligned/lib/python3.12/site-packages/pyscf/scf/_response_functions.py, cpcm-rij-memory/memory.py, rij-jkfit-qualification/rij.py, derivative-route-audit/REPORT.md and cpcm-response-probe-v2/analysis.json. This is a source-reviewed next-step design; implementation and independent frozen prelaunch review remain required.
