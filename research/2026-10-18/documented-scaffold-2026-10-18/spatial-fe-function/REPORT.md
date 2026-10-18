# Spatial Fe function and ancestry: conditional bounds, unresolved attribution

The source-informed four-pool model leaves incoming-material function
ambiguous even when regional Fe totals, bulk Fe ancestry and site competence
are hypothetically known. It nevertheless gives useful conditional bounds.
All frozen numerical checks passed. **Experimental held-out validation is
INSUFFICIENT_DATA**; this iteration identifies no novel compound or integrated
life function.

## Source and chemistry boundary

[Wei et al. (2025)](https://doi.org/10.1021/jacs.5c00438) motivates separate
edge-associated and plane-associated Fe states in Fe-doped Ni hydroxide.
The acquired [primary SI](https://acs.figshare.com/articles/journal_contribution/28718969)
uses total-Fe-normalized turnover and different specimens, supports or
electrolytes for local electrochemistry, bulk characterization and Raman.
It does not supply matched, independent regional competent-Fe counts or Fe
ancestry measurements. Oxygen isotope exchange does not label Fe origin.
Main-article access remains restricted. The full source audit and acquisition
failures are retained in `SOURCE_AUDIT.md` and `ACQUISITION.md`.

The model is an intentionally favorable limiting test: every Fe atom within
a region shares a known, fixed nonnegative competence, and background is
known. It does not represent measured per-site rates or independently
identified active/inactive pools. Ni reconstruction, inactive Fe,
speciation and transport/contact changes introduce further unknowns. This
static observation model does not replace a kinetic transport model.

## Exact result

For edge inventory E, plane inventory P and incoming inventory N,

```
max(0, N - P) <= N_E <= min(E, N)
j_new = k_P*N + (k_E - k_P)*N_E
```

Evaluating both endpoints gives the exact attainable interval, including
when plane competence exceeds edge competence. For the frozen case
E=0.7, P=0.3, N=0.4, k_E=10, k_P=1 and b=0.2, the incoming contribution is
**[1.3, 4.0]** while the total observed current is **7.5**.

| Synthetic world | Founder edge | New edge | Founder plane | New plane | Founder current | New current | Total current |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lower endpoint | 0.6 | 0.1 | 0 | 0.3 | 6.0 | 1.3 | 7.5 |
| Upper endpoint | 0.3 | 0.4 | 0.3 | 0 | 3.3 | 4.0 | 7.5 |

Both worlds conserve the same total Fe, founder Fe, incoming Fe and regional
inventories, with the same fixed coefficients and background. The nonzero
conditional lower bound is information under these assumptions; it is not
an observation of new-material activity in this paper.

The measurement matrix for regional totals, bulk incoming Fe and current
has rank **3** over four pools. Its null direction `(1,-1,-1,1)` changes
incoming current by `k_P-k_E` per unit while preserving those observations.
Adding independently measured incoming edge Fe raises the rank to **4**.
That resolves this algebra only; it does not calibrate competence or prove
same-specimen repair.

## Positive controls and negative outcomes

| Frozen control | Conditional incoming-current bounds | Identified under model assumptions |
|---|---:|---|
| Equal competence | [0.4, 0.4] | Yes |
| No incoming Fe | [0, 0] | Yes |
| All Fe incoming | [7.3, 7.3] | Yes |
| Empty edge | [0.4, 0.4] | Yes |
| Empty plane | [4, 4] | Yes |
| Zero inventories | [0, 0] | Yes |
| Edge competence zero | [0, 0.3] | No |
| Plane competence zero | [1, 4] | No |

All **720** rational-grid cases and **15,120** feasible allocations satisfy
the frozen nonnegativity, closure, unchanged-current and attainable-bound
checks at 1e-12. The maximum recorded residual is 4.44e-16. Three unit-test
scenarios cover exact endpoint attribution, reversed/equal competence and
invalid pools, coefficients and allocations. These are implementation and
algebra checks, not independent empirical replicates.

The empirical screen has zero training points and zero held-out points:
**INSUFFICIENT_DATA**. No rate fitting or experimental model-selection result
is claimed. The prior remote-Fe models' five-hour ordering failures and
failed 1e-5 numerical convergence screen remain unchanged and preserved.
`AMENDMENTS.md` corrects the frozen protocol's description of these as
"fitted-model failures": they were unfitted synthetic-model failures.
The frozen protocol bytes, mathematics and cases are unchanged.

## Reproduce and inspect

From the workspace root, use the installed Python environment with NumPy:

```sh
python3 documented-scaffold-2026-10-18/spatial-fe-function/analyze.py
python3 documented-scaffold-2026-10-18/spatial-fe-function/test_model.py
```

The observed invocation used Python 3.12.3 at
`/USER_HOME/.pyenv/versions/3.12.3/bin/python3`.

| Scenario | Binary observable | Captured artifact |
|---|---|---|
| Frozen grid, controls and matrix test | Exit 0; all eight summary checks true | `results/run-output.json`, full `results/analysis.json`, `results/grid_allocations.csv` |
| Endpoint, competence and invalid-input tests | Exit 0; 3 tests OK | `results/test-output.txt` |
| Empirical evidence eligibility | Status exactly INSUFFICIENT_DATA; 0 train/0 held out | `results/analysis.json` |

Original protocol and source hashes are in `EXTRACTION.md` and the analysis
artifact. `NEGATIVE_RESULTS.json` retains the scientific limitations.

The next discriminating evidence needs matched founder preload/damage and
metal supply/withdrawal, regional Fe-origin observations, and independently
calibrated competence or a justified founder functional ceiling, with
simultaneous function on the same specimen. Register specimen holdouts
before extracting their outcomes. No integrated complement, active repair,
functional inheritance, life or intelligence requirement closes here.
