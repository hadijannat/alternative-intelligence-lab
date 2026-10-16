# What an active-retention experiment must identify

No current source or calculation establishes intact, active retention of nominal Mo34WV. The zirconia experiment measures PEG separation after corrosion exposure; the different aqueous POM comparator uses destructive zinc analysis. The new POM/polyoxocation boundary proposal also contains Mo and W, so elemental uptake could include wall formation as well as the proposed cargo. The following is an unexecuted measurement design and conservation argument, not a fitted transport model or a successful complement.

## Separate identity, activity and total inventory

For a parent-Mo36 comparator, let C be intact competent clusters, I intact inactive clusters and F all other Mo in Mo-atom equivalents. Each donor, receiver and wall compartment has these states. C and I are amounts, not concentrations; measure volumes independently. Include collected effluent and withdrawn samples:

36 sum(C + I) + sum(F) + M_effluent + M_sampled = M_initial + M_feed.

These inventories are disjoint: collected permeate leaves the receiver inventory before entering the cumulative effluent term, and wall metal already counted in F is not added a second time. Include initially present wall Mo/W in the initial elemental inventory when applying the target balance below.

The observable total Mo cannot identify competence. The three nonnegative states (C,I,F) = (1,0,0), (0,1,0) and (0,0,36) each give 36 Mo-atom equivalents. Even a perfectly calibrated intact-cluster measurement C+I cannot distinguish the first two. This is an exact counterexample to inference from total retention, without choosing kinetic constants or assuming a linear activity assay.

For the nominal target, the corresponding metal inventory vector is (34,1,1)(C+I) + (F_Mo,F_W,F_V), with separate sampling, effluent and feed terms. These are conditional bookkeeping identities for the proposed stoichiometry; they do not establish that such clusters exist. An apparent 34:1:1 ratio can also arise from a precursor or fragment mixture. If a complement contains those elements, include its independently measured inventory rather than assigning all recovered metal to the target. The POM/polyoxocation pair contains both Mo and W; La, P and Si are useful additional observations, but changing wall composition prevents treating a fixed marker ratio as proof of intact cargo.

Seed competence is a separately calibrated functional response under standardized conditions. Neither product yield nor a lag time is automatically a linear cluster count. Matrix effects, heterogeneous nucleation, altered founders and fragments can reproduce apparent activity. Analytical identity and catalytic competence must be measured on appropriately matched recovered fractions; multiplying unrelated bulk fractions does not prove their intersection.

## Smallest discriminating sequence

1. Establish a parent-compatible medium and molecular identity assay before the membrane experiment. A parent result is a comparator; it cannot admit the substituted target. For the target, repeat with independently established target identity and its actual medium.
2. Pulse characterized clusters through the specified boundary, then chase with cluster-free matched medium. Follow donor, permeate, collected effluent and validated wall extracts over time. Run membrane-free aging, membrane-only blank and matched no-flow contact/wash controls. Measure total elements, intact species and standardized competence, with recovery standards and uncertainty.
3. Independently measure precursor passage and proton/acid input-output accounting. pH alone is not a proton flux. Measure support dissolution. Keep inaccessible wall inventory as unresolved recovery rather than calling it destruction.
4. Only after intact competence survives, transfer measured recovered material into clean vessels containing precursor feed without freshly supplied active clusters. Compare zero seed, recovered seed, characterized parent/target seed, activity-disabled matched material and membrane-blank eluate. Follow formation and competence through measured serial transfers.
5. Bound founder carryover across liquid and wall inventories, including protected adsorbed material and altered founders. Where suitable labels exist, close each label balance and test exchange/recycling. Label incorporation alone does not demonstrate new competent clusters or functional inheritance.

Use the existing protected-founder rival in [carryover-v1](../../discovery-loop/experiments/carryover-v1/model.py) as a logical control. The RNA work supplies conservation and observer distinctions, with its [transport failure retained](../../rna-turnover-tests-2026-10-15/transport_diagnosis/REPORT.md); its numerical rates do not transfer to POM chemistry.

## Parameters still unidentifiable

Existing data do not determine intact-cluster permeability, adsorption/desorption, destructive transformation, competent fraction, background nucleation, seed-dependent production or wall renewal rates for either the parent in the proposed boundary or the target. The reported 97% elemental endpoint cannot supply these rates. No target training/holdout split exists, and none is invented here. Freeze assay precision, schedules, competing mechanisms and decision thresholds before collecting the corresponding outcomes.

After retention and propagation, boundary renewal still needs a distinct loss/restoration test: controlled wall loss, restored selectivity, persistent cluster identity/competence, material accounting and interruption of the proposed repair coupling. A visible growing precipitate does not close that requirement.

Independent design challenge: /root/cpcm_memory_design identified missing identity/recovery observations, founder discrimination and prospective thresholds. Root added the exact inventory counterexamples and the Mo/W-containing-wall confound. No physical experiment, numerical fitting, target validation or complement admission occurred.

Independent final design review found no material error and requested explicit disjoint inventories and initial wall-metal accounting; those clarifications are included above. Approval covers the unexecuted design only.
