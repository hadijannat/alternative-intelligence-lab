# Independent retrospective implementation review

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

Scope: cpcm-rij-memory-qualification/PROTOCOL.md, preparation.json, run.py, test_run.py; unchanged memory.py, RI wrapper, original supervisor, native gradient definition, and completed run-v1 artifacts. The qualification directory is untracked, so this review inspected its full source rather than claiming a committed baseline diff. No notepad path was supplied. Root confirmed launcher session 37144 terminated with exit 0 before this terminal audit. No scientific operators or SCFs were launched by this reviewer.

## Independent verification

All 57 preparation pins equal run-v1/pins.json and match freshly computed SHA256 hashes. Five ordered operator receipts match their supervisor files; all six children exited 0 without termination or monitor error, within their 180-second / 2-GiB sampled-RSS guards. Phase1 gate and final result match all case checks. Seven gate/provenance unit tests independently passed in 0.343 seconds.

Direct NumPy recomputation from each operators-*/arrays.npz and the previous campaign arrays verified exact density/input provenance, finite arrays, all four J/PCM comparisons, J zero/additivity, affine PCM q/V controls, and epsilon1 zero response. This does not import or invoke the scientific worker.

| Case | Checks | Max J error | Max PCM V error | J additivity error | PCM affine V error |
|---|---:|---:|---:|---:|---:|
| anion-water | 42 | 0 | 6.11e-16 | 5.15e-13 | 2.13e-14 |
| neutral-water | 42 | 0 | 2.78e-16 | 1.01e-12 | 1.42e-14 |
| anion-eps1 | 46 | 0 | 0 | 5.15e-13 | 0 |
| heldout-Mo2O7 | 42 | 2.20e-13 | 8.33e-16 | 1.63e-12 | 4.09e-14 |
| new-external | 42 | 7.39e-13 | 7.77e-16 | 1.40e-12 | 5.15e-14 |

PCM oracle energy and q differences are zero in these arrays. The largest affine q error is 1.33e-14. Zero J is exactly zero. All are within frozen thresholds. Each operator case has seven sequential metric-call receipts with finite J, CD factorization, and no three-index cache/output. Factor records show RI metric first, PCM surface second, PCM rebuild third; pointer aliasing, read-only and Fortran flags pass. Reset, new-factor, unsupported-method and storage checks pass in saved records. These transient properties are recorded process evidence, not reconstructed live heap inspections.

For the sole SCF, independently recomputed 2*C_virtual.T*F*C_occupied gives memory gradient norm 1.484382496048251e-7 and direct gradient norm 1.8679534436433578e-4, within 1e-5 and 1e-3 respectively. Density maximum difference is 8.712475185745916e-13, and electron trace is 86.00000000000006 (error 5.684341886080802e-14). The stored density reconstructs from occupations/orbitals to 1e-12, and orbital overlap orthonormality holds to 1e-10. Total energy -663.7140752270335 Eh agrees with the native convergence log and differs from the saved native RI result by 9.094947017729282e-13 Eh. There are 32 sequential iteration records, 36 sequential valid RI calls and nine passing SCF checks. Sampled SCF RSS maximum is 607600640 bytes; wall time 59.1992 seconds.

Evidence: run-v1/result.json, phase1-gate.json, pins.json, operator-receipts.json; each operators-*/{arrays.npz,result.json,supervisor.json,metric-calls.jsonl}; scf-new-external/{arrays.npz,result.json,supervisor.json,metric-calls.jsonl,iterations.jsonl,native.log}. Operator sampled RSS maxima range from 118587392 to 147521536 bytes.

## Findings by severity

CRITICAL: None.

HIGH: None.

MEDIUM: None affecting this frozen scientific acceptance.

LOW: run.py:69-84 and throughout uses untyped dictionaries/functions and densely combined statements. This falls short of the programming skill's strict type-contract perspective and makes future changes harder to review. It follows nearby frozen drivers and has not demonstrated a correctness failure in this bounded run. Do not alter these pinned files to address stylistic feedback after execution; consider typed records in a separately versioned successor.

## Skill-perspective check

Loaded programming/SKILL.md, its Python reference, and remove-ai-slops/SKILL.md. The overfit/slop pass found no deletion-only, removal-verification, brittle prompt, or tautological tests. The gate tests meaningfully check negative admission behavior; the provenance test additionally prevents operator/SCF calls, though its count assertions alone are only structural checks. Production geometry/source parsing serves actual input/provenance boundaries. No unnecessary new abstraction or unrelated parsing was identified. Strict programming style deviations are recorded LOW above; no material remove-ai-slops violation found. Broad worker exception handling retains traceback and returns failure at the process boundary.

## Limits

APPROVE applies only to retrospective implementation equivalence for these cases. It establishes neither parent-scale memory feasibility nor physical or chemical validity, fresh holdout performance, target existence, or chemical complementarity. Sampled RSS is not a certified peak or hard OS cap. The saved Focks permit independent gradient arithmetic, not independent reconstruction of the Focks themselves. Total DFT energy components are not saved, so total energy was cross-checked against logs/previous results rather than recalculated from component integrals. No fresh scientific runs, full-repository lint/typecheck/security scan, or parent execution were performed. No source, pins or scientific results were modified.
