# Sequential heredity-complement checks — 15 October 2026

**The goal remains unmet. Four candidates were checked; zero joint additions are verified.** The base `[MoVI34WVI VVO112(H2O)16]9−` has unresolved molecular identity. These are source and accounting checks, not synthesis, new laboratory observations, or proof that inorganic life is impossible. [candidates.json](candidates.json) preserves each candidate's function, check, conditions, disposition and next-candidate decision.

## Materially new results

**CHA supplies a measured functional change but fails an inference of faithful phenotype copying.** Freshly reacquired primary XML yields eight Table 1 rows in [cha-texture.csv](cha-texture.csv). The original K-form seeds have approximately 0.001 cm³/g accessible micropore volume; the 24-hour product has 0.24 cm³/g. For recovered founder mass `F ≤ M`, an *unchanged* founder capacity contributes at most `F×0.001/(M×0.24) ≤ 1/240`, or **0.4167%**, of final accessible capacity. Therefore at least **99.5833%** requires new or altered accessibility in this restricted additive accounting model. This excludes unchanged-founder property persistence as the whole explanation at the reported point values. It does **not** attribute the capacity to newly deposited atoms: ion exchange can change the old seed's accessibility. The seed value is approximate; no calibrated uncertainty bound exists, so the calculation is not a statistical exclusion. The measured function is N₂-accessible porosity after drying/heating, not autonomous catalytic maintenance. [Primary paper](https://doi.org/10.1039/C9RA10825D).

The same study reuses products as seeds twice while Si/Al and Na content rise and K content falls. Topology retention therefore does not establish faithful transmission of the cation-dependent adsorption phenotype. The source's single-growth adsorption time course and its serial topology/composition panel are distinct datasets; combining them into serial functional inheritance would invent an endpoint. This is the most informative candidate in this bounded check because it offers both growth and an actual material-function measurement, while leaving the attribution question explicit.

