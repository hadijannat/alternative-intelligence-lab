# Zheng 2014 Beta seed-composition evidence

Primary source: Bumei Zheng et al., *Chinese Journal of Catalysis* 35 (2014), 1800-1810, [DOI 10.1016/S1872-2067(14)60089-9](https://doi.org/10.1016/S1872-2067(14)60089-9). The publisher [full HTML](https://www.cjcatal.com/fileup/0253-9837/HTML/20141103.htm) and PDF were acquired on 2026-10-18. Local source bytes and their hashes are in `sources/receipt.json`. Tables 1 and 2 were extracted from HTML and visually checked against PDF pages 3 and 4 (printed pages 1802-1803), saved as `sources/page-3.png` and `sources/page-4.png`.

This is a new primary-source acquisition in this branch, but the headline composition convergence has already been inspected before any model protocol. Any subsequent split is retrospective. No fitting, prediction scoring, or simulation was performed in this acquisition task.

## Methods and exact numeric package

Section 2.2 uses a gel with molar oxide composition Na2O:Al2O3:SiO2:H2O = 11.4:1:40:640. Fumed silica was dissolved in NaOH solution, then NaAlO2 was added with stirring. Calcined Beta seeds were added at 10 wt% **relative to the silica source**, not relative to all solids, all framework atoms, product mass, or total wet gel. Synthesis was static at 140 degrees C in a 100 mL autoclave. Products were filtered, washed, and dried at 110 degrees C. This does not state a 100 mL reaction volume.

The original seeds were synthesized with organic structure-directing agents and calcined in air at 540 degrees C for 6 h. Al-containing seeds used TEAOH, TEABr, or both; pure silica seeds used TEAOH and NH4F. The subsequent growth gel was OSDA-free. These experiments therefore do not establish an origin entirely without organic reagents.

`sources/tables-exact.json` preserves every table cell including header cells, missing-value dashes, the spacer column, and footnotes. `sources/seed-product-table.csv` gives the joined numeric rows. `NA` means not reported; `inf` records the pure-silica composition, not a large finite ratio. Ratios are **SiO2/Al2O3**, not Si/Al. Seed XRD crystallinities use S6 as reference, whereas product XRD crystallinities use BEA9. They must not be divided as though measured on a shared absolute scale. Product table footnote says the tabulated products contain no other crystal phases; lower crystallinity does not imply another crystalline phase in those selected samples.

| Seed | Seed SiO2/Al2O3 | Product | Product SiO2/Al2O3 | Product XRD % vs BEA9 | Yield % |
|---|---:|---|---:|---:|---:|
| S1 | 11 | BEA1 | 11 | 16 | unreported |
| S2 | 12 | BEA2 | 11 | 19 | unreported |
| S3 | 23 | BEA3 | 11 | 49 | unreported |
| S4 | 22 | BEA4 | 10 | 60 | unreported |
| S5 | 31 | BEA5 | 10 | 64 | unreported |
| S6 | 38 | BEA6 | 10 | 89 | 32.5 |
| S7 | 30 | BEA7 | 10 | 93 | 32.3 |
| S8 | 29 | BEA8 | 10 | 94 | 32.6 |
| S9 | pure silica | BEA9 | 10 | 100 | unreported |
| S10 | pure silica | BEA10 | 10 | 97 | 32.4 |

Yield percentages appear in Table 2 and early-time figure insets, but an explicit denominator/formula for these percentages and absolute recovered dry masses were not found in the acquired article. They must not be converted into founder fractions or multiplication factors without that basis. Likewise, 10 wt% seed addition does not determine the fraction of surviving founder material after dissolution, washing and growth.

## What changes the heredity assessment

The same nominal gel recipe with compositionally different seeds gives products clustered at oxide ratio 10-11. The pure-silica seeds yield Al-containing product, which requires acquisition of Al from the feed. Section 3.2 and the conclusion attribute the similar product composition and morphology primarily to the synthesis conditions. This directly opposes an assumption that the seed's initial bulk Al fraction is copied to product under these conditions.

Seed dependence is nevertheless observed in growth timing, attainable crystallinity and crystal size. Section 3.2 says the unseeded synthesis did not yield Beta. Seed ratios, size, crystallinity, defects and preparation histories covary, so these data do not independently identify a composition-only causal growth law. Product measurements include residual seeds: this is a bulk endpoint assay, not a physically isolated daughter population. No uncertainty bars or independent replicate count are supplied with the table rows.

Section 3.3.1.1 reports dissolution during induction. Residual Al-containing seeds can host growth of new small crystals. Pure-silica remnants appear smoother, with no visible equivalent surface growth; dissolved fragments are proposed as the main nuclei source for this case. This is a mechanistic inference from morphology and spectroscopy, not direct tracking of each fragment.

Section 3.3.1.2 compares calcined and uncalcined S6 seeds. Calcined seeds show faster dissolution and shorter induction. Uncalcined seeds give a doublet XRD feature consistent with a high-ratio seed core and lower-ratio newly grown shell. This qualitative case supports distinguishing retained parent material from a new product state. It does not provide an independent numerical product-composition table for an uncalcined holdout.

The article's introduction cites prior re-seeding work (Kamimura 2010/2011). The acquired study does not itself report a serial transfer chain with founder dilution, distinct inherited variants and maintained function. A reference to those papers is not new evidence that the present ten-row comparison contains serial inheritance data.

## Functional measurements and remaining gaps

Section 2.3 measures N2 adsorption/desorption at -196 degrees C after vacuum activation at 350 degrees C for at least 6 h. Table 2 includes micropore and mesopore volumes for BEA5-BEA10: micropore volumes 0.18-0.21 cm3/g and mesopore volumes 0.04-0.08 cm3/g. These are useful structural/adsorption endpoints on recovered products. They establish accessible porosity after growth under the assay preparation; they do not establish catalytic turnover, active-site retention under operating conditions, substrate selectivity transmission or a coupled maintenance service.

Catalytic uses of Beta are cited as background; this study presents no before/after-growth chemical reaction-rate or selectivity assay. No coupled PMo12 or Mo34WV experiment, redox compatibility measurement, autonomous repair or intelligence test appears. Hydrothermal growth at 140 degrees C in alkaline gel is a different regime from the documented acidic PMo12 electrochemical operation. Integration remains untested.

## Acquisition outcomes and preserved negatives

The parent investigator reported two prior web-tool timeouts for the full HTML; these remain reported prior-route failures, not failures independently reproduced here. Direct curl retrieval succeeded. The legacy PDF link present in the full HTML returned HTTP 404; its actual response body is saved. The modern PDF button's `download_EN.js` exposes `showArticleFile.do`; following that actual interface returned a signed PDF URL and the 11-page primary PDF. No guessed URL variants or broad literature searches were used.

Acquisition checks verify the source title, 11 PDF pages, ten joined seed/product rows, correct table cell alignment and source hashes. The source package provides evidence for product composition convergence and residual-seed confounding. It provides no claim that a functionally inherited complement has been established.
