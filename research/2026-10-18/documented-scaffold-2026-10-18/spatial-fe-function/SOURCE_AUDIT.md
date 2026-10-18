# Spatial Fe function: methods and identifiability audit

Primary source: [Wei et al., JACS (2025), DOI 10.1021/jacs.5c00438](https://doi.org/10.1021/jacs.5c00438). Native evidence: [SI record 28718969](https://acs.figshare.com/articles/journal_contribution/28718969), `sources/ja5c00438_si_001.pdf`, 35 pages, with independently checked identity/hash in `sources/verification.json`. Page references below are the SI's printed S-pages, which equal PDF page numbers. Main abstract is primary, but the main body remains unavailable: the parent agent's normal IAB check on 2026-10-18 redirected to the abstract, displayed lack of access and offered $48 pay-per-view. No login or purchase was attempted. See `ACQUISITION.md` for the dated browser-access note.

## Decision

**Useful spatial-chemistry constraint; insufficient for independently quantified active/inactive Fe populations, Fe-origin-resolved repair or functional inheritance.** The SI supports selecting spatially heterogeneous Fe-doped Ni hydroxide as a documented model class. It does not supply the required paired site-population/function measurements to calibrate a unique repair or inheritance model. A generic assumption that every retained Fe atom is equally catalytic conflicts with the primary abstract's spatial interpretation, but that qualitative interpretation cannot supply quantitative per-site rates.

## Material and intervention

- Starting material is Ni LDH single-crystalline nanosheets prepared from nickel perchlorate and strongly alkaline NaOH at 140 °C for 48 h, then water/ethanol washed (S2). Use the authors' Ni LDH label; a complete invariant empirical formula is not supplied in the audited methods.
- Potential pretreatment: 1.45, 1.50, 1.55 or 1.60 V for 3 min in 1 M KOH; then 50 µM ferric nitrate added and the potential held another 5 min, followed by a gentle water rinse (S2). Those are controlled intervention inputs. The wording gives final nominal Fe addition, not an analytically established free dissolved Fe species/concentration in strong alkali.
- ICP-AES reports total Fe loading descriptors of 0.5, 1.3 and 2.1 wt% for the 1.50/1.55/1.60 V preparations (S3). These were visible during methods inspection; no independent active/plane/edge Fe amounts, uncertainty or replicate table accompanies them. Total Fe differs across treatment potential, confounding a pure spatial-location interpretation if a model ignores loading.
- FeLPD/Ni LDH and FeHPD/Ni LDH appear in figure captions S7/S8/S12/S13. The SI methods do **not explicitly map these labels to specific treatment potentials**. Do not silently equate them to chosen voltage endpoints pending native main verification.
- NiOOH and Fe-modified NiOOH surfaces are computational/operando-state models (S5–S7, S14–S26), not proof of a homogeneous final catalyst formula. Exact terminal active-state stoichiometry and Fe site partition are not quantified here.

## Assay and matching matrix

| Measurement | Native setup | Interpretation boundary |
|---|---|---|
| Bulk CV/Tafel | 1 M KOH, room temperature, GC 3 mm disk, carbon-rod counter, Ag/AgCl reference; CV 1.03–1.68 V vs RHE at 5 mV/s, cathodic sweep (S2) | Tafel and chosen overpotential come from CV, not a demonstrated transport-independent steady-state rate |
| Bulk preparation | 5 mg Ni LDH + 5 mg activated carbon + 0.6 mL water + 0.6 mL ethanol + 50 µL Nafion; 5 µL deposited (S2) | Carbon/additive/support contributions require controls; carbon-free activity is not established by this assay |
| Characterization preparation | Same described procedure except no activated carbon and FTO replaces GC (S3) | Composition assay specimens differ from bulk activity specimens; same-coupon linkage and mass accounting are not explicit |
| SECCM local function | Samples dispersed in water on ITO; about 100 nm pipette with 0.5 M KOH; Ag/AgCl quasi-reference/counter; 32×32 grid, 1 µm steps; contact detected at 0.50 V, 0 V for 200 ms, then local CV (S3) | Different electrolyte, substrate, reference and geometry from bulk; local wetting/contact area and uncompensated potential matter |
| Local scan comparisons | S7 compares edge FeHPD vs pristine; S8 compares plane FeLPD vs FeHPD; both 1 V/s | These are figure-only currents without raw arrays, replicate identifiers or independent local Fe counts in acquired package |
| Fine edge mapping | S9 topography/local current-density map, 50 nm step at 1.2 V vs Ag/AgCl | Special scan geometry; do not replace the general 1 µm method with 50 nm everywhere |
| In situ Raman | Au 3 mm disk, ethanol-dispersed sample, Pt-wire counter, Ag/AgCl reference; 532 nm laser, 50×/NA0.55; mapping 12×12 after 60 s at each 1.425/1.450/1.475 V (S3–S4) | Raman intensity/oxidation-state maps are not absolute active-Fe population measurements |

The audited SI does not document reference-to-RHE calibration, iR compensation, electrolyte volume, stirring/flow, quantitative pipette contact-area normalization, or a common transport calibration across these assay geometries. It gives electrolyte molarity rather than a measured pH series. These are **not found in SI**, not asserted absent from an unavailable main article. Matched labels in figure captions are not enough to establish independent specimen pairing, exact local Fe dose, common electrode history or equal electrochemically active area.

## Independent population evidence versus inferred activity

ICP-AES measures total Fe. HAADF-STEM/EDS maps, SEM, AFM, XRD and Fe K-edge XANES/EXAFS are listed (S4). These can support composition, spatial distribution and coordination but do not, by themselves, count which Fe atoms are catalytic under the functional assay conditions. No independently calibrated active-site census or separate inactive Fe inventory is supplied in the acquired SI.

The TOF equation is `j*A/(4*F*m)`, where `m` is **total moles of Fe on the electrode** (S2–S3); S5 explicitly says normalized by overall Fe. Thus TOF is a current-derived average over total Fe. It cannot independently validate an assumed active fraction or a per-active-site rate. Fitting activity and then naming the fitted fraction active Fe would be circular. Ni sites can also contribute to current, further limiting exclusive Fe turnover attribution.

The primary abstract associates edge Fe–O_bridge–Ni with enhanced function and plane O_hollow(NiNiFe) with detrimental function, combining microscopy, Raman and theory. This is useful motivation for distinct spatial states. It is not a numerical dataset of their population, interconversion rates, or lineage.

## Isotope and repair limits

S4 labels oxygen using 98 atom% H2-18O electrolyte: five CV cycles (0.50–1.65 V vs RHE, 5 mV/s), then 1.50 V for 3 min, replacement with 1 M KOH in ordinary water, and another specified potential for 3 min before Raman. S12/S13 show oxygen-label Raman experiments.

**18O follows oxygen exchange, not Fe origin.** It cannot distinguish newly supplied Fe atoms from founders or label their functional contribution. The isotope exchange and Raman experiment also has a different substrate/protocol from bulk CV. No Fe isotope tracing, founder-exhaustion bound, damaged/no-damage crossed with Fe/no-Fe rescue, offspring passage, or retained-founder functional ceiling is documented in the acquired SI. Oxygen exchange alone is not active repair.

## Model constraints and data availability

The defensible next model can distinguish edge-associated and plane-associated Fe, Ni background activity and a geometry-dependent measurement operator. It must expose the underidentification: current alone gives sums of site population times site activity, with background and contact/transport effects. Do not estimate new site-specific rates from DFT free energies or oxygen-exchange shifts without a justified kinetic observation model.

S5–S7 provide DFT method settings and Table S1 thermodynamic corrections; free-energy diagrams are figures. These are thermodynamic inputs, not measured barriers or time-resolved rate data. No native DFT structures/trajectories are attached to the acquired record. S20 caption says edge sites while S19's preceding pathway is labelled plane; preserve this caption inconsistency rather than assigning a model based only on adjacent numbering.

Only one PDF is advertised in the exact Figshare record; it has zero embedded files. No numerical SECCM/Raman matrices, raw local CVs, particle-ID-linked ICP/site counts, or repeatability dataset was acquired. The main article's data-availability statement remains unverified. Therefore a response-point holdout is not yet a source-qualified held-out validation; even later figure digitization would be retrospective and would need a frozen extraction protocol, specimen-level splits and digitization uncertainty.

## Preserved negatives and bounded outcome

1. Native SI access succeeded despite ACS403; main native access did not succeed in this worker's routes.
2. No acquired raw table supports an independent quantitative active/inactive Fe census.
3. Total-Fe-normalized TOF cannot resolve that missing census.
4. Preparation potential changes both Fe amount and probable spatial incorporation; cross-assay support/electrolyte/reference changes prevent pooling as one matched experiment.
5. Oxygen isotope exchange does not supply Fe ancestry or functional inheritance.
6. Bulk demonstrated implementation includes activated carbon, GC and Nafion; ethanol also appears in synthesis/processing/Raman. Individual SECCM mounting uses ITO/water, but that does not establish an autonomous carbon-free life chemistry.
7. No current digitization, kinetic model fit, held-out performance claim or active-repair claim was made by this acquisition worker.
