# Bloor 2016 primary acquisition and constraints

Acquired 2026-10-18. Scope: documented PMo12 plus WO3 photocharging and subsequent electrochemical hydrogen production. No property is assigned to hypothetical Mo34WV. This package supplies evidence and constraints; it contains no fitted model or simulated result.

## Provenance and acquisition

Bloor et al., *Solar-Driven Water Oxidation and Decoupled Hydrogen Production Mediated by an Electron-Coupled-Proton Buffer*, JACS 138 (2016), 6707-6710, DOI [10.1021/jacs.6b03187](https://doi.org/10.1021/jacs.6b03187), PMCID PMC5033397.

- Article: [Glasgow author repository record](https://eprints.gla.ac.uk/119451/), which links the acquired [published PDF](https://eprints.gla.ac.uk/119451/7/119451.pdf). Saved as `sources/bloor2016.pdf`, 1,154,310 bytes, four pages, SHA256 `3f1224a42e7969b907bbd04efd95a90bf3005d8d884a71b0ea6bcafec444c077`.
- PMC article HTML and Europe PMC article XML are saved as `sources/pmc.html` and `sources/epmc.xml`. The HTML links supplement `ja6b03187_si_001.pdf`, validating its association with this article.
- SI: [Europe PMC supplementary-file endpoint](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5033397/supplementaryFiles) returned a ZIP, preserved as `sources/epmc-supplementary.zip`. Extracted only named member `ja6b03187_si_001.pdf` into `sources/bloor2016-si.pdf`: 395,523 bytes, 11 pages, SHA256 `ca05559d0a7e792e0416022f28ce966d12151c91e82e3e756a1c0751a64b72ab`.
- Text extractions: `sources/bloor2016.txt`, `sources/bloor2016-si.txt`, with PDF page markers. Rendered SI pages 5-8 are retained; pages 5 and 7 were visually checked against extracted numbers.
- `sources/download_receipt.json` records exact URLs, final URLs, HTTP status, content type, byte length, and hashes. It preserves failed routes and their response bytes. A 200 response containing HTML is recorded as failed rather than accepted as PDF.

Acquisition failures retained: web reader returned a PMC recaptcha screen and ACS article 403; requests to PMC's actual supplement link returned a download challenge HTML (HTTP 200); ACS SI returned HTTP 403; alternative PMC asset path and old NCBI OA endpoint returned 404. The Europe PMC package succeeded without bypassing the challenge. Search snippets were discovery aids; quantitative claims below were checked in downloaded primary PDFs.

## Chemical identity and observed coupling

The article uses H3PMo12O40 as oxidized material and H5PMo12O40 as two-electron-reduced material in its abstract; equations 1a/1b/2 use [PMo12O40]3-/5- and explicit electrons/protons. These are source bookkeeping representations, not a new experimentally resolved proton-location model. The authors obtain photocurrent with WO3 and PMo12 together at zero applied cell bias, then move the reduced PMo12 solution into an externally powered hydrogen-producing cell.

This extends Symes and Cronin 2013 (DOI 10.1038/nchem.1621): the reduction/water-oxidation step now receives light; the second step still requires electrochemical input. The +0.75 V versus Ag/AgCl working-electrode potential is **not** the full cell voltage. The article's rough energy calculation assumes 1.5 V across the second cell and cites Symes 2013; it does not measure that voltage-time integral in the 47 C experiment.

## Measured setup and endpoint constraints

| Quantity | Primary location | Constraint and qualification |
|---|---|---|
| PMo12 inventory | SI-2 S3; SI-6 S6-S7 | 25 mL of 0.5 M H3PMo12O40 in water: 0.0125 mol cluster inventory. |
| Acid compartment | SI-2 S3 | 25 mL of 1 M methanesulfonic acid; main article p6708 reports pH 0.1. |
| Photoanode | SI-2 S3 | WO3 on FTO, area 1 cm2. Literature preparation, not synthesized in this study's SI recipe. No quantitative film thickness/loading supplied here. |
| Charge-stage cathode | SI-2 S3; SI-6 S6 | Large-area carbon felt; dimensions/electroactive area not quantified. |
| Separator | SI-1/SI-2 S3 | Nafion N-117, 0.180 mm thick; exposed membrane area and permeability absent. |
| Resistance | SI-2 S3 | Approximately 14 ohm; plots uncompensated. Not an independently measured ion-selective transport coefficient. |
| Light | SI-2 S3; SI-3 S5 | Oriel 150 W simulator, AM1.5G, calibrated 100 mW/cm2 at 1 cm2 illuminated area. Incident optical power is 0.1 W; lamp electrical power is not the same system-boundary quantity. |
| Light switching | SI-2 S3-S4 | At zero bias: 30 s dark, 30 s light, repeated ten times. Sweep: 10 s dark/10 s light; bias and sweep rate depend on figure. |
| Atmosphere/stirring | SI-2 S3 | Sealed, oxygen-free, stirred; argon degassing for 20 min. Dark cathodic compartment. |
| Oxygen assay | SI-3 S4-S5 | Different Teflon/quartz-window setup with **Pt mesh counter electrode**; 1 cm2 WO3 working electrode; same stated solution volumes/concentrations. Do not treat its cathode as carbon felt. |
| O2 readings | SI-3 S5 | 60 min dark baseline, then 1 h illumination, 1 s readings, 12 mL total system headspace, two-point probe calibration 0 and 20.9% O2, 5% reading error. At least duplicate gas determinations. |
| O2 recovery | article p6709; SI-3 S5 | 84 +/- 6% Faradaic yield. Figure 4 has step changes from manually dislodging anode bubbles. This is not a direct loss-rate measurement. |
| H2 during photocharging | SI-4 S5-S6 | Neither chamber's headspace had detectable H2; detection threshold 0.04 vol%. Samples 50 microliters; typical total headspace ~12 mL. No detection does not mean exactly zero production. |
| Complete photocharge endpoint | SI-6 S6 | Overnight illumination, zero bias, total measured charge 47 C. Exact elapsed irradiation time and integrated optical energy are not given. |
| Subsequent discharge | SI-6 S6-S7 | Same 25 mL reduced PMo12; carbon felt working electrode; Ag/AgCl reference; Pt mesh counter in 25 mL 1 M acid; Nafion-separated, argon-degassed; 25 degC. |
| Discharge control | SI-6 S7 | Working electrode held +0.75 V vs reference until yellow color restored and current reached negligible background. Duration/current trace/full-cell voltage are absent. |
| Discharge endpoint | SI-6 S7 | 47 C recovered; burette 6.0 +/- 0.2 mL gas, GC identifies H2. Source uses molar volume 24 L/mol, giving 2.5e-4 mol measured vs 2.44e-4 mol from 47/(2F). |

Derived inventory constraint (using source F = 96485 C/mol): the two-electron capacity is 2412.125 C, so the 47 C endpoint accesses approximately 1.9485% of full inventory capacity. Thus this endpoint does not test near-depletion behavior. The source does not show complete reduction of all 12.5 mmol clusters. Ideal 47 C hydrogen volume is approximately 5.845 mL with its 24 L/mol convention, consistent with the stated burette uncertainty; the rounded central measured efficiency is slightly above 100%, so do not silently cap measured data to one.

## Energy accounting and source limitations

SI-7 S7-S8 is explicitly an estimate. It assumes average 1 mA/cm2 for a 1 cm2 electrode at 0.1 W/cm2: 100 C takes 100000 s and receives 10000 J solar input. Assumed 1.5 V discharge requires a further 150 J. For 100% charge-to-H2 yield and 286 kJ/mol higher heating value, the resulting H2 contains about 148 J combustion enthalpy; reported overall efficiency is about 1.5%. Pumps/compressors and other balance-of-plant are excluded. This is HHV output divided by mixed optical/electrical input, not a measured whole-cycle efficiency or Gibbs-work efficiency.

No measured 47 C cycle duration or full-cell discharge voltage trace is available in these PDFs. Its actual complete-cycle electrical-plus-light energy cannot be recovered uniquely. Assumption-based reconstructions must retain those labels. The separate O2 assay's 84% recovery cannot automatically be imposed as a 16% mediator charge loss in the carbon-felt 47 C cycle.

The SI S5 sentence describes the Faradaic-efficiency ratio in the inverse order (charge-predicted volume divided by measured volume), while its reported 84% value and the article figure are consistent with the conventional measured/predicted definition. Preserve this source wording inconsistency and use explicit formulas; do not encode the inverse ratio silently.

## Negative controls and remaining life functions

At zero applied bias, removing WO3 (bare FTO with PMo12), removing PMo12 (WO3-FTO with acid in both compartments), or turning off light produces little/no photocurrent at the main-figure scale. SI S2/S3 magnify the small control responses; source data should not be coerced to exact zeros. At higher applied biases these controls need not remain inactive. SI S4/S5 cover sweeps up to +1.5 V at 5 mV/s.

Observed restoration is an electrochemically driven return of the mediator's redox state, established by returned charge/color/current endpoint. It does not demonstrate repair of decomposed clusters, synthesis of replacement active material, autonomous maintenance, growth, reproduction, inherited function, selectable variation, or intelligence. Repeat chopped-light experiments establish short-term reproducibility, not indefinite cycling or self-renewal. This device includes carbon felt, methanesulfonic acid, Nafion and external instrumentation, so it is not a demonstrated carbon-free autonomous system. No compatibility with Mo34WV was tested.

The article p6710 says underlying datasets are available by contacting L.C.; no such contact was made. This package contains primary published figures and numerical endpoints, not the authors' raw time-series dataset. New figure-derived validation must declare digitization uncertainty and whether any data were already inspected. The 47 C/6.0 mL endpoint provides an independent charge-to-gas balance check relative to Symes 2013, but a parameter-free stoichiometric check is not kinetic validation.

## Figure 3 extraction feasibility and verification

Article PDF page 2 was rendered and visually inspected. Figure 3 is an embedded raster (PDF xref 246, 623 by 938 pixels, combined panels A/B), saved without resampling as `sources/figure3-native.png`. The 18 vector drawings on this page are page furniture/rules, not vector current samples; full inventory is `sources/figure3-inventory.json`. Panel A has readable 0-600 s and photocurrent axes and a clearly separated red current trace, so approximate digitization is feasible. It contains ten light pulses, small intra-pulse decline, and lower late pulse heights. Exact raw points, acquisition precision and replicate dispersion cannot be recovered. Black/blue controls at this scale overlap near zero and should instead be read from SI expansions if needed. No digitization or fit was performed for this acquisition task.

Verification invocation used Python requests/zipfile/PyMuPDF plus SHA256 recomputation over every receipt entry. Binary observable: every byte count and hash matches, and PDFs parse as 4 and 11 pages. Captured artifact: `sources/verification.json`; source/figure review artifacts are the retained PDF pages and native raster. This acquisition passes byte-integrity and source-association checks, while raw-series availability and measured full-cycle energy remain unresolved.
