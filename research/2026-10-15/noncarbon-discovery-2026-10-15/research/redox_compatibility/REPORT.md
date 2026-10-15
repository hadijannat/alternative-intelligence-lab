# Common-medium redox and transport compatibility

Reviewed 15 October 2026. **Neither Mo36 + hydrated WO3 nor the nominal Mo34WV derivative has demonstrated common-medium compatibility, active-state inheritance or autonomous maintenance.** The literature supports separate assembly and state-storage functions. Differences between published conditions identify tests; they do not by themselves prove that coupling is impossible.

This audit read the POM, memory and critical dossiers, independently checked primary material, and used one read-only child agent for oxide-condition extraction. It ran no chemical simulation or experiment. The [condition table](conditions.csv), [source ledger](sources.json), [access log](raw/acquisition.json) and [verification](verification.json) retain unresolved fields and failed access.

## Reported conditions

Values below are reported conditions, not a preparation protocol. No potential scale was converted here. Nominal acid concentration is not substituted for measured pH.

| System | Medium, temperature and concentration | Electrical / atmosphere boundary | Observation and scope |
|---|---|---|---|
| Mo36 assembly | Approximately pH 1.7; 24.3°C. Reported molybdate 0.25 M/HCl 0.047 M have a feed-versus-initial-concentration ambiguity. | No imposed potential; oxygen handling not specified for this assay. | Seed-dependent formation. At pH >4.5 formation slows; strongly reduced conditions (>60% Mo centers) cause decomposition within one second. These are parent-system observations. [Miras 2020](https://doi.org/10.1073/pnas.1921536117) |
| WO3 / mono- and dihydrate electrocatalysis | 0.5 M H2SO4; electrochemical temperature not explicitly stated in main methods. | Continuous H2 purge; Hg/Hg2SO4 reference calibrated to RHE; imposed current/potential. | HER begins above approximately 450 mV overpotential. Monohydrate is the strongest HER catalyst of these three phases. This is a possible charge-consumption pathway. [Spencer 2024](https://doi.org/10.1039/D4SC00102H) |
| Hydrated-oxide operando diffraction | Same nominal acid; electrodes contain Nafion and carbon. | Leakless Ag/AgCl cross-calibrated to RHE. Monohydrate CV spans −0.493 to +0.644 V versus RHE. | Hydrates show no detected phase transition; monohydrate morphology remained unchanged after a separate cycling check to −0.8 V versus RHE. This argues against assuming inevitable dissolution. [Spencer 2024](https://doi.org/10.1039/D4SC00102H) |
| WO3/Nafion/PdHx memory device | Room temperature; nearly 100% relative humidity; solid device, not an aqueous suspension. | 5% H2/Ar, without ambient-air exposure; gate/channel voltages referenced to the device's PdHx reservoir, not RHE. | Electron-blocking electrolyte helps retain state. Oxygen ingress, hydrogen loss and electrode degradation are identified risks. [Yao 2020](https://doi.org/10.1038/s41467-020-16866-6) |
| Crystalline WO3 thin-film interfacial kinetics | Principal kinetic measurements: 2 M HCl + 2 M KCl at 70°C. Separate pH comparison: 0–4.5, ionic strength 4 M. | SCE reference; authors report selected results on RHE; oxygen handling not found in reviewed main methods. | At pH 4.5 current/capacity decreases and dissolution is inferred. Rates vary with interface, film and conditioning; these are not room-temperature hydrate constants. [Roychowdhury 2025](https://doi.org/10.1021/acselectrochem.5c00137) |
| Monovanadium Keggin comparators | H4[PVMo11O40] / Na4[PVW11O40]; 1 mM analyte, HCl-adjusted pH 1. | CV/SWV; reference, temperature and oxygen handling unresolved in acquired main paper; SI inaccessible. | Characterized redox comparators; no transferable potential is assigned to Mo34WV. [Raabe 2023](https://doi.org/10.3390/inorganics11040138) |
| Reduced Li6[P2W18O62] reservoir | Concentration-dependent aqueous behavior, including 50–100 mM cases. | Externally electrochemically charged. | Highly reduced clusters aggregate/protonate; dilution can release H2. Serial transfer cannot assume conserved stored state. [Chen 2022](https://doi.org/10.1021/jacs.1c10584) |
| Nominal [MoVI34WVI VVO112(H2O)16]9− | No established solution identity, concentration or operating window. | No measured redox potential, site localization, electron path or transport coefficient. | Formal charge only. Every compatibility endpoint remains unmeasured. |

The Miras main text and SI describe equal-volume feed mixing, whereas figure captions label the same concentrations as initial values. The SI also uses “increased [H+]” beside pH >4.5. This audit preserves those inconsistencies; it does not repair the source by guessing final concentrations or a corrected boundary. Its chemical-reductant experiment provides no electrode-potential threshold for Mo36 destruction. The single-V reduction hypothesis cannot be assessed by equating it with reduction of most Mo centers.

Spencer's three overpotentials at 10 mA/cm² (501.0, 531.7 and 621.5 mV for monohydrate, anhydrous and dihydrate) are interpolated from quasi-equilibrium chronoamperometry, not directly sampled at that current. Bulk-proton participation in HER is the authors' mechanistic interpretation, supported by electrochemistry/structure/calculations. Their study does not measure autonomous memory retention.

## Pairwise compatibility test

This is an evidence test of claims, not an equilibrium or kinetic calculation.

| Claim | Disposition | What would resolve it |
|---|---|---|
| Mo36 assembly and hydrate state storage survive one shared acid/counterion/temperature environment | **UNMEASURED** | Simultaneous species-resolved Mo36 identity/formation and oxide proton-state measurements in the same medium. Acidic operation of both separately is insufficient. |
| A reduced oxide can support Mo36 renewal without destructive over-reduction | **UNMEASURED** | Actual interface potentials, electron transfer and cluster speciation. Parent over-reduction is a contrary regime, not a single-electron veto. |
| Mo36 or another POM can program the oxide without an externally wired circuit | **UNMEASURED** | A charge-balanced electron-transfer pathway plus proton flux. Proton diffusion alone does not supply the accompanying electron. |
| Faster coupling preserves a parent-specific state | **UNMEASURED** | Distinct initial states followed through exchange and new-material formation. A redox mediator can also equilibrate compartments; this is a physical inference, not a measured erasure rate. |
| The useful oxide survives operation without metal dissolution/reconstruction | **CONDITION-DEPENDENT; JOINT TEST UNMEASURED** | Dissolved-metal and structural balances in the actual mixed system. The hydrate result and higher-pH thin-film loss must both remain visible. |
| W/V substitution preserves Mo36 topology and adds a stable redox memory | **UNMEASURED** | Identity, site occupancy, reversible function and newly formed descendants. Charge arithmetic cannot establish any of them. |
| Physical retention supplies functional inheritance | **UNMEASURED** | Newly made material retains seed-conditioned function after founder carryover is excluded. None of the reviewed coupling studies supplies this endpoint. |

## Consequence for the proposed compound and model

For the nominal anion, `34×6 + 6 + 5 − 112×2 = −9`; a formally V(IV) counterpart gives −10. This calculation assumes fixed oxide/aqua counts, unprotonated oxide sites and the assigned oxidation states. It does not locate an added electron or verify the molecular structure. No meaningful predicted transport rate or safe potential window can be calculated from this formula alone.

A defensible future model must separately account for dissolved POM states, oxide proton/electron occupancy, finite vacant sites, solution ions and an explicit electron-transfer route. Include HER, oxidation/loss, dissolution and state equilibration only with measured parameters or visibly labeled hypotheses. At full occupancy, an insertion-only model has no vacant capacity; extra reducing input needs another explicitly accounted pathway. A single unrestricted transport coefficient or infinitely receptive charge reservoir would conceal the central failure modes. These are conservation constraints, not evidence that a particular integration works.

The next decisive evidence is a joint same-medium measurement, followed by complete-condition held-out tests. First establish chemical identity and reversible function; then distinguish retained founders from new functional descendants. Preserve failure to form the target, mixed species, irreversible discharge, diminished seed dependence and environmental equilibration as negative outcomes. No simulated heredity result is reported here.

Skipped: new fitting, atomistic calculations, exhaustive speciation databases and wet synthesis. Main risk: coupling can consume or equalize the stored state, and the nominal Mo34WV species may not exist as a stable single compound.
