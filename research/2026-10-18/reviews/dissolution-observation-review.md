# Independent review: dissolution observation

Scope: `documented-scaffold-2026-10-18/dissolution-observation/`, primary DOI 10.1021/acscatal.6c01228. Reviewer owns only this file. Source files and executor results were inspected without alteration; the CLI was not rerun into its output directory. No experimental response points were digitized and no chemistry parameter was fitted. Rounded source outcomes and figures were already exposed, so this is not blind validation.

## Verified source and methods

Native PDF: 9 pages, 2,037,302 bytes, SHA256 `e5ae9fa1eacd667d2f464fbdbfd35dbe80c0453d360b423602d76a258fd9b0aa`. Native DOCX: 7,850,022 bytes, SHA256 `7b93a4d8c5920e33fd9222417a393895a193d6f5c7d1a880c1273ce436d43048`. Both copies match the Downloads originals byte for byte; DOCX ZIP CRC test returns no bad member; the PDF contains the expected DOI. Artifacts: `sources/cs-2026-01228g.pdf`, `sources/cs-2026-01228g_si_001.docx`, and acquisition receipts.

The native page-2 image confirms **50 mL**, not 50 microlitres. Figure 1 shows a reservoir feeding the cell in both states: cell outlet returns during recirculation and goes to ICP-MS during sampling. The separate baseline feed is not a replacement feed into the reaction reservoir. No complete reset or fresh top-up is depicted. The exact well-mixed circulating volume, sampling concentration statistic, prior-export correction and valve/dead-volume details remain unspecified. Total electrolyte used is not independently measured circulating inventory.

Main flow is approximately 3.2 microlitres/s; SI outlet flow is approximately 3.5 microlitres/s. Five-minute OCP collections occur at nominal 1, 2, 3 and 6 polarization hours. Conditional withdrawal volumes are 0.96 and 1.05 mL. Approximate 50 mL volume and these flows imply turnover times 4.34028 and 3.96825 hours, not a five-minute complete exchange. Actual mixing and dissolution during OCP remain unmeasured assumptions.

ICP-MS calibration standards and matrix dilution do not provide raw blank variance, an accumulation-specific quantitative detection threshold, recovery, or a complete observation operator. The naturally abundant Ni-60 and Fe-56 channels are not origin labels. Fig. 6c repeats data from 6a; SI S9 is beginning/end average potential, not a continuous paired trace. XRF 300 spatial measurements are not 300 independent dissolution replicates. Acidic internal-standard mixing precedes elemental analysis; elemental signal alone cannot universally distinguish ionic dissolution from particles or attribute catalytic activity.

## Independent native equation and axis audit

Invocation: Python 3.12 `zipfile.ZipFile`, `xml.etree.ElementTree`, and PyMuPDF reads of the native source files; inspect `word/document.xml` namespace `http://schemas.openxmlformats.org/officeDocument/2006/math`, zero-based `oMath` elements 9, 10, 12 and 13. Binary observables: ZIP intact; element 10 contains an explicit `m:f` numerator `0.059`, denominator `3`; elements 9 and 13 have balanced atom/charge counts. Captured source evidence is retained in `sources/si-equation-09.xml`, `-10.xml`, `-12.xml`, `-13.xml`, and `sources/si-math-structure.json`.

The suspected Nernst coefficient error is **rejected**. Native Eq. S5 evaluates at log10 ferrate activity −9 to `2.236 + (0.059/3)*(-9) - 0.039*pH`: 1.552 V at pH 13 and 1.513 V at pH 14, agreeing with rounded main-text 1.55/1.51 V. Plain text concatenated numerator and denominator into `0.0593`. Native Reaction 30 separately prints `FeO4(2−) + 8H(+) + 3e(−) ⇌ Fe(3+) + 5OH(−)`; it fails atoms (left H8/O4, right H5/O5) and charge (left +3, right −2). This is a real displayed-expression inconsistency, not proof that Eq. S5 or the paper's diagram is wrong. Replacing that product with four waters would balance the acidic half-reaction; no source file was silently corrected.

Figure-6a ticks were independently recovered using PyMuPDF `get_drawings()` on PDF page index 4, selecting black major-tick rectangles near x=91.12 and 256.14 points, y=330–410 points, widths 2–2.3 points. Left tick centers for 0/5/10/15 are 407.9210205/383.8510132/359.7310181/335.6610107; right centers for 0/2/4/6/8 are 407.9210205/392.3310242/376.7810059/361.1910095/345.5960236. Outer-tick slope ratio exactly reproduces `sources/fig6-axis-calibration.json`: 1.617206663 microgram/cm² per ppb, equivalent conditionally to 45.84780890 mL at 0.02835 cm². An independent all-tick least-squares method gives 1.616749613 and 45.83485154 mL. An initial strict equality assertion comparing these different estimators failed; using the documented outer-tick calculation resolves the comparison, without changing either source or saved values. This reviewer-side estimator mismatch is preserved here.

The approximately 8.3% difference from an exact 50 mL conversion exceeds the tiny tick-estimator difference but has no supplied statistical uncertainty model. Approximate reservoir volume, sampling loss and conversion choices remain unresolved. The effective volume is neither a measured inventory nor evidence that the experiment is erroneous. Detector pulses return toward baseline between collections; the two axes are converted versions of one signal, not independent stock and export measurements. No curve response values were extracted in this review.

## Independent numerical reproduction

