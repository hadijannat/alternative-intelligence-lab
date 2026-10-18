# Frozen spatial-function and ancestry identifiability test

2026-10-18. Freeze before numerical execution. The primary SI and abstract have
been inspected; the main text is access-restricted. This is a source-informed
analytical/synthetic test, not an experimental holdout or a kinetic fit.

## Question and source constraint

Wei2025 (10.1021/jacs.5c00438) motivates distinct edge and plane Fe states.
The acquired package gives total-Fe-normalized turnover, not independent
counts of competent Fe. Its local electrochemistry, bulk ICP/CV and Raman
use different supports or electrolytes. No response points will be digitized
or pooled to infer site rates. Oxygen isotope labels are not Fe ancestry.

Test the stronger hypothetical observation set of independently known edge
and plane Fe totals, fixed site turnover coefficients, and bulk incoming-Fe
fraction. If even these idealized measurements leave origin-specific
function ambiguous, present that ambiguity explicitly. Also calculate the
bounds they could provide; do not equate nonuniqueness with zero information.

## Model and assumptions

At one matched condition let E = F_E + N_E and P = F_P + N_P, where F and N
denote founder and incoming Fe. All four pools are nonnegative. Total Fe is
E + P; incoming inventory is N = N_E + N_P. The idealized current is

    j = b + k_E E + k_P P
    j_new = k_E N_E + k_P N_P.

The coefficients and background b are fixed across counterexamples, with
all Fe within each region assumed to have the same nonnegative competence.
This is a favorable limiting assumption, not a measured property. Inactive
subpopulations, Ni reconstruction and transport/contact uncertainty would
add unknowns. Coefficients are arbitrary dimensionless synthetic values,
not rates extracted from DFT or transferable chemistry.

Conservation implies

    max(0, N-P) <= N_E <= min(E, N).

Thus j_new has exact attainable bounds obtained from the two endpoints.
The direction (F_E,N_E,F_P,N_P) + d*(1,-1,-1,1) preserves both regional
inventories and bulk Fe ancestry, while changing incoming current by
d*(k_P-k_E). For k_E = k_P the incoming functional contribution is identified
in this idealized model; preserve this positive control. Spatially resolved
Fe ancestry identifies j_new only under the fixed-competence assumptions.

## Frozen cases and checks

- Main counterexample: E=0.7, P=0.3, N=0.4, k_E=10, k_P=1, b=0.2.
- Controls: equal k_E=k_P=1; no incoming Fe; all incoming Fe; empty edge;
  empty plane; zero inventories; edge activity zero; plane activity zero.
- Exhaustive rational-grid checks: E and P in {0,0.2,0.7,1}; N in
  {0,0.25,0.5,0.75,1}*(E+P); k_E and k_P in {0,1,10}; b=0.2.
  Evaluate 21 equally spaced feasible allocations in each case. Check
  nonnegativity, founder/incoming/total closure, unchanged regional totals
  and total current, and agreement with the analytical attainable bounds
  at absolute tolerance 1e-12. These are numerical checks, not independent
  experimental replicates or a new empirical validation dataset.
- Reject negative/nonfinite pools or coefficients, and N > E+P. Include a
  small meaningful test for the analytical bounds and invalid inputs.
- Report a design matrix rank/null direction without requiring SciPy.
  Independently adding N_E resolves the four-pool algebra; that does not
  calibrate per-site competence or establish same-coupon chemical repair.

## Decision rules and negative preservation

Publish every case and diagnostic, including failures. Empirical held-out
validation is INSUFFICIENT_DATA because no qualified matched specimen-level
numerical site/ancestry/function dataset was acquired. Do not invent training
or validation points. A nonzero conditional lower bound is not observed new
material activity. Neither a synthetic identified limiting case nor a good
mass balance admits a life, inheritance or integrated-complement claim.

Necessary next empirical discriminator: matched founder preload/damage and
metal supply/withdrawal, regional Fe-origin observations and independently
calibrated competence or an experimentally justified founder functional
ceiling, with simultaneous function on the same specimen. Register specimen
holdouts before outcome extraction. Preserve the remote-Fe five-hour and
convergence failures; this test does not repair those fitted-model failures.
