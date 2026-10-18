# Dissolution observation: measurement and transport test

The full Mo34WV-plus-complements objective and its 12-function contract remain unchanged. The preceding Fe-site turn made progress, but did not identify repaired material. This step tests whether the next primary source supplies a defensible metal-loss observation operator before using it to select a renewal mechanism.

## Exposure and frozen scope

The native main article and DOCX SI for DOI 10.1021/acscatal.6c01228 have been acquired. Root and the advice/review agents saw qualitative conclusions and rounded six-hour amounts in source text before this protocol. No numerical response curve is digitized, no response split is claimed blind, and no chemical rate is fitted here. Missing circulating volume, mixing, sampling statistic and top-up semantics prevent an identified kinetic fit. A retrospective forecast of the plotted observable would not supply the missing renewal attribution, so it is not used as evidence of a better material.

The independently documented inputs are the main-text flow 3.2 microlitres/s, SI outlet flow approximately 3.5 microlitres/s, five-minute sampling windows at nominal hours 1, 2, 3 and 6, geometric electrode area 0.02835 cm2, and approximately 50 mL total electrolyte. The last number is not automatically the well-mixed recirculating volume. Main Figure 1 shows a reservoir returning liquid during recirculation and draining toward ICP-MS during sampling. Native Figure 6 dual-axis tick conversion will be audited separately without fitting response values.

## Conditional models and computations

Use normalized mass units and hours. These simulations test measurement assumptions, not the observed chemistry. Set initial dissolved mass and collected mass to zero. During each polarization interval inject one normalized unit per hour from a finite solid pool of 10 units into liquid. There is no redeposition, new-metal supply or active repair in this null. Source strength is arbitrary and linear; it is not estimated from the source. Between intervals, set source to zero for the five-minute OCP window, explicitly as an unverified scenario.

For each of the two documented flow values, compute three sampling operators:

1. No replenishment: conditionally start with 50 mL well-mixed liquid. During sampling withdraw q*300 seconds, leave concentration unchanged, and track decreasing volume and collected mass.
2. Clean replenishment: conditionally keep 50 mL fixed by continuous matched clean inflow during sampling. The liquid inventory decays by exp(-q*300/V); collect the removed mass. This is an alternative assumption, not a documented experimental top-up.
3. Complete reset: remove all liquid metal after each sampling window. Track it in collected mass so conservation is not lost. This is a separate comparison operator, not justified by nominal flow and volume.

Apply each window after operating durations [1, 1, 1, 3] hours. The five-minute sampling periods add wall time; they do not add polarization time. Save pre/post-sample liquid inventories, volumes, concentrations and exported mass at every window. A hypothetical 50 microlitre fixed-volume mixing case may be calculated only as a unit/topology sensitivity; the native text actually says 50 mL.

Self-check finite nonnegative pools and total solid+liquid+collected mass conservation, exact zero-flow/zero-source limits, agreement with analytic withdrawal formulas, linear scaling with source, and unchanged final input/protocol hashes. Check that nominal five-minute outflow cannot be called complete replacement of a well-mixed 50 mL reservoir. No arbitrary pass threshold, posterior probability, calibration/validation score or held-out chemical prediction is assigned to these synthetic results.

## Inference and decisions

Concentration times assumed volume is a liquid stock; integrated q*c is exported mass. They are distinct operators, and earlier collected metal must be accounted before interpreting net recovery. Detector dilution, electrolyte-matched blanks and an unspecified limit of detection must not become a zero-dissolution observation. Net release does not identify gross dissolution or redeposition: adding the same nonnegative flux to both leaves the net balance unchanged within admitted inventories. It also does not identify origin-specific catalytic activity.

Use the new source only to strengthen a net-loss measurement design or reject an unsupported inference. Do not add a verified complement, transfer rates to another preparation/medium, extrapolate 6 h mild-current behavior to the earlier 300/800 mA/cm2 failures, or replace any previous negative result. A fitted repair model remains pending genuinely discriminating observations, not successful execution of this transport calculation.

Completion of this step requires source/package audit, executed conservation checks, machine-readable negative results, independent interpretation review and an updated full-goal ledger. Full-goal completion remains unproved.
