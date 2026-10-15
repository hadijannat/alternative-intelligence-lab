# Chemistry and independent challenge evidence

The high-concentration background reaction is experimentally real. A coupled model must explain why it is strong in bulk yet remains weak in the serial vesicle control. Simply turning down the Hyper-A route until the serial control fits would discard a useful falsification test.

This review made no measured-data fit, changed no earlier laboratory, and contacted no authors. The retained workbook and literature had already been inspected in earlier work: their unused conditions are retrospective challenges, not newly blind data. Source locations and SHA256 digests are in `sources.json`; `verify.py` independently checks the extracted challenge values against the workbook.

## What can and cannot be inferred from fragment chemistry

Salibi's Figure S11 depicts a base-paired tetramer containing two A and two B fragments. It is a static secondary-structure drawing, without ligation arrows, measured occupancy, or rate constants. It supports considering finite fragment complexes. It does not establish that a collision of four free molecules is elementary, that both ligation sites react simultaneously, or that one event creates two released F1 molecules. S13b separately depicts Hyper-A assisting reporter ligation while returning to the catalyst position. The mutated reporter is inactive after ligation. [Salibi et al.](https://doi.org/10.1038/s41467-023-36940-z)

There are two chemically different issues: reversible sequestration into nonproductive complexes and finite occupancy of a productive catalyst. In F1 self-replication, Robertson and Joyce identify nonproductive A–B complexes that lower substrate availability. They also report that faster F1 catalysis increases both catalysed and spontaneous replication. These observations argue for testing limited availability while retaining background initiation. Their conditions differ from Salibi's sucrose assay; their F1 kinetic measurement used enzyme-excess single-turnover conditions with trace A and 100 µM B, rather than the serial-vesicle mixture. Its constants are not direct parameters for this laboratory. [Robertson and Joyce](https://doi.org/10.1016/j.chembiol.2013.12.004)

Earlier E/E′ work directly measured product release and competing substrate binding. Its approximately 0.1 µM substrate-complex dissociation constant and greater-than-1/min dissociation rate belong to cross-replicating E/E′ under its own buffer and temperature. They support the existence of a competing-complex mechanism; fixing these numbers as Salibi F1 constants would be an unsupported transfer. [Ferretti and Joyce](https://doi.org/10.1021/bi301646n)

## Minimal model implications

The existing `kh A² [B/(KB+B)]²` term is a phenomenological low-dimensional background law. S13 observes reporter yield at A=1–2.5 µM, not a direct measurement of the newly created active F1 inventory. Extrapolating the same free-fragment law to a concentrated cohort, a persistent exterior pool, and repeated feeding leaves the active feedback route weakly constrained. The positive feedback can amplify any small initiation error over many generations. This is an interpretation of the model structure, not evidence that all observed background is an artefact.

The smallest defensible comparisons retain the old model and change one chemical assumption at a time:

1. **Finite precursor availability.** Add reversible pools `A+B ⇌ U_A` and `R+B ⇌ U_R`, with explicitly counted A, reporter and B moieties. A declared nonproductive closure permits productive events only from free molecules. Alternatively, treating a precursor pool as a catalytic target requires stating that productive conformer closure. The source does not identify the proportion of these roles.
2. **Finite catalyst occupancy.** A and R compete for a finite catalytic pool. In a rapid-equilibrium reduction, a shared occupancy denominator bounds total turnover at fixed catalyst inventory; in an explicit complex model, binding consumes available catalyst and ligation/release restores it. The A and R products have different functional roles even when affinities are tied to economise parameters. The Hyper-A initiation route must remain present.

These changes may be combined if their separate tests justify the added parameters. A reduced net background event `2A+B -> A+F` represents an A catalyst plus an A/B target; `A+R+B -> A+P` represents its reporter analogue. Both conserve RNA moieties and require only one net B per ligated product. A `2A+2B` intermediate must retain its unreacted A/B contents if only one product is released. It must not silently consume two B to create one F. Conversely, `2A+2B -> 2F` is a possible two-ligation closure, not an observation established by S11.

Preserving a full-length competent inventory does not establish enzyme availability: bound, inactive and free states require separate accounting. Transporting all complexes at the same permeability as free RNA is a declared closure because the tracer does not identify complex mobility. Neither membrane-dependent rate factors nor selective catalyst protection can be fitted from the current PAGE observable alone. Report inside/outside active inventories and reporter-production increments alongside the reporter fraction. The observer's denominator and the continued culture must remain distinct.

## Existing numerical challenges

| Dataset | Exact conditions and contents | Admission |
|---|---|---|
| S13 | 5 µM Cy5-A, 7.5 µM B, F1 0.1–1 or Hyper-A 1–2.5 µM; 20 mM MgCl2, 50 mM EPPS pH8.5, 900 mM sucrose; 42 °C | Existing means/SD/n. Whole-dose and late-time splits remain retrospective. |
| S18, zero FT plus 42 °C | Hyper-A9, Cy5-A1, B15, F1=0 or1 µM; 60 min at42 °C; EPPS/MgCl2 listed, sucrose not listed | Six exact replicate values, suitable for a separately labelled high-substrate **buffer-transfer challenge**. No FT-rate assumption is needed at zero FT. |
| S18, FT arms | Same recipe, one FT=10 min−80 °C plus10 min room temperature, optional60 min42 °C | 48 total replicate values. These demonstrate nonzero pre-incubation chemistry but do not identify kinetics for the shorter GUV5+5 min cycle. |
| S15 | Nominal Cy5-A0.5, B1, F1=0 or1 µM; 0/0.25/0.5 vesicle-suspension fraction; 60 min42 °C | 18 replicate values; low-substrate membrane-modulation challenge. Methods add10 µL buffer/GUV mixture to10 µL reaction, while caption repeats nominal concentrations. The possible twofold dilution is unresolved. |
| S10 | Methods: Hyper-A4.5, Cy5-A0.5, B12, F1=0 or0.5 µM; same sucrose/Mg/EPPS/42 °C as S13 | Stronger condition match, but workbook contains embedded gels without a numerical table. Caption instead says5 µM each substrate. No numerical holdout extracted or recipe conflict silently resolved. |
| S12 | Hyper-A9, Cy5-A1, B10; seed0/1 or inactive reporter-only control; 30 min42 °C and tenfold serial dilution; sucrose not listed | Already exported126 replicate values. Earlier work identified unresolved initial-sampling/normalisation behaviour. Retain as functional-renewal context, not an exact matched-condition fit. |

At zero FT after42 °C, S18 reports unseeded yields **63.832,62.544,62.042%** and seeded yields **67.115,70.555,67.602%**. Their means are62.806% and68.424%, a5.618-point difference. These numbers constrain the direction of any claim that strong bulk background must be absent; the buffer difference prevents imposing them as a hard matched-condition calibration target. S15 bulk F1 yields are25.52,9.978,32.663%, compared with39.717,35.847,40.145% at0.25 suspension fraction and41.205,42.632,42.107% at0.5. All corresponding negative-control entries are zero. These are membrane-associated modulation under that assay, not a measured correction factor for the encapsulated reaction.

## Evidence boundary

No compatible new measurement of F1/Hyper-A association, active-catalyst survival, complex permeability, or paired functional inheritance was found in this targeted review. The six S18 zero-FT values are especially useful because they can reject an implausible background-suppression mechanism without pretending that buffer transfer is known. Freeze the challenge treatment and any uncertainty sensitivity before looking at candidate scores. Report every candidate, capped fit, failed accuracy screen and seed-contrast failure.
