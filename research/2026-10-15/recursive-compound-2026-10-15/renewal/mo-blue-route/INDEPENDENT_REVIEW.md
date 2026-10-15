# Independent review of Mo-blue source constraints

**PASS for the scoped method constraints, with the sampling-side ambiguity recorded below.** This review inspected the original SI directly, including rendered PDF page8, extracted pages5,7–10, and independently checked arithmetic rather than rerunning root audit.py. It does not verify target renewal, inheritance, or original raw spectral measurements.

Source: JACS supplementary DOI10.1021/jacs.3c09344.s001, local raw/ja3c09344_si_001.pdf;8385595bytes;SHA256693c8723f09a0d9c4bb96131c60172f575c21c986047556637cbcdd2e53d64fa. PDF pagination equals the printed page numbers examined.

## Recipe arithmetic: confirmed, conditionally interpreted

Page8 visually prints15mL of1g/mL Na2MoO4, and1M H2SO4 additions3.90,4.68,6.25,10.90,12.50mL assigned c(H+)/c(Mo)=1.25,1.5,2,3.5,4 respectively. Text extraction is accurate for these quantities. The later Raman paragraph uses n(H+)/n(Mo); in a common solution volume the nominal ratio is the same, but neither expression establishes measured proton activity.

Taking15g sodium molybdate literally, oneMo per formula unit, and two nominal acid equivalents per H2SO4, the implied mass is M=r*15g/(2*V_acid[L]*1mol/L). Independently calculated rows are2403.846153846154,2403.846153846154,2400,2408.256880733945,2400g/mol. They agree with root analysis.json. Ordinary Na2MoO4 and its dihydrate cannot account for that scale. Therefore the printed recipe and nominal assignments remain unreconciled under the declared accounting; no typo, hydration state or corrected recipe is established.

Crucial limitation: c(H+) could be interpreted as equilibrium free proton concentration, and sulfate dissociation/molybdate protonation mean two nominal acid equivalents are not a measured free-H+ concentration. This audit establishes an internal nominal-stoichiometric consistency problem, not an independently measured pH contradiction. Retain root's explicit two-equivalent assumption.

## Raman scaling: confirmed

Pages8–9 describe Gaussian–Lorentzian subpeak fits, fixed peak positions/FWHM and R2 above0.99. Page9 sets each species' own maximum to100%. Thus the published relative profiles preserve within-species time dependence under that processing, but not a common concentration scale. Fit quality is not a cross-species Raman response calibration or proof of a unique species assignment. No such calibration is supplied in these methods. The profiles alone cannot be summed as concentrations or used to close a molybdenum mass balance. An independent two-sequence arithmetic check verifies that multiplying a species profile by10 leaves its own-max-normalized curve unchanged.

## Ex-situ ESI: confirmed with timing precision

Page9 specifies negative-ion ESI-TOF; selected samples stand no more than30min, then are diluted sample:acetonitrile1:39 and transferred to the source at400µL/h. The printed wording supports a bounded standing interval before dilution/transfer; it does not explicitly guarantee that every scan finishes within30min of sampling. Root's maximum_reported_delay_minutes=30 is acceptable only with that wording, not as a total acquisition-latency guarantee. The40-fold mixed-solvent dilution and ex-situ delay do not establish unperturbed operando solution identity. Mo36→Mo154 sample times0,280,2000,4000,6000s match root extraction. The separate sulfate route uses0,800,2000,4000s.

## Sampling side and apparatus

Page8 says the quartz Raman flow cell is connected to the anolyte; that same page defines the Mo assembly solutions as cathode electrolytes and again calls the chosen Raman solutions cathode electrolytes. Treat the literal anolyte wording as a source-method ambiguity; do not silently replace it with catholyte or claim a verified sampling location. The methods alone do not resolve the plumbing.

Page5 confirms carbon paper for both electrodes, Nafion115 membrane and IrO2-loaded area2cm×2cm for oxygen evolution. Pages7–8 confirm112mL/min externally pumped circulation,2.5mA/cm2 and4cm2 geometric area. The Raman loop separately gives100rpm, not a calibrated112mL/min loop flow. Neither carbon-free apparatus nor autonomous energy supply follows. Source Mo36→Mo154 and sulfate route→Mo102 are distinct transformations, not preservation/repair of nominal Mo34WV.

No new scientific fit, operator, candidate role, physical experiment or source correction was introduced. Root code/results were read only. The primary source discrepancy and sampling-side ambiguity remain unresolved.
