# Claude-surfaced MAX-phase repair leads: fresh load-bearing oxide, finite repair capability

Date: 2026-10-18. This audit independently acquired the two primary leads supplied by the root agent from the actual Claude search. It verifies their chemistry and data scope; it does not certify a completed Claude answer. No new simulation, fit or physical experiment was performed here.

## Decision

**Ti2AlC is a stronger primary comparator for chemically rebuilding a mechanical function than the previously screened molten-carbonate redistribution mechanism.** Damage exposes surfaces; matrix Al reacts with atmospheric oxygen to form adherent, load-bearing alumina in cracks, with some titania. Mechanical retesting measures recovered function. The positive result is real component evidence, not merely a visually sealed crack.

The repair consumes an existing matrix reservoir, needs externally maintained high temperature and oxygen access, and eventually loses toughness. It neither replenishes the Ti2AlC stock nor transmits function to independent descendants. Ti2AlC contains carbon as a structural carbide; this is an inorganic metallo-ceramic, not a carbon-free compound. Its high-temperature gas protocol supplies no common operating window with the documented acidic aqueous PMo12 scaffold. A separated thermal architecture would be a new untested proposal, not established integration.

## 2020: mechanical function measured after repeated healing

Osada et al., [*Full strength and toughness recovery after repeated cracking and healing in bone-like high temperature ceramics*](https://doi.org/10.1038/s41598-020-75552-1), Scientific Reports (2020), DOI 10.1038/s41598-020-75552-1, PMC7643164.

The acquired main text reports repeated wedge-splitting of Ti2AlC, with force and crack-mouth opening displacement measured at room temperature and acoustic emission used to estimate crack growth, calibrated against final microscopy. Between mechanical tests, the sample is removed and heated in air for **4 h at 1473 K**. Contact surfaces are polished after healing to remove surface-oxide friction effects. External handling, furnace energy and polishing are part of the procedure.

Crack filling is newly formed Al2O3, with TiO2 in wider regions. Microscopy maps the chemical filler and shows fracture often passing through the oxide rather than debonding from its matrix. The remaining Ti2AlC microstructure supplies toughness through interlocking, bridging and deflection; the new filler is not mechanically independent of that scaffold.

Force, displacement and acoustic measurements provide functional evidence. Local strength and toughness are subsequently **inferred by inverse three-dimensional finite-element analysis**, not directly measured as separate isolated-filler properties. The source's Figure 6 reports recovery through the first three healing cycles and a clear decline after the fourth. Its inverse-model pristine reference is approximately 240 MPa strength and 5.43 MPa sqrt(m) toughness. Error bars reflect optimizer increments, not a reported population sampling confidence interval. Do not treat the paper's inverse fit as independent held-out prediction.

**Negative result preserved:** fourth-cycle strength falls and local toughness approaches the brittle filler range. Accumulated oxide thickness and the loss of participation of surrounding tough matrix are proposed to explain the decline. The source's approximately 2 micrometre healed thickness and 4.5 micrometre alumina process-zone size are consistent with a thickness/process-zone ratio near 0.4. A prose passage reverses that ratio; Figure 6b explicitly labels thickness/process-zone size. The figure was inspected and saved; no new threshold was fitted. The article also contains an apparent numerical inconsistency describing a 2.37 mm crack as extending beyond an earlier 3.05 mm crack; no lineage geometry or rate is inferred from that sentence.

High-temperature recovery of mechanical properties is suggested by the authors, but this 2020 experiment actually retests at room temperature after high-temperature healing. Preserve that distinction.

## 2016: spatial transport limitation and slower repeat repair

Sloof et al., [*Repeated crack healing in MAX-phase ceramics revealed by 4D in situ synchrotron X-ray tomographic microscopy*](https://doi.org/10.1038/srep23040), Scientific Reports (2016), DOI 10.1038/srep23040, PMC4789783.

The material is cracked at **1000 K** and healed at approximately **1500 K in air**. Time-resolved synchrotron tomography records crack gaps. The nominal isotropic pixel size is 0.65 micrometre, with one reconstructed scan every 45 seconds in the stated acquisition. Published figures provide local gap trajectories and total filled-volume fraction; accompanying videos show spatial reconstructions/segmented healing sequences.

Matrix Al diffuses outward and reacts to form Al2O3; some Ti also oxidizes. Preferential Al mobility and adhesion explain effective bridges. Following the first repair, reloading initiates the next crack elsewhere, supporting mechanical integrity of the repaired path. This is stronger than crack-image closure alone, but the paper does not give the detailed recovered strength/toughness analysis later supplied in 2020.

**Negative results preserved:** small internal islands remain unfilled after external access seals; oxygen transport becomes unavailable. The third crack reopens the second healed path, starts wider and fills more slowly. At roughly one hour, source-reported filling is about 80% for that third crack versus about 90% for the first two cracks in pristine regions. These are geometric filling fractions, not 80/90% mechanical recovery. Existing oxide inhibits additional growth. Initial crack width differs, so no unique cycle-deactivation rate can be extracted from those percentages.

The authors describe the bulk matrix as effectively an infinite Al reservoir for the studied local events. This is a scale-limited approximation, not literal unlimited resources or a replenishment measurement. Oxidative stoichiometry requires a finite Al inventory: each mole of new Al2O3 consumes two moles of Al and 1.5 moles of O2. The source does not provide a closed long-term Al/O2 inventory, measured total oxygen uptake, or matrix-regeneration cycle. No generic Ti2AlC-to-products reaction is inferred without specifying the evolving residual matrix and carbon fate.

## Acquired data, access limits and checks

Both main XML files came directly from Europe PMC's exact fullTextXML endpoints. Their DOI identifiers were parsed and matched. Both supplementaryFiles archives were also acquired and all members enumerated in `sources/claude-leads/supplement-receipts.json`.

- PMC7643164 package: 27 members, including a 13-page SI PDF and one MP4, plus published figure/equation assets. The SI supplies specimen geometry, acoustic-emission calibration, constitutive-model equations and compression measurements/figures. It is not a raw force-time dataset or released finite-element source code.
- PMC4789783 package: 21 members, including one one-page SI PDF listing five movies, five video files, and published figure/equation assets. Rendered videos and plots are available; no raw tomography stack, voxel segmentation volume, numerical CSV or reconstruction code appears in this acquired package.

The main XML of neither source contains an identified Data Availability section or external raw-data-repository link. This is an inspection outcome for the acquired packages, not a claim that no raw data exist elsewhere. The source email addresses were not contacted. The 2020 Nature browser reader failed through its identity redirect; the 2016 Nature page was readable. Native Europe PMC acquisition succeeded for both.

**Verification scenario:** native source identity, byte integrity and supplement structure. Invocation: Python urllib download, XML article-id DOI parsing, SHA256 comparison, ZIP member enumeration/CRC validation, and PyMuPDF SI parsing. Binary observables: exact expected DOIs, matching nonempty byte counts/digests, ZIP CRC checks returning no failed member, and SI page counts of 13 and 1. Captured artifacts are under `sources/claude-leads/`, with machine-readable outcome in `verification.json`. The 2020 Figure 6 image was inspected to verify the preserved fourth-cycle failure and ratio label. Video files are retained inside the archives; they were not independently played or resegmented.

No inherited variation, self-replenishing repair reservoir, chemical catalysis recovery or PMo12 integration is established. The valuable next modeling target, if pursued separately, is finite-reservoir oxide growth with oxygen-access cutoff and accumulated-scar mechanics; the two papers must not be pooled into a single rate dataset without matching geometry, temperature, observable and preparation.
