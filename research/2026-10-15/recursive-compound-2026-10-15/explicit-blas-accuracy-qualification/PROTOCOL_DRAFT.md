# Conditional explicit BLAS controller accuracy qualification

Status: DRAFT FOR ROOT SCOPE REVIEW, preparation/design only. No numerical evaluation, implementation runner, approval, or qualification outcome is supplied. Parent two-J diagnostic outcome is UNKNOWN to this draft. Freeze the reviewed protocol, implementation, tests, source manifests and launch approval before evaluating the selected geometry. This draft is not itself a launch token.

## Recommendation and scope

Qualify the exact fresh-child explicit OpenBLAS1/PySCF4 controller against five reused Mo reference cases and one separately frozen prospective numerical case. Preserve both tight implementation-equivalence and original direct-accuracy gates. A parent repeated-J pass is a prerequisite, never an accuracy oracle. Do not run parent SCF, parent PCM, target geometries, optimization, frequencies or chemistry selection. W/V transfer is outside this minimum Mo-only qualification; a pass cannot authorize Mo34WV parent chemistry without a separate scope decision.

## Exact source reuse

All paths below are relative to recursive-compound-2026-10-15/.

* Controller: unchanged `parent-saved-metric-solve/run.py:single_blas_fresh_child`, used by `parent-explicit-blas-j/run.py`. Preserve approved interpreter/environment, `parent-blas-control-audit/probe.py:REQUESTED`, binary hashes, `_flapack`/LAPACK/OpenBLAS dpotrf symbol equality, fresh initial getter counts (4,4), explicit setter to (1,4), snapshots before/after setup and every numerical stage. Counts are configured limits, not measured teams. Child exits after restoration; getter restoration is not restoration of implicit control mode.
* Numerical implementation: unchanged `cpcm-rij-memory/memory.py`, `rij-jkfit-qualification/rij.py`, `cpcm-blocked/blocked_pcm.py`. Reuse `cpcm-rij-memory-qualification/run.py` operators, storage/reset/rejection checks and SCF checks; route outputs locally and add controller and strict new gates without editing old files. Reuse supervisor `parent-pilot/pilot.py:monitored_run`.
* Retrospective baselines: `rij-jkfit-qualification/run-v1/<case>/{arrays.npz,result.json,supervisor.json}`, its pins/receipts/preparation, and recursively pinned `rij-qualification-v2` direct references. Fixed case order: anion-water, neutral-water, anion-eps1, heldout-Mo2O7, new-external. Labels: initial, perturbed, direct_converged, RI_converged. Last case is H2Mo2O7, ICIQ100/28777. Every case and density has already been used; historical names containing heldout/new confer no freshness now.
* Gate/runtime guards: retain complete runtime source mapping and standard-library extension inventory from `parent-openmp-qualification-v2/run.py`, including actual imported module/native locations and hashes; retain rejection of missing, duplicate, reordered, malformed, failed or resource-limited records and exclusive SCF claims. Do not invoke that campaign's automatic launcher.

## Separately frozen prospective case

Use only `identity/next-step/pcm-heldout-selection/raw/HMo2O7.xyz`, unchanged atom order and Angstrom coordinates; do not execute its downloaded input. Original `selection.json`, `REPORT.md`, `acquisition.json`, metadata and input are provenance, all pinned. ICIQ100/28778, dataset 10.19061/iochem-bd-1-201, shared source family with reused external cases. XYZ SHA256 3133155e610321f92d1fe9735baa0f6192243aece1db91f90a8ab90f62b6f2f2; input SHA256 68d8fc04c461636ca17441d89bef1a9618a079244af5d7677e13193cdd0ff922. Validate 10 finite coordinates, Mo2O7H, charge -1 and exact raw hashes before launch. Original input spin is null, source-output spin unverified; preserve those facts.

Declared computational convention: RKS, PySCF spin=0 (Nalpha−Nbeta), closed-shell singlet ansatz. Electron arithmetic: 2×42+7×8+1−(-1)=142 all-electron electrons; Mo def2 ECP removes 28 per Mo, yielding 86 explicit electrons, 43 alpha and 43 beta. Validate actual ECP core counts and mol.nelectron=86 when later building the molecule; disagreement aborts. Even electron count permits this ansatz but does not establish a measured multiplicity or lowest-energy state. Do not inspect deposited output to infer spin or tune the choice. Source ADF/PBE/TZP/large-core scalar-ZORA/COSMO and exported geometry are not method-equivalent to this PySCF calculation; exported coordinates differ from input starting coordinates, with no verified stationary point. Freshness means no numerical comparison found in the recorded audits; aliases, transformed geometries and outside use remain possible. Reaudit manifests for the identifier/hash before freeze; discovered prior numerical use removes prospective status and blocks this preregistered holdout, without silently replacing it.

