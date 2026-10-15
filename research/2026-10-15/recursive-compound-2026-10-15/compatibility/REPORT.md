# Common-medium constraint and next recursive comparator

15 October 2026. **A concrete medium transfer fails for retained PMo12: 10 mM phosphomolybdic acid in 0.1 M sodium phosphate initially adjusted to pH 3 or 4 is reported as 0% PMo12 among assigned POM phosphorus signals, both initially and after 24 h at 37°C.** This is a source-condition exclusion, not proof that PMo12 cannot persist in any acidic medium, nor that the proposed Mo34WV compound is incompatible. No integrated life, functional heredity, or intelligence result exists here.

The new data are published triplicate NMR tables from Gumerova and Rompel, [Speciation atlas](https://doi.org/10.1126/sciadv.adi0814). The complete supplementary PDF was acquired through Europe PMC; selected rows are manually transcribed in [selected_rows.csv](selected_rows.csv), retaining replicates and reported means. Source PDF pages 144,157,160,67,83,87 and their rendered images permit inspection. Raw FIDs were not acquired or reprocessed: [PHAIDRA](https://doi.org/10.25365/phaidra.398) landing access failed and its attempted metadata endpoint returned an empty HTTP200 body. This access result is recorded, not counted as dataset acquisition.

## Quantitative result

All rows below use 10 mM initial POM. Phosphate is 0.1 M. NMR measurements were at 25°C, including the samples incubated for 24 h at 37°C. Percentages are the authors' reported integer means, not a fresh integration.

| Starting material and medium | Actual initial pH | Actual pH after incubation | Reported parent % initially → after incubation | Tables |
|---|---:|---:|---:|---|
| H3[α-PMo12O40], phosphate nominal pH3 |1.97±0.04|1.89±0.06|0 → 0|S17–S19|
| H3[α-PMo12O40], phosphate nominal pH4 |2.10±0.06|2.03±0.09|0 → 0|S17–S19|
| H3[α-PMo12O40], D2O |1.30±0.06|1.20±0.05|76±2 → 74±3|S17–S19|
| K6[α-P2W18O62], phosphate nominal pH3 |2.99±0.08|2.98±0.06|100±0 → 100±0|S8,S10,S11|
| K6[α-P2W18O62], phosphate nominal pH4 |4.00±0.06|3.97±0.06|100±0 → 100±0|S8,S10,S11|

In both selected phosphate PMo12 rows, the tabulated other species are 99% combined P2Mo5/PMo6 and 1% P2Mo18, initially and after incubation. All three parent replicates are zero; all three Dawson-parent replicates in the comparator rows are 100. These are reported absence/persistence at the tables' precision. No numerical analyte-specific detection/quantification limit was found in the inspected methods or these tables; **0% is not a demonstrated zero molecular population, and 100% is not a calibrated complete metal recovery**.

The after-incubation D2O parent replicates71,76,77 average74.67%, whereas the source prints74±3%; that rounding inconsistency is preserved, not corrected or used to infer a decay rate.

The denominator excludes free phosphate and includes assigned POM phosphorus peaks. It is neither an Mo/W atom balance nor automatically a molecular mole fraction across species with differing phosphorus stoichiometry. The PMo12 table headers inconsistently mention Na3[PMo12O40], while captions, methods and material purchase identify H3[α-PMo12O40]·9H2O; we retain that discrepancy and use the latter explicitly identified material. Both time and temperature change between measurements, preventing an inferred isothermal decay constant. The unbuffered comparator uses D2O and source-reported pH; no isotope pD correction is invented.

This supplies two new constraints: acidity alone does not license phosphate compatibility, and the final pH must be measured after adding each component. The nominal-pH3 PMo12 run shifts by −1.03 pH units initially, versus −0.01 for Dawson. This arithmetic is not a proton inventory or an explanation of the mechanism.

## Exactly what the atlas covered

The ten entries are PW12 ([α-PW12O40]3−); α-P2W18 and α/β-P2W18 ([P2W18O62]6−, separate starting materials); Preyssler P5W30; [(α-PW11O39Zr(μ-OH)(H2O))2]8−; [α-PMo12O40]3−; [α-P2Mo18O62]6−; [TeW6O24]6−; [α-SiW12O40]4−; and [V10O28]6−. **Neither Mo36 nor Mo34WV, WO3, silica or zirconia solids were tested as joint systems.** The Zr-containing POM is not a zirconia wall. The Si-containing POM is not a silica wall.

The actual Dawson salt was K6[α-P2W18O62]·19H2O; the mixed-isomer salt was (NH4)6[α/β-P2W18O62]·14H2O. This cannot be silently replaced with the lithium salt or an electrochemically reduced Dawson reservoir. The zirconium sandwich used diethylammonium counterions and therefore is not an entirely carbon-free preparation. The main text and SI also differ on the oxygen count in the Preyssler formula; that unrelated formula is not used in calculations here.

[atlas_scope.json](atlas_scope.json) preserves all buffer/pH entries: acetate 4,5,5.5; citrate 3,4,5,6,6.5; sodium phosphate 3–8 in integer steps; PBS7.4; tris7.5,8,8.5; glycine8.6; HEPES7,8; MES; MHB7.4; F-12 Ham7.4; unbuffered water. Standard buffer concentration was 0.1 M; glycine also 0.2 and0.5 M. Main Table1 lists MES pH6 whereas SI specifies5.5; this discrepancy remains visible. The SI explicitly warns phosphate does not buffer effectively over3.5–5.5. The design has27 medium conditions examined at two stages, not54 independent chemical recipes.

The standard POM concentration was10 mM. TeW6 and SiW12 were examined only at selected conditions using20 mM POM and doubled buffer concentration because of low-sensitivity 183W NMR; acquisition was about60 h. Their data must not be described as instantaneous snapshots equivalent to31P measurements. Every NMR spectrum was acquired at25°C; “after24h37°C” specifies incubation, not the NMR acquisition temperature.

## Recursive decision and joint intersection

1. **Reject the benign-phosphate transfer for a retained-PMo12 function at the tested concentrations and starting buffers.** The actual pH near2 does not rescue that inference. This is positive evidence of speciation change, although the zero has reporting limits.
2. **Advance oxidized potassium α-Dawson as a component-supported persistence comparator in the same starting phosphate matrix.** It has measured100% parent signal in these rows, but a different final pH. It has no demonstrated shared-mixture persistence with Mo36, no inherited redox state, and no demonstrated boundary regeneration. Do not equate replacing PMo12 with preserving PMo12's assembly or catalytic function.
3. **Keep a separate chloride-acid parent-Mo36 arm as the assembly baseline.** The [parent primary paper](https://doi.org/10.1073/pnas.1921536117), re-read locally, reports assembly nearpH1.7 at24.3°C with0.25M molybdate/0.047M acid figures (feed-versus-final wording remains unresolved). It did not test the atlas phosphate matrices or the target.
4. **WO3 remains a distinct electrode subsystem.** The [primary hydrated-WO3 study](https://doi.org/10.1039/D4SC00102H), re-read from retained XML, uses0.5M H2SO4 and H2-purged electrochemistry. No pH or potential conversion is inferred. Differences from chloride Mo36 and phosphate NMR are missing intersection evidence, not a proof of chemical incompatibility.
5. **Preformed unmodified silica and zirconia remain unverified boundaries.** The prior compartment dossier supplies no common-medium intact-cluster transport data. The companion [boundary report](../boundary/REPORT.md) separately checks supported-Mo transformations and total-Mo adsorption; neither observation proves parent/target retention. Boundary report quantities were not imported into the present calculations.

Thus the *experimentally verified full joint-condition intersection* is empty in the reviewed evidence: no shared mixture/run establishes all four functions. The *physical chemical intersection* is unknown. A spatially separated design is also only a hypothesis until measured transport and coupled function survive. No abstract model fills this gap.

## Next discriminating test specification

First compare parent Mo36 alone, parent plus PMo12, and parent plus oxidized potassium α-Dawson under the same measured acid/counterion/pH history, with isolated-POM controls. Include the atlas phosphate rows as speciation-change and persistence references, while keeping their distinct final pHs explicit. Verify analytical recovery and set detection limits before judging a candidate. A broad acid label is insufficient; record composition, concentrations, temperature and oxygen/redox history.

Then add unmodified SiO2 or ZrO2 contact in separate arms, followed by WO3 contact and only then controlled electrochemical operation. At each stage measure total Mo/W/V/P balance, molecular identity, parent seed-dependent assembly and solution/wall fractions at matched times. Measure species immediately and through the intended operating interval;0/1/24h would be a proposed sampling design, not a source-derived kinetic optimum. Use validated cluster-sensitive analysis for Mo36/target;31P alone cannot see a phosphorus-free target. Do not advance an unverified Mo34WV mixture merely because metal ratios match its nominal formula.

A stage fails if active parent identity/function cannot be recovered above validated assay limits and controls, even if elemental retention is high. Numeric functional pass thresholds require assay precision and use requirements and are not invented here. Retention alone cannot establish the reciprocal reconstruction required by the broader goal.

## Evidence and limits

[CHECKS.md](CHECKS.md) maps each criterion to exact artifacts and invocations. The check tests transcription arithmetic, conditional normalization and source hashes; it does not independently validate spectra or chemistry. Existing laboratories were not modified.

Skipped: raw-FID reprocessing, wet synthesis, kinetics/potential fitting and integrated operation. Risk: published signal fractions omit free phosphate and cannot establish intact-cluster mass recovery or target compatibility.
