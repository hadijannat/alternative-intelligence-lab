# Measurement-integrity follow-up review

Date: 2026-10-16.

- codeQualityStatus: CLEAR
- recommendation: APPROVE as a source-informed measurement design, not scientific result admission
- blockers: []
- Reviewed REPORT.md SHA256: `9717274ac3eae665250c728e47976b36a2cf0463185b02fda44d8b4bc8e54129`
- Reviewed acquisition.json SHA256: `8839f2f74faac714c5a9a85eb04bbe6c2b02081cbf12b04f53cded2fda0692bc`

## Findings by severity

CRITICAL: none. HIGH: none. MEDIUM: none. LOW: none requiring changes.

## Independent source checks

Read the local report/acquisition record. Opened the [author poster](https://www.bruker.com/en/landingpages/bdal/poster-hall-mrms-2020/_jcr_content/root/sections/section/sectionpar/accordion/item_1601303372394.download-asset.pdf/ff5a8435-53b3-4a27-86cc-046e88e244ae/mp-444-structure-and-dynamics-of-inorganic-polymers-in-solution-studied-with-high-resolution-ms--lcms-and-16o18o-exchange-focus-on-polyoxometales.pdf) through the web PDF text reader, independently recovering its one-page parsed text. It supports the report's narrow descriptions of gas-phase oxygen loss, ion-pairing-assisted chromatographic retention and oxygen exchange with solvent. It does not establish Mo34WV behavior, an intact unchanged metal framework during exchange, new framework production or inherited competence. No rates, spectral assignments or quantitative parameter values were imported by this review.

Direct opening of [PubMed PMID35756945](https://pubmed.ncbi.nlm.nih.gov/35756945/) returned a browser-check page in this review. A targeted DOI search recovered the bibliographic record and the [primary publisher abstract](https://pubs.rsc.org/en/content/articlehtml/2022/qi/d1qi01618k). The abstract supports the reported distinction between solution mixed-valence decavanadate and electrospray artifacts via differing chromatographic profiles. This independently corroborates the report's abstract-level claim; it does not verify every historical root acquisition event or detailed methods. The unresolved amine-naming statement is explicitly investigator-reported, so it is not promoted to independently verified chemistry.

## Retained failed response

Independently read and hashed the retained `raw/poster-response.body`:293 bytes, SHA256 `e6b1fc626ab1d3c1d3df093c2dcdd61fac27477c8c1debe4bd4fe82c8646a653`. It is HTML labelled406 Not Acceptable, not PDF. `raw/poster.headers`:271 bytes, SHA256 `150914dd12abcf31dd542b5ea37e29ee486a51267a46421d51c461d34f3c11b3`; statusHTTP/2 406 and content-length293. Both hashes match acquisition.json. Thus the recorded curl exit0 is correctly separated from source-byte acquisition. No direct failed download was repeated.

## Measurement interpretation

The proposed before/after-column comparison, column-free aging control, recovery accounting and competence measurement in collected fractions address assay-induced change rather than assume chromatographic peaks faithfully preserve the original target. Source-energy variation, blanks, washout, spike recovery, disabled controls and additive/acidity intervention accounting are proposals, not evidence that the assay has already been qualified.

The precursor-free founder plus labelled-water control is a useful exchange baseline. The report correctly states that extra isotope incorporation after precursor addition alone cannot distinguish growth from changed exchange kinetics. It additionally requires framework-sensitive ancestry and founder accounting, and retains metal exchange/recycling controls. It explicitly denies both inference of new framework/inherited competence and inference that the old framework necessarily stayed intact. No isotope-control result is claimed.

The desired recovery-corrected solution-resolved competent fraction is a proposed observable. Source V10 observations under analytical additives do not establish compatibility, kinetics, stability or target identity in acidic Mo34WV. No raw spectra, chromatograms or active-retention dataset is admitted, and no numerical thresholds are invented. Aggregate24/0 is carried as context, not independently recounted in this narrow review; zero new roles/complements is consistent with this follow-up's scope.

## Perspectives and limits

Programming/remove-ai-slops perspectives were already loaded and consulted: this is prose/evidence review with no executable production/test diff, so no prose-pinning tests or code cleanup is warranted. No implementation complexity violations apply. No native computation, physical assay, fitting, simulation, held-out geometry or live parent outcome was inspected or executed. No source report/code was edited; only this review and the separately assigned plan-review append were written.

No visual poster/figure verification, full article byte acquisition, supplement or raw dataset audit was performed. The approval covers the narrow claims and proposed controls only; identity, retention, competence, new-framework formation and inheritance remain unmeasured.
