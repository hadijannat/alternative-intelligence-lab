<p align="center">
  <img src="assets/hero.svg" alt="Alternative Intelligence Lab: an open investigation of chemistry, evolution and computation. The network illustration is conceptual." width="100%">
</p>

<p align="center">
  <a href="docs/FINAL_RESULTS.md"><img alt="Scientific outcome: goal unmet" src="https://img.shields.io/badge/scientific_outcome-goal_unmet-d8a64b?style=flat-square"></a>
  <a href="docs/EVIDENCE_GUIDE.md"><img alt="Evidence: scoped and traceable" src="https://img.shields.io/badge/evidence-scoped_%26_traceable-2aa99b?style=flat-square"></a>
  <a href="https://github.com/hadijannat/alternative-intelligence-lab/releases/tag/research-2026-10-13"><img alt="Research snapshot: 13 October 2026" src="https://img.shields.io/badge/snapshot-2026--10--13-6574a5?style=flat-square"></a>
</p>

<h1 align="center">Could another kind of matter become alive—and eventually think?</h1>

This repository publishes the final record of an exploratory research campaign: alternative chemistry, physical information processing, digital emergence, and collective computation. It brings literature evidence, saved numerical experiments, matched controls, negative results, and explicit limits into one inspectable archive.

**The central result: useful subsystems were identified and tested, but no autonomous non-carbon organism, integrated chemical lineage, or human-comparable emergent intelligence was demonstrated.** The latest Mo36 comparison cannot establish whether preformed FeIII or iron-free silica preserves the intact cluster better. The chemical investigation ended at a qualified-input dependency; its full goal remains unmet.

This is a research archive with computational results and literature analysis. It is not a report of new laboratory measurements or a peer-reviewed demonstration of alternative life.

**15 October continuation:** [Nine new laboratories](research/2026-10-15/README.md) add measured-chemistry models, RNA failure diagnostics, retention/inheritance assay simulations and a 1,000-record inorganic materials screen. Negative prediction results remain preserved. The proposed Mo/W/V composition remains unverified; no living or intelligent entity was demonstrated. The earlier tagged release remains unchanged.

<p align="center">
  <a href="#the-results-at-a-glance">Results</a> ·
  <a href="docs/FINAL_RESULTS.md">Scientific report</a> ·
  <a href="#read-at-your-own-depth">Reading paths</a> ·
  <a href="#download-the-research-record">Data &amp; archives</a> ·
  <a href="#selected-primary-sources">Sources</a>
</p>

## The results at a glance

| Research track | What the saved record establishes | What remains unresolved |
| :--- | :--- | :--- |
| **Chemical evidence map** | **329 preparations across 58 source-architecture groups**, registry v2.44 | These include organic controls, hybrids and engineered devices; they are not 58 demonstrated forms of life |
| **Mo36 / FeIII / silica** | **480** conditional electrostatic encounter cases; the preference reverses across allowed assigned fields | Intact-cluster survival, chemical adsorption, precipitation and clogging |
| **Quantum-chemistry runtime** | H2 and water electronic calculations converged; the final two-process repeat difference was zero | A qualified full Mo36 geometry and validated target binding or breakdown energies |
| **Collective Cognitive Organism pilot** | **24 trained runs**; CCO128 achieved **49.67%** ID correctness, recurrent GNN **100%** | The registered CCO advantage was unsupported; GNN longer-path OOD correctness fell to **51.39%** |
| **Digital learning and copying** | Supplied programs showed causal memory effects and three descendant transfers in two prepared histories | Natural origin, robust open-ended adaptation and physical chemical implementation |
| **Separate noncarbon-route programme** | **465 Stage A–C runs** with conditional model-level mechanisms | REQ-18 was not met; physical cognition gate G4 remained unresolved |

Counts are taken from the saved, dated reports and canonical registry. Source reviews, numerical calculations and experimental literature observations are different evidence classes and are never pooled into a single success rate. See the [final report](docs/FINAL_RESULTS.md) and [evidence guide](docs/EVIDENCE_GUIDE.md).

## From chemistry to cognition: the missing transitions

```mermaid
flowchart LR
    A["G0 · Compatible chemistry"] --> B["G1 · Driven maintenance"]
    B --> C["G2 · Functional heredity"]
    C --> D["G3 · Adaptive evolution"]
    D --> E["G4 · Physical cognition"]
    E --> F["G5 · Human-comparable capability"]
    F --> G["G6 · Supported evolutionary connection"]
    classDef open fill:#132337,stroke:#d8a64b,color:#ffffff,stroke-width:2px;
    class A,B,C,D,E,F,G open;
```

