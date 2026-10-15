# Energy transduction and maintained regeneration

2026-10-15. **Four carbon-free active-material candidates evaluated; zero additions to a verified joint system.** The nominal [MoVI34WVI VVO112(H2O)16]9− target has no established solution identity or operating window. Its existence, functional regeneration and energy coupling remain unverified. Acquired component data and exact bookkeeping do not establish noncarbon life or intelligence. External energy is permitted and necessary for sustained nonequilibrium function; the unmet criterion is demonstrated coupling to target maintenance, not the presence of an external supply.

Scope is the missing energy/regeneration function only. Files were added only under this energy directory; earlier laboratories were read without modification. No wet experiment, paid computation or publishing occurred. [Candidates](candidates.json) retain the sequence, failed criterion and next step for each alternative.

## Sequential alternatives

| Step | Formula and role | Directly supported conditions/observation | Failure against the target; next alternative |
|---|---|---|---|
| 1 | WO3·H2O / HxWO3·H2O: proton/electron reservoir and catalytic interface | Spencer et al.: 0.5 M H2SO4, H2-purged electrode system, imposed electrical drive. Monohydrate reaches reported x≈0.69 in its tested window; interpolated HER overpotential 501.0 mV at 10 mA cm−2. Temperature unresolved in inspected methods. | Carbon-free oxide, but electrode construction uses carbon/Nafion. No shared Mo36 or target assay, autonomous recharge, or renewed inherited function. Storage can be consumed in HER. Next: soluble Dawson reservoir to test whether a separately characterized large charge store supplies the missing role. |
| 2 | Li6[P2W18O62]: soluble multi-electron reservoir | Chen et al.: concentrated aqueous lithium salt, externally electrochemically reduced; up to 18 e−/anion under reported concentration-dependent conditions. UV–vis follows a separate 10 mM 0–12 e− experiment; these endpoints must not be combined. | Dilution-driven H2 evolution consumes stored reducing equivalents. No common target medium, measured target transfer, or maintained recharging. Next: PMo12, whose complete electrically driven buffer cycle is directly demonstrated. |
| 3 | H3PMo12O40 / [PMo12O40]3−: electron-coupled proton buffer | Symes & Cronin: 0.5 M buffer, pH≈0.3, externally driven two-stage electrolysis; reference benchmark 100 mA cm−2. Source potentials already use NHE. | The complete cycle consumes external electrical input. Membranes/electrodes include carbon-containing implementations. No transfer to Mo36 at pH≈1.7, much less the unknown derivative. Next: CeO2, which offers a different, thermal energy source. |
| 4 | CeO2 / CeO2−δ: thermal water-splitting cycle | Arribas et al.: nine cycles in three tests, externally irradiated solid in Ar/steam at 1 bar. Thermocouple maxima 990–1280°C and pyrometer maxima 1305–1760°C disagree substantially; neither is silently chosen as the true sample temperature. | A maintained external heat/gas cycle is demonstrated at component scale. It has no same aqueous medium with Mo36. A hot/cold interface, gas delivery and useful target coupling would be additional unverified components. Next: shared-medium PMo12/Mo36 measurements, conditional on first establishing the target identity. |

