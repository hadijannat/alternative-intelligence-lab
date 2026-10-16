# Serial native RHS prefix: completed bounded diagnostic

The single approved run is terminal **COMPLETED_SERIAL_RHS_PREFIX_DIAGNOSTIC_ONLY**. It completed two positive-P0 native pass-1 contractions, caught two exact stop sentinels before any solve and used one real factorization. There were zero solves, completed Coulomb J calls, SCFs or PCM builds.

The saved `b_A.npy` and `b_B.npy` arrays are finite float64 of shape (19612, 1) and bitwise identical: maximum absolute difference 0, RMS difference 0 and zero unequal entries. Both file SHA256 values are `aa5ed22825b38ee7f5dcd9c5b30b966b530117df5901cc356315a7e71b3e4260`. This passes the frozen serial RHS repeat criterion only. See [result.json](run-v1/result.json) and [comparisons.json](run-v1/comparisons.json).

Each serial vector differs from the earlier explicit-BLAS1/PySCF4 RHS A by maximum 8.958522812463343e-11 and from RHS B by 8.913048077374697e-11. These descriptive comparisons have no chemical acceptance threshold and do not establish exclusive causality. Configured thread getters describe configuration, not measured executing worker teams. Only the native pass-1 contraction was scoped to one OpenMP thread; setup and factorization retained the frozen explicit BLAS1/PySCF4 configuration.

## Execution and review

The [launch receipt](run-v1/launch-result.json) records exit 0, wall time 893.8663067501038 seconds and sampled maximum RSS 3,627,646,976 bytes, within the 1800-second and 10-GiB guards. No limit termination or monitor error occurred. Sampled RSS does not certify unsampled peaks. The [frozen protocol](PROTOCOL.md), preparation and [prelaunch approval](independent-root-review.json) remain unchanged; their preparation-state wording is historical.

The recorded invocation was:

```sh
OMP_NUM_THREADS=4 OMP_DYNAMIC=FALSE OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python -B recursive-compound-2026-10-15/parent-serial-rhs-diagnostic/run.py --launch
```

The [independent terminal review](INDEPENDENT_REVIEW.md) is CLEAR and approves publication of this scoped result. It verified all 30 output hashes, independently recomputed RHS equality and historical comparisons, reconciled the supervisor receipt and confirmed the child absent. It rechecked 473 of 474 grouped preparation pins, leaving the large saved-metric rehash to root. New metric/factor arrays were not retained for elementwise reconstruction, and configured getters do not measure native teams. The separate [prelaunch review](PRELAUNCH_REVIEW.md) remains preserved. No rerun is part of this publication checkpoint.

## Consequence and remaining dependencies

The original full-J absolute 1e-10/relative-zero criterion was **not tested**. Its earlier failure remains maximum 6.702407517877873e-10 with 630 entries above the limit. No tolerance was relaxed, and prefix equality establishes no repaired J operator, crash cause, parent SCF readiness, chemical accuracy or physical admission. The prospective accuracy qualification remains gated off and the reserved holdout unused.

The registered [parent H-only relaxation and orbital-stability comparison](../identity/next-step/REPORT.md) also requires qualified derivatives and response. The current [ground-state wrapper](../cpcm-blocked/blocked_pcm.py) explicitly rejects gradients, Hessians and stability/response operations. Numerical prefix repeatability cannot execute that chemical comparison; no replacement physics is implemented here.

The aggregate remains 24 assessed roles, zero verified integrated complements and all twelve requirements I/E/T/B/R/H/V/S/M/A/J/C unmet. The separate tantalum/alumina and vanadate NMR dossiers remain reviewed source constraints only, with no target experiment or held-out validation.
