# OpenBLAS runtime control: tiny native qualification

2026-10-16. Status: PASS_TINY_CONTROL_PROBE_ONLY. No compound, chemical function, large metric factorization, J, SCF, or PCM calculation is qualified by this result.

The qualified environment loads OpenBLAS 0.3.34, `NO_AFFINITY USE_OPENMP VORTEX MAX_THREADS=128`, with `openblas_get_parallel()==2`. Under the existing requested environment (`OMP_NUM_THREADS=4`, `OMP_DYNAMIC=FALSE`, `OPENBLAS_NUM_THREADS=1`, and MKL/VECLIB/NUMEXPR counts 1), its reported runtime count is **4**, not 1. These getters report configured thread counts; a 4-by-4 kernel does not establish the number of workers actually executing a large parallel factorization.

| Scenario | BLAS getter | PySCF getter |
|---|---:|---:|
| Initial / baseline solve | 4 | 4 |
| PySCF `with_omp_threads(1)` before explicit BLAS setter | 4 | 1 |
| Direct `openblas_set_num_threads(1)` | 1 | 4 |
| PySCF context after explicit BLAS setter | 1 | 1 |
| PySCF context exit | 1 | 4 |
| Explicit setter restoration after intentional exception | 4 | 4 |

Each solve's before/after counts agree. Five non-diagonal SPD Cholesky factorizations and solves produced bitwise identical answers `[1,-2,3,-0.5]`, exact zero residual, and exact zero solution error. The preregistered code tolerance was `100*float64_epsilon*max(1,max(abs(rhs))) = 2.914335439641036e-13`; it is a tiny-example acceptance threshold, not a parent-metric accuracy target. The matrix is constructed as `L L^T` with positive diagonal 2 in nonsingular triangular L. `verify.py` independently checks the stored matrix, solutions, and RHS using exact Fraction arithmetic. SciPy used writable Fortran storage in-place for the lower Cholesky factor. This is a small API and restoration check, not evidence of stability for dimension 19,612.

`observed.json` records the loaded images and available binary hashes. Dynamic lookup of `dpotrf_` through the SciPy `_flapack` extension, `liblapack.3.dylib`, and the selected `libopenblas.0.dylib` returned the same address. The OpenBLAS binary SHA256 is `7a89772da7fb86aea4c91eefdbc4e6980fb1f668d77bbc34537503a5d1f29c07`. macOS Accelerate image names are also present in the loaded-image list; no claim is made that every NumPy operation uses this OpenBLAS. Three system image paths have no ordinary disk file and are listed explicitly rather than assigned invented hashes.

## Invocation and resource evidence

From workspace root:

```sh
recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-blas-control-audit/probe.py
recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-blas-control-audit/verify.py
```

The successful fresh child PID 75828 exited 0 in 0.4089422500692308 seconds. Seven `ps` RSS samples observed a maximum 88,178,688 bytes, below the 1 GiB sampled limit; the wall limit was 30 seconds. Neither limit fired. This supervisor samples RSS rather than enforcing a hard allocation cap; a between-sample transient could be missed. The child executes only five 4-by-4 solves. The launcher refuses to overwrite existing output; a deliberate new run needs a separately preserved attempt. No package installation, environment-file change, or parent scientific input mutation occurred.

## Preserved failed observations

- Root's earlier `threadpoolctl` probe (tool chunk `d6580e`, exit 1, reported elapsed 0.391180792 s) failed with `ModuleNotFoundError: No module named 'threadpoolctl'`. This is root-reported tool evidence. The successful child independently reproduced the missing import and records it in `observed.json`; no dependency was installed.
- `failed-v1/` retains the first probe source, supervisor and stderr. It stopped before thread controls or solves when hashing a loaded macOS shared-cache image path that has no ordinary disk file. Exit 1, 0.36795737501233816 s, sampled RSS 90,750,976 bytes. The correction records such paths separately.
- `failed-v2/` retains the next source and outputs. `otool -L` failed with exit 69 because Xcode's license is not accepted. No thread-control or solve work was reached. Child exit 1, 0.6429179169936106 s, sampled RSS 92,585,984 bytes. No license was accepted; direct dynamic symbol lookup replaced that unavailable inspection path.

The failed supervisors' `scope` describes the planned run, not completed solves. Their original artifacts and hashes remain intact. The successful supervisor and `verification.json` identify the observed successful scenario and preserve both failures.

## Primary-source contract and limits

The [OpenBLAS v0.3.34 header](https://github.com/OpenMathLib/OpenBLAS/blob/v0.3.34/cblas.h) declares the exact ctypes signatures used: the setter takes an `int` and returns `void`; the count/parallel queries return `int`; config returns `char*`. Local symbol resolution succeeded for all these functions. The [official README](https://github.com/OpenMathLib/OpenBLAS/blob/v0.3.34/README.md) states that OpenMP builds use `OMP_NUM_THREADS` and ignore `OPENBLAS_NUM_THREADS` for this initialization choice. This explains why requested environment values alone cannot support the label “BLAS1.”

The [v0.3.34 OpenMP implementation](https://github.com/OpenMathLib/OpenBLAS/blob/v0.3.34/driver/others/blas_server_omp.c) sets an explicit-control flag when the public BLAS setter is called. It updates BLAS state without calling `omp_set_num_threads` in that setter. Restoring the reported count to 4 does **not** establish restoration of the previous implicit/adaptive mode: that flag remains set. Therefore a future comparison must use fresh children and record the control history, not infer full runtime-state restoration from equal getters. Downloaded primary-source snapshots are in `sources/`, with hashes in `verification.json`; they document the matching release API, not an assertion that the packaged binary is a byte-for-byte build of those sources.

Next proposed diagnostic: independently freeze and review a new saved-metric factor/solve experiment using the already preserved original matrix, direct BLAS setter 1, getters immediately surrounding the factor/solve, and fresh-child isolation. Preserve the original matrix, frozen RHS vectors, previous SIGBUS, and all original accuracy gates. No large run was launched here. A successful serial factorization would be evidence about that execution condition only; it would not by itself prove that BLAS threading caused the earlier crash or that target chemistry exists.