## Frozen numerical settings and acceptance bounds

Every case: PBE/def2-SVP, Mo def2-SVP ECP, fixed def2-universal-jkfit, RKS spin0, grid level2, direct_scf=True/direct_scf_tol=1e-13, max_memory=512 MiB, no checkpoint, C-PCM/SWIG Lebedev17/vdw_scale1.2/probe0/epsilon78.4; epsilon1 only for existing anion-eps1. Initialize get_hcore before immutable molecule fingerprints. SCF conv_tol=1e-11 Eh, conv_tol_grad=1e-7, max_cycle60, no retry. Preserve original initial-density generator. Fresh deterministic perturbation uses NumPy default_rng(7392016), Gaussian matrix symmetrized as (A+A.T)/2, scaled to Frobenius norm0.01; exact implementation/version pinned.

All error gates are absolute with relative tolerance zero, finite required; no sign cancellation in maxima. Preserve:

| Observable | Bound |
|---|---|
| Memory J versus saved native RI J, every retrospective density | max abs <=1e-10 Eh |
| Memory J versus contemporaneous unchanged native RI J, prospective densities | max abs <=1e-10 Eh |
| MemoryPCM versus unchanged BlockedPCM, each density | abs energy and max abs q/V each <=1e-10 |
| Memory J versus direct J, every density | max abs <=1e-3 Eh |
| Coulomb energy discrepancy | abs(0.5 Tr[P(Jmemory−Jdirect)])/nMo <=1e-3 Eh per Mo |
| finite symmetric J | max asymmetry <=1e-10 |
| J zero and incremental additivity | max abs <=1e-9 |
| PCM affine q/V F(P+dP)−F(P)−F(dP)+F(0) | max abs <=1e-10 |
| epsilon1 energy/q/V | abs/max abs <=1e-10 |
| reset/rebuild initial PCM energy/V | abs/max abs <=1e-10 |
| retrospective H2Mo2O7 SCF versus saved JKFIT SCF | abs energy <=1e-8 Eh; max abs density <=1e-5 |
| prospective RI SCF versus new direct SCF | abs total energy/nMo <=1e-3 Eh per Mo |
| full solvent-aware MemoryRI Fock gradient norm at RI-converged density/orbitals only | <=1e-5 |
| full solvent-aware direct Fock gradient at RI density | <=1e-3 |
| electron trace | abs Tr[PS]−Ne <=1e-8 |

Require SCF convergence explicitly. Apply the MemoryRI Fock stationarity gate only to RI-converged density/orbitals, never to direct-converged density/orbitals. The direct full solvent-aware Fock residual at the RI-converged density/orbitals retains <=1e-3. Retrospective direct matrices are saved `<label>_Jdirect`; recompute direct J at all four saved densities under the explicit controller as well, compare to saved direct matrices at the existing strict implementation bound1e-10 and use new direct J for direct-error screening. This separates changed runtime from RI approximation. Prospective direct/nativeRI/BlockedPCM comparisons share a runtime, so their agreement alone cannot establish independent correctness; retrospective pinned cross-runtime references are essential. Do not require PCM energy additivity or homogeneous q/V because nuclear offsets and quadratic energy invalidate those tests.

Storage/behavior checks remain mandatory: RI metric built with initial J before any PCM intermediates; AO block1; Fortran/read-only metric and surface factors, actual same-pointer/shared-memory in-place factor receipt, factor identity reuse, no retained S, no four-center ERI or stored three-index tensor, CD factor type/no fallback. Verify reset clears caches and builds new surface factor. Preserve rejected nuclear gradient/Hessian/response/TDA/TDDFT paths. No replacement rho or factor, basis adjustment, grid change or threshold tuning.

## Stages and resource budget, after approval only

