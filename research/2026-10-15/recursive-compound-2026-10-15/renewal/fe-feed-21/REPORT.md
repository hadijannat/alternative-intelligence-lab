# Candidate-role21: Fe(II) feed for active material renewal

**FeSO4·7H2O is retained as a component-supported renewal comparator, with no verified addition to the Mo34WV assembly.** The proposed partner is a borate-intercalated NiCoFe layered hydroxide on an externally driven electrode. Its solid composition varies; assigning it a single molecular formula would be misleading. The source demonstrates precursor-specific recovery of electrode performance consistent with replenishment. It does not demonstrate repair of the target cluster or inherited function in newly formed descendants.

The [primary study](https://doi.org/10.1038/s41467-021-26281-0) uses alkaline borate electrolyte, with pH14 for the comparisons examined here and a20°C cell. This differs from the acidic Mo36-derived hypothesis; the actual Mo34WV operating medium is unverified. The apparatus includes Nafion between electrode chambers. This is not evidence that the complete experimental organization is carbon-free or that its repair mechanism transfers to the target.

## Recovered measurements

The complete source package was acquired from EuropePMC. Five XLSX workbooks were inventoried and original bytes pinned; [analysis.json](analysis.json) identifies the exact source cells, panel mapping and missing uncertainty. Article and workbooks are one retrospective evidence family. No fitting or held-out validation is claimed.

In Figure2e, the caption specifies30µM Ni(II), Co(II) or Fe(II) addition at0.5h. Each curve has an exact recorded point at0.5h and at the common endpoint2h:

| Added ion | Potential at0.5h, V vs RHE | Potential at2h, V vs RHE | Within-curve change |
|---|---:|---:|---:|
| Ni(II) | 1.70779 | 1.72804 | +20.25mV |
| Co(II) | 1.69771 | 1.66624 | -31.47mV |
| Fe(II) | 1.71003 | 1.62190 | -88.13mV |

These descriptive changes distinguish the feed responses in the reported chronopotentiometry. They are not replicated treatment-effect estimates, deposition rates, atom-replacement fractions or evidence of target renewal. Baselines differ; uncertainty and replicate count are not supplied in the worksheet. The0.5h point is not established as strictly before dosing. Figure2e's exact current density is not specified in its caption or graphic, so the10mA/cm2 label from adjacent panels is not transferred.

Figure1c contains12deposition-rate observations. The recorded values are zero from1.54 through1.62V vs RHE,1.4ng/cm2/min at1.64V, and16ng/cm2/min at1.76V. Reported zeros do not establish a detection limit. The anticipated matched Co-assisted EQCM curve is absent from this source-data comparison: Figure2e instead measures potential versus time. No quantitative Co-induced deposition-rate ratio can be calculated from these two panels.

## Conflicts and limits that change the next test

Figure2d workbook cellC1 says `with 50 mM Fe(II)`, while the article text and published graphic say50µM. This1000-fold unit discrepancy is preserved. Its apparent nature as a header error does not justify silently changing the acquired data or fitting dose-response kinetics from it.

The separate no-added-feed experiment reports film Fe decreasing from10.4 to5.4nmol/cm2 in10h. It measures net inventory loss in that preparation. It cannot supply a founder-replacement bound for the fed experiment. Likewise, nominal50µM addition,22.7µM fresh soluble Fe and7.5µM after aging are different quantities; nominal feed is not freely available dissolved inventory.

The next discriminating renewal measurement needs isotope-labelled Fe feed, time-resolved isotope composition of the solid and solution, and simultaneous catalytic function. Founder retention, atom exchange, new inactive precipitate and newly competent material require separate accounting. Target admission additionally needs species-resolved Mo34WV persistence and useful maintained function in a demonstrated shared medium or a characterized coupled compartment. None is present here. No chemical rate or inheritance rule is supplied by assumption.

[SOURCES.md](SOURCES.md) records acquisition, license and hashes. [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) records the separate cell/claim audit. Run `analysis.py` with the recorded openpyxl environment to reproduce the descriptive extraction. The earlier failures remain intact; no new physical experiment or verified integrated complement was produced.
