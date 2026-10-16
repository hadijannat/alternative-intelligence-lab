# Parent J repeatability: completed with numerical nonpass

This is one separately frozen diagnostic, launched once by root in exec session57609 after independent exact-preparation approval. The final preparation SHA256 is5746a8e8fbecfb9084070dad998f3edb03d0135e19c5e6a07171d59379d52dde. Root and the independent reviewer each ran all11 synthetic tests successfully. All256 grouped pins (252 unique paths), including eight preserved pre-amendment files, matched before launch.

Session 57609 terminated with exit 0 and worker PID 37763 is absent. The authoritative status is COMPLETED_WITH_NUMERICAL_NONPASS: all three requests completed, while the fixed numerical criteria failed. One factor, three metric calls and zero SCFs were recorded. Wall time was 696.6868703749496 seconds, sampled maximum RSS 3,655,090,176 bytes, with no supervisor termination or monitor error. Sampled RSS is not a guaranteed peak-memory bound. No retry occurred.

The unchanged protocol executed +P0,+P0,-P0 using one object/factor within 1000 seconds and 10 GiB sampled RSS, with no SCF or PCM build. All three returned matrices were saved before acceptance decisions. Numerical nonpass did not suppress the remaining planned finite/invariant-safe calls. The launcher records 24 artifact hashes, no missing artifacts and no invariant errors. Root verified those hashes and all frozen preparation pins. All three matrices are finite and exactly symmetric.

The absolute tolerance remains 1e-10, with relative tolerance zero. Root independently recomputed the following from read-only saved arrays in 64-row blocks, reproducing every maximum, first row-major argmax, operand value, operand maximum and exceedance count in the driver's 16-row report.

| Comparison | Maximum absolute discrepancy | Entries above threshold | Result |
|---|---:|---:|---|
| J2-J1 | 4.844054046770907e-10 | 284 | NONPASS |
| J3+J1 | 4.420286359163583e-10 | 231 | NONPASS |
| J3+J2 | 4.142748366575688e-10 | 31 | NONPASS |
| J1-Jold | 4.718572199635673e-10 | 304 | NONPASS |
| J2-Jold | 9.484324436925817e-11 | 0 | PASS |
| J3+Jold | 3.2159164220502134e-10 | 14 | NONPASS |

The same-sign discrepancy means this run does not support attributing the problem exclusively to density-sign reversal. Its cause remains unresolved. Two positive requests supply one contrast, not a variance estimate; negative sign is confounded with third-call order. Jold is a preserved run of the same implementation, not an independent algorithmic oracle. This diagnostic does not reproduce the failed SCF density or preceding PCM allocation history. Neither target chemistry, parent SCF readiness nor the earlier SIGTRAP cause is established. All earlier failures remain unchanged.

The three .npy arrays are retained. The publication exporter omits tiny post-call .bin close markers under its existing binary policy; structured stage and artifact-hash receipts preserve the recorded closes. Original marker bytes, excluded runtime and other original inputs are still required for exact historical provenance replay. This is a reproduction limit, not an unrecorded native result.

[Independent terminal review](INDEPENDENT_REVIEW.md) separately reproduced all six comparisons in seven-row blocks, reconstructed the signed input digests, verified the artifact hashes and frozen gate, and confirmed the worker's absence. The factor itself was not saved; its equal hashes are runtime observations rather than independently rehashed factor bytes. Review approves preserving the evidence and negative classification, without granting scientific admission.

Prelaunch review identified a fingerprint-order defect before any native attempt. The exact affected sources and preparation remain under preparation-history/. The corrected baseline follows the existing core-Hamiltonian initialization, and the mocked setup regression accepts that initialization while rejecting later mutation. Final review is recorded at workspace .omo/evidence/parent-j-repeatability-prelaunch-review.md; root approval binds that review and the final preparation.
