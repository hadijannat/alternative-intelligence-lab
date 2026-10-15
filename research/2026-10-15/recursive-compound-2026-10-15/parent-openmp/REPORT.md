# Isolated OpenMP environment receipt

Runtime probe PASS; numerical qualification NOT RUN.

Official https://pyscf.org/user/install.html was read using web tool and supports dedicated conda-forge Apple Silicon environments. Direct urllib snapshot request returned HTTP403; no local HTML snapshot is claimed. conda-pyscf-metadata.json preserves live channel metadata. arm64 host has Homebrew libomp; xcrun compiler discovery fails on Xcode license prerequisite. No compiler, license or global environment was changed.

Install invocation: `python3 recursive-compound-2026-10-15/parent-openmp/guard.py solve`, followed by same script with `install`. Frozen explicit-spec.txt contains 59 package URLs and MD5s; solve.stdout records package SHA256 values. bootstrap.json pins micromamba download. All prefix/cache/temp directories are local. Install returncode0, elapsed23.408s, maximum sampled logical bytes1,071,310,972 (<2GB). Sampling is not a certified instantaneous peak. No source compilation.

Runtime invocation: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 recursive-compound-2026-10-15/parent-openmp/env/bin/python recursive-compound-2026-10-15/parent-openmp/probe.py`

Observed exit0. Assertions require lib.num_threads=1,4,1 in order. Existing runtime __kmpc_fork_call creates native teams of1,4,1 workers; each reports matching omp_get_num_threads and complete thread numbers. Four distinct thread identifiers are recorded in the four-worker case. Artifacts: probe-result.json and probe.stdout. Python callback bodies run with the GIL, so this demonstrates runtime worker creation, not throughput or chemical-integral speedup.

PySCF2.14.0 build py311h47f6db6_102; Python3.11.17; NumPy2.4.6; SciPy1.17.1; h5py3.16.0. Dependencies differ from old environment. source-binary-pins.json freezes PySCF Python/native sources, environment dylibs and conda package metadata. Recreate via explicit-spec.txt in isolated prefix; avoid moving installed prefix because package paths are relocated.

Scope limited to parent-openmp and .omo/evidence/parent-openmp. Prior environment and scientific results were not edited. Operators0, SCFs0. No equivalence, convergence, performance or chemistry claim. Root must run frozen small-case numerical qualification before parent diagnostics.