**PMo12 has a newly identified methods inconsistency that blocks an exact shared-medium claim.** Main-text p10703 describes equal-volume mixing with 4 M HClO₄; SI §4-2 instead describes 0.06 M HCl. Their nominal post-mixing concentrations are 2 M and 0.03 M, a **66⅔-fold difference**, plus a different acid anion. Main molybdate stock is 1.4 M with phosphate; SI says 0.7 M and omits phosphate in that paragraph. These may reflect reporting errors or different preparations; neither explanation was verified. The calculation compares nominal mixing inputs, not proton activity or solution pH. Exact source locations and both descriptions are retained in the ledger. [Primary paper and SI](https://doi.org/10.1073/pnas.1921536117).

## Sequential decisions

| Step | Complement | Actual discriminator | Result and next step |
|---|---|---|---|
| H1 | Mo36/Mo6 assembly system | Compare measured seeding with the proposed molecular feedback mechanism | Mo36 is a legitimate assembly reference. SI pS32 treats Mo36→Mo6 templating as an experimentally difficult assumption explored in a model. No measured inherited functional variants; move to H2. |
| H2 | `[PMo12O40]3−` | Check exact preparation and whether increased formation is inherited useful activity | Recipe inconsistency above; no common-medium verification or parent-specific functional transfer. Carbon-containing PMo12⊂Mo124Ce4 is excluded. Move to H3. |
| H3 | NaClO3 | Recheck mass-based handedness and founder rival | 11/13 crops contain opposite-handed mass. Founder removal alone leaves microscopic carryover unbounded; no inherited catalytic trait. Move to H4. |
| H4 | Na/K CHA aluminosilicate | Check serial growth separately from quantitative adsorption capacity | New/altered capacity is supported; faithful transmission into new material is not. Stop this four-candidate sequence without manufacturing a next positive result. |

For H1/H2, the source's seeded product curves measure amplification, while the specific Mo6 feedback and hereditary functional alternatives require separate evidence. Relevant locations are main pp10701–10704 and SI §§3–4, pS32. No model rates are imported into the proposed mixed-metal cluster.

For H3, the [2021 primary source](https://doi.org/10.1016/j.ultsonch.2021.105763) and retained trial table are reused, not relabelled as untouched validation. The [existing founder analysis](../../discovery-loop/experiments/chlorate-founder-mass-bound-v1/report.md) derives `F=M(2s−1)` for matching founders plus exactly racemic new mass. Its required thresholds are 3.0253512–10.52424 g, and the requisite independent founder upper bound remains absent. Our new opposite-mass total is descriptive; it is neither a copying error rate nor evidence for selectable function. Printed mean inconsistencies remain unresolved.

## Compatibility and the remaining gates

The CHA growth feed is `1SiO2:0.05Al2O3:0.3Na2O:0.1K2O:100H2O`, with seeds at 10 wt% **of silica**, 170°C growth and 24-hour serial rounds. Its adsorption readout uses 77 K after 300°C vacuum treatment. It is not an in-operando acid-water maintenance assay. Mo36's primary experiment suppresses formation at pH >4.5 after reducing HCl stock to 0.001 M; the standard reference is 24.3°C. This is measured condition dependence and absence of a demonstrated overlap, not a theorem excluding all engineered coupling. The CHA article also shows MER replacing CHA at particular more alkaline feeds. No Mo34WV/CHA mixture was tested.

Useful selectable variation would require at least two parent-associated functional states, measured on new material after quantitatively bounding founders, persisting through shared-environment transfers and producing differential outcomes. Neither crystal handedness, higher yield, seed retention, nor a reporter signal alone meets that test. A single kinetic curve cannot supply the joint life-lineage evidence. Reproduction is not asserted to be necessary for every form of learning; here it is a requirement of the proposed integrated living-lineage claim. Cognitive capability remains a separate untested endpoint.

## Evidence and reproducibility

Invocation: `python3 recursive-compound-2026-10-15/heredity/check.py`.

| Scenario | Binary observable | Captured artifact |
|---|---|---|
| Source table extraction | Eight rows, exact endpoint and 6-hour row assertions pass | [checks.json](.omo/evidence/checks.json), [CSV](cha-texture.csv) |
| Restricted capacity bound | Actual calculation tested at founder fractions 0, 0.1, 0.5 and 1; two capacity controls; 11 invalid value/unit cases rejected; exact bound remains 1/240 | [checks.json](.omo/evidence/checks.json) |
| Chlorate reuse | 13 valid rows; 11 positive opposite-mass crops | [run.log](.omo/evidence/run.log) |
| PMo12 discrepancy arithmetic | 2/0.03 = 200/3; no identity of media asserted | [checks.json](.omo/evidence/checks.json) |
| Candidate integrity | Four distinct candidates; every joint-addition flag false; required fields and artifacts present | [ledger-validation.json](.omo/evidence/ledger-validation.json) |

[sources.json](sources.json) pins the inspected source bytes. [acquisition.json](raw/acquisition.json) retains the failed RSC figure download and successful EuropePMC XML acquisition. Web-tool RSC full text returned 403 and PMC rendered a browser challenge; the EuropePMC API supplied the complete article XML. No numbers were invented from the inaccessible Fig13 image. Prior reports were used as navigation, then the decisive primary text/table was checked directly. No active ULW attempt was found; evidence stays within this assigned folder's `.omo/evidence/`.

Validation correction: the first version included two literal Fraction identities that did not exercise a calculation function. Those assertions have been replaced by calls to the actual founder-contribution calculation, with six valid scenarios and eleven rejection scenarios. The reported scientific bound is unchanged. Unit labels are checked; incorrect labelling of physical measurements cannot be detected by these tests.

Skipped: wet work, rates, new compound synthesis, functional-lineage measurements and publication. Main risk: interpreting new adsorption capacity or serial topology as inherited activity in newly formed material; the cited experiments do not settle that question.
