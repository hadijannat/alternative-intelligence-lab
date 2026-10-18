# Remote Fe transport: methods and controls

Primary evidence: [Zhao et al. 2025](https://doi.org/10.1038/s41467-025-60728-y), acquired native main, 27-page SI, 32-page peer-review file and numerical source workbook. Exact acquisition and hashes are in `ACQUISITION.md` and `sources/acquisition-checks.json`. No response values were extracted or models fitted in this audit.

## Candidate and experimental boundary

The new proposed modifier is the **nominal chloride precatalyst [Ni0.75Fe0.25]0.6Zn0.4Clx**, followed by electrochemical conversion to a Zn-depleted Ni(Fe) oxyhydroxide. The formula describes a precursor composition, not a structurally identified fixed-stoichiometry final molecule. The source proposes that leaching creates cation vacancies which accommodate Fe. Its DFT models represent selected vacancy arrangements; they do not independently determine macroscopic capture/release rate constants.

The electrode inks contain acetylene black and Nafion, and routine tests use glassy carbon. Carbon paper and titanium felt occur in distinct assays. These are functional electrode assemblies, not a demonstrated carbon-free autonomous system or an established complement compatible with Mo34WV.

Preserve two preparation inconsistencies: the methods specify a **4:1 NiCl2:FeCl3 solution** while naming Ni0.75Fe0.25 material (nominal 3:1), and one loading paragraph reverses the LDH subscripts to Ni0.25Fe0.75. Do not silently choose either conflicting composition for exact chemical modeling. The named comparison and source-data headers consistently identify the Ni0.75Fe0.25-LDH family.

## Controls and measurement conditions

| Feature | Native source method | Consequence for modeling |
|---|---|---|
| Cell comparison | Single chamber (SC), H-cell with Alkymer W-25 AEM, H-cell with Nafion 212 described as PEM/CEM | Membrane chemistry and cell geometry change together; a pure Fe-permeability intervention is not established |
| Medium | O2-saturated 1 M KOH, ambient temperature; initial pH 14.00 ±0.01 | Initial pH is measured; spatial/time-resolved pH during CA is not supplied |
| Volumes | Approximately 20 mL SC and 30 mL HC | Not matched solution volume; HC allocation between compartments and exact transport distances are not specified in the acquired methods |
| Routine electrode | Glassy carbon area 0.196 cm², 10 µL deposited ink; LDH loadings 6.5 or 65 µgNiFe/cm² | Low/high loading are distinct inventories; mass is Ni+Fe basis, not total LDH mass |
| Counter/reference | Platinum plate 1×2 cm²; Hg/HgO reference calibrated versus RHE | Counter deposition affects the whole apparatus, not just an isolated catalyst |
| Activation/program | Ten CVs, 1.225–1.575 V_RHE at 10 mV/s; CA at 1.53 V_RHE for five hours in the main comparison | Activation creates the starting state; current retention after activation is not a damage-and-repair challenge |
| Ohmic correction | Fresh OCP EIS before each experiment; high-frequency intercept; E_corrected=E_measured−iR | Paper reports CA at 1.53 V_RHE and says all potentials are iR corrected, but does not specify real-time feedback versus subsequent correction for the CA command. Constant corrected interfacial potential throughout CA cannot be assumed. SI mentions ~5.1 Ω for selected CV corrections |
| Post-exposure matched assay | **Same working electrode**, stable initial CV in SC, CA in assigned geometry, then CV again in SC with refreshed electrolyte; SI Fig. 6 and peer-review pp12–13,18–19 | This is a useful control for persistent catalyst change and immediate electrolyte/bubble effects. It does not erase differences in exposure history or identify Fe-origin-specific function |
| Counter-deposit assay | 50 µL of 2 mg/mL LDH ink on 1×1 cm² carbon paper (100 µgLDH/cm²); after each five-hour CA, counter soaked in 10 mL 1 M HNO3 for one hour; ICP-MS | Different substrate/loading from low-loading GC CA. Acid extract ppb is collected counter material, not a direct instantaneous transport flux or a complete Fe balance |
| Surface/bulk composition | SEM-EDS/XPS contrasted with ICP-MS after acid dissolution | Different sampling depths/assays; total Fe enrichment is not an independently counted active-site population |
| Turnover frequency | Current divided by a site estimate from Ni2+/Ni3+ redox charge and nominal Fe/Ni ratio | Derived from current; cannot serve as independent validation of current or origin-resolved Fe activity |

The transparent peer-review file explicitly discusses OH− transport, local electrolyte composition and bubble artifacts. The authors added the same-cell, refreshed-electrolyte pre/post CV control in response. Preserve this positive control evidence; saying the paper has no attempt to address membrane confounding would be incorrect. Electrode distance, membrane area/thickness under operation, agitation, full Fe mass recovery and a calibrated Fe permeability coefficient are not established by the present method descriptions.

## Source workbook mapping before response extraction

`sources/workbook-structure.json` is the authoritative header inventory. Workbook dimensions are declared extents, not counts of independent observations.

| Potential analysis | Sheet/columns and headers | Suitable scope |
|---|---|---|
| Low-loading CA comparison | `Fig1`: AP:AQ SC; AR:AS HC/AEM; AT:AU HC/PEM. Row 3 Time/current density, row 4 **minutes** and **mA/cm²** | Strongest direct response traces for an explicitly retrospective cross-condition observation test |
| CV history | `Fig1` A:L SC and N:Y HC/AEM, low/high loading, cycles 10/50/100 | Potential–current curves; normalization and branch handling require a frozen protocol |
| Counter Fe/Ni | `Fig2` N:Z, CA Time (h), Fe/Ni SC, HC/PEM and HC/AEM, ppb and error bars | Separate loading/substrate assay; do not combine with low-loading CA as one measured mass balance |
| Zn-derived candidate retention | `Fig3` H:M, CV cycles and activity retention (%), LDH/NiFeCl/NiFeZnCl | Tests activity retention under repeated CV; no direct supplied-metal replacement or inheritance readout |
| Candidate TOF/composition | `Fig3` O:S derived TOF/error bars; AB:AF Fe/Ni ratios by SEM-EDS/ICP-MS | Related observations, with explicit dependence and sampling differences |
| High-loading CA | Sheet **`FigS5`**, internal label **Fig S4**, A:D Time(min)/Activity retention(%) for SC and HC/AEM | Potential reserved loading challenge after resolving normalized-response semantics |
| Same-cell pre/post CA control | Sheet **`FigS7`**, internally **Fig S6b/c/d**: SC A:B before/C:D after; CEM F:G before/H:I after; AEM K:L before/M:N after. Row 3 E−IR vs RHE/current density; row 4 V/mA/cm²; row 5 Before CA/After CA | Stronger independently measured functional comparison under refreshed matched SC conditions; CV branches and specimen pairing still need a frozen evaluation rule |

There are material numbering inconsistencies. Sheet `FigS4` internally labels Fig S3 and contains CVs; sheet `FigS5` internally labels Fig S4 and contains high-loading CA. Sheet `FigS12` internally labels Fig S11 but contains dopant dissolution. Main Fig. 1 caption exchanges c/d meanings relative to main text and workbook headers (peak shifts versus retention). Map by panel content, units and conditions rather than sheet name alone. **Preserved audit correction:** an initial check of sheet names alone found no `FigS6` and prematurely described the matched control's numerical block as unidentified. Examination of every sheet's internal labels established that `FigS7` contains all three paired pre/post control blocks. The numerical control is available and should not be counted as missing.

Main Fig. 1 error bars are described as standard deviations of at least three independent measurements. That does not make the many points along a single CA trace independent replicates. The workbook's visible headers contain summary error bars; full replicate-level provenance and instrument exports are not established.

## Oxygen labels, repair and origin

The isotope experiment labels **oxygen**, using H2(18)O during a separate 0.1 M KOH exposure, rinsing with H2(16)O, then measuring evolved oxygen in ordinary KOH. It uses titanium felt at 1.5 mg/cm² and different potentials/programs from the low-loading CA comparison. It is evidence about oxygen participation, **not labeling of founder versus incoming Fe**. Isotope-independent transfer of Fe between electrodes, Fe accumulation and DFT capture energies do not establish which material supplies functional catalytic current.

The source is stronger than current-only evidence because it combines membrane interventions, same-cell post assays and counter deposition. It still does not supply a measured founder-function ceiling, labeled new-metal catalytic contribution, selective founder removal, or serial functional descendants. Zn removal is a precursor-conversion strategy; persistent current or Fe capture alone cannot establish active repair after damage.

## Recommended frozen-test boundary

A bounded retrospective test can use the three raw CA blocks after freezing time units, calibration interval, reserved conditions/times, conventional baselines and treatment of dependence. The source can falsify an observation model's prediction of current retention. It cannot uniquely identify Fe capture/release kinetics or prove repair through fitting current. Treat the Zn-derived precursor as a candidate for separately tested catalyst retention, and retain every failed baseline, composition ambiguity, mapping correction and unsupported origin claim.
