# Patterned KTiOPO4: new-layer optical function, incomplete functional heredity

**Periodically poled KTiOPO4 is a documented functional-state carrier worth retaining as a component candidate.** Its grown layer reproduces a seed's domain grating and produces spatially measured second-harmonic light. This advances the evidence beyond total retained metal or an attached structure without a function assay. It does not establish serial functional descendants, alternative inherited functional variants, active repair or a living/intelligent system. Exact Mo34WV identity remains unverified; no verified integrated complement is added.

## Primary observation and its scope

The new primary package is Peña et al., [*Template-growth of periodically domain-structured KTiOPO4*, Optical Materials Express 1,185–191 (2011)](https://doi.org/10.1364/OME.1.000185), acquired as the public [HAL author manuscript](https://hal.science/hal-00909130/file/PPKTP_OMEx_Revised_280411.pdf). Its [2012 growth companion](https://doi.org/10.1016/j.jcrysgro.2011.11.081) refers back to this optical experiment and is not an independent replication. Native PDFs, rights/identity metadata, checksums, complete extracted text and inspected figure pixels are in `sources/`. [Source audit](<SOURCE_AUDIT.md>).

The authors first program a 38.86µm domain grating electrically into the seed. They grow KTP from an inorganic KTP/KPO3/KF flux, beginning at 1005.5K with a 0.05K/h cooling ramp. The operating temperature is below both the stated Curie range and polar-face roughening threshold, protecting the seed pattern and growth morphology. The resulting layer remains attached. Named crystal and flux compositions contain no carbon; the fabrication, lithographic processing and complete apparatus carbon inventory are not established.

The important function assay is spatial: the laser propagates along the crystallographic a axis, parallel to the seed/layer interface. Figure5 compares a beam centered 275µm inside the seed with a beam centered 225µm inside the newly grown layer. The fundamental beam's 1/e² diameter is 70µm. Both locations generate quasi-phase-matched second-harmonic light. Reported peak wavelengths are 2127.1±0.5nm and 2126.9±0.5nm, respectively. This is an actual optical assay in new material, not merely a calculation from its composition or an assumed utility of handedness.

The new-layer peak is approximately 28% lower. Both spectra have a 12.7nm·cm bandwidth product, compared with a calculated ideal 9.4nm·cm. Clean growth is established to about 225µm; cracks and inclusions occur farther into the layers. The headline 800µm growth extent is not 800µm of demonstrated defect-free optical function. No measured cross-talk bound, isolated daughter assay, serial regrowth or independent raw numeric dataset is supplied.

## Executed optical checks

[The protocol](<PROTOCOL.md>) discloses that these source outcomes were known before calculations. No parameter was fitted and no held-out validation is claimed. [The executable](<check_optics.py>) performs source-consistency and synthetic observation-symmetry checks; [results](<results/optics.json>) preserve source/protocol/script hashes, every sensitivity scenario and the missing experimental bounds as null.

For an ideal Gaussian pump, the radius is **35µm**, not 70µm. At a 225µm separation from the seed half-plane:

| Conditional observable | Calculated fraction |
|---|---:|
| Pump power in the seed half-plane |3.92×10^-38|
| Integrated local squared-intensity SHG proxy |3.54×10^-74|
| Coherent on-axis source-power proxy |1.54×10^-75|

The last two rows describe different collection/coherence assumptions; neither is a universal bound on a real detector. The source's layer/seed peak ratio is about 0.72. Thus nominal direct beam overlap is a poor explanation for a founder-only signal under those idealized assumptions. Even increasing the assumed beam radius to 140µm leaves the local squared-intensity proxy at 2.74×10^-6. These larger radii are fixed hypothetical sensitivity scenarios, not measured beam uncertainty.

This calculation strengthens the spatial interpretation but **does not manufacture an independent founder-function bound**. The proxies assume the specified transverse profile throughout the interaction and idealized collection; actual waist evolution is not supplied. Scattering, beam walk, aberrations, non-Gaussian wings and collection cross-talk were not quantitatively bounded by the paper. Under an additional identical-mode conversion assumption, explaining 0.72 relative SHG by redirected seed illumination would require about 0.849 of the reference pump in that seed mode. Different focusing or conversion geometry invalidates that simple square-root relation. No measured stray-light limit or absolute conversion efficiency is inferred.

The two quoted wavelength intervals overlap; their centers differ by 0.2nm. The ±0.5nm definition is not supplied, so this is not a significance test. Multiplying the plotted 19.5nm FWHM by the 0.65cm path gives 12.675nm·cm, consistent with the reported 12.7 after rounding. The measured bandwidth product is **1.351 times** the ideal value. Similar seed/layer spectra coexist with nonideal optical quality; neither result is erased.

## An assumption that erases a candidate memory bit

For the usual undepleted coherent observation, amplitude is proportional to `integral d33(s) exp(i*DeltaK*s) ds`, and the measured intensity is its squared magnitude. Reversing **every** domain sign changes amplitude sign but leaves intensity unchanged. The exact piecewise integral and a synthetic 20-period scan confirm zero intensity difference between these globally reversed gratings.

![Conditional optical geometry and synthetic sign symmetry](<results/optics.png>)

This readout cannot identify absolute global polarization from an intensity spectrum. It does not erase all pattern information: periodic and uniform structures have different phase-matching spectra, and grating period or relative domain arrangement can remain observable. A phase-sensitive measurement or two distinguishable pattern variants is needed before calling this a signed hereditary-state assay. The synthetic mismatch axis is dimensionless; it is not a predicted wavelength spectrum or a fitted copy-error rate.

## Recursive disposition and full-goal dependencies

| Requirement | What this candidate adds | What remains unverified |
|---|---|---|
| I: material identity | Documented KTiOPO4 crystal and template growth | Exact Mo34WV identity and persistence are unchanged |
| H/M: state carrier | Seed-related grating propagation plus new-layer nonlinear optical function | Measured founder cross-talk bound, separated daughter function and serial transmission |
| V: functional variants | An engineered periodic pattern can affect optical response | Two parent-associated functional patterns transmitted under common growth, with variation/selection |
| R/B/T | New crystalline material is supplied through flux growth | Damage repair, selective maintained boundary and waste/resource transport coupled to competent organization |
| E/S/A/C | Optical pumping converts frequency in a state-dependent material | Complete-cycle maintenance energy, relevant sensing, chemical adaptive update/generalization and intelligence |
| J: integration | No demonstrated joint system | Common characterized organization with Mo34WV or PMo12, state renewal/partitioning and add/remove/rescue controls |

Retain **component-supported template growth and new-layer SHG**. Do not admit full H/V or an integrated complement. The growth furnace, cooling/control, initial electrical patterning and optical pump are supplied externally. External drive is allowed by the goal but must be accounted; it does not demonstrate autonomous material renewal or adaptation. High-temperature fluoride/phosphate flux is not the acidic aqueous operating environment of the PMo12 component. No shared-medium transfer or complete separated thermal architecture was tested.

The next discriminating carrier experiment would use two functionally distinguishable seed patterns under the same growth conditions, spatial cross-talk calibration or a separated grown piece, then regrow a second generation and assay its function. For a signed domain state, the readout must retain phase. Those observations are missing; no simulation can supply them as facts.

Other scouts found NaClO3 and tellurium leads already analyzed locally; no new source/candidate credit is given for those rediscoveries. An unconsumed Fe-redox/site-counting SI, DOI10.1021/acscatal.2c03898, remains a concrete next R-assay lead. Its corrected redox charge and apparent TOF are mathematically coupled, and its carbon-black/Nafion preparation is not an admitted noncarbon complement. It must not be used as a universal founder-activity ceiling or transferred to the Poli/Han systems without measurement.

This goal turn is **progress**: it acquires a new primary evidence family, identifies a spatially assayed new-material function, and tests an actual readout ambiguity. All earlier negatives remain. The full twelve-function objective remains active and unachieved.
