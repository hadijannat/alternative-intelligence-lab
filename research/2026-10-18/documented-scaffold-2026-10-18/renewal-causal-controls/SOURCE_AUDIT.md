# Primary controls for competent-organization restoration

## Native source acquired

K. Nishioka, S. Hiro and K. Murase, *Phosphate buffer-induced depletion of nickel redox sites limits oxygen evolution on stainless steel anodes*, Journal of Materials Chemistry A 14, 23803-23813 (2026), DOI [10.1039/D6TA02355J](https://doi.org/10.1039/D6TA02355J).

The exact DOI/title was absent from the prepared October 18 research ledgers before this screen. The paper's full text was readable through normal Chrome after an automatic publisher verification page. No challenge was solved, login changed or restriction bypassed. The publisher page identifies CC BY 4.0 and states that data supporting the study are in the article and SI. Its observed native PDF link redirected to a public publisher CDN; that actually observed URL supplied the acquired native PDF after direct routes failed. The signed query is transient and is sanitized in the public receipt; the stable publisher link remains available for reacquisition.

| Asset/route | Observed state |
|---|---|
| Direct migrated RSC main PDF | HTTP403 body preserved as `sources/nishioka-main.pdf`; this is HTML, not an acquired PDF |
| Direct RSC SI | HTTP403 body preserved as `sources/nishioka-si.pdf`; SI remains unacquired |
| Browser-observed publisher CDN main | HTTP200, 1,069,448 bytes, valid PDF, 11 pages |
| Native main SHA256 | `cc0a2f41fb99889e0b28cebe2d21270e3c532823f515727b89f53953862ce825` |

`sources/receipt.json` preserves the initial four failed primary requests, including Stevens and Cimino. `sources/browser-main-receipt.json` separately records the later successful main request. `sources/verification.json` checks all five stored bodies against their original hashes/sizes, native title/DOI/pages, the preserved failures and the source-unit discrepancy. Full page-delimited text and renders remain local. The source payloads are excluded from curated publication.

## Preparation, perturbation and common-medium function

Main methods (journal23804-23805, PDF2-3) use a 0.2 mm 304 stainless-steel sheet, exposed area0.50 cm2, Pt mesh counter, Ag/AgCl reference, room temperature and500rpm. Commercial hot cleaning and oxide removal precede measurements; those processing dependencies are recorded rather than treated as an autonomous organization. Phosphate electrolytes are0.2/1/3M K2HPO4, nominally pH11.5 using specified KOH ratios. The external regeneration electrolyte is1M KOH.

Recovery is **repeated electrochemical oxidation in KOH**, not mere passive immersion. The declared program applies1.581V_RHE for10min and0.981V for5min, twice; two bidirectional1.061-1.581V sweeps at5mV/s follow; the two-step sequence is repeated12times. The source's shorthand immersion wording must not omit this external drive and handling.

Fig6 (journal23810, PDF8) provides within-electrode pretreatment,250-cycle phosphate deactivation and KOH re-oxidation. Importantly, the recovered CV is the first subsequent CV **back in phosphate electrolyte**, not a comparison of phosphate function with KOH function. This is stronger than an immediate electrolyte-dependent current change. It supports persistent functional reconditioning across the return to that assay medium. It does not identify the material responsible for recovery.

The Ni reduction-peak integral is a redox-site indicator, with stated assumptions relating it to catalysis; it is not an independently calibrated census of catalytically competent Ni. OER activity is assessed from current/potential. The native main does not provide an independent oxygen-output recovery assay, specimen identifiers, a replicate distribution or propagated uncertainty for the key recovery comparison. Missing uncertainties are not zero.

## Material evidence and unresolved origin

The damage interpretation is broader than phosphate adsorption. The authors describe selective Ni/Fe dissolution, supported by concentration/time/temperature trends and EQCM mass changes. Their monolayer estimate is conditional on assigning mass loss to Ni/Fe; EQCM is not a metal-specific dissolved-species assay.

The EQCM specimen is a **separate** quartz-supported100nm Ti/300nm304SS coating, area0.196cm2 (PDF3). Similar composition and potential trends do not make it the bulk functional sheet. Fig7's caption calls its object a sheet, while the methods specify a sputtered quartz-supported coating; preserve this ambiguity. There is no demonstrated simultaneous material-inventory/recovery trace on the bulk functional specimen.

Initial-treatment STEM/EDX/XPS compare a KOH-derived thicker Ni/Fe-containing surface film with a phosphate-derived thin Cr-rich layer. These are treatment-product comparisons, not a direct measurement of rebuilt material in the recovery sequence. After recovery the authors report disappearance of detectable P and similar other-element surface states, interpreting removal/reconstruction and Ni-site re-exposure (PDF10). Similar chemical states in XPS are not proof of identical atom inventory, especially given its finite sampling depth.

No intentional soluble-Ni precursor is supplied during recovery, but the304SS substrate and pre-existing layer are substantial retained Ni reservoirs. Their contributions are not bounded by the main. The data do not distinguish residual-site exposure, active material newly formed from substrate metal, or reincorporation of dissolved metal. Absence of external Ni does not by itself prove absence of reconstruction, and current recovery does not prove new competent material.

**Disposition:** component-supported externally driven common-medium functional recovery, with evidence consistent with dissolution and surface reconstruction; organization-level renewal attribution unresolved. Reject the preliminary pure-deblocking interpretation as too narrow. Do not promote this source to verified active-material replenishment or autonomous repair.

## Preserved source discrepancies

- PDF6/journal23808 prints the KOH-treated capacity as0.399C/cm2; PDF7/journal23809 prints0.399mC/cm2. The literal units differ by1000. Renders confirm both readings. Figure5's axis is in mC, but no corrected raw capacity is silently chosen for analysis.
- The abstract's four-to-six-monolayer statement is stronger than the conditional mass interpretation in the body; retain the latter's assumptions and absent error bars.
- XPS depth is described as roughly5-10nm in one passage and several tens of nanometers elsewhere. Neither establishes atomic origin of recovered sites.
- Irreversibility is limited to the phosphate-deactivation conditions; it does not mean no external intervention can recover function.

These discrepancies are source limits. No rate, new response-point analysis or holdout was extracted from them. Full-text reading and figure exposure are consumed literature evidence, not prospective validation.

## Other bounded primary leads

**Stevens2017**, [10.1021/jacs.7b07117](https://doi.org/10.1021/jacs.7b07117): an independent primary-reader screen found incorporation into initially Fe-free Ni films, not the requested selective damage/add-back rescue. Root direct author-PDF retrieval returned403; no native bytes were acquired locally. Treat this as a bounded primary-reader screen, not source-integrity-verified new material evidence.

**Cimino et al.**, [10.1016/j.cattod.2023.114366](https://doi.org/10.1016/j.cattod.2023.114366): a separate primary-reader obtained a transient parsed8-page CNR PDF, while later exact-URL opens and direct retrieval returned403. It describes sulfur-aged Li-Ru/Al2O3, washing-associated Li loss, LiNO3 replenishment and hydrogen/thermal regeneration, with a washed-only functional comparator and a common sulfur-free assay. The regenerated numerical table value reported in the search came from an indexed primary-PDF snippet, not the exposed native-reader excerpt. No response values are used here. Native bytes/SI are unacquired; no source-integrity or quantitative reanalysis is claimed. The missing washed+thermal/H2-without-Li arm leaves replenishment bundled with treatment. This remains an externally regenerated-material lead, not a verified causal Li-addition repair result or integrated member.

## Full-goal consequence and next observation

The correct next experiment can test reconstruction of a competent assembly rather than exclusive new-atom turnover. It still needs measured damage/reconstitution and calibrated retained-material/feed accounting, matched no-feed/redox/deblocking controls and common-medium function. The present Nishioka paper adds the common-medium recovery observation but not that joint material evidence. The Cimino lead may add independent material-loss information if its native package becomes accessible; the missing thermal/no-Li contrast remains essential to its particular attribution.

No shared operation with PMo12 or exact Mo34WV is established. Separate compartments would require measured transport, leakage, proton/electron balances, drive cost and retained component identities before J credit. No source here supplies founder-bounded serial variants, boundary renewal, causal chemical adaptation or intelligent behavior.
