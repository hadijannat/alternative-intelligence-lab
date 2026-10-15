# Product release, rebinding, and the remaining RNA-model failures

This targeted review recommends a finite product-release comparator and a separate reversible full-length-binding comparator. Both are bounded hypotheses for the existing Salibi S13 measurements. No parameters were fitted here, no new compatible quantitative holdout was acquired, and no authors were contacted. The earlier failed models remain required comparators. See [sources.json](sources.json) for source locations, short exact passages, conditions, and access limits.

## What the primary sources establish

Salibi's S13 reaction drawings contain a reporter-containing ligation complex followed by release. S13/S14 sampling uses formamide/EDTA, heat denaturation, and denaturing PAGE. Therefore a ligated reporter in a noncovalent complex belongs in the ligated-product observer. Hyper-A and reporter precursor differ by G38A and a 5′ Cy5 label. S13 uses 42 °C, 20 mM MgCl2, 50 mM EPPS pH 8.5, and 900 mM sucrose. It does not supply product-binding, release, or bound-catalyst-inactivation constants. The prior source workbook is the published numerical data source, not a new holdout. [Salibi et al., 2023](https://doi.org/10.1038/s41467-023-36940-z)

Ferretti and Joyce measured E/E′ product-complex release at 0.21 min⁻¹ and dissociation equilibrium Kd=16 nM, giving their calculated association constant 1.3×10⁷ M⁻¹ min⁻¹. Conditions were 44 °C, 25 mM MgCl2, and 50 mM EPPS pH 8.5. Product release limited component multiple turnover, while competing substrate complexes limited overall amplification. Those substrate complexes had Kd approximately 0.1 µM and dissociation faster than 1 min⁻¹. RNA degradation was approximately 5% per hour. These are measurements or calculations for the older cross-replicating enzymes, not calibration of Salibi F1, Cy5-F1 binding, or functional lifetime. [Ferretti and Joyce, 2013](https://doi.org/10.1021/bi301646n)

Robertson and Joyce's F1 ligation measurement gives kcat=16.6±0.4 min⁻¹ and Km=7.1±0.5 µM under enzyme-excess single-turnover conditions with trace A and saturating B. F1's replication optimum was 46–50 °C; its 0.14 min⁻¹ growth measurement used 10 µM substrates at 48 °C. They discuss the older 0.21 min⁻¹ release result as a replication ceiling; this is not a new Salibi-condition release measurement. Temperature affects productive complexes, product dissociation, and competing substrate binding. Their reported degradation near 0.1% per minute likewise cannot identify the previous model's much faster fitted competence loss. [Robertson and Joyce, 2014](https://doi.org/10.1016/j.chembiol.2013.12.004)

Olea and Joyce explicitly draw self-replication proceeding through E·E and its dissociation into two copies. Their fluorescence method requires an evolved enzyme and a modified B leaving group. It supports the topology and warns that reporter chemistry can matter, but supplies neither the G38A/Cy5-A efficiency ratio nor an assay of Salibi full-length dimers catalysing further ligation while remaining bound. [Olea and Joyce, 2016](https://doi.org/10.3390/molecules21101310)

The sources distinguish a product complex containing competent full-length molecules from an additional catalytically active dimer species. No directly measured extra ligation activity of the bound Salibi F1·F1 complex was identified in this review. Model QFF as two potentially competent but currently unavailable strands; do not call it destroyed RNA, and do not give it an additional catalytic rate without evidence.

## Minimal finite-release topology

Let A=Hyper-A, R=Cy5-A, B=triphosphorylated fragment, F=free competent F1, P=free inactive reporter product, and D=full-length wildtype-equivalent material that has lost competence. QFF and QFP are noncovalent product complexes. The proposed reduction is:

```text
F + A + B -> QFF + PPi       vFA = ka F A s
QFF -> 2F                   release = krel QFF
F + R + B -> QFP + PPi       vFR = kf F R s
QFP -> F + P                release = krel QFP
s = B/(KB+B)
```

These are coarse event fluxes, not three-body elementary collision laws. The one shared release rate is a deliberate parameter economy, not a measured equality between FF and FP. The fitted ligation coefficients may change because the preceding model already absorbed unrepresented turnover into effective coefficients. Importing 0.21 min⁻¹ as a fixed measured S13 parameter would be unjustified.

Only the F-mediated components enter QFF/QFP. Existing precursor-assisted initiation `kh A² s²` and reporter formation `krh A R s²` have no F catalyst to sequester; keep their former net products as a declared partial-turnover approximation. Routing their entire flux into QFF/QFP would consume nonexistent F and corrupt the mechanistic meaning. Modeling precursor-bound products would be a separate hypothesis, not a bookkeeping correction.

For the six free states plus QFF/QFP, the RNA moiety totals are:

```text
wildtype-A: A + F + D + 2QFF + QFP
reporter-A: R + P + QFP
B:          B + F + D + P + 2QFF + 2QFP
PAGE:       100 (P+QFP)/(R+P+QFP)
competent full-length inventory: F + 2QFF + QFP
immediately available catalyst:  F
```

Finite residence supplies a clock distinct from F0×time. For F1-only data, `L=P+QFP`, `L'=kf(F0−QFP)R s`, and `QFP'=L'−krel QFP` when there is no competence loss. This can separate matched-exposure curves through the transient bound fraction; it does not guarantee the observed direction or magnitude. With positive release, remaining substrate, and surviving catalyst, finite release alone does not create a permanent conversion plateau. The 60-minute flattening is not an infinite-time measurement.

## Keep loss and binding assumptions explicit

Using `F→D` only for free F would automatically protect bound catalyst from loss. That is a distinct hypothesis. The recommended main closure applies the same competence-loss hazard per competent strand, while retaining the complex until ordinary release:

```text
F -> D                      kd F
QFF -> QFD                  2 kd QFF
QFD -> QDD                  kd QFD
QFP -> QDP                  kd QFP
QFD -> F + D                krel QFD
QDD -> 2D                   krel QDD
QDP -> D + P                krel QDP
```

The three additional inactive complex states require no extra fitted parameters. They prevent a hidden bound-state protection benefit and avoid assuming that loss instantly dissociates the duplex. This remains an unmeasured closure: losing competence is assumed to preserve binding and release. It is not a chemical hydrolysis model. A free-only loss scenario is a useful fixed sensitivity if registered before its scores are inspected.

For a no-regeneration control, the active-fragment ligation event can create QFD rather than QFF. The newly ligated strand retains its mass but never gains competence. Do not count two competent strands in such a control complex. With the loss extension, competent inventory is `F+2QFF+QFD+QFP`, whereas immediately available catalyst remains F.

## Reversible full-length binding as a separate comparator

Product complexes can also form by reassociation of completed strands. The older E/E′ pulse-chase and equilibrium experiments support that possibility, but do not establish FF or FP affinity in S13. A finite-release-only model deliberately omits this back reaction and tests residence after productive ligation. A separate rebinding model asks whether accumulating full-length RNA further sequesters catalyst.

If D is assumed to keep binding competence, allow its reassociation consistently. A shared-affinity closure over full-length pools F, D, and P contains six pair species: QFF, QFD, QDD, QFP, QDP, and QPP. QPP is inert but competes for P that otherwise could bind F. It adds one state and no parameter. Omitting QPP while giving all other pairs a common affinity is an additional asymmetry, not a consequence of reporter inactivity.

One consistent convention is homotypic association `0.5 kon X²`, heterotypic association `kon X Y`, and dissociation `krel QXY` for every pair. The factor is a rate-constant convention, not a new empirical fact. It makes total full-length association independent of relabeling a strand F→D. Alternatively use `kon X²` and `2 kon X Y`; report the convention before comparing constants. Shared affinities of F, D, and P remain unmeasured, especially because P carries a mutation and dye.

The expanded PAGE numerator is `P+QFP+QDP+2QPP`; its denominator adds free R. Wildtype inventory adds `2QFD+2QDD+QDP` to the first total above; reporter inventory adds `QDP+2QPP`; B inventory adds `2QFD+2QDD+2QDP+2QPP`. The competence inventory is unchanged from the preceding subsection. Pure binding never changes denaturing-PAGE yield.

Register all-free and initially equilibrated seeding as fixed preparation scenarios. S13 preparation on ice followed by Mg addition does not establish either state. For initial F-only seed total T, with the first association convention and K*=krel/kon, equilibrium solves `T=F+F²/K*`; use the positive, numerically stable root. Initial D=P=0, so other full-length pairs start empty. Do not reset to equilibrium after every transport step: finite-rate binding must retain its history.

## Consequences for validation and transport

The six-parameter independent-efficiency-plus-loss predecessor remains a failed baseline. It improved dose prediction but failed its registered whole-dose, late-time, and historical transport screens. A seven-parameter release comparator and separate shared-binding preparation scenarios are small enough to test without introducing per-dose efficiencies or a large folding network. A better reporter score does not establish the simulated free-F or competent-inventory trajectory.

Preserve every whole-dose and late-time failure, initial-state scenario, bound parameter, and unresolved fit. If the family is selected on a dose-validation score, use nested selection for its performance claim. All existing S13 values were inspected previously; these tests remain retrospective. A high-dose residual must not license choosing another topology after inspecting that same held-out score.

The primary sources do not measure transport or retention of FF/FP/inactive complexes under the FT protocol. Carry every species and its moieties through transfer and loss; label any common retention rule as an assumption. Membrane partitioning, leakage, freeze-thaw dissociation, and local concentrations cannot be repaired by relabeling a better bulk curve as calibrated transport chemistry.

No newly acquired numerical dataset matched S13 enzyme, reporter, temperature, buffer, and observer. Existing S12/S15/S18 or Robertson/Olea datasets can challenge different conditions, but cannot be silently pooled as the missing compatible holdout. A discriminating measurement would combine matched S13 reporter kinetics with denaturing measurement of unlabeled full-length formation and an independent post-release activity assay, plus a product-spike or pulse-chase test. Early sampling would distinguish first turnover from recycling; independently varying A/R/B would separate substrate competition from product binding.

## Verification and limits

`python3 rna-turnover-tests-2026-10-15/research/verify.py` checks source hashes/needles, the proposed stoichiometric inventory, competence loss, PAGE invariance under binding/release, and the analytic initial-state formula. These are source/bookkeeping checks, not experimental validation or fitting. The exact Salibi source text and diagram were inspected locally. Direct PMC page opens and attempted BioC downloads failed; the older primary articles were inspected through indexed primary full-text results. Short exact passages are retained in the ledger; failed download receipts are preserved in `raw/retrieval.json`.

No wet experiment, microscopic parameter identification, or exhaustive literature search was performed. The principal risk is that several unmeasured closures can improve reporter predictions while giving incompatible catalyst inventories.
