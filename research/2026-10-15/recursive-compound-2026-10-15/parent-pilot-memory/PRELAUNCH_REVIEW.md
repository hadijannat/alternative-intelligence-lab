# Independent parent-pilot prelaunch review

Prelaunch status: CLEAR
codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

Read-only review of pilot.py, PROTOCOL.md, test_pilot.py, preparation.json, existing test output and unchanged qualified MemoryRI/PCM/supervisor sources. No parent arrays, chemistry operators, scientific runs, synthetic subprocesses, or approval records were created by this reviewer.

Fresh standard-library-only verification imported the driver and recomputed preparation_pins(), qualification_manifest(), and allocation(). All 66 preparation hashes matched, including the original 57 qualification pins and unchanged supervisor. All 33 qualification artifact hashes and six child result/supervisor gates validated. independent-root-review.json and run-v1 were absent at inspection, as required before root approval.

The driver reserves run-v1 exclusively, validates approval in launch and worker, binds preparation and qualification hashes, and exclusively creates worker-started.json. Missing approval or existing output fails closed. There is one explicit mf.kernel(dm0=dm), at most 20 cycles, and no restart, second SCF, direct-J fallback, optimization, or target calculation. Root approval remains necessary before this one attempt.

Input checks bind P0_A XYZ and metadata, exact heavy-site mapping, Mo36O128H32/196 atoms, charge -8, spin 0, 3068 AOs and 1568 explicit electrons. RKS PBE/def2-SVP with Mo ECP, grid2, direct tolerance 1e-13, JKFIT, C-PCM epsilon78.4/SWIG17/scale1.2/probe0 and AO1 agree with the frozen scope. Metric build precedes PCM and is checked against empty PCM intermediates. Actual native factor aliases, immutable Fortran factors, two exact factor stages/shapes, no retained S, no ERI and no three-index storage are enforced initially and each cycle.

Arithmetic independently gives 10622806400 bytes = 9.893259406089783 GiB. This is very close to 10 GiB and does not bound native scratch/transients. The protocol clearly discloses this. One 900-second/10-GiB sampled-RSS child uses the unchanged supervisor and one requested thread; no hard OS memory cap or guaranteed peak is claimed.

Stages are written before expensive phases. Initial density is checkpointed before metric construction; cycle density/orbitals atomically replace partial.npz via partial.tmp. Native checkpoint/log, metric calls, factor receipts, iterations, storage and terminal supervisor receipts preserve available progress. Exception tracebacks are retained when Python can execute them; process kills may leave only prior artifacts. This is an appropriate bounded failure model.

Existing tests.txt records six passing gate/arithmetic/synthetic-supervisor tests. Inspected their source: negative child/review/hash/dimension and existing-run tests exercise admission behavior; supervisor cases exercise successful completion and timeout. No deletion-only, brittle prompt or tautological removal tests were found. These tests were not rerun during this read-only review.

Findings by severity:
- CRITICAL: none.
- HIGH: none.
- MEDIUM: none affecting this attempt.
- LOW: pilot.py uses untyped record dictionaries and densely combined statements, as do nearby frozen drivers. Programming/remove-ai-slops perspectives were consulted earlier in this review session and applied here. Strict programming type/style expectations are not fully met; no needless production parsing/abstraction or material test-slop violation was identified. Frozen files should not be cosmetically changed after approval.

Approval is for one bounded numerical pilot only. Neither prospective convergence nor parent peak-memory feasibility is established. Even numerical success would not establish chemical validity, orbital stability, target existence, geometry optimization or relative chemistry. No full-repository typecheck/lint/security scan was performed.
