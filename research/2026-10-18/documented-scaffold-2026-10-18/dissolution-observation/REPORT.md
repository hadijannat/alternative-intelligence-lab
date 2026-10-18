# Better metal-loss measurements still do not establish active renewal

The remaining dissolution-control lead is now acquired as a native nine-page article and DOCX supplement. It improves the measurement design for the NiFe renewal proposal, but does not identify newly active material or justify adding a verified complement to Mo34WV. The full 12-function objective remains active and unachieved.

## New primary evidence

Da Silva, Igel and Cherevko, [*Setting the Record Straight: A Systematic Study on Fe and Ni Dissolution in NiFe-Based Oxygen Evolution Reaction Catalysts*](https://doi.org/10.1021/acscatal.6c01228), ACS Catalysis16,8633–8641 (2026). [Acquisition](ACQUISITION.md) records the two native files, byte hashes, live browser download links and preserved failed routes. The live DOCX attachment differs from Crossref's registered PDF-supplement route. No raw instrument export or separate raw deposit was located; the acquired supplement contains ten images and one composition table.

The source compares electrodeposited NiFe oxyhydroxides, FeOOH/NiOOH references and commercial NiFe-LDH. Online non-detection is followed by accumulation measurements that reveal Fe entering the sampled electrolyte while beginning/end electrode performance changes little under a mild 1mA/cm2 protocol. This supports a loss-observation method. It does not establish damage repair, origin-specific catalysis or unchanged material inventory. Naturally abundant Fe56/Ni60 detector channels are not atom-origin labels.

## What the native methods resolve

[The methods audit](SOURCE_AUDIT.md) verifies approximately50mL total electrolyte, five-minute OCP sampling at1,2,3,6h, and a reservoir returned to the cell during recirculation. A separate electrolyte stream supplies the analyzer baseline between samples. A return of the detector trace to baseline is therefore not evidence that the electrode's liquid inventory has become zero.

The main article reports flow approximately3.2microlitres/s; the SI reports approximately3.5. The source does not fully specify mixed circulating volume, dead volume, top-up, or the conversion from sampled concentration to cumulative loss. Figure6's aligned axes are converted forms of one measurement, not independent mass and concentration assays; its panel c repeats the NiFe curve from panel a. Tick-only calibration gives an amount/concentration factor about8.3% below an exact50mL/0.02835cm2 conversion. That is an unresolved mapping difference, not proof of an erroneous experiment or a measured45.85mL reservoir.

Daily calibration, matched-matrix baseline, reaction-gas interference suppression and matrix-dependent dilution are described. Numeric blank distributions, accumulation-specific detection limits, recoveries and censoring rules are not supplied. An online detection limit is not a zero-dissolution constraint, and its transfer across matrices or sampling modes is not established. The acidic internal-standard stream also prevents treating elemental ICP-MS signal alone as particle-resolved speciation.

## Executed transport and measurement test

[The frozen protocol](PROTOCOL.md) avoids fitting unidentified chemical rates. Root and reviewers had already seen rounded source endpoints; no blind or held-out chemical validation is claimed. The test uses finite synthetic pools, an arbitrary constant source during polarization, zero source during OCP as an explicit scenario, and separate liquid-stock/exported-mass bookkeeping. No repair, redeposition or incoming metal is present in this null.

[The implementation](test_measurement.py) and [results](results/measurement.json) compare unreplenished and clean-replenished well-mixed50mL scenarios with a complete-reset comparison. All12 numerical checks pass, including conservation, finite exhaustion, analytic withdrawal, scaling and separation of wall time from polarization time. Maximum conservation residual is1.78e-15 normalized mass units.

After six polarization hours, six arbitrary mass units have left the solid:

| Flow, microlitres/s | Sampling assumption | Remaining liquid mass, units | Collected mass, units |
|---:|---|---:|---:|
|3.2|Unreplenished50mL start|5.7634|0.2366|
|3.2|Continuous clean replacement|5.7754|0.2246|
|3.5|Unreplenished50mL start|5.7406|0.2594|
|3.5|Continuous clean replacement|5.7549|0.2451|
|Either nominal flow|Assumed complete reset|0|6|

A five-minute window transports0.96–1.05mL. In the first unreplenished50mL window that removes1.92–2.10% of liquid mass; concentration stays unchanged under ideal mixing. Complete reset requires a different, assumed full50mL removal/refill per window, independent of nominal flow. These are conditional predictions, not estimates of what the experiment actually did. The hypothetical50microlitre sensitivity is explicitly not the native stated volume. The synthetic cases remain conditional calculations; plotting them or reporting a fitted score would not supply experimental validation.

This changes the next action: resolve the sample-to-stock/export operator and blanks before extracting a dissolution rate. Treating every sampled packet as a fresh independent interval, or summing liquid-stock readings as exported mass, is unsupported. This source's mild-current observations do not calibrate the earlier300/800mA/cm2 failures.

## Chemical and functional limits

[The chemistry audit](CHEMISTRY_AUDIT.md) confirms the native ferrate equation contains `0.059/3`; a flattened-text coefficient suspicion was rejected. Atom/charge bookkeeping and the source's rounded onset potentials agree for Eq.S5. A separate unbalanced Reaction30 line is preserved as a transcription inconsistency, without attributing the source's calculations to that typo.

Even perfect net-loss measurements do not uniquely split gross dissolution from recapture: adding the same admissible flux to both leaves their difference unchanged. Additional fluxes require independent measurements and finite inventory bounds. Similarly, retained current cannot assign catalytic competence to newly supplied atoms. The source supplies no matched damaged-founder supply/withdrawal comparison, selective new-material function, founder functional ceiling or serial functional descendants. Its nominal cast mass is not a catalytic-capacity bound.

NiFe remains a documented inorganic OER component under alkaline source conditions. The graphite counter is recorded as external apparatus; it is not by itself a reason to reject an inorganic active mechanism. There is still no same-medium identity/persistence or coupled renewal evidence for Mo34WV or the PMo12 branch. No rate or stability property is transferred between those preparations.

## Recursive disposition

Retain accumulation plus explicit sampling balance as a better assay proposal. Reject complete-reset and zero-loss inferences that are not supported by the observation operator. Leave gross cycling, active repair, functional inheritance and integration unresolved. No verified integrated complement is added; all earlier negatives remain intact.

The concrete next requirement is a matched source package containing liquid volumes/top-up, raw concentration and electrochemical traces, blank/recovery distributions, electrode inventories and origin-resolved function or a valid founder-capacity ceiling. Further curve fitting to the consumed figures cannot supply those missing observations. This step is progress through new native evidence, executed measurement checks and a changed inference decision; it is not completion of the full goal.
