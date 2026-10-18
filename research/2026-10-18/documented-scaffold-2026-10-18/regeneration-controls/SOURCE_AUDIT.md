# Poli 2025: source audit for metal supply and repair attribution

Audited 2026-10-18 against the locally acquired primary article XML, supplementary PDF/text, Dataverse metadata, acquisition receipt and selected native headers. This audit does not extract, fit or evaluate electrochemical curves. Author-reported outcomes are distinguished from new numerical findings. The source is the same Poli dataset already acquired; it is not an independent replication or a new candidate.

Primary identifiers: [article, DOI 10.1039/D5GC00114E](https://doi.org/10.1039/D5GC00114E); [dataset, DOI 10.34894/XW7RK6](https://doi.org/10.34894/XW7RK6). Local source root throughout this note: `../founder-repair-search/sources/repair/poli2025/`.

## Audit conclusion

There are matched *nominal metal-supply and pulse-policy* comparisons: iron-lean, added 100 ppb Fe and added 5 ppm Fe, each with and without regeneration, at 300 mA/cm². They are separate-wire experiments, not an isotope-resolved founder-to-descendant or old-to-new-material experiment. A separate pair uses 120 ppb added Fe at 800 mA/cm². An additional same-wire sequential Zn-then-Fe addition control is documented in SI Figure S19; its raw curve is absent from the acquired 481 files and no S19/Zn-labelled file was found among all 638 deposit metadata entries.

This dataset can test whether a model captures Fe-supply-dependent maintenance of electrochemical performance. It cannot by itself determine how much activity comes from newly supplied Fe rather than retained, rearranged or recycled initial metal. There is no isotopic time-of-entry tag, calibrated active-site inventory, initial-founder catalytic upper bound, or intervention that selectively removes old active material while keeping the new material functional. The nickel wire itself persists. Even a successful reserved-curve prediction would establish predictive adequacy under those conditions, not active repair beyond retained founders.

## Verified acquisition boundary

The local receipt contains **481 files, 55,239,493 bytes**. A fresh read-only pass rehashed every local byte array against both its receipt SHA256 and its matching repository checksum in the 638-entry metadata. Observable: **481 present, zero size/hash mismatches**. Formats: 467 DTA, 6 TXT, 3 XLS, 1 XLSX, 4 OPJU. File count is not experiment count: the potentiostat emits separate files for alternating OER and regeneration steps.

The 481 files cover:

| Deposit grouping | Files | Meaning |
| --- | ---: | --- |
| Fig. 2a | 94 | Commercial KOH pulse/no-pulse comparison and Origin project |
| Fig. 3a | 16 | Three metal-supply arms without regeneration and Origin project |
| Fig. 3b | 274 | Three metal-supply arms with regeneration and Origin project |
| Fig. 6b | 96 | High-current pulse/no-pulse comparison and Origin project |
| Root reading instructions | 1 | `How to open the data.txt` |

The complete 638-entry metadata also lists Fig. 4b (106), ToF-SIMS (47), XPS (2), Fig. 2b (1), and two root files in total. These are not all part of the 481-file acquisition; do not claim new numerical composition analysis from the electrochemical subset.

Eight acquired files are genuinely zero-byte repository entries and must remain unusable data, not be repaired or imputed:

- `data/Fig. 2a/WNi79T/RUfinal.xls`
- `data/Fig. 6b/WNi225T-A/CVfinal.DTA`
- `data/Fig. 6b/WNi225T-A/Regen_41.DTA`
- `data/Fig. 6b/WNi225T-A/Regen_42.DTA`
- `data/Fig. 6b/WNi225T-A/Regen_43.DTA`
- `data/Fig. 6b/WNi225T-A/RuFinalZ.DTA`
- `data/Fig. 6b/WNi225T-A/WNi225T-A_42.DTA`
- `data/Fig. 6b/WNi225T-A/WNi225T-A_43.DTA`

## Experimental comparability

| Comparison | Nominally shared conditions | Distinction / limit | Primary anchor |
| --- | --- | --- | --- |
| Fe-lean ± regeneration | Purified 1 M KOH, 30°C, 300 mA/cm², 72 h, high-purity Ni wire | Fe-lean is expected <36 ppb by the literature purification method; not a measured zero-Fe bath. Author reports negligible regeneration benefit. | Article Fig. 3; `article.txt` line 14 |
| Added 100 ppb Fe ± regeneration | Same electrolyte preparation and current/temperature/time framework | Author reports loss of performance without pulses and preservation with pulses; separate specimens, no quantified identical initial Fe inventory | Article Fig. 3; `article.txt` lines 15–17 |
| Added 5 ppm Fe ± regeneration | Same 300 mA/cm² framework | Red precipitate persists: nominal total addition is not a known dissolved concentration. Author reports stable activity in both arms within 72 h. | Article Fig. 3/5; `article.txt` lines 20–22 |
| Added 120 ppb Fe ± regeneration | 800 mA/cm², 30°C, same nominal pulse schedule | Wire length and geometric area are halved versus 300 mA/cm² tests. Author reports eventual pulse-arm deactivation after ~66 h. | Article Fig. 6; `article.txt` lines 23, 36 |
| Commercial KOH ± regeneration | 1 M KOH, 30°C, 300 mA/cm² | Fe content not quantified for each batch. Authors explicitly report batch-dependent differences. | Article Fig. 2; `article.txt` lines 10–13 |
| Sequential Zn and Fe | One wire at 300 mA/cm² in Fe-lean KOH: 1 h baseline, +5 ppm Zn, 1 h later +5 ppm Fe | Same-specimen evidence of Fe-specific activation, but no order-reversed Zn/Fe, matched-anion/volume sham, or damaged-founder replacement control documented | SI p.17, Fig. S19; `article.txt` line 25 |

Main controlled experiments are not feed-switch sequences. SI p.18 Fig. S20 describes disassembling and acid-cleaning the cell and replacing the membrane when going from high-Fe experiments to lower-Fe experiments. New membranes were activated for 1 h in commercial 1 M KOH. This is a carryover-control procedure between experiments; it is not a same-wire lineage protocol. The source does not report a measured residual-metal carryover concentration after cleaning.

The authors state each electrochemical experiment was performed at least in duplicate (`article.txt` line 39), but the selected file groups are not automatically independent duplicates. The many cycle segments must not be treated as biological/chemical replicates. SI Figure S2 has three commercial-KOH pulse experiments; those images and the duplicate statement do not create raw replicate uncertainty for every Fig. 3 arm.

## Chemical and instrumental conditions to retain

- Working electrode: Ni wire 99.995%, diameter 0.5 mm, sonicated 15 min ethanol then 10 min MilliQ water. Standard immersed length ~1.2 cm, geometric area ~0.19 cm². 57 mA therefore corresponds to 300 mA/cm². At 800 mA/cm², 76 mA and ~0.6 cm immersed length imply ~0.095 cm². Roughness-derived ECSA 0.41 cm² pertains to the standard wire and uses an assumed specific capacitance of Ni in NaOH, not a new direct active-site count. (`article.txt` lines 22, 31, 36, 38.)
- Thermostated H-cell, 30°C, Selemion AHO separator, Ni mesh counterelectrode, Hg/HgO/1 M KOH reference; both sides stirred. Anode bath 36 mL. This is not an open continuous-feed reactor. (`article.txt` lines 31–33; SI Fig. S20.)
- Main pulse schedule: 100 s at 1.43 V vs RHE after each 100 min OER. Native headers show OER blocks of 6000 s and 15 s zero-current presteps, versus 259200 s continuous-control setting. Pulse headers show 100 s and 0 or 0.5 s presteps. Wall-clock time, OER-on time and plotted concatenated time must be distinguished. Main-text fraction 1.67% is pulse/OER time, not pulse/total elapsed time.
- SI Fig. S1 is a different preliminary schedule: ~13 min pulse steps at 1.43 V, 1.23 V, OCP, or 40 CV cycles. Do not transfer it to the 100 s main experiment.
- SI Fig. S2 says **1.47 V**, whereas main Fig. 2 and main text say **1.43 V**. Retain this source discrepancy. In acquired headers, `Regen_1.DTA` uses instrument `VSTEP1` 0.510 V for WNi78T/WNi99T and 0.515 V for WNi176T-A/WNi198T-A/WNi225T-A. Using SI's stated conversion these become approximately 1.4222/1.4272 V before any correction. They do not justify silently forcing all pulse values to precisely 1.430 V.
- SI Note 2: reported RHE conversion is measured V + 0.098 V + 0.059 V × pH, pH 13.8. Offset is 0.9122 V. Methods say plotted curves are iR-corrected using initially measured Ru, typically 2–2.5 ohm, at 1.43 V, following 60 s conditioning. A raw Gamry voltage must not receive an inferred second correction. Published Origin projects carry additional processing history (including `Subtracted by 0.042` strings); reconcile each exported quantity before comparing absolute potential.
- Native AREA headers are inconsistent with physical area: many show 1.0 cm²; WNi194T-A and WNi197T-A main scans show 0.19 cm²; WNi198T-A OER shows 0.19 while its pulse header shows 1.0. Use source geometry and actual current, not an assumed universal header normalization.
- Fe added as Fe(NO3)3 to purified KOH immediately before experiments. The 5 ppm method text opens with “commercial KOH” but then explicitly uses 36 mL iron-lean solution; preserve exact source wording and rely on the stated controlled-addition protocol without inventing a measured bath assay. Dilute Fe stock hydrolysis/precipitation with storage is acknowledged by authors. (`article.txt` line 33.)
- At 36 mL, nominal additions correspond approximately to 3.6 micrograms Fe at 100 ppb, 4.32 micrograms at 120 ppb and 180 micrograms at 5 ppm, before background and precipitation. These are preparation inventories, not measured dissolved or electrode-retained amounts. Bath concentration, accessible pool and catalytic-site inventory remain different quantities.

## Raw mapping constraints

`data/How to open the data.txt` says OPJU files are processed Origin plots, DTA files are native Gamry data, and pulse sequences were reunited into `SampleName_processed.txt`. Those processed files are derived copies and cannot be counted as separate experiments.

| Figure | Raw folders | Confirmed from headers without curve fitting |
| --- | --- | --- |
| 2a | `WNi78T`, `WNi79T` | WNi78T has 6000 s OER segments and 100 s regeneration files; WNi79T is continuous-control export. OPJU contains `WNi98T-A` rather than raw-folder `WNi78T`: exact published regeneration-trace identity needs reconciliation. |
| 3a | `WNi175T-A`, `WNi194T-A`, `WNi197T-A` | Each main DTA is 57 mA, 259200 s; selected headers have blank notes, so filename alone does not encode Fe supply. Obtain exact figure-to-sample mapping from Origin dataset/plot metadata, not outcome shape. |
| 3b | `WNi99T`, `WNi176T-A`, `WNi198T-A` | Each has 57 mA OER segments and regeneration files. OPJU strings include these names and legend order iron-lean / 100 ppb / 5 ppm, but string presence alone is insufficient to prove the column-to-curve association. |
| 6b | `WNi214T-A`, `WNi225T-A` | Both OER headers explicitly note `120 ppb F`, use 76 mA. WNi214T-A continuous-control setting; WNi225T-A pulse sequence. |

## What the composition evidence actually measures

Article Fig. 4 compares different wires harvested fully active, before deactivation, after deactivation, and after 72 h with regeneration. The analysis is destructive and does not follow atoms or active sites on one wire across those states. Fig. 4/5 surface ratios use ToF-SIMS fragments; depth profiles are calibrated via sputter craters on a separate pure Ni foil. Four randomly chosen spots per wire provide surface-ratio standard deviations; these are within-wire spatial measurements, not four independent wires. Selected depth profiles average two spots with differing sampling rates. No absolute Fe mass balance or active-site turnover calibration follows from those ratios.

The authors report active wires richer in surface Fe and deactivated wires richer in subsurface Fe (>4 nm), supporting a surface-accessibility model and motivating a distinct buried/inaccessible pool. The authors themselves describe redeposition of highly oxidised leached Fe as a reasonable assumption, with the species left to future work (`article.txt` line 28). Desorption to bath, burial, surface redistribution, and retention are therefore competing causal components, not individually measured rate constants.

SI Table S1: pristine Ni wire ICP-OES Fe 5 ± 1 ppm and Co 151 ± 6 ppm, from duplicate bulk digests of ~340 mg. Cutting with stainless steel pliers may have overestimated Fe. This assay does not measure each experimental wire's initial active surface Fe and provides no per-site maximum catalytic activity. XPS Fe2p is masked by Ni/Co Auger signals; weak Fe3p appears in the active sample. Neither is an old/new Fe discriminator. No direct gas-output / Faradaic-efficiency assay is reported in the inspected article/SI for these arms, so current and potential alone should not be promoted into newly repaired O2-producing sites.

## Negative outcomes and discrimination requirements

Preserve the reported Fe-lean no-benefit result, 5 ppm no-observed-extra-stability benefit within 72 h, 5 ppm precipitation and proposed fouling risk, 800 mA/cm² late failure despite regeneration, batch dependence, zero-byte raw files, and source pulse/identity ambiguities. A model must not redefine all maintenance as new-material repair or assign all pulse-associated recovery to incoming Fe.

A chemistry-grounded comparison should admit at least active surface, inactive/buried material, solution/precipitate supply and persistent Ni host. The voltage observation is sensitive to the total competent surface plus ohmic, morphology and bubble effects; it is not inherently sensitive to atom age. Origin-labelled subpopulations with the same kinetic and catalytic coefficients are structurally unidentifiable from total activity alone. A founder-retention/rearrangement alternative can therefore remain viable even when a supply-sensitive model predicts the pulse curves.

Decisive followup would require a matched same-specimen damage-and-recovery sequence with equal total metal supply and electrochemical history, time-of-entry isotopic label, quantified loss/inventory, measured function, and selective old/new-pool attribution or a valid founder-activity upper bound. A fresh isotope signal by itself is still insufficient if its active fraction and founder contribution remain unbounded.

## Evidence and invocation

A bounded format-tool followup found no installed supported Origin reader. Current [LabPlot's parser](https://github.com/KDE/labplot/blob/5cfefccab121917fba303de6cc755b15b0e1ce30/src/backend/datasources/projects/OriginProjectParser.cpp#L57) explicitly excludes OPJU pending liborigin support. [Origin's documented conversion route](https://docs.originlab.com/quick-help/convert-opju-project-file-format-to-older-opj) uses Windows Origin Viewer to save OPJ. The [official Mac Viewer page](https://www.originlab.com/viewer/) restricts that reader to macOS10.10–10.15, so no unsupported installation was attempted on this newer host. Printable metadata and unsupported renaming are insufficient to certify curve binding. This explains the retained exact-mapping uncertainty; it does not prevent the atom-origin identifiability test.

Source inspection: standard-library XML figure-caption extraction; numbered article text lines 10–42; SI Notes 1–3, Figures S1–S22 and Table S1. Native header inspection was restricted to settings before `CURVE`, plus ASCII Origin labels/history and deposit paths; no electrochemical curve fit was performed by this audit. A broad initial header-print command was truncated and was replaced by selected-key output; no conclusion relies on truncated content.

Checksum scenario: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3` read `data-receipt.json`, joined all entries by repository file ID to `dataverse.json`, recomputed SHA256 and repository checksum for every local `data/<path>`, and compared declared byte size. Binary observable: no mismatch paths; all 481 files present. Captured result: this audit's verified acquisition section. Parent analysis should retain its machine-readable per-file verification artifact for end-to-end reproducibility.

Verified source SHA256:

- `article.xml`: `5843d84d03b3b7ff281feca4d8a9b0e3e9714e2c0791bc4dfde012340614c519`
- `supporting-information.pdf`: `230268c2a4b6961b5009fe51afb80055d4217e495637628563be18cfae384d5f`
- `dataverse.json`: `af9f5b943b4ac95734f3d87e468239b0c7d27050ff86956361ce4ddb47590363`
- `data-receipt.json`: `0254d9b1244c05317ae3a0b5fdc34c3037cbf8af02c1041fbf99380b58479d23`

## Bounded raw-label followup: exact assignments remain unresolved

A second pass inspected all Fig. 3 native DTA `NOTES` blocks, complete deposit file descriptions and ASCII dataset/legend/plot-style metadata in both native Origin projects. No curve endpoints were used for condition assignment. All six Fig. 3 samples have blank experimental notes. Deposit descriptions label only two XPS files, with no Fe-condition lookup table. None of `originpro`, `opju`, `opjfile`, `pyorigin` or `olefile` is installed in the qualified Python environment; no package was installed and no unsupported binary-parser claim is made.

Concrete byte-offset evidence in `data/Fig. 3a/Overlay no reg AEM.opju`:

- Six dataset names `Book3_A` through `Book3_F` occur at offsets 222, 30147, 128432, 158361, 265289 and 295215.
- Legend strings at offsets 402854, 402873 and 402891 associate plot **1** with iron-lean, plot **3** with 100 ppb Fe and plot **2** with 5 ppm Fe. The text's display order is therefore not its plot order.
- Column comments at offsets 401555, 401794 and 402034 record subtraction of 0.042 from B, D and F. The project has no ASCII WNi175/WNi194/WNi197 sample labels. It cannot be joined to those raw files from the inspected labels alone.

Concrete evidence in `data/Fig. 3b/Reg overley AEM.opju`:

- Six dataset names `Book1_A` through `Book1_F` occur at offsets 222, 13938, 36642, 50358, 104917 and 131566.
- Column comments label WNi99T-A, WNi176T-A and WNi198T-A at offsets 226652, 226924 and 227199. Each records subtraction of 0.042.
- Legend strings at offsets 229208, 229227 and 229246 associate plots 1, 2 and 3 with iron-lean, 100 ppb Fe and 5 ppm Fe, respectively.
- Three consecutive `__STYLEHOLDERSOURCEINFO` blocks contain sample labels WNi99T-A (offset 229984), WNi176T-A (230672), WNi198T-A (231370). Their ordering supports the **provisional** assignment 99→lean, 176→100 ppb, 198→5 ppm. It has not been established with a supported Origin reader that the binary record order is the legend plot-number order, so this remains a hypothesis, not a proven mapping.

Permissible assignments for a strict raw-data analysis therefore remain all six permutations of (lean, 100 ppb, 5 ppm) over (175, 194, 197) and, conservatively, all six over (99, 176, 198). The cross-product is 36 combinations. The ordered-record hypothesis for 3b may be reported separately as a labelled sensitivity assumption, but an outcome-based choice of the best-fitting permutation would contaminate evaluation. A supported original-project readout or depositor-supplied sample key would resolve this; condition cannot be inferred solely from activation level or run number/date.

All five acquired `*_processed.txt` files have only the header `Hours` and `Potential (mV)` (with minor whitespace differences). Their headers do not state reference electrode, reference conversion, or iR correction. The author's reading instructions describe concatenation of pulse files but do not specify any voltage transformation. The OPJU plot axes say potential vs RHE, and the paper says its plotted values are iR-compensated; these facts establish the intended published scale, not the status of each intermediate processed text export. The extra 0.042 subtraction in Origin processing history reinforces the need to avoid double correction or treating the processed-header unit as a verified calibration. The native RHE conversion and Ru protocol above remain the only explicit methods-level calibration instructions.

This followup establishes a **label-provenance limitation**, rather than an experimental negative result. No sample was relabelled and no numerical model was fit to decide its identity.
