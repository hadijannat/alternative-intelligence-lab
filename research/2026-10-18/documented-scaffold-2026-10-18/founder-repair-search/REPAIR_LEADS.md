# Primary repair datasets acquired, 2026-10-18

**Best next candidate: Fe-incorporating Ni hydr(oxy)oxide on nickel felt with periodic electrochemical activation (EA), Han et al. 2025.** This source adds an isotope-switch comparison to functional electrode measurements. It can test a restricted metal-retention model; it does not show descendant inheritance, a founder-free functional assay, or compatible integration with PMo12/Mo34WV.

Scope: primary-source search and acquisition only. No model was fitted and no worksheet isotope outcomes were extracted. Author-rounded outcomes in the main-text isotope paragraph were encountered during the methods audit, so any subsequent challenge must be labelled retrospective and source-informed. The exact worksheet values can still be withheld from parameter fitting; they cannot honestly be described as wholly unseen evidence.

## 1. Han et al., Nature Communications 16, 4803 (2025)

- DOI: https://doi.org/10.1038/s41467-025-60201-w
- Main: `sources/repair/han2025/article.xml`, `article.txt`, `article.pdf`.
- Native source data: `sources/repair/han2025/41467_2025_60201_MOESM3_ESM.xlsx` (40,501,102 bytes; 42 worksheets).
- SI: `41467_2025_60201_MOESM1_ESM.pdf` (47 pages) and text extraction. The separate MOESM2 PDF is the peer-review file, not a second experiment.
- Acquisition receipts: `receipt.json`, `pdf-receipt.json`; source ZIP retained. Original Fig. 3: `41467_2025_60201_Fig3_HTML.jpg`.
- Article licence: CC-BY-NC-ND-4.0; retain source attribution and do not assume unrestricted redistribution of adapted article material.

### Exact isotope comparison and experimental conditions

The electrode is commercial nickel felt, 250 micrometres thick, 60% porosity, 20 micrometre fibre diameter, Bekaert 2Ni18-025, geometric area 1 cm2. The active surface evolves into Fe-incorporating Ni hydr(oxy)oxide; it is not a fixed molecular formula or a separately collected daughter material.

Initial conditioning: EA at 0.5 A/cm2 for 20 h in unpurified 1 M KOH containing approximately 76 ppb natural Fe. The EA cycle uses 1 h at the imposed OER current followed by 3 min at 0.6 V versus RHE. The source calls 50 cycles '50 h' despite added reduction intervals; do not silently equate its OER clock with total elapsed time.

After initial conditioning, the electrode enters purified 1 M KOH with 100 ppb added 57Fe, for a further nominal 20 h, in three arms:

1. High current, 0.5 A/cm2, without EA.
2. Low current, 30 mA/cm2, without EA.
3. High current, 0.5 A/cm2, continuing EA at 0.6 V versus RHE.

The first Fig. 3g bar is the initial 20 h state, followed by these three arms. Samples are rinsed with pure water and measured by ICP-MS. The caption reports standard errors from three independent replicates. The purified electrolyte itself contains approximately 20 ppb background Fe. The isotope feed is prepared from a named 57Fe plasma standard (10 micrograms/mL); isotope enrichment/purity is not numerically specified in the inspected methods. Half-cell methods specify 50 mL electrolyte in each H-cell compartment, a Pt counter electrode and saturated calomel reference. These are supplied electrode, electrolyte and externally driven apparatus conditions.

Workbook mapping, obtained from text cells without extracting numerical isotope values:

| Sheet/cells | Meaning |
|---|---|
| `Fig3!H25` | Panel 3g |
| `Fig3!I26:J26` | 56Fe, 57Fe |
| `Fig3!K26` | Sum 56Fe+57Fe |
| `Fig3!H27` | Initial EA high-current state |
| `Fig3!H28` | Subsequent high current without EA |
| `Fig3!H29` | Subsequent low current without EA |
| `Fig3!H30` | Subsequent high current with EA |

`fig3-text-cells.json` captures the textual labels; `fig3g-cell-layout.json` captures populated-cell locations/types. The block supplies four rows of three numerical values and no adjacent error/replicate columns. The caption's three-replicate claim must not be converted into invented replicate data or error bars. Before treating uncertainty as unavailable everywhere, inspect whether the plot or another source table supplies it.

### Appropriate constraints and retained negatives

- A final 57Fe inventory exceeding the measured initial 57Fe inventory contradicts a strict no-influx, retained-founder-only **atom-inventory** model. It does not by itself assign catalytic function to those new atoms. A conservative fresh-57Fe lower bound can subtract all initial 57Fe from the final inventory, provided comparable normalization and measurement uncertainty are handled.
- Residual natural Fe in purified KOH means final 56Fe cannot simply be equated to retained founder atoms. Natural abundance in the initial stock and isotope purity of the feed must be distinguished.
- Endpoint isotope amounts do not identify separate dissolution and redeposition rate constants or a full time-dependent exchange model. No concurrent solution isotope inventory is supplied in the inspected methods.
- A source typo compares '56Fe' to '56Fe' in the sentence describing a two-to-threefold isotope ratio. Preserve that defect and resolve isotope assignment against the figure and worksheet; do not silently repair the sentence.
- OER activity traces, isotope endpoints, Raman measurements and device oxygen measurements are related but different experiments. Do not pool them as synchronized observations of one specimen.
- The paper measures oxygen Faradaic efficiency using gas-water displacement in its AEM device at 1 A/cm2 (SI Fig. 29). This is stronger function evidence than current alone, but it does not establish the half-cell isotope arms' gas efficiency or new-atom-specific activity.
- The AEM device depends on Pt/C, carbon paper, organic ionomer/membranes and external control. Its 1000 h claim includes a membrane replacement at 525 h. EA-off operation from 1050 to 1100 h causes degradation; resumed EA leaves a residual approximately 60 mV voltage penalty at 1150 h relative to 1050 h. These are component/device observations, not autonomous repair of a complete organism.
- Predeposited NiFe on nickel felt worsens under EA (SI Fig. 24), so successful regeneration of bare felt must not be generalized to all preformed NiFe catalysts.
- Strongly alkaline pH 14 conditions have no demonstrated common operating medium with the acidic PMo12 source system. No properties transfer to Mo34WV.

