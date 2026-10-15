# Requirement checks

Status: investigation complete, independently reproduced and approved for this bounded research scope. Every predictive adequacy screen fails. The pass entries below refer to completing and verifying the investigation, not validating a physical mechanism.

| Requirement | Verdict | Evidence | Correction or limit |
|---|---|---|---|
| Reproduce previous failure from the source | pass | [Diagnostic receipt](diagnosis/.omo/evidence/verification.json): 120 workbook values, 400 predictions, exact replay | Earlier scores include t=0; new primary scores exclude those eight fixed zeros |
| Identify a structural failure | pass | [Diagnosis](diagnosis/REPORT.md): F1×time collapse and five measured counterexamples | Establishes incompatibility of the reduced family, not a unique cause |
| Ground alternatives in primary chemistry | pass | [Source review](research/REPORT.md), [10 source/design checks](research/.omo/evidence/verification.json) | Rate laws and initial complex occupancy remain hypotheses |
| Freeze fair comparison and retain failed attempts | pass | [Protocol](PROTOCOL.md), [snapshot](results-v1/freeze.json), development-v1/v2, [all fits](results-v1/fits/) | Six starts, max_nfev=160 per start; derivative calls additional. 22 unsuccessful starts retained; no selective retry |
| Test material, observation and split logic | pass | [30-test log](verification-tests.log); 23 model/validation tests passed before launch, seven verifier tests afterward | Software evidence only |
| Whole-dose, nested and late-time validation | pass | [Validation](results-v1/validation.json), [late-time](results-v1/late_time.json), [raw predictions](results-v1/predictions.csv) | All six candidates and nested procedure fail the accuracy screen. Retrospective data, eight dose groups only |
| Profiles, state inventories and numerical refinement | pass | [20 profiles](results-v1/profiles.json), [240 state rows](results-v1/bulk_state_inventories.csv), [numerical checks](results-v1/numerical_checks.json) | Coarse profiles are not confidence intervals; full-fit numerical certification does not separately certify each fold |
| Frozen chemistry in both historical transport closures | pass | [Transport results](results-v1/transport.json), [refinement](results-v1/transport_refinement.json) | Both benchmark screens fail. Active catalyst and complex retention remain assumed |
| Independent result audit, replay and full refit | pass | [Independent receipt](independent-verification.json), [replay](saved-parameter-replay.json), [repeat summary](verification-v1/summary.json) | 248 fits, 1,488 starts, 2,512 predictions, 392 splits; 262 refit files match. No physical replication |
| Preserve previous laboratories and source inputs | pass | Independent receipt checks 21 frozen inputs plus ten prior-laboratory hashes | No prior fit or source was overwritten |
| Final figures, report, links and review | pass | [Report](REPORT.md), [figure](comparison.png), [presentation checks](presentation-checks.json), [independent review](../.omo/evidence/rna-reaction-tests-code-review.md) | Review APPROVE, no blockers; WATCH records low-priority missing interface type annotations. Dedicated static analysis not run |