**All seven gates remain unresolved for the proposed integrated alternative system.** The arrows describe requirements, not an observed evolutionary sequence. A seed-dependent reaction, a durable material, or an engineered memory device can establish a subsystem without establishing a living lineage. Carbon life provides a reference; its known capabilities do not transfer to a proposed alternative by analogy.

## Mo36: a promising assembly lead with a decisive measurement gap

The strongest scoped inorganic assembly lead was acidic-water **[Mo₃₆O₁₁₂(H₂O)₁₆]⁸⁻**, with Mo(VI), externally supplied molybdate and acid. Published seed-dependent assembly supports molecular autocatalysis under particular conditions. It does not establish inherited functional variants or autonomous reproduction. [Assembly kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC7245103/), [templating intermediate](https://pubmed.ncbi.nlm.nih.gov/20044572/).

The final comparison used a narrower physical model: planar Poisson–Boltzmann electrostatics with **assigned** interface potentials, charges and geometry. Surface-complexation theory motivates this electrical contribution, while distinguishing it from chemical reactions at the interface. [3]

![Conditional Mo36 encounter comparison: increasing added salt reduces the electrical preference under assigned FeIII +50 mV and silica 0 mV fields. The plotted quantity is a log encounter weight, not survival.](assets/mo36-encounter-illustrative.svg)

For the illustrated assumptions, added salt reduces the electrical preference for encountering the FeIII-bearing interface. Across the full admitted sensitivity grid, however, the natural-log encounter ratio spans **−11.661949 to +15.174195**, and changing the assumed fields can reverse the ranking.

**Neither support is a demonstrated preservation winner.** Greater encounter frequency could improve retention or increase destructive contact. Capturing total molybdenum cannot by itself establish that intact Mo36 survived.

<details>
<summary><strong>Technical model, assumptions and numerical checks</strong></summary>

For a monovalent bath, the dimensionless diffuse-layer field was

```text
u(x) = 4 atanh[tanh(psi_d / (4 V_T)) exp(−kappa x)]
L = ln(c_Fe / c_Si) = −z [mean(u_Fe) − mean(u_Si)]
```

Here `exp(L)` is an electrical-only infinite-dilution statistical weight. It is not a measured adsorption constant or probability of intact recovery.

Distances are measured from the assigned diffuse-boundary plane, the plane of `psi_d`. Both charge representations share one centre distance `d = a + gap`, where `a` is the padded shell radius and the gap runs from that plane to the nearest point of the shell. The point model uses `u(d)`; the shell model uses the surface average `(1/2) ∫[−1,1] u(d + a·mu) dmu`. With these conventions, the formula and the values stored in the full output (the shell radius, the thermal voltage and the screening constant `kappa` of each bath) reproduce the saved rows; placing the point charge at `x = gap` instead gives 12.007 rather than 6.290 for the illustrated point value at zero added NaCl (FeIII +50 mV, silica 0 mV, 0.5 nm gap). The conventions are those of the archived `encounter/protocol.md` and `encounter/model.py` (release asset `research-0003.tar.gz`).

The illustrated CSV uses T = 297.45 K, nominal ideal HCl pH 1.7, assumed relative permittivity 78.5, FeIII +50 mV, silica 0 mV, charge −8, and a 0.5 nm gap. Point and uniformly charged-shell representations are compared. The shell radius includes an assumed 0.300 nm padding around the Mo skeletal radius.

The 480 main cases varied bath, two interface fields, distance and charge representation. Equal-field, sign, swap, far-field, weak-field and quadrature controls passed. Maximum 64/128-point shell quadrature discrepancy was **4.26 × 10−14** in L. Such checks establish numerical consistency, not empirical calibration.

In all 480 rows the sign of L equals the sign of the assigned Fe-minus-silica potential, so every reversal is an input assumption: it requires silica to be assigned a higher potential than the FeIII interface. Literature charge-reversal points added in post-publication review [9, 10] are discussed, with their limits, in the [final report](docs/FINAL_RESULTS.md#conditional-electrical-result).

The model omits surface reaction pathways, dissolution, real Mo speciation, nucleation, transport and clogging. It is also a test-charge calculation: the assigned interface fields do not respond to the −8 solute, and dielectric boundaries and solute-induced field distortion are neglected. Each assigned potential is held fixed across the salt grid as a deliberate sensitivity choice; real surfaces may regulate charge. The archived protocol calls the test-particle approximation “especially conditional” for the highly charged Mo36, and treats the point/shell comparison as representation sensitivity, not a confidence interval. Only 36 qualified Mo coordinates were available; incomplete/anomalous O/H information prevented justified full-cluster DFT. [4]

The [complete frozen 480-case result](data/mo36-encounter-full.json), [illustrated data](data/mo36-encounter-illustrative.csv), and [scientific limits](docs/FINAL_RESULTS.md#mo36-interface-comparison) are available separately.

</details>

## A useful negative result: collective cells did not win this task

The registered CCO pilot trained eight architectures with three seeds each. Its 128-cell model remained near chance on the held-out graph-reachability task and did not outperform its primary learned baselines. A conventional recurrent GNN solved the in-distribution task, but its performance deteriorated on unseen longer paths.

The ID test has 512 queries in 256 graph pairs, and each OOD set has 384 queries in 192 pairs. Every graph supplies one positive and one negative query, so chance is exactly 50%. Each run received 192 optimizer updates, with no hyperparameter search. The GNN's 51.39% on longer paths is a one-sided failure, not chance-like behavior: a post-publication recount of the archived predictions, pooled over the three seeds, found all 576 negative predictions correct (192 queries per seed) and only 16 of the 576 positive predictions correct, all 16 from one seed.

![CCO pilot correctness: CCO remained near chance; recurrent GNN solved the ID task but failed on longer-path OOD queries.](assets/cco-summary.svg)

This is a bounded negative result for the architecture, benchmark and training allowance. It does not refute collective intelligence generally. Compute, routing, recurrent-state capacity and parameters differed between some baselines (the GNN has 52,033 parameters against 37,706 for CCO128, but about one-fifth of the estimated forward compute of CCO128); compute-matched superiority was not tested. The complete pilot report, checkpoints, predictions and analysis are in the [CCO release archive](https://github.com/hadijannat/alternative-intelligence-lab/releases/tag/research-2026-10-13).

## What the gold and SAPO-34 papers actually contributed

| Paper | Supported contribution | Evidence boundary |
| :--- | :--- | :--- |
| **Duan et al., gold-autocatalyzed multielement nanoparticles** [5] | Feed-controlled material synthesis and separately powered catalytic testing | The inspected main text did not establish parent-linked functional heredity; supplementary information was not fully inspected |
| **Akhgar et al., SAPO-34 seed study** [6] | Seed/recipe-dependent product properties and MTO catalyst performance | A seed-dependent materials effect does not by itself establish a replicating, evolving functional lineage |

These are valuable materials results. Their contribution to the alternative-life question depends on additional tests of identity, transmission, new-product function and resource closure.

## Read at your own depth

| Reader | Start here | Then explore |
| :--- | :--- | :--- |
| **Curious reader** | The result table and chemistry-to-cognition diagram | [Plain-language evidence guide](docs/EVIDENCE_GUIDE.md) |
| **Student or educator** | [Final findings and glossary](docs/FINAL_RESULTS.md) | Compare a subsystem result with the evidence needed for heredity |
| **Chemist or physicist** | The Mo36 technical section and full output | Registry, interface protocols and archived sensitivity studies |
| **ML or simulation researcher** | The CCO negative result and digital controls | Frozen predictions, model code, configurations and historical reports |
| **Reviewer or reproducer** | [Provenance and reproducibility](docs/REPRODUCIBILITY.md) | Manifests, checksums, archive policy and exclusions |

## Download the research record

**Snapshot:** 13 October 2026. [Download the tagged research release](https://github.com/hadijannat/alternative-intelligence-lab/releases/tag/research-2026-10-13).

The repository holds the synthesis, figures and key machine-readable results. Release assets preserve the much larger authored scientific record: reports, numerical outputs, configurations, model code, negative findings and historical studies. Archives are split where needed; membership and checksums are indexed.

The release preserves **23,926 eligible files in 14 archive parts**: 3.04 GB of compressed archives (the 14 archive parts, without the manifest and index assets) and 6.91 GB of reconstructed files, in decimal gigabytes (10⁹ bytes). Counts include historical versions and repeated provenance copies. Select a study group with the [extraction helper](docs/ARCHIVE_POLICY.md#invocation) when you need a smaller subset.

- [Complete archive catalogue](data/archive-catalogue.json) — assets, sizes, checksums and coverage.
- [Searchable research-file index](data/research-index.csv) — result/report paths and asset membership.
- [Canonical candidate summary](data/candidates.csv) — all 329 preparation records, with source-architecture families and evidence status.
- [Initial claim-level evidence ledger](data/initial-evidence-ledger.json) — 34 claims, conditions and limitations from the earlier bounded review.
- [Publication policy and exclusions](docs/ARCHIVE_POLICY.md) — third-party acquisition payloads, private tool records, dependencies and path sanitization.

Historical reports retain their original dates and conclusions. Some describe an investigation as “active”; the [current status overlay](docs/FINAL_RESULTS.md) supersedes those statements. Publication does not rerun or independently replicate the original scientific experiments. Corrections made after the tagged snapshot are listed in [docs/CORRECTIONS.md](docs/CORRECTIONS.md).

## Inspect and reproduce

```sh
git clone https://github.com/hadijannat/alternative-intelligence-lab.git
cd alternative-intelligence-lab
python3 tools/verify_publication.py
```

The verifier checks this publication's links, key data counts and archive metadata. It does not execute scientific models. [Reproduction instructions](docs/REPRODUCIBILITY.md) explain how to recover the larger archives, interpret transformed hashes and locate each original environment and protocol.

To rebuild the displayed charts from the saved summary CSVs, install the documented plotting dependency and run `python3 tools/render_figures.py`. This redraws existing results; it does not retrain models or simulate new chemistry.

## What would change the conclusion?

For the FeIII/silica comparison, a consequential next dataset would measure initial and timed **intact Mo36** in both liquid and recoverable solid fractions, with matched arms, a no-support baseline, recovery calibration, uncertainty and material closure. Endpoint recovery and continuous molecular survival require different interpretations.

For the larger goal, those results would still need to connect to driven maintenance, functional inheritance, adaptive evolution, physical cognition and justified multidimensional capability tests in the same system. A new model would require qualified inputs and independent error/convergence controls before it could settle those transitions.

## Selected primary sources

1. [Mo-oxide molecular autocatalysis and seed-dependent assembly (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7245103/). See initial-ledger claims N10–N11 for conditions and phenomenological-rate limits.
2. [Mo36-centred templating intermediate in molybdenum-oxide assembly (2010)](https://pubmed.ncbi.nlm.nih.gov/20044572/). Assembly templating is the scoped claim.
3. [Li & Zarzycki (2022), *A computational pipeline to generate a synthetic dataset of metal ion sorption to oxides for AI/ML exploration*](https://doi.org/10.3389/fnuen.2022.977743). Theory context; synthetic data do not calibrate our two supports.
4. [Junkers et al. (2025), Mo36 coordinate-source preprint](https://doi.org/10.26434/chemrxiv-2025-tjp5z). The local coordinate qualification and its limitations are retained in the archive.
5. [Duan et al. (2025), *Gold-Autocatalyzed Synthesis of Multi-Element Nanoparticles*](https://doi.org/10.1002/adma.202501110).
6. [Akhgar, Towfighi & Hamidzadeh (2020), *Investigation of synthesis time and type of seed along with reduction of template consumption in the preparation of SAPO-34 catalyst and its performance in the MTO reaction*](https://doi.org/10.1039/D0RA05673A).
7. [Engineered XNA genetic information storage and recovery (2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3362463/). Carbon-containing polymers and supplied enzymes.
8. [XNA catalytic function and FANA fragment ligation (2014/2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4336857/). Catalysis and copying machinery do not establish autonomous organisms.
9. [Kosmulski (1998), *Positive Electrokinetic Charge of Silica in the Presence of Chlorides*](https://doi.org/10.1006/jcis.1998.5859). Added in post-publication review; abstract-level reading only. Context for the assigned silica potential, not a calibration.
10. [Schwertmann & Fechter (1982), *The point of zero charge of natural and synthetic ferrihydrites and its relation to adsorbed silicate*](https://www.cambridge.org/core/journals/clay-minerals/article/point-of-zero-charge-of-natural-and-synthetic-ferrihydrites-and-its-relation-to-adsorbed-silicate/6731E772B614A298097A94D944C9E24F). Added in post-publication review; abstract-level reading only. Not a calibration of the FeIII support.

Links identify the primary literature behind specific claims. An accessible citation is distinct from a newly verified full text; the archived ledgers record which originals, methods and supplements were actually inspected.

## Cite, contribute and reuse

Use [CITATION.cff](CITATION.cff) to cite this dated research archive; it has no assigned DOI. Maintainer: [MHadi Jannatabaadi](https://github.com/hadijannat). Research and publication preparation used AI assistance; scientific claims remain limited to the cited evidence and saved calculations. See [contribution requirements](CONTRIBUTING.md).

Original code is provided under [MIT](LICENSE). Original synthesis, figures and project-generated data are provided under [CC BY 4.0](LICENSE-DATA.md). Third-party works retain their own rights and licenses. Historical embedded notices take precedence for third-party components.
