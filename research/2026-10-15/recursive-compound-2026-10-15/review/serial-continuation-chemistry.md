# Independent chemistry dossier review

codeQualityStatus: CLEAR
recommendation: APPROVE
blockers: []

## Scope and findings

Reviewed the authored files listed below and referenced local primary PDFs, acquisition headers, patent text, and five rendered page images. No source files changed; no native process touched. No separate notepad supplied. The previously checked loop status was `ULW_LOOP_PLAN_MISSING`, so this report uses `.omo/evidence/`.

- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: none requiring correction for this bounded scope.

Approval covers two retrospective source constraints and the small arithmetic reproduction. It does not approve a new complement, a target model, or target validation. The stated 24/0 aggregate is unchanged by these dossiers; the entire prior aggregate was not re-audited.

## Primary-source verification

Directly inspected `tantalum-coated-alumina-followup/raw/page-7.png`. Printed page 7, Example 5 and Table 3 confirm the untreated, heat-only and tantalum-coated/heat-treated rows: mass losses 30.4, 14.6, 7.2 percent; air flows 0.95, 0.95, 0.85 L/min at 5 psi. The 16-hour static exposure, pH 1, 0.1 M KCl/HCl, ethanol/ethoxide preparation and one-hour hold at 650 C match the prose. Table label wrapping is awkward but the three treatment identities and numeric pairs are preserved. Airflow chronology and replication are not supplied; the dossier correctly leaves them unknown. The general experimental dimensions and static-versus-flow warning were checked in local extracted text. Elemental coating distribution is not promoted to phase purity, carbon absence, aqueous selectivity, or target retention. Heat-only behavior remains visible as a comparator.

Directly inspected vanadate `raw/page-1.png` through `raw/page-4.png` (printed 499-502). Visually compared every numeric entry in Table 1 with the eight CSV rows, including all three prediction columns. They match. Page 499 supports temperature and medium; page 500 explicitly normalizes spectra to equal highest-peak intensity. Page 501 identifies separately prepared samples with NMR followed by emf and specifies total V for the table. Page 502 gives the rough three-unit uncertainty, small-area underestimation, and the limitation that neutral monomer is not established and cannot definitively be ruled out. The dossier preserves these limits and does not interpret acidity as an independently calibrated hydrogen-ion activity scale. No Mo/W target conclusion follows from this vanadate-only comparator.

The primary PDFs, image sizes and hashes, text/header files all match their acquisition manifests. Both acquisition headers support HTTP 200; the readable primary-page images provide an additional content check. Download commands and historical query counts were not re-executed. No new internet research was performed.

## Arithmetic and code review

Executed `analysis.py` under Python with `-B`; all six embedded arithmetic/invalid-input checks passed, and the complete emitted JSON matched `analysis.json`. Independently checked residual vectors against the visually transcribed table: maxima 3, 24, 5 percentage points; counts within inclusive three-unit bands 8, 0, 1. Sums of squared residuals are 32, 2535, 175 across eight rows, yielding RMS 2, sqrt(2535/8), sqrt(175/8). This is arithmetic on existing predictions, not fitting or out-of-sample performance. Negative model comparisons remain present.

Consulted the previously loaded `omo:remove-ai-slops` and `omo:programming` perspectives. The script has a single narrow numerical responsibility. CSV input checking is appropriate at this data boundary. Tests exercise sign, inclusive tolerance, empty/mismatched input, nonfinite values and range rejection using small inputs; they do not mirror published constants or pin prose. No deletion-only test, prompt test, needless abstraction, or production data-normalization layer was added. Neither skill perspective is violated for this scope. No lint/typecheck suite was run for this standalone reproduction; functional execution and direct inspection are the validation used.

## Exact authored-file bindings

Paths below are relative to `recursive-compound-2026-10-15/`.

| File | SHA256 |
|---|---|
| boundary/tantalum-coated-alumina-followup/REPORT.md | 5db3478a868861beb8b2875ec08fced042cc2e4b8624a55a266b61f3390f45e8 |
| boundary/tantalum-coated-alumina-followup/acquisition.json | a21714a132b4c58265ac00aef5787cf8fc3c71aec6d92881b96fdd55f66631b0 |
| boundary/tantalum-coated-alumina-followup/evidence.json | c97580fa466cc54cdd18a2387cf149037b3c980aaa3e40ccb18011e22f867d6c |
| boundary/tantalum-coated-alumina-followup/observations.csv | 0ec36fa78ff9d1440a5b253432100c840f323d1156bfcb4bdc7e2dc207e5865d |
| identity/vanadate-nmr-control/REPORT.md | 617b2744a615f14f874807136f885f6dbe0db6418b21bd2893cf385aa963fafe |
| identity/vanadate-nmr-control/acquisition.json | 0f1ec037e59de1667fcc9b820ed381e75e880b9806e171b5989e1385fb948067 |
| identity/vanadate-nmr-control/analysis.json | c1be5389f8a2f3668b70f58511aa7c8630969191f01aedbffef6c53a7f22cacf |
| identity/vanadate-nmr-control/analysis.py | 47fac0ff0d03de4a35482b8e16e5a0397a513c9d384cd8955808d7dae4399578 |
| identity/vanadate-nmr-control/observations.csv | 8ae1571132f3300897c2aef4a10aa2c52c4a09c2c02d7a1137a1b4c8160d8837 |

No experiment, target-rate inference, fit, held-out target validation, publication, or Git operation occurred. The four unrendered vanadate pages were not visually reviewed; the claimed table and limitations are covered by pages 499-502. Source-reported observations remain unreplicated.
