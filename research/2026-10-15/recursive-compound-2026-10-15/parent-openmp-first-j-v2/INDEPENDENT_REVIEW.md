# Independent parent first-J v2 terminal audit

codeQualityStatus: CLEAR
recommendation: APPROVE
blockers: []
Scientific scope: PASS_BOUNDED_FIRST_J_ONLY.

Root confirmed authoritative launcher20337 terminated with exit0. Audit used only saved arrays, metadata, SHA256 checks and read-only manifest/gate reconstruction through parent-openmp/env-aligned/bin/python. No molecule, new density, integral, operator, SCF or PCM surface was evaluated. Evidence: .omo/evidence/parent-first-j-v2-result-audit/check_artifacts.py and artifact-audit.json.

All172 preparation input hashes match current files. Live validate_gate() exactly matches launch-gate.json, thereby also rechecking qualification artifacts, qualified runtime/source manifests and root-review hash binding. Supervisor receipt equals the embedded launcher receipt: returncode0, no termination reason, no monitor error, wall251.5328401250299seconds against300seconds, sampled RSS maximum3432890368bytes against10GiB. Launcher and worker agree on PASS_BOUNDED_FIRST_J_ONLY, one J and zero SCFs, with all12 checks true. Independent checks.json matches the worker record.

J.npy independently loads as float64 shape(3068,3068), all entries finite, maximum asymmetry exactly0. SHA256 is88f8f78f3d371295cc5834db043d9c9223819132a35251dc536b56903c2fb007 and equals both worker and launcher hashes. This checks the saved output's integrity and structural properties; it does not compare against an independently computed parent J oracle.

There are exactly8 ordered stage records: worker_started, saved_density_load_start, basis_build_start, setup_complete, first_J_start, RI_factor_start, RI_factor_complete, first_J_returned. First J starts at9.195462seconds, factor completes at22.577040seconds, J returns at249.516471seconds. Measured first-J duration is240.32092929200735seconds. All times use worker elapsed time except supervisor total wall.

The sole factor observation is19612square, same input/output pointer, shares_memory=true, Fortran=true and readonly=true. Exactly one sequential metric receipt records CD, finite_J=true, no cached3index and no tensor output. Exclusive worker claim PID matches the terminal supervisor. Actual PySCF threads are4, interpreter resolves to the qualified aligned environment, and observed loaded native hashes match the qualified manifest. Source guards enforce BLAS controls1 and forbid instance SCF/kernel and PCM build entry points.

The original parent's saved partial.npz independently contains exactly density and integer scalar cycle0; density is finite float64(3068,3068), symmetric within1e-12, and validation metadata matches this run. Its hash is included in the verified input pins; no initial guess was regenerated. Worker checks record no PCM, no ERI, no three-index storage and immutable Fortran factor. These transient storage facts are process observations plus inspected code guards, not a reconstruction of the terminated process heap.

The original first-J run remains INCOMPLETE_OR_FAILED_FIRST_J and has no first_J_start event. Its source, preparation/review and specified failure artifacts are included in the172 verified pins. The earlier parent SCF timeout evidence is also bound through parent input provenance. No earlier result was replaced or rerun by this audit.

Findings by severity:
- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: none new in the narrow v2 guard repair. Existing dense/untyped driver style remains as documented in earlier reviews.

Programming and remove-ai-slops perspectives were consulted earlier in this review session and applied to the inspected diff. The production change is narrowly limited to the native unbuilt-PCM predicate and preservation pins for the old failure. It accepts only None or empty built-in dict for both caches, requires no nuclear grid potential, and is reused at both boundaries. No needless abstraction or removal-only test behavior was identified. The16 preparation tests were not rerun for this terminal artifact review; no full-repository lint/typecheck/security scan was performed.

This is evidence that one initial parent Coulomb request completed within the specified monitored bounds. Sampled RSS is not a certified peak or hard OS memory cap. There is no parent J oracle comparison, PCM numerical evaluation, SCF convergence/readiness evidence, whole-SCF performance estimate, speedup claim, physical admission or experimental validation. No follow-up scientific run is authorized by this result.
