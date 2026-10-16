# Frozen serial native RHS prefix diagnostic

Two attempts A/B use the identical positive saved P0 and native MemoryRI prefix.
Common setup, integrals, optimizer and the single actual in-place factorization use
the previously tested explicit BLAS1/PySCF4 configuration. Only the native
`jk.get_jk` pass-1 contraction is scoped through `lib.with_omp_threads(1)`.
The process-local interception verifies scripts, integral, symmetry, shell slices,
fakemol identity, optimizer identity and the pass-1 prescreen function pointer.
Unexpected contractions, including pass 2, fail closed. OpenMP restores to four
before return, capture, storage and runtime guards; interception restores in finally.

At the private cho_solve entry, copy RHS then raise a unique BaseException instance
before calling any solver. Catch only that exact instance at the outer attempt
boundary. No dummy factor, rho replacement, pass 2, completed J, SCF or PCM build.
Both attempts share the real factor and optimizer. Completed MemoryRI call and
metric counters remain zero, while prefix/pass-1/sentinel counters each reach two.
Inherited geometry, ECP, basis, density, screening, q_cond, factor pointer/hash,
read-only/Fortran storage and runtime/source/binary/symbol checks remain active.
Metric hash equality with prior construction is consistency evidence only.

Save/close/hash b_A and b_B before classification. Require finite float64
(19612,1) arrays and byte-for-byte equality for the serial repeat criterion.
Report max/RMS/numerically unequal entry counts for B-A and each serial vector
against both saved explicit-BLAS1/PySCF4 RHS vectors. Comparisons are descriptive,
with no chemical error threshold. Signed-zero byte differences fail bitwise
equality even if numerical inequality count is zero. No exclusive causal claim.
The original J absolute 1e-10, rtol=0 criterion is unchanged and UNTESTED here.
No parent SCF readiness, held-out validation or physical complement admission.

One fresh child only, 1800 seconds, 10 GiB sampled RSS guard, no retry.
Pass-1 entry and return timings are emitted immediately at the contraction
boundary, distinct from inherited deferred factor receipt timestamps.
Preparation hashes sources/results/runtime and reads saved density only; it does
not construct molecular operators. Mock tests run without parent chemistry.
Root approval must bind preparation SHA and inherited qualification artifacts.
All outputs stay in this new directory. Prior frozen sources/results are untouched.

Commands (qualified interpreter):

    recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-serial-rhs-diagnostic/test_run.py --record
    recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-serial-rhs-diagnostic/run.py --prepare

Only after independent root approval, with OMP_NUM_THREADS=4,
OMP_DYNAMIC=FALSE, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1,
VECLIB_MAXIMUM_THREADS=1, NUMEXPR_NUM_THREADS=1, execute the same interpreter
and run.py with --launch. Preparation does not authorize launch.