Invocation from repository root: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3` with a read-only here-document importing `test_measurement.py` through `importlib.util.spec_from_file_location`, loading `results/measurement.json`, and separately evaluating these recurrences for all eight scenarios and all four windows:

```python
solid, liquid, exported = 10., 0., 0.
for dt in (1., 1., 1., 3.):
    solid -= dt
    before = liquid + dt
    dv = q * .3  # mL in 300 seconds, q in microlitres/s
    if operator == 'unreplenished':
        after = before * (volume - dv) / volume
        volume -= dv
    elif operator == 'clean_replenishment':
        after = before * math.exp(-dv / volume)
    else:
        after = 0.
    exported += before - after
    liquid = after
```

Binary observables: **all 32 records reproduce** saved solid, pre/post liquid, export, volume, concentration and wall time within 2e−14; maximum absolute difference 3.9874186305e−15. Total solid+liquid+export remains 10 within that tolerance. All 11 pure `checks()` assertions pass; independently recomputed input hashes equal all four saved hashes (the CLI's twelfth check). Artifacts: `results/measurement.json`, `results/EXECUTION.md`, and this captured independent result. No outputs were overwritten.

| q (microlitres/s) | Operator | Final liquid | Final exported | Final volume (mL) |
|---|---|---:|---:|---:|
| 3.2 | Unreplenished | 5.763418443116 | 0.236581556884 | 46.16 |
| 3.2 | Clean replenishment | 5.775379903714 | 0.224620096286 | 50 |
| 3.2 | Complete reset | 0 | 6 | 50 |
| 3.5 | Unreplenished | 5.740571425800 | 0.259428574200 | 45.8 |
| 3.5 | Clean replenishment | 5.754901404065 | 0.245098595935 | 50 |
| 3.5 | Complete reset | 0 | 6 | 50 |

First-window fractions retained are 0.9808/0.979 without top-up and 0.980983145993/0.979218964569 with clean matched inflow. Hypothetical 0.05 mL fixed-volume final liquid is 1.3761545261e−8/2.2747681289e−9 units; this is explicitly a synthetic topology/unit sensitivity. Native volume has not been reinterpreted as microlitres.

Source exhaustion, zero source, physical zero-flow limits, linear scaling, analytic retention, concentration invariance, and rejection of draining a too-small unreplenished pool are checked. Complete reset correctly has distinct semantics: it removes/refills 50 mL regardless of q, exporting 200 mL across four windows; it is deliberately excluded from the flow-governed zero-flow limit. Final wall time is 6 + 4/12 hours, not an assertion about the source's full plotted conditioning clock.

Verified calculation hashes:

- `PROTOCOL.md`: `73e57b30ecdec0c4dc3543feb0aa0d9e3acc3d9350d0f8281e904355c7e8d3b8`
- `test_measurement.py`: `45423a4df1d1109bcdf43334cb5c6098a266dd246b08cd53427ffd2ee3a3cb29`
- `results/measurement.json`: `1ecc25cd3093789e505eea27ff1260cdbce9cd16e1d114ba32f1b2b5f6293e03`

## Scientific interpretation and current disposition

The frozen protocol and executed calculation are scientifically defensible as a **conditional measurement and conservation test**. Complete replacement is unsupported by the nominal flow/50 mL scenario. Successful numerics do not identify which operator generated the paper's measurements. Liquid stock `cV`, integrated exported mass `integral(qc dt)`, and gross electrode dissolution are distinct. Simultaneously adding an admissible common nonnegative flux to dissolution and redeposition leaves net liquid change unchanged; net elemental loss alone cannot identify either gross flux or origin-specific active repair.

No measured outcome fit, held-out prediction, isotope-resolved function, founder-capacity bound, isolated descendant, serial functional inheritance, high-current stability extrapolation, compatible complement, or integrated life/intelligence claim follows. Earlier negative outcomes remain applicable. The correct next requirement is a calibrated observation operator and discriminating origin/function controls, not an additional free repair rate fitted to ambiguous net loss.

## Final report review and terminal verdict

Reviewed `REPORT.md`, `CHEMISTRY_AUDIT.md`, `negative_results.json`, `checks.md`, and `progress.md` against the independently inspected sources and reproduced calculations. One report sentence could have implied that synthetic calculations become empirical evidence without a plot; root replaced it with the explicit statement that plotting or a fitted score supplies no experimental validation. The corrected text was verified directly. There are no remaining blocking scientific or numerical findings within this bounded scope.

Final read-only Python JSON/hash assertions passed: exactly 12 unique negative IDs; no empirical holdout, fitted chemistry, origin-specific function or added complement; all 12 saved binary checks pass; maximum saved conservation error is 1.7763568394002505e−15; all four frozen inputs retain their saved hashes. This validates the new ledger's contents, not a new global repository audit. The negative ledger retains access failures, missing raw data, sampling/reset uncertainty, flow discrepancy, axis mapping, detection/matrix uncertainty, gross/net ambiguity, unresolved repair, the rejected coefficient suspicion and separate source typo, absent kinetic holdout, and stress/integration limitations.

Final reviewed hashes:

- `REPORT.md`: `c34f4ba61d5d32356220ea41016442bfe915e999f8602564c23ae50b1f22cd9e`
- `negative_results.json`: `6d96f5f4467a3582bb1c56881fc624a29fab03286a9102511d7ecc5366d659d5`
- `CHEMISTRY_AUDIT.md`: `079351f501d969c5295d7bd052b83105b51c3a59ffd6d9c601aeb95e307312d5`
- `SOURCE_AUDIT.md`: `8140818370e04663d64b062ce0be4c4de3f1f7d63624a887d4f82b683abff2cc`

**APPROVE — bounded native-source, chemical-transcription and conditional sampling/mass-balance analysis.** No empirical active-repair validation, prospective/held-out chemistry result, functional inheritance, new verified complement, or full-goal completion is approved. The source improves assay requirements while leaving the identified scientific negatives intact. Parent may mark this independent review complete; no additional numerical rerun is needed.
