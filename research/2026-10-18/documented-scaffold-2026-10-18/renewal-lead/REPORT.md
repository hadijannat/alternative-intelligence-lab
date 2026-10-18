# Beta growth transmits some structure while resetting bulk state

Acquiring the previously missing [Zheng et al. 2014 primary study](https://doi.org/10.1016/S1872-2067(14)60089-9) changes the inheritance assessment. Compositionally different Beta seeds grow Beta under the same nominal gel, but the bulk product does not copy the parent composition. This rejects a particular copying assumption; it does not prove mineral inheritance impossible.

The archived11-page PDF and publisher HTML provide ten joined seed/product records. The gel is Na2O:Al2O3:SiO2:H2O=11.4:1:40:640, seeds are10wt% relative to silica source, and growth is static at140C. Seeds were initially synthesized with organic templates and subsequently calcined. [SOURCE_NOTES.md](SOURCE_NOTES.md) preserves exact preparation, table definitions, yield/access gaps and source hashes.

Seeds have SiO2/Al2O3 ratios11–38, plus two pure-silica samples. Products cluster at10–11. Pure-silica parents lead to an Al-containing product; unchanged founders cannot supply that Al, so feed-derived material is involved. Seed size, defects, preparation and composition covary, preventing a composition-only causal kinetic inference. Bulk measurements also include residual founders.

## Retrospective transfer comparisons

For chemistry-consistent comparison, convert oxide ratio r to cation Al fraction `x=2/(r+2)`. Pure silica is x=0; oxide ratio10 corresponds to x=1/6. The complete tables were inspected before fitting; the following split withholds rows from parameter estimation only, not from prior observation.

Fit S1–S8 to `x_product=(1-alpha)*g+alpha*x_seed`, with0<=alpha<=1 and0<=g<=1. This is a bulk mixture/partition descriptor. It is not a measured copying probability or founder fraction. The constrained optimum is **alpha=0**, g=0.161859. The unconstrained slope is−0.136334; the nonnegative fit therefore reaches a boundary. That boundary is reported rather than hidden as a precise biological heritability estimate.

| Comparison on S9/S10 pure-silica parents | RMSE | Meaning |
|---|---:|---|
| Effective common-product composition descriptor |0.004808 cation Al fraction|Predicts Al acquisition and convergence|
| Direct parent composition copying |0.166667 cation Al fraction|Fails: predicts no Al in product|
| Common-product micropore baseline, calibrated on S5–S8 |0.009014 cm3/g|Closer to recovered-product N2 accessibility|
| Unchanged parent micropore volume |0.041231 cm3/g|Retained state-transfer mismatch|

The micropore baseline is0.1975 cm3/g; the held products are0.21 and0.20. N2 accessibility is measured after350C vacuum activation and at−196C, not during hydrothermal growth or PMo12 operation. These observations cannot be called inherited catalytic activity or a maintained boundary service. Table rounding and absent replicate errors limit the significance of small residual differences; no statistical inheritance-pass threshold is claimed.

## Why H and R remain open

1. **Topology and kinetics can remain seed-dependent while other states reset.** The source reports seed-conditioned induction/growth and no Beta in the unseeded case, but products converge in bulk composition. General seed dependence is not erased; the particular proposed information carrier is.
2. **New Al-bearing material is not yet newly competent functional material.** No catalytic reaction/selectivity assay separates fresh product from unchanged or altered founder activity.
3. **Founder contribution remains unbounded.** Selected yield values32.3–32.6% have no recovered explicit denominator/absolute dry mass. The10wt% seed/feed ratio cannot supply a final active-founder fraction.
4. **No serial functional variants.** The study does not track a founder-bounded chain transmitting alternative useful states. Qualitative high-ratio-core/low-ratio-shell XRD in the uncalcined case further separates retained parent from new state; it is not an extra numerical holdout.
5. **No common operating regime with PMo12 or Mo34WV.** Alkaline140C growth is not demonstrated to preserve the acidic electrochemical mediator or target. Original template use also remains disclosed.

Decision: retain Beta as a component-supported seeded-growth/porosity candidate, **reject direct bulk-composition copying in this source regime**, and leave functional inheritance and integrated active renewal unresolved. The next useful inheritance evidence must track a parent-associated function in new material under matched feed with a quantitative founder bound. It must not rely only on bulk ratio, topology or growth acceleration.

All source rows, missing fields and failed comparisons are preserved in [results/analysis.json](results/analysis.json) and [results/joined_tables.csv](results/joined_tables.csv). No source or negative result from the earlier Beta assessment was overwritten.
