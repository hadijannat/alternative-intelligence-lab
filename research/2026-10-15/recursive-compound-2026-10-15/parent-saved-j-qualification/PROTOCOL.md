# Single-use saved-J handoff: small retrospective qualification

Status: implementation and synthetic tests only; no preparation, operators, SCF or parent work has run. Independent root review is required before preparation and launch. Existing failed campaigns, runtime qualification, successful parent first-J artifacts and published records are immutable inputs.

## Workload and fixed bounds

Only the already inspected neutral H2Mo2O7 `new-external` geometry is used. Two sequential children are permitted: an effective-potential/operator comparison, then one cached SCF only after the operator child is accepted. Each child has 180 seconds and a sampled 2 GiB RSS guard, four actual OpenMP threads and BLAS controls of one. Aggregate child wall caps are 360 seconds plus setup/validation overhead. At most one SCF, at most 60 cycles, no retries or extra children. RSS monitoring is not a hard allocation limit.

The unchanged existing process-group supervisor is reused. Unique run and worker-claim files reject duplicate execution. The launcher retains full receipts, partial parsed results and parse/supervisor/gate errors on failure. Actual runtime package/interpreter/source/native inventory is checked against the frozen successful v2 runtime qualification, in addition to actual thread checks. No numerical parent data is loaded by this runner: parent J is only streamed for a provenance digest. The parent J is never recomputed.

## Admission and frozen inputs

`--prepare` first validates the completed parent first-J gate, accepted independent supervisor and terminal result, passing storage checks, one J/zero SCFs, exact saved J digest and unchanged original/runtime pins. It additionally requires the completed fourteen-operator/one-SCF OpenMP qualification. It freezes first-J source/protocol/review/preparation/result/receipt/density-validation/native-observation/factor/stage/NEXT_STEP artifacts, the approved small operator and SCF references, geometry/charge metadata, and this driver/wrapper/tests/protocol.

The small proof uses only the accepted 4-thread runtime-v2 `operators-new-external/arrays.npz`. The fixed runner derives and freezes `density_sha256` from that archive's `initial_P`; `j_key=initial_Jmemory`, `density_key=initial_P`, case `new-external` and operator-phase result identity are fixed. Thus the density/J pair and accepted case originate from the same pinned archive. The wrapper checks that supplied immutable density against the frozen digest. A caller-supplied proof alone is not an independent input/runtime admission: the runner's frozen manifest and root review provide that binding.

An `independent-root-review.json` must carry status `APPROVED_SMALL_SAVED_J_QUALIFICATION`, `independent_root_review: true`, a nonempty reviewer and the exact preparation SHA256. The launch gate freezes this review's digest; each worker and completion recheck it and all preparation pins. Commands are explicit `--prepare`, `--gate-check`, `--launch`; there is no default execution. Run with the qualified aligned interpreter. This implementation is submitted unfrozen for review.

## Single-use ownership and request semantics

`handoff.install` attaches only to a fresh MemoryRI instance with no native calls, no RI factor and the qualified 1e-13 screening cutoff. It keeps a reference to the exact immutable initial density and a row-streamed content digest, without copying the density. It stores only frozen provenance metadata until consumption; no J array is loaded during installation.

The first supported J-only request must use that exact density (shape, float64 values and digest), the same molecule object and unchanged coordinates/basis/environment, PBE, direct SCF, def2-universal-jkfit, Hermitian flag 1, omega None, and no three-index tensor/cache output. A mismatch raises before consumption or native fallback. The cutoff remains fixed for later requests too.

At the accepted first request, streamed file digests and independent supervisor/result provenance are rechecked. Ordinary `np.load(..., allow_pickle=False)` creates one writable J allocation independent of the source file; NumPy may expose it as a reshape view of its own allocated base. The loader verifies that ownership chain and forbids memmaps. It returns this array directly, avoiding a second full J copy. The cache then clears its density/proof references, records `saved_J_hits=1`, and leaves native `_rij_calls=0`. All later requests delegate to the unchanged MemoryRI method; its actual native counters, metric construction, guards and errors remain intact.

A minimal NPY branch is covered by synthetic tests for future parent use: it requires an accepted first-J result whose `J_sha256` equals the artifact digest and a caller-bound exact cycle-zero density digest. The caller must independently bind that digest to the pinned original cycle-zero density, inputs and runtime. This small runner never selects the NPY branch; a future parent consumer still needs its own reviewed driver and memory protocol.

The pinned pure-PBE RKS implementation adds initial J into its exchange-correlation buffer and retains J as `vhf.vj`. Later incremental requests add prior `vhf.vj` into a newly returned J. Writable independent ownership therefore matters. Clearing the cache removes its extra reference; the caller/kernel and `vhf.vj` can still retain density/J. Mapping is not free resident storage, and no parent memory-margin claim is made here.

## Operator child and stage-aware storage

Use unchanged PBE/grid2/def2-svp Mo ECP, C-PCM water eps78.4, Lebedev17, scale1.2, probe0, AO block1, direct_scf_tol1e-13 and the same MemoryRI/PCM implementations. The cached object has no preliminary J request. Its first effective potential must have exactly one saved hit, native calls zero, PCM factor present and RI metric absent.

Compare cached and uncached initial gas-phase effective-potential matrices, tagged solvent potential/energy, Coulomb energy and exchange-correlation energy separately at 1e-10. The solvent wrapper intentionally keeps solvent outside the numeric gas-phase matrix, so matrix equality alone is insufficient.

Then evaluate the saved perturbation through native incremental RKS using dm_last/vhf_last. Require the cached object's first native request to be the exact density difference, with PCM present and RI absent before the request; its fallback builds RI while PCM remains resident. Compare the same five effective-potential/energy quantities at 1e-10, then make a zero-increment request to test factor reuse. Save initial/perturbed/delta densities and all cached/uncached matrix/solvent/scalar comparison data for independent recomputation.

At every effective-potential stage and SCF callback, validate PCM and RI independently whenever present: actual shape against surface-point/auxiliary-AO count, finite factor, immutable Fortran layout, factor reuse after construction, no retained S/ERI/three-index tensor. Record actual in-place aliasing when each factor is created. No fixed RI-before-PCM order is assumed.

## SCF child and unchanged thresholds

Use a fresh handoff; feed the same immutable initial density directly into kernel(dm0=...), with no regenerated guess and no preliminary effective-potential request that would consume the SCF handoff. Verify cached-first/PCM-before-RI ordering and later native fallback from actual request/stage records. Compare against the existing successful uncached small SCF: energy error <=1e-8 Eh; density max error <=1e-5; memory full-Fock gradient <=1e-5; direct full-Fock gradient <=1e-3; electron trace error <=1e-8; convergence required. Save density, MO coefficients/occupations, full memory/direct Fock matrices, overlap and initial density for independent audit.

A pass is `PASS_RETROSPECTIVE_SAVED_J_HANDOFF`. It establishes only the scoped small-case handoff and storage-order agreement. This is not a fresh holdout, parent SCF execution/readiness, whole-SCF performance, physical admission or chemistry validation. Parent metric reconstruction while PCM is resident remains a separate resource question.
