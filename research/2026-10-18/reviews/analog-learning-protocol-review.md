# Analog-learning replay: source and protocol advice

Date: 2026-10-18. Read-only protocol review; no numerical response arrays inspected, no replay, no downloads. Scope: acquisition PROTOCOL, local primary `noncarbon-discovery-2026-10-15/research/information/raw/analog-2024.xml`, verified `analog-learning-replay/sources/browser-native/README.md` and `PNASscriptFig3.m`. The attempt1 `.m` files are preserved HTML403 responses. No genuine Fig4 script or Experiment2 helper was available at review time. This is a conditional replay recommendation, not approval of an unwritten implementation or an empirical result.

## Verified mapping

- Primary Fig3 uses XOR, two variable inputs, differential output O=O+−O−, and nudge eta=0.5. Fig4 regression uses one output node, one varying input plus fixed boundary nodes, eta=1. The 29 Fig5 tasks are separately trained tasks, not held-out task generalization.
- README: TRAIN/TEST rows are sources followed by targets; columns are examples. Multiply normalized node values by NODEMULT to obtain volts. TLOC gives zero-based row/column locations of output nodes. TestFreeState axes are `(row,column,measurement,test-example)`; TestClampedState is a different network and must never be used as prediction.
- Fig3 script: `Time=cumsum(EXP.LearnTimes)/10^6`. LearnTimes is microseconds spent unfrozen between measurements; primary paper explicitly excludes switching/settling overhead. Do not call this elapsed wall time or infer whole-system energy from it.
- Fig3 output is `(TestMeasurements(2,:,:)-TestMeasurements(1,:,:))*NODEMULT`. For DEL=1, targets are alternating pairs in rows SOR+1 through SOR+TAR, with second-minus-first order. Training output/labels use the analogous TRAIN fields. Stored TestMSE is scaled by NODEMULT squared. These fields may be derived class properties: their implementation and denominator are not established by Fig3 alone.
- For a direct reconstruction, read target free-network voltages at TLOC in the documented order, then apply differential conversion only where DEL and target count support it. Validate row/column orientation and alignment against any independently stored measurement fields. Do not guess MATLAB object internals or transpose until a desired curve appears.

## Minimal retrospective replay

1. Freeze the exact native checksum, run inventory, eligible task families and all-run inclusion rule after schema inspection but before numerical responses. Separate independent physical runs from duplicate exports and single-point/oscilloscope/calibration data. If only Fig3 mapping is established, perform the XOR replay first; Fig4 stays pending instead of silently borrowing its output convention.
2. Audit TRAIN/TEST overlap using the full source boundary vector, including fixed inputs. Record exact duplicate examples, unique input sets, target conflicts, ordering and counts. Compare in native coordinates before conversion. If an approximate comparison is required, justify its tolerance from storage/acquisition precision before results. Report shared points and genuinely new points separately; TEST names alone confer no independence. Do not invent a held-out set from already trained examples.
3. Use observed free-network outputs without fitting a digital readout. Calculate explicit mean squared voltage error over examples; keep targets separate when their task meanings differ. Compare recomputed error with stored error only as a consistency check, allowing an explicitly reported normalization difference rather than selecting a convenient denominator.
4. Evaluate the first demonstrably valid initialized snapshot and the final recorded complete snapshot. Do not choose a minimum-error epoch. Report the complete trajectory descriptively, including missing/nonfinite observations. If initialization cannot be validated, call it the earliest available snapshot, not a frozen pretraining control. A no-learning intervention run would be stronger causal evidence and is not implied by a fixed first-snapshot baseline.
5. Frozen-initial baseline: hold that earliest valid response vector fixed on the same evaluation input set. This is valid only where those initial input responses are actually observed; no arbitrary interpolation across missing inputs.
6. Constant baseline: train-label mean for each run/output. Affine baseline: least-squares intercept plus physical variable inputs, fitted using TRAIN only and scored on the same TEST set. For XOR use intercept,V1,V2, with no interaction term; adding V1*V2 would change the baseline family. For regression use intercept,V1. Handle rank deficiency with a declared least-squares convention and report it; never add a post-hoc model to beat the observed network.
7. Report endpoint errors and differences versus all baselines, per run and as a complete run table. Ratios with zero denominators remain undefined. Do not bootstrap timepoints as independent experiments or infer population confidence from one trajectory. No generalization claim without actually untrained observations, and no full A/C or chemical-maintenance credit from this electronics component.

