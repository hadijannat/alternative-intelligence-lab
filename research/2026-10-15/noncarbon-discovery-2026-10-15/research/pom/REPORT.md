# Carbon-free polyoxometalate candidates: what is supported

Reviewed 15 October 2026. This is a targeted primary-source assessment, with a new acquisition of the existing Mo36 dataset. No molecule was synthesized, no electronic-structure calculation was performed, and no living or intelligent system was discovered.

The most defensible experimental reference remains **[MoVI36O112(H2O)16]8−**. A proposed **[MoVI34WVI1VV1O112(H2O)16]9−** derivative is charge-balanced but has no verified structure or functional evidence in this review. It is a composition target to falsify, not an identified compound. Its proposed benefit is particularly uncertain because making a cluster harder to rearrange could impair the very assembly cycle needed for regeneration.

## Three bounded targets

| Target | Exact scope | Why investigate | Evidence boundary |
|---|---|---|---|
| T1: one-W/one-V Mo36-derived composition | Hypothetical [MoVI34WVI1VV1O112(H2O)16]9−; parent and singly substituted compositions are controls | Test whether a distinguishable redox site can coexist with the parent assembly motif | Only formal charge is established. No verified isolated structure, selective site occupancy, aqueous lifetime, autocatalysis, redox protection, inheritance, or novelty |
| T2: known Mo36 plus a known monovanadium Keggin | Mo36 reference with H4[PVMo11O40]; Na4[PVW11O40] is a separate W comparator | Separate assembly from a characterized inorganic redox readout before attempting one-molecule integration | Components are known. Their common-medium behavior and reciprocal support are unmeasured; a coupled configuration is not a new compound |
| T3: known Mo36 plus a Dawson charge reservoir | Mo36 reference with Li6[P2W18O62] | Test an explicitly concentration-dependent external energy reservoir | Low priority until compatibility is measured. Charge storage does not supply replicator identity or copying; dilution can discharge the reduced reservoir |

These priorities concern informative measurements, not the probability of non-carbon life. T1 is a high-risk exploratory target; T2 gives a more interpretable comparator. Neither can inherit the parent Mo36 results by analogy.

## Correct the chemical identity before screening

The Miras et al. abstract misassigns a Mo57-containing formula to Mo36. The author PDF's Figure 1 caption, visually inspected in the retained page image, gives **[MoVI36O112(H2O)16]8−**. Its all-Mo(VI) charge is 36×6−112×2 = −8; coordinated waters are neutral. A documented potassium salt is K8[Mo36O112(H2O)16]·nH2O. Hydration and counterion composition must be measured rather than inferred from the anion. [Primary paper](https://doi.org/10.1073/pnas.1921536117), [author PDF](https://www.chem.gla.ac.uk/cronin/images/pubs/Mathis-PNASMay2020.pdf).

For T1, 34×6+6+5−112×2 = −9. Reducing V(V) to V(IV), with everything else unchanged, gives −10. Formal Na9 and Na10 salts would balance those *unprotonated* formulas; they are not established isolable salts. Proton uptake, Mo reduction, hydroxo formation, water replacement or altered nuclearity changes this bookkeeping. The location of an added electron cannot be assigned to V from charge alone.

The conservative structural hypothesis would test peripheral octahedral substitution first, without assuming replacement of a pentagonal MoO7 center. This is chemical judgment, not a computed stable geometry. W and V incorporation might instead change the cluster, produce a mixture, or promote precipitation. No exact alternative formula is better supported merely by replacing atom labels.

