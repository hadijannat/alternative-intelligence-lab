# Verification

| Requirement | Verdict | Evidence and limit |
|---|---|---|
| Audit all481 acquired files | Pass | inventory.py; file_manifest.json/csv; every acquisition/repository hash and size matches; exact path coverage |
| Preserve empties, gaps and derived copies | Pass |8emptyfiles, absent225block41,603unsupportedprocessedrows including12missingvoltages; no imputation |
| Qualify metal-supply controls | Pass for source audit; raw dose binding unresolved | SOURCE_AUDIT.md; separate-wire nominal factorial, no matched founder-preload withdrawal;36admissible exact raw assignments |
| Freeze evaluator before numeric outcomes | Pass within retrospective scope | PROTOCOL.md; AMENDMENTS.md clarifies metadata-only longtail/gap before extraction; published rounded outcomes already known |
| Avoid fitting reserved observations | Pass | analyze.py passes only training mask to fit; fixed24h cutoff, grids, slopes and tolerances;140training/280reserved summaries |
| Native current/voltage and clock semantics | Pass for explicit conditional handling | extraction_notes.md; raw specimen-relative voltage; actual currents and pulse durations; unassigned gaps and geometry differences retained |
| Conserved-competence model and baseline | Scientific model fails overall | M0/M1each4/10screens versusflat7/10; all slope sensitivities retained; no post-forecast model changes |
| Numeric/parser self-checks | Pass | results/analysis.json selfchecks; known synthetic aggregation, exact phase/zero-rate limits, positivity, competence conservation, synthetic recovery and M0 nesting |
| Founder/new active-function discrimination | Unresolved by source data; ambiguity demonstrated | Same-initial finite-inventory counterexample has different active origins and identical total activity/voltage; no actual atom-age functional attribution |
| Independent review | Pass for bounded negative experiment | Workspace .omo/evidence/regeneration-controls-review.md: APPROVE; independently reproduced all420aggregates and60fits, phase-recursion predictions, source controls, gaps and origin conservation. This does not validate repair or material origin. |
| Final JSON and frozen-input integrity | Pass | Both authored result ledgers parse;12unique negative IDs; saved protocol/amendment/script/manifest hashes match final files; final analysis SHA256 c9f3a2a18fed457d8842318c10d43c1557d21e34fe7f7bb092842351a695412c |
| No new life/integration claim | Pass for scope | Zero verified integrated complements; prior source/model negatives unchanged |

Executed with `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`. Commands: `inventory.py` and `analyze.py` in this folder, from repository root. Execution observables are in results/execution.txt; parser/extraction failures remain in execution_failures.txt and INVENTORY.md. Native-source errors and failed scientific forecasts are not confused with implementation checks.

Biome LSP is unavailable and was previously declined; authored JSON is checked with the standard-library parser. No SciPy repair, new dependency installation, author contact, physical experiment, prospective validation, complete Fe/charge/energy closure or gas-output attribution is claimed.
