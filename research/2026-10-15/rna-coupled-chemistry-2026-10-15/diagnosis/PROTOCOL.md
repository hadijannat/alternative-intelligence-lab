# Fixed-parameter background amplification diagnosis

Frozen before this diagnostic executes. This is an explanation of the previous
model, not a new fit or a held-out model selection exercise. All previous files
remain unchanged.

Use the previous selected bulk chemistry and previous fitted transport parameters
for legacy, bath and patch. Initial seed doses are 0 and 2 µM; simulate seven
serial generations with the previous 3-FT/60-minute/half-feed schedule.

For each family run exactly six interventions: unchanged reference; inert exterior
(including no exterior competence decay, matching the prior sensitivity); discard
exterior after each measured aliquot; remove active background source kh; remove
direct reporter background source krh; remove both background sources. All other
parameters and source/transfer rules stay fixed. Retain duplicates and failures.
Deleting reaction channels is a causal model diagnostic, not an admissible fitted
mechanism or physical prediction.

Integrate separate va=ka F A s, vr=kf F R s, vh=kh A²s², vp=krh A R s²,
and kd F reaction extents with the chemical state, where s=B/(KB+B). Report inside
and exterior contributions per unit total internal volume. Compute rates in every
cohort before weighting; separately show the unphysical rate-of-means comparator
as a moment diagnostic. Exterior is homogenized before warm incubation exactly as
in the previous model. Record exchange net uptake of A, B, F and reporter P,
new production each generation, substrate exposure, and intracellular/exterior
A/B/F ranges. Nominal S13 initial calibration coverage is A 0–2.5 µM, F 0–1 µM,
R=5 µM and B=7.5 µM. Passing such bounds does not establish in-domain chemistry;
mixtures and trajectories differ.

Numerics: independent DOP853 augmented integration at rtol=1e-9, atol=1e-11,
60-minute warm steps; 0.25-minute dense output grid for independent Simpson
quadrature and domain summaries. Replay all paths with rtol=1e-11, atol=1e-13,
0.125-minute grid. Check all stoichiometric inventories to 1e-7 µM, augmented versus
quadrature extents to 1e-7 µM, tighter-replay yields to 1e-5 percentage points,
and primary reference versus unchanged prior LSODA simulator to 1e-5 percentage
points. No negative state may be below -1e-8 µM; no failed path is silently dropped.

A positive seed0 vh flux is the only active-F initiating channel in this model.
Subsequent va and vr can therefore descend from background without identifying
molecular ancestry. Channel counts must not be called inherited founder activity.
