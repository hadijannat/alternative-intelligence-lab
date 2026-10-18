# Han isotope model independent review

2026-10-18. Verdict: **CLEAR APPROVE for the bounded numerical test and chemistry interpretation.** The tested closed-reservoir model fails. This review does not approve a living system, inherited function, active-site turnover fraction, or a validated mechanistic rate model.

Scope: `documented-scaffold-2026-10-18/founder-repair-search/test_han.py`, its `results/han_test.json`, frozen protocol/deviations, and the Han-specific scientific sections of `REPORT.md`. Consultation/UI completion and the other primary-source packages are outside this review. Reviewer changed no implementation or source files.

## Source and assay checks

Inspected the native main article text, supplementary text, Figure 3 JPEG, native XLSX XML, and relevant pages of the 139-page peer-review PDF. DOI: https://doi.org/10.1038/s41467-025-60201-w. The publisher web-tool open redirected to an inaccessible identity-provider page; local native bytes were inspected directly.

- Figure 3g and `Fig3!I27:K30` agree on isotope identity and micrograms per geometric cm2. The 1 cm2 geometric electrode area makes the nominal microgram inventories numerically equal to the reported area-normalized values; no hidden BET or felt internal area is used.
- The electrode is Bekaert 2Ni18-025 nickel felt. Initial and endpoint groups are independent coupon assays. Main methods describe water rinsing followed by ICP-MS, without a digestion or selective active-film isolation protocol. The measured stock cannot be treated as isolated active-site inventory.
- The H-cell methods specify 50 mL in each compartment and describe the cell as undivided. Both 50 mL and 100 mL accessible-reservoir conventions are therefore conditional assumptions. Neither is a measured transport coefficient or closed experimental isotope balance.
- Enriched-standard isotope purity and labile Fe fraction are unspecified. Natural-background amount fractions are correctly converted to mass fractions in the model. Initial measured 57Fe/56Fe is 0.10730924, versus nominal natural mass ratio 0.02350743. The source Figure 3g visually contains this discrepancy; it is not merely a parser error.
- Individual isotope sums differ from the supplied sum column, including 3.181 versus 3.189 micrograms/cm2 for continued EA. Both values remain preserved. The reported sum covers 56Fe and 57Fe, not all iron isotopes.
- Caption SEM/n=3 does not supply numerical SEM or replicate values in the isotope block. No statistical rejection or significance level follows from the analyst's 0.25 microgram/cm2 tolerance.
- Peer-review PDF page 116 reports approximately 0.5 microgram/cm2 inherent Fe in bare felt. Page 31 reports a separate device open-circuit-rest comparison with about 80 mV improvement. These support caution about host-associated Fe and resting controls, but do not supply isotope-resolved active-film function or half-cell pulse-rate calibration.

## Independent execution and captured observables

Python used: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`.

The live review invocation imported the script through `runpy.run_path`, called `self_check()`, recomputed `fit_controls()` separately for both saved bath inventories, and recomputed both `pulse_prediction()` clock cases. It asserted control and pulse predictions against saved JSON with `atol=1e-12, rtol=0`, without running `main()` or overwriting results. Captured terminal observables were `SELF_CHECK_PASS` and `REPRODUCED_PASS`.

Reproducible invocation for that scenario:

```python
import runpy, json, numpy as np
from pathlib import Path
b = Path('documented-scaffold-2026-10-18/founder-repair-search')
m = runpy.run_path(str(b / 'test_han.py'))
m['self_check']()
r = json.loads((b / 'results/han_test.json').read_text())
ini = np.array([2.49, .2672])
obs = np.array([[.814, .2167], [1.259, 3.10598]])
for s in r['finite_bath_models']:
    bath = np.array(s['initial_bath_ug_cm2'])
    p, _ = m['fit_controls'](ini, bath, obs)
    pred, _ = m['advance'](ini, bath, p[0], np.array([.5, .03])[:, None]*p[1], 20)
    assert np.allclose(pred, s['control_predictions_ug_cm2'], atol=1e-12, rtol=0)
    for t in s['reserved_tests']:
        y, liquid, _, _ = m['pulse_prediction'](ini, bath, *p, t['clock'])
        assert np.allclose(y, t['predicted_ug_cm2'], atol=1e-12, rtol=0)
        assert max(abs(y+liquid-ini-bath)) < 2e-14
