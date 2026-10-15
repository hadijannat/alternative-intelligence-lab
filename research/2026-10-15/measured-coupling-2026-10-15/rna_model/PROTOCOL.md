# R3C/POPC measured coupling protocol v1

Written before any numerical fitting in this package on 2026-10-15. Figures and published endpoints were inspected during source discovery, including Figure3 values. This is a disclosed analysis-design holdout, not a blinded or prospectively unseen experiment. No parameter, model-selection, or threshold tuning may use held-out values.

## Question and evidence boundary

Test whether a concentration-conserving model of active catalyst production, RNA retention, and horizontal serial propagation can jointly predict Salibi et al. Figure3 under the same measured POPC/R3C conditions. Functional parent-offspring compartment inheritance is a separate required evidence question, unidentifiable from these population assays. A positive fit cannot establish it. This is ligation of prepared52nt+14nt fragments, not sequence-general copying.

## State and chemistry

Each cohort carries concentrations in micromolar of active substrate A=Hyper-A, reporter substrate R=Cy5-A, substrate B, active catalyst F=F1, inactive reporter P=Cy5-F1, and inactive product D used only in ablations. Initial seed/GUV A/GUV B cohorts each have one-third interior-volume weight. Weighted concentrations assume equal encapsulated volume per amount of added GUV population; this is not measured individually.

During the60min42C phase, define inhibition denominator H=1+(P+F+D)/Ki. Primary effective fluxes are va=k*F*A*B/H + kb*A^2*B^2 and vr=rho*k*F*R*B/H. Units k=micromolar^-2 minute^-1, kb=micromolar^-3 minute^-1, Ki=micromolar. The tetramer term is motivated by SI Fig11 but is not an established elementary rate law. Product inhibition is a coarse saturation hypothesis, not a mechanism established by this dataset. All full-length products enter it including carried-over active F; it does not reset on transfer. Stoichiometry consumes one A+B per active product and one R+B per reporter. P never catalyses. rho=1 is a declared equal catalytic efficiency assumption, not measurement. A reviewer identified an artificial phase-specific initial-F subtraction before any fit; it was removed before freezing the numerical run.

Each FT step maps cohort xj to r*((1-m)*xj+m*weighted_mean(x)); r=0.55^(1/3) is an approximate inferred concentration retention from the paper's45% loss estimate. m in[0,1] is the fitted exchange fraction. Lost species enter an explicit sink. The default assumes no chemistry during the frozen/thaw phase; SI18 shows it is small relative to the warm stage but not zero, so this is a limitation. Following each generation the old cohort weights halve and fresh A and B cohorts each receive weight0.25. Compartments are supplied externally; no simulated spontaneous growth/division.

Reporter observation is100*sum(w*P)/sum(w*(R+P)), including old reporter carryover. Concentrations and loss/feed accounting remain distinct from this ratio.

## Frozen calibration and prediction

1. Fit k, kb, Ki to all numerical S13c F1/Hyper-A time-course summary means, using unweighted squared error in percentage points. Do not duplicate S13d endpoints. Bounds: k[1e-5,1], kb[1e-9,0.1], Ki[0.01,1000]. Optimize logarithms with fixed multiple starts; retain fit errors and boundary hits. Do not interpret these effective parameters as separately measured elementary constants.
2. With those parameters fixed, fit m to Figure2 negative-control and1uM-seed endpoint replicates at FT counts1,2,3. Zero-FT is a structural check. m cannot rescue chemical parameters.
3. Predict Figure2 2uM seed and every Figure3 generation for every seed without fitting. Report RMSE, signed bias, maximum error in percentage points. A pragmatic model adequacy screen is held-out RMSE<=2 percentage points AND maximum absolute mean error<=4 points, defined now; this is a numerical screen, not proof of chemical mechanism.
4. Fixed-parameter controls: no-regeneration routes every newly made active product to inactive D but retains old F catalysis and substrate consumption; no-exchange m=0; no-feed replaces fresh populations with empty ones. A simpler homogeneous-pool model assumes complete mixing m=1; evaluate the same prediction task and errors.
5. Prespecified sensitivity: retention over3FT in{0.4,0.55,0.7} and rho in{0.5,1,2}, refit calibration only independently for each, report all rather than select by heldout. These are structural scenario ranges, not measurement confidence intervals. Check Ki profile at{0.03,0.1,0.3,1,3,10,30,100,300,1000} while refitting k,kb on calibration only. Passive carryover baseline begins from measuredG1 reporter concentration and propagates loss/dilution without further formation; explicitly conditional on that first observed measurement.

## Verification

Exact stoichiometric moiety conservation between events; nonnegative states; bounded reporter0..100; label cannot create catalyst; no-exchange separated cohorts show no reaction; seed-only catalyst decreases under ablation; loss and feed mass balances; timestep/refinement agreement; parser workbook-coordinate checks; deterministic fresh-process replay. Publish raw data hashes, fit/prediction outputs, source-conditioned parameters, trajectories and a figure. Do not claim reproduction of a living entity or functional lineage inheritance.
