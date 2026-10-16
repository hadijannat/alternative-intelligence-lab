# Requested thread settings versus observed library state

The new [bounded control probe](parent-blas-control-audit/REPORT.md) changes how earlier `OMP4/BLAS1` shorthand must be read. For the pinned OpenBLAS0.3.34 USE_OPENMP binary in `parent-openmp/env-aligned`, the same environment request reports four OpenBLAS threads and four PySCF threads. `OPENBLAS_NUM_THREADS=1` alone did not verify single-threaded BLAS. The matching release documentation explains that its OpenMP initialization uses OMP_NUM_THREADS.

This is a correction to the runtime-control claim, not a deletion or reclassification of saved numerical observations. Historical results, failures, hashes and sampled memory values remain as observed. A fresh probe cannot recover the exact active worker team of every historical call. The correction is scoped to this binary and configuration; it does not assign the same behavior to other environments or earlier builds.

The explicit OpenBLAS setter produced getter count1 while PySCF remained4 in the fresh tiny probe. A PySCF OpenMP context alone changed PySCF's reported count without reducing OpenBLAS's already initialized count. Returning both getters to4 does not restore the original implicit-control mode, because the setter leaves an explicit-control flag enabled. Comparisons therefore require fresh children and recorded control history.

The metric v2 SIGBUS stack contains parallel OpenBLAS Cholesky. That makes thread control relevant to the next diagnostic but does not prove it caused the invalid write. A separately prepared replay of the saved matrix will change this control deliberately, with no claim that its factor or results must match the original realization. Getter values document library configuration; tiny tests do not measure large-kernel worker teams or establish parent numerical stability.

No target chemistry, joint function, or complement admission follows from this correction. All original accuracy criteria remain unchanged.
