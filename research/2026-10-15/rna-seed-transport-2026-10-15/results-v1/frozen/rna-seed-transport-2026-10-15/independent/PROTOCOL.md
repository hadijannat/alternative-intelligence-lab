# Independent numerical verification

This check uses synthetic states only and performs no measured-data fitting. Its own transport implementation integrates every inside and exterior state with DOP853; it does not reuse the production analytic transport formulas or matrix exponential. Its own reaction right-hand side and event maps check short serial trajectories.

Before comparison, freeze these checks:

- Four nonuniform cohort weights; seven channels A, R, B, F, P, D and the passive competent-founder tag H. Compare empty and preloaded exteriors, volume ratios 1, 3 and 30, one and three FT units, and patch-exchange rates 0.001, 0.1 and 10.
- Check all species concentrations and weighted inside-plus-exterior inventories. The tracer anchor is 0.55 after three FT units from an empty exterior. Require concentration error at most 1e-9 micromolar and conservation error at most 1e-9 micromolar for these transport checks.
- Check zero duration, three successive one-unit FT events against one three-unit event without intervening washing, reuptake, isolated-patch inventories, and convergence toward the common bath as patch exchange increases.
- Independently reproduce three-generation finite-bath and finite-patch trajectories at seeds 0, 1 and 2 micromolar and all four fixed exterior sensitivities: reactive/inert by carried/discarded. Reactions are closed-membrane during warm incubation. All exterior chemistry, including activity decay, is frozen in the inert sensitivity. Exterior patches homogenize before warm chemistry. Serial feed halves prior intracellular cohort weights, adds A/R and B cohorts of weight 0.25 each, and halves exterior concentration in the carry case.
- Check every stage, new reporter production, washed intracellular PAGE, competence and founder tag. Require short-serial concentration error at most 1e-6 micromolar and PAGE error at most 1e-4 percentage points. These are numerical agreement tolerances, not physical adequacy criteria.
- The PAGE observer must leave the continuing culture unchanged. Chemical moieties exclude the duplicate founder tag. Check H <= F and exponential tag decay separately.

Retain the exact synthetic inputs, complete comparison rows, source hashes, run versions, and every check disposition in a new output directory. Refuse overwriting an existing output directory. Neither agreement nor conservation validates the physical transport closure.
