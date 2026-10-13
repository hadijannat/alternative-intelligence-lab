# Final research results — 13 October 2026

## Scientific conclusion

The full objective was an alternative chemical system supporting integrated maintenance, functional heredity, adaptive evolution, physically implemented cognition, human-comparable capability and supported evolutionary connections. **That objective was not achieved.** The final chemical checkpoint, E1092, is blocked at a qualified-input dependency; all integrated G0–G6 gates remain unresolved.

The campaign identified useful assembly, materials and information-processing subsystems. It also produced conditional calculations, engineered digital constructions and negative model results. These outcomes narrow particular questions without establishing a naturally emerging alternative organism.

This publication is the final saved record of the campaign requested by the maintainer. Its constituent studies have different start dates and scopes. Earlier work is retained as historical context; the snapshot is not a homogeneous six-day experiment or six days of uninterrupted physical measurement.

## Current canonical evidence map

Registry **v2.44** contains **329 explicit preparations across 58 source-architecture groups**. Preparations in a common family are not independent origins of life. The inventory includes:

- Inorganic chemistry and mineral assemblies.
- Carbon-containing alternatives, hybrid routes and conventional biological controls.
- Fabricated physical information-processing devices.
- Candidate interfaces and externally maintained experimental preparations.

The initial 6 October review contained 10 candidate groups (C01–C10) and 34 claim records across 30 primary URLs: 28 records for those groups and six cross-cutting records tagged `CROSS`. Its claim-level ledger is published separately. It is an earlier bounded study, not the full latest registry.

## Mo36 interface comparison

### Target and scope

The strongest scoped assembly lead is C09-v1, acidic-water [MoVI36O112(H2O)16]8−. Nominal source conditions include pH approximately 1.7 and 24.3 °C, with externally supplied molybdate and acid. Published seeding supports molecular assembly behavior; transmitted functional variants and autonomous regeneration remain unestablished.

The user's final material question compared preformed FeIII-bearing interfaces with iron-free silica. Completed acid/phase, transport/retention and protonation sensitivity studies were already in the record. They were not repeated for this publication.

### Quantum environment

The saved final runtime diagnostic used Python 3.12.3 and PySCF 2.14.0. H2 at 0.74 Å used RHF/STO-3G; fixed water used PBE0/def2-SVP, integration grid 3.

| Saved runtime output | Value |
| --- | ---: |
| H2 energy | −1.1167593073964255 Eh |
| Water energy | −76.27627012278069 Eh |
| Final two-process energy difference | 0 Eh for each fixed scenario |
| Mo def2-SVP/ECP construction | 28 core electrons; 14 explicit electrons; 31 atomic orbitals |
| Actual Mo electronic calculation | Not performed |

The first driver attempt failed after the H2 calculation on an API call. The error was repaired; two later drivers succeeded. Repeatability does not establish experimental accuracy or validated Mo36 interaction energies. Actual BLAS worker count was not recovered.

Only 36 qualified Mo positions were admitted for skeletal geometry. Hydrogen coordinates were missing and two O-coordinate anomalies remained unrepaired. A complete hydrated/protonation-resolved geometry was therefore not invented for a binding-energy calculation.

### Conditional electrical result

The new calculation applied an assigned planar Poisson–Boltzmann field to point and shell charge representations. The Mo skeletal circumsphere radius was 1.020344589 nm; assumed padding of 0.300 nm produced a model shell radius of 1.320344589 nm. Both representations place the charge centre at d = a + gap from the assigned diffuse-boundary plane, where a is the shell radius and the gap is the distance from that plane to the nearest point of the shell. The point value is the field at d; the shell value is the average of the field over the sphere surface. The published formula reproduces the saved rows only with these conventions, which the archived protocol and model state.

Four baths × four Fe fields × five silica fields × three gaps × two representations produced **480 main cases**. Formal charge −8 and assumed effective-charge sensitivities were considered. The cluster is at infinite dilution; actual concentrated-recipe ionic strength was not inferred.

The saved electrical-only log encounter ratio spans **−11.661949 to +15.174195**. Equal assigned fields give unity weights. Assigning silica a higher potential than Fe reverses the preference for the negative solute. Therefore no ranking is robust to the admitted unknown fields.

