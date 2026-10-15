# Chemistry and condition audit

The strongest usable joint dataset is **C3 production and droplet turbidity under the same reported nominal Figure 1 formulation**. It supports a measured chemistry model of production while a compartment exists. It does not identify retained active catalyst or functional inheritance. The more functional KR3 refueling experiment offers direct survival/product-composition observations, but its exact seed and volume bookkeeping is inconsistent, and it never measures offspring inheritance.

## Provenance and scope

Primary article: Soria-Carrera, Kauling and Boekhoven, *Primitive genotype-phenotype coupling in fuel-dependent synthetic cells with an autocatalyst*, [DOI 10.1016/j.chempr.2025.102816](https://doi.org/10.1016/j.chempr.2025.102816). Online publication was November 5, 2025; the issue date is March 12, 2026. The article is CC BY 4.0.

The [author repository](https://github.com/hsoria/Primitive-Genotype-Phenotype-coupling/tree/5e39536facd68c2a133454b6a31390d53f19ad30) was acquired at commit `5e39536facd68c2a133454b6a31390d53f19ad30`. `manifest.json` records source URLs, byte lengths, SHA256 hashes and retrieval UTC for 81 files (5,763,075 bytes) and the 12,295,593-byte SI PDF. MIT is present at the repository root; no separate data license was identified. Downloaded notebooks were read as JSON, never executed. Large TIFF files were omitted.

`supplement.pdf` contains all supplemental methods, tables and captions; `supplement.txt` is `pdftotext -layout` output. The publisher HTML routes returned 403, the full Elsevier API returned 401, and the public supplementary CDN with `?download=true` succeeded. `article.txt` contains the first 14 pages of the combined article/SI PDF. The 31,666,696-byte combined PDF was processed in memory and not retained; `article_manifest.json` records its SHA256, source URL, extraction and text hash. Local retained source artifacts are below 30 MB.

## Usable condition match

Main article printed pages 2-4 and Figure 1, plus SI printed pages 10-11 (Tables S6-S7), report:

| Variable | Reported value |
|---|---|
| Solvent and buffer | Aqueous MES, reported 200 mM |
| Final pH / temperature | 4.0 / 25 C |
| Active compartment precursor | 16.0 mM Ac-F(RG)2D-OH |
| Polyanion | 50.0 mM PSS monomer units, 17.0 kDa polymer |
| Initial fuel | 50.0 mM EDC |
| Autocatalytic building block | 3.2 mM C-N3 (cysteic-acid derivative) |
| Tripropargylamine / copper / ascorbate | 0.84 / 1.0 / 2.0 mM |
| Added product seed | None in the Figure 1 kinetic experiment |
| Start event | EDC and sodium ascorbate added together |

`Figure1F_Click_droplets.csv` contains C3 concentrations in mM at 0, 0.16, 0.5, 1, 2, 4, 8 and 16 minutes, with two observations per time. `Figure1C_Click.csv` contains OD650 with named wells G6 and G2. These assays share nominal chemistry; no sample or replicate identifier links HPLC observations to a particular turbidity well. Treat the HPLC replicates as unpaired observations. Same-condition evidence is supported; same-aliquot or simultaneous molecule-level observation is not.

The raw turbidity files include 20 unlabeled constant-0.09 rows over times -4 through 0. They lack the well/sample metadata of the measured trace and are excluded from normalized observations. The original CSVs remain unaltered. Negative late-time blank-corrected OD values are retained. HPLC measurement noise and small nonclosure of species mass balance are retained rather than clipped.

The no-PSS condition is available for comparison. Its `Figure1F_Click_no_droplets.csv` T values duplicate `FigureS1.csv`, Type `With RG2`, exactly: these are not independent observations. Figure S1 also provides C-N3, mono- and bis-triazole intermediate concentrations.

The reported buffer concentration and recipe are not perfectly consistent. All stocks except EDC/ascorbate are described as 200 mM MES, while 4.5/50 uL aqueous additions would imply 182 mM final MES. Main text explicitly states 200 mM. Table S6 reports 0.8 mM alkyne while 4.2 uL of 10 mM in 50 uL gives 0.84 mM, as the main caption specifies. Its no-droplet row says 6.0 uL alkyne and consequently does not sum to the stated target volume. Models should use **reported nominal** conditions and retain these conflicts; exact independently verified formulations are unavailable.

## Compatibility ledger

| Measurements | What can be combined | What prevents stronger use |
|---|---|---|
| Figure 1F C3 + Figure 1C click OD650 | Same reported C-N3/PSS/fuel formulation; production overlaps compartment existence | No active C3 partition, retained fraction, exchange, or daughter function |
| Figure S1 no-PSS T + Figure 1F no-PSS T | Cross-check identical data | Duplicate observations; no independent replication |
| Figure S2 C3 seeding | Evidence that added C3 changes kinetics, seeds 0/0.2/0.5 mM, triplicates | Caption does not restate peptide, EDC or PSS; cannot assume Figure 1 droplet background |
| Figure S3 fuel/anhydride, Condition 0/1 | Internal EDC-cycle dataset; notebook maps 0=Control, 1=Click | PSS not specified in S3 caption; exclude from full droplet calibration |
| Figure S4 single-azide conversion | Same scaffold for each stated azide; useful for KR or C azide consumption | Azide consumption is not catalytic-product concentration; C3 and KR3 are chemically distinct |
| Figure S5/S7/S10 competition | Comparison with/without PSS at each stated azide pair | Additional 3.2 mM competing azide changes composition and product mixture |
| Figure 2F substrate/Cu partition | Static enrichment measurements under stated partition protocol | No ascorbate; CuII and unreacted substrates, not active CuI-complex or KR3 exchange |
| Figure 3H FRAP | Mobility of labeled fraction, in situ versus ex situ assembly | Internal 4 um spot recovery is not trans-boundary leakage or retained catalytic activity |
| Figure 4 EDC-only refueling | Persistence of phenotype under repeated 8/50-minute fuel cycles | No repeated addition of genotype building blocks; no mother-daughter tracking |
| Figure 5 refueling + products | Within one experiment family, 8-minute survival versus 50-minute dissolution associates with different final product composition | Exact seed/volume conflicts; relative HPLC only; no active KR3 counts or daughter inheritance |

## Retention and refueling constraints

SI printed pages 13-15: azide/copper partitioning omits ascorbate, waits 2 minutes, then centrifuges for 1 minute. The pellet-volume correction uses a separately estimated dense-phase fraction of 0.5%. This coefficient is a concentration ratio, not a kinetic retention constant. The volume method text says concentrations are doubled, while listed amounts in 100 uL yield the standard 16 mM peptide/50 mM PSS. No uncertainty interval for phase fraction is supplied.

SI printed pages 17-18: FRAP uses NBD-R labeling and a 4 um bleached spot. Source CSVs give in situ half-time 46.235 s and ex situ 15.469 s. These concern recovery within a droplet region. Equating them with whole-compartment escape would add an unsupported assumption. `source_models.json` records the published fitted quantities without turning them into transport parameters.

SI printed pages 15-16 and source CSV timestamps resolve the refueling intervals as **8 and 50 minutes**, not 90 minutes as one main-text passage says. Raw Figure5B is the 8-minute dataset and raw Figure5C the 50-minute dataset, reversed relative to the main caption wording. The raw `Refuel_time` field and start times 0/8/16 versus 0/50/100 are decisive. The survival phenotype is memory across fuel cycles of a population, not demonstrated inheritance across daughter compartments.

Figure 5/Table S12 exact concentration conflicts remain unresolved:

- Main text describes 510 uM seed. SI calls the seed stock 0.51 mM and adds 10 uL into a larger final mixture, so the final seed concentration cannot also be 0.51 mM if read literally.
- The listed first-cycle volumes sum to 58.3 uL. The prose says 45.5 uL before fuel, then adds 10 uL seed and 4.5 uL fuel/ascorbate, implying 60 uL. Main nominal concentrations often presuppose 50 uL. These alternatives cannot all hold.
- Subsequent additions are 1.0 uL 2.7 M EDC, 1.5 uL 10 mM tripropargylamine and 2.2 uL 50 mM ascorbate. Their concentrations depend on the uncertain first-cycle volume and growing total volume.
- Seed preparation includes MES containing 320 mM NaCl; the consistent final salt concentration is not recoverable from the contradictory volume descriptions.
- Product recovery through anion-exchange spin filtration is explicitly nonquantitative. Figure 5 product values are relative peak areas after subtraction of the control KR3 seed signal. They are not absolute newly generated catalyst concentrations.

## Source kinetic models and reproducibility limitations

The article uses a phenomenological sigmoid for C3 and exponential curves to guide the eye for azide conversion. The Figure 1 sigmoid code has parameters `a` and `b` only through `a-b`; fitting both independently is nonidentifiable. A new simulator should not treat this as evidence of mechanistic rate constants.

The supplied `Aspartic_Fitter.py` has a four-parameter EDC model. Figure S3 first invokes it with fixed `k0=0.01`, then overwrites the result with `fitter_simpler`, which is absent from the pinned repository, with `k0=0.001`. Cached output contains three parameters and half-lives of 28.58/23.03 s, while main text says approximately 50 s. The source's final fit cannot be reproduced merely by running the included script. The raw F and An observations remain usable independently; Ac is derived as 16-An and W equals 50-F, so treating all four as independent measurements would overcount evidence.

The S5/S7/S10 notebook reads an absent `Active_Kinetics.xlsx` and exports differently named files. The associated CSVs do exist and were acquired. No notebook execution was needed or claimed.

## What a coupled simulation may test

Measured C3 formation and same-condition turbidity can ground the production and compartment-presence modules. Conservation equations may then ask what *unknown* retention, active fraction, transfer, dilution and division parameters would be required for inherited function. Keeping these unknowns free permits equal-observation scenarios with opposite inheritance outcomes. Such scenarios reveal what the current measurements cannot identify.

Neither substrate Kp, FRAP time, OD650, nor the composition-weighted error statistic identifies functional inheritance. The main article explicitly states that genotype was not transmitted to offspring in these experiments. Division with a replicator is future/ongoing work in the article, with no numerical daughter data in this pinned source.

Required new joint measurements are active catalyst per mother and daughter, catalytic activity after transfer, transfer-associated substrate/fuel carryover, whole-droplet catalyst exchange under active click conditions, and renewed daughter catalyst production after sufficient dilution to eliminate simple carryover. A positive fitted curve alone does not supply those measurements.

## Files and verification

- `conditions.json`: machine-readable nominal formulation, condition groups, conflicts and unknowns.
- `tables/observations.csv`: 7,104 source-preserving long-form observations with original source file and CSV line number; concentrations, conversions, turbidity, partitioning, FRAP and endpoints remain distinct measurement classes.
- `tables/counts.json`: per-condition row counts.
- `source_models.json`: original model equations and published fit outputs, with identifiability warnings.
- `acquire_sources.py`, `acquire_article_text.py`, `normalize_sources.py`: reproducible acquisition/extraction; normalization validates all retained source hashes before writing tables.

No model was fitted and no source notebook was executed in this source-audit task. No physical experiment, active leakage measurement or functional-inheritance test was performed.
