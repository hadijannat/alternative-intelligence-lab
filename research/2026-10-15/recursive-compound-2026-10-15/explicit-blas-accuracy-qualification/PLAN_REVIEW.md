# Explicit-controller accuracy qualification draft review

Date: 2026-10-16. Scope: design review before implementation, not execution approval.

- codeQualityStatus: WATCH
- recommendation: APPROVE for implementing the scoped adapter, with the two pre-freeze clarifications below
- blockers to implementation: []
- Launch approval: not granted; implementation, tests, complete freeze and independent review are still required
- Draft SHA256 at review: `070474ef7d65d0f08f334bbf9fbb1c638831a085aa7561f3a5e8fae3b45102be`

## Findings by severity

CRITICAL: none. HIGH: none.

MEDIUM — `explicit-blas-accuracy-qualification/PROTOCOL_DRAFT.md:67` requires every child to save nonempty stderr. A successful clean child can legitimately emit zero stderr bytes. Interpreting this literally would reject successful execution or encourage fabricated filler. Before freeze, require preserved native.log/stdout/stderr files with hashes and sizes; allow empty stderr and require evidence-bearing output through structured receipts/native logs. Do not synthesize diagnostic text solely to satisfy nonemptiness. This is an evidence-contract correction, not a numerical criterion change.

LOW — draft lines44 and57 should explicitly bind the MemoryRI gradient <=1e-5 to the RI-converged density and RI orbitals/occupations. The text requests comparisons at both direct- and RI-converged densities and then says all table gates. Original code computes this stationarity norm only at RI convergence. Requiring RI stationarity at the direct-converged density would add an unintended condition; direct and approximate RI stationary points need not coincide. Evaluate operator/PCM comparison gates at both densities; retain full MemoryRI and direct-Fock-at-RI residual checks at RI convergence. Additional direct-SCF residuals may be recorded descriptively without inventing a new tuned acceptance bound.

## Source and threshold verification

Read the draft and existing source/protocols directly, without reading the running parent diagnostic outcome or the prospective XYZ/input/output contents. The scoped scientific design is coherent: explicit OpenBLAS1/PySCF4 numerical qualification on Mo references, not W/V transfer, target-compound validation, experimental evidence or parent-SCF authorization.

Verified against `cpcm-rij-memory-qualification/run.py` and its PROTOCOL.md:

- five ordered retrospective cases, four saved-density labels;
- memory/native J and MemoryPCM/BlockedPCM E/q/V absolute <=1e-10;
- J zero/additivity <=1e-9;
- affine PCM q/V, epsilon1 E/q/V, reset/rebuild E/V <=1e-10;
- retrospective SCF energy <=1e-8, density <=1e-5;
- full memory gradient <=1e-5, direct gradient at RI density <=1e-3, electron trace <=1e-8;
- explicit convergence, fresh initial metric before PCM, factor-only storage/reuse/alias checks, reset/cache clearing and unsupported-path rejection;
- original PBE/def2-SVP/ECP/grid2/screening, SCF 1e-11 energy/1e-7 gradient/max60 settings.

Verified direct-accuracy definitions against `rij-jkfit-qualification/run.py:204-245` and `rij-qualification-v2/run.py:106-147`: max elementwise J error <=1e-3 Eh; absolute 0.5 Tr[P delta-J]/nMo <=1e-3 Eh/Mo; symmetry <=1e-10; total SCF energy error <=1e-3 Eh/Mo; the same full-Fock residual and trace limits. No tolerance relaxation is proposed. Perturbation seed7392016, symmetrization and Frobenius0.01 match `rij-jkfit-qualification/run.py:183-187`.

Comparing newly recomputed direct J to saved direct J at 1e-10 is a new application of the existing strict equivalence bound, not a check that the original memory campaign already performed. The draft adds it prospectively and before observing the case, so it is legitimate; describe that distinction accurately in the final implementation/report.

Confirmed solvent attachment in `cpcm-blocked/blocked_pcm.py:120` delegates through pcm_for_scf; the pinned runtime `_attach_solvent.py:96-107` adds v_solvent in get_fock. Original residuals use get_fock(dm=RI_density), then the norm of get_grad with RI orbitals and occupations. Independent residual review should reproduce that exact definition, including its occupation convention and full solvent potential, rather than substitute a vacuum commutator or a differently scaled residual.

