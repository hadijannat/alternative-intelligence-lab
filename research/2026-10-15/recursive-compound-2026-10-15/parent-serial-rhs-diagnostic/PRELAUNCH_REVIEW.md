# Independent serial RHS native prelaunch review

Date: 2026-10-16. Scope: the frozen one-child RHS-prefix diagnostic, not publication readiness or scientific qualification.

- codeQualityStatus: CLEAR
- recommendation: APPROVE for the specified bounded native diagnostic, subject to separate root approval and full remaining pin verification
- blockers: []
- Preparation SHA256: `0da90217f8074035deb9902173fb9bd3aa53d7679be4e56c0ec4736eded2f92b`
- Bounds: one fresh child, at most two prefix attempts/pass-1 contractions/sentinel captures, one factorization, zero solves/completed J/SCF/PCM;1800 seconds,10GiB sampled RSS; no retry.

## Independent checks

Read the complete new driver/tests/protocol, preparation receipt, inherited explicit-J setup, stage-localization interception, repeatability storage guard, MemoryRI and installed PySCF df_jk.get_j, scf.jk.get_jk, _VHFOpt.prescreen and lib.with_omp_threads implementation. The prior review of the supervisor and explicit BLAS controller remains applicable because their hashes are unchanged. Source/publication review is not treated as launch approval.

Independently hashed473 of474 grouped pins, all match. Only original_metric.npy (3,077,044,480 bytes) was left for root's full pin verification. New source hashes:

- run.py: `4fd5d46ef41585deedcace63feef663f303b555ca94fc8fbf124af01ea24585c`
- test_run.py: `214f373ea253b122ba8aef2c169ad6b7cd031e7e0d72cd1ff47d060c60f997d0`
- PROTOCOL.md: `1f3e925d89c9426a9a820f4eb3570fa6ddf5729c2f985b31dd28ae66b74af17c`
- qualification.json: `afa05513c55b70714e415a50603541f9c2d80c98c18bfc9261bc67be67ae1e47`

At inspection, approval and run-v1 were absent. Ran the qualified interpreter with `-B parent-serial-rhs-diagnostic/test_run.py`, without --record: seven tests passed, exit0,0.018 seconds. No native molecular operator was executed. Tests exercise restoration on native error, exact sentinel handling, duplicate/pass2 rejection, save-before-classification, bitwise signed-zero distinction and tampered approval/pins. They are behavioral tests, not deletion-only, tautological or prose-pinning tests.

## Installed API and control-flow audit

Installed `pyscf/df/df_jk.py:415-503` imports scf.jk within get_j, so replacing that module's get_jk is visible to the private MemoryRI clone. Native pass1 at474 uses exactly scripts=['ijkl,ji->kl'] for one density, intor='int3c2e', aosym='s2ij', hermi=0, the declared eight-entry shell slice and the same optimizer. Its temporary prescreen is CVHFnr3c2e_vj_pass1_prescreen. `_VHFOpt.prescreen` returns the integer-valued ctypes pointer field; comparing with `_fpointer(...).value` is appropriate. Native jk.get_jk accepts the intercepted positional/keyword signature and dispatches direct_bindm.

Installed `pyscf/lib/misc.py:210-241` with_omp_threads stores the prior getter, sets1 on entry, restores it in __exit__, and does not suppress exceptions. The diagnostic additionally requires4 before/after and1 inside. Its outer finally restores jk.get_jk even on errors. Inherited explicit-BLAS controller snapshots cover setup and the prefix boundaries; these are configured limits, not measured team sizes. The source gives no basis for claiming observed native thread-team cardinality.

Native first pass exits its temporary prescreen context before reshaping jaux and calling private cho_solve at482. RHSCapture copies the19612x1 RHS and raises a unique BaseException instance without invoking the supplied solver. The installed Cholesky try/except only covers factor creation and catches LinAlgError, so it does not swallow that sentinel. The outer attempt catches only PrefixStop and accepts only capture.stop by identity. Different sentinels/errors propagate. Solver/pass2 cannot be reached after the accepted stop; a hypothetical second contraction is additionally rejected by count/script/keyword checks.

