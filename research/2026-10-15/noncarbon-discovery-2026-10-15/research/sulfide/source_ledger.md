# Primary-source ledger

Checked 2026-10-15. “Downloaded” means local bytes acquired; “read” includes tool-visible publisher or author text; neither implies experimental replication. This screen used no secondary review as evidential support.

| ID | Primary source / data | Access and local record | Used for / limits |
|---|---|---|---|
| S1 | Wilkin & Beak 2017, [10.1016/j.chemgeo.2017.04.023](https://doi.org/10.1016/j.chemgeo.2017.04.023) | PMC primary text read; XML access failed 500. | Ni uptake, phase and environmental constraints; not heredity. |
| D1 | EPA [10.23719/1374560](https://doi.org/10.23719/1374560), [catalog](https://catalog.data.gov/dataset/wilkin-and-beak-2017-chemgeol-v462-p15) | `raw/nickel-mackinawite.csv`, catalog HTML. Exact file URL retained below. | Uptake/spectroscopy source data; header rows and spectra are not replicates. |
| S2 | Le Pape et al. 2026, [10.5194/ejm-38-135-2026](https://doi.org/10.5194/ejm-38-135-2026) | `raw/feS-2026.html`, `.txt`. | Phase drift; raw data available on request. |
| S3 | Taran 2017, [10.3389/fchem.2017.00049](https://doi.org/10.3389/fchem.2017.00049) | Full primary text read online. | Surface redox; organic quinone part cannot support carbon-free organization. |
| S4 | Hoenig et al. 2024, [10.1038/s41467-024-52109-8](https://doi.org/10.1038/s41467-024-52109-8) | `raw/mos2-pores.xml`, `.txt`. | Ion transport/irreversible pore etching; organic processing present. |
| D2 | Hoenig et al. [10.5281/zenodo.13117482](https://doi.org/10.5281/zenodo.13117482) | `raw/zenodo_record.json`, five `mos2-fig*.csv`. Official API succeeded after web 429. | CC-BY-4.0 source data; full raw data and processing code also described as on request in paper. |
| S5 | Ran et al. 2025, [10.1038/s41467-025-62592-2](https://doi.org/10.1038/s41467-025-62592-2) | `raw/mos2-operando.html`, `.txt`. | Direct Ag filament evidence, fabrication confounds and failure dynamics. |
| D3 | Ran et al. [source XLSX](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-62592-2/MediaObjects/41467_2025_62592_MOESM8_ESM.xlsx) | Link identified in primary HTML; not downloaded. | Figure data only; supplementary videos also linked. |
| S6 | Braun et al. 2023 primary manuscript, [arXiv:2309.13900](https://arxiv.org/abs/2309.13900) | `raw/polymer-residues.pdf`, `.txt`. Journal publication status not established. | PtSe2/PMMA controls; general attribution confound, not universal carbon necessity. |
| S7 | Xie et al. 2025, [10.1038/s41565-025-01988-z](https://doi.org/10.1038/s41565-025-01988-z) | Publisher abstract, figure descriptions and data statement read. | Fabricated BN memory comparator; data/code on request. |
| S8 | Mondal et al. 2024, [10.1002/aenm.202400809](https://doi.org/10.1002/aenm.202400809) | Primary publisher indexed text read. | Phosphide reconstruction; do not assume nominal phase is active state. |
| S9 | Liu et al. 2024, [10.1002/anie.202315034](https://doi.org/10.1002/anie.202315034) | Primary publisher/author institution abstract read. | Co3Mo3N surface transformation; no quantitative fitting. |
| S10 | WS2 device study 2024, [10.1088/1361-6528/ad6006](https://doi.org/10.1088/1361-6528/ad6006) | Primary abstract/PDF search text only. | Screened, not promoted; full methods and data not audited. |

Exact D1 download: `https://pasteur.epa.gov/uploads/10.23719/1374560/Wilkin%20and%20Beak%20%282017%29%20ChemGeol%20v462%20p15.csv`

D2 API: `https://zenodo.org/api/records/13117482`; the returned file URLs and checksums are retained in its JSON. Local SHA256 values and source-table dimensions are in `data_audit.json`. The two large ZIP files listed by the repository were not downloaded.

`raw/phosphide-reconstruction.html` and its extracted text are a saved browser challenge from an attempted separate ACS/PMC lead (PMC10900598), not evidence supporting any report conclusion. No hidden conversion of failed access into “reviewed data” is intended.

No measured fitting or held-out validation occurred in this research subtask. Candidate novelty is unestablished; all named compound families already exist in the cited literature.
