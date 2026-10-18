# Functional boundary repair: acquired comparator, integration rejected

2026-10-18. One new primary experimental paper and its linked data deposit were examined after reading the existing POM-polyoxocation, tube-alternative and copper-phosphate boundary reports. No prior negative was changed. No complement is admitted.

Kazakli et al., *Journal of Membrane Science* 600 (2020), 117855, DOI [10.1016/j.memsci.2020.117855](https://doi.org/10.1016/j.memsci.2020.117855), provides an actual damage/recovery/function experiment. Its primary author-repository record is https://eprints.ncl.ac.uk/263089 and data DOI is https://doi.org/10.25405/data.ncl.9610601.v1 . The accepted paper, processed data and metadata were downloaded; checksums.json records byte counts and hashes. Three downloaded dataset files match the repository MD5 values.

## Material and experiment

The successful autonomous-repair arm uses porous alpha-Al2O3 with Li2CO3:Na2CO3:K2CO3 at 43.5:31.5:25 molar ratio. A 20 wt% sacrificial glassy-carbon phase, 5–10 micrometres, is oxidized to create dispersed voids. The carbonate melts near 400 C. Permeation is measured at 700 C, atmospheric pressure, with 50 mol% CO2/N2 feed and Ar sweep; damage is induced at 600 C with oxygen-containing streams. Carbonate remains liquid during that damage step. The paper reports restored CO2 selectivity approximately ten hours after returning to original permeation conditions (around 40 to 50 h). This is functional selective transport recovery, beyond a morphology-only growth claim. See PDF physical pages 14–15, Fig. 8; both pages were visually inspected and saved as PNGs.

The distinct large-hole arm uses a 20:60:20 carbonate mixture with melting point near 640 C. It repairs after externally imposed remelting; retain its non-autonomous classification. PDF page 14 distinguishes these arms. Do not assign the cited generic CO2/N2 selectivity near 1000 to this measured device: page 14 gives detection-limited minimum selectivity 5–10 for the low-flux measurement.

## Numeric data are available, with unresolved provenance details

The linked Figshare record explicitly describes this self-healing membrane, but README_file.txt starts with the different title *Dendritic silver self-assembly in molten-carbonate membranes for efficient carbon dioxide capture*. It also describes a drilled-channel area correction that is not independently reconciled to this pellet geometry. Files Figure4.csv and Figure5.csv have labels predating the accepted paper's Figs. 7 and 8. Approximate transitions match those plots, but this correspondence does not resolve calibration/area provenance.

Figure4.csv contains 7,679 rows with independently sampled time/flux column pairs: 2,963 valid N2 pairs and 6,331 valid CO2 pairs, ending near 52.75 h. Figure5.csv contains 43,539 rows, 43,536 valid N2 pairs and 13,273 valid CO2 pairs. Blank and '--' entries must be retained as missing. Many CO2-column entries have no time partner and cannot be assigned timestamps. Negative N2 values remain present; do not clamp them before handling detection limits.

Figure5 extends to approximately 111 h, while the displayed Fig. 8 stops near 83 h. At approximately 100 h the file contains N2 flux 8.31501 and CO2 flux 8.79884, compared with 0.04337 and 0.12523 at approximately 80 h. These are direct data values, not a model fit. Conditions after the displayed interval are undocumented here, so the late increase cannot be called spontaneous membrane failure, a new damage cycle or durable recovery. It is preserved as an unresolved negative-leaning observation. No recovery rate, permeability, data cleaning rule or held-out split has been fitted.

## Admission decision

This is a strong inorganic functional-repair comparator in its own gas-separation apparatus. It does not demonstrate synthesis of new competent material: pre-existing molten carbonate redistributes into the new voidage. There is no founder-bounded new-active-material attribution, catalyst retention, POM identity or catalytic recovery assay. Carbonate and CO2 contain carbon; the system is inorganic but not literally carbon-free. PVA occurs in fabrication of the separate carbon-fibre arm, and vacuum grease is used outside the hot zone. Neither is evidence of an organic active healing scaffold in the dispersed-carbon arm.

The 700 C gas-phase operation supplies no shared aqueous operating window with PMo12 or the hypothetical Mo34WV. Direct integration is rejected; no properties transfer between these materials. This comparator can constrain what counts as a meaningful B/R assay, but cannot fill the goal's integrated B/R requirement.

## Evidence discipline and access negatives

Scenario: acquire paper plus linked numeric data. Invocation: curl -L --fail --max-time 40 against the repository PDF and Figshare API/download URLs. Observable: successful downloads, parseable 20-page PDF, JSON and CSVs, repository-matching MD5 for all three data files. Artifacts: kazakli2020.pdf, figshare-9610601.json, Figure4.csv, Figure5.csv, README_file.txt, checksums.json.

Scenario: verify functional damage/recovery claim. Invocation: PyMuPDF extraction/rendering; direct visual inspection of paper-page-14.png and paper-page-15.png. Observable: Fig. 8 shows damage, loss and return of CO2 selectivity; paper distinguishes liquid-phase reorganization from remelting-triggered repair. Artifact: these PNGs and kazakli2020.txt.

Browser DOI/API access failed, then curl API succeeded. A PMC chemical-garden lead returned a CAPTCHA and was not evaluated as a second primary source. A first numeric inventory failed on literal '--'; reinspection retained missing entries and used only valid paired fields. Web PDF screenshot of page 16 timed out; local rendering succeeded. These failures are access/parsing negatives, not chemical outcomes.

Skipped: physical experiments, rate fitting, source-author contact and unreconciled raw-data validation. Principal risk: incorrectly treating inorganic high-temperature repair as compatible aqueous catalyst renewal.
