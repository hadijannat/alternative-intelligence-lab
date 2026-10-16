# Independent prelaunch review: J stage localization

codeQualityStatus: CLEAR
recommendation: APPROVE one bounded diagnostic for root launch consideration
blockers: []

No native work was launched. This review does not itself create executable approval or establish native qualification.

## Frozen evidence

- run.py: 7997719c2a4c12c1782695b30b6d707bb0fa5980c4640059038deb92f9d9e589
- test_run.py: 0d6f699b2f29ab6cfeedafcecaeb329d1104bc6baaed5caad1557718a4560501
- PROTOCOL.md: 85deb5593f724d04f22070ef9cca6f1819856d9f3b6be28b8ad817f6e7acdb23
- preparation.json: 077b972b1ea43bbf0472a7dcda5e3bbe89f964a583ee6ea2f34282c32b806c73

Fresh manifest equals preparation pins: 288 grouped entries, including 29 repeatability-outcome and 3 localization entries. run-v1 and independent-root-review.json were absent at inspection. Independently ran all eight synthetic tests under qualified env-aligned Python, OMP4/DYNAMIC FALSE and BLAS1: eight passed in 0.036 seconds. No molecule or chemical operator was created.

## Findings

CRITICAL: none.
HIGH: none.
MEDIUM: none requiring source changes for this bounded diagnostic.
LOW: malformed/truncated result.json, an unexpected supervisor exception or artifact hashing error can escape launch before launch-result.json is written. Standalone supervisor/raw files remain where already written, and no false success/retry follows. Do not promise a launcher receipt in every exceptional path.
LOW: deferred factor-stage timestamps are assigned when the buffered stage is flushed after the enclosing get_j, not when the original factor event occurred. They establish receipt ordering, not actual factor duration. Native logging remains independent. Avoid interpreting deferred timestamps as timings of internal stages.

## Boundary and invariants

Reviewed new driver, tests, protocol, preparation, reused repeatability setup/MemoryRI and installed PySCF get_j/_VHFOpt source. The native code completes optimizer initialization, auxiliary q_cond append, factorization, fake molecule construction and assignment to dfobj._vjopt before pass1 and cho_solve. Baseline optimizer state is therefore captured at a valid initialized point in the first solve hook. _VHFOpt.q_cond returns its actual retained ndarray; its shape, data pointer and content are fingerprinted. Cutoff and base/auxiliary/fake molecule arrays and metadata are included. dm_cond legitimately changes between passes and is not incorrectly frozen. The base fingerprint remains after ECP initialization in reused setup.

Factor identity/pointer/layout/read-only/content, call counters, requested density bytes, method/runtime and absence of ERI/three-index/PCM state remain checked by unchanged guards. The installed module globals are not patched. r.load/r.save are bindings in this separately loaded local helper module, used to buffer its Python receipts. Private SciPy solve facade is replaced only for the new local MemoryRI instance.

For A and B, SolveCapture invokes the original checked solve, copies RHS and ordinary result into independent small buffers, and returns the exact solver result object unchanged. Tests verify identity and absence of capture aliases. For C, ordinary b_C and rho_C are computed and retained before an independent exact copy of captured rho_A is returned to native pass2. Saved rho_ordinary_C is not overwritten by the substitution. C's resulting J is explicitly controlled output rather than ordinary J(P0).

Native pass2 recomputes its screening density from the substituted rho, as required by the unchanged source. This experiment changes both pass2 contraction input and its rho-derived screening values consistently; it is not an intervention on contraction arithmetic alone. Shared factors/library and call order remain potential confounders. The output flags correctly deny proof of stage causality and ordinary-J status for C.

## Storage, failure and workload

Exactly three planned calls A/B/C on fresh independently loaded positive P0, one optimizer/factor, one exclusive child/run directory, 1000-second wall and sampled10-GiB RSS guard, OMP4/BLAS1. Initial guesses, SCF, effective potential and PCM build remain forbidden. No oracle integrals or unrelated numerical work were added. Bounds are sampled/process supervision, not an OS allocation limit.

Six vector captures total941376bytes; C adds one temporary vector copy. Full J is saved and later deleted rather than retained for comparison. Factor and molecule fingerprints use shared-memory views. File hashing inherits whole-file read_bytes, so saving/hashing a J can transiently allocate approximately75MB; the vector/capture description must not be read as total process overhead.

No capture disk I/O occurs in the solve hook. Deferred factor/save/stage/metric records flush after the enclosing get_j returns and after its returned arrays are saved/closed/hashed. On a native exception before return, pending Python receipts and in-memory vectors may be unavailable; no saved result is claimed for that case. Native logging remains enabled as declared.

Each returned J and both captured vectors are exclusively saved before numerical classification and later count/density/storage guards. A returned-to-driver invariant failure therefore preserves arrays already written. An internal immutable-adapter rejection or native crash before return cannot guarantee output preservation. All three calls proceed through finite numerical/symmetry nonpass; invariant/nonfinite failures abort. Comparisons run only after all three calls and use original J threshold1e-10/rtol0. b/rho differences report exact equality, maximum and RMS without a newly invented pass threshold.

## Skill perspective and scope

Programming and remove-ai-slops perspectives were applied. Tests exercise ordinary-object identity, exact controlled substitution with ordinary-C preservation, setup deferral, mutation/layout rejection, bounded call count, and retained output before invariant failures. They do not assert prompt prose or merely restate a removal. No material skill-perspective violation was found within this review scope.

Eight mock tests are preparation evidence only. There has been no native trial of these hooks, optimizer fingerprints or controlled return layout. A completed diagnostic could constrain which stage varies; it cannot by itself establish allocator cause, parent SCF readiness, chemical validity or life/intelligence.
