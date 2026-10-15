# C-PCM blocked qualification

Status: PASS_IMPLEMENTATION_EQUIVALENCE_ONLY. No physical admission and no parent SCF.

The implementation specializes the installed PySCF 2.14.0 SWIG equations: off-diagonal S_ij = erf(xi_i xi_j r_ij / sqrt(xi_i²+xi_j²))/r_ij; diagonal S_ii = xi_i sqrt(2/pi)/switch_i. With f=(eps−1)/eps, q=−f S⁻¹v, q_sym=q, E=q·v/2; the AO potential is the negative AO/charge contraction. No D or dense R is built.

S is constructed in 128-row blocks. S and a reusable Cholesky factor remain resident. AO-surface blocks default to 8; each tensor and fake molecule is explicitly deleted before the next integral call. Reset clears surface, nuclear potential, intermediates/factor, density, energy and AO potential. Factorization failures propagate without regularization or alternate solver. Public attached gradient/Hessian/response/excited-state/post-SCF entry points reject explicitly. Direct use of upstream internal factories is outside this interface.

## Observed checks

| Case | Cycles | Absolute energy difference (Eh) | Solvent-aware residual | Electron trace error | Wall seconds |
|---|---:|---:|---:|---:|---:|
| anion-water | 16 | 1.47793e-12 | 1.51038e-07 | 7.10543e-14 | 13.405 |
| neutral-water | 14 | 1.13687e-13 | 7.24447e-08 | 4.26326e-14 | 7.567 |
| anion-eps1 | 17 | 4.54747e-13 | 3.47005e-08 | 2.13163e-14 | 12.793 |

Maximum surface S discrepancy/error across recorded checks: 0.

Maximum nuclear potential discrepancy/error across recorded checks: 3.55271368e-15.

Maximum electronic potential discrepancy/error across recorded checks: 0.

Maximum surface charge q discrepancy/error across recorded checks: 1.49359691e-15.

Maximum solvent energy discrepancy/error across recorded checks: 2.77555756e-16.

Maximum AO potential discrepancy/error across recorded checks: 7.21644966e-16.

Maximum normalized backward error discrepancy/error across recorded checks: 5.29680187e-17.

Maximum centered-density derivative error: 5.71025278e-12 Eh, at frozen h=1e-4 and 5e-5 with seed7392016 and ||deltaP||F=0.01.

Every operator comparison was repeated for initial, symmetrically perturbed and new converged densities at blocks 1, 7 and 8. All three cases have absent cached four-center ERIs. Repeat build, reused factor, geometry-reset S/nuclear comparison, cache invalidation and API/method guards passed. The separately induced negative-S Cholesky failure was expected and retained in boundaries.json, with no fallback. No calculation failed; no retry or tolerance change occurred.

## Reproduction and artifacts

Invocation from workspace root:
```sh
./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/cpcm-blocked/qualify.py
```
The supervisor records argv, return codes, stdout/stderr and wall time in evidence/receipts.json; it refuses to overwrite result.json. Exactly three SCFs were launched, each in a child with a 90-second timeout and all five thread environment requests set to one. Boundary checks were invoked with the same interpreter and thread variables via check_boundaries.py and launched zero SCFs.

For every numerical scenario, evidence/{case}.json contains the scenario, exact observable and boolean verdict. evidence/{case}.npz captures densities, perturbation, S, nuclear/electronic potentials, q, energies and AO matrices for independent comparison; evidence/{case}.scf.log and stdout/stderr contain raw outputs. result.json contains main-run receipts and hashes; SHA256SUMS.json covers the completed artifact set.

## Allocation estimates and limits

Parent-size estimate (9,284 surface points, 3,068 AOs): S plus factor = 1,379,082,496 bytes; one AO block8 result = 602,407,936 bytes; upstream block400 = 30,120,396,800 bytes. See allocation.json for row temporaries, finite-check buffer, AO output and contraction temporary; these estimates are not certified peak RSS.

No parent timing, parent numerical stability, certified RSS peak, gradients, aqueous identity, target incorporation or integrated life function was tested. A later parent run still requires explicit resource preflight, the 10 GiB sampled RSS guard and root review. The retained parent-pilot rejection is unchanged.
