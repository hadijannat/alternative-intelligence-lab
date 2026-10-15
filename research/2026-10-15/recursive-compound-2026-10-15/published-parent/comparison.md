# Published parent source audit

The downloaded reference is compositionally Mo36O128H32 with charge −8, but its recorded hydrogen-contact arrangement differs materially from P0_A. This is an external computational reference, not experimental solution identity or held-out target validation. No new SCF or geometry modification was performed.

## Source and geometry scope

The actual shell-wrapped ADF input specifies PBE, TZP, large frozen core, scalar ZORA, analytical frequencies, NumericalQuality Good and `ScanFreq -1000 0`. Its solvation block requests water, Delley surface, conjugate-gradient charged treatment and C-Mat POT. Parsed output declares ADF 2019, SINGLE POINT, PBEc/PBEx, TZP, dielectric 78.39000 and solvent radius 1.93000 Å. These are not the PySCF def2-SVP/Mo-ECP/SWIG C-PCM settings merely because both use PBE.

Both geometry CML and the sole molecule in output CML contain 196 atoms: 36 Mo, 128 O and 32 H. The output molecule occurs under `cc:initialization`, not `cc:finalization`. Geometry CML matches those initialization coordinates exactly in the same ID/element order. The maximum difference from the more precise input coordinates is 0.0000733723 coordinate units, consistent with output rounding. No independently declared final or optimized molecular geometry appears in the parsed output. The SINGLE POINT label cannot establish how the submitted coordinates were previously prepared.

CML coordinate attributes omit explicit units. Contact calculations use the Å interpretation of these supplied molecular coordinates, consistent with the input and output solvent-radius units; no coordinate conversion or repair was applied.

A finalization module and properties exist, but no explicit SCF convergence flag was found by dictionary-key inspection. This is not proof of failed convergence or proof of normal executable termination. The final `cc:total` value −1433.3726 eV occurs in the ADF energy-summary/decomposition context; it is not a directly comparable PySCF absolute total energy. No cross-code energy subtraction was made.

## Hydrogen contact comparison

The nearest-O distance threshold was fixed at 1.2 Å before calculation. Each H is assigned only to its nearest O within that threshold. Labels below describe geometry, not verified chemical bonds or formal protonation.

| Descriptor | Published geometry | P0_A |
|---|---:|---:|
| O with two assigned H, aqua-like | 4 | 16 |
| O with one assigned H, hydroxo-like | 24 | 0 |
| O with no assigned H | 100 | 112 |
| H outside the threshold | 0 | 0 |
| Nearest H–O range, Å | 0.9774008–1.0140288 | 0.9800000–0.9800000 |
| Minimum H–Mo distance, Å | 2.4653784 | 2.4997402 |

The higher-precision published input gives the same 4/24 contact classification. Every H’s nearest/next-nearest O distance, nearest Mo distance and every O’s assigned-H count are retained in `analysis.json`. This difference precludes treating the two explicit-H arrangements as interchangeable without a separately justified scientific comparison.

An element-pair-constrained comparison of sorted heavy-atom distance distributions avoids inventing a site mapping. RMS differences are 0.519224 Å for O–O (8128 pairs), 0.544825 Å for Mo–O (4608 pairs) and 0.594597 Å for Mo–Mo (630 pairs). These are permutation/rigid-motion-invariant distribution differences, not mapped atomic displacement RMSDs. No unique site correspondence or heavy-atom displacement is claimed.

## Frequencies and ScanFreq scope

All frequency-related arrays were collected with XML context and units. Two `cc:frequency` arrays each contain 582 entries (3N−6): one rounded displacement-associated array without an explicit unit attribute and one intensity-associated array labelled `nonsi:cm-1`. The latter has 49 negative signed entries, 46 below −20 cm⁻¹, and minimum −189.805048 cm⁻¹. This is an audit observation, not an assertion of 49 final imaginary modes.

One explicit ScanFreq old/new block contains 13 negative old values replaced by positive values from 86.877 to 156.516 cm⁻¹. Each old value matches one original full-array entry within 0.000501 cm⁻¹, accommodating rounding to 0.001 cm⁻¹. No ambiguous matches occurred. Applying only these explicit replacements yields conditional accounting of 36 remaining negative entries, 34 below −20 cm⁻¹, with minimum −189.805048 cm⁻¹. The JSON preserves original arrays, all 13 matches and the conditional array. This reconstructed accounting is not an explicitly declared final corrected Hessian spectrum.

Both thermochemistry contexts are preserved. The earlier context has symmetry number 2 and total entropy 818.691 cal mol⁻¹ K⁻¹; the finalization context has symmetry number 1 and total entropy 984.244 cal mol⁻¹ K⁻¹. Their total internal energies are respectively 581.748 and 611.459 kcal mol⁻¹. These changes indicate distinct thermochemical records; they do not independently explain how every remaining mode was handled. Negative signed wavenumbers conventionally encode imaginary modes, but units alone do not establish that sign convention or the final correction scope. A minimum/nonminimum verdict remains unresolved from this audit.

## Reproduction and evidence

From workspace root:

```sh
python3 -B recursive-compound-2026-10-15/published-parent/test_analysis.py
python3 -B recursive-compound-2026-10-15/published-parent/analysis.py
```

`evidence/tests.txt` captures six passing guard scenarios: malformed XML, mismatched atom count, nonfinite number, incorrect array size, incomplete frequency scope and missing ScanFreq pair. `evidence/analysis.stdout.txt` captures the actual audit observations; `analysis.json` holds numeric details, source hashes, XML context paths and interpretation limits. Source findings are observations, not threshold-based acceptance tests. Files were read locally without network or chemistry calculations. No source was repaired and no physical admission or held-out validation is claimed.
