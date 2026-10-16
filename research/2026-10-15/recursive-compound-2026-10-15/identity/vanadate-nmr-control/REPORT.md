# Vanadate NMR control: measured comparator, no target identity

[Pettersson et al. (1985)](https://actachemscand.ki.ku.dk/pdf/acta_vol_39a_p0499-0506.pdf), DOI 10.3891/acta.chem.scand.39a-0499, studied vanadate by 51V NMR and potentiometry at 25 C in 0.6 M Na(Cl). Table 1, printed p501, gives eight monomer fractions at total V 0.3125 mM and three existing equilibrium-model predictions. Root visually transcribed every column into observations.csv. These are published summaries, not raw instrument data.

The acidity coordinate is minus log hydrogen-ion concentration, not an independently established activity-pH scale. Figure 1 spectra have equal maximum intensity; their plotted heights cannot supply cross-sample concentrations. Samples were prepared separately, with NMR before emf on each sample. The authors estimate monomer-fraction uncertainty at most three percentage units and note underestimation of small areas. Their discussion leaves neutral H3VO4 unestablished but not definitively excluded. No Mo/W-containing target was measured.

Original analysis: analysis.py reports residuals for all three printed models, without fitting or using a holdout. Counts inside the authors' rough three-unit estimate are descriptive, not confidence tests. Raw spectra, calibrated recovery and replicate distributions are unavailable here. No parameter is transferred to Mo34WV.

| Printed model | Maximum absolute residual, percentage points | Rows within three units |
|---|---:|---:|
| No neutral monomer | 3 | 8/8 |
| Neutral monomer log beta 11.72 | 24 | 0/8 |
| Neutral monomer log beta 11.00 | 5 | 1/8 |

All residuals, including unfavorable models, remain in analysis.json. Six arithmetic/invalid-input self-checks passed. This reproduces a table comparison; it is neither a new equilibrium fit nor experimental replication.

Original assay consequence: add vanadium-only controls at the target's actual acidity, ionic medium, concentration, aging time and analytical processing. Quantify free/condensed vanadate and intact mixed-cluster identity together, with recovery and catalytic-competence measurements. A changing 51V signal alone cannot establish V incorporation, active retention or inheritance. This refines the existing identity requirement; zero new roles or complements are admitted. Aggregate remains 24/0.
