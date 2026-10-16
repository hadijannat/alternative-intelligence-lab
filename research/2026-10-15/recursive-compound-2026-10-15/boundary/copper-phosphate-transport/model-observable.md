# Coupled volume, composition and competence: what the growth measurement identifies

This is a conditional balance model, not a fitted transport simulation. It changes which parameters may be inferred from the recovered source. The target's identity and boundary compatibility remain unresolved. No numerical coefficient below is calibrated to target material.

Define Vg as observed geometric tube volume, Vw as solid-wall volume inside that geometric envelope and Vl = Vg - Vw as liquid volume. All volume rates have the same units. Let Qp be delivered pump flow, Qm net inward membrane liquid flow, Qt tip/outlet flow, and Sv liquid-volume change from reaction/mixing or other explicitly measured sources. An incompressible control-volume balance is

dVl/dt = Qp + Qm - Qt + Sv,

hence

dVg/dt / Qp = 1 + (Qm - Qt + Sv + dVw/dt) / Qp.

Only with negligible tip loss, reaction/mixing-volume change and wall-volume growth does a geometric ratio equal 1 + Qm/Qp. The reported 1.89 +/- 0.05 is a regression slope of geometric volume-growth rate against pump flow, not necessarily a pointwise ratio: a nonzero intercept would contribute an additional intercept/Qp term to that ratio. The source does not establish a zero intercept. The reported slope by itself does not measure every term in the balance. Changing a growth regime or wall thickness can alter the observation without the same change in molecular selectivity. The author's osmotic interpretation is retained as an interpretation rather than relabeled as a solute assay.

Even an independently measured Qm would constrain hydraulic permeance only after interface area and the hydraulic/osmotic driving forces are known. For inward-positive Qm, define DeltaP = Poutside - Pinside and DeltaPi = pioutside - piinside. A relationship such as Qm = A*Lp*(DeltaP - sigma*DeltaPi) then introduces an additional constitutive assumption; this source observation does not separately identify Lp, sigma, effective area or all electrolyte activities. Concentrated reacting electrolytes cannot silently be replaced by ideal dilute solutions.

For cargo, use disjoint inventories of intact competent clusters C, intact inactive clusters I, fragments F and wall-bound forms, as defined in ../active-retention-identifiability.md. Each species needs its own advective/diffusive passage, adsorption/desorption and chemical-conversion terms. Metal conservation constrains these reactions; it does not choose their rates or competence. The proposed wall contains copper/phosphate rather than target Mo/W/V, which simplifies some elemental attribution but leaves molecular and functional identification unresolved.

There is an exact observational non-identifiability here: hold wall and background chemistry fixed, with zero target in the initial state, feed and internal sources. Then a tube-growth experiment has the same geometric observation for any assumed target permeability or inactivation rate, because target concentration and its reaction terms remain zero. Models predicting zero, intermediate or complete target passage when target is later supplied are therefore indistinguishable under this target-free dataset. This does not predict zero passage after adding target. A high fitted growth slope cannot favor one of those target models. Five linear-growth rows also cannot become target-training or target-holdout data by relabeling their endpoint.

The next discriminating observation is paired species-resolved donor/permeate/wall recovery and standardized competence in a jointly established medium, with measured volumes, wall material and tip losses. Treat phase changes, support dissolution and precipitate growth as chemistry states coupled to transport. Only then can conservation plus held-out interventions test seed-dependent retention against background formation, without importing a generic background-suppressing parameter.
