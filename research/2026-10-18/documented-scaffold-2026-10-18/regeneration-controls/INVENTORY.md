# Acquired regeneration files: byte and acquisition audit

All **481 acquired files, 55,239,493 bytes**, were independently rehashed against both the deposited SHA-1 values in `dataverse.json` and acquisition SHA-256 values in `data-receipt.json`. Every checksum and size matched. The local data tree exactly matches receipt paths. The full deposit has 638 entries; this audit covers the acquired subset and uses the full metadata for gap checks.

`file_manifest.json` records every file's deposit identifier, path, bytes, SHA-256, repository checksum, declared MIME, observed magic/format, specimen directory, selected acquisition headers, table columns/units/row counts, and time ranges. It contains no numerical potential/current observations or response endpoints. `file_manifest.csv` is the compact per-file index. Source files were opened read-only.

## Native formats and integrity

| Observed format | Files | Scope |
|---|---:|---|
| Gamry plaintext | 462 | 460 `.DTA` and two misnamed `.xls` files |
| Plaintext | 6 | Five processed traces and the author's opening instructions |
| Empty | 8 | Deposited and acquired as zero bytes; preserved |
| Origin OPJU | 4 | `CPYUA` magic; not independently decoded into graph series |
| XLSX | 1 | ZIP CRC passed; one worksheet, declared A1:CH201, 201 row elements |

The 462 nonempty Gamry files contain 494 tables. Parsed row widths are consistent. Every explicit table row count agrees with the parsed count; 56 tables omit a declared count and remain marked as unknown. Every Gamry file yielded at least one table. There are no nonempty exact-byte duplicates. The only duplicate hash group contains all eight empty files. Processed files and Origin projects are derived representations, so their absence from an exact-hash duplicate group does not make them independent experiments.

`RU.xls` and `WNi79T.xls` in WNi79T are Gamry text despite the extension. `RUfinal.xls` is empty. Dataset MIME labels therefore cannot be trusted as parsers. Comma decimal notation occurs in raw DTA; time fields are parsed after comma-to-point conversion. Native units remain explicit.

## Acquisition groups and clocks

Dates below are native header dates, with day/month ordering as printed. They describe recorded files rather than randomized replicate assignment. Specimen labels are folder identifiers; they do not independently prove physical coupon identity or replicate independence.

| Figure group | Specimen | Files | Main schedule and native date span |
|---|---|---:|---|
| 2a | WNi78T | 90 | 43 OER blocks, each6000s/401points;43regeneration files, nominally100s but final Regen43 records only6s;16–19March2022. A separate86400s CHRONOP tail follows a >3h gap and EIS; see AMENDMENTS.md. |
| 2a | WNi79T | 3 | Continuous CHRONOP, 8378 points, 0–251310 s; 21 March 2022 |
| 3a | WNi175T-A | 5 | Continuous CHRONOP, 17281 points, 0–259200 s; headers 16–22 May 2023 |
| 3a | WNi194T-A | 5 | Continuous CHRONOP, 17281 points, 0–259200 s; 14–17 July 2023 |
| 3a | WNi197T-A | 5 | Continuous CHRONOP, 17281 points, 0–259200 s; 21–24 July 2023 |
| 3b | WNi176T-A | 92 | 43 OER blocks, each 6000 s/201 points; 43 regeneration blocks, each 100 s/2001 points; 22–26 May 2023 |
| 3b | WNi198T-A | 91 | 43 OER blocks, each 6000 s/401 points; 43 regeneration blocks, each 2010 points spanning −0.45–100 s; 25–28 July 2023 |
| 3b | WNi99T | 90 | 43 OER blocks, each 6000 s/201 points; 43 regeneration blocks, each 100 s/2001 points; 21–27 June 2022 |
| 6b | WNi214T-A | 4 | Continuous CHRONOP, 15486 points, 0–232275 s; 7–10 November 2023 |
| 6b | WNi225T-A | 91 | OER 1–40 each 6000 s/201 points; regeneration 1–40 each 100 s/2001 points; later raw acquisition gaps below; 8–11 December 2023 |

