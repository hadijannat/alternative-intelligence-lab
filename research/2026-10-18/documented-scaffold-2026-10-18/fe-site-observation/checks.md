# Verification status

| Requirement | Verdict | Evidence / limit |
|---|---|---|
| Native primary source and identity | Pass for SI | SOURCE_AUDIT.md and sources/receipt.json; exact DOI, one deposited file, MD5/SHA match,11pages; main body unavailable |
| Noncircular response | Pass | Current only fromS8a, density fromS8dleft axis; no TOF response or current reconstruction |
| Extraction fidelity | Pass within stated raster limits | Native image/annotations, extract_figS8.py, source hash, axes/units and five calibration checks; only four current groups resolved |
| Predeclared split/evaluator | Pass for retrospective scope | PROTOCOL.md before point extraction; baseline1, fit2–4, reserved5–7, fixed models and tolerances |
| Numerical checks | Pass | Unit conversion, analytic constrained fits, synthetic recovery, nesting, zero limits and reserved-value perturbations in results/models.json |
| Model discrimination | Unresolved scientifically | Nominal M0 passes, M1 fails; both calibration and extraction sensitivity limit inference |
| Origin-specific repair | Unresolved | Identical-initial conserved-inventory witness gives equal total counts/current with different origins; no actual founder function bound |
| Negative-result preservation | Pass | negative_results.json, extraction_failures.txt and all older analyses unchanged |
| Independent review | Pass for the bounded uncertain analysis | .omo/evidence/fe-site-observation-review.md: APPROVE; separate reviewer reproduced source/pixel checks, nominal fits and all16384corners, and reviewed final interpretation |
| Final JSON and frozen-input integrity | Pass |12unique negative IDs; protocol, script, point and SI hashes match results/models.json; final results SHA2567b69af287c29c10eb6c749165ee90bc6a42e20c57f7e12eb9920e177640c6609 |
| Full objective | Incomplete | Exact target identity and integrated12requirements unproved; zero integrated complements added |

Run: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/fe-site-observation/test_models.py`, exit0. All16384corners evaluated; source interval correlation and continuous-box extrema are not certified. Native figure/source and final plot were visually inspected. No new dependency, wet-lab experiment, isotope-labelled function assay, prospective or independent-specimen validation is claimed.