Close prior art already exists for modified Mo36-related material. Sanchez Sanchez et al. assign {Mo36−xNbxO112} solution species by in-situ Raman during hydrothermal mixed-oxide formation, and describe shifts that *might* indicate partial V substitution. These observations concern 448 K reactions and eventual solid-oxide formation, with niobium oxalate among the inputs. They establish neither an isolated one-W/one-V molecule nor a wholly carbon-free operating process. Generic “heterometal-doped Mo36” novelty would therefore be a weak claim. [Primary author manuscript and SI](https://pure.mpg.de/rest/items/item_1849723/component/file_1854326/content), [published DOI](https://doi.org/10.1002/anie.201200746).

## Assembly, redox state and the missing reciprocal loop

Miras et al. report seeded lag removal and recognition-inhibition experiments for Mo36 in acidic water, with approximately pH 1.7 and a Figure 2 temperature of 24.3°C. Strong reduction in their tested preparation produced rapid decomposition in under one second. Their specific Mo36→Mo6 feedback mechanism remained experimentally unresolved and their large-network rates were phenomenological. PMo12 also had autocatalytic evidence in a separate preparation. The larger Mo132 cluster contains acetate; the PMo12⊂Mo124Ce4 example contains cysteine-derived ligands. Those demonstrated products fail a strict carbon-free active-framework screen. [Miras et al.](https://doi.org/10.1073/pnas.1921536117).

The present proposal must distinguish three outcomes:

1. Parent material persists or crystallizes: physical retention.
2. Parent accelerates formation of new material from feedstock: chemical amplification.
3. A rebuilt descendant retains a parent-specific catalytic or redox function in a shared environment: functional inheritance.

The cited POM studies do not establish outcome 3. They also do not show that a compartment regenerates its useful catalyst while that catalyst regenerates the compartment. Calling templated wheel assembly “reciprocal reconstruction” would supply a missing causal link verbally.

Raabe et al. characterize H4[PVMo11O40] and Na4[PVW11O40], including aqueous CV/SWV at pH 1 and 1 mM analyte. Their broader substitution series shows increasing isomer complexity and dissociation as V content rises. This supports a one-V reference with explicit speciation checks, not the assumption that more V improves function. Their molybdate preparation uses inorganic oxide/acid inputs; some NMR measurements use acetone-d6, and a free-acid extraction route uses ether. These analytical or preparative auxiliaries must remain visible in any carbon audit. [Primary paper](https://doi.org/10.3390/inorganics11040138).

Chen et al. study Li6[P2W18O62] as an aqueous electron reservoir, with up to 18 electrons per cluster under their conditions. Protonation, counterions and aggregation affect the state; highly reduced concentrated material is metastable and dilution can generate hydrogen. Thus an electron count cannot be imported as a durable memory state through serial dilution. Their redox state is externally written, not copied into newly assembled descendants. [Primary paper](https://doi.org/10.1021/jacs.1c10584).

## Public measurements and what they can constrain

The [retained seed table](raw/mo36_seed_timeseries.csv) contains **480 rows: six seed conditions with 80 observations each**. A fresh download at author-repository commit `5c143e908367fa756a5bf6468b6bd46a92c7bcd0` exactly matches the previous archive SHA256. The table gives native Time, Concentration and seed_value columns but no explicit units or replicate IDs. The c.pred columns are previous fitted predictions and must not be treated as data. [Pinned author table](https://github.com/croningp/clusterautocatalyticsets/blob/5c143e908367fa756a5bf6468b6bd46a92c7bcd0/Timeseries%20Data/Tidy_mo36_seeding_timeseries.csv).

This table can test retrospective within-condition forecasting. It cannot constrain W/V derivative kinetics, active retention, physical reaction constants without resolving calibration, or functional inheritance. The earlier repository calibration report already documents this boundary; this review does not relabel descriptive fits as chemical validation.

Raabe's supplementary Figures S38–S46 and Table S1 are identified as electrochemical data, but the SI download was not acquired here (attempted candidate URL returned 404; landing access failed). The main PDF and its tabulated molecular compositions were acquired. Crystal deposits 2240685/2240686 concern NaPV2W/NaPV5W, not T1. Chen's paper contains SAXS, redox and spectroscopy data; its full PDF was acquired, but no machine-readable raw kinetic/retention archive was recovered. None supplies repeated parent-to-descendant functional measurements for these targets.

## Decision gates for a useful next study

First establish solution identity and composition under a common solvent, pH, temperature, counterion and redox condition. A nominal formula is insufficient. Separately quantify parent survival, newly formed material and catalytic/redox function; retained founders must not count as reconstruction. Use the parent, each single substitution, an unseeded matched composition and an inactive or structure-destroyed seed control.

Only then test seed dependence across independent preparation batches, with held-out batches and perturbations frozen before fitting. Preserve failed synthesis, mixed-species outcomes, precipitation, loss of autocatalysis and function loss alongside successes. A shared-environment transfer test must distinguish a parent's transmitted function from a fresh feedstock-imposed equilibrium. These are acceptance questions; no wet procedure or successful result is asserted.

The smallest computational work justified now is charge/accounting and measured-reference validation. Inventing T1 rate constants, DFT energies, replication fidelity or memory lifetime would not create evidence. [Formula checks and data verification](checks.json) record the bounded checks actually performed; [source ledger](source_ledger.json) and [acquisition log](raw/acquisition.json) separate acquired files from failed access.

Skipped: wet synthesis, DFT/MD, complete patent/database clearance and raw electrochemical-curve recovery. Main risk: the proposed derivative may not exist as a stable single species, and no candidate has demonstrated carbon-independent functional heredity or intelligence.