Six files are at figure/root level, giving 481 total. The author's `How to open the data.txt` says regeneration loops produce multiple DTA files subsequently joined into `SampleName_processed.txt`. Those files label their columns `Hours` and `Potential (mV)`. The four complete processed records end at 71.66666667 h, matching 43 × 6000 s OER time; 43 × 100 s regeneration adds 1.19444 h to the prescribed protocol, plus any other acquisition delays. Do not treat processed `Hours` as the full wall clock or assume its potential column has undergone a particular reference conversion merely from its name. Every table time sequence parsed is monotone; WNi198T-A's negative pre-step times must remain distinguished from positive pulse time.

## Metal-supply matching evidence and unresolved mapping

The folder and deposit metadata identify figure panels and specimen codes; they do **not** attach Fe concentration to each coupon. Neither acquired article text nor supporting-information text contains the WNi specimen identifiers. Consequently this inventory does not assign concentrations from directory sorting.

Printable metadata in `Fig. 3b/Reg overley AEM.opju` names WNi99T-A, WNi176T-A and WNi198T-A, and includes `\\l(2) 100 ppb Fe` and `\\l(3) 5 ppm Fe`. In `Fig. 3a/Overlay no reg AEM.opju`, the concentration legend order differs: `\\l(3) 100 ppb Fe`, `\\l(2) 5 ppm Fe`. These support candidate matched supply panels, but do not by themselves resolve the complete sample-to-plot binding. An independently decoded Origin graph/worksheet relation or source-author mapping is required before assigning sample-level metal-supply effects. Figure-level matching also requires the source's geometry, electrolyte, current, pretreatment and timing controls.

`Fig. 2a/commercial KOH.opju` includes WNi79T-A and **WNi98T-A**, whereas the acquired regenerating folder is **WNi78T**. This naming discrepancy is preserved; neither spelling was silently substituted. Source preprocessing comments embedded in Origin are evidence of processing history, not permission to apply transformations to raw data without resolving their reference and physical meaning.

## Missing and empty data retained

- WNi79T/RUfinal.xls is empty.
- WNi225T-A/CVfinal.DTA and RuFinalZ.DTA are empty.
- WNi225T-A/Regen_41.DTA, Regen_42.DTA and Regen_43.DTA are empty.
- WNi225T-A/WNi225T-A_42.DTA and WNi225T-A_43.DTA are empty.
- **WNi225T-A_41.DTA is absent from both the acquisition and all 638 deposited metadata entries.**

Despite those late raw gaps, `WNI225T-A_processed.txt` contains 8643 rows with a 0–71.66666667 h clock, the same count as 43 full 201-point blocks. Its final three nominal blocks require a separate numerical/provenance check. This inventory does not treat that processed tail as observed raw support and has not read out its potential values. Book1.xlsx declares 201 rows across 86 columns, also requiring a later worksheet/raw relationship check before any fill or reconstruction is accepted.

## Reproduction and evidence

Scenario: audit every acquired entry without exposing numerical response observations.

Invocation, from repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/regeneration-controls/inventory.py
```

Observed final result: exit 0; 481 exact-path records; all repository and acquisition hashes/sizes match; zero explicit-count mismatches. Artifact: `file_manifest.json` (`summary` and all per-file records), plus `file_manifest.csv`. The script's synthetic self-check verifies comma-decimal time parsing, declared and undeclared table counts, zero-byte classification, and that synthetic potential values are excluded from extracted table metadata.

Preserved implementation failures: the first run rejected a native CV `TABLE` with a blank count; the parser now records that count as null. Inspection then found EIS/CV markers with no trailing tab, omitted by the initial table matcher; the matcher now recognizes both legal observed forms, and a synthetic regression check covers the absent-count form. The complete inventory was rerun after these fixes. These are parser failures, not chemical-model results.

No response fitting, causal classification, active-metal attribution, or reconstruction of Origin numerical series was performed in this inventory. A checksum pass verifies deposit identity, not scientific validity or independence.
