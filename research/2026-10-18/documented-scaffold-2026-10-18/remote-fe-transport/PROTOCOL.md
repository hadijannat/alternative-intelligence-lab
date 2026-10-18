# Remote Fe transport and a vacancy-derived retention candidate

## Scope and exposure

The original Mo34WV-plus-complements objective and all 12 requirements remain unchanged. The preceding dissolution-observation turn made progress. The new Zhao2025 source supplies numerical membrane interventions and a separate Zn-derived precursor candidate; it does not supply origin-specific new-Fe function or integrated heredity.

This protocol is fixed after source/header/control audit and before numerical response extraction. Published qualitative contrasts, rounded claims and the source interpretation are known. Root knows AEM exposure is reported to worsen activity despite Fe enrichment. This is retrospective and paper-informed, not blind validation. The numerical source workbook and paired control curves have not been read for outcomes by root or the implementation worker. Preserve all results without changing thresholds, windows or model class after extraction.

Use the native XLSX linked to DOI10.1038/s41467-025-60728-y. Native headers/units and internal panel labels govern mapping; worksheet names alone are unreliable. Source DFT structures do not supply reaction rates. Initial composition inconsistencies, carbon-containing electrode assembly, unmatched counter-deposit loading, uncertain CA interfacial-potential correction and geometry/local-pH effects remain limitations.

## A. Reserved membrane-intervention screen

Extract native low-loading CA from sheet Fig1: AP:AQ single-cell, AR:AS AEM H-cell, AT:AU PEM/CEM H-cell. Time is minutes; current density is mA/cm2. Keep original row/cell provenance and missing values. Reject nonfinite pairs; retain duplicate times without inventing specimens. Do not interpolate beyond a curve's support.

Report five-minute-bin medians and each trace's 5–10min anchor and 295–300min endpoint (left closed, right open, final endpoint included). Normalize to its own positive anchor. Save window minima/maxima and midpoint/median ratios as descriptive within-trace envelopes, not experimental uncertainty or independent replicates. If required windows are unsupported, leave the result null rather than shift them.

All AEM post-10min function responses are reserved for the predefined directional screen; the AEM anchor is an explicitly supplied initial observation. No parameter is fitted to AEM or chosen from its endpoint. No permeability, Fe inventory or shared catalytic coefficient is calibrated from the separate counter-deposit experiment.

The simple exchange hypothesis has normalized Fe pools A(active), D(dissolved), X(inactive), C(counter-associated):

```
dA/dt = -kd*A + kr*D
dD/dt = kd*A - (kr+kp+kc)*D
dX/dt = kp*D
dC/dt = kc*D
```

For common nonnegative chemistry, identical starting pools and an AEM acting only to reduce kc, the cooperative A/D dynamics predict A_AEM >= A_CEM. This is a parameter-free conditional invariant. Comparing corrected function additionally assumes current proportional to A with a common coefficient. The lower-sink ordering is a source-motivated hypothesis, not independently calibrated low-loading membrane permeability. A directional contradiction rejects this combined model/observation/boundary hypothesis, not all metal exchange or every membrane mechanism.

Separately extract sheet FigS7's internally labeled FigS6 same-electrode CV control: SC A:B before/C:D after; CEM F:G before/H:I after; AEM K:L before/M:N after. Both before and after are measured in refreshed single-cell conditions. At fixed1.53V find every distinct piecewise-linear crossing of each curve, with no branch selected by activity. Retain all crossing currents, their min/max and nominal arithmetic mean. Compute after/before ratio bounds from extrema only when all denominators are positive. A secondary fixed1.55V check is a declared sensitivity, not another chance to choose a favorable result. No source current is reconstructed from TOF.

Test whether AEM function retention lies below CEM in both CA and the matched post-exposure assay; report overlap or disagreement. The source's Fe/Ni ratios are relative, depth-dependent observations and must not become absolute conserved Fe inventories. No statistical p-value is computed from correlated scan points.

## B. Minimal coupled-chemistry hypothesis

Test a possible inhibitor missing from the simple exchange model: coarse-grained A+D -> 2X. Add -ka*A*D to dA and dD and +2ka*A*D to dX. This counts Fe units but is not an established elementary reaction or uniquely selected mechanism. It tests whether competition/aggregation can reverse the simple retention prediction without violating finite mass conservation.

Use synthetic initial(A,D,X,C)=(1,0,0,0), kd=kr=1/h, kp=0.05/h, kc in{0,2}/h and ka in{0,0.1,1,10,100}/(normalized mass*h), over5h. Record every case, including no reversal. These rates are not fitted, transferred or claimed measured. Use positive analytic reaction substeps, with dt0.001h and a half-step convergence check. For ka0, verify the sink-order invariant over all sampled times. For every case verify nonnegative pools and A+D+X+C=1. Do not change the grid to obtain a desired sign. Do not label simulated X as a measured FeOOH amount.

## C. Candidate retention forecast

The named candidate is nominal [Ni0.75Fe0.25]0.6Zn0.4Clx, converted electrochemically to Zn-depleted Ni(Fe) oxyhydroxide. It is a precursor designation, not an exact final-cluster formula. Extract Fig3 H:I LDH, J:K NiFeCl and L:M NiFeZnCl: CV cycle versus reported activity retention in percent. Keep derived TOF out of the evaluator.

For each material, fix y0 to its first positive reported value at n0. Fit cycles<=40 and reserve every later cycle, provided there are at least3training and2reserved observations; otherwise report insufficient data without moving the split. These are temporal held-out points from each preparation, not an unseen candidate prediction or independent experimental replication.

Compare last-training-value carry-forward, irreversible first-order loss, and a two-state competence diagnostic:

```
loss:      y(n)=y0*exp(-k*(n-n0))
two-state: y(n)=y0*exp(-k*(n-n0))+b*(1-exp(-k*(n-n0)))
```

Use k=0 plus1001log-spaced values from1e-4 to10 per cycle, fixed before extraction. At each k, fit b analytically by constrained least squares with b>=0. For k0 set b=y0 and retain the constant prediction. Choose smallest training SSE, resolving exact ties by the earliest grid entry. This is the observable solution of active/inactive conversion at constant drive. k and b combine unresolved rates, initial competence and readout scale; the individual activation/deactivation rates and pool capacity are not identified. No candidate-dependent rate is predicted from DFT.

Save every fitted value, prediction and residual. Report training/reserved RMSE in percentage points, normalized RMSE divided by max(mean(abs(observed)),1percentage point), and maximum fractional error with the same1point denominator floor. The fixed operational screen is normalized RMSE<=0.10 and maximum fractional error<=0.20. It is not a chemistry-validation threshold. Preserve calibration failures, parameter boundaries, near-optimal parameter ranges, flat-baseline advantages and all reserved failures. No retry after outcomes.

## Verification and claim limits

Check native mapping and units; synthetic parser/fit recovery; k0/loss nesting; exclusion of reserved responses from fitting; branch-crossing handling; positivity, conservation, convergence and source/protocol/script hashes. Show experimental curves and reserved forecasts in a legible plot. Report source control successes as well as missing controls.

Only a source-condition retention role can be supported. Active repair, new-atom function, founder exclusion, serial inheritance, exact Mo34WV identity and same-system integration remain unproved. Carbon black/Nafion and external apparatus dependencies must be explicit. Do not add a verified integrated complement. Preserve prior source/model negatives and retain any failures here.
