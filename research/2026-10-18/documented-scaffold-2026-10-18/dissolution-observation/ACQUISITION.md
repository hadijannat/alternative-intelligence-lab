# Primary acquisition record

Target: Gabriel C. da Silva, Carolin S. Igel, and Serhiy Cherevko, *Setting the Record Straight: A Systematic Study on Fe and Ni Dissolution in NiFe-Based Oxygen Evolution Reaction Catalysts*, ACS Catalysis 16(9), 8633–8641 (2026), [10.1021/acscatal.6c01228](https://doi.org/10.1021/acscatal.6c01228).

## Acquired evidence

**Native main PDF and SI DOCX were acquired through the ordinary in-app browser after the direct requests failed.** Root opened the actual ACS article, clicked its SI Download link and Open PDF anchor, and supplied the browser's downloaded files. Both were copied byte-for-byte into `sources/`, package identity and file magic checked, and text extracted using existing PyMuPDF and Python standard-library XML/ZIP tools.

| Native file | Bytes | SHA256 |
|---|---:|---|
| `cs-2026-01228g.pdf` | 2,037,302 | `e5ae9fa1eacd667d2f464fbdbfd35dbe80c0453d360b423602d76a258fd9b0aa` |
| `cs-2026-01228g_si_001.docx` | 7,850,022 | `7b93a4d8c5920e33fd9222417a393895a193d6f5c7d1a880c1273ce436d43048` |

The PDF has nine pages and visibly states CC BY 4.0. The DOCX ZIP integrity check passed; its title and authors match. The native package contains one XRF table and ten image assets, extracted unchanged into `si-media/`; no raw numeric trace file or embedded workbook was identified. `supporting-information.txt` includes paragraph text and linearized equation tokens, while `supporting-document.xml` preserves complete native equation structure. Extracted text is not a substitute for native equation structure: the structural check in `si-math-structure.json` verifies Eq. S5's actual numerator `0.059` and denominator `3`. The main Figure 1 schematic was rendered separately as `fig1-methods.png`; Figure 6 as `fig6-axis-audit.png`. Only the latter's axis ticks were numerically inspected, with no response-point extraction.

The live native SI link, observed and clicked in the browser, is:

https://pubs.acs.org/accacs/article-supplement/5142681/docx/cs-2026-01228g_si_001/

`sources/browser-main-receipt.json` and `browser-si-receipt.json` record this successful route, original local download paths, byte equality, hashes, and file inventories. `sources/receipt.json` separately preserves 15 direct requests, their status, resolved URL, byte count, hashes, and payloads. Fourteen response bodies were saved; one hostname failed DNS resolution. **Native files acquired by direct HTTP routes: zero; by the normal browser: two.** Files named `*-response.bin` remain HTML failure bodies.

Crossref main metadata confirms the exact title, authors, journal, DOI, and the version-of-record CC BY 4.0 license. Its native PDF link is:

https://pubs.acs.org/accacs/article-pdf/16/9/8633/64857843/cs-2026-01228g.pdf

Crossref component metadata independently identifies [10.1021/acscatal.6c01228.s001](https://doi.org/10.1021/acscatal.6c01228.s001) and the registered SI URL:

https://pubs.acs.org/doi/suppl/10.1021/acscatal.6c01228/suppl_file/cs6c01228_si_001.pdf

This **PDF** registration differs from the actually downloaded **DOCX** attachment on the live publisher page. The live attachment supersedes the stale/different route for acquisition without erasing its failure receipt. The component metadata and acquired SI do not establish a separate SI license; the main-article license must not silently be treated as a separately verified SI license.

`sources/publisher-indexed-methods.json` retains the earlier web-tool response to three targeted ACS searches for volume, calibration, and detection limit. Its decoded text contains omissions and duplicate passages. The final methods audit uses the native files, which supersede those excerpts for source interpretation.

## Preserved failures and availability limits

| Route | Observed result |
|---|---|
| New ACS article HTML; DOI HTML | HTTP 403, HTML saved |
| Crossref-advertised native main PDF | HTTP 403, HTML saved |
| Conventional DOCX SI route inferred from advertised type | HTTP 403, HTML saved; guessed filename explicitly unverified |
| Registered SI PDF and SI DOI redirect | HTTP 403, HTML saved |
| Figshare resource DOI and exact SI DOI search | HTTP 200, empty arrays |
| Figshare general title, exact-phrase title, Fe/Ni dissolution search | HTTP 200, returned unrelated records; no exact source identified |
| `publications.fz-juelich.de` search | DNS failure |
| `juser.fz-juelich.de` DOI search | HTTP 200, 248-byte JavaScript challenge; no returned bibliography/data |

Additional web searches for the exact title, DOI, registered SI filename, and institutional copies did not supply a raw data deposit. The acquired SI provides plotted data and one composition table, not original instrument traces. No separate raw numeric deposit was located. This is **not proof that the authors possess no data or that no deposit exists**.

The primary source is open access. No paywall bypass, account creation, subscription, author contact, or purchase was performed. Before the successful ordinary browser acquisition, root's optional Tier 1 engine failed because its optional dependencies/API key were unavailable; its 18 recorded route attempts were mostly dependency failures, not 18 actual publisher requests. Root owns that fallback provenance separately. The direct HTTP failures remain preserved here.

## Reproduction and binary observables

From the repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/dissolution-observation/sources/acquire.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/dissolution-observation/sources/ingest_browser_si.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/dissolution-observation/sources/audit_downloads.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/dissolution-observation/sources/audit_axes.py
```

The acquisition command captures direct network outcomes. The ingestion command requires the two already acquired browser downloads at the recorded local paths; it does not automate the browser. The ingestion and audit commands completed with exit 0. `sources/acquisition-checks.json` records `receipt_hashes_valid=true`, `metadata_identity_valid=true`, `direct_route_native_article_or_si_files_acquired=0`, and `native_article_or_si_files_acquired=2`. These establish actual source acquisition and byte identity, not empirical model validity. All negative access outcomes remain retained.

The axis-audit command also completed with exit 0. It asserts four left and five right major ticks with a common zero, then records the graphical conversion in `sources/fig6-axis-calibration.json`. Its reported `response_points_extracted=0` defines the scope. The ingestion command's mathematical-structure assertion independently verifies the 0.059/3 fraction and saves the actual native XML subtrees; it prevents the linearized-text false alarm from being treated as a chemical finding.
