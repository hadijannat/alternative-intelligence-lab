# Regeneration controls: frozen numerical protocol

Task: audit the481 acquired Poli2025 files for matched metal-supply controls and test whether a chemistry-grounded model distinguishes active new-material repair from retained-founder activity. Output is this folder; native sources and every previous negative result remain unchanged. Completion requires a complete inventory, source/control map, executed test with failures, independent review, report, checks and handoff. No publication or new synthesis is included.

## Exposure and scope

Frozen before reading numerical raw potential/current traces or processed endpoints. The paper's rounded outcomes and previous source-level summaries are already known. This is a retrospective, paper-informed forecast, not blinded experimental validation. Agents inspected filenames, acquisition headers, times, row counts and Origin printable labels, not numerical response traces.

All481 files are inventoried and hash checked. DTA fragments are acquisition segments, not independent specimens. The acquired subset contains ten specimen folders, no qualified complete same-condition replicates, and unresolved exact raw-specimen-to-Fe plot assignments. Main Fe-lean/nominal100ppb/5ppm × pulse/no-pulse comparisons are separate wires with different starting feeds. No matched preloaded-founder supply-withdrawal experiment is assumed. Fe-lean is not zero Fe, and5ppm nominal Fe precipitates. The SI-only Zn→Fe same-wire control has no identified raw entry in the deposit.

Numeric analysis uses native OER tables and their own specimen identifiers; it does not assign Fe doses by response, filename sort or best fit. All6×6 cross-panel dose assignments remain possible for a strict raw-level comparison. Commercial Fig2a raw/published specimen-name discrepancy is retained.800mA has different current, geometry and feed; it is a separate stress case.

## Fixed observations, split and evaluator

1. Parse native Gamry data, including comma decimals and misnamed plaintext.xls. Keep original units/columns. Confirm monotone native time and current compliance; exclude regeneration transients from OER voltage summaries. Never infer current from a nominal header area.
2. For continuous OER records, use medians in the final300s of each complete6000s OER interval. For loop records, use the same last300s within each native OER block. No interpolation, filling of missing blocks or processed-tail substitution. Retain partial records/gaps as limitations.
3. Use cumulative **OER exposure** for the primary clock, with actual nonnegative native pulse durations inserted between observed OER blocks. Absolute wall-clock gaps are reported separately; they are not silently assigned to known chemical phases. Anchor each specimen at the median raw potential during0.5–1h of its first OER exposure. No reserved offsets are fitted.
4. Fit complete summaries at OER exposure≤24h. Forecast summaries after24h without refitting. Entire specimens and pulses are not randomized into point-wise folds. This is within-specimen extrapolation, weaker than independent specimen validation.
5. Primary screen: reserved RMSE≤0.050V and maximum absolute error≤0.100V, both required. These are analyst operational tolerances, not confidence limits. Report RMSE/MAE/max error per specimen, no sampling CIs from autocorrelated points. Equal-weight each interval. Also compare a constant prediction equal to the final training summary.
6. Analyze raw instrument-reference potential **changes relative to each specimen's anchor**. These are uncorrected electrochemical voltage observations, not isolated kinetic overpotentials. No unsupported RHE conversion or iR subtraction is made; unknown time-dependent resistance/bubbles remain confounders. Compare processed files with raw values only as a provenance check, retaining offsets/scales and unsupported tail rows.

## Conserved competence model

Use a minimal finite competence pool with active fraction x and inactive fraction1−x, x∈[0,1]. At the anchor x=1. During OER, `dx/dt=−d*x`; during a measured pulse, `dx/dt=r*(1−x)`. Both exact updates preserve nonnegativity and total normalized competence. This is an effective catalytic-state model, not a measured Fe atom inventory or closed electrolyte balance.

At fixed current, parallel catalytic contributions with a common Tafel slope give the conditional observation law

`DeltaE = b*[log(1+g)−log(1+g*x)]`.

Here g is an uncalibrated initial Fe-associated activity gain relative to host activity, and b is a conditional natural-log voltage slope. Resistance and changing morphology are not identified by this law. Primary b=0.040V; sensitivity b=0.020 and0.080V. Report all three, never select b against reserved outcomes. No transfer of the previous nickel-felt/Han rates or isotope calibration is allowed.

- M0 passive interruption: r=0; OER losses pause during pulses.
- M1 reversible competence restoration: r≥0 during pulses. It represents a more explicit active/inactive chemical state than survival alone, but could describe founder reactivation or material replacement.
- Flat baseline: final training value carried forward.

Fit g,d on61-point log grids: g10^-3…10^8, d10^-5…10h^-1. For pulse runs M1 adds41 positive r values10^-4…10^3h^-1 plus exact r=0, nesting M0. Minimize training squared error only. Coarse-grid rates are representative effective parameters; boundary/near-optimal multiplicity is retained, no precision or physical identifiability claim. Nonpulse M1 equals M0. No new mechanism/parameter range is added in response to reserved failures.

## Origin-discrimination test

Construct two mechanistic interpretations with the same conserved active/inactive states and observation law: activation of retained founders versus activation supplied by new material. Voltage observes total competence, not atom origin. Explicitly verify identical predicted traces under both interpretations at the fitted parameters. Separately construct a closed active/buried/liquid metal-pool counterexample with founder/new origin labels, conserved elemental inventory and shared kinetics; relabeling origin while holding summed pools fixed must preserve voltage. These are mathematical identifiability tests, not evidence that either interpretation actually occurs.

Passing a forecast only supports the conditional total-activity law. Distinguishing new competent repair requires an origin-resolved functional measurement or quantitative maximum founder contribution. Relative SIMS profiles on separate sacrificed wires cannot supply this bound. No isotope function, Faradaic efficiency, total energy balance, heredity or integrated-life credit is inferred.

## Required checks and preservation

Check parser columns/units/row counts, source hashes and missing/empty files; validate aggregation with a known synthetic pulse record. Check exact limiting cases, positivity/conservation, no-loss/no-restoration controls, M0 nesting in M1, synthetic parameter-grid recovery, no reserved observations in fitting, and origin-equivalent predictions. Preserve parser/model failures and all source contradictions. Save figures, machine-readable results and independent review. Do not tune after reserved outcomes.
