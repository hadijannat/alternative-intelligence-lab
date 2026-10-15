# Experiments that could identify new functional F1 and its inheritance

15 October 2026. This is a prospective design. Source-supported chemical identities are distinguished from proposed analytical methods, planning thresholds and simulated effects. No wet experiment has been performed. The previous RNA model's failed kinetic fit is not a source of calibrated reaction rates.

## 1. Establish what the measurements identify

| Material | Identity/origin measurement | What identity alone cannot establish |
|---|---|---|
| Original founder F1 | Full-length 66-nt wild-type RNA carrying a validated permanent founder isotope code | Whether it remains active or was reactivated during recovery |
| Newly ligated F1 | Full-length 66-nt wild-type RNA, appropriate feedstock code and covalent A–B junction | Catalytic activity or the compartment in which it formed |
| Cy5-F1 reporter | 66-nt G38A mutant with Cy5; distinguish sequence and label from wild-type F1 | Production of new active F1 |
| Hyper-A and B | 52-nt precursor and 14-nt ligation partner, separately quantified | Hyper-A carryover can contribute to reporter formation |
| Inactive intact wild-type F1 | Same sequence and potentially same mass as active F1 | Its inactive state requires a functional measurement |

These identities are verified against Salibi's SI, including the sole G38A difference between Hyper-A and Cy5-A. [Primary study](https://doi.org/10.1038/s41467-023-36940-z); [exact sequence ledger and checks](research/assays/ledger.json).

A separate activity assay is essential. Even perfect measurements of founder amount, new amount and total activity can leave new activity ambiguous. For example, 10 fmol of old RNA plus 10 fmol of new RNA with 10 fmol-equivalent total activity is consistent with all activity being old or all activity being new. The simulations retain this counterexample.

## 2. Experiment A: qualify identity, provenance and functional attribution

First validate the observer in matched bulk and compartment-extract matrices. Use authentic wild-type F1, isotope-labelled F1, Hyper-A, B, Cy5-A, Cy5-F1, unlabelled G38A product, blanks and deliberately contaminated mixtures. Include an inactive wild-type preparation only if its inactivity is reproducible through processing; a sequence mutant is not a universal proxy for loss of wild-type function.

The proposed analytical workflow separates three aliquots:

1. **Identity and origin.** Validate full-length enrichment followed by intact mass and sequence-informative mapping. Require G38 identity and an informative ligation-junction fragment. Quantify precursor carryover, isotope overlap, degradation and analytical carryover. A complete nucleotide digest without prior species isolation loses molecule identity. MS is destructive; it does not prepare separate isotope fractions for the functional assay.
2. **Native-recovered capacity.** Recover RNA gently, challenge it with fresh inactive reporter substrate and B, omit fresh Hyper-A, and measure the initial product increment above the sample's time-zero background. Authentic F1 processed through the same procedure supplies the reference capacity scale. Establish the linear range and quantify nuisance-only mixed standards.
3. **Refolded capacity.** Repeat after the analytical denaturation/refolding route. Keep this result separate: restored activity can demonstrate refoldability without demonstrating survival of the original catalytic state.

