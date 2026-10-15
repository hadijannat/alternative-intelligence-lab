# Oxygen labels constrain oxide-renewal inference

**Disposition: source-qualified measurement constraint.** Oxygen isotope exchange alone cannot establish renewal of the nominal Mo34WV target core or newly competent material. This audit adds zero candidate assessments, target observations, or verified complements; the existing 22 assessments and zero verified complements are unaffected.

The acquired source is Villa, Ohlin, Rustad and Casey, *Isotope-Exchange Dynamics in Isostructural Decametalates with Profound Differences in Reactivity*, original [supporting information](https://doi.org/10.1021/ja905166c.s001). Its title, authors, resource DOI and file identity match publisher metadata. The complete 19-page SI is retained with SHA256 `17f478c53e89545ccd211e828e1cad87856b4ea39d90fea62161811f19f5c5a0`; publisher metadata declares CC BY-NC 4.0. Main-article bytes were not acquired, so this audit makes no main-article figure readings. `SOURCES.json` records provenance and locators.

## Complete table and meaning

`rates.csv` preserves all 17 experimental rows of Table S-1-2, S3: 12 at 35.5 C and five at 6.0 C, with seven sites each. Of 119 site cells, 74 contain a rate/uncertainty pair, three Site D cells are too fast to estimate without a numerical bound, and 42 are unreported. The two pH 8.03 rows have concentrations 4.22 and 2.81 mM and remain separate. Blank cells are never zero rates or proof of no exchange. The table labels `log(k) s^-1` without explicitly defining its base. Reported log differences are primary. CSV `log_base=10` is a declared conventional arithmetic assumption; the fold ratios below depend on it.

The ion is [HxTi2Nb8O28]^(8-x)-. Site A is mu6-oxo; B is mu3-oxo; C/D/E are mu2-oxo; F/G are terminal oxos. **The source explicitly assigns Site A's rates to transformation into a new molecule.** Acidic Site B and other signal changes also cannot independently prove exchange within an unchanged molecule. Site D at pH <=7.5 and 35.5 C is too fast to estimate, not inactive. The remaining `--` cells receive no invented reason.

Table S-1-1, S2, uses 50 mM PIPES, HEPES, TRIS, CHES or CAPS across the corresponding pH ranges, and 50 mM tetramethylammonium hydroxide at pH 12.5. All buffers contain 0.1 M tetramethylammonium chloride; pH is adjusted with tetramethylammonium hydroxide and/or HCl. These organic-buffer/electrolyte conditions do not establish target compatibility. S3 states temperature uncertainty +/-0.2 C and concentration uncertainty +/-1%. Log-rate uncertainties are the larger of regression error and repeated-trial standard deviation; they are not stated as 95% confidence intervals.

## Reproduced point contrasts

Each ratio uses two reported entries from one row, so temperature, pH and concentration match. F/A compares oxygen-signal exchange with molecular transformation, not two equivalent atom-exchange endpoints.

| Row | Temperature C | pH | Concentration mM | Ratio | Reported log difference | Conditional fold ratio if base 10 |
|---|---:|---:|---:|---|---:|---:|
| S3-01 | 35.5 | 6.61 | 2.76 | F/A | 2.98 | 955 |
| S3-02 | 35.5 | 7.15 | 4.22 | F/A | 3.18 | 1,514 |
| S3-03 | 35.5 | 7.49 | 2.84 | F/A | 3.33 | 2,138 |
| S3-05 | 35.5 | 8.03 | 2.81 | D/E | 3.97 | 9,333 |
| S3-06 | 35.5 | 8.52 | 2.81 | D/E | 4.03 | 10,715 |

These rounded conditional fold ratios use `10**(log_k1-log_k2)` under the declared base-10 assumption. No uncertainty distribution, covariance, confidence interval, fitted kinetics, or target transfer is assumed.

## Structural and functional limits

Figure S-1-1 (S4) reports D/F/G signals essentially gone after three hours at pH 8.49 and 35.5 C. Figure S-1-2 (S5) reports C/E signal decline over several weeks at pH 8.03 and 35.5 C, while A/B remain constant; the authors interpret this as no molecular transformation. These qualitative observations are not assigned exact rate bounds or conflated with the pH 8.52 table row. At pH 6.61 and 35.5 C, Figure S-1-6 (S9) instead shows slow signals splitting and conversion to a new stable mu6-oxo signal with near conservation of that signal's intensity; asterisks identify signals from an unknown compound. This supports label retention through changed molecular identity without identifying the new compound or assigning a numerical retention fraction.

Together, the source separates isotope-label movement, persistence of a local oxygen signal, and molecular transformation. It supplies neither isotope-resolved competence of new material nor target-specific metal-framework replacement, structural heredity, autonomous reproduction, or life. A target renewal assay would need independent metal-framework/structural identity measurements and simultaneous functional attribution; oxygen labels alone cannot supply them.

## Verification

The standard-library analysis hashes the primary SI and frozen CSV, validates numeric fields/units/censoring, and reproduces the five same-row ratios. Seven tests pass, including changed source bytes, changed reported values, invalid units/nonfinite values, censored-as-zero input, missing rows, and endpoint/claim limits. Complete output is `.omo/evidence/oxide-isotope-constraints/tests.txt`; arithmetic is `analysis.json` and `.omo/evidence/oxide-isotope-constraints/analysis-output.json`. The rendered source table is `table-s-1-2.png`; the source-to-CSV comparison and acceptance ledger are in the same evidence directory.
