# Functional inheritance: four primary datasets

Search and acquisition date: 2026-10-15. These systems provide independent constraints on sequence-dependent function, network composition, and newly synthesized RNA. None of these four studies supplies a dataset joining identified physical parent–daughter compartments, newly synthesized active catalyst, and repeated autonomous compartment reproduction. Their rate constants must not be pooled with the Salibi R3C/POPC freeze–thaw model.

## 1. Azoarcus autocatalytic networks: directly relevant negative constraint

[Ameta et al., 2021](https://doi.org/10.1038/s41467-021-21000-1) measures assembled RNA compositions in microfluidic droplets. The archived Supplementary Data 2 contains **1,837 network compositions and 20,039 individual droplet fraction/UMI records**. Experimental fractions and author-model fractions are exported separately. The paper explicitly reports a heredity limitation: noncovalently assembled catalysts drive relaxation toward substrate-determined compositions, weakening memory of supplied covalent catalysts. Thus apparent regeneration need not transmit a distinct functional state.

Conditions: nominal reaction buffer 30 mM EPPS pH 7.4, 20 mM MgCl2, 48°C for 1 hour; WXY about 0.1 µM per component after fusion, Z 1.6 µM. Actual fusion numbers vary, so these are preparation/nominal concentrations rather than identical per-droplet concentrations. Oil is HFE 7500 with 2% surfactant. Droplet splitting is part of destructive sequencing preparation; barcodes identify sampled droplets, not multigeneration pedigrees. Independently measured initial slopes distinguish covalent-catalyst and noncovalent-complex contributions. This motivates an explicit background-assembly term and a test of memory loss at fixed feed composition.

Downloaded: article XML, SI PDF, oligonucleotide workbook, numeric composition workbook. [Figshare collection](https://doi.org/10.6084/m9.figshare.c.5103962) metadata also indexes raw main, cross-talk, and random-trajectory data; those larger files were not downloaded because the published numeric workbook supplies the needed screening data. Source license: CC BY 4.0.

## 2. Evolved RNA replicator networks: sequence-linked functional benchmark

[Mizuuchi et al., 2022](https://doi.org/10.1038/s41467-022-29113-x) supplies isolated clone sequences, dominant-mutation genotypes and replicate replication measurements. The normalized Figure 4 table preserves **182 entries**, including the literal missing-data label `sample loss`. It connects RNA lineage sequences to different replication interactions. This is stronger evidence of inherited molecular function than a fluorescent reporter alone.

It uses an **RNA-encoded protein Qβ replicase and reconstituted E. coli translation machinery**, not RNA-only catalysis. Population propagation uses 37°C for 5 hours, fivefold dilution, and mechanical fusion/division of water-in-oil droplets. Clone-function assays separately translate 30 nM donor RNA for 2 hours without UTP, then dilute threefold and assay replication for 2 hours with 1.25 mM UTP and 30 µg/mL streptomycin; optional second RNA is 10 nM. The complete translation-buffer formulation is referenced to earlier work and has not been independently reconstructed here. Do not transfer these fold changes into R3C rate constants.

Downloaded: article XML, SI PDF, sequence/genotype XLSX, Source Data XLSX. The source workbook has numeric Figure 4 and supplementary tables, **no numeric Figure 5 time-series sheet**; the 22-round trajectory remains a paper observation, not a downloaded numerical constraint. Physical parent–daughter identities and active replicase retention are absent. License: CC BY 4.0.

## 3. Encapsulation and sequence–activity landscapes

[Lai et al., 2021](https://doi.org/10.1073/pnas.2025054118) measures self-aminoacylating RNA sequence activities inside versus outside OA/POPC 1:1 vesicles. It provides an assay design for inherited function: compare the same sequences across compartments and measure chemistry rather than total fluorescence. For low-activity sequences, only the product of fitted rate and amplitude is well determined; fitting them independently would create false mechanistic precision.

Conditions: 100 mM HEPES pH 7, 100 mM NaCl, 100 mM KCl, 5 mM MgCl2, 5 mM CaCl2, 0.5 µM total RNA, 90-minute incubation, BYO substrate 10–1,000 µM. The accessed main methods do not state a numeric reaction temperature. Vesicles are extruded through 100-nm pores. Selection uses RT-PCR and retranscription between rounds; it does not demonstrate autonomous catalyst replication or vesicle descent. RNA outside concentrated vesicles was below a 250 pg/µL detection limit; this is an assay bound, not a kinetic active-catalyst retention coefficient.

[Dryad](https://doi.org/10.5068/D1PX0K) metadata lists raw reads, count tables, and MATLAB analysis archives under CC0. Metadata and article XML are archived. **Numeric archive retrieval failed**: the download API returned HTTP 401, and the public web route returned 403. No quantitative reanalysis of this dataset is claimed; manifests explicitly mark the two attempted MATLAB archives not downloaded.

## 4. QT45: newly synthesized sequence and functional-product checks

[Gianni et al., 2026](https://doi.org/10.1126/science.adt2760) reports a 45-nt RNA polymerase using activated triplets. Separate complement and self-synthesis reactions yield about 0.24% and 0.17% after 72 days. Shared conditions include 80 nM catalyst, 8 nM primer/template, 50 nM each substrate, 0.4 mM MgCl2, 1.2 mM KCl, 1 mM CHES-KOH pH 9, and −7°C ice. Self-synthesis additionally uses a defined hexamer and one pH–heat–freeze cycle. Strand sequestration is a stated obstacle; these are not a closed self-amplifying catalyst cycle.

Its hammerhead function experiment distinguishes recovered sequences followed by RT-PCR/retranscription from a separate assay of directly isolated mini-hammerhead products. This distinction should be retained in any model observer: sequence correctness, regenerated active catalyst, and downstream product formation are separate measurements.

Downloaded: author-manuscript XML, [Zenodo record 13891380](https://doi.org/10.5281/zenodo.13891380) metadata and **57,014,823-byte fidelity archive**. It contains 14 FASTA files (3 references plus 11 processed read collections), totaling **5,323,070 FASTA records including references**. The supplied archive checksum and ZIP CRC pass. Fidelity values have not been recalculated. Zenodo declares MIT licensing; the article manuscript carries its own permissions. Larger fitness-landscape archives remain indexed, not downloaded. No membrane retention or physical offspring measurement is present.

## Assay requirements implied by these datasets

1. Identify physical parents and descendants with a label independent of catalyst concentration; separately quantify horizontal exchange.
2. Label newly synthesized catalyst distinctly from founder molecules. Measure retained **active** new catalyst after transfer, alongside total RNA and leaked RNA.
3. Recover descendant catalyst for a calibrated substrate-conversion assay. Include same-length inactive variants, founder-only dilution, no substrate, and no regeneration controls.
4. Vary founder composition while holding feed composition fixed. Ameta's results show why convergence to the feed-determined state can mimic compositional reproduction.
5. Measure sequence variants and their reaction rates in the same environment. Keep a recovery/retranscription assay distinct from direct activity of newly made molecules, as illustrated by QT45.
6. Measure replication/ligation, inactivation, reversible sequestration, and membrane transfer separately before estimating them jointly. The datasets here constrain assay design and model structure; none identifies Salibi's active-R3C retention coefficient.

## Reproduction and evidence

Run `python3 rna-mechanism-2026-10-15/sources/inheritance/acquire.py` for acquisition, then `python3 rna-mechanism-2026-10-15/sources/inheritance/verify_extract.py` for offline verification and exports. `manifest.json` stores URLs, licenses, hashes, sizes, and failures. `verification.json` records **23 passing integrity/export scenarios and six normalized artifacts**. CSV export retains original source representations and missing values; the archive is inspected without executing author notebooks.

Skipped: no physical experiments, full sequencing reprocessing, author contact, or bulk multi-gigabyte archive downloads. Risk: none of these chemistry conditions is interchangeable with the R3C vesicle system; molecular lineage evidence is not physical compartment inheritance.