## 2. Poli et al., Green Chemistry (2025): newly accessible raw deposit

- DOI: https://doi.org/10.1039/D5GC00114E
- Deposit DOI: https://doi.org/10.34894/XW7RK6
- Current public API successfully returned version 1.0, RELEASED 2025-06-16, CC-BY-4.0, 638 files totalling 124,028,278 bytes. Prior Anubis/403 failures remain unchanged in their original records; the new successful access is a separate observation.
- Local metadata: `sources/repair/poli2025/dataverse.json`.
- Native main XML and SI ZIP acquired via EuropePMC PMC12053971. SI PDF extracted as `supporting-information.pdf` (20 pages), with text extraction.
- Selected raw subsets: Fig. 2a, 3a, 3b and 6b plus the README: 481 files, 55,239,493 bytes. All files match the deposit's checksums. `data-receipt.json` records each file ID, URL, relative path, SHA256 and checksum comparison.
- Formats include Gamry DTA plaintext, processed text, Origin OPJU, XLS and XLSX. Repository MIME labels some DTA files 'application/x-stata'; README and inspected magic/header identify Gamry, not Stata. No Origin installation is necessary to parse the DTA files.

Useful comparison: 99.995% bare Ni wire in 1 M KOH at 30 C, 300 mA/cm2, with versus without periodic 100 s reductions to 1.43 V versus RHE after each 100 min of OER. Feed controls include Fe-lean electrolyte, nominal 100 ppb Fe addition, and 5 ppm Fe. At higher current (800 mA/cm2) a separate comparison uses 120 ppb Fe. This higher-current arm contains a published late failure despite regeneration and is a useful adverse condition to preserve.

The 300 mA/cm2 electrode has approximately 0.19 cm2 exposed area (1.2 cm wire); the 800 mA/cm2 electrode is half that length, approximately 0.095 cm2, to limit absolute current. The raw Gamry header says AREA=1, so it must not override the manuscript's actual geometric-area normalization. DTA potential is versus the instrument reference, whereas published plots use RHE with resistance correction. Initial/terminal EIS files are provided, not a blanket licence to subtract an arbitrary resistance from every point. The regeneration duty cycle and omitted regeneration segments need explicit accounting.

Poli supplies functional electrode potential and relative ToF-SIMS surface/subsurface Fe evidence, but the inspected main/SI methods do not contain a direct gas-output assay or isotope tracing. ToF-SIMS relative signal is not calibrated active-atom inventory. It is therefore a secondary regeneration comparator, weaker than Han for separating newly incorporated metal from retained founder metal. No kinetics or data curves were fitted here.

## Duplicate and rejected lead log

- DOI 10.1038/s41467-021-26281-0 (NiCoFe borate LDH) is already audited at `recursive-compound-2026-10-15/renewal/fe-feed-21/REPORT.md`. A new XML/ZIP retrieval had started before duplication was identified and is retained under `sources/repair/nicofe2021/`, with no new experiment or candidate credit.
- DOI 10.1038/s41560-020-0576-y (dynamic Fe sites) and DOI 10.1038/s42004-025-01500-7 (hybrid perovskite equilibrium healing) were located but flagged as previously consumed source families by the root inventory. No new fit or source transfer was made.
- Initial Nature web-tool opens redirected to inaccessible identity-provider pages; publisher search indexing and EuropePMC/native publisher retrieval subsequently provided Han data. RSC HTML direct web open returned 403, and the initial Groningen `/ws/files/` PDF route returned 403. Those access negatives coexist with successful EuropePMC and Dataverse acquisition.
- Search phrases included `self-healing oxygen evolution source data dissolution`, `repair catalyst source data Fe self healing nickel`, and `self healing catalyst regeneration 2025 Source data`. Selection was bounded to relevant primary repair studies; generic stability curves, redox recharge alone, and organic polymer healing were excluded.

## Reproduction evidence

Acquisition scenario: fetch the recorded EuropePMC/native publisher URLs and the Dataverse API/file URLs in receipts; binary observable is nonempty XML/PDF/ZIP/XLSX or raw data plus matching checksum. Hashes and sizes are retained in the corresponding receipt JSON files. The Dataverse download completed with 481/481 files, zero failed requests and zero checksum mismatches.

Header-audit scenario: use Python standard-library `zipfile` and `xml.etree.ElementTree` on the native XLSX; binary observable is labelled `Fig3` isotope block with the four condition rows, without extracting its numerical outcomes. Captured artifacts: `fig3-text-cells.json`, `fig3g-cell-layout.json` and `asset-validation.json`.

No physical experiments, fitted repair rates, prospective validation or founder-free inheritance were performed by this source-acquisition subtask.
