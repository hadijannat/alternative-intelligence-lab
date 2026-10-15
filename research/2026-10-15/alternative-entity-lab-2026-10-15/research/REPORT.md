# Evidence for a coupled fueled-compartment route

Reviewed 15 October 2026. This is a targeted review of ten primary studies plus one associated public dataset. It is not a systematic review or a demonstration of life.

The most defensible next route is a **fueled compartment whose retained catalyst improves compartment persistence, followed by inheritance tests and only then an adaptive-control module**. This is a research inference from separate component demonstrations. No reviewed source establishes the proposed complete entity. The repository's integration problem should therefore become the central experiment: measure whether the same material system can keep itself operating, regenerate its useful contents, transmit functional differences, and use experience to improve later resource acquisition.

## Primary evidence and its limits

| Source | What the experiment supports | Consequence for the proposed route |
|---|---|---|
| [Soria-Carrera et al., Chem, DOI 10.1016/j.chempr.2025.102816](https://www.sciencedirect.com/science/article/pii/S2451929425004073) | A chemical autocatalyst and a fueled droplet benefit one another. | Best candidate integration spine; division with replicator inheritance still has to be established. |
| [Wenisch et al., Chem, DOI 10.1016/j.chempr.2025.102578](https://pure.mpg.de/rest/items/item_3680173/component/file_3680175/content) | Fueled coacervates form offspring speckles, transmit molecules, and can be rescued by refueling. | Makes a retention/offspring experiment concrete. It does not prove functional heredity of a replicator or open-ended evolution. |
| [Ameta et al., Nature Communications, DOI 10.1038/s41467-021-21000-1](https://www.nature.com/articles/s41467-021-21000-1) | RNA network connectivity changes reproduction, variation, and robustness. Self-assembly can erase inherited composition by pulling it toward substrate-determined states. | Use a common external environment, multiple transfers, and a passive-carryover control; a stable composition alone is insufficient. |
| [Ameta et al., Communications Chemistry, DOI 10.1038/s42004-023-00887-5](https://www.nature.com/articles/s42004-023-00887-5) | Multispecies RNA autocatalytic networks function in coacervates with transient protection of composition. | Measure molecular leakage and regeneration in the actual compartment. A bulk autocatalytic curve cannot supply either value. |
| [Salibi et al., Nature Communications, DOI 10.1038/s41467-023-36940-z](https://www.nature.com/articles/s41467-023-36940-z) | RNA propagates through seven serial-transfer generations with temperature-driven content exchange. | Environmental cycling and externally prepared substrate vesicles are supplied support. The authors explicitly state that the tested fragment system cannot evolve or confer a vesicle fitness advantage. |
| [Pinheiro et al., Science, DOI 10.1126/science.1217622](https://pubmed.ncbi.nlm.nih.gov/22517858/) | XNAs support heredity and selection using engineered polymerases. | XNA is an alternative information carrier; the demonstrated workflow depends on biological machinery and does not establish autonomous XNA replication. |
| [Lincoln and Joyce, Science, DOI 10.1126/science.1167856](https://pmc.ncbi.nlm.nih.gov/articles/PMC2652413/) | Cross-catalytic RNA ligation supports exponential replication and competition, with roughly hour-scale doubling in its tested conditions. | Compare replication time with compartment loss time. The RNA conditions and the fueled-droplet conditions cannot be combined by assigning their published rates to one simulation. |
| [Abil et al., Nature Communications, DOI 10.1038/s41467-024-53226-0](https://www.nature.com/articles/s41467-024-53226-0) | DNA self-replicators undergo selection in liposome systems with supplied translation machinery. One repeated campaign showed no improvement. | Useful conventional positive comparator; quantify externally supplied machinery and replicate failures. |
| [Chong et al., arXiv:2607.20810](https://arxiv.org/abs/2607.20810) and [data DOI 10.5281/zenodo.21453837](https://zenodo.org/records/21453837) | Measured photocurrent depends on prior light pulses. | Supports material memory as a separate component. The source is a July 2026 preprint; device bias, preprocessing, and readout remain external support. It supplies no evidence of self-maintenance or autonomous learning. |
| [Ivan, Szilagyi and Szathmary, PNAS, DOI 10.1073/pnas.2621400123](https://pubmed.ncbi.nlm.nih.gov/42766742/) | A theoretical/computational study, published September 2026, finds alternative stable autocatalytic compositions and selection-driven population switching under its defined rules. | Motivates compositional memory and partition tests. It does not establish a physical implementation, delayed-cue learning, or our simulator's behavior. |

The selection favors experimentally observed interfaces over isolated candidate chemistries. It does not rank every possible alternative substrate. Detailed evidence classification, access depth, dataset status, and DOI links are in [sources.json](sources.json).

The recent PNAS study's [author model repository](https://github.com/manukalexi/Bistability-of-compartmentalized-autocatalytic-systems/tree/9f8e22e44e97b6371e36008b14f0d6735c870dcf) was inspected at commit `9f8e22e44e97b6371e36008b14f0d6735c870dcf`. Its README describes two autocatalytic cycles, random distribution at a prescribed division threshold, and composition-dependent environmental rate effects. Those are supplied modeling assumptions. We inspected the abstract and repository description; the full publisher page redirected to a cookie page. Its code was neither run nor copied, and no license file was present in the inspected tree.

## Public numerical observations actually acquired

All six files are retained under [data](data). The three chemical CSVs are pinned to author-repository commit `5e39536facd68c2a133454b6a31390d53f19ad30`. The repository MIT license is retained verbatim; no separate data license was found. The physical archive is CC BY 4.0 according to the retained Zenodo API response, and its MD5 matches the repository metadata. [datasets_manifest.json](datasets_manifest.json) records each URL, UTC acquisition time, SHA256, byte count, units, role, and limitations. Total retained download size: 407,843 bytes.

### Chemical component observations

[Figure3C_Lifetime.csv](data/Figure3C_Lifetime.csv) contains two observations per condition. The mean author-reported lifetime is **22.7167 minutes for KR Click** (range 20.4833–24.9500) and **5.6667 minutes for matched KR Control** (5.4167–5.9167), a descriptive ratio of **4.0088**. These are the supplied CSV subset's values, not a restatement of the paper's rounded narrative. Two observations do not establish a precise population effect.

[Figure2G_Error_Rates.csv](data/Figure2G_Error_Rates.csv) gives mean wrong-product fractions of **0.216290 with seeded droplets** (`n=2`) and **0.433271 without seeded droplets** (`n=4`). The unseeded no-droplet mean is 0.592067 (`n=2`), a different comparison. This chemical selectivity metric must never be used as a per-base mutation rate.

[Figure3B_Data.csv](data/Figure3B_Data.csv) supplies 494 measured turbidity rows. Four sequential series are identifiable by time resets; the file has no explicit replicate identifier. Our operational half-peak crossing occurs at 8.350/7.774 minutes for Click and 4.600/4.923 minutes for Control. It is the first downward crossing of half the raw peak, without baseline subtraction, measured from acquisition start. It is **not** an exponential half-life or the author's lifetime definition. Full-interval AUC values are stored for inspection, but the observation windows differ and should not be compared as matched exposure integrals.

### Material-memory observations

[fig2.zip](data/fig2.zip) contains 19,744 baseline-corrected current rows over 400 light pulses, conditional mean traces, their standard deviations and sample counts, and the author's timing notes. True pulse period is 5.007 seconds. Current is in amperes; illumination levels are arbitrary relative units.

For identical present illumination, the difference between high-past and low-past mean current is:

| Present level | At pulse start | At 4 seconds | Fraction remaining | Pulse counts at interpolation brackets, low/high |
|---|---:|---:|---:|---:|
| 1.0 | 4.8642 nA | 1.1802 nA | 0.24262 | 46 / 51 |
| 0.5 | 5.2557 nA | 1.3448 nA | 0.25587 | 39 / 42 |

Each past group has its own time grid, so the 4-second values are linearly interpolated without extrapolation. Four seconds avoids sparsely populated tails; this is a descriptive, unregistered choice. The supplied slow-drift correction was not reconstructed. The rows are repeated pulses within the supplied sequence, not independent devices. These results identify a seconds-scale history effect under those measurement conditions; they do not establish adaptation or transport any parameters into chemical models.

No empirical curve was fitted to the entity simulator. [results.json](results.json) contains direct data summaries and method definitions only.

## What the integration laboratories should test

These are proposed acceptance questions, not experimental outcomes.

1. **Resource-supported persistence.** Account for supplied fuel, useful catalyst, waste, boundary material, and environmental exchange. Compare catalyst-containing compartments with an identical catalyst-disabled condition and equal external fuel input. Persistence should fail when required energy input is removed and recover only when sufficient material remains.
2. **Regeneration plus inheritance.** Track molecular identity and catalytic function through transfers or offspring formation. Compare with inactivated catalyst, fresh initialization, and passive dilution. A bookkeeping threshold is `G * r * s > 1`, where `G` is newly measured amplification, `r` is content retention after exchange, and `s` is the fraction passed to a tracked descendant. This is necessary accounting, not sufficient proof of life or evolution.
3. **Compatibility.** Measure regeneration and retention under one common solvent, temperature, ionic, and fuel regime. The reviewed minute-, hour-, and second-scale systems use different materials and imposed conditions. Until that interface is measured, they remain separate modules.
4. **Causal adaptation.** Present a cue with a delayed resource consequence, then reverse it. Compare adaptive coupling against fixed, random, memory-reset, and energy-matched controls. Measure success on unseen sequences and the cost of sensing, retaining information, and acting. A material response to history, or a trained external readout, is insufficient.
5. **Lineage-level selection.** Only after regeneration is established, test whether inherited functional differences predict descendant success in a common environment. Include no-selection and shuffled-parent controls. An externally coded mutation/fitness rule supplies those capabilities and cannot demonstrate their chemical emergence.

A small system passing the first two gates would be worthwhile progress. Adding an external controller could produce an engineered adaptive hybrid, but that controller's role must remain visible. The currently supported conclusion is **promising subsystem evidence; integrated living adaptive entity unestablished**.

## Reproduction and checks

From this directory, use the already installed Python:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 analyze_data.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 -m unittest -v test_analysis.py
```

The analysis validates retained input hashes before calculating results. Initial acquisition used `analyze_data.py --download`; it refuses to replace an existing acquisition manifest. All dependencies are Python standard library. Five tests cover known interpolation/crossing values, prohibition of extrapolation, duplicate time rejection, nonfinite values, and sample statistics. The first development run exposed blank padded tail cells in the physical data; parsing was corrected to omit missing observations and use the documented individual grids. The successful rerun and tests are the acceptance evidence.

Article page access sometimes encountered publisher redirects or bot checks; indexed primary text and institutional copies supplied the reviewed evidence. All numerical file downloads succeeded. Sequencing datasets linked by S03 and S08 were reviewed for availability but not downloaded or analyzed; their license was not separately verified.

No wet laboratory, autonomous organism, evolved intelligence, or shared chemical/physical calibration was demonstrated. The principal remaining risk is incompatible subsystem conditions; combining successful component papers does not resolve it.