print('REPRODUCED_PASS')
```

| Accessible bath | Control RMSE | Reserved OER-clock prediction [56Fe,57Fe] | Reserved elapsed-clock prediction [56Fe,57Fe] |
|---|---:|---|---|
| 50 mL | 0.43683167563729586 | [0.39098819055592315, 0.6065856584258107] | [0.28970034657041266, 0.4494459927823957] |
| 100 mL | 0.3537739074341402 | [0.24102655493465264, 0.5741830896447482] | [0.14722019336179049, 0.3507138269701784] |

Units are micrograms/cm2. Largest independently observed conservation residual was 1.7763568394002505e-15. Both control screens and all four reserved screens fail. OER-clock execution has 20 h OER plus 1 h pulses; elapsed-clock execution has 19.05 h OER within 20 h. Unknown pulse charge remains null.

A second live invocation recomputed every 0.5, 1, 2, 4, 8 timescale sensitivity using `advance()` and `pulse_prediction()`, asserting SSE and predictions against JSON to 1e-12. Captured terminal observable: `SCALING_REPRODUCED_PASS`. At factors 1, 2, 4 and 8 the control SSE stays 0.7632876513603507 for 50 mL and 0.5006239103248785 for 100 mL. Reserved predictions change substantially. An interior grid optimum therefore does not identify absolute rates. No multiplier was selected to fit the reserved endpoint.

Independent algebraic check: any common nonnegative isotope-rate history in this specified closed reservoir produces `S = alpha*S0 + beta*(S0+L0)`, with nonnegative coefficients. The minimum attainable 56Fe/57Fe mass ratios are 0.6445720981445575 and 0.4197729945055977. The entire reserved +/-0.25 tolerance box permits at most 0.3728959861890375. Both deterministic comparisons returned `NO_ADMISSIBLE_PASS`. This makes failure of the operational screen robust within this model class despite the rate ambiguity. It does not establish statistical incompatibility or reject actual Fe exchange.

The excess-label arithmetic was checked independently: `(2.567 - 0.2672)/(0.614 + 2.567) = 0.722980194907262`, and excess is 2.2998 micrograms/cm2. Its denominator is the measured two-isotope stock. It is a conditional population descriptor, not a lower bound on new functional sites or a tracked-coupon turnover measurement.

## Interpretation and preservation

The report correctly makes calibration failure primary. Reserved failure cannot uniquely diagnose missing pulse-enhanced uptake because homogeneous stock, accessible bath, species pools and assay assumptions can already fail. The source functional electrode evidence and separate device gas assay are not merged into a new-atom-specific activity measurement. No functional-inheritance or integrated-complement credit is granted.

The reserved endpoint was analyst-exposed before implementation. This protocol violation is explicitly retained in `DEVIATIONS.md`; the numerical fitting still excludes EA. Reported validation is retrospective and analyst-exposed, not blinded or fully protocol-compliant. Previous implementation failures and negative source/model findings remain recorded by the root.

Reviewed immutable hashes:

- `test_han.py`: `f1fb05fe42f4b7c555a952ff3b31e5326712e0e925da56cff81ba99b57e6664e`
- `results/han_test.json`: `4db38242d9a32f117fac24e7e1e2e53955d3ca766846593984d6639f5be698d4`
- `PROTOCOL.md`: `1ddca9cca5effc7da93458365ae61b8c7f63e41becffcd2d91f5dcc17edd14ce`
- `DEVIATIONS.md`: `6e1d75396ce0ee62134c39fcdae0674feba5d7c41b16d2dd560215ac2cc4bc9a`
- Native source workbook: `6807bd68789619eaa116329b9b73b14ed3d1e779696590dca665c77f12183206`

No physical experiment, source replication, isolated-new-material activity assay, full electrolyte Fe balance, or independent Claude UI completion check was performed in this review. The missing assay and isotope uncertainties limit mechanistic inference; they do not turn the failed model into evidence against inorganic repair generally.
