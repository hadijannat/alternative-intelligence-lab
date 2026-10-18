# WO3 photo-input complement: support and limits

The newly acquired [Bloor et al. 2016 article and supplement](https://doi.org/10.1021/jacs.6b03187) support light-driven charging of PMo12 followed by electrically driven hydrogen release. This is **component support for energy input**, not an autonomous maintained system and not evidence about Mo34WV. [SOURCE_NOTES.md](SOURCE_NOTES.md) identifies the actual cells and measured versus assumed quantities.

The SI-6 experiment uses 25 mL of 0.5 M mediator, a WO3/FTO photoanode, carbon-felt cathode, methanesulfonic acid and Nafion. After overnight illumination at zero cell bias, 47 C was passed. The same reduced mediator solution was then transferred into a separate electrically driven cell and reoxidized, delivering 47 C and 6.0 +/-0.2 mL H2. The second stage is not a zero-input reaction.

## Executed source-consistency checks

Using the source conventions F=96485 C/mol and 24 L/mol gas volume, 47 C predicts **5.84547 mL H2**, within the reported 5.8–6.2 mL interval. The rounded central measured/predicted ratio is **1.0264**, with burette-only ratio allowance0.0342; it was not clipped to100%. This is a parameter-free stoichiometric consistency check on already-inspected endpoints, not a fresh chemical prediction or fitted rate.

The nominal inventory has **2412.125 C** of two-electron capacity. The experiment accesses only **1.94849%**. It therefore does not validate near-depletion transport, full active inventory utilization, or repeated complete stock renewal. A202-row ideal charge-coordinate trajectory tracks Ox/Red and gas equivalents; maximum Decimal charge residual is1e-26 C. Its coordinate is fraction of the stated charge endpoint, not elapsed time. Oxygen equivalents are formal stoichiometric predictions, not observed O2 from this cycle.

Reproducing SI-7's explicitly assumed100 C example gives10000 J incident sunlight,150 J electrical release input at assumed1.5 V across the full discharge cell, and148.210 J hydrogen HHV, or **1.46019% HHV/input**. Average1 mA and the1.5 V cell voltage are estimation assumptions. No actual whole-cycle voltage/current/light integral for the47 C experiment is available. +0.75 V versus Ag/AgCl is a working-electrode potential, not the discharge cell voltage. Pumps, degassing, compression and lamp wall-plug losses remain outside the quoted estimate.

## Negative results and admission decision

- **Do not merge the oxygen assay with the charge/release cell.** SI-3 uses a Pt-mesh counterelectrode, while SI-6 photocharging uses carbon felt. The reported84 +/-6% O2 recovery and bubble-release steps cannot be assigned as16% mediator loss in the47 C cycle. The SI's ratio wording is also inverted relative to the conventional measured/predicted interpretation; this inconsistency remains recorded.
- **No full-capacity validation.** A two-percent charge excursion does not test depletion or high-dose behavior.
- **No zero-input complete cycle.** Hydrogen release still receives electrical input.
- **No new-material renewal or inheritance.** Returning charge and color restore a redox state; no newly synthesized competent mediator or transmitted functional variant is measured.
- **No demonstrated organic-free organization.** Carbon felt, organic acid and Nafion are operational source dependencies. An acid/electrode substitution requires its own compatibility evidence.

Decision: WO3/FTO plus its source device is **component-supported for photocharging PMo12**. It is not admitted as a verified integrated life complement. The full R/H/J requirements remain open, as does exact Mo34WV identity. Numerical results, including missing measurements as null, are retained in [results/analysis.json](results/analysis.json).