## Source-script traps

Fig3 prepends synthetic x=1e-10 plotting points; they are not measured times. It suppresses the first mode-error row when `sum(errvals)==0`, which can also reflect cancellation of nonzero signed errors. It plots an initial truth table using measurement index 2. None of these is an adequate data-validity rule for a new replay. The independent protocol must preserve raw rows and determine initialization structurally, not from favorable errors. Mode decomposition is optional and unnecessary for the minimal error/baseline replay; reproducing it would require the actual mode helper and clear normalization.

## Review status

CRITICAL: none. HIGH: none in the acquisition protocol. MEDIUM: no assessed code change yet. LOW: none.

Skill-perspective check: programming and remove-ai-slops criteria were consulted in this review session. Their minimality guidance favors direct measured-output reconstruction, two conventional baselines and a complete run table, with no unnecessary mode-analysis framework or prose-pinning tests. Mapping consistency checks are meaningful; tests that simply assert a chosen scientific conclusion are not.

Recommendation: proceed to freeze a narrowly scoped replay protocol once schema and output/time orientation are confirmed. Exact Fig4 implementation mapping, initial-row validity and independently stored measurement availability are still open. Reported source findings were already consumed, so any replay is retrospective. No source-level observation establishes maintained repair, inheritance, integration with PMo12/Mo34WV or general intelligence.

## Review of subsequently frozen REPLAY_PROTOCOL.md

Reviewed the newly authored protocol before real-data numerical replay. The named-property schemas now establish stored `TestMeasurements` shape `(TAR,TST,MES)`, `DOTEST` and `TestMSE` shape `(1,MES)` for the XOR and modes13 families. `TrainFreeState` contains one grid per snapshot, confirming the protocol's prohibition on inventing a complete training-grid output tensor. This resolves the initial advice's uncertainty about whether TestMeasurements is available as stored data; actual raw/stored equality is still a prospective consistency check.

Verdict: **APPROVE the analysis design; implement the following boundary clarifications before execution.** They do not change the scientific question or select favorable outcomes:

- Evaluate raw/stored target agreement on complete measured snapshots, as the root's implementation assignment specifies. Do not let a mismatch in an explicitly excluded placeholder silently block an otherwise valid run, and do not use agreement itself to select favorable snapshots. Preserve mismatch diagnostics and stop the run if any eligible snapshot fails.
- Require even TAR for DEL=1. Retain zero-complete-snapshot runs as failures without indexing an empty result or manufacturing a baseline.
- DOTEST is stored as float64. Validate a stated flag encoding rather than applying generic truthiness that accepts NaN or arbitrary nonzero values. If its actual encoding is not established, stop and document the mapping uncertainty.

The source-independent direct free-node construction plus stored-target cross-check is startable for both families without executing unavailable MATLAB helper methods. Earliest/final complete measurements, exact plus fixed-tolerance whole-boundary overlap, train-only mean/affine rivals and a frozen earliest observed vector are correctly specified. The protocol explicitly avoids best-epoch selection, claims of pretraining initialization, a causal no-learning control, independent TEST inference, and chemical maintenance credit. Input drift and capacitor change remain diagnostics. Signed-error cancellation and source plotting tricks are not used as validity rules.

No numerical response values were read in this review. No implementation or empirical result was approved. CRITICAL/HIGH findings: none. The boundary clarifications above are ordinary implementation requirements, not evidence of a scientific protocol defect.