The controller and runtime source references resolve: unchanged saved-metric explicit controller, BLAS REQUESTED environment, binary/symbol checks and configured-count snapshots; parent-openmp-qualification-v2 runtime_pins includes imported package paths, package source/native/basis files and stdlib extensions. Existing operator_gate checks alone are insufficient for the draft's stronger exact-check-set requirement: the adapter must implement the declared nonempty/exact names, phases/order/counts and malformed/nonfinite rejection rather than merely invoke old all(checks) acceptance.

## Prospective-case and SCF boundary

The declared HMo2O7(-1) arithmetic is internally correct: 142 all-electron electrons, minus 56 Mo ECP core electrons gives 86 explicit electrons; spin0 implies 43 alpha/43 beta. This supports a declared RKS singlet ansatz, not measured multiplicity or a ground-state claim. Actual ECP core counts and molecule electron count remain mandatory future checks. No source-output spin was inferred here.

A prospective numerical case from the same source family is useful for avoiding direct tuning to its computed residuals. It is not an independent experimental measurement or method-independent validation. The draft correctly preserves source-method/geometry limitations, alias/freshness uncertainty, and the no-substitution rule after prior use or failure. Raw hash/provenance/freshness audits must occur before freezing; this review did not consume the geometry.

The phase dependency is sound: complete passing parent repetition evidence is required before launch; all five retrospective operator children before one retrospective MemoryRI SCF; that SCF before prospective operators; prospective operator pass before prospective SCFs; direct convergence and saved evidence before MemoryRI SCF. The prospective initial density must be frozen once and reused across its operator/SCF children. Exclusive claims must be enforced inside worker entry as well as the coordinator.

Budget arithmetic is correct: 5 retrospective operators +1 retrospective SCF child +1 prospective operator +1 prospective SCF child =8 children. The last child contains 2 SCFs, yielding at most3 SCFs total. Each child's 180 seconds includes all its work; the nominal cap sum is1440 seconds excluding setup/termination overhead. Sampled 2GiB RSS is not a hard peak bound. Resource failures remain incomplete, with no automatic extension/retry.

## Review perspectives and limits

Programming and remove-ai-slops perspectives were loaded earlier in this reviewer session and applied here. No production diff or tests yet exist for this draft. Do not add prose/phrase tests: mock tests should target the actual gate/claim/resource/result contracts. Pin verification and malformed-result checks are justified trust-boundary work, not unnecessary parsing. Exact expected check sets must be derived from the frozen scientific contract and exercise missing/extra/duplicate checks, not simply echo a success list from the implementation.

Only this report was written. The approval-bound original prelaunch report was not modified. No numerical operator, molecule build, SCF, PCM, held-out geometry, deposited source output, or live parent result was consumed. Existing source inspection establishes design consistency, not execution success. No independent verification of prospective raw hashes/freshness is claimed. Freeze review must still verify the adapter, tests, complete manifests, explicit-controller behavior and the two clarifications before launch; zero physical admissions remain.

## Corrected-draft disposition, 2026-10-16

Independently compared the full corrected draft to the retained prior version. The changes are confined to the two requested clarifications: stderr may be empty and logs require meaningful protocol evidence rather than arbitrary nonempty bytes; MemoryRI stationarity and direct-Fock residual apply at RI-converged density/orbitals, while operator comparisons apply at both converged densities. Numeric bounds, cases, settings, resource budgets and phase order are unchanged. Both findings above are resolved.

Independently hashed corrected draft `27943221f7205f7dda7f4077935dc6dc9ac3e11f9d833b09877a4a0a92f262c6` and retained `PROTOCOL_DRAFT.before-scope-clarifications.md` `070474ef7d65d0f08f334bbf9fbb1c638831a085aa7561f3a5e8fae3b45102be`. Both match preparation-audit.json. The latter audit remains preparation-only; its raw geometry inventory assertions were not independently rerun here. No live parent outcome or prospective geometry was inspected.

Updated codeQualityStatus: CLEAR. Recommendation: APPROVE for scoped implementation, blockers: []. This supersedes the WATCH design disposition, not the requirement for implementation/tests/freeze and separate launch approval. The approval-bound original prelaunch report remains untouched.
