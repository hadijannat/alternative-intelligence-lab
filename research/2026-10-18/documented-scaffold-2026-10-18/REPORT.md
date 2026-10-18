# A documented replacement and bounded complementary-function tests

Phosphomolybdic acid, H3PMo12O40, is the selected replacement scaffold for this branch. Its experimentally demonstrated role is an **externally driven electron/proton buffer**. In the selected acidic assay, the operational states are principally [H2PMo12O40]- and [H4PMo12O40]-. This replaces an undocumented molecular anchor with a measured service and a tractable transport constraint. It does not establish an evolving or intelligent entity.

The user explicitly authorized this replacement on 2026-10-18. The exact-Mo34WV branch remains blocked historical work, with its sources, calculations and negative outcomes intact. No property of Mo36, W72V30 or Dawson clusters is assigned to Mo34WV. The relevant primary source is [Symes & Cronin 2013](https://doi.org/10.1038/nchem.1621), including its newly acquired 37-page official supplement. [SOURCES.md](<SOURCES.md>) maps conditions and claims to pages. The actual Claude Opus 5.5 consultation and primary-evidence audit are recorded separately in `consultation/`.

## Selection and chemical scope

PMo12 was selected because electron/proton storage, subsequent hydrogen production and electrode transport limits were demonstrated together. Mo36 is a stronger assembly-data comparator, but missing dose conversions and consumed holdouts prevent using those traces as new physical-rate validation. Dawson charge storage depends on concentration/counterions and can lose stored reducing equivalents on dilution. W72V30 stability spectra do not identify the active kinetics needed for these tests.

The experimentally demonstrated complement is the **electrode/proton-transfer environment**, including applied electrical drive, hydrogen/oxygen electrodes and a separator. The full device contains carbon-bearing components such as Nafion or cellulose membranes and, in some configurations, carbon electrodes. An inorganic mediator is not an experimentally demonstrated carbon-free living system.

## Frozen source comparisons

The protocol was written and hashed before these numerical fits. The figures had already been inspected, so all held-out evaluations below are **retrospective source-panel comparisons**, not fresh independent experiments. Twenty-nine plotted vector markers were extracted with reproducible affine axis calibration and finite plotting allowances. The dataset is figure digitization, not native raw data; individual experimental error bars and replicate covariance were not reconstructed.

| Test | Calibration and withheld outputs | Result | Interpretation |
|---|---|---|---|
| Finite kinetic/transport law | Six Fig4a Pt points at voltage magnitude <=1.8 V; two higher-voltage points withheld | RMSE **1.299 mA/cm2**, screening threshold 10 | Describes high-voltage saturation better than the chosen baseline within this condition |
| Kinetic-only exponential baseline | Identical six calibration points and two held points | RMSE **142.167 mA/cm2** | Retained failed extrapolation |
| Unchanged geometry transfer | Fig4a parameters fixed; all nine Fig5a Pt points | RMSE **125.870 mA/cm2** | Retained failure; larger mediator-side electrode changes cell behavior |
| One-time-constant GC response | GC outputs through 240 min used to fit; outputs at 360–600 min withheld; measured charge is prescribed input | RMSE **0.6055 percentage points**, threshold 0.3 | Failed late-time prediction; instantaneous baseline is better at **0.3410**, and also fails threshold |

The fitted effective limit is 110.398 mA/cm2, slope 4.536 V^-1 and midpoint 1.537 V. No fitted bound is active. The two held current predictions are 99.093 and 106.925 mA/cm2, versus plotted 100.9 and 106.6. The effective coefficient inferred from 0.25 M initial Red is 0.002288 cm/s. This is not a separately identified diffusion coefficient or membrane permeability.

The Fig5 mesh condition reaches 2.59 times the old limiting current. Its actual immersed mesh area is unavailable; the source supplies only mesh surface-density information. Consequently no numerical geometry correction was fitted to those test points. This failed transfer is evidence against universalizing the Fig4 parameters, not against the source experiment's observed improvement.

The fitted detector time is 73.75 min. A single response time misses the late catch-up by almost one percentage point at 360 min. The source attributes lag to the GC tubing. Neither the failed lag fit nor the slight negative plotted initial GC value is converted into slow mediator chemistry, material loss or an altered Faradaic efficiency. No revised observation model was tuned after examining this failure.

## Coupled finite inventory

The dynamic scenario tracks the source-grounded reactions:

`Ox + 2H+ + 2e- -> Red`

`Ox + H2O -> Red + 0.5 O2` during charging;

`Red -> Ox + H2` during discharge.

The illustrative reservoir is explicitly **1 mL at 0.5 M**, with 0.031 cm2 Pt normalization. The volume, 12-hour charging, 3-hour rest, 24-hour discharge and 12-hour recharge are scenario choices, not a reconstruction of the plotted experiment. Charging is prescribed external current and capped by inventory. During discharge, a fixed 1.7 V corrected-voltage scenario uses the fitted effective series flux with declining Red inventory. Extending that relation to depletion assumes first-order effective transport and omits the changing Nernst term, decomposition and competing electrode reactions. It is a conditional model, not validated depletion kinetics.

The 0.5 mmol inventory has 96.485 C of two-electron capacity. It delivers **0.49718 mmol H2 / 95.941 C** during the 24-hour discharge, leaving 0.00282 mmol Red. A rival that holds the initial current throughout would demand **1.56625 mmol H2**, over three times the available stock, and is rejected by conservation. Subsequent electrical recharge restores the redox state. It does not replace destroyed mediator.

The entire schedule accepts 192.427 C charging and rejects 75.413 C of additional requested charging at the inventory boundary. It ends with a fully charged reservoir; therefore its cumulative H2:O2 ratio must include reducing equivalents still stored at the end. Required absolute proton throughput is 2.98872 mmol. The model assumes a boundary capable of supplying that throughput; no measured membrane rate is inferred.

Mediator conservation has zero mol residual, bound-H2-equivalent bookkeeping closes within 1.1e-19 mol, and electron/charge balances close within 5.7e-14 C in the saved trajectory. The no-drive control explicitly disconnects the circuit. No-buffer and initially oxidized/no-charge controls produce zero **mediator-supported** H2. Initially reduced stock with discharge enabled produces bounded H2 without charging or concurrent O2, testing stored reducing equivalents. Direct water splitting outside this pathway is excluded from the model, not declared experimentally absent.

## Retained constraints and failures

The separate SI cycle condition contains 3.5 mL of 0.5 M mediator: nominal capacity 337.6975 C, first reduction 317 C (93.87%), fourth 308 C (91.21%). Fourth/first is 97.16%. This contradicts assuming full utilization and perfectly invariant throughput. It does not identify a molecular survival fraction or a transferable degradation constant.

The source also reports finite long-term charge loss, H2 permeability of cellulose and partial mediator reduction under H2 exposure. Carbon electrodes fail as oxygen-evolution electrodes in the tested arrangement. The source's energy penalty remains: approximately 86.7% relative efficiency from the three-electrode estimate and 79% for the separate two-electrode comparison. Corrected polarization voltages are not full terminal electrical work. A GC normalization ambiguity flagged by Claude remains unresolved without calibration records; the quoted Faradaic efficiencies remain source reports, not independently established constraints.

All failures are retained in [negative_results.json](<negative_results.json>), with full residuals, controls and output in [results/results.json](<results/results.json>). The earlier output with incomplete control coverage is retained as `results/initial_control_coverage.json`; independent review prompted an actual no-charge/discharge-enabled control and reduced-stock positive control, without changing fits or splits.

## What this changes for the broader goal

Claude Opus 5.5 Max recommends retaining PMo12 with this narrow scope. The consultation audit (dependency not included: `documented-scaffold-2026-10-18/consultation/AUDIT.md`) verifies its useful advice and rejects unsupported numerical interpretations of MS intensity, loss rates and proton transport. A separate light-driven PMo12/WO3 configuration was verified in primary literature as a later comparison, not folded into this model.

The project now has a documented scaffold and a testable charge-delivery/transport service, supported separately by the source's energy-conversion experiment. The improved finite transport law passes a narrow voltage extrapolation screen; transfer across electrode geometry and the proposed single-time-constant observation model fail. Balanced storage/recharge is possible in an ideal conditional model, but active-material renewal, functional inheritance, evolving variation, autonomous boundary maintenance and intelligence remain unestablished.

The next discriminating evidence is measured current versus actual mediator-side area, redox fraction and controlled hydrodynamics, with native charge/gas time series and known GC transfer response. A functional-inheritance claim would additionally require serial-transfer retention of a causal chemical function after removal of externally imposed state.

Reproduction and independent review are recorded in [checks.md](<checks.md>). The comparison figure is [results/comparisons.png](<results/comparisons.png>).

Subsequent goal continuation acquired a separate [photo-input package](<photo-complement/REPORT.md>) and the previously missing [Beta composition study](<renewal-lead/REPORT.md>). The latter supplies a new negative result for direct bulk-state copying. [The complete goal ledger](<CONTINUATION_LEDGER.md>) records why these component results leave renewal, inheritance and intelligence unachieved.

The later [GTM/STW follow-up and activation assessment](<cue-free-inheritance/REPORT.md>) preserves missing cue-free functional inheritance, weak function despite structural purity, thermal inactivation and active organic ligation. A GTM-4 depletion model passes a narrow retrospective screen; stationary untreated product branching fails. No additional integrated complement is admitted.
