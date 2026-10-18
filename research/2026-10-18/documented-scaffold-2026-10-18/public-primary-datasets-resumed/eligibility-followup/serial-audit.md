# Independent founder-function eligibility audit

Date: 2026-10-18. Scope: exact Idrees/Reuven/Markovich 2025 source and its already identified seed-method chain. This audit follows `PROTOCOL.md` in this directory. All twelve integrated requirements remain open; PMo12's authorized role is unchanged.

## Decision

**INSUFFICIENT_DATA for an independent founder-function ceiling or serial-inheritance test.** An independently specified precursor inventory can upper-bound the quantity of original-seed terbium introduced, assuming the stated aliquot is representative. The source does not independently calibrate how much adsorption that founder material could cause under the secondary-batch assay conditions. Choosing an occupancy factor from the offspring adsorption response would be circular. A one-molecule-per-Tb ceiling is not validated by the inspected source.

The new evidence progress is successful acquisition of the native supplement through the official Europe PMC `supplementaryFiles` route, preservation of source bytes, and direct inspection of the capacity-model assumptions, controls and source chain. No response dataset was assembled or fitted and no H/V test was run. Root and reviewer consumed Table S6 while reading the PDF; details below.

## Exact article and independently observed preparation

[Idrees, Reuven and Markovich, DOI 10.1021/jacs.4c16883](https://doi.org/10.1021/jacs.4c16883), *High Enantioselectivity in Adsorption of Chiral Molecules on the Surface of Chiral Terbium Phosphate Nanocrystals*. Authors were verified in the current main XML and SI title page.

The main experimental section specifies 285 μL of 100 mM Tb precursor, a 100 μL aliquot from approximately 11 mL of seed suspension, a secondary synthesis without freshly added TA, centrifugation, and use of the resulting precipitate in a 2 mL adsorption assay. The functional assay therefore does use the seed-produced batch. These are preparation inputs, not independently measured surviving-founder mass, surface area or capacity. There is no measured separation of original seed material from newly incorporated material.

Seed-only adsorption is not reported in the inspected methods or SI. The acid-only references calibrate CD/titration, and the ICP-MS experiment compares dissolved Tb/phosphate in water versus ASP exposure. Neither identifies the residual founder's adsorption capacity. Reported phosphate release also cautions against assigning an invariant surface-site formula during the assay. Organic carryover is a potential state-confound, not an automatic structural-carbon exclusion.

## Candidate ceilings and why they do not identify the required contrast

1. **Precursor inventory:** The stated Tb input multiplied by the stated seed-volume fraction supplies a candidate upper bound on founder Tb atoms, under representative sampling and at most complete conversion. This bound is independent of the desired adsorption response. It is intentionally not evaluated numerically here. Recovery into the secondary pellet and isotope-resolved founder survival are unmeasured.
2. **Inventory-to-function conversion:** A useful test additionally needs an independently supported maximum adsorption contribution per founder quantity in the actual medium. A symbolic ceiling would be `Q_founder <= N_Tb,founder,max × q_max`, where `q_max` includes relevant surface changes and non-direct adsorption routes. The source provides no separately measured `q_max` for the original seeds. The source's phrase “same amount” for opposite-handedness NC samples is not such a calibration.
3. **Crystallographic/site estimate:** Crystallography identifies the material and facets; it does not independently establish accessible original-seed surface area or an absolute maximum occupancy under the assay. Three-point molecular anchoring is a proposed geometric explanation, not a calibrated universal number of adsorbates per Tb atom. Neither one nor another chosen stoichiometric multiplier is justified by that discussion.
4. **Langmuir ceiling:** SI page 13 explicitly assumes monolayer adsorption, finite identical sites, and no lateral interactions. The model relates measured adsorbed concentration to fractional coverage; its proportionality/saturation capacity is not independently calibrated for seeds. The main article reports that the racemate extension does not describe the observations, and SI page 10 describes unsaturated adsorption and possible intermolecular stabilization. A fit to the seed-produced batch cannot serve as an independent seed-only ceiling.
5. **TA carryover:** The residual-TA estimate concerns ligand contamination. It does not bound the original seeds' adsorption activity. The 2019 preprint has an explicit geometry/full-coverage TA estimate; absence of a founder-function calibration must not be misreported as absence of every quantitative bound.
6. **Trivial feed ceiling:** Total supplied adsorbate bounds the maximum removable adsorbate independently, but applies equally to the founder-only explanation and whole-batch explanation. It cannot discriminate the desired inheritance claim.

No numeric stoichiometric multiplier was selected from the observed adsorption curves. No test threshold or favorable response point was chosen.

## Control and lineage audit

| Source observation | What it can establish | Missing discriminator |
|---|---|---|
| Idrees 2025 adsorption of purified secondary-batch precipitate | Useful adsorption is assayed in a batch produced with seeds | Original seeds and newly produced material are not assayed separately; no seed-only matched-capacity arm |
| CD calibration and acid-only titration reference, SI p9 | Conversion between solution signal and adsorbate concentration | No independent founder capacity or state-erased material comparison |
| ICP-MS of water/ASP supernatants | Dissolution/material-solution response can be assessed | No founder-specific label or complete retained-solid capacity allocation |
| Langmuir discussion, SI p13, and interaction discussion p10 | Explicit adsorption-model assumptions and limits | No validated monolayer/occupancy ceiling for all relevant founder pathways |
| Schwartz 2023 methods, DOI 10.1002/chir.23523 | Prepared L-seeds added once to L/D-TA feed, with in-situ luminescence/CPL | No adsorption assay or repeated isolated recipient-as-parent lineage |
| Hananel source-chain author preprint, arXiv:1808.05406, SI pp17–19 | Early seeds purified twice, seed dilution followed by growth/CPL; assumption-based TA bound | Not verified final-publication SI; no seed-only adsorption calibration or isolated serial descendants |

The methods describe seed preparation followed by one secondary batch and assay, not a documented succession where isolated recipients become parents. The older optical experiment cannot substitute for an adsorption-capacity calibration on the 2025 seeds: the readout, preparation and physical assay differ. Text searches support this inspection, but absence of a keyword alone is not the basis of the decision.

## Exact missing measurement and next discriminating experiment

A startable founder test would require an independently measured upper adsorption capacity for an original-seed-only control subjected to the same handling, medium, time and dose range, with a conservative upper founder quantity and allowance for surface transformation; alternatively, independently identified newly produced material could be separated and assayed against quantified founder carryover. Repeated isolated recipient-as-parent transfers under the same feed, preserving opposite useful states and matched erased/unseeded controls, remain necessary for the serial claim.

Those measurements are not present in the inspected package. The existing native adsorption tables can support a separately declared bounded adsorption analysis, but cannot supply this missing independent calibration by re-fitting themselves. No physical experiment or author contact is authorized by this audit.

## Native acquisition and captured artifacts

All paths below are under `serial-sources/` beside this file. The earlier failure records and earlier source packages were not changed. New acquisitions used `curl --fail --silent --show-error --max-time 30` (40 seconds for the supplement ZIP) with the exact official URLs below. An initial in-memory `urllib.request.urlopen` to the same routes independently reported HTTP 200; downloaded artifacts were then parsed and hashed locally. ZIP extraction was restricted to the exact named PDF with `unzip -n -j`, preventing overwrites.

| Local artifact | Exact source URL | Bytes | SHA256 |
|---|---|---:|---|
| `idrees2025-main.xml` | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12046555/fullTextXML | 80907 | `f132e272fa0e34b76600454fc94fc5c716064d47506d01224eca15a12f6e6ac7` |
| `europepmc-supplementary.zip` | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12046555/supplementaryFiles | 1202571 | `ccc97cff0220fca801293a474a196f2e18c51a81d48e1e93b94535f83beb689a` |
| `ja4c16883_si_001.pdf` | Exact member of preceding ZIP; deposit alternative https://ndownloader.figshare.com/files/53780128 | 760874 | `3bab9ca7cc2c69a11484b795b383ce82598dbb60824340aa62f626b262359602` |
| `figshare-28823413.json` | https://api.figshare.com/v2/articles/28823413 | 6764 | `2a99c1dc9f882160508bfa6baee7410db0e2d6299c409321256afac8bf94f8fd` |
| `schwartz2023-main.xml` | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10108007/fullTextXML | 57460 | `bc69defd71703e0ae08800020b80c3e5aea35724b793ab5c6b99178e22bf558f` |
| `hananel-preprint.pdf` | https://arxiv.org/pdf/1808.05406 | 1978587 | `6ce5b54efff8dfb6cdf81481da039855082955399a280653f561f2b56d6e44f2` |

The initial in-memory ZIP had the same byte count but SHA256 `2cbc43f470438843c0f6fb273f6398014de6b1d16dd128ab183e2db256875863`; only the later ZIP bytes are saved. The exact PDF member agrees with its earlier SHA256 and with repository MD5 `3aa8545778bb6b3466aa8b81d817cf02`. Therefore archive-level bytes differed between requests while the inspected PDF content remained identical; no byte identity of the two ZIP containers is claimed.

The deposit advertises exactly one PDF under supplement DOI `10.1021/jacs.4c16883.s001`, license CC BY-NC 4.0. The 2025 main XML gives CC BY 4.0. The ZIP also contains article image assets; none were analyzed as numerical responses. SI is a 13-page PDF of plots, tables and methods, not a lineage-indexed CSV/XLSX. No new license determination was made for the older preprint or 2023 XML; their use here is methods inspection.

## Verification and consumed outcomes

Scenarios/invocations/observables: official XML retrieval and `xml.etree.ElementTree` parse succeeded; official supplement ZIP retrieval and `zipfile.ZipFile` member read succeeded; `pypdf.PdfReader` reported 13 SI pages and 25 preprint pages; local SHA256/MD5 checks agree with the table/deposit. These source-access checks are captured by the files above and this receipt. The assay-to-seeded-batch linkage is explicit in the parsed main methods. Independent seed-function calibration established=false; isolated serial recipient transfers established=false; new numerical inheritance test executed=false.

Methods-oriented reading exposed already published prose summaries of adsorption behavior, including explanatory text on SI page 10; these are consumed retrospective observations. The root agent additionally reports direct inspection of SI pages 9, 10 and 13, with full page-10 text extraction exposing Table S6 numerical values. Those table outcomes are therefore now consumed by the team and must not be represented as unseen or held out. No fitting, new numerical calculation or scientific test was performed in this audit; the worker did not extract a new response series into a result. The eligibility decision does not depend on a favorable observed adsorption magnitude. No new literature search, external code execution, contact, purchase or access bypass was performed.
