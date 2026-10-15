# Independent saved-J qualification result audit

codeQualityStatus: CLEAR
recommendation: APPROVE
blockers: []
Result: PASS_RETROSPECTIVE_SAVED_J_HANDOFF, scoped to the small new-external case.

Root confirmed launcher42747 terminated exit0 before this audit. Reproducible saved-array-only audit: .omo/evidence/parent-saved-j-result-audit/check_arrays.py and array-audit.json, executed using the qualified aligned interpreter. No scientific operator, PCM surface, molecule, regenerated initial guess or SCF was run. Parent J was only hashed through the provenance gate, never loaded numerically or recomputed.

Live validate_gate() matches run-v1/launch-gate.json, revalidating the complete frozen manifest, root-review binding, original first-J provenance and successful OpenMP runtime/source qualification. Both runtime observations record actual4threads and the exact frozen qualified runtime inventory/interpreter. Both receipts match their independent supervisor files and launcher embedded receipts, exit0 with no termination/monitor error, within180seconds and2GiB sampled RSS each. Launcher errors are empty and gate_unchanged=true.

There are21 passing operator checks and79 passing SCF checks,100 total. Repeated stage/callback storage checks are distinct process observations, not100 independent scientific trials. Exactly zero SCFs occur in the operator child and one in the SCF child; there is no parent execution.

## Independently recomputed effective-potential comparisons

All saved arrays are finite. Initial densities exactly match the frozen proof archive and its independently recomputed row-streamed density digest. Saved perturbation equals the frozen delta; perturbed density equals initial+delta exactly.

| Quantity | Initial absolute error | Incremental absolute error | Limit |
|---|---:|---:|---:|
| Gas-phase effective potential | 4.796163466380676e-13 | 4.796163466380676e-13 | 1e-10 |
| Solvent potential | 0 | 0 | 1e-10 |
| Solvent energy | 0 | 0 | 1e-10 |
| Coulomb energy | 1.1368683772161603e-13 | 4.547473508864641e-13 | 1e-10 |
| Exchange-correlation energy | 0 | 0 | 1e-10 |

The first cached native request digest independently equals perturbed-initial (including floating-point subtraction). The second equals the zero matrix. Thus the test exercises native incremental and zero-increment paths after the one saved hit, not simply repeated full-density evaluation.

## SCF comparison

Saved density reconstruction from occupations/orbitals passes1e-12; overlap orthonormality passes1e-10. Independent arithmetic against the original4thread uncached small SCF gives:
- Density max error7.092659792817813e-13, limit1e-5.
- Total energy difference2.2737367544323206e-13Eh, limit1e-8.
- Electron trace error0 against86electrons, limit1e-8.
- Full memory Fock orbital-gradient norm1.4843850840990713e-7, limit1e-5.
- Direct full-Fock orbital-gradient norm1.8679534481994985e-4, limit1e-3.

Gradients were independently evaluated as2*C_virtual.T*F*C_occupied. Native log has one convergence-energy entry matching the saved total energy; the32 iteration records are sequential and convergence is true. Total DFT energies were cross-checked rather than reconstructed from integrals/quadrature.

## Handoff and factor lifecycle evidence

Both cached objects' first effective-potential record has saved_J_hits1, native_calls0, PCM present, RI absent. Their first native fallback request has PCM present and RI absent; later requests/stages retain both. Every cached stage records exactly one saved hit. The operator child has2 sequential cached native calls; the SCF has34. All metric-call receipts record finite J, CD factorization, no cached3index and no tensor output. Saved passing ownership checks confirm pending=false after consumption and unchanged immutable initial density.

Operator factor creation shapes are746square (cached PCM),1085square (uncached RI),746square (uncached PCM),1085square (cached fallback RI). SCF shapes are746square (cached PCM),1085square (cached fallback RI),746square (direct comparator PCM). Every observed factor shares its input storage, retains the same pointer, and is immutable Fortran. Every recorded storage dictionary is all true, covering shape/reuse and no S/ERI/three-index storage whenever applicable. These are recorded in-process properties plus source inspection, not independent inspection of a terminated heap.

Operator wall6.129336540936492seconds, sampled RSS902234112bytes. SCF wall27.049825499998406seconds, sampled RSS928759808bytes. These samples are not certified peaks or OS allocation limits.

## Findings and perspective checks

CRITICAL: none.
HIGH: none.
MEDIUM: none.
LOW: no new blocker or material test-slop finding; dense/untyped scientific-driver style remains a previously documented maintainability limitation.

Programming and remove-ai-slops perspectives were consulted during this review session and applied to the handoff/runner inspection. Provenance/density/request validation is necessary boundary logic for this specific handoff, and the native adapter supplies the required single-use behavior. No needless production extraction or removal-only assertion was identified in the inspected scope. Synthetic tests were not rerun during this terminal audit; repository-wide lint/typecheck/security scans were not run.

The result establishes retrospective small-case saved-J handoff, incremental semantics and PCM-before-RI storage ordering. It does not qualify a parent consumer, parent SCF convergence/readiness, parent peak memory, whole-SCF performance, fresh holdout, physical admission or chemistry. Parent metric construction while PCM remains resident is still a separate resource question. Prior failures and first-J results remain unchanged through verified provenance; this review authorizes no additional scientific run.