The MemoryRI completion callback and _rij_calls increment occur only after native get_j returns, so both remain zero for accepted prefixes. `storage(0)` is therefore correct: it expects zero metric-completion receipts while still enforcing one real factor and its immutable content/pointer/shape. Explicit prefix and sentinel counters are independent from completed-J counters. Second attempt retains the initialized optimizer and factor; q_cond/molecule/fakemol fingerprints and factor hashes are checked. No dummy factor or substituted rho is introduced.

The inherited e.setup interception is correctly composed: temporarily setting e.OrdinaryCapture supplies RHSCapture to stage setup, while e.write routes the original-metric receipt into the new directory. Inherited deferred receipts are flushed after capture. Source objects/writers restore in finally. The previous outcomes are read/pinned, not overwritten.

## Small native API qualification decision

An additional small native integration smoke test would improve empirical confidence, but it is NOT a prerequisite blocker for this narrowly bounded exploratory prefix run. Reason: the novel interception's exact signature, module lookup, pointer type, thread-context restoration, sentinel propagation and zero-completion counter behavior are directly supported by the installed source, while mocks exercise the failure paths. There is no discovered API mismatch needing native disambiguation, and this parent run is itself a diagnostic rather than an accuracy qualification. Guards reject unexpected dispatch and prevent solve/pass2; a failure remains incomplete, not a scientific pass. A small comparison cannot establish parent-scale bitwise repeatability or safety in any case.

This decision does not claim native qualification already happened. If root elects to require the extra smoke test, freeze and independently authorize it separately: use a reused small case (no held-out input), the same explicit controller, actual first-pass dispatch/sentinel and restoration checks, with independent caps and preserved artifacts. Do not silently add that run to the frozen one-child parent budget or reinterpret publication review as authorization.

## Evidence and resource semantics

Two RHS arrays are saved/closed/hashed before classification. Finite float64 shape is enforced; byte equality is stricter than numeric equality and correctly rejects signed-zero differences. Differences against both prior OMP4 vectors remain descriptive. Original full-J1e-10/rtol0 is UNTESTED; no new full J is produced. Equality of a newly constructed metric with a saved digest is consistency evidence only. Original explicit-J failures remain pinned and unaltered.

Launch requires preparation/qualification-bound independent approval; worker independently checks the launch token. Exclusive run-v1 and exclusive JSON/array writes prevent reuse. The existing supervisor receives1800s and10*2**30 bytes, sets the original thread environment, starts one owned process group, and fails closed on resource-monitor failure. This is a sampled RSS guard with termination grace, not a hard memory or exact wall-time ceiling. New pass1 timings are emitted at entry/return; inherited deferred factor timestamps are not native timing measurements.

## Findings and perspectives

CRITICAL: none. HIGH: none. MEDIUM: none.

LOW: untyped script/test style remains inconsistent with the programming skill's preferred strict typing/pytest conventions, as in inherited code. No demonstrated bounded-run defect follows. The deliberately broad top-level BaseException handler writes a traceback and re-raises; it is justified by the unique BaseException sentinel and does not silently convert failures into success. Final-gate exceptions now retain their traceback, improving the earlier transparency limitation.

Programming and remove-ai-slops skills were loaded in this reviewer session and applied to code/tests. Boundary validation and temporary wrappers are necessary to distinguish pass1 from prohibited native work; no unnecessary normalization, speculative abstraction or useless tests were found. No lint/typecheck or native-smoke result is claimed. Only this report was written. The large metric rehash remains assigned to root, and no approval/native launch was created. Parent execution behavior, bitwise RHS outcome, full-J repeatability, physical identity, retention, inheritance and scientific admission remain unverified; zero admissions.
