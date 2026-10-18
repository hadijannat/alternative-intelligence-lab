# Extraction and analysis boundary

No experimental response points were extracted or fitted in this iteration.
The source worker inspected methods, captions and the primary abstract before
the parent froze `PROTOCOL.md`. Total-Fe loading descriptors were already
visible during that audit. This is not a prospective experimental holdout.

`analyze.py` implements the frozen four-pool model with known, fixed synthetic
site competence and background. Its rational grid uses `fractions.Fraction`
for inputs and feasible allocations, then tests floating-point observables at
absolute tolerance 1e-12. NumPy supplies matrix ranks, without SciPy. The
reported current is dimensionless and is not a measured rate.

The main counterexample, eight controls and 720 grid cases are fixed in the
protocol. `results/analysis.json` records all case bounds and diagnostics;
`results/grid_allocations.csv` records all 15,120 grid allocations. Neither
file is an experimental dataset. No train/test split, parameter search or
candidate ranking was performed.

Original input SHA-256 values at execution:

| Input | SHA-256 |
|---|---|
| `PROTOCOL.md` | `7ddde2de239ec378debd191e16ac0bcc0035a3c411d54f9216b0203f00770822` |
| `SOURCE_AUDIT.md` | `37996dc504dd133dfaea230167439baf9277d5b674a563407d643221f7229fb9` |
| Native SI `sources/ja5c00438_si_001.pdf` | `658e8a17f67d282b219ea77cefb59aa59dccfe1deb06555b7a7a3f93e1f6dca1` |

The execution also hashes its own code in `results/analysis.json`. The PDF
hash records the audited source identity; no PDF response data enter the
calculation. A published projection can omit that licensed native file and
still run the synthetic algebra, but its regenerated source hash will then
be null. Original source hashes must remain distinct from any sanitized
publication hashes.

Primary source: [Wei et al., DOI 10.1021/jacs.5c00438](https://doi.org/10.1021/jacs.5c00438);
[native SI record](https://acs.figshare.com/articles/journal_contribution/28718969).
See `SOURCE_AUDIT.md` for assay mismatch, total-Fe normalization, lack of
independent competent-site counts and restricted main-article access.
