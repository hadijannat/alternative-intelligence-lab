# Independent OpenMP v2 terminal-result audit

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []
Numerical result: PASS_RETROSPECTIVE_RUNTIME_EQUIVALENCE within the frozen scope.

Root confirmed launcher62048 exit0 before review. This reviewer used parent-openmp/env-aligned/bin/python, read the protocol/source/preparation and completed artifacts, and ran only saved-array arithmetic and source/runtime guard reconstruction. No molecule, integral, PCM operator or SCF was generated. Reproducible evidence: .omo/evidence/openmp-v2-result-audit/check_arrays.py, array-audit.json, runtime-guard.json.

## Pins, process and case admission

All2524 pinned entries hash-match:102 original inputs/sources,2419 runtime files,3 driver/protocol/test files. Live manifest reconstruction equals preparation, including original-to-imported byte-equivalent source checks, actual isolated module/native paths and versions. All77 lib-dynload extension files are frozen, including _elementtree and pyexpat. The exact fourteen ordered child/result gate passes. Every child records the requested actual PySCF thread count (1 or4), the approved interpreter and loaded native hashes contained in the manifest. The worker source additionally enforces OMP_NUM_THREADS and BLAS controls1; those environment values are guarded in the executed source rather than separately saved verbatim.

All14 operator receipts match their supervisor records and have exit0, no monitor/termination error, wall<180seconds and sampled RSS<2GiB. All operator records have zero SCFs and runtime_guard_pass=true. The sole SCF receipt also matches and passes; scf-claimed.json restricts the claimed case to new-external at4threads, maximum1. Its sampled maximum RSS is826408960bytes and wall27.723825seconds. No parent case is present.

There are520 recorded operator checks: five Mo cases contribute214 at each thread level (42+42+46+42+42), and W/V contribute46 at each thread level (23+23). The SCF adds9, total529. All529 are true. These include numerical comparisons and recorded structural/runtime controls; they are not529 independent experiments.

## Independent matrix arithmetic

All56 saved densities (7cases x2thread levels x4density states) exactly match original campaign inputs. All56 Jmemory matrices agree with the original saved RI J matrices within1e-10. Largest J difference is2.8812507935072063e-12Eh at4threads/new-external. All saved arrays are finite.

For all40 Mo density states, contemporaneous oracle energy/q/V differences were independently computed from saved paired arrays and meet1e-10. Largest oracle energy difference is1.6653345369377348e-16Eh; V<=8.881784197001252e-16 and q<=1.2067170179763664e-16. Saved Mo delta/zero J controls satisfy1e-9; affine PCM q/V controls satisfy1e-10; epsilon1 response is zero within1e-10. Saved factor pointer/share/read-only/Fortran observations pass.

For all16 W/V density states, paired scalar oracle energies independently agree within1.6653345369377348e-16Eh. For the8 W/V converged states, PCM q/V also independently agree with original W/V arrays: V<=1.1102230246251565e-15, q<=1.691355389077387e-15. W/V contemporaneous oracle q/V, deltaJ and zeroJ are not retained in these NPZ files, so those checks could only be verified as saved passing measurements and inspected source logic, not recalculated independently. This limitation does not affect the56 direct saved-J comparisons.

The4thread new-external SCF independently yields:
- Density max error versus saved native RI:2.3101520696400257e-12 (limit1e-5).
- Energy difference:2.2737367544323206e-13Eh (limit1e-8); native convergence log agrees with recorded energy.
- Full memory Fock orbital-gradient norm:1.4843925966025415e-7 (limit1e-5).
- Direct Fock orbital-gradient norm:1.8679534504511042e-4 (limit1e-3).
- Electron trace error:2.842170943040401e-14 (limit1e-8).

Saved initial/reference densities match their originals; density reconstructs from occupations/orbitals within1e-12 and overlap orthonormality holds within1e-10. Gradients use independently evaluated2*C_virtual.T*F*C_occupied. Total DFT energy was checked against logs and saved baseline, not rebuilt from quadrature/integrals. Thresholds are unchanged from the original memory qualification.

## Findings by severity and skill perspective

CRITICAL: none.
HIGH: none.
MEDIUM: none blocking scoped retrospective acceptance.
LOW: W/V operator NPZs omit contemporaneous oracle q/V and delta/zeroJ arrays, limiting independent reconstruction of those recorded checks. Preserve this distinction in downstream claims; no new scientific run is warranted merely to fill it.
LOW: untyped/dense driver code remains a strict-programming maintainability deviation, consistent with preceding campaign scripts.

Programming and remove-ai-slops perspectives were loaded in this review session and applied. The scope uses necessary provenance guards and a bounded W/V operator counterpart because the existing W/V worker always performs SCFs. No deletion-only or brittle prose tests were identified from the inspected review context; no test suite or repository lint/typecheck/security scan was rerun for this terminal artifact audit. Full-source gate review and saved numerical evidence support this conclusion; no misleading fresh scientific validation is implied.

The old parent-openmp-qualification/run-v1/result.json remains FAIL with phase1_pass=false and phase2_skipped=true. It was inspected and not modified. This audit confirms continued presence/status, not a fresh historical byte-for-byte snapshot of every prior failure file. The repair adds complete stdlib-extension coverage; it does not remove the loaded-library guard.

Approval establishes retrospective runtime agreement only. It is not a fresh holdout, physical admission, experimental validation, parent readiness, speedup benchmark or parent memory guarantee. The earlier parent WALL_LIMIT remains independent negative evidence. A separately reviewed parent first-J attempt is outside this audit.
