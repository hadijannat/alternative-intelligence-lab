# Primary acquisition: Wei 2025 spatial Fe function

Acquired 2026-10-18. Target DOI: [10.1021/jacs.5c00438](https://doi.org/10.1021/jacs.5c00438), Jie Wei and colleagues, *Role of Site-Specific Iron in Fe-Doped Nickel Hydroxide Toward Water Oxidation Revealed by Spatially Resolved Imaging at the Single-Particle Level*, JACS 147(16), 13502–13511 (2025).

## Acquisition boundary and result

The exact primary supporting-information file is acquired and verified. The main article's native body/PDF has not been acquired. The publisher's indexed primary page offers purchase and exposes its abstract/SI description. This is a source-methods audit; no current-response digitization, kinetic fitting or held-out performance test was performed here.

`sources/dedup.json` records a scoped exact-DOI search before acquisition: existing continuation/audit references were found, with no native file identified in that search. This is not a claim about every file on the computer.

## Routes and preserved failures

`sources/acquire.py` and `sources/receipt.json` preserve seven direct requests, bodies and metadata:

| Route | Observed result |
|---|---|
| ACS DOI landing page | HTTP 403, response retained as `acs-doi.html` |
| ACS migrated `jacsat/article/147/16/13502/3771257/...` page | HTTP 403, response retained as `acs-new.html` |
| Crossref main DOI | HTTP 200, `crossref.json` |
| Crossref SI DOI | HTTP 429, zero-byte `crossref-si.json`; not an acquired SI record |
| Figshare exact `resource_doi` query | HTTP 200, one exact match, record 28718969 |
| Figshare exact SI DOI query | HTTP 200, same record |
| Figshare title query | HTTP 200, first 100 records; only exact target among those records was 28718969; this is a bounded search |

`sources/acquire_si.py` then fetched the [primary Figshare metadata](https://api.figshare.com/v2/articles/28718969) and its listed [native file](https://ndownloader.figshare.com/files/53382659), both HTTP 200. `sources/si-receipt.json` preserves request/resolved URLs, sizes, hashes and verification results. The signed resolved S3 URL is a transient download redirect; use the stable Figshare file URL for reacquisition.

Additional web searches on the exact DOI plus FeLPD/Data/1.50/1.60 produced many near-DOI false matches (`jasms.5c00438`, `jacsau.5c00438`), excluded. Title/PDF, FeLPD/Wei, institutional-domain and title/1.50 queries yielded the primary ACS abstract/SI listing, but no additional native main article or machine-readable dataset was identified. These search observations are supplementary to the captured direct-request receipts, not raw-file acquisition evidence.

On 2026-10-18 the parent agent also checked the exact migrated publisher URL in a normal IAB browser. The publisher redirected to `article-abstract` with `redirectedFrom=fulltext`, displayed “You do not currently have access to this content”, and offered $48 pay-per-view. The abstract and SI description were visible; the latter explicitly described TOFs normalized by overall Fe. No login or purchase was attempted. This dated note records the parent agent's observed browser access verdict; it is not a native main-article acquisition or a saved UI transcript. The browser check establishes that the direct-request 403 was not the only access limitation.

## Native inventory and reuse

| Native file | Type/pages | Bytes | SHA-256 |
|---|---|---:|---|
| `sources/ja5c00438_si_001.pdf` | valid PDF, 35 pages | 1,342,459 | `658e8a17f67d282b219ea77cefb59aa59dccfe1deb06555b7a7a3f93e1f6dca1` |

Native MD5 `e08c00938f919d0bd21ffc76112e8ec6` and size both match publisher Figshare metadata. Its resource DOI is exactly the main DOI; its SI DOI is `10.1021/jacs.5c00438.s001`; posted 2025-04-02. The record specifies **CC BY-NC 4.0**. This license applies to this SI record; do not transfer it to the paywalled main article. Main Crossref license entries are STM publisher policies, not an open Creative Commons license. No license inference from public accessibility was made.

The acquired primary record advertises one PDF, with no embedded attachments. There is no CSV/XLSX/raw SECCM image matrix, raw Raman series, ICP replicate table or VASP coordinate archive in this acquired package. This is a package-level statement, not proof none exists elsewhere. Main-article data-availability wording remains unverified.

## Reproducible evidence

Run from repository root:

```sh
python3 documented-scaffold-2026-10-18/spatial-fe-function/sources/verify_sources.py
```

Binary observable: `all_pass: true` plus exit code 0. Artifact: `sources/verification.json`. The scenario checks exact DOI identity, PDF signature, publisher MD5/size, page count, file inventory, embedded-file absence and nonempty text/renders. It validates acquisition integrity, not scientific conclusions.

Extraction: `sources/ja5c00438_si_001.pdf.txt` (PyMuPDF, page-delimited). Visual methods artifacts: `sources/si-methods-page-2.png`, `-3.png`, `-4.png`. The extraction retains the complete document text; only methods/captions were audited. No plotted current-response points were extracted or fitted. Reported total-Fe loading descriptors were encountered during the methods read, so subsequent analysis must disclose this paper-informed exposure.

No purchases, author contact, login changes or new packages were used. An active OMO attempt was checked but the toolkit returned `ULW_LOOP_PLAN_MISSING`; the captured source evidence remains inside the assignment's owned directory.
