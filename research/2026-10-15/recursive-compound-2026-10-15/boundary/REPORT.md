# Recursive boundary-complement evaluation

15 October 2026. **Five inorganic candidates evaluated; zero verified complements.** None of the inspected primary evidence jointly establishes selective transport, preservation of active Mo36 and boundary renewal in the same acidic/redox environment. The nominal `[MoVI34WVI VVO112(H2O)16]9−` remains unmade and structurally unverified. Parent-Mo36 measurements cannot establish the substituted compound's behavior.

This dossier owns only `recursive-compound-2026-10-15/boundary/`. It adds a sequential candidate ledger, retained primary sources, a measurement specification and bounded conservation checks. It makes no life, intelligence, novelty, synthesis or publication claim.

## Sequential evaluation

The order below is a measurement sequence, not an empirical ranking of survival. Each failed evidence gate led to the next concrete alternative. Full findings, limits and next alternatives are in [candidates.json](candidates.json); access limitations and primary references are in [sources.json](sources.json).

| Step | Complement and actual evidence | Disposition and next alternative |
|---|---|---|
| B1 | **Unmodified porous SiO2.** A primary catalyst study finds a silicomolybdate phase after preparation with pH-1 impregnating solution. This exposes a possible identity-changing interaction; it does not show destruction of aqueous Mo36 at pH 1.7. The closest supported-Mo36 result instead uses aminopropyl-functionalized SBA-15 and a nitrosyl derivative. | First simple measurement baseline, unverified. If identity or active retention fails, test B2. [Silica study](https://doi.org/10.1039/F19878302835); [supported cluster study](https://doi.org/10.1002/slct.201900756). |
| B2 | **Unfunctionalized monoclinic ZrO2.** A 2026 primary paper provides total-Mo uptake data in 3 M HNO3. At 50 and 700 mg/L feed, reported capacities are 7 and 51 mg/g; fitted Langmuir maximum is 66.70 mg/g. This is a different medium and unresolved molecular identity. | Unverified oxide alternative. An intact-cluster/seed-activity assay must precede any use as a renewing enclosure. If it sequesters inactive species or blocks feed, advance to B3. [Primary study](https://doi.org/10.1007/s11270-026-09246-1). |
| B3 | **Unfunctionalized TiO2.** Primary studies show pH-dependent molybdate uptake; calcined material reaches oxide-monolayer coverage near 6.6 wt% at pH 3.98. The characterized species are surface oxides after thermal treatment, not intact aqueous parent Mo36. | Surface-reactivity comparator only. No conclusion that calcination results predict ambient destruction. If reversible active retention fails, advance to B4. [1989 study](https://doi.org/10.1016/0021-9517(89)90273-X); [authors' full 1990 study](https://doi.org/10.1627/jpi1958.33.347). |
| B4 | **Preformed alpha-FeOOH/goethite.** The 2024 study uses 5 g/L solid, 10–100 µM Mo, 10–100 mM NaNO3, pH 3–10, 10–75 °C and 72 h equilibration. Mo uptake approaches complete removal near pH 3. The main text points to approximately 700 SI data points; those raw points were not downloaded. | Strong binding/sink comparator, unverified. No extrapolation to concentrated Mo36 near pH 1.7. Fresh garden precipitates are a different phase. If no active reversible retention survives, examine B5 as a separate boundary control. [Primary study](https://doi.org/10.1016/j.apgeochem.2024.105907). |
| B5 | **Inorganic-feed iron hydroxide/sulfide precipitation boundary**, with phase-resolved FeS control. Existing primary SI confirms an organic-free-feed electrical membrane example. Independent sulfide work shows elemental-Mo capture can accompany Mo(VI)-to-Mo(IV) conversion and mineral transformation. That study starts with tetrathiomolybdate and uses organic MES buffer at initial pH 5.9. | Deprioritize direct contact with the acidic parent cluster. Retain as a boundary-growth and destructive-capture control. If no shared window is measured, return to B1/B2 behind a measured separator; do not declare a successful recursive complement. [Garden study](https://doi.org/10.1002/anie.201501663); [sulfide capture study](https://doi.org/10.1021/acsearthspacechem.0c00176). |

The SBA-15 author institution verifies the organic-functionalized support. The indexed author-paper excerpt identifies `(NH4)12[Mo36(NO)4O108(H2O)16]`; the publisher full text was inaccessible. Neither its different formula nor six catalytic reuse runs establish parent-Mo36 assembly, carbon-free boundary function or renewal. Organic-essential membranes are excluded from positive evidence. Organic buffers in a failure-mechanism comparator remain explicitly disclosed.

The zirconia source switches Mo(VI) and Mo(IV) labels in its kinetics prose and mixes speciation discussions. We import its reported concentrations and removal quantities as source-reported data; no oxidation-state assignment or unique adsorption mechanism is inferred from its kinetic fit.

## What previous work actually allows

The three assigned prior dossiers were read, followed by source and code inspection of the earlier Mo36 interface and FeIII inventory work. File hashes are captured by the checker. The prior interface code assigns material potentials and an assumed radius padding; its electrostatic encounter ratio cannot identify adsorption, intact-cluster retention or transport. The FeIII code computes conditional hydrolysis/precipitation inventory with imposed conditions and geometric assumptions; it lacks Mo36 loss/assembly kinetics. Neither was rerun or promoted to empirical evidence.

The parent primary paper directly supplies seed-dependent formation near pH 1.7 and a separate strongly reduced destructive regime. Its Figure 1 specifies `[MoVI36O112(H2O)16]8−`; its abstract contains an inconsistent cluster label, so that abstract formula is not used. Feed/final concentration wording is also ambiguous. These issues are retained, not silently resolved. [Parent study](https://doi.org/10.1073/pnas.1921536117).

## Bounded quantitative result

Running `python3 recursive-compound-2026-10-15/boundary/checks.py` produces [checks.json](.omo/evidence/checks.json). This is inventory arithmetic and explicit atom/charge conservation; it is not a chemical simulation.

* The zirconia kinetic run's 100 mg/L × 0.010 L / 0.050 g gives a **20 mg/g absolute feed-inventory ceiling**. The 66.70 mg/g isotherm fit cannot be inserted as the uptake of that run. It comes from other feed concentrations, so this is not an allegation of a source inconsistency. The two reported isotherm points imply 70% and about 36.43% removal, respectively.
* The goethite loading domain supplies only **2–20 µmol Mo per gram of solid** from its tested feed. This is an inventory range, not a saturation capacity and not an intact-cluster count.
* Formal parent assembly `36 MoO4²− + 64 H+ → [Mo36O112(H2O)16]8− + 16 H2O` balances atoms and charge. Formal FeOOH dissolution consumes three protons per Fe; formal FeS dissolution to Fe²+ and H2S consumes two. Reverse precipitation releases those protons. Silicic-acid condensation to SiO2 and water also balances. These identities supply no rates or direction of reaction.
* With an inventory of 36 Mo atoms, both **zero intact Mo36** and **one intact Mo36** satisfy elemental balance. More generally, measured retained Mo gives only `0 ≤ n(intact Mo36) ≤ n(retained Mo)/36` until molecular identity is measured. For a verified Mo34WV target, separate Mo/W/V inventories would be necessary and still insufficient.

No permeability, active fraction, pore size, repair rate, redox window or mutation parameter was invented.

## Most informative next experiment

The next discriminating result is a **parent-Mo36, species-resolved contact-and-exchange comparison of unmodified SiO2 versus ZrO2**, with an unconfined parent control, before any W/V-substituted target is used. This is a measurement specification, not a preparation recipe.

Use a characterized parent reference and the same measured acid/counterion/temperature/redox history in every arm. Require separate liquid-inside, liquid-outside and wall-associated measurements of total Mo, molecular identity and seed-dependent formation activity, with dissolved support elements recorded. Pair a cluster-resolving method with a structural/spectroscopic reference and an activity assay; UV absorbance or elemental ICP alone cannot establish active Mo36. Validate wall extraction/recovery because a destructive extraction can manufacture apparent loss or preservation.

Estimate feed, product, proton and intact-cluster exchange independently using measured time series and material accounting. A reduction in solution Mo is not sufficient. A boundary candidate passes the initial retention gate only if recoverable, intact, active material remains distinguishable from adsorption of fragments, fresh replacement and wall-catalyzed reporter chemistry. Prespecify numerical thresholds from assay precision and controls before viewing outcomes; no such thresholds are justified by current data.

Only after this passes should a controlled wall-loss/renewal comparison be attempted, measuring restored selective transport and cluster activity together. Compare new-wall supply with a matched abiotic precipitation control and interrupt the claimed cluster-to-renewal coupling. Record wall material, dissolved losses, energy inputs, charge/proton inventory and active species over the same interval. A preformed support that merely persists does not satisfy renewal. New precipitate that seals every pore does not satisfy selective transport. A continuing external supply of fresh active cluster does not establish preservation or self-maintenance.

If both simple oxides fail, keep the negative result and proceed through B3–B5 only against their recorded falsifiers. A separated acidic domain is then an engineered hypothesis whose actual separator flux must be measured. There is no admitted direct joint-function dataset for fitting a life model or selecting a winner today.

## Evidence and limits

Primary files, extracted text, web access returns and failed routes are retained under [raw](raw). The checker verifies source-file hashes, five candidate dispositions, source links, explicit reaction balance and published-inventory arithmetic. [CHECKS.md](CHECKS.md) maps each deliverable criterion to its invocation, observable and artifact. Passing those checks establishes the dossier's accounting only. It does not establish the boundary function or the existence of Mo34WV.

Skipped: wet chemistry, DFT/MD, old-model reruns, new kinetic fitting and exhaustive structure/patent searching. Main risk: coupling can retain elemental Mo while destroying the active cluster; boundary renewal and selective transport remain unmeasured.