The sign of L equals the sign of the assigned Fe-minus-silica potential in all 480 rows, so every reversal is an input assumption: it requires silica to be assigned a higher potential than the FeIII interface. A post-publication review added literature context at abstract level only. The isoelectric point of silica is reported at pH 2 in HCl ([Kosmulski 1998](https://doi.org/10.1006/jcis.1998.5859)), and the point of zero charge of synthetic Fe oxides usually lies between pH 7 and 9 ([Schwertmann & Fechter 1982](https://www.cambridge.org/core/journals/clay-minerals/article/point-of-zero-charge-of-natural-and-synthetic-ferrihydrites-and-its-relation-to-adsorbed-silicate/6731E772B614A298097A94D944C9E24F)). At nominal pH 1.7 these values make silica-above-Fe the less expected ordering. In the 72 saved rows with silica at 0 mV and Fe at +25 to +100 mV, L is positive throughout (0.0007 to 11.66). This is context, not calibration: a point of zero charge gives the sign of surface charge, not the diffuse-layer potential, and the same source reports a far lower value, near pH 3, for one natural goethite and relates lower values to adsorbed silicate and other impurities. Neither support is a demonstrated preservation winner.

For assigned Fe +50 mV, silica 0 mV, z = −8 and gap = 0.5 nm:

| Added NaCl, M | L, point | L, shell |
| --- | ---: | ---: |
| 0.00 | 6.290 | 6.744 |
| 0.03 | 3.812 | 4.478 |
| 0.08 | 2.181 | 2.957 |
| 0.18 | 0.994 | 1.757 |

The displayed values are rounded transcription from the original report. The full exported output retains all saved numerical rows. Field/charge assumptions are not probability distributions or measurements.

Numerical controls passed, including a maximum 64/128-point quadrature discrepancy of 4.26 × 10−14 in L. These validate implementation consistency. They do not validate the chosen material parameters.

### Survival, precipitation and clogging

**Neither FeIII nor silica was shown to preserve intact Mo36 better.** The model omits specific surface chemistry, dissolution, hydrolysis, Mo speciation, nucleation, transport, precipitation and clogging. It is also a test-charge calculation: the assigned fields do not respond to the highly charged solute, dielectric boundaries and solute-induced field distortion are neglected, and each assigned potential is held fixed across the salt grid although real surfaces may regulate charge. The archived protocol calls the test-particle approximation “especially conditional” for Mo36, so the numerical values of L are conditional electrical weights; the point/shell difference is representation sensitivity, not a confidence interval. Electrical encounter cannot settle those processes. The earlier conditional screens are retained with their original limitations.

Total-Mo adsorption can coexist with intact-cluster loss or reconstruction. Timed intact inventories in liquid and recoverable solids, with a no-support arm and calibrated recovery, would allow a consequential material comparison. Endpoint recovery would still differ from evidence of uninterrupted molecular survival.

## Collective Cognitive Organism pilot

The completed pilot trained eight architectures under a frozen protocol with three seeds, giving 24 runs. All completed eight epochs; checkpoint selection used minimum validation loss. Held-out evaluation followed training. Each run used 192 optimizer updates (12,288 example presentations) with Adam at 0.003 and no hyperparameter search.

The ID test has 512 queries in 256 graph pairs, and each OOD set has 384 queries in 192 pairs. Every graph supplies one positive and one negative query, so chance is exactly 50%. ID intervals are the descriptive 95% crossed-bootstrap intervals of the saved report.

| Model | ID correctness | ID 95% interval | Longer-path OOD correctness |
| --- | ---: | ---: | ---: |
| CCO128 | 49.67% | 48.70–50.39 | 50.26% |
| Independent cells128 | 50.59% | 49.61–52.73 | 49.74% |
| Centralized recurrent | 50.00% | 48.83–51.30 | 50.17% |
| Recurrent GNN | 100.00% | 100.00–100.00 | 51.39% |

The registered CCO advantage is **unsupported within this protocol**. The adjusted paired CCO-minus-GNN interval was entirely below zero (−50.33 points; −51.69 to −49.35); because the GNN was correct on every ID query, this difference is CCO's own ID correctness minus 100 points. The adjusted intervals of the two comparisons that bear on communication include zero: CCO minus independent cells −0.91 points (−3.67 to 0.78) and CCO minus centralized recurrent −0.33 points (−2.28 to 1.56); the saved report states that they do not establish a useful communication effect. All three are 98.333% crossed-bootstrap intervals (Bonferroni adjustment for three comparisons). The exact deterministic oracle achieved 100%; it is not a learned competitor.

The GNN's 83.45% OOD macro conceals its 51.39% longer-path result. That result is a one-sided failure, not chance-like behavior: a post-publication recount of the archived predictions (`cco/artifacts/pilot/evaluation/predictions.jsonl`), pooled over the three seeds, found all 576 negative predictions correct (192 queries per seed) and only 16 of the 576 positive predictions correct, all 16 from seed 202. Training positives had path distance two or three; the longer-path positives have distance four.

The benchmark is a narrow procedural graph family. Model parameters, routing, state capacity and compute differ (GNN: 52,033 parameters and 2.73 million forward MACs; CCO128: 37,706 and 13.71 million); compute-matched superiority was not tested. Seven of the eight learned architectures stayed between 49.48% and 50.59% ID. On the selected CCO checkpoints, intact minus messages-off was −0.33 points and intact minus shuffled contents −0.13 points, against a preregistered 3-point drop; with the intact system at chance, these ablations could not show a benefit of communication and showed no cost. Near-chance damage stability does not demonstrate useful repair. No new training was run for publication.

## Digital emergence and engineered controls

Digital studies establish some bounded mechanisms under supplied laws and prepared conditions. Causal-memory interventions changed choices; in the acquired-memory study (`simulation/acquired-memory-01`), an equally timed program using original-page storage achieved the same choices without the recruitment fee. Engineered learning chains (`simulation/learning-chain-01`) executed inherited instructions over three descendant transfers in two predetermined histories.

Random-origin and lineage assays also retain failures, temporary effects and context dependence. A candidate's material persistence after functional failure was not promoted to lineage continuity. The archive preserves raw traces and controls so these distinctions can be inspected.

These studies do not demonstrate a chemical implementation, natural open-ended evolution, human-comparable cognition or a capacity advantage merely from extra storage.

## Parallel programmes

The separate Claude noncarbon-route record reports **465 Stage A–C runs**. P1–P3 findings remain conditional at the model level; REQ-18 was not met and G4 remained unresolved. Its final B262 status and user-stopped model-side G4 pursuit are distinct from E1092.

The biological-intelligence survey and speculative scenarios are separate again. They include literature thresholds and uncalibrated conditional ensembles, not a forecast of the probability or time of intelligence. The LLM collective-intelligence folder retains explicitly pending held-out tests; development/mock outputs are not final scientific evaluation.

## Integrated acceptance gates

| Gate | Final status | Missing evidence |
| --- | --- | --- |
| G0 compatible chemistry | UNRESOLVED | Intact target/contact dynamics and matched phase/medium closure |
| G1 driven maintenance | UNRESOLVED | Productive energy/material coupling exceeding actual losses |
| G2 functional heredity | UNRESOLVED | New functional variants, transmission and reproductive consequences |
| G3 adaptive evolution | UNRESOLVED | Unscripted heritable adaptation under ecological/resource constraints |
| G4 physical cognition | UNRESOLVED | Same-system sensing, writable memory, learning and action |
| G5 human-comparable capability | UNRESOLVED | Justified multidimensional held-out comparison |
| G6 evolutionary connection | UNRESOLVED | Supported accessible intermediates connecting the preceding stages |

Conventional carbon-life reference records may support gates within their own scope. That does not upgrade these integrated alternative-system gates.

## Why the goal stopped

E1090, E1091 and E1092 encountered the same missing-qualified-input/applicable-model dependency. The final independent audit found no materially new execution-ready calculation in the inspected state. The goal was marked blocked, not complete. This does not establish global literature/model exhaustion or impossibility of alternative life.

No scientific models, completed simulations or historical scientific validators were rerun for this publication. New publication checks verify packaging and presentation only.

## Glossary

**Autocatalysis:** a product assists further production; it does not automatically imply heredity.

**Functional heredity:** transmitted differences retain a causal function across offspring or new product, with suitable attribution controls.

**Conditional simulation:** a result that follows from specified laws, assumptions and inputs; empirical transfer requires additional justification.

**Intact recovery:** measured recovery of the target molecular species. Total elemental recovery is a different observation.

**OOD:** out of distribution; evaluation conditions differ from the training distribution.

**Unresolved:** the available evidence does not settle the registered question. It is not synonymous with impossible.

## Traceability

Authoritative records are the canonical candidate registry v2.44, E1092 checkpoint report, Mo36 interface-resume report dated 13 October 2026, CCO pilot v1 report dated 9 October, digital study-specific protocols, and separate B262 report. Their publication membership is recorded in the [research index](../data/research-index.csv) and release manifests. The [README source list](../README.md#selected-primary-sources) and claim-level ledgers connect literature claims to originals. Changes made after the tagged snapshot, with the source of each corrected statement, are listed in [CORRECTIONS.md](CORRECTIONS.md).