The numerical planning model assigns half the sample to identity and one quarter to each activity route. Actual aliquot allocation must be requalified against the instrument and sample budget. RNA isotope labelling and LC-MS analysis have primary precedents, but they do not validate this complete 66-nt F1 assay or its detection limit. [Isotope methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC7810713/); [RNA LC-MS platform](https://pmc.ncbi.nlm.nih.gov/articles/PMC2790879/).

For a validated additive regime, calculate a conservative bound in common capacity units:

```text
new-capacity lower bound = max(0,
    total-capacity lower bound
  - pre-existing-F1 amount upper bound × maximum specific capacity
  - precursor/reporter nuisance-capacity upper bound
  - imported-catalyst capacity upper bound)
```

Use the upper envelope of nuisance-only mixtures if additivity fails. Without a calibrated envelope, return **unresolved**. A positive bound establishes a minimum contribution from new material; it does not identify the exact active fraction or assign function to every new molecule. Incompatible amount/function intervals are an assay-consistency failure, not positive evidence.

Qualification targets are prospective choices: label-equivalence confidence intervals inside 0.8–1.25; LOQ dilution-series bias and CV each at most 20%; off-target signal below 1% of the smallest target effect; and recovery uncertainty that covers the relevant mixtures. Confirm these using independent blinded standards. Failure requires a revised assay or a new protocol version, not silent error-bar reduction. Detailed gates are in the [assay source report](research/assays/REPORT.md).

## 3. Experiment B: separate catalyst retention from loss of function

Start with a purified, nonreacting F1 preparation without ligatable A/B feedstock. This isolates retention and inactivation from production. Measure before treatment, immediately after treatment, and after any warm incubation. Retain all inside, outside, wash and apparatus-associated fractions, with measured volumes and species-specific recovery standards added before and after processing.

Report three different estimands:

- Molecular retention: inside full-length F1 amount divided by its before-treatment amount.
- Capacity retention: inside native-recovered capacity divided by before-treatment capacity.
- Specific capacity: native-recovered capacity per recovered F1 molecule, with a paired before/after contrast.

Changing concentration is insufficient because volume changes can mimic retention. Unknown extraction recovery can exactly mimic leakage. Retained RNA can be inactive, and refolding can restore it. The simulation therefore includes high-retention/inactivation, low-retention/active, unequal-recovery and unqualified-recovery cases. Shared errors may cancel in a paired ratio only under its explicitly validated observation model.

Repeat the design with founder-labelled and newly formed F1 mixtures. Origin-resolved amounts plus capacity generally provide **intervals** for new-age activity retention, rather than an exact percentage. If the before-treatment new-capacity lower bound is zero, its retention ratio is unidentified.

Then repeat with the complete reaction, keeping immediate post-cycle and post-incubation samples separate. The source comparison uses 50 mM EPPS pH 8.5, 20 mM MgCl₂, 900 mM inner sucrose/outer glucose and 42°C. Device, wash, membrane, salt, volume or timing changes form separate conditions requiring calibration. Do not carry rates across these changes. No-feed and no-treatment preparations are matched controls; device-associated RNA and failed compartments remain in the accounting.

## 4. Experiment C: tracked physical generations and new function

Qualify a parent-to-two-daughter division platform before claiming a generation. Imaging must establish closed daughters and loss of lumen connectivity, not merely constriction. Record parent ID, daughter IDs, timestamps, volumes, integrity, external feed and any fusion/exchange edges. A mechanically divided liposome is an engineering precedent, but the published demonstration used different lipid/solution conditions and approximately 6-µm vesicles; it does not validate a larger F1-compatible growth/division platform. [Mechanical division study](https://doi.org/10.1021/acsnano.7b08411).

Repeated division also needs membrane/volume restoration and fresh substrate delivery. These are supplied experimental operations and contamination opportunities. The simulator charges feed and records external inputs. Division alone neither grows the family RNA inventory nor establishes autonomous reproduction.

Randomize independent root families to high versus low parental catalytic state at matched total RNA, buffer and volume. Randomize device positions and batches, then give descendants common conditions. Include no-founder, inactive-founder and no-regeneration controls. Compare intact transmission with a matched state-reset intervention; validate that the reset/sham handling has equivalent recovery and non-target effects. A parent-label shuffle is an additional analysis check, not a substitute for randomized experimental controls.

The primary simulation follows physical trees through six divisions. At generation 5, randomly assigned terminal daughters are destroyed for analysis while identified sisters continue; generation-6 descendants are then sampled. Pool only terminal descendants from the same root and generation. Every sacrificed member is removed from subsequent propagation. Independent roots and experimental batches, not daughters or instrument injections, provide replication. Missing pedigrees and failed samples stay in the denominator and contribute uncertainty.

Two provenance questions require different labels:

- A permanent founder code distinguishes original catalyst from material produced since seeding.
- A separately resolvable terminal-generation pulse identifies F1 synthesized during the sampled daughter incubation. Its nuisance bound includes **all** pre-pulse F1, including material synthesized in ancestors. Continuing sisters receive ordinary feed; separate terminal cohorts receive their pulse. Validate the additional code and quantify residual labelled precursors. Reusing two alternating codes cannot date every molecule uniquely.

A physical child can inherit catalytically active material without synthesizing it. Requiring a positive current-generation activity bound tests renewal inside the child as a distinct capability. The parental-state comparison is based on this new-capacity measurement, so surviving founder activity cannot alone create the claimed functional-state contrast.

Run isolated and exchange-permitted conditions, unrelated labelled donors and catalyst-free recipient sentinels. Measure outside active F1 and bound possible import. Unknown import remains a competing explanation. Optical parentage does not exclude molecular exchange, and newly labelled imported catalyst must not be called locally synthesized lineage material.

## 5. Material and statistical admission

At 1 µM, a spherical 10-µm GUV contains 0.524 amol of RNA. The relevant quantity is recovered analyte **amount**, after aliquot splitting. The numerical LOQs are hypothetical design scenarios, not measured specifications for a particular instrument.

```text
analysed fmol = concentration in µM × volume in pL × 0.001
               × recovery × aliquot fraction × relevant species fraction
```

Require the least sensitive necessary channel to clear its validated LOQ. Same-family pooling preserves a family-average estimand, but cannot establish that every daughter functions. A larger compartment requires its own chemical, transport and division qualification. Increasing the number of unrelated roots improves statistical replication; it does not repair a per-family assay below LOQ.

The numerical protocols freeze sample sizes, noise/calibration assumptions, effect thresholds, seed namespaces and decision rules before official runs. Planning targets are at least 80% sensitivity and at most 5% false-positive probability, assessed with Monte Carlo confidence intervals. Decisions must hold at both terminal generations and include identity, bounded new capacity, pedigree and control conditions. Strong, weak, carryover, inactive-new, reporter-only, shared-environment, common-feed and horizontal-transfer worlds are retained, including inadequate and inconclusive designs. [Assay protocol](assay/PROTOCOL.md); lineage protocol and numerical results are linked from the final report.

## 6. What a positive result would mean

A qualified positive experiment could demonstrate recovered new catalytic competence, its retention, and renewal-dependent persistence of a parent-dependent catalytic state over the observed generations. The fixed F1 fragments provide no established heritable sequence variants. Such a result would not by itself establish genetic inheritance, stable alternative types, evolution, autonomous life or intelligence. A negative or unresolved result identifies which measurement or physical mechanism remains insufficient.
