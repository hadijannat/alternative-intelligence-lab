# Factor-only memory mechanics: tiny tests only

A local specialization is feasible without mutating installed PySCF or SciPy globals. Eight tiny tests pass. This is not SCF qualification, parent performance evidence or physical admission. The concurrently running JKFIT campaign and all historical files were left unchanged.

`memory.py` clones the native `df_jk.get_j` function with a private globals dictionary containing a private SciPy linalg facade. The function's native two-pass contractions remain unchanged. The facade requires a writable Fortran float64 metric, checks finite values in bounded slices, requests in-place Cholesky and verifies actual aliasing before publishing a read-only factor. A destructive Cholesky failure becomes `FactorizationAborted`, which is not a LinAlgError and therefore bypasses the native regular-solve fallback. The private regular solver rejects calls. The qualified JKFIT adapter is cloned with this private backend, retaining its density/method/storage/geometry guards and per-call receipts; the entry point initializes ECP routing through get_hcore before installing its molecular fingerprint.

`MemoryPCM` changes only construction/storage and the local solve binding: Fortran surface S, in-place Cholesky, factor-only intermediates, fixed AO block1. It reuses the inherited contractions, ground-state guards and cache reset. It no longer supplies a stored S matrix to consumers, so callers expecting `_intermediates['S']` must not use this implementation. The existing qualified solver remains untouched.

Finite checks scan at most65536 float64 elements per temporary Boolean array. Factors are read-only and validated in bounded slices on each solve; RHS and output are also checked. This avoids the full-square Boolean temporary of SciPy's default finite check. Read-only NumPy flags are an internal programming contract, not protection against malicious external mutation; no security claim is made.

## Observed evidence

- Synthetic16x16 SPD factor reused the input pointer and was read-only; solve residual2.84217e-14.
- Real He/sto-3g JKFIT metric was23x23, Fortran-contiguous and factorized at the same pointer. Private versus native J maximum difference2.22045e-16; repeated calls reused the factor. Original installed callable identities were unchanged.
- The bounded finite-check test now uses a literal65536 ceiling and a131075-element input independent of the implementation constant. It observed chunks65536,65536,3 and rejected a nonfinite last element after scanning all three chunks. An explicit mutation to CHUNK=65537 failed the test as expected (retained in evidence/chunk-mutation-control.txt). Layout, nonfinite RHS and writable-factor controls rejected as expected.
- An injected failure deliberately modified the metric before raising LinAlgError. The local facade raised FactorizationAborted; the regular solve was called zero times and the DF optimizer remained unpublished.
- Six-point He C-PCM retained no S, used AO block1 and matched the old solver: energy difference0, AO-potential difference5.55112e-17, reconstructed-S error1.11022e-16. Reset cleared the factor.
- The guarded private RI adapter produced one cached-Cholesky metric receipt and rejected a changed functional.

No test invoked SCF; a sentinel on SCF.kernel would raise if invoked. No parent-shaped matrix was allocated. The largest factor was the actual23x23 atomic metric. Raw tests, observations and source hashes are retained.

## Allocation arithmetic only

Installed def2-universal-jkfit shell data imply spherical auxiliary counts Mo255/O77/H18, or19612 functions for36Mo/128O/32H. This count was computed from atomic basis data without building the parent molecule or metric. One parent-sized metric factor would occupy3,077,044,352bytes. For9284surface points and3068AOs, one surface factor is689,541,248bytes and AO block1 is75,300,992bytes.

`allocation.json` preserves the required4GiB scratch allowance and32denseAO buffer allowance, plus eight row-block temporaries, one bounded Boolean chunk and one nuclear block. Total10,622,806,400bytes (9.893259406GiB) leaves only114,611,840bytes below10GiB. Passing this arithmetic screen is not a memory certification or launch authorization. Native Q-condition arrays, integral-engine/DFT/BLAS scratch and allocator transients are not independently bounded. Real parent aliasing, numerical conditioning, memory peaks and throughput remain untested.

## Reproduction and next gate

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 ./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/cpcm-rij-memory/test_memory.py
```

Scenario, invocation, observables and results are in `evidence/tests.txt`, `evidence/observations.json` and `evidence/verification.txt`; allocation arithmetic output is in `evidence/allocation.txt`. `source_pins.json` is checked at import. A separate bounded numerical comparison on retained densities against native J and the old PCM must precede any new SCF qualification. No parent launch is authorized here.
