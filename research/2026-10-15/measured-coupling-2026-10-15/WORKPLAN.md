# Measured chemistry coupling: active goal

Objective: develop simulations grounded in measured chemistry to test whether catalyst regeneration, compartment retention, and functional inheritance can work together under the same conditions.

Previous work classification: progress. The prior suite produced verified computational constructions and acquired component data. Its rates and copying rules were explicitly hypothetical, so it does not fulfill the present measured-chemistry objective.

## Completion requirements

1. Acquire and inspect primary numerical chemistry observations and associated experimental conditions, equations, units, controls, uncertainty and provenance. Prior descriptive summaries alone are insufficient.
2. Select at least one coherent common-condition chemical system. Keep incompatible buffers, temperatures, reactants and externally supplied procedures separate. Record whether each required process is observed, fitted, assumed, bounded or unidentifiable.
3. Implement coupled kinetic/transport/transfer simulations for regeneration, retention and functional composition. Infer admissible parameters from observations, evaluate held-out observations where available, and compare simpler kinetic models. Do not substitute investigator-selected values for missing measurements.
4. Test simultaneous operation, depletion, dilution/transfer, and functional lineage identity with matched controls, sensitivity bounds, explicit resource balance and founder carryover. If important parameters are unidentifiable, preserve a conditional envelope and demonstrate what prevents a unique conclusion.
5. Run tests, numerical convergence/conservation checks, fresh-process replay and independent scientific/code review. Produce traceable results, figures, report, checks and reproducible commands.

The objective is not satisfied by fitting a persistence curve alone or by attaching empirical lifetimes to the previous generic agent. A negative or insufficient-evidence scientific outcome is acceptable only after the coupled requested tests are implemented and their actual evidential coverage is audited.

## Work tracks

- Source acquisition: fueled autocatalyst/droplet system, exact kinetic/partition/retention observations and condition matching. Completed with missing active transport and inheritance retained.
- Independent source acquisition: RNA autocatalytic coacervates and temperature-cycled vesicle propagation, selecting complete common-condition data. Completed; coacervate rates excluded and vesicle observer distinguished from active catalyst.
- Models and integration: both branches implemented, fitted, challenged and replayed; independent review approved the bounded investigation. Completed. See checks.md and verification-v2/verification.json.

Allowed changes: this new directory plus a navigation link in the previous suite after a verified deliverable exists. Existing accepted simulations and raw evidence remain intact. Use the existing Python 3.12.3 scientific runtime. No paid computation, messages to authors, publishing or physical laboratory actions are authorized or needed for the current computational task.

Record any source access failure, model misspecification, changed fit or failed criterion. Scientific parameters and held-out splits will be frozen before main fitted-model evaluation. A date-stamped local protocol is not independent preregistration.
