# Origin/function evidence audit

## Wei access refresh

The current remote snapshot already includes the completed Wei study and its synthetic observation test. The existing native SI was independently rehashed as `658e8a17f67d282b219ea77cefb59aa59dccfe1deb06555b7a7a3f93e1f6dca1`. No duplicate SI download or repeat model run was needed.

Normal Chrome navigation to <https://pubs.acs.org/doi/10.1021/jacs.5c00438> again redirected to the publisher's abstract-only article route. It displayed lack of access and a purchase option. No purchase, login change or restriction bypass was attempted. This is an authored record of observed UI state, not acquisition of a native main article. FeLPD/FeHPD preparation assignments and main data availability remain unverified. Institutional bibliography pages and an access-index search supplied no new native main text; that bounded search does not prove no legitimate copy exists elsewhere.

## Distinct primary candidate: Ou 2023

Y. Ou and colleagues, *Cooperative Fe sites on transition metal (oxy)hydroxides drive high oxygen evolution activity in base*, Nature Communications 14, 7688 (2023), DOI [10.1038/s41467-023-43305-z](https://doi.org/10.1038/s41467-023-43305-z). An exact DOI/title search found no entry in the existing October 18 scaffold Markdown/candidate ledgers before acquisition. This is a scoped deduplication result.

Native article, supplement and figure workbook are acquired. Main data availability explicitly points to [Figshare 24197487](https://doi.org/10.6084/m9.figshare.24197487); its metadata resource DOI matches exactly. The main's final page and dataset record specify CC BY 4.0. The unneeded DFT-structure workbook is listed but was not downloaded. Source receipts retain stable URLs, resolved routes, timestamps, size, SHA256 and dataset-provided MD5. `sources/verification.json` verifies original bytes, PDF titles/page counts and workbook inventory. Complete page-delimited text and methods/control renders remain local with the native payloads.

| Asset | Bytes | Verification |
|---|---:|---|
| Author-hosted main PDF | 2,036,782 | Valid PDF; 12 pages; exact title/DOI in native text |
| Publisher SI | 3,418,265 | Valid PDF; 35 pages; matching title |
| Figshare metadata | 6,003 | Exact resource DOI; CC BY 4.0 |
| Native figure workbook | 1,662,539 | Publisher MD5 `f9ac3a56fe0e8a187d653790c2679622` and size match; 21 sheets |

## Material and assay linkage

The active films are Ni or Co hydr(oxy)oxides on Pt/Ti-coated glass or quartz, with Fe either supplied from electrolyte or introduced during codeposition. No single invariant formula for the operating mixed film is established here. Main methods p9 describe cathodic electrodeposition, purified 1 M KOH, measured pH 13.88 +/- 0.06, Hg/HgO-to-RHE calibration, resistance compensation, a Pt counter, 40 mL electrolyte and magnetic stirring. Initial CA conditioning lasts 3-5 minutes before nominal 0.1 ppm metal spiking. A nominal addition is not a measured dissolved-species distribution; the authors discuss Fe solubility/colloid uncertainty.

Critically, the electrically measured film is subsequently dissolved for calibrated ICP-MS. Acid extraction completeness is checked by post-digestion voltammetry and comparison with bare Pt/Ti. This directly improves the experimental linkage between incorporated total material and current. It is stronger than assuming that two differently supported preparations constitute one specimen. The post-digestion check verifies analytical recovery; it is not a catalyst damage-and-rescue experiment.

The deposited workbook provides actual CA/CV current traces alongside aggregated Fe loading/TOF tables. It does **not** expose a row-level pairing of specimen and replicate IDs, independent current, per-film Fe/Ni/Co masses and their covariance across the TOF series. Experimental same-film pairing is described in the paper; the individual pairings are not recoverable from this deposited workbook. Multiplying mean TOF by mean Fe mass does not recover their covariance or provide an independent current validation.

## Function, state and withdrawal observations

Main Fig3's TOF is current divided by total ICP-measured Fe. It remains a derived average, not an independent competent-site count. A changing TOF can reflect changing active fraction, per-site function, host contribution or geometry; a unique site mechanism does not follow from that ratio alone.

CA incorporation histories, redox changes, morphology and spectroscopy constrain surface/internal interpretations. Operando XAS uses 0.1 M flowing KOH in a separate geometry. It is not a simultaneous regional Fe-origin census under the 1 M bulk-current protocol. No quantitative initial residual-Fe detection ceiling or founder functional ceiling was established in the audited methods. Operationally purified electrolyte must not be equated with an analytically demonstrated zero-Fe founder.

SI Fig29 (p24) is a genuine functional intervention: current increases during Fe addition, decreases after transfer into Fe-free KOH, and recovers substantially on return to the original Fe-containing solution. It was visually checked together with its complete caption. This supports supply-dependent functional recovery under the stated sequence. It does not separate Fe loss, redeposition, retained-site reactivation, host restructuring, changed solution effects or transport. It supplies no simultaneous Fe inventory/origin trajectory. The native figure workbook has no S29 or S30 sheet.

SI Fig30 (p25) contrasts Tafel evolution in fresh Fe-free versus retained Fe-containing electrolyte. Its stated error bars describe the uncertainty of linear Tafel fits; they must not be silently treated as material-replicate uncertainty. This is additional state/function evidence, not serial inheritance or a founder-resolved repair assay.

## Eligibility decision before response extraction

The package passes identity/access and supplies new component observations. It fails qualification for a unique origin-resolved repair or inactive-state transport model: missing founder bounds, independent competent/inactive populations, joint time-resolved stock/flux/function measurements, and recoverable per-replicate composition/current linkage. No chemical-rate fit, response digitization, reconstructed-current validation or new empirical holdout is justified in this iteration.

This decision does not deny the measured supply response. A narrowly frozen descriptive trace comparison could quantify that response, but would not supply the missing R/H/J discriminator, so it is not pursued here. Figure-only S29 recovery is not converted into an invented quantitative repair rate.

Prior exposure is explicit: the paper's abstract, methods, Fig3 caption and nearby interpretation were read; the S29 control was viewed; an independent auditor's overbroad PDF search also exposed numerical prose and SI summary rows. Those outcomes are consumed literature observations. No response values were exported to a new numerical analysis, no train/holdout split was assigned, and no prospective validation is claimed.

## Dependencies and integration

The active mixed oxide is inorganic, while electrode fabrication uses carbon cloth; plastic cells, epoxy/hot glue, filters and the XAS window/flow apparatus contain organic material. External electrodeposition, electrical drive, pumping/stirring, electrolyte purification, supplied metal and terminal acid digestion are accounted apparatus/material inputs. Their presence alone does not make the oxide mechanism carbon-based, but it precludes claiming an unsupported autonomous maintained organization. No shared-medium operation with PMo12 or exact Mo34WV, boundary renewal, functional descendants or adaptive material update is demonstrated.

## Separate H near-miss

A second independent screen examined Ma et al., *Transforming Silver Nanoclusters from Racemic to Homochiral via Seeded Crystallization*, [10.1021/acs.jpclett.3c00794](https://doi.org/10.1021/acs.jpclett.3c00794). Indexed primary text describes Ag40 with 20 TBBM thiolates and 12 acetates, and a ligand-bearing chiral framework. This rejects admission of that exact architecture as a fully noncarbon active organization. Organic solvents and controlled seeded crystallization are additional dependencies. A quantitative founder functional ceiling and serial common-feed functional variants were not verified. Native main/SI bytes were not acquired in this bounded screen, and access-reader failures are retained as limits; missing heredity evidence is unresolved rather than proven absent. The distinct 2020 Ag40 cluster with 22 thiolates and 10 acetates must not be substituted for the 2023 identity.

## Next discriminator

For the Ou sequence, obtain specimen/replicate-linked current and ICP records, quantitative initial Fe bounds and Fe stock/speciation during the withdrawal/readdition stages. Combine an independently justified founder functional ceiling or selective/isolated new-material function assay with a common-medium post-assay that separates persistent film change from immediate solution effects. Isotope tracing is one possible route, not a mandatory substitute for a valid quantitative bound. Only then register a model, entire-specimen holdout and uncertainty before extracting unseen response outcomes. H further requires recipient separation, shared feed, controlled variants and serial transmission. These measurements are not supplied by the acquired package.
