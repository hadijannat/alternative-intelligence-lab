# Au-to-silica-to-Pt state transfer: source audit

Primary source: Luan et al., *Enantioselective synthesis of chiroplasmonic helicoidal nanoparticles by nanoconfinement in chiral dielectric shells*, Nature Communications16,2418(2025), DOI [10.1038/s41467-025-57624-w](https://doi.org/10.1038/s41467-025-57624-w). Article XML and supplementary ZIP were acquired from public EuropePMC endpoints, with HTTP200, hashes and exact member provenance in `sources/receipt.json` and `sources/verification.json`.

## Material and operation

| Stage | Native anchor | Evidence and limit |
| --- | --- | --- |
| Parent state | Main Methods Sec15 | Opposite Au helicoids are prepared using L- or D-cysteine, surfactants and L-ascorbic acid. This is externally prepared chirality. |
| State carrier | Sec16; Sec18; SI5–7 | TEOS-derived silica coats Au, receives PVP/heat treatment, then Au is partially or extensively etched. Empty shells retain geometric shape. SI5 compares optical signals of Au seeds in shells and empty shells; it does not calibrate residual Au mass or a functional detection limit in the later Pt product. |
| Recipient nuclei | Sec19; Fig3b,c | Pt is first deposited on partially etched Au. A subsequent Au(III)/iodide treatment in CTAB is described as removing Au, followed by collection/washing. These nuclei contain Pt made before the claimed Au-removal stage. |
| Recipient growth | Sec19; SI12 | Further Pt precursor and L-ascorbic acid are added in PVP solution. The standard growth lasts75min at30°C. Images show a growth sequence; precursor doses do not establish deposited masses or functional amplification. |
| Carrier removal | Sec23 | NaOH/PVP treatment, centrifugation and water washing remove silica shells according to the source. No calibrated residual silica/ligand census for the optical specimens was identified. |
| Recipient structure | Fig3q–t; SI9–11 | Diffraction, microscopy, Pt mapping, XRD and Pt-region XPS support crystalline Pt helicoids. They do not constitute a bulk calibrated Au/C/Si impurity bound. |
| Recipient function | Fig3h | Opposite chiroptical responses are measured after shell removal. The source reports an approximate g-factor magnitude0.0007 near445nm. This published outcome was consumed before this protocol and was not independently re-estimated here. |
| Retained-core comparator | SI15–17; main Sec6 | Au-retained Pt helicoids show similar chiroptical spectra. This supports a shape-related interpretation but is a separately prepared, differently timed growth route, not a quantified residual-Au spike series on matched Pt specimens. FDTD spectra in SI17 are simulations. |

The Pt recipe specifies common feed for the two prepared template states. It includes L-ascorbic acid and PVP; it is neither achiral nor carbon-free. Organic fabrication does not by itself refute an inorganic shape mechanism, but continued organic dependence and residual chiral ligands remain unquantified. No ligand-free operation or ligand removal is inferred.

## What the native controls can discriminate

SI8 shows growth using empty silica shells rather than seeded shells. It tests nucleation/growth morphology; it is not a calibrated no-founder optical subtraction. SI9 reports three morphology batches, each with more than500 classified particles, and a size distribution from more than250 particles. Its reported “purity” is the proportion of geometrically classified helicoids, not elemental purity or the fraction of new functional matter.

The37-sheet source workbook contains `Figure 3h`, `Supplementary Figure 5`, `Supplementary Figure 9`, `Supplementary Figure 10`, `Supplementary Figure 11`, `Supplementary Figure 16` and `Supplementary Figure 17`, among other sheets. The verifier inventories dimensions and the first three rows of text labels, without selecting numerical spectra. The optical sheets expose wavelength, g-factor and normalized extinction columns. The inspected schema supplies neither linked residual-Au measurements nor an optical replicate/covariance structure. SI9's morphology batches must not be treated as optical replicates. SI11 contains the Pt4f region, not a calibrated total-Au census.

A near-flat seed/empty-shell signal in SI5 and a later nonzero Pt signal are useful controls. They do not bound all rival contributions after metal growth: Au–Pt coupling can change optical response, normalized extinction removes an absolute scale, and ligands/matrix can change state during processing. A linear combination of isolated component spectra has not been validated for these products. No founder signal budget or residual detection threshold is assigned from visual flatness.

The movie-description file identifies six electron-tomography reconstructions of Au@Pd/Au@Ag products. They are not time-resolved serial inheritance movies. The two-page Nature peer-review file contains a short approval and notes earlier review elsewhere; it supplies no additional founder controls.

## Unresolved identity and evidence boundaries

Main Fig3c names `Pd seeds` while the associated Pt paragraph and Methods Sec19 specify Pt. Both readings are retained. The audit follows the Pt recipe as described but does not silently repair the caption or treat the label discrepancy as resolved.

No quantitative residual-Au/ligand/silica contribution bound, recipient-as-parent serial functional transfer, selection experiment, repair cycle or same-system integration was identified in the native main/SI/workbook schema inspected here. These are dataset-specific missing observations, not a proof that such chemistry is impossible.

The main article states CC BY-NC-ND4.0. The review file separately states CC BY4.0. Native XML/PDF/workbook/archive and figure renders stay local and are excluded from the curated publication; authored analysis and provenance do not relicense them. No derivative source figure is published.
