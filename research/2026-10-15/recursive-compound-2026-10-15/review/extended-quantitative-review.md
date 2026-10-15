# Extended independent source and quantitative review

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

This extension covers finalized compatibility and site_chemistry, the revised heredity calculation, WORKPLAN.md and PROTOCOL.md. It supersedes the initial finding about the two literal heredity controls: those controls have been replaced and the original finding is resolved. The pending root REPORT.md was not reviewed.

## Findings by severity

CRITICAL: none.

HIGH: none.

MEDIUM — `heredity/check.py:6–10,52–55`: the revised calculation now has genuine input-dependent tests, but it also adds configurable unit-label arguments and strict runtime Fraction-type checks to an internal arithmetic helper whose only actual data callers already supply Fraction values in fixed units. The labels cannot validate real measurement units and are never varied in actual calculation calls. This is unnecessary interface/validation complexity under the programming/remove-ai-slops perspectives. Prefer fixed documented units and typed arguments; retain meaningful mass/domain controls and changed-input tests. The current calculation is correct, and this does not block the scientific dossier.

LOW — `PROTOCOL.md:38` calls the calculation “fixed-geometry substitution strain.” What was calculated is a bond-valence mismatch, not a strain, strain energy or relaxation. Use “fixed-geometry bond-valence mismatch” to prevent an energetic interpretation. The detailed site report already makes the correct distinction.

LOW — `compatibility/selected_rows.csv:2–3` contains only selected species columns. The D2O rows omit PMo11 and PMo9, so the displayed species columns do not exhaust the stated assigned-POM denominator. The report's parent fractions are accurate and do not sum these partial rows. If this CSV is reused, explicitly preserve its selected-column status or include the omitted species. Do not renormalize its three displayed species columns to 100%.

## Compatibility: direct primary-table verification

Visually inspected all six retained SI page images (144, 157, 160, 67, 83, 87), rather than accepting extracted text or check output. PMo12 phosphate pH3/pH4 has 0/0/0 parent replicates and 1% P2Mo18 plus 99% combined P2Mo5/PMo6 at both stages. Actual pHs reproduce: 1.97±.04 → 1.89±.06 and 2.10±.06 → 2.03±.09. D2O parent replicates are 73/77/77 initially and 71/76/77 after incubation, with source means 76±2 and 74±3. The 74.67 versus printed 74 discrepancy is accurately preserved. The D2O tables also contain PMo11 and PMo9, explaining the partial-column CSV sums.

Potassium alpha-Dawson phosphate pH3/pH4 rows have 100/100/100 parent replicates both initially and after incubation. Actual pHs reproduce: 2.99±.08 → 2.98±.06 and 4.00±.06 → 3.97±.06. These are different actual media from the PMo12 rows despite matching starting-buffer labels.

Primary main text `raw/article.txt:1927–1929` explicitly says that integration considers assigned POM peaks and ignores free phosphate. Therefore these are conditional phosphorus-signal fractions, not total-metal recovery or necessarily molecular mole fractions. The report correctly preserves the lack of a numerical analyte-specific detection limit and does not equate printed 0/100% with zero molecules or quantitative recovery. Incubation at 37°C and NMR acquisition at 25°C are correctly separated.

The SI table headers explicitly identify K6 alpha-Dawson. The oxidized potassium 10 mM result cannot establish the concentrated reduced lithium reservoir behavior in a different paper. The report and protocol retain this distinction. Neither Mo36 nor the proposed Mo34WV joint system was tested. The reported empty *verified* joint-condition intersection is an evidence statement, not a demonstrated empty physical compatibility region.

## Site chemistry: independent 324-sum recomputation

Read primary Table 4 rows directly from `sources/gagne2015.txt:846,858,886`: V(V): R0 1.799 Å, B .388 Å, 714 polyhedra, RMSD .105 vu; W(VI): 1.909, .339, 436, .188; Mo(VI): 1.903, .349, 970, .143. The parameter file and report match one primary publication.

A fresh read-only standard-library calculation read the parent coordinates and independently computed distances, exponentials, sums and rankings for 36 metals × 3 cutoffs × 3 parameter sets. Maximum discrepancy against all 324 saved sums was zero at floating-point precision. Every cutoff reproduces Mo range 5.9034774878–6.3121660494 and parent RMSD .14467664485 vu. W's best label is Mo8 (6.0047903982), followed by Mo9 (6.0525440446). V's best label is Mo7 (4.7190643440), followed by Mo18 (4.6771692607). Inversion-copy differences are numerical roundoff. All V sums are below five.

Crucially, Mo7 is also the worst parent site: Mo BVS 6.3121660494. That warning is present prominently in the site report. The published calibration RMSDs are not uncertainties for these cluster sites, and agreement between aggregate parent RMSD and published Mo RMSD cannot validate a target oxidation state. Uniform use of oxide-ion parameters at inferred aqua donors, missing hydrogens/counterions and lack of coupled-site relaxation prevent promoting these ranks to an incorporation probability, stable target, pair energy or synthesis recommendation. These limitations are accurately retained.

## Heredity repair recheck

Inspected the revised function and tests. The measured-data calculation now calls the same function tested with zero, fractional and full founder masses and changed capacities. To avoid the module's output writes, isolated only that pure function with AST and exercised it independently with previously unused values: F=1, M=4, q_seed=.003, q_product=.2 gives 3/800; zero-founder gives zero; F=2, M=4, q_seed=.2, q_product=.1 gives one. Founder mass above product and zero product capacity raise ValueError. The original tautological-controls concern is resolved. Additional unit/type machinery remains a nonblocking minimality concern as listed above.

## Scope and skill perspectives

WORKPLAN and PROTOCOL retain the full goal, explicit unverified target, same-system requirement, material renewal, inheritance, variation/selection, sensing/state/action and bounded intelligent behavior. There is no aggregate life score, invented acceptance threshold, assertion of current holdout validation or claimed target synthesis. Carbon-free active organization is distinguished explicitly from fabrication and measurement apparatus. External energy/training do not silently substitute for the claimed local mechanism; reliance on organic materials inside the maintained organization remains an unresolved requirement. This is a transparent evidence contract rather than a claim that the present candidates achieve it.

Both requested skill perspectives remain applied from the earlier loaded programming/remove-ai-slops documents. Primary-table transcription and geometry extraction serve the stated scientific task. The revised heredity controls now test real behavior; residual unnecessary unit/type interface checks are the sole new medium minimality finding. Compatibility's equal-fraction example is an explicitly labeled mathematical nonidentifiability counterexample, not claimed physical or software validation.

No new source search, source downloads, output-generating candidate runs, physical experiments or target calculations were performed. Root synthesis remains pending review; final conclusions must preserve these same limits.
