# Fixed-geometry solvent response: component check passed

**PASS_RESPONSE_COMPONENT_ONLY.** The corrected, separately reviewed child completed all 60 frozen checks on the retrospective hypothetical MoO4 fixture, at dielectric constants 1 and 78.4. It retained 93 finite float64 arrays/scalars. Root and an independent reviewer reconstructed the numerical comparisons from those saved arrays without rerunning molecular integrals. All 180 preparation pins still match.

| Comparison | Maximum absolute discrepancy | Frozen absolute tolerance |
|---|---:|---:|
| Stock C-PCM response, eight cases | 3.122502256758253e-17 | 1e-10 |
| Central finite difference, h=0.001 | 5.023950615874913e-13 | 1e-8 |
| Central finite difference, h=0.0005 | 1.3873530518577603e-12 | 1e-8 |
| Linearity | 3.8163916471489756e-17 | 1e-10 |
| Reciprocity | 1.7787691892340307e-20 | 1e-10 |

Relative tolerance remains zero. The dielectric-one and zero-direction responses are exactly zero. All eight screening curvatures satisfy the fixed nonpositive criterion. The saved perturbations match the declared zero, positive, negative and seeded mixed directions; the initial density matches the existing fixture. These directions are numerical response probes, not claimed physical occupied densities or inherited chemical states.

The child returned zero after 7.009772666962817 seconds. Thirty-three RSS samples had maximum 281,526,272 bytes, within the 120-second/2-GiB sampled guard, with no cap termination or monitor error. The PySCF getter and requested OMP count were both one; actual native team size was not measured. The child process is terminal and absent. No SCF, nuclear gradient, parent molecule or held-out case was evaluated.

The [saved-array analysis](analysis.json), produced by [analyze.py](analyze.py), verifies complete check coverage, finite arrays, central-difference reconstruction, linearity, reciprocity, curvature, pins and artifact hashes. The [terminal review receipt](TERMINAL_REVIEW.json) binds the independent review. Both approval copies and supervisor/launch receipts agree. The original [v1 startup failure](../cpcm-response-probe/FAILURE_REPORT.md) and its nine terminal artifacts remain unchanged. V2 corrected only when the mock support libraries are imported; it did not change the response operator, fixtures, tolerances or resource limits.

The worker records successful cache/factor/surface preservation checks, but its transient snapshots were not saved and cannot be independently reconstructed. Input preservation used numerical array equality rather than direct flag/identity/byte measurements. The checkpoint writer is non-atomic; this clean result has valid CRCs and complete matching arrays, which does not qualify interrupted-run recovery. Geometry and solvent settings must remain unchanged after build. Stock and candidate share integral/runtime components, so agreement establishes bounded implementation equivalence rather than independent physical accuracy.

This closes one prerequisite identified by the derivative/stability audit: the standalone electronic C-PCM response action at fixed geometry on this reference. Full solvent-aware Fock response, production response wiring, internal/external orbital-stability channels, consistent nuclear derivatives and parent electronic accuracy remain unqualified. The prior full-J failure remains. Exact Mo34WV identity and all twelve integrated requirements remain unmet: 24 assessed roles, zero verified complements. No new native run or physical admission follows from this result.