Primary sources: [Spencer 2024](https://doi.org/10.1039/D4SC00102H), [Chen 2022](https://doi.org/10.1021/jacs.1c10584), [Symes 2013](https://doi.org/10.1038/nchem.1621), [Arribas 2018](https://doi.org/10.3390/en11092451). Each is standalone component evidence. Failure here means failure of the joint-evidence criterion, not chemical impossibility. Neither oxide doping nor choosing a bigger reservoir fixes the missing energy path by itself.

## New quantitative evidence

The new [nine-row transcription](ceria_cycles.csv) comes from Arribas Tables 2–3, checked visually against retained [page 8](raw/ceria2018-table2.png) and [page 13](raw/ceria2018-table3.png). Test 1 cycle 1 uses oxidation-only 3.10 mL, rather than whole-cycle 4.78 mL. Volume uncertainty is reported as ±1.01 mL; no covariance or distribution is assumed. [Executed arithmetic](.omo/evidence/checks.json) verifies all nine power×time sums and rounded cycle efficiencies.

| Test | Total incident energy (J) | Total reported H2 HHV (J) | Recalculated 100×ΣHHV/Σenergy (%) | Source test column (%) |
|---|---:|---:|---:|---:|
| 1 | 535005 | 53.03 | 0.0099121 | 0.025 |
| 2 | 419715 | 48.17 | 0.0114768 | 0.036 |
| 3 | 645435 | 60.36 | 0.0093518 | 0.028 |

The source test column equals the sum of rounded cycle percentages, not the aggregate energy ratio. These are apparatus-specific central-value calculations, not uncertainty bounds or intrinsic limits on ceria. Raw sensor traces were not reanalysed. The temperature discrepancy and large volume errors preclude a precise kinetic fit.

The independently acquired 2010 ceria [supporting material](raw/chueh2010_si.pdf) further identifies a porous material made using starch/graphite poreformers and an externally operated high-flux reactor. That preparation history prevents calling the demonstrated entire process carbon-free solely from CeO2's formula; it does not prove residual carbon in the operating oxide. Its efficiency convention includes a sweep-gas term and differs from the 2018 table, so efficiencies are not pooled. [Primary SI](https://authors.library.caltech.edu/records/1b3yx-yz883)

For PMo12, the source benchmark gives charging 2.17−0.46=1.71 V and discharge-stage electrolysis 0.85−(−0.38)=1.23 V. Equal two-electron throughput makes the sum 2.94 equivalent V, versus 2.55 V for the source direct-electrolysis comparator: 86.73% relative energy efficiency, or 15.29% more electrical energy. This reproduces the authors’ estimate from separate half-cell comparisons at the same benchmark current density: 0.5 M 50:50 oxidized/reduced buffer versus a 1 M H3PO4 comparator, with platinum electrodes and author-reported NHE potentials. It is not an integrated full-cell energy measurement, a potential conversion, or a target energy prediction. Returning the mediator's oxidation state does not erase the electrical work supplied in both stages. [Source pp.404–405](https://www.chem.gla.ac.uk/cronin/images/pubs/251.SymesNatureChem_sDKDy5D.pdf)

## Conservation constraints reused without upgrading their scope

Both earlier runners were inspected and executed directly, with outputs saved here. They write stdout only, leaving old artifacts unchanged.

- [Finite occupancy replay](.omo/evidence/capacity-replay.json): 63 hypothetical initial states, 252 allocations, 180 feasible allocations and 72 rejected allocations; 180 full algebraic reversals. For the registered idealized HWO3 endpoint, `2 rMn + rCe ≤ W_empty`; `2 MnII + CeIII + W5` is invariant. Fully occupied tungsten cannot accept additional forward charge. Reversal undoes the corresponding formal Mn/Ce oxidation. This is exact inventory algebra, not an accessible phase diagram or proof of repair. The measured monohydrate x≈0.69 is **not** substituted into this older hypothetical network.
- [Counterion replay](.omo/evidence/counterion-replay.json): all 24 stipulated cases and 72 voltage decompositions pass. At 297.45 K and pH 7/8/9→1.7, equal-counterion neutral-pair transfer terms are 30.18/35.88/41.57 kJ mol−1 H+. Electrical terms cancel for the complete H+/Cl− pair or H+/Na+ exchange. These are conditional activity-gradient terms, not measured pumping costs or an actual interface. No counterion activity, temperature or pH is imported into the candidate data above.

More generally, internal transfers cancel when summing a reservoir inventory: over an interval, charge consumed in useful reactions plus loss cannot exceed initial stored charge plus externally supplied reducing equivalents. Cyclic restoration of *all* reservoirs therefore needs counted input whenever useful reduced products or losses leave. This is a conservation statement, not a fitted rate law; oxidizing water, photons, chemical feed or an electrical circuit must be explicitly represented if used as input. Neither balanced stoichiometry nor a source of hydrogen establishes a pathway that maintains the target structure and function.

## Next measurement and admissible computation

First establish target identity and oxidation/site assignments in solution. Before that, a known Mo36 + PMo12 comparator is interpretable only as a comparator. The next decisive measurement is species-resolved cluster survival/new formation and mediator charge turnover in **one specified solvent, pH, ionic composition, temperature and oxygen condition**, alongside the complete external energy/charge and product balance. Measure whether mediator cycling supports new functional material rather than merely reducing, dissolving or equilibrating it. No safe transferable electrode window follows from these papers.

Once same-medium charge, concentrations, products and independently measured uncertainty are available, the next admissible computation is a measured charge/material balance with propagated uncertainty and zero-input controls. Do not assign interfacial transfer rates, fit a regenerative model to separate-medium curves, or count retained founder material as regenerated material.

Evidence scope and exact invocations are recorded in [.omo/evidence/verification.json](.omo/evidence/verification.json); primary URLs and current file SHA256 hashes are in [source_ledger.json](source_ledger.json). No verified joint-system member was added; the original life/intelligence goal remains unmet.

Skipped: wet measurements, electronic-structure calculations and fitted coupling kinetics. Main risk: the nominal target may not exist, and useful coupling may consume or erase the state intended for maintenance.
