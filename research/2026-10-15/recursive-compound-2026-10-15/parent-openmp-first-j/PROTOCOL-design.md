# Proposed bounded parent first-J probe

Design only. No driver, preparation, parent-array load, molecule build or numerical launch is authorized by this document. Root placed implementation on hold after reported W/V errors in the first runtime-qualification campaign. Preserve that campaign and the earlier failed parent attempt unchanged. A terminal passing runtime qualification and independent root review are prerequisites; neither is asserted here.

## Proposed scope

One subprocess, one `mf.get_j(dm=saved_density)` request on the unchanged P0_A geometry, charge -8, spin 0, def2-svp basis/ECP and def2-universal-jkfit auxiliary basis. Reuse the exact qualified MemoryRI implementation in the approved aligned runtime. The parent has 196 atoms, 3068 AOs, 1568 explicit electrons and 19612 auxiliary AOs, subject to verification. Read the earlier `parent-pilot-memory/run-v1/partial.npz` cycle-zero density; never create a replacement guess. Validate its pinned bytes, exact density shape and float64 dtype, finiteness, symmetry to 1e-12, and scalar integer cycle zero.

Use a standalone worker. It must not import or invoke any parent SCF worker. Read the original parent preparation pins, metadata, P0_A.xyz, site mapping and historical outcome artifacts. Reuse the unchanged RKS/PBE and MemoryPCM attachment settings, leaving PCM unbuilt; explicitly reject PCM build and SCF entry. No surface matrix, grids, optimization or SCF is in scope. Calling the unchanged MemoryRI install may perform its normal core-Hamiltonian setup, which must be timed separately from the single first-J request.

## Proposed admission and supervision

Require an identified terminal runtime qualification whose current frozen source/native-runtime manifest still matches. Verify all fourteen ordered 1/4-thread operator children through their separate receipts, supervisor files, case/thread identities, all checks, runtime guards and zero SCF counts. Require the one successful gated small SCF and its matching accepted supervisor receipt, plus terminal PASS and phase-one gate. Freeze these artifacts and preserve prior negative outcomes.

Preparation may freeze only reviewed inputs and driver/protocol/tests. An independent root review must bind its preparation digest and complete terminal qualification artifact map. Before launch and inside the child, verify the same review, sources, saved density and runtime. Use an exclusive fresh run directory and worker claim; no retries or duplicate launches.

Proposed limits: 300 seconds and 10 GiB sampled RSS, using the existing process-group supervisor. RSS is monitored, not a hard OS allocation cap. Verify actual PySCF OpenMP thread count 4 before the call; BLAS control variables remain 1. One child maximum, one J request maximum, zero SCFs maximum. Parent execution remains subject to independent review of these proposed limits.

## Proposed observables and evidence boundary

Record setup/start/return stage timestamps, actual runtime/thread/native-library identity, factor allocation and alias evidence, RI metric shape, factor immutability and Fortran layout, elapsed first-J seconds, and sampled child peak RSS. If J returns, save J and check exact AO shape, finiteness, symmetry to 1e-10, exactly one RI call, no ERI, no cached or output three-index tensor, and no PCM intermediates or surface. Retain stage, factor, supervisor, stdout/stderr and failure evidence if the child cannot finish.

Successful completion would show that this first parent Coulomb construction finished inside the stated limits with the storage checks satisfied. It would not establish SCF performance, SCF convergence, parent readiness, numerical equivalence against a complete parent oracle, physical admission or experimental chemistry. No whole-SCF performance or speedup claim follows.

Planned synthetic checks cover missing/failed terminal qualification, incomplete or malformed receipts, mismatched root-review bindings, changed pins, invalid cycle/density fixtures, output containment, duplicate claims, and one-child/zero-SCF routing. Small synthetic arrays may be used; no real parent arrays are needed to validate guards.
