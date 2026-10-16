# Metric saved; native factorization failed

The one approved attempt is terminal and incomplete. Worker73957 exited with signal10 after6.843436292 seconds; the launcher returned1. The supervisor recorded neither a timeout nor a sampled-memory-limit termination. Sampled maximum RSS was6,213,337,088bytes; this is not a certified peak or whole-process-tree bound. The process is absent. No automatic retry occurred.

The metadata repair passed the original full parent/auxiliary checks and produced `run-v1/original_metric.npy`. The exact OS report for this PID identifies EXC_BAD_ACCESS/SIGBUS, KERN_PROTECTION_FAILURE, in OpenBLAS Cholesky factorization. Its native stack includes the matrix-packing routine, parallel symmetric rank update and `dpotrf_L_parallel`, followed by SciPy's Cholesky wrapper. The fault address maps to an executable region belonging to an h5py extension; this does not identify h5py as the cause. An invalid native write is observed; its underlying cause remains unresolved.

`matrix-factor.json` and all answer/residual/condition results are absent. The factorization was entered and did not return successfully. There is no completed factor, solve, condition estimate, J call, SCF or PCM build from this attempt. The original v1 metadata failure and all previous J failures remain preserved.

## Saved-matrix postmortem

The [inspection script](postmortem/inspect_saved_metric.py) reads the existing array in bounded row blocks and preserves the matching OS crash report. It performs no factorization, solve or new integral calculation. Three tiny integrity/math checks pass; all seven original terminal artifact hashes match the launch receipt.

| Observation | Result |
|---|---|
| File SHA256 | `00a6c22b1bbf0d90ae9d4905b4dd4fa9edc864bb27c2af9a93ca2ce1b40aa3af` |
| File bytes | 3,077,044,480 |
| Shape and storage | 19612 by19612, float64, Fortran contiguous |
| Finiteness | All entries finite |
| Maximum symmetry discrepancy | 0 |
| Infinity norm | 40024.485520835566 |
| Diagonal range | 0.2101484812890207 to214.0643709742175 |

These observations establish readable saved bytes and elementary matrix properties. Positive diagonal entries and symmetry do not prove positive definiteness, conditioning, accuracy or suitability for the proposed compound. No numerical success replaces the failed factorization. [Machine-readable record](postmortem/result.json).

## Thread-control assumption requiring correction

A fresh root query using the same qualified interpreter and requested environment reported OpenBLAS0.3.34 `USE_OPENMP`, `openblas_get_parallel()=2`, `openblas_get_num_threads()=4`, and PySCF thread count4. Thus setting `OPENBLAS_NUM_THREADS=1` alongside `OMP_NUM_THREADS=4` did not establish actual single-threaded BLAS in that probe. The earlier `OMP4/BLAS1` wording records requested environment variables; actual BLAS1 operation was not verified. The parallel crash stack makes this a relevant control gap, but the fresh query alone does not establish the exact worker count at the fault or prove the crash cause.

The optional threadpoolctl query failed because that package is absent; no dependency was installed and the frozen environment was unchanged. A separately bounded small probe is evaluating the library's explicit thread controls. Any saved-metric replay requires new frozen inputs, measured controls and independent review. No fresh parent launch is authorized by this failed attempt.

Scope remains a numerical prerequisite on the Mo36 surrogate. No target identity, joint chemistry, functional inheritance, complement admission or intelligent behavior is demonstrated.
