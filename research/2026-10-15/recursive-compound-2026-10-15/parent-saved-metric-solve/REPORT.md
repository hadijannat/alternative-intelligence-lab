# Controlled saved-metric replay completed; coefficient sensitivity remains

The single approved replay completed in66.03815049992409seconds. Child83941 returned0, is absent, and triggered neither supervisor limit nor monitor error. Sampled maximum RSS was6,496,583,680bytes, below the10GiB sampled guard; this is not a certified peak bound. Root and the independent reviewer verified all37 saved artifact hashes. The original SIGBUS attempt and all earlier numerical failures remain preserved.

The full prelaunch gate matched384 grouped file pins, including the original3,077,044,480-byte metric and the exact qualified runtime. The new child used a readonly mapping, one writable Fortran factor copy, four explicit solves and a DPOCON estimate. Configured OpenBLAS/PySCF getters were1/4 around operations and4/4 initially and after restoration. These receipts do not measure executing worker-team sizes. The process ended without using its altered explicit-control mode for subsequent work.

## What the experiment establishes

The two solves with the identical saved A right-hand side produced bitwise identical coefficient arrays. This is one successful repeated pair in one execution. B and C each ran once; general determinism is unproven. The experiment reused previously examined inputs and is not held-out validation.

| Saved contrast against A1 | Maximum RHS difference | Maximum coefficient difference | Relative RHS change | Relative coefficient change |
|---|---:|---:|---:|---:|
| A2 |0|0|0|0|
| B |1.000444171950221e-11|2.0332596854455431e-4|2.353419153170805e-15|1.9856152879395542e-5|
| C |2.4556356947869062e-11|9.639826773497617e-4|5.776574285055613e-15|9.413941343331941e-5|

Relative changes use infinity norms divided by their respective A baselines:4251.0241773221915 for RHS and10.239947777373475 for coefficients. They describe strong sensitivity of this coefficient representation, not a measured Coulomb-field error or a condition-number certificate.

DPOCON reported reciprocal one-norm condition estimate4.004423558640322e-14, corresponding to2.4972383299521492e13, with info0. It is an estimate, not a certified bound. The saved normwise backward diagnostics range6.58897e-17 to1.12012e-16; componentwise maxima range4.98249e-15 to1.20353e-14. These are floating-point diagnostics whose computation itself rounds.

The new factor content hash261d6cbcbe2d0ee2b42f3dfb064570df01ca831676e968591518f6083c242c0e differs from historical15f8e083a4b323de758bf30b03438e1c0da0d80604b577208cc708b6c2f1a31c. The factor was not serialized, so elementwise reconstruction of that difference is unavailable. The original metric digest was unchanged during this replay. Different factor realizations and execution settings prevent exclusive attribution to an earlier solve; success here does not establish the cause of the previous SIGBUS.

## Independent residual check

The independent reviewer reproduced the saved vector comparisons and checked selected matrix rows. A compensated sum of rounded products changed some residual signs and magnitudes. Exact rational arithmetic over the stored binary64 inputs then gave:

| Arm and zero-based row | Saved floating residual | Exact stored-input residual, rounded decimal |
|---|---:|---:|
| A1,7405 |-2.955857780762017e-11|1.092375420880339e-12|
| B,7915 |4.638422979041934e-11|1.5706655883156099e-12|
| C,10 |2.7284841053187847e-11|3.59400365547532e-13|

The exact rational numerators/denominators and compensated comparisons are preserved in [the independent review](INDEPENDENT_REVIEW.md). Only these three rows received exact arithmetic. Neither the full residual norm, underlying molecular integrals nor forward coefficient error is thereby certified. Small residuals and a successful factorization coexist with a highly sensitive representation.

## Consequence for the chemistry calculation

For a positive-definite Coulomb metric M and coefficient difference d, the physically relevant model quantity is d^T M d, rather than the unweighted coefficient maximum alone. For an exact unscreened auxiliary coupling vector g, Cauchy-Schwarz gives |g^T d| <= sqrt(g^T M^-1 g) sqrt(d^T M d). These are conditional mathematical relations, not evaluated target-error bounds. The current screened native contraction introduces additional dependencies, and cancellation-sensitive arithmetic cannot certify these quantities from rounded residuals alone.

The evidence supports testing the explicit runtime controls in the full ordinary J operator before choosing ridge regularization, auxiliary-basis truncation or a changed screening threshold. The next proposed diagnostic uses two ordinary +P0 calls, saves both full matrices and solve intermediates, and retains the original absolute1e-10/relative0 criteria. Its [separate preparation](../parent-explicit-blas-j/PROTOCOL.md) now has six passing mock tests and 429 grouped pins, with no independent launch approval or native run. This completed replay authorizes no additional run. Any later approximation change needs independent accuracy qualification, fixed direct-reference/solvent-aware criteria and an untouched numerical case. No historical failure is waived by a small scalar energy contraction.

No J, SCF, PCM, geometry optimization or new integral calculation ran here. Parent SCF readiness, exact Mo34WV identity, shared-medium chemistry, seed dependence and functional inheritance remain unverified. Aggregate24 assessed roles,0 verified integrated complements; all twelve full-goal requirements remain unmet.

The frozen protocol's universal streaming-hash sentence is too broad: the large metric and new outputs use streaming hashes, while some inherited small/runtime helpers retain buffered hashing. The bound approval and independent prelaunch review record this qualification. Frozen source/protocol/preparation files were not rewritten after outcomes.
