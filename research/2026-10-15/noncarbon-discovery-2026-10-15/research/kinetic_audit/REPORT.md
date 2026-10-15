# Mo36 kinetic evidence audit for the proposed inorganic compound

15 October 2026. **The parent data support a checked descriptive forecasting reference. They do not constrain the proposed Mo/W/V derivative, background suppression, active catalyst retention, functional inheritance or intelligence.** The original chemical study has broader autocatalysis evidence than the six selected traces; this audit preserves that distinction.

## What the original study supports

Miras et al. report seed-associated lag removal, saturation and inhibition experiments for Mo36 assembly. They describe an uncatalyzed initiation pathway followed by autocatalytic amplification. Therefore spontaneous unseeded production is part of their proposed chemistry, rather than automatically a model defect. Their large-network stochastic model is phenomenological: templated reactions are assigned a tenfold acceleration, and an additional completion-dependent formation preference is needed to produce large clusters. Increasing every intermediate's stability preferentially accumulates smaller products. The proposed Mo36→Mo6 feedback mechanism was not experimentally resolved. [Original paper](https://doi.org/10.1073/pnas.1921536117), [retained author text](../pom/raw/miras2020.txt).

These results justify investigating seed-modulated inorganic assembly. They do not establish indefinite seed dependence, multiple transmissible functional states, dilution survival or carbon-independent intelligence. Seeded rate acceleration can coexist with eventual convergence to a common product distribution. A new derivative must demonstrate its own identity and function; a proposed substitution cannot inherit the parent observations.

## What was independently checked here

The freshly acquired author CSV is identical to the archived parent dataset: SHA256 `b9cfcb759f2140d61a7b21a984f3c5c761958d7d93ac9c815289596fae4520a7`. All 480 time, signal and seed-value triples match the repository's extracted observations. There are six conditions, 80 observations each, with seed labels 0.46296, 0.92593, 1.38889, 1.85184, 2.31480 and 3.19442. **None is an unseeded control.** [Pinned deposited data](https://github.com/croningp/clusterautocatalyticsets/blob/5c143e908367fa756a5bf6468b6bd46a92c7bcd0/Timeseries%20Data/Tidy_mo36_seeding_timeseries.csv).

The CSV does not declare physical units or independent preparation identifiers. Existing fitted columns `c.pred`, `c.pred.u` and `c.pred.l` are predictions, not additional observations. The parent descriptive package normalizes by the observed endpoint for visualization; the later forecasting package correctly excludes this endpoint normalization and those prediction columns. See the existing [published-model account](../../../metal-oxide/docs/published-model.md) and [measurement-provenance audit](../../../metal-oxide/published/calibration/data-provenance.json).

The existing calibration fits each seed condition independently. Its primary split trains on points 1–40 and forecasts 41–80; its earlier-cutoff stress split trains on 1–20 and forecasts 21–80. Time scaling, initial values and solver objectives use only the training prefix. Successful optimizer starts are selected by training SSE. Main and expanded numerical bounds are retained separately. All data had already been available before the analysis, so this is retrospective within-trace validation, not prospective validation or a held-out batch, seed dose or composition.

An independent standard-library implementation replayed the saved formulas without importing the fitting implementation. It reproduced all 7,680 saved point predictions exactly on this host, verified the phase labels and source measurements, recomputed all 96 sets of training/held-out metrics, and checked that all 72 nonlinear fits selected the successful start with minimum training SSE. Eight original manifest hashes matched. No existing result was modified. [Executable arithmetic audit](verify.py), [machine-readable receipt](checks.json).

The existing five tests also passed again in the package's existing environment. They include a held-out-response perturbation that changes scores without changing fitted parameters or forecasts, deterministic fitting, formulas, explicit failure retention and numerical degeneracy checks. This is a software isolation check; it cannot certify historical model-selection chronology or independence of future experiments. [Test receipt](test-receipt.txt).

## Forecast performance and retained negative results

The following are means over six conditions, in native signal units multiplied by 10⁻⁶. They are descriptive summaries with no inferred confidence interval.

| Description | Train 40, forecast 40 | Train 20, forecast 60 |
|---|---:|---:|
| Last observed value | 2.0667 | 5.4150 |
| Linear extrapolation from last ten training points | 1.3398 | 14.2543 |
| Single relaxation | 2.0215 | 4.3822 |
| Double relaxation | 1.3080 | 1.6246 |
| Offset logistic | 2.4269 | 5.0803 |

The two-component relaxation predicts these curve tails well, but its fast shape hits the main upper bound in 8 of 12 fits. All 24 logistic fits put the offset at the lower bound. Successful optimizer convergence (1,008 saved starts) does not identify chemical rate constants or a physical background concentration. Two relaxation terms also have exact degeneracies when one amplitude is zero or their shape parameters coincide. These negative identifiability results remain in the original outputs and the new receipt. [Original bounded report](../../../metal-oxide/published/calibration/report.md).

## Consequences for background amplification and inheritance

| Question | What this evidence permits | What it cannot decide |
|---|---|---|
| Does the known parent respond to seeds? | Original study's separate seeded and inhibited chemistry supports seed-modulated assembly. | The selected all-seeded table cannot independently re-estimate the zero-seed effect. |
| Is background amplification too strong? | A matched unseeded trajectory would supply a necessary comparison. | No zero-seed trajectory, transport coefficients or calibrated species balance occurs in this fitting subset. An adjustable curve offset is not a background reaction. |
| Does fitted seed dependence generalize? | Continuation of each observed seeded trace is tested. | No seed-value covariate or shared dose-response law is fitted; no unseen seed dose is forecast. |
| Is retained material still active? | Optical growth supplies a potential observation channel. | Identity-resolved retained catalyst and catalytic activity were not tracked through transfer. |
| Do descendants inherit function? | Nothing in this selected dataset directly tests this question. | There are no parent/descendant labels, common-environment transfers, variant functions or fresh-material lineage accounting. |
| Does the proposed Mo/W/V composition work? | The parent provides an experimental comparison target. | None of the 480 rows contains the proposed derivative. Its rates, transport and function remain unmeasured. |

The informative next dataset would couple independently prepared parent and derivative batches with matched unseeded controls, calibrated species-specific production and loss, retained activity, and transfers into a common environment. A model would then be fitted on designated preparation batches and tested on held-out batches and perturbations. Parent persistence, new production and transferred function must be scored separately. This describes missing evidence, not an executed experimental protocol or a successful result.

Skipped: a new optimization campaign, the original Julia network, derivative kinetics and wet experiments. Main risk: accurate curve extrapolation can be mistaken for a validated chemical mechanism or inherited function.
