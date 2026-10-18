# PPKTP primary-source audit

## Acquisition and identity

The primary is Pena et al., *Template-growth of periodically domain-structured KTiOPO4*, Optical Materials Express 1, 185–191 (2011), DOI [10.1364/OME.1.000185](https://doi.org/10.1364/OME.1.000185). The acquired HAL author manuscript is eight PDF pages including the repository cover. HAL API reports open access and HAL Authorization, not a Creative Commons license. Its one listed attachment is the manuscript; no supplementary numeric dataset is listed. All eight pages were extracted and read; decisive figures 4–5 were inspected as rendered pixels.

The companion is *Bulk PPKTP by crystal growth from high temperature solution*, DOI [10.1016/j.jcrysgro.2011.11.081](https://doi.org/10.1016/j.jcrysgro.2011.11.081). Its HAL manuscript has five PDF pages including cover. It cites the 2011 optical results and must not count as independent optical replication. Complete text was read. The acquisition receipts contain URLs, HTTP status, bytes and SHA256; the first pages identify their DOI. Native source files remain unmodified.

| Artifact | SHA256 | Observation |
|---|---|---|
| `sources/ome2011.pdf` | `8edd175ce10cdbe22c2d0387da1fcdc23857d49bf0358367ab92fd26a6ecfc1c` | 378376 bytes, valid eight-page PDF |
| `sources/jcg2012.pdf` | `27ba4dd347b377eaad316f0e8b02bfca4ec7f4423b9587a0a33920ae92d4a256` | 658142 bytes, valid five-page PDF |
| `sources/hal-metadata.json` | Receipt records hash | DOI, public file URL, rights |
| `sources/hal-companion-metadata.json` | Receipt records hash | Companion identity and rights |

Access negatives: web publisher full-text route returned Internal Error; DOI redirect displayed “Please wait”; HAL landing-page web fetch failed; ResearchGate author-upload web fetch returned HTTP429. Search indexing exposed author text, then the official HAL API supplied a working public native PDF URL. No access restriction was bypassed, login used, purchase made or author contacted. These failures do not imply missing scientific evidence. No raw SHG observations, replicate files, SI, or dataset identifier appears in either acquired manuscript or its HAL attachment listing. Publisher SI inventory could not be independently inspected.

## Scientific observations

The 2011 source reports KTiOPO4 growth from inorganic KPO3/KF flux onto an electrically patterned seed. The newly grown layer has spatially measured optical function. The table identifies observations rather than a fitted model.

| Observable | Native location | Value / condition |
|---|---|---|
| Seed dimensions and patterned region | PDF p7 | 11×6×1 mm; central patterned 7×3×1 mm |
| Domain period | PDF p7; Fig5 p8 | 38.86 µm |
| Growth mixture | PDF p6–7 | Molar 0.1 KTP / 0.6 KPO3 / 0.3 KF |
| Cooling | PDF p7 | Start 1005.5 K; 0.05 K/h |
| Preliminary single-domain experiment | PDF p6 | 2.2% supersaturation, 6 K below saturation; seed rotation 30 rpm; do not silently assign all preliminary settings to final patterned experiment |
| Temperature constraints | PDF p5 | Cited Curie range 1193–1233 K; calculated polar-face roughening about1053 K; observed polar faces below1048 K |
| Layer extent / defect boundary | PDF p7 | Up to800 µm on each c face; clean domain propagation to225 µm; cracks/inclusions farther out |
| SHG measurement geometry | PDF p7, Fig5 p8 | Propagation along a; input/output polarized c; d33 probed; room temperature |
| Beam size | PDF p7 | Fundamental 1/e² diameter70 µm |
| Probe locations | Fig5 p8 | 275 µm inside seed;225 µm into new layer from interface |
| Optical sample diagram | Fig5 p8 pixels | 6.50 mm propagation length,3 mm width,1.5 mm thickness |
| Peak wavelength | PDF p7 | Seed2127.1±0.5 nm; layer2126.9±0.5 nm |
| Spectral acceptance | PDF p7 / Fig5 | Both12.7 nm·cm; FWHM19.5 nm; calculated ideal9.4 nm·cm |
| Peak signal | PDF p7 | Layer about28% lower than seed; scattering is author interpretation |

The grown layer contains an inherited patterned nonlinear susceptibility and generates second-harmonic light in a spatially addressed volume. This exceeds a mass-only growth observation. It is still attached to the founder. Neither source provides measured stray-light/cross-talk, a founder-only measurement in the displaced beam geometry, an isolated daughter, different parent-pattern functional alternatives under matched conditions, or serial daughter-as-seed cycles. A Gaussian overlap calculation would be an explicitly conditional optical model, not a measured founder bound. SHG intensities also lose the absolute sign/phase of nonlinear susceptibility; matching intensity spectra alone does not identify every polarization bit.

Carbon: the named active crystal and growth flux contain no carbon. Lithographic founder preparation, commercial seed manufacture, polishing, electrodes, furnace and optical apparatus are incompletely specified. Do not claim the entire fabrication chain carbon-free. The paper's inherited pattern originates in externally applied lithographic/electrical programming. External heat, rotation/cooling control and optical pumping are required. The recorded experiment supplies no self-repair, autonomous daughter separation, metabolism, serial functional variants, cognition or coupling to Mo34WV/PMo12.

## Negative and ambiguous results retained

- The800 µm growth thickness is not800 µm of demonstrated defect-free optical performance. Optical function was measured at225 µm, with28% peak loss and broader acceptance than ideal.
- The2011 abstract describes good quality beyond800 µm, while detailed results identify cracks/inclusions beyond225 µm. Detailed limits govern our claim.
- The2012 companion reports2 µm/h from SEM and gravimetry, but no time-series raw data. Its clean optical region is described as200 µm and refers back to2011.
- In the acquired2012 author manuscript, Fig4 lists0.120/0.586/0.293 mixture while main growth text lists0.103/0.598/0.299. It prints identical seed/layer2θ=33.859° while claiming nonzero lattice mismatch1e−3. Do not calculate a corrected mismatch or merge these recipes.
- The2011 manuscript sentence about defect density increasing “up to225 µm” is less clear than the preceding section's cracks beyond225 µm. Preserve wording ambiguity rather than inventing a continuous defect profile.
- No complete raw numerical dataset, uncertainty definition, independent specimen count or serial-transmission error rate is supplied. The plotted wavelength errors are not established confidence intervals.

## Evidence scenarios

Acquisition invocation: Python3.12.3 `urllib.request.urlopen` on exact URLs in `sources/acquisition.json` and `sources/companion-acquisition.json`; binary observable = PDF magic, parse success, stated DOI, nonzero pages; captured artifacts = both PDFs, text extractions and JSON receipts. Figure inspection invocation: PyMuPDF rendering of pages7–8 followed by `view_image`; observable = spatial locations and SHG axes visible; artifacts = `sources/ome2011-page7.png` and `sources/ome2011-page8.png`.

Eligibility outcome: positive bounded evidence of new-layer nonlinear optical function under a founder pattern; full functional heredity remains unproven. No new numerical fits were performed in this source audit.
