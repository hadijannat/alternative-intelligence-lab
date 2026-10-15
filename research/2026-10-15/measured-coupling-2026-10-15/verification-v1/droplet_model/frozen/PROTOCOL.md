# Measured droplet coupling protocol, version 1

This analysis plan is frozen before parameter fitting. The source data and their
rough shape have already been inspected: the holdout is a temporal extrapolation
check, not blinded independent validation. No model or cutoff will be changed in
response to its result. Scope: this folder's model, runner, tests and evidence;
the source bundle and other laboratories remain untouched.

## Measurements and conditions

Use only normalized observations with condition_id `single_Cys_PSS`: C3 HPLC
concentration from Figure 1F and OD650 from Figure 1C of
https://doi.org/10.1016/j.chempr.2025.102816. They share reported nominal chemistry
but are separate aliquots with no cross-assay pairing. The two HPLC observations
at each time have no established longitudinal replicate identity.

Reported conditions: 25 C, final pH 4, MES 200 mM, peptide Ac-F(RG)2D-OH 16 mM,
PSS 50 mM monomer, EDC 50 mM, C-N3 3.2 mM, tripropargylamine 0.84 mM, Cu 1 mM,
ascorbate 2 mM. Buffer/alkyne rounding conflicts are retained in conditions.json.
Do not import S3 fuel rates (PSS unspecified), CuII/no-ascorbate partition data,
internal FRAP mobility, or KR3 seeding/refueling parameters into this C3 fit.

## Fixed fit and challenge

Fit every C3 observation at t <= 2 min by unweighted least squares. Hold out all
t >= 4 min (six observations); include t=0 in counts but acknowledge it gives no
rate information. Fix stoichiometric capacity Q=0.84 mM and initial C3=0.

Model: dT/dt = (k0 + kcat*T)*(Q-T). k0 has units min^-1 and kcat mM^-1 min^-1.
It is an effective, lumped product-dependent rate, not a microscopic chemical
mechanism: mono/bis intermediates and catalyst activation are unresolved.
Compare kcat=0 fitted on the identical rows. Bounds: 1e-6 <= k0 <= 20 and
0 <= kcat <= 100. Fixed multistart least squares; profile kcat on 101 values
0..20 with k0 reoptimized. Report the descriptive profile envelope whose SSE is
within 0.0025 mM^2 of minimum, with NO confidence-level interpretation. Capacity
sensitivity: refit training only at Q=0.80 and Q=0.88 mM; these are assumptions,
not measured confidence limits. No rescue of holdout error by introducing decay.
Report RMSE, residuals and holdout versus baseline; use an explicitly engineering
tolerance of 0.084 mM (10% nominal capacity), not an experimental error bar.

OD is read independently. Each well's operational persistence window ends at
the first sample below 10% of that well's maximum OD. Report sample bracket, do
not infer phase volume, droplet number, active catalyst or division from OD.

## Coupled ledgers and explicit unknowns

Track nmol of unreacted TPA, azide, founder C3 inside/outside, new C3
inside/outside; fixed aqueous volume is 50 uL. Each new C3 consumes one TPA and
three azide molecules. Catalyst redistribution uses production-localization
fraction l and first-order entry/escape rates. Bulk reaction uses total active
C3 with assumed active fraction f, freely accessible pooled substrate and
phase-independent catalytic activity. These are closure assumptions, not
measured transport physics. kcat and f are confounded; fitted kcat uses f=1.

Witness A: l=1, no exchange, all newly produced catalyst remains inside.
Witness B: l=0, no exchange, all catalyst outside. Both give the identical
single-batch total C3 and observed OD while opposite retention is predicted.
This demonstrates nonidentifiability in this observation model; it does not
prove phase-coupled real chemistry has phase-independent reaction rates.
Also run finite exchange and verify conservation/numerical refinement.
Retained-compartment witnesses are limited to the first two minutes while both
OD wells remain above the operational threshold. Their phase identities must not
be extrapolated past the observed dissolution window.

## Hypothetical transfer intervention

Eight 2-minute passages, fresh scaffold supplied externally each passage, fixed
50 uL after refill; this intervention was NOT performed in Figure 1. Initial seed
0.02 mM is assumed, with a founder-free control. At each passage remove 25 uL,
retain half the soluble substrates, choose fraction q of dense-phase C3 to
retain, discard all exterior C3, then refill 25 uL to restore TPA=0.84 mM and
azide=3.2 mM. This is hypothetical selective compartment collection, not random
half-volume pipetting or a demonstrated daughter lineage. q is an amount
fraction; no partition volume or division physics is calibrated. All discarded
material and added substrate are counted. Contrast actual random bulk half
transfer (all species multiplied by 0.5) and complete pooling, which convey no
tracked vertical identity. New/founder labels remain conserved separately.

Sweep l in {0,0.5,1}, q in {0,0.5,1}, escape in {0,1} min^-1,
active fraction in {0,0.5,1}; entry fixed 0. Compare catalytic regeneration,
baseline-only (kcat=0), and no-regeneration controls. Score only conditional
retained catalytic function: retained active new C3 >=0.01 mM and its marginal
initial production rate kcat*f*Tnew*Q >=0.01 mM/min at passage 8, with founder
active fraction <=1% of total active C3. The thresholds are arbitrary explicit
operational challenges, not definitions of life. There are no measured
functional variants, sequence copying, compartment division or intelligence.
The marginal catalytic-rate score uses each control's actual catalytic
coefficient, zero for baseline-only and reaction-disabled controls. Volume is
prescribed protocol bookkeeping; chemical mass conservation is numerically
checked independently.

## Verification and outputs

Run unit tests for analytic/ODE agreement, stoichiometry, nonnegativity, zero
baseline/seed, exact transfer accounting, label conservation, opposing witness
retention with equal observations, and tighter-tolerance refinement. Freeze
code/config and input hashes in the run evidence directory. Replay offline to a
fresh directory and compare scientific JSON/CSV, excluding timestamps. Keep
failures visible. Completion is an executable, audited joint constraint test,
not a positive life or inheritance result.