1. Five sequential retrospective operator children, all run once even after an ordinary numerical failure. Twenty saved-density comparisons with above gates; zero SCFs. Any source/runtime/controller failure halts remaining execution because prerequisites are no longer trustworthy. Complete and persist each operator before classifying errors.
2. Only all five complete all-pass receipts plus unchanged pins unlock one H2Mo2O7 MemoryRI SCF, initialized from saved initial density. Preserve original retrospective SCF and direct full-Fock checks. No new direct SCF.
3. Only stages1–2 passing unlock one HMo2O7 operator child: initial and perturbed densities, nativeRI/direct/BlockedPCM comparisons, zero/additivity/affine/reset/storage checks. No SCF. This consumes the prospective case; no substitution if it fails.
4. Only stage3 passing unlock one HMo2O7 SCF child: one direct BlockedPCM SCF and one MemoryRI+MemoryPCM SCF, both from the same frozen initial density. Persist direct convergence, energy, density before RI work; failed direct convergence blocks RI. At both converged densities repeat all direct/nativeRI/MemoryRI and BlockedPCM/MemoryPCM comparisons. Persist orbitals/occupations/overlap/full solvent Focks for independent residual checking. Require all table gates at their specified densities and storage invariants: the operator-comparison gates apply at both converged densities; MemoryRI stationarity <=1e-5 and direct Fock residual <=1e-3 apply at RI-converged density/orbitals only. No RI stationarity gate is imposed at the direct-converged density. Do not compare prospective energies to deposited ADF outputs.

Each child: 180-second wall cap, sampled RSS2GiB through unchanged process-group supervisor, sequential exclusive execution, no implicit retry. At most8 children and3 new SCFs, cap sum1440s (24min) excluding overhead. RSS sampling does not certify peak memory. Each SCF has a separately exclusive claim marker written before kernel invocation, including direct worker entry. Resource failure is an incomplete qualification under these bounds, not evidence of inaccurate chemistry; never silently extend bounds or relaunch.

## Freeze, gatecheck and evidence contract

After root scope review, implement the smallest local adapter and pure/mock tests; tests must cover every missing/reordered/duplicate/wrong-phase/empty-check/nonfinite/malformed/controller-mismatch result, resource failure, stale pin, direct-worker bypass, SCF-count cap and output exclusivity. Preparation performs raw/source checks and no operators. Pin this final protocol, adapter/tests, prospective declaration, untouched provenance, all original manifests and actual reference arrays/results/receipts, runtime sources/binaries/basis, controller, supervisor, and the completed parent diagnostic artifacts plus independent review. Historical report status alone is insufficient: independently verify arrays, all metrics/checks and supervisor receipts. The parent prerequisite must include A/B full-J repeatability <=1e-10, symmetry/storage/controller gates, completed arrays, accepted supervisor and unchanged pins; retain historical-reference comparisons descriptively and do not substitute them for repeatability/accuracy.

`--gate-check` (future interface, not implemented here) must perform no native operators, emit exact preparation SHA256, matching root approval, all required manifest identities, fixed case/order/settings/counts/budgets, absent run output, parent prerequisite evidence and prospective raw hashes. Any missing requirement fails closed. Recheck pins before every child, between gated phases and at end. Direct worker invocation must enforce the same phase/claim gates. Root approval binds preparation digest and test artifacts. A changed manifest needs a new reviewed attempt, never silent repinning.

Each child preserves native.log/stdout/stderr files with their hashes and byte sizes, supervisor.json, thread identity/snapshots, factor/metric receipts, incremental checks and arrays closed before further postchecks. Successful stderr may be empty; never require or fabricate nonempty stderr. Validate stdout/native logs only for specifically required protocol evidence, not arbitrary nonempty bytes; structured receipts and arrays must contain the required parseable evidence. Parent results retain expected/executed/skipped case IDs, explicit reason, counters and pins. Independent review recomputes all stated differences and solvent-aware residuals from arrays, verifies exact expected check names/counts rather than trusting arbitrary all-pass lists, and verifies no unexpected child or SCF.

Outcomes are separate: FAIL_PREREQUISITE (no launch), FAIL_RETROSPECTIVE (holdout unconsumed), FAIL_PROSPECTIVE_OPERATOR, FAIL_PROSPECTIVE_SCF, INCOMPLETE_RESOURCE_OR_EXECUTION, or PASS_SCOPED_EXPLICIT_CONTROLLER_NUMERICS. Preserve all failures. No pass means qualified target identity, parent SCF readiness, experimental validity, stability, retention, inheritance or life/intelligence. Zero physical admissions. No outcome-dependent method/gate/case tuning; any redesign is a new preregistration and this case is thereafter reused.
