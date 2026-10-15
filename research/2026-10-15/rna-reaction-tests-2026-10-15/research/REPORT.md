# Mechanistic alternatives and data admission

This review supplies a small, source-grounded set of competing hypotheses for the **bulk S13 assay**. It performs no fitting and selects no winner. Rate expressions below are proposed reductions, not microscopic rate laws established by the literature. Reporter-only observations cannot establish that a fitted trajectory of active F1 is correct.

## What the source actually measures

The retained Salibi SI identifies Hyper-A as 52 nt, B as a 14-nt 5′-triphosphate, and F1 as their 66-nt concatenation. Cy5-A differs by G38A and a 5′ dye; its ligation product is inactive. S13 has 5 µM Cy5-A and 7.5 µM B, with separate F1 or Hyper-A dose series at 42 °C, 20 mM MgCl2, 900 mM sucrose, and pH 8.5. Figure S13b proposes precursor-assisted reporter ligation. Figure S11 proposes a 2A2B structure; this does not establish a fourth-order kinetic law. S13d reuses endpoints and is not an independent validation set. [Salibi et al., article and SI](https://doi.org/10.1038/s41467-023-36940-z)

The selected prior revised model uses `hroute=0`: it forces the same `kf` on F1-mediated active-fragment and reporter ligation, while direct precursor-assisted reporter formation is absent. The previously tested `hroute=1` candidate enables that route and ties its coefficient to the `kh` for active-fragment initiation. Inspect `rna-mechanism-2026-10-15/model/model.py`, function `rates`. The new three-parameter baseline retains the selected `hroute=0` topology. Its previously fitted KB upper-bound and q=1 behavior cannot demonstrate saturation or an inactive substrate fraction. Those are diagnostics to reproduce, not evidence for a physical cause.

## Stoichiometry before kinetics

Use A=Hyper-A, R=Cy5-A, B=triphosphorylated fragment, F=active F1, P=inactive reporter product, I=inactive full-length wildtype. Each ligation consumes **one** A or R and **one** B; it releases one pyrophosphate. A catalytic molecule is returned unless a separate inactivation event occurs.

| Route | Net reaction | Proposed effective flux |
|---|---|---|
| F-mediated active-fragment ligation | F + A + B → 2F + PPi | `v_FA = k_FA F A g(B)` |
| F-mediated reporter ligation | F + R + B → F + P + PPi | `v_FR = k_FR F R g(B)` |
| Precursor-assisted active-fragment ligation | 2A + B → A + F + PPi | `v_HA = k_HA A² g(B)²` |
| Precursor-assisted reporter ligation | A + R + B → A + P + PPi | `v_HR = k_HR A R g(B)²` |
| Loss of functional state | F → I | `v_d = k_d F` |

Here `g(B)=B/(KB+B)` is a reduced occupancy function. The squared occupancy in the precursor routes is an assumption inherited from the revised model, not an extra stoichiometric B consumption. A putative 2A2B intermediate could release one F plus residual A and B, then recycle them; it does not require consuming two B per product. Do not conflate reaction order with material balance.

The corresponding free-species equations are `A′=−v_FA−v_HA`, `R′=−v_FR−v_HR`, `B′=−v_FA−v_HA−v_FR−v_HR`, `F′=v_FA+v_HA−v_d`, `P′=v_FR+v_HR`, `I′=v_d`. Therefore `A+F+I`, `R+P`, and `B+F+I+P` are conserved. This I state is a **loss of catalytic competence without fragmentation**, not a claim that RNA hydrolysis preserves intact mass.

## Minimal alternatives worth testing

1. **Independent routes:** release `k_FA=k_FR` and introduce an independent precursor-assisted reporter coefficient `k_HR`. The selected baseline fixes that route to zero; the previous enabled-route candidate instead tied `k_HR=k_HA`. The two substrates differ chemically, so equality is not guaranteed; no reviewed experiment measures their efficiency ratio in the S13 mixture. F1-only curves constrain `k_FR`; Hyper-A curves constrain active-path effects only indirectly. This five-parameter comparator tests equal F efficiencies and the omitted reporter route, but retains F1-only dose–time collapse and therefore cannot explain violations of that invariant.
2. **Functional inactivation:** append `F→I` with one rate to the three-parameter revised baseline, keeping material and activity separate. This four-parameter model breaks dose–time collapse through an independent clock. It cannot identify hydrolysis, unfolding, or chemical modification from fluorescence alone. Zero inactivation must remain nested.
3. **Independent routes plus inactivation:** combine the preceding changes as a six-parameter hypothesis. Additional freedom may improve interpolation without identifying active catalyst production; report parameter bounds and confounding.
4. **Finite-rate reversible trapping:** add `A+B⇌CA` and `R+B⇌CR` to the three-parameter baseline with shared `kon,koff` (five parameters total). Their net complex fluxes are `jA=kon A B−koff CA` and `jR=kon R B−koff CR`; free A/R/B enter catalytic rates. Complex formation changes free substrate on a clock independent of F and can break dose–time collapse. Both complexes are nonproductive in this candidate; the effective productive precursor route remains separate. This represents competing complexes rather than claiming that the productive 2A2B drawing is itself the trapped species. Shared binding constants for A and R are an unmeasured simplifying assumption. Report identifiability: neither separately estimated binding rate should be promoted to a measured chemical constant.

For explicit trapping, the conserved totals become `A+F+I+CA`, `R+P+CR`, and `B+F+I+P+CA+CR`. Substrate held in a complex must be excluded from free-substrate rates until released. A phenomenological inhibitor denominator alone would retain the F1-only dose–time symmetry if every remaining derivative is proportional to F; it is therefore a less useful explanation for a demonstrated symmetry violation.

### Initial complex state is a preparation assumption

S13 Methods says the mixture was prepared on ice and reaction initiated by adding magnesium and incubating at 42 °C. That defines the assay start but does **not** establish that every strand is unbound at that time. Pre-magnesium base pairing, duration on ice, and warming kinetics are not quantified. Register `CA(0)=CR(0)=0` as an all-free conditional initialization, with a prespecified equilibrium sensitivity using the same totals and `Kd=koff/kon`. Do not fit a separate initial fraction for every dose.

For shared Kd, let `T=A_total+R_total`; total complex C satisfies `Kd C=(T−C)(B_total−C)`, with `CA=C A_total/T` and `CR=C R_total/T` (both zero when T=0). The equilibrium calculation is a limiting preparation scenario at the model's rates; it does not establish ice-equilibrium occupancy or the actual initial state. If conclusions depend on this choice, the discrimination experiment needs controlled premixing time and an association measurement. A fitted lag is not evidence that a particular complex existed before incubation.

Freeze these alternatives and fit budgets before scoring. Do not add combinations in response to held-out errors. The preceding proposals deliberately omit a free fitted pyrophosphate-inhibition term, multi-state folding network, enzyme/product oligomerization network, and separate microscopic binding/release rates: the measured output does not independently constrain them.

## Mechanistic support and its limits

[Ferretti and Joyce 2013](https://doi.org/10.1021/bi301646n) directly characterize E/E′ component ligation, product dissociation, and competing substrate complexes. Their central distinction is between turnover limitation and substrate sequestration limiting overall amplification. They also report approximately 5% RNA degradation per hour under their 25 mM MgCl2, 44 °C conditions. This motivates a loss challenge; it is not a transferable Salibi F1 inactivation constant, nor proof that functional loss rather than substrate sequestration explains S13.

[Robertson and Joyce 2014](https://doi.org/10.1016/j.chembiol.2013.12.004) study optimized F1. The article distinguishes simple ligation efficiency from overall replication; temperature changes productive complexes, product release, and competing substrate complexes. It reports F1 single-turnover `kcat=16.6±0.4 min−1` and `Km=7.1±0.5 µM` with trace A and saturating B, and amplification at 48 °C/25 mM MgCl2. These values cannot be inserted as S13 multi-turnover constants. Neither those measurements nor the historical product-release rate establish a Salibi product-inhibition denominator.

[Olea and Joyce 2016](https://doi.org/10.3390/molecules21101310) engineered a variant to accept a fluorophore-modified B substrate. That experiment demonstrates that a label can require kinetic reoptimization; it does not quantify the effect of Salibi's different label and G38A change. Its real-time signal reports leaving-group release and uses a different enzyme/substrate design, so its curves are not an unused same-condition F1 test set.

## Additional numerical datasets: admission boundaries

The strongest available prediction test remains complete S13 dose curves held out together. These curves have already been inspected in prior work: call this retrospective grouped validation, never a blinded new experiment. With four doses per branch, reserve endpoint extrapolation separately from within-range interpolation and prevent model selection on the outer validation fold. Preserve every failed fit and prediction.

| Dataset | Status and possible use | Why it is not a same-condition independent kinetic test |
|---|---|---|
| S13 negative control | Two supplied zero summaries; structural null check | Already inspected; does not distinguish candidate active pathways |
| S12 serial transfer | 126 exported replicate values; functional-renewal challenge | 9 µM A/1 µM R/10 µM B, sucrose unstated; initial sampling/normalization ambiguity |
| S15 membrane addition | 18 exported replicate values; membrane sensitivity | Different dose and possible post-addition dilution; not bulk S13 |
| S18 FT bulk assay | 48 exported replicate values; temperature-cycle challenge | Different recipe and longer freeze/thaw; sucrose unstated |
| Salibi S10 | Gel images of mixed A/R, includes unseeded activity | No new compatible quantitative time-course table identified in this targeted review |
| Robertson 2014 figures/SI | F1 substrate/temperature and single-turnover measurements | Different Mg, temperature, reporter and substrate regimes; no numerical raw dataset acquired here |
| Ferretti 2013 tables/figures | Binding and component kinetics | Related E/E′ rather than same F1/G38A reporter mixture |
| Olea 2016 figures | Modified-substrate comparison | Evolved variant and different reporter mechanism |

The existing source export's row/cell provenance is retained; no values are silently pooled across conditions. This targeted search found mechanistic constraints and distinct-condition datasets, **no newly acquired compatible numerical holdout**. A decisive future dataset varies B independently and measures newly formed full-length wildtype plus activity, alongside matched reporter curves, under exactly S13 buffer/temperature. Independently measure activity after substrate-free F1 pre-incubation to test inactivation; a substrate concentration series or binding assay can challenge sequestration. These interventions distinguish the proposed causes more directly than another fit to the same fluorescent curves.

## Verification

Run `python3 rna-reaction-tests-2026-10-15/research/verify.py`. The artifact `research/.omo/evidence/verification.json` checks retained primary-source hashes, exact sequence identities, model equality locations, data row inventories, and the proposed net-reaction conservation equations. These are source/design checks, not verification of any mechanism or physical rate constant. Browser direct opens of Nature and PMC were blocked; indexed primary text was available and is identified in `sources.json`.
