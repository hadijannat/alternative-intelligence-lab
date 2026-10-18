# Native extraction and frozen tests

Invocation: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/remote-fe-transport/analyze.py` from the repository root. The final execution completed with process exit 0 and saved `results/execution.log`. Exit 0 means artifacts were emitted; **one numerical convergence diagnostic is false**. The script does not convert scientific failures into software exceptions.

The worker read the fixed protocol before native response extraction. Qualitative published contrasts were already known. This is retrospective, with no prospective or independent-specimen validation. `data/native_cells.json` preserves each selected worksheet, header, original row, cell address, x/y value and validity flag. Interior missing rows would be retained and excluded from numeric operations; no missing or nonnumeric rows occur in the selected CA/candidate blocks. CV crossings never bridge an invalid row. The source XLSX, protocol, script and extracted data SHA256 values are stored in `results/analysis.json`; `results/artifact_hashes.json` hashes the numerical results, raw extracted cells, plot and saved trajectories.

## A. Membrane comparison

CA mapping is Fig1 AP:AQ (SC), AR:AS (AEM), AT:AU (CEM/PEM). Time units are minutes and current density mA/cm². All bins use native sample membership, no interpolation. Every bin saves contributing row numbers, observed minima/maxima/median/midpoint, sample count and time bounds. Ratios use a positive 5–10 minute anchor; envelope ratios enumerate the four endpoint/anchor extrema combinations. These are within-trace envelopes, not confidence intervals or independent measurements.

| Condition | Anchor samples | Anchor median | End-window samples | Observed end-window median | Median ratio | Extrema ratio envelope |
|---|---:|---:|---:|---:|---:|---:|
| SC | 300 | 1.866645 | 301 | 1.578450 | 0.845608 | 0.821979–0.944203 |
| AEM | 30 | 1.854795 | 30 | 0.301360 | 0.162476 | 0.152576–0.171454 |
| CEM | 60 | 1.846160 | 60 | 1.351730 | 0.732185 | 0.710528–0.764778 |

**Coverage negative:** AEM stops at 299.83333 minutes and CEM at 299.91667 minutes. Both have native samples in [295,300], but neither covers the exact 300-minute edge. Accordingly `strict_full_edge_retention` is null for both; the table reports only `observed_window_retention`. No manufactured endpoint or shifted window repairs the strict screen. SC includes an out-of-order final workbook row 18005, AP=300 and AQ=1.72858, after the earlier chronological sequence reaches 301.53027 minutes. That row is retained in raw provenance and the final window. Its elevated value broadens the SC envelope. There are no duplicate times in these three blocks. The initial SC 0–5-minute bin also has partial support because SC starts at 1.54773 minutes; every bin records support.

The observed AEM/CEM envelopes are disjoint in the direction opposite to a model that treats a lower counter-electrode sink as the only AEM change while maintaining common current-per-active-pool competence. However, the strict whole-window CA screen remains incomplete. The independent paired control below provides a separate conditional test.

CV mapping uses FigS7, internally labeled Fig S6, in refreshed single-cell conditions before and after exposure. SC A:B/C:D; CEM F:G/H:I; AEM K:L/M:N. Native units are E−IR versus RHE in V and current density in mA/cm². Each pre/post curve has two distinct crossings at each target. Every crossing saves its original bracketing row pair and four cell addresses. No branch was selected according to its activity. The nominal ratio divides the arithmetic mean of all after crossings by the corresponding before mean; the bounds span all cross-combinations. The shared result schema calls this representative value `median`, but each crossing summary explicitly labels it as an arithmetic mean.

| Potential | SC after/before | CEM after/before | AEM after/before |
|---|---|---|---|
| 1.53 V | 0.849557 [0.818241, 0.881972] | 1.266341 [1.262522, 1.270177] | 0.400723 [0.381951, 0.420186] |
| 1.55 V sensitivity | 0.860347 [0.856974, 0.863735] | 1.281433 [1.279028, 1.283840] | 0.432359 [0.428622, 0.436142] |

At both fixed potentials all AEM retention bounds lie below all CEM bounds. CEM's post-assay increase contrasts with its declining CA current, reinforcing that different readout/exposure conditions cannot be silently treated as one calibrated active-Fe inventory. These controls constrain the combined simple chemistry/transport/readout hypothesis, not all exchange mechanisms. No Fe/Ni ratio was converted into an absolute inventory, no counter-deposit assay supplied a fitted rate, and no TOF reconstruction supplied a current value.

## B. Synthetic coupled chemistry

The exact frozen ten scenarios were run with ka=0,0.1,1,10,100 and kc=0,2, other parameters and initial pools unchanged. Symmetric positive analytic reaction substeps use dt=0.001 h and dt=0.0005 h. Both complete trajectories are saved in `results/synthetic_trajectories.npz`. The mass error across both runs is 1.27e−14 and the minimum pool is zero. The ka=0 lower-sink ordering holds over every saved time at both resolutions.

| ka | Low-sink minus high-sink active pool at 5 h | Minimum coarse difference over 0–5 h | Time of minimum (h) |
|---:|---:|---:|---:|
| 0 | 0.408769 | 0 | 0 |
| 0.1 | 0.328087 | 0 | 0 |
| 1 | 0.111493 | −3.86e−13 | 0.001 |
| 10 | 0.012224 | −0.0251332 | 0.835 |
| 100 | 0.000932 | −0.00681856 | 1.015 |

Thus aggregation permits a transient ordering reversal for ka=10 and 100, but **none of the five ka pairs reverses the ordering at five hours**. No transient time was promoted into a new endpoint success criterion. The ka=1 tiny negative value is numerical, smaller than the observed step discrepancy. Fine-step minima for ka=10/100 are −0.02513308/−0.00681776. Their signs and amplitudes survive the specified halving, although no step comparison is a rigorous global numerical error bound.

The implementation added a 1e−5 absolute convergence diagnostic (the protocol specified a halving comparison without a numerical tolerance). It **fails** for both ka=100 scenarios: maximum all-time/all-pool differences are 1.08729e−5 and 1.15277e−5. The other eight are below 9.0e−7. All coarse/fine values and the false check remain saved. No tolerance, dt, reaction grid or chemical model was changed to obtain a pass. This limits any precision claim; it does not turn the frozen endpoint negative into a positive result.

The added A+D→2X term is a coarse-grained loss of two Fe units into an inactive pool. It is not an identified elementary reaction, fitted rate, measured FeOOH mass or validated explanation of these electrodes. Transient structural possibility and the five-hour failure both remain in the record.

## C. Candidate forecast fails the data-count gate

Fig3 H:I, J:K and L:M each provide cycles **20,30,50,70,80,100,150,200**. Therefore each material has only **two training observations at cycles≤40**, versus the frozen requirement of at least three. All have six reserved rows. The script emits `insufficient_data`, an empty fits object and all native values for LDH, NiFeCl and NiFeZnCl. It does not fit either kinetic model or the carry-forward forecast, shift the cutoff or substitute qualitative retention for held-out model validation.

At cycle 200, native reported retention values are 35.69157%, 103.0303% and 101.2285%, respectively. These are descriptive source observations. The Zn precursor does not exceed the NiFeCl comparator at that endpoint. Distinct compositions, activation pathways, uncertainty and source normalizations remain relevant; this single observation is not proof that either precursor is generally superior or performs active repair.

## Verification and preserved execution failures

`results/analysis.json` records 11 passing implementation/invariant checks and the failed convergence diagnostic. Tests cover invalid-row gaps, both CV branches, positive denominator requirements, exact synthetic on-grid two-state recovery, reserved-response exclusion, k=0, loss nesting, source units, nonnegative pools, mass conservation and the ka=0 sink-order invariant. Candidate fit primitives are tested with synthetic data; no fitted candidate validation is claimed.

The first invocation failed before native extraction because a synthetic integer y0 generated an integer division-output buffer. Explicit float dtype corrected that implementation bug. The next invocation reached the convergence diagnostic and stopped on its 1e−5 assertion. The final code preserves the diagnostic as false while emitting all results; it did not change the threshold or scientific parameters. These execution failures are retained here rather than omitted from the run history.

`results/observations.png` was visually inspected: all four panels, units, legends and scientific limitations are legible. It shows native bin medians, branch-inclusive paired CV ratios, raw candidate observations with the unfulfilled training gate, and full synthetic ordering trajectories. It contains no invented candidate forecasts. Active repair, origin-specific new-metal function, inheritance and Mo34WV compatibility are not established.
