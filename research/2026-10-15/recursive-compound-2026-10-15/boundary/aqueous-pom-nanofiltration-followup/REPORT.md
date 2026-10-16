# Aqueous POM nanofiltration: measured comparator and conditional consistency check

Status: retrospective source analysis; **zero new candidate roles, zero complement admissions, zero target validations**. The nominal Mo34WV compound was not tested. This is a polymer-membrane comparator for the existing retention problem, not a new all-inorganic complement. All 15 extracted table rows were inspected before analysis; none is a held-out set.

Primary source: Schidowski et al., *Investigations on the Recovery of Different Structure Types of Polyoxometalates from Aqueous Solution Using Nanofiltration Membranes*, ACS Omega 11 (2026), 23290-23301, [DOI 10.1021/acsomega.6c00086](https://doi.org/10.1021/acsomega.6c00086). The complete Europe PMC XML is archived at `raw/article.xml`, SHA256 `7fb77831963fcd4e25a5f62f454cbc8412525628f0e3286fa12f4f984b20f955`. Source access history is in `acquisition.json` and the root acquisition record. The subsequent successful supplementary acquisition extends the analysis to Tables S7/S8 and source discrepancies in S4-S6. The original main-only result remains unchanged in `main-table-results.json`.

## What the measurements constrain

The paper tests commercially supplied polymer membranes with a polypiperazine separation layer, a 33 cm2 active area, prewetting, ambient temperature, 100 mL aqueous feed, 15 mL/min pump flow, 32 bar, and 1100 rpm for Tables 1-3. Table 1 and Table 2 use 5 mM Lindqvist Na5[V3W3O19] and Anderson-Evans Na9[TeV3W3O24], respectively. Table 3 varies the Anderson-Evans concentration from 1 to 50 mM on TS-80. The archived extraction preserves every source cell, including anomalous text.

Table 1 reports W/V elemental rejection of 99/99% for TS-80, DK-Series and TS-40; 99/97% for XN-45; and 97/88% for UA60. Table 2 reports Te/W/V rejection of 98/99/99%, 85/99/99%, 81/99/99%, 62/99/99%, and 19/98/95%, in that membrane order. These are element-specific concentrations measured by ICP-OES. They establish a strong negative comparator: high W/V rejection can coexist with appreciable loss of another constituent.

The paper's Equation 1 is R_x = 1 - beta_x(permeate)/beta_x(feed). The denominator is the concentration of the same element in the feed, not the retentate. Equation 2 obtains permeate flux from collected permeate over time and active area, with conversion to L m^-2 h^-1. Flux and rejection do not determine an intrinsic membrane permeability without the driving forces, concentration profiles and boundary conditions.

Structural evidence is a separate arm. Figures 3, 4 and 6 specify **25 mM** for the corresponding before/after Raman and recovered-solid ATR-FTIR comparisons. The main text reports additional NMR comparisons in the supplement. For Anderson-Evans it reports recovered-solid Te/V/W 0.8/2.8/3 after the process and 0.8/2.8/3.0 before, and recognises Te leaching despite retained structural signatures. These spectra support retained recognizable structures in the measured samples; they do not quantify every molecule's integrity or a surviving catalytically competent fraction at each 5 mM table row. No target-specific catalytic turnover, seed-dependent propagation, functional inheritance, or autonomous maintenance is established here.

## Conditional arithmetic audit of Table 3

For an assumed feed molar ratio Te:V:W = 1:3:3, define q_x = 1 - R_x. Converting the element-specific mass concentrations to molar concentrations cancels atomic mass within each rejection. The predicted permeate ratio, normalized to W = 3, is then:

`Te/V/W = (q_Te/q_W) / (3*q_V/q_W) / 3`.

The main text gives feed 1/3/3 in its membrane-comparison discussion. Applying it to every concentration in Table 3 is an explicit conditional assumption, not an independently measured feed ratio for each arm. The source gives no rounding policy or uncertainties for these printed integers. We therefore test a hypothetical nearest-integer rounding envelope of +/-0.5 percentage point on every rejection. Closed endpoints conservatively include rounding ties. These are arithmetic envelopes, **not reported experimental error bars**. A secondary test also permits +/-0.5 unit on the printed Te and V ratio coefficients while retaining W=3 as the normalization convention.

| Feed mM | Te/W/V rejection % | Flux L m^-2 h^-1 | Printed Te/V/W | Central prediction | Allowed Te coefficient under rejection rounding | Joint compatibility |
|---:|---|---:|---|---|---|---|
| 1 | 90/98/96 | 232 | 38/5/3 | 5/6/3 | 3.8 to 7 | Excluded under both conditional tests |
| 5 | 96/99/99 | 210 | 11/3/3 | 4/3/3 | 7/3 to 9 | Excluded under both conditional tests |
| 10 | 97/99/99 | 198 | 7/3/3 | 3/3/3 | 5/3 to 7 | Not excluded; exact printed ratio only at a boundary |
| 25 | 96/99/99 | 173 | 4/3/3 | 4/3/3 | 7/3 to 9 | Not excluded |
| 50 | 98/99/99 | 147 | 3/3/3 | 2/3/3 | 1 to 5 | Not excluded |

The joint check intersects the W passage interval required by **both** Te and V ratios, rather than checking independent intervals with different denominators. At 10 mM the exact printed ratio requires q_W = 0.005 and q_Te = 0.035, touching both outer boundaries. This is weak compatibility with a conservative envelope, not positive validation. At 1 and 5 mM the separation remains even when ratio coefficients are also allowed to round by half a unit.

This result identifies a need for unrounded element concentrations, dilution factors, sample pairing, measured feed ratios and the composition-normalization procedure. It does not establish which number or interpretation is wrong, and is not a misconduct finding. Unspecified measurement error, different sample origins or a different normalization could invalidate the conditional assumptions. No entry has been repaired or discarded.

## Preserved ambiguities and negative results

- Table 3 prints V rejection 96% at 1 mM; the surrounding prose prints 97%.
- The Anderson-Evans discussion gives feed pH 4.5 and then pH 5. The exact feed pH for each table arm is not resolved here. The target's acidic operating conditions cannot be substituted into these results.
- Figure 6 names W15 in its Raman panel and experiment caption, but W16 in its ATR-FTIR panel.
- The Lindqvist 25 mM integrity paragraph refers to V and Te rejection, although its formula contains V and W and no Te. The Anderson-Evans comparison initially also describes V and Te as 99%, before discussing substantial Te loss.
- Table 2 TS-80 at 5 mM gives Te rejection 98% and flux 227; Table 3's nominally corresponding arm gives 96% and 210. The observations remain distinct; the source does not provide enough paired-run information here to pool them or infer uncertainty.
- A subsequent Lindqvist discussion gives flux endpoints 232 and 147, identical to the printed Anderson-Evans Table 3 endpoints. Supplementary Table S4 instead prints Lindqvist flux endpoints 245 and 149. The discrepancy is preserved; no table is silently substituted for the prose.
- The XML prints TS-80 pore radius as `0.36-45` using an en dash and embedded reference punctuation. It is retained as source text and is not interpreted as a calibrated radius or silently changed to 0.36-0.45 nm.
- Table 2's discussion reports additional permeate compositions (including TS-80 36/5/3). Those prose ratios have not been used to replace Table 3. The arithmetic audit is explicitly scoped to Table 3.

## Supplementary acquisition and uncertainty audit

The root acquired the supplementary archive from Europe PMC and extracted the 21-page `raw/ao6c00086_si_001.pdf` (1,917,706 bytes; SHA256 `2161f703c72a5bcf5412fa2654425adf4f31d6be7efde87f88661a283303aa96`). This analyst inspected the local text conversion, including Tables S1-S8; root separately checked the rendered S8 page. The extracted rows below come from `raw/supplement.txt`, whose hash is pinned in the extraction script. PDF text extraction is a separate step from the numerical computation; the script checks the PDF and text hashes before using either source.

Table S7 gives 10 observations for 5 mM Anderson-Evans on TS-80 (ambient, 100 mL water, 1100 rpm):

| Pressure bar | Pump mL/min | Te rejection % | W rejection % | V rejection % | Flux L m^-2 h^-1 |
|---:|---:|---:|---:|---:|---:|
| 32 | 10 | 97.3 | 99 | 99 | 182 |
| 32 | 12.5 | 97.2 | 99 | 99 | 179 |
| 32 | 15 | 98.2 | 99 | 99 | 185 |
| 32 | 17.5 | 98.3 | 99 | 99 | 195 |
| 32 | 20 | 98.1 | 99 | 99 | 191 |
| 15 | 15 | 99.2 | 99 | 99 | 103 |
| 20 | 15 | 99.1 | 99 | 99 | 133 |
| 25 | 15 | 98.9 | 99 | 99 | 163 |
| 30 | 15 | 98.7 | 99 | 99 | 190 |
| 35 | 15 | 98.6 | 99 | 99 | 195 |

Table S8 supplies three optimized-condition runs at 35 bar and 20 mL/min. Its caption gives no feed concentration; none is inferred from S7. W and V are censored as `>99`, and are not converted to exact 99 values.

| Run | Te rejection % | W rejection % | V rejection % | Flux L m^-2 h^-1 |
|---:|---:|---|---|---:|
| 1 | 99.1 | >99 | >99 | 260 |
| 2 | 98.7 | >99 | >99 | 273 |
| 3 | 98.9 | >99 | >99 | 265 |

From those printed values, mean Te rejection is 98.9%, sample SD 0.2 percentage point; this reproduces the reported value. Mean flux is 266 L m^-2 h^-1, sample variance is exactly 43, and sample SD is 6.55744 L m^-2 h^-1. The population SD is 5.35413; the standard error of the mean is 3.78594. The paper prints a flux **standard deviation of 4**, which does not reproduce using either SD convention on the printed values. Rounded SEM could give 4, but that numerical coincidence does not establish the authors' calculation. The reported uncertainty is quarantined from fitting or validation until unrounded runs and the calculation convention are available. This check addresses the printed data, not independently repeated experiments.

Additional supplementary ambiguities are retained: S4 labels the Lindqvist formula with only V/W but reports three-component permeate compositions identical to all five Anderson-Evans Table 3 ratios; the unspecified component order is not resolved by this analysis. S5 and S6 identify Keggin and Wells-Dawson structures in their titles but give Lindqvist Na5[V3W3O19] in both experimental footnotes. Those compositions and conflicting identity annotations are quarantined from chemical parameter fitting. No corrections or inferred identities are inserted into the source.

S1 lists supplier/literature membrane pH ranges, including TS-80 pH 1-12 and an isoelectric point of 2.5. These are material specifications, not evidence that the target stays intact and active at acidic pH. They also prevent transferring the paper's negatively charged-membrane explanation directly to the target's proposed pH near 1.7 without measuring membrane charge and target speciation in that environment.

## Consequences for a coupled chemistry-transport model

An element observation must be represented as a sum over chemically distinct species: C_x = sum_s(n_xs*c_s). Each species can have a different permeation flux, and the species inventory can change by reaction, association, adsorption or desorption during transport. A retained target and retained fragments can contribute the same bulk Mo/W/V totals. Elemental rejection alone therefore cannot identify the target's intact, active concentration or its seed dependence.

For the target, admission still requires paired feed/retentate/permeate molecular-identity measurements, element balances including membrane-associated material, and catalytic competence per retained intact target under a common operating protocol. A matched membrane-free control is needed to separate chemical decomposition from membrane-induced effects; an empty-membrane control tests wall contribution. Independent no-seed and carryover controls are required for inheritance. Conditions and pass criteria must be fixed before an untouched validation experiment. This paper constrains the need for those distinct observables; it supplies no justified Mo34WV transport or reaction-rate parameter.

Decision: retain TS-80 and the other polymers as conventional retention comparators, with Anderson-Evans constituent loss as a negative control case. Do not add the polymer to the all-inorganic complement set. Keep the inorganic confinement proposition open. No new simulation fit, synthesis, held-out validation or life/intelligence claim follows from this source.

## Reproduction

From the workspace root:

```sh
python3 -B recursive-compound-2026-10-15/boundary/aqueous-pom-nanofiltration-followup/extract_and_check.py
```

The script uses only the Python standard library, checks the acquired XML/PDF/text hashes, extracts 15 main-table and 13 supplementary rows, executes four mathematical self-checks and three statistical assertions, and writes `extracted-results.json` with exact rational interval endpoints and all assumptions. Successful exit proves extraction and conditional arithmetic only. The source tables and all negative or incompatible observations are retained.
