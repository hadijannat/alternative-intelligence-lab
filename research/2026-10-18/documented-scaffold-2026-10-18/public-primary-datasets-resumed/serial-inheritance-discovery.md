# Public serial functional inheritance: discovery record

Date: 2026-10-18. Scope: inorganic solid-material H/V component data. This is a metadata/methods/access screen, not an executed scientific test. No response values were extracted, digitized, fitted, or recomputed. Parent agent assigned this exact evidence file after completion of the read-only search; no other file was changed by this worker.

## Decision

No eligible public native dataset was established among the three records below. This bounded search does not show that qualifying data do not exist. None closes H/V or any other full12 criterion. A usable test would require traceable recipient-as-parent generations, useful function measured for inherited variants under common feed, unseeded/state-erased controls, and an independently calibrated residual-founder/function bound. Nominal seed volume, offspring images, and bulk optical accumulation cannot substitute for those conditions.

## 1. Silver nanoparticle autocatalysis

- Primary article: McGlothin et al., DOI [10.1002/anie.202413444](https://onlinelibrary.wiley.com/doi/full/10.1002/anie.202413444), *Autocatalytic Nucleation and Self-Assembly of Inorganic Nanoparticles into Complex Biosimilar Networks*.
- Access: publisher full text inspected. Data statement points to article/SI. Listed file: `anie202413444-sup-0001-misc_information.pdf`, 4.2 MB. [Exact SI link](https://onlinelibrary.wiley.com/doi/suppl/10.1002/anie.202413444/supinfo/anie202413444-sup-0001-misc_information.pdf). Both web click and direct opening returned `Internal Error`; SI contents and native headers were not inspected. File license unverified. No separate native-data repository established.
- Methods/axes: extinction spectrum/time, NTA particle concentration/time, TEM/LPTEM image sequences. AgNO3/citrate under illumination; citrate is an explicit surface ligand/reaction participant. Some surface experiments use polyelectrolyte-functionalized grids. Native specimen, replicate and lineage fields unavailable.
- Generations: article describes mother→daughter→granddaughter imaging events and says particles need not be identical. Therefore **generations are present**, but isolated serial common-feed functional transmission is not established. No inherited functional variants or calibrated founder-function bound found in inspected main text.
- Classification: `PUBLIC_ARTICLE_ADVERTISED_SI_UNINSPECTED`; native-data test not startable. Useful component evidence concerns autocatalytic particle formation; no H/V closure.

## 2. Luminescent terbium-phosphate nanocrystals

- Primary article: Schwartz, Hananel and Markovich, DOI [10.1002/chir.23523](https://onlinelibrary.wiley.com/doi/full/10.1002/chir.23523), *Circularly polarized and total luminescence as probes of nucleation and growth in chiral nanocrystals*. Publisher full text succeeded after an initial error. [Publisher syndication](https://www.sciencedirect.com/org/science/article/pii/S0899004222016729) also inspected.
- Data availability explicitly says “Data available from the authors upon request.” No public native file, license, header, specimen identifier or replicate field established.
- Methods/axes: Eu-doped TbPO4 hydrate; total emission I and CPL ΔI versus time; 704-nm emission and 365-nm excitation. L-seeds prepared with L-tartaric acid are centrifuged and added to L/D-tartaric-acid precursor at start versus late induction. Tartaric acid is an active chiral feed director; inorganic lattice composition does not prove removal of organic surface carryover.
- Limits: one seed-to-batch comparison; no serial recipient-as-parent rounds or state-erased arm identified. Seed volume is not a measured founder-function bound. Authors interpret later CPL qualitatively owing to scattering uncertainty.
- Classification: `PUBLIC_ARTICLE_ON_REQUEST_NATIVE_DATA`; no executable public-data H/V test. Conditional component test would compare early/late-seed CPL with measured founder-luminescence adjustment, after protocol freeze and native-data eligibility. It was not executed.

Follow-up discovery only: PNAS DOI [10.1073/pnas.1821923116](https://doi.org/10.1073/pnas.1821923116), *Spontaneous and directed symmetry breaking in the formation of chiral nanocrystals*, surfaced a racemic-tartaric-acid seed study. Direct [PMC page](https://pmc.ncbi.nlm.nih.gov/articles/PMC6561299/) returned CAPTCHA; search excerpts were not promoted to verified native data. A 2026 adsorption follow-up at [Molecules 31/18/3187](https://www.mdpi.com/1420-3049/31/18/3187) returned HTTP 429. Neither is counted as a verified candidate deposit.

## 3. Chiral plasmonic superlattice deposit

- Exact deposit: [10.5281/zenodo.14736840](https://zenodo.org/records/14736840), *Chiral plasmonic superlattices from template-assisted assembly of achiral nanoparticles*; Luis Alberto Pérez; v1, published/created 2025-01-25.
- Direct repository page inspected: metadata public, files **restricted**. No public filenames, sizes, checksums or native columns were exposed. Rendered License heading contained no value, so license remains unverified.
- Associated [PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11830766/) returned CAPTCHA. Hidden data content was not inferred.
- Classification: `PUBLIC_METADATA_RESTRICTED_FILES`. Axes, lineage, replicate and specimen fields unavailable for inspection. No public-data test startable; no H/V claim.

## Verification scenarios and binary observables

All invocations below used `tools.web__run` through `functions.exec`; the conversation tool results are the original retrieval trace. This file is the authored captured evidence record, not a raw downloaded-source archive.

| Scenario | Exact invocation | Binary observable | Captured artifact |
|---|---|---|---|
| Silver data-route eligibility | `open: [{ref_id: "https://onlinelibrary.wiley.com/doi/full/10.1002/anie.202413444"}]`; `find` for `Data Availability`, `Supporting Information`, `generation`; `click` link 74; direct SI URL open | Main article readable: yes. Advertised SI inspected: no. Native serial functional test ready: no. | This file, record 1 |
| Lanthanide data-route eligibility | `open: [{ref_id: "https://onlinelibrary.wiley.com/doi/full/10.1002/chir.23523"}]` plus publisher syndication URL above | On-request native-data statement present: yes. Public native file established: no. H/V test ready: no. | This file, record 2 |
| Zenodo public-file eligibility | `open: [{ref_id: "https://zenodo.org/records/14736840"}]`; `find` for `Files` and `License` | Metadata readable: yes. Files explicitly restricted: yes. Public native-file inspection: no. | This file, record 3 |

No numerical test was executed. Missing access or required experimental dimensions are eligibility failures, not scientific null results.

## Exact search-query log

All 25 entries were passed literally as `q` values in `tools.web__run({search_query: [...]})`. The numbered order is the query order across calls. Results included irrelevant hits; only inspected primary records above support conclusions.

1. `site.zenodo.org "chirality" "replication" gold`
2. `site.figshare.com "nanoparticles" "chirality" "inheritance"`
3. `site.researchdata.gla.ac.uk inorganic reproduction dataset crystal`
4. `site.zenodo.org "self-replication" nanoparticles`
5. `site.figshare.com "self-replication" "silver"`
6. `site.deepblue.lib.umich.edu/data "replication"`
7. `"chiral" "nanoparticles" "generations" replication`
8. `"McGlothlin" "self-replication" data`
9. `"silver" "self-replication" "data availability"`
10. `"inorganic" "inheritance" "Source data" crystal`
11. `"chirality" "serial" "nanoparticles" replication`
12. `"202413444" data`
13. `"inorganic" "serial propagation" crystal`
14. `"crystal" "domain inheritance" dataset`
15. `"McGlothin" "dataset"`
16. `"chiral" "secondary nucleation" "catalytic" data`
17. `"crystals" "serial transfer" "optical"`
18. `"23523" "data" chirality`
19. `"terbium phosphate" "seed" data luminescence repository`
20. `"Circularly polarized and total luminescence" dataset`
21. `"terbium phosphate" "seed" "zenodo"`
22. `"terbium phosphate" "secondary nucleation" data`
23. `"Autocatalytic Nucleation" "data" McGlothin repository`
24. `"terbium phosphate" "amplification" "data availability"`
25. `"Hananel" "seeds" nanocrystals 2019`

Other source-access observations: Michigan dissertation handle `https://deepblue.lib.umich.edu/handle/2027.42/176658` returned `Internal Error`; no thesis dataset inspected. A search surfaced the excluded Luan DOI, but it was not promoted or counted as fresh evidence. Simulations, organic replicators, unrelated metadata and review results were not treated as native inorganic inheritance data.

## Scope and risk

No large downloads, source-code execution, response extraction, fitting, contact, purchase or restricted-access attempts. Main-text statements and public repository metadata establish this screen only. Required serial-lineage/control/bound data may exist elsewhere or in inaccessible files; they remain unverified.

Memory was used only for the pre-existing evidence boundary (functional assays and founder bounds), not as current dataset evidence: `/USER_HOME/.codex/memories/MEMORY.md`, lines 336–337 and 356. Source facts above were checked live where explicitly stated.

## Targeted follow-up: PNAS source chain and 2025 adsorption function

This append records a separately requested exact-source follow-up on 2026-10-18. The original 25-query log remains intact. Four additional, targeted queries were issued: `"pnas.1821923116.sapp.pdf"`; `"1821923116" "seed"`; `"ja4c16883_si_001.pdf"`; `"Spontaneous and directed symmetry breaking" "seed" "racemic"`. No generic discovery expansion or numerical test was performed.

### PNAS 2019: final-publication access unresolved; author preprint methods inspected

- [Europe PMC final fullTextXML endpoint](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6561299/fullTextXML): web tool inaccessible; direct standard-library `urllib.request.urlopen` returned HTTP 500 on three attempts. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6561299/) still returned CAPTCHA. [PNAS main](https://www.pnas.org/doi/full/10.1073/pnas.1821923116) returned robots denial through web. [Advertised final SI](https://www.pnas.org/doi/suppl/10.1073/pnas.1821923116/suppl_file/pnas.1821923116.sapp.pdf) returned HTTP 403 through urllib. The indexed primary record advertises `pnas.1821923116.sapp.pdf`, 697 KB, under PNAS license; final SI bytes were not obtained. [NCBI OA lookup](https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC6561299) returned HTTP 404. These are access observations, not findings about hidden contents.
- Legitimate author preprint [arXiv:1808.05406 PDF](https://arxiv.org/pdf/1808.05406) was obtained in memory: HTTP 200, `application/pdf`, 1,978,587 bytes, SHA256 `6ce5b54efff8dfb6cdf81481da039855082955399a280653f561f2b56d6e44f2`. It contains 25 pages including SI. Parsed with the already installed `pypdf.PdfReader(io.BytesIO(bytes))`; no download was written. This is the author preprint, not verified byte-equivalent to the final publication/SI. Preprint reuse license was not separately verified.
- SI pages 17–19 describe early L-TA seed isolation, two centrifugations, then decreasing seed additions to racemic-TA synthesis, followed by luminescence/CPL. Authors interpret the observation as growth from preformed seeds with little spontaneous nucleation. No isolated serial recipient-as-parent experiment is described in these methods.
- The seed percentage is a synthesis-volume fraction, treated as an upper amount estimate under maximum precursor-conversion yield. The supplement also explicitly estimates residual TA assuming particle geometry and full ligand coverage. Thus **a quantitative TA-carryover calculation does exist**; it must not be described as absent. It is an assumption-based ligand bound, not independent calibration of remaining founder material or its maximum optical function. No seed-only functional-capacity calibration identified.
- Access class: `PRIMARY_AUTHOR_PREPRINT_MAIN_AND_SI_INSPECTED_FINAL_SI_UNAVAILABLE`. Native format inspected: PDF figures/methods, not a lineage-indexed data table. No new H/V test is startable.

### 2025 primary adsorption follow-up: public SI confirmed

Exact article: [10.1021/jacs.4c16883](https://doi.org/10.1021/jacs.4c16883), *High Enantioselectivity in Adsorption of Chiral Molecules on the Surface of Chiral Terbium Phosphate Nanocrystals*; PMC12046555. ACS web page returned HTTP 403 and PMC returned CAPTCHA, but the official public [Europe PMC XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12046555/fullTextXML) succeeded:

| Resource | Observed format/access/size | Hash or rights |
|---|---|---|
| Europe PMC XML | HTTP 200, `application/xml`, 80,907 bytes, read in memory | SHA256 `f132e272fa0e34b76600454fc94fc5c716064d47506d01224eca15a12f6e6ac7`; article license CC BY 4.0 |
| [Figshare DOI lookup](https://api.figshare.com/v2/articles?resource_doi=10.1021/jacs.4c16883) | HTTP 200 JSON, 1,258 bytes | SHA256 `6e4574f962bb0d794621f181dffc399fd424400c160a6f5557c72947160955dc` |
| [Figshare metadata](https://api.figshare.com/v2/articles/28823413) | HTTP 200 JSON, 6,764 bytes; supplement DOI `10.1021/jacs.4c16883.s001`, v1, published 2025-04-18 | SHA256 `2a99c1dc9f882160508bfa6baee7410db0e2d6299c409321256afac8bf94f8fd`; **supplement license CC BY-NC 4.0** |
| [Native SI PDF file 53780128](https://ndownloader.figshare.com/files/53780128) | `ja4c16883_si_001.pdf`, HTTP 200, `application/pdf`, 760,874 bytes, 13 pages | SHA256 `3bab9ca7cc2c69a11484b795b383ce82598dbb60824340aa62f626b262359602`; MD5 `3aa8545778bb6b3466aa8b81d817cf02`, agrees with repository metadata |

The [public repository landing page](https://acs.figshare.com/articles/journal_contribution/High_Enantioselectivity_in_Adsorption_of_Chiral_Molecules_on_the_Surface_of_Chiral_Terbium_Phosphate_Nanocrystals/28823413) is identified by the inspected API. Only one PDF is listed, with `is_link_only=false`; no CSV/XLSX or separate raw instrument file is listed. SI was parsed in memory; no local PDF was saved. Two later reads of its exact download URL returned HTTP 500. Initial successful retrieval and checksum agreement remain direct evidence of access at that time, not a guarantee of future service availability.

**Methods/eligibility.** Adsorption assays explicitly use precipitate from the purified **seeded-synthesis** NC batch. Initial enantiopure seeds produce one secondary batch without freshly added TA, then that batch is assayed for TA/ASP adsorption. The preparation states 100 μL from approximately 11 mL of seed suspension, about 1% of synthesis quantity; it does not independently measure remaining founder mass or surface capacity. Purification leaves an estimated residual TA concentration below 10 μM. This bounds an organic contaminant, not original-seed adsorption capacity; TA carryover alone is not a structural-carbon exclusion.

The assay measures free adsorbate by calibrated CD after separation; potentiometric titration estimates total adsorption. PDF records include CD spectra, peak/concentration tables, and titration figures/tables. Main figure uncertainties are titration-estimate uncertainty, not documented independent synthesis replicates. No lineage identifiers, paired founder/descendant functional records, seed-only capacity arm, state-erased arm, or repeated recipient-as-parent transfers were established. Main-text scans found no `seed-only`, `seed only`, `serial transfer`, `generation`, `mass of`, `triplicate`, or `replicate`; this supplements, but does not replace, methods inspection.

Access class: `PUBLIC_PRIMARY_MAIN_XML_AND_NATIVE_SI_PDF_INSPECTED`. This improves the previous access-negative source chain: public functional-assay records do exist. It still does not supply the pairing needed to decide serial inheritance or exclude founder-carried function. A bounded adsorption-data check could be separately frozen by the root agent; this worker has neither frozen nor executed one. No response series were extracted or fitted.

### Follow-up verification observables

Invocation: `python3` standard-library `urllib.request.urlopen` to each exact URL above; XML parsed with `xml.etree.ElementTree`, PDF with installed `pypdf`, SHA256/MD5 with `hashlib`. No third-party source code was downloaded or executed. Binary observables: final PNAS XML/SI obtained=false; author preprint+SI obtained=true; 2025 main obtained=true; native SI obtained=true; repository MD5 match=true; adsorption batch explicitly seed-produced=true; independently calibrated founder-function bound established=false; isolated serial H/V test ready=false. Captured artifact is this appended record; the original bytes were inspected in memory and hashes recorded, not preserved as local raw-source archives.
