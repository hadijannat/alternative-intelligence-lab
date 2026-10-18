# Primary source acquisition

Target: Zhao, Zhang, Ye et al., *Remote Iron dynamics of NiFe (oxy)hydroxides toward robust active sites in water oxidation*, Nature Communications **16**, 5601 (2025), [DOI 10.1038/s41467-025-60728-y](https://doi.org/10.1038/s41467-025-60728-y), [PMC12216224](https://pmc.ncbi.nlm.nih.gov/articles/PMC12216224/). Native main, all five linked attachments, publisher HTML, PMC HTML, BioC XML, and Crossref metadata were acquired directly.

## Actual access and files

`sources/receipt.json` records five initial requests. Direct Python urllib requests returned HTTP 200 for Nature HTML, PMC HTML, BioC XML, and Crossref. The attempted legacy PMC OA API URL returned HTTP 404; its body remains saved. The web-tool PMC open separately returned a browser challenge, whereas the direct saved PMC response contains the article. These are different observed routes, not contradictory acquisition claims.

`sources/acquire_attachments.py` discovers the five attachment links from the acquired Nature HTML and downloads the exact observed links from `media.springernature.com`. It also downloads the native article PDF from the publisher. `sources/attachment-receipt.json` records all six successful HTTP 200 responses, exact URLs, bytes and SHA256 hashes. No subscription, author contact, browser session, new dependency or inferred attachment filename was required.

| File | Acquired content | Bytes |
|---|---|---:|
| `main.pdf` | Native article, 12 pages | 1,473,710 |
| `41467_2025_60728_MOESM1_ESM.pdf` | Supporting information, 27 pages | 1,726,376 |
| `41467_2025_60728_MOESM2_ESM.pdf` | Description of additional files, one page | 173,257 |
| `41467_2025_60728_MOESM3_ESM.zip` | 17 optimized-structure CIF files and two directory entries | 44,337 |
| `41467_2025_60728_MOESM4_ESM.pdf` | Transparent peer review, 32 pages | 1,922,634 |
| `41467_2025_60728_MOESM5_ESM.xlsx` | Published numerical source data, 19 worksheets | 2,196,285 |

The structure ZIP is DFT geometry data, not experimental transport trajectories. It describes original/defective Ni0.75Fe0.25OOH models and the defect arrangement used for the Fe-capture calculations. The source workbook supplies figure-level numbers and traces. Its status as a published source-data workbook should not be inflated into original instrument exports with every independent replicate.

## Identity, license and scope

Native main DOI, SI title/authors, BioC DOI/PMCID, file magic and ZIP integrity were checked. Every acquired response body matches its saved SHA256 and byte count. Full hashes and inventories are in `sources/acquisition-checks.json` and the request receipts.

The article explicitly uses **Creative Commons Attribution–NonCommercial–NoDerivatives 4.0**, [license terms](https://creativecommons.org/licenses/by-nc-nd/4.0/). This is not CC BY 4.0. The paper's statement covers included images/material unless separately credited. A distinct license for the numerical source workbook or CIF archive was not established by this audit. Local source copies are retained unchanged; scientific analysis is kept separate from deposited material.

Native PDF text was extracted with installed PyMuPDF. `sources/main-passages.json` and `methods.txt` derive from the acquired PMC BioC XML. `sources/workbook-structure.json` records sheet names, declared dimensions, and **text cells from the first five rows only**. Numerical response values were not printed, extracted into a response table, plotted or fitted during this methods audit. The source's qualitative conclusions and rounded results were already exposed through the paper, so later tests are retrospective and paper-informed.

## Reproduction and captured observables

From the repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/remote-fe-transport/sources/acquire.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/remote-fe-transport/sources/acquire_attachments.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/remote-fe-transport/sources/inspect_sources.py
```

All commands completed with exit 0. `acquisition-checks.json` records `byte_hashes_valid=true`, `identity_valid=true`, `native_attachments=5`, `main_pdf_acquired=true`, and `workbook_sheet_count=19`. The native ZIP files pass integrity checking. Acquisition success does not validate a physical transport or repair model.
