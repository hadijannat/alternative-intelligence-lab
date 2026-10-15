# Sources for a transport model that can retain seed history

The strongest new physical constraint is **local exchange through a transiently permeable membrane and its surrounding solution**. Global averaging, irreversible loss of activity, and uniform concentration thinning are separate model assumptions. None is directly identified by the recovered reporter ratio. This review supplies mechanism and condition constraints; it performs no measured-data fitting. The source ledger is [sources.json](sources.json), and download successes and failures are retained in [raw/retrieval.json](raw/retrieval.json).

## What the sources support

[Peter and Schwille (2023)](https://doi.org/10.1002/syst.202300008) observed mixing near the interface of deliberately separated GUV populations, spanning a few vesicle diameters. Dense packing reduced loss to the surrounding phase. Their tracers were 26-base DNA, in 900 mM sucrose/glucose, without the Salibi catalytic buffer. This supports finite local exchange and geometry-dependent leakage, not a measured graph radius or active-RNA retention constant. Raw numerical data are available only on request; no author was contacted. The article was inspected through the primary publisher's web reader; direct HTML and SI downloads returned HTTP 403.

[Litschel et al. (2018)](https://doi.org/10.1088/1367-2630/aabb96) found local density-dependent exchange, persistent membrane labels, and transport of cargo up to 40 kDa. Smooth gradients could extend across tens to hundreds of vesicles under their preparation. Therefore a universal nearest-neighbor radius and perfect immobilization of 66-nt F1 are unsupported. The primary PDF was acquired and its text extracted. Its 26-base DNA and dextran observations supply physical comparison, not matched catalytic calibration.

[Peng et al. (2022)](https://doi.org/10.1016/j.cub.2021.10.047) independently measured encapsulation effects on hairpin-ribozyme docking and activity. This establishes that folded availability and covalent RNA survival need not be the same variable. It does not measure reversible F1 inactivation or a freeze-thaw reset in Salibi's POPC GUVs. Accordingly, rescuing all inactive F1 after each cycle would be a deliberately optimistic sensitivity, not a source-established mechanism.

## Preserve the Salibi assay meaning

The [original study](https://doi.org/10.1038/s41467-023-36940-z) used separate F1, A/reporter, and B GUV preparations. F1 was added only initially. G0 precedes reaction; G1 follows three FT cycles and 60 minutes at 42 °C. Later generations combine equal suspension volumes of old material and fresh A/B feed, re-pellet, repeat three FT cycles, then incubate. The PAGE protocol washes away exterior material and counts recovered labelled ligation product relative to all recovered labelled strands. It does not directly assay active F1.

The retained article and SI provide the exact conditions and locations in the ledger. Three FT cycles correspond to the approximate 55% aggregate RNA retention used by earlier simulations. Its division into identical per-cycle factors, species-specific retention, and local concentration thinning are assumptions. Equal suspension volumes also need not imply equal internal aqueous volumes. Re-pelleting supports considering remapped contacts between generations; it does not establish persistent neighboring vesicles. Figures 2 FT3 and 3 G1 have the same nominal schedule but different measured means in the previous audit. Their difference must remain an assay-transfer limitation, not an adjustable dataset offset.

**The continuing serial culture is not documented as washed at each generation.** SI S19, lines 444–449, distinguishes the half transferred to feed from the collected aliquots: “Collected samples were washed”. Main Methods line 111 gives the same transfer sequence. Thus a local exterior pool must normally survive all three FT episodes and the subsequent transfer. Halve its inventory with the sampled suspension and add RNA-free feed exterior. Setting it to zero each generation adds an inaccessible-reservoir or wash assumption. Figure 2 explicitly washes only after FT and the 60-minute warm stage.

Preparation volumes do not identify accessible exterior volume. The general procedure starts with 24 µL aqueous emulsion input and 600 µL outer phase, then washes with approximately 700 µL and resuspends the pellet in approximately 15 µL outer buffer. Figure 2 uses 10 µL suspension aliquots. Figure 3 starts with 10 µL seed plus 20 µL substrate suspensions, discards 15 µL supernatant after the initial wash, takes 5 µL for G0, and subsequently transfers 5 µL old suspension into 5 µL feed. No measured encapsulated aqueous fraction, interstitial volume, or effective diffusion-accessible exterior/interior ratio is reported. These nominal preparation volumes cannot fix that ratio.

The S13 bulk calibration uses the same nominal buffer and temperature, but different substrate proportions and no vesicle interfaces. S15 changes substrate concentrations and lipid exposure; S18 uses 10-minute freezing and 10-minute thawing, whereas the PAGE GUV protocol uses 5+5 minutes. These are mechanistic challenges, not interchangeable calibration rows. SI Table 1 gives F1 66 nt, Hyper-A/Cy5-A 52 nt and B 14 nt. Length is available; membrane permeability and hydrodynamic radius are not.

## Which assumptions can erase seed dependence

These are deductions about the model, not new measurements:

1. **Global exchange erases co-localization.** Moving every compartment toward one population mean repeatedly reduces spatial variation. The mean of a nonlinear reaction is generally different from the reaction at the mean. A compartment's catalyst/substrate overlap can matter even when total inventories match.
2. **Uniform concentration loss suppresses every local reaction.** Removing molecules proportionally from all compartments lowers each nonlinear reaction rate. Losing a subset of compartments or replacing their contents has the same aggregate inventory effect but different local chemistry. The prior campaign tested two such limits and both failed; do not discard those outcomes.
3. **Irreversible competence loss removes founder information.** A fitted decline of reporter activity in a bulk model need not identify actual RNA destruction. Applying the same irreversible hazard to all competent strands, without reactivation or protection, is one restrictive interpretation.
4. **Background initiation plus one attracting serial state can remove history.** Under fixed local substrate trajectories, a small catalyst perturbation has approximate generation gain

   `M = (1/2) rF exp(integral_0^60 [ka A(t) B(t)/(KB+B(t)) - kd] dt)`.

   With common retention `rF=0.55`, the warm stage needs a net factor greater than `1/0.275 = 3.636...` merely to avoid contraction. This is a conditional linearization, not a measured threshold or a global stability proof. Locality can slow convergence but cannot guarantee retained seed dependence when all local perturbations contract and background initiation continually seeds the connected system.
5. **Observer retention can imitate propagation.** Preferential retention of ligated labelled product raises its PAGE fraction without producing more active F1. Track reporter denominator and active inventory separately; never count passive carryover as new function.

## Smallest defensible comparison

The final comparison keeps the frozen bulk chemistry and contains **three transport families**: the historical irreversible-loss/global-mean comparator, a finite common exterior bath, and deterministic effective exterior patches. There is no lattice, random contact graph or selective-mobility family. The patch reduction is

```text
dc_i,s/dtau = kappa (e_i,s - c_i,s)
de_i,s/dtau = (kappa/nu) (c_i,s - e_i,s) + D (mean_e_s - e_i,s)
mean_e_s = sum_i w_i e_i,s / sum_i w_i
interior volume = w_i; exterior-patch volume = nu w_i
```

The exchange operator conserves `sum_i w_i(c_i,s + nu e_i,s)` for every species. `nu` is a common effective exterior/interior volume ratio; `D` is an effective exterior equilibration rate per FT exposure. Neither is a measured spatial distance or pore geometry. Shared molecular permeability avoids silently privileging competent catalysts. The common bath is the homogeneous-exterior limit, not a separate fitted active-retention mechanism.

At the start of the warm stage, exterior patches are homogenized conservatively to their weighted mean. Interior membranes are treated as closed, and interior chemistry proceeds independently. This exterior homogenization is an unmeasured closure that intentionally removes exterior spatial correlations between FT exposure and warm chemistry. It must not be described as observed local neighborhoods or inherited vesicle contacts.

Serial transfer halves old interior cohort weights, adds fresh A and B weights of 0.25 each, halves exterior concentration through addition of RNA-free feed exterior, and redistributes the resulting exterior uniformly. This assumes the initial and feed suspensions share the same `nu`. The nominal suspension volumes do not establish that equality.

For a closed initially empty exterior bath with volume ratio `nu=Ve/Vi`, uniform initial internal tracer, equal permeability, and zero FT chemistry, the proposed exchange equations imply

```text
R(3) = [1 + nu exp(-3 kappa (1 + 1/nu))] / (1 + nu)
kappa(nu) = -nu/[3(nu+1)] log([0.55(nu+1)-1]/nu)
nu > 9/11
```

This is algebraically consistent for the nonreacting reference and for the weighted mean of equal-permeability patches. It reduces parameters by treating the approximate gel-based 55% figure as an exact initial tracer constraint. It does not convert that estimate into a measured uniform-tracer experiment or establish a physical pore rate. A carried, nonempty bath will not continue to impose 55% interior retention every generation; that is an intended distinction from repeated global loss.

The primary finite-bath models carry exterior inventory and allow exterior warm chemistry using the same frozen bulk rates. A fixed 2×2 sensitivity crosses **reactive versus inert exterior** with **carried versus discarded exterior**. Applying sucrose-calibrated rates in glucose exterior and setting exterior reactions to zero are both unmeasured kinetic closures. Discarding the exterior at the registered serial boundary represents an inaccessible-reservoir limit; it is not the reported sampling-only wash. All four outcomes must remain visible, without choosing the best benchmark after inspection.

Fresh feed creates new substrate compartments and reduces the sampled **number/weight** of old ones. It should not halve the concentration inside surviving old compartments before exchange. This distinction is already respected by the prior cohort model and is not a newly discovered coding bug. All reaction and observer moieties must survive exchange and sampling bookkeeping.

Freeze model families, homogenization rules, numerical tolerances, bounds and selection rule before new transport fits. Calibration on selected Figure 2 rows does not make previously inspected Figure 3 prospective data. Withhold whole seed arms and later generations, report all fixed models and every failed screen, and retain unresolved fits. A gain in reporter prediction alone cannot validate the hidden active-catalyst inventory.

## Useful measurements still absent

No new numerical dataset matching the original R3C/POPC/buffer/FT/observer conditions was acquired. Peter's microscopy would constrain spatial covariance, mixing-distance distributions, density and loss jointly if raw coordinates and intensities became available. It would still not identify active F1. Existing coacervate and fatty-acid retention datasets retained in earlier laboratories remain different chemistries.

A new public [Tsuji (2026) dataset](https://doi.org/10.1038/s42003-026-10218-8) was acquired with the final article and SI: seven workbook sheets cover mixing, initial RNA dose, recipient ratio and seven passages. It concerns 2041-nt RNA copied by supplied protein Qβ replicase. The serial protocol uses 50% DMSO, −20 °C for one hour, explicit exterior replacement, and 37 °C for two hours; protein enzyme and nucleotides are replenished. Its feed-withdrawal arm is a useful negative control. Initial RNA dose is varied in the single-round experiment; the serial experiment uses one initial dose and includes overnight/12-day storage. It therefore does not establish serial seed memory or autonomous catalyst inheritance. The workbook's serial sheet lacks replicate identifiers, and threshold/fluorescence column wording needs clarification before quantitative reuse. No values enter this laboratory's measured calibration or validation. [Dataset inventory](dataset_inventory.json) preserves sheet coverage and cell locations; the complete workbook is retained.

The discriminating dataset would pair, for the same populations and each FT/feed stage, recovered full-length F1 mass, activity after standardized release/refolding, precursor and reporter recoveries, interior volumes, and catalyst/substrate spatial covariance. A labelled founder/new-product distinction plus descendant activity would be needed for functional inheritance. These are measurement priorities, not performed experiments.

Run `python3 rna-seed-transport-2026-10-15/research/verify.py` from the workspace root. [Verification](verification.json) checks retained source hashes, exact local passages, workbook inventory, closed-bath algebra and weighted patch conservation. This checks provenance and algebra, not the empirical adequacy of the transport model. The primary publisher web passages for Peter and Peng were inspected online but could not be retained as complete downloaded source files; the ledger records that access limit.

No model fit, author contact, wet experiment, or exhaustive dataset scrape was performed in this source review. The principal risk is mistaking a successful transport fit for identified active retention or inheritance.
