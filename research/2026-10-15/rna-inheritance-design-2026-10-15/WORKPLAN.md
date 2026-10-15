# F1 experiment design and simulation

Objective: design and simulate experiments that distinguish newly generated active F1 from reporter product, measure catalyst retention, and test functional inheritance across physical compartment generations.

Scope: this directory only, plus an independent review record in `.omo/evidence/`. Preserve all previous laboratories, failed model results and source archives. Use the installed pinned numerical runtime. No physical experiments, paid computation, publishing or author contact is needed for this design task. Main-task effort settings are not exposed by a runtime-inspection tool; no change to them is claimed.

## Completion requirements fixed before official simulations

| Requirement | Evidence required |
|---|---|
| Chemical identity and origin | Primary-source sequence/length audit; founder/new/reporters/precursors separated; isotope and junction identity controls; no mass-to-activity shortcut |
| New functional catalyst | Observable-based conservative activity attribution; explicit indistinguishable-world counterexample; calibration, contamination, recovery, native/refolded and censoring gates |
| Catalyst retention | Before/after inside/outside/surface observations; amounts and volumes; mass retention, capacity retention and inactivation separated; unknown recovery and missing-fraction counterexamples |
| Physical generations | Explicit parent/daughter identities, conservative partition, finite feed, chemical origins, external exchange and destructive sampling; no replacement of division with serial dilution |
| Functional inheritance | Randomized parental-state intervention under common conditions; independent root families; founder and prior-generation carryover bounds; current-generation pulse; matched controls and horizontal-transfer challenge |
| Feasibility | Sample-amount/LOQ calculation; single-compartment versus same-family pools; realistic admission gates for analytical methods and repeated compatible division |
| Prospective simulation | Frozen protocols/configurations/seeds; positive, negative, weak and unqualified worlds; power/false-positive/coverage estimates with uncertainty; all failed and inconclusive conditions retained |
| Reproducibility | Tests before official runs, raw observations/decisions, snapshots/hashes, numerical replay, rendered figures and independent scientific/code audit |
| Delivery | Experiment specification, results report, source ledgers, executable laboratories, checks.md and accurate progress.md |

Success means these design and simulation deliverables are complete and verified. It does not require a positive scientific outcome. No simulation result will establish a qualified physical F1 assay, autonomous division, genetic inheritance or evolution.

## Implementation and evaluation boundaries

The previous chemistry model fails its prediction screen. Its fitted rates are not used as validated truth. The new simulations explore explicitly hypothetical reaction, retention, measurement and lineage scenarios while preserving source-grounded chemical identities and stoichiometry. They assess the information supplied by proposed experiments.

Assay work owns `assay/`; lineage work owns `lineage/` and consumes the shared assay interface. Research owns `research/assays/` and `research/lineage/`. Root owns integration, final experimental specification, verification and reporting. Independent review is read-only except its review evidence file.

Each worker records its protocol and configuration before its official campaign. Root reviews the protocols first. Development runs use distinct seeds. No parameter or criterion is changed to force an official positive result. Corrections preserve failed attempts and receive a new output version. Campaign sizes are fixed before execution using development runtime estimates; any unresolved physical qualification remains explicit.
