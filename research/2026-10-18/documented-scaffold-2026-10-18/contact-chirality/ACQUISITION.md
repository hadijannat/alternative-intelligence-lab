# Native source acquisition

Source: Niinomi et al., *Plasmonic Manipulation of Sodium Chlorate Chiral Crystallization: Directed Chirality Transfer via Contact-Induced Polymorphic Transformation and Formation of Liquid Precursor*, Crystal Growth & Design 20 (2020), 5493–5507, [DOI 10.1021/acs.cgd.0c00693](https://doi.org/10.1021/acs.cgd.0c00693).

The native supplement and two relevant movies were acquired on 2026-10-18. The [receipt](sources/receipt.json) records URLs, file sizes, SHA256 hashes and agreement with publisher-deposited MD5 values. The metadata are retained verbatim. Methods discovery was outcome-exposed and retrospective; nothing here is a preregistered or held-out test.

| Source artifact | Native publisher record | Bytes | Check |
|---|---|---:|---|
| cg0c00693_si_001.pdf, 13 pages | [Figshare 12662087](https://api.figshare.com/v2/articles/12662087) | 933404 | MD5 and size match |
| cg0c00693_si_008.mp4, Movie SI7 | [Figshare 12662108](https://api.figshare.com/v2/articles/12662108) | 6992954 | MD5 and size match |
| cg0c00693_si_009.mp4, Movie SI8 | [Figshare 12662111](https://api.figshare.com/v2/articles/12662111) | 8234589 | MD5 and size match |

Movie numbering differs from file numbering because the PDF is file 001. Movie SI7 is contact-triggered transformation; Movie SI8 is the authors' directed chirality-transfer demonstration. The deposited SI metadata specify [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). This does not establish a license for the inaccessible main article.

Reproduction invocation, from the repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/contact-chirality/sources/acquire.py
```

Observed final invocation exited 0 and produced the receipt after the size and MD5 assertions. The first invocation failed with HTTP 500 while downloading Movie SI7. The final receipt preserves two failed query URLs before the successful third query. A preliminary direct PDF request also returned 500, and an ACS-domain download variant returned an empty response. Adding a download query retrieved the native file; no authentication bypass was used. The initial failed script invocation did not produce a receipt and is recorded here rather than counted as success.

The main publisher request returned HTTP 403; its actual response body is saved as `sources/publisher-main-response.html`. The [NYCU institutional record](https://ir.lib.nycu.edu.tw/items/a3bd2336-ee8c-417a-a853-cfd4cc4d942d) supplied indexed citation/abstract material, while its live page rendered a login shell. An OpenAlex DOI query returned only the publisher location and no public PDF. These are bounded access checks, not proof that no accessible manuscript exists. The full main text was not read.

Root subsequently inspected the normal in-app browser after following the DOI. The [native ACS article page](https://pubs.acs.org/cgdefu/article-abstract/20/8/5493/871395/Plasmonic-Manipulation-of-Sodium-Chlorate-Chiral?redirectedFrom=fulltext) explicitly displayed “Available to Purchase” and “You do not currently have access to this content,” with abstract and SI access. This is a primary UI observation reported by root, distinct from this worker's saved HTTP 403 response. No purchase or login was attempted. It confirms the restriction encountered for the main text while leaving the acquired free SI valid.

`ffprobe -v quiet -print_format json -show_format -show_streams <movie>` observed H.264 640×480 videos: SI7 has 268 frames and a container duration of 8.975634 seconds; SI8 has 308 frames and a duration of 10.310300 seconds. These include title cards and are not measured reaction durations.

Contact sheets were generated with the following commands and inspected. The snapshots sample the movies; no trajectory, speed, size, optical rotation or transfer probability was extracted.

```sh
ffmpeg -v error -i documented-scaffold-2026-10-18/contact-chirality/sources/cg0c00693_si_008.mp4 -vf 'fps=1,scale=480:-1,tile=3x3' -frames:v 1 documented-scaffold-2026-10-18/contact-chirality/sources/movie7-contact-sheet.png
ffmpeg -v error -i documented-scaffold-2026-10-18/contact-chirality/sources/cg0c00693_si_009.mp4 -vf 'fps=1,scale=480:-1,tile=4x3' -frames:v 1 documented-scaffold-2026-10-18/contact-chirality/sources/movie8-contact-sheet.png
```

Both commands exited 0. Title cards identify Movie SI7 and SI8 and call playback real time. The scale bars belong to the original source; rescaled contact sheets are only qualitative viewing aids. The native MP4s retain full resolution.

Final integrity check loaded `receipt.json` and recomputed SHA256 for every listed artifact; the binary observable `ALL_RECEIPT_HASHES True` was returned. PDF page positions were independently checked with PyMuPDF: movie captions are on PDF page 11, thermal discussion on pages 5–8, and precursor discussion on pages 2–4.

Previous sources were deduplicated before acquisition: the 2021 sonication study already has a native XML/SI package and founder-bound analysis at `discovery-loop/experiments/chlorate-founder-mass-bound-v1/`; the 2019 initial-breeding paper already has an access/mechanism audit at `discovery-loop/sources/chlorate2021/initial-breeding-audit.md`. Neither is counted as a new acquisition here.

An additional discovery-only lead is Arteaga et al. (2023), [DOI 10.1002/chir.23569](https://doi.org/10.1002/chir.23569), in-situ Mueller-matrix polarimetry of sodium-chlorate cooling crystallization. The publisher abstract supports time-resolved optical-rotation observation; the publisher data statement says data are available on reasonable request. No native dataset was acquired, no author was contacted, and no inheritance evidence from it is admitted.
