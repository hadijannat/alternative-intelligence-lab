# Independent Fe-site observation review

2026-10-18. Scope: `documented-scaffold-2026-10-18/fe-site-observation/` native SI, source audit, frozen protocol, extraction code/pixels/points, model code, saved results, final `REPORT.md` and `negative_results.json`. No source or executor output was overwritten; only this review is authored by the reviewer.

**Source, extraction and numerical verdict: PASS for a bounded, uncertain figure-derived analysis.** No blocking numerical error identified. The nominal M0 reserved screen passes, M1 fails and neither result establishes new-material repair. The JPEG does not resolve seven independent cycle currents. Interval sensitivity changes conclusions, and even current plus a total accessible-Fe proxy does not identify atom origin under the admitted equal-coefficient alternatives.

**Final interpretation verdict: APPROVE.** The report accurately preserves calibration failure despite M0's nominal reserved success, M1's worse conditional prediction, extraction ambiguity and the limit of corner enumeration. One prose ambiguity was raised and corrected: both models constrain k to be nonnegative; M1 gamma is signed, not constrained positive. No scientific model, source point, grid or evaluator changed for this correction. The ledger parses with 12 unique negative-result IDs. The report's closing abstract-screened DOI10.1021/acscatal.6c01228 lead is outside this review and receives no acquisition or scientific validation here.

The report's post-hoc B4 interior example was independently checked with a read-only Python invocation: set only cycles4–7 to 35 mA/cm², assert each value lies in its recorded interval, and compute B4's three reserved residuals. Observable: all interval assertions pass and all residuals equal zero. Source points/results were unchanged. This deliberately hypothetical, correlation-unqualified example validly demonstrates why zero passing corners is not continuous-box rejection.

## Findings and scientific limits

1. Source identity is verified: SI DOI `10.1021/acscatal.2c03898.s001`, parent DOI `10.1021/acscatal.2c03898`; acquired PDF has 11 pages, 644,572 bytes, SHA256 `fa82d1784dbd4257238e31a3a907e1b7fbc07c0849b3be2663b6350c63d857ab`, deposited MD5 `873f9d0e1b058f7be27f508f518657c5`. Main-article access failure does not make this SI a complete main-paper methods record.
2. S8 explicitly describes repeated cycling from -0.4 to 1.6 V in 1 M KOH with 2 micromolar Fe3+. Current at 1.52 V is read directly from S8a; the green density symbols use S8d's left axis. Orange derived TOF bars are excluded. The SI's count formula uses electron count; for molar areal density the conversion is Faraday's constant, not elementary charge times moles. The implemented factor is **0.38594132848 mA per (nmol per second)**, equivalently mA·s/nmol. It is numerically correct.
3. The original S8 image is a 540×412 embedded JPEG at xref65 on PDF page9, with no page vector drawings. A lossless PNG and nearest-neighbor enlargement cannot restore missing trace information. The current legend provides seven labels but only four reliably separable color groups here. Pairs 1/2, 3/4 and 6/7 share intervals and nominal midpoints. The branch direction is not identified. These are explicitly uncertain manually selected envelopes, not seven resolved measurements or measurement confidence intervals.
4. The nominal M0 fit succeeds on reserved midpoint currents despite failing the operational screen during calibration. M1 lowers training SSE but extrapolates poorly. This is not evidence of changing-competence chemistry, and M0's apparent coefficient is not an independently measured single-site turnover. It combines baseline assumptions and a redox-accessibility proxy. All models depend on uncertain extraction; measured reserved Fe density is supplied as a conditional input, so no density dynamics are forecast.
5. Every corner of a 14-dimensional independent interval box was evaluated, but the box ignores shared-axis/color/branch correlations. Corner extrema are not global extrema over the continuous interior, probabilities, confidence levels, or a validated image likelihood. B4's zero passing corners does not prove that it fails every interior assignment. M0's nominal success is not robust evidence of its mechanistic truth.
6. The source's redox proxy and current can both increase through access to retained material or incorporation of new material. The finite-pool witness admits the same initial founder/new inventories and identical accessible counts/current with distinct origins. It is a structural counterexample, not evidence that either history occurred. Failure of a constant baseline is not a universal founder-activity bound; founders may change state.
7. Carbon black, Nafion and glassy carbon are components of the actual electrode. The source remains an assay/mechanism comparator, not an admitted inorganic system complement. No Fe-site coefficient transfers to the Ni-wire/felt, Mo34WV or PMo12 systems on this evidence. Scan rate, independent charge reintegration, background uncertainty, product/Faradaic efficiency and isotope-resolved function remain unresolved.

## Exact observed checks

Qualified binary: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`. All read-only numerical checks used `python3 -c` from repository root, importing modules without calling `main()`.

| Scenario | Invocation/method | Binary observable | Captured artifact |
| --- | --- | --- | --- |
| Source and raster identity | Recompute SHA256/MD5 and bytes; open with PyMuPDF; inspect page9 images/drawings; compare decoded pixmap to PNG pixel array | 11 pages; correct hashes/size; no vector drawings; xref65=540×412; identical decoded PNG pixels | This review, native PDF, `data/figS8_native.png` |
| Axis and interval conversion | Independent formulas `(152-y)*50/138` and `(381-y)*10/158`; independently map 1.52 V to x | All seven current/density intervals and midpoint values agree within 1e-12; target x=208.1 | This review, `data/figS8_points.json`, `data/point_provenance.csv` |
| Source-assignment surface | Opened `data/figS8_calibration.png` with `view_image`; read native SI S8 caption/methods | Green density markers separated from orange TOF; plausible branch/color intersections covered by deliberately broad envelopes; no precision inferred | Annotated/native PNGs and `EXTRACTION.md` |
| Fit/split/units/selfchecks | Import `test_models`, call `self_check`; reproduce nominal fits; independently calculate per-cycle predictions and metrics | Exit0; current factor correct; all nominal predictions exactly equal saved arrays; all metric/screens agree; changing reserved currents and reserved densities leaves fit unchanged | This review, `results/models.json` |
| Full corner test | Separate vectorized least-squares calculation over `itertools.product((0,1), repeat=14)`; code below | All16,384 corners reproduced; same pass counts and extrema within 4.44e-16 | This review, `models.json:digitization_corner_sensitivity` |
| Origin counterexample | Independently check accessible/inaccessible founder pools and accessible/liquid fresh pools | All pools nonnegative; founder total3 and fresh total2 conserved; summed counts/current identical | This review, `models.json:self_checks.origin_counterexample` |
| Final plot | Open `results/models.png` via `view_image` | Both observables, midpoint/extraction ranges, cycle4/5 split and all four model traces visible; plot labels deny experimental-CI interpretation | `results/models.png` |

Nominal reserved numerical outcomes reproduced:

| Model | RMSE (mA/cm²) | Normalized RMSE | Maximum fractional error | Screen |
| --- | ---: | ---: | ---: | --- |
| M0 | 1.4853502854 | 0.0393026519 | 0.0540203416 | PASS, midpoint only |
| M1 | 14.0316719063 | 0.3712807156 | 0.4381008816 | FAIL |
| B1 | 19.3631654079 | 0.5123530508 | 0.5277777778 | FAIL |
| B4 | 10.3926155864 | 0.2749905911 | 0.2962962963 | FAIL |

M0 training normalized RMSE is 0.13660868 and maximum fractional error 0.20086866; M1 training normalized RMSE is 0.10748482. Both fail the specified screen during calibration. M1's fitted gamma is -1.67628195, inside the fixed grid rather than a boundary; its near-optimal range is approximately [-1.83746, -1.51050]. Training uses cycles2–4 with shared cycle1 baseline; reserved cycles5–7 enter only conditional prediction/scoring. The code never uses the TOF bars as a response or to reconstruct current.

## Independent full-corner reproduction

The following program was executed with the qualified binary's `-c` argument (line breaks shown for readability). It uses a separate algebraic implementation of least squares and metrics, and does not call the implementation's `fit`, `predict`, `metrics` or `corner_sensitivity` functions:

```python
import pathlib, json, itertools, numpy as np
p = pathlib.Path('documented-scaffold-2026-10-18/fe-site-observation')
a = json.loads((p / 'results/models.json').read_text())
points = a['points']
bounds = np.array([x['n_interval_nmol_cm2'] for x in points] +
                  [x['j_interval_mA_cm2'] for x in points])
gamma = np.linspace(-np.log(10), np.log(10), 1001)
gamma[500] = 0
C = 4*96485.33212*1e-6
E = np.exp(gamma[:, None]*np.arange(1, 4)/3)
stats = {k: {'passes': 0, 'min': np.inf, 'max': 0.,
             'lo': np.full(3, np.inf), 'hi': np.full(3, -np.inf)}
         for k in ['M0', 'M1', 'B1', 'B4']}
for bits in itertools.product((0, 1), repeat=14):
    values = bounds[np.arange(14), bits]
    n, j = values[:7], values[7:]
    dn, dj = n[1:4]-n[0], j[1:4]-j[0]
    z = C*E*dn[None, :]
    denom = np.einsum('ij,ij->i', z, z)
    num = z@dj
    k = np.maximum(0, np.divide(num, denom, out=np.zeros(len(gamma)), where=denom > 0))
    residual = z*k[:, None]-dj
    sse = np.einsum('ij,ij->i', residual, residual)
    choices = {'M0': 500, 'M1': int(np.argmin(sse))}
    for name, st in stats.items():
        if name in choices:
            ix = choices[name]
            pred = j[0] + C*k[ix]*np.exp(gamma[ix]*np.arange(4, 7)/3)*(n[4:]-n[0])
        else:
            pred = np.full(3, j[0] if name == 'B1' else j[3])
        err = pred-j[4:]
        nr = np.linalg.norm(err)/np.linalg.norm(j[4:])
        frac = np.max(np.abs(err)/np.maximum(np.abs(j[4:]), .1))
        st['passes'] += int(nr <= .1 and frac <= .2)
        st['min'], st['max'] = min(st['min'], nr), max(st['max'], nr)
        st['lo'], st['hi'] = np.minimum(st['lo'], pred), np.maximum(st['hi'], pred)
maxdiff = 0
for name, st in stats.items():
    expected = a['digitization_corner_sensitivity']['models'][name]
    assert st['passes'] == expected['pass_corners']
    pairs = [(st['min'], expected['nRMSE_min']), (st['max'], expected['nRMSE_max']),
             (st['lo'], expected['prediction_min_mA_cm2']),
             (st['hi'], expected['prediction_max_mA_cm2'])]
    for x, y in pairs:
        maxdiff = max(maxdiff, float(np.max(np.abs(np.asarray(x)-y))))
        assert np.allclose(x, y, rtol=1e-12, atol=1e-12)
print(json.dumps({'corners_independently_recomputed': 16384,
    'passes': {k: v['passes'] for k, v in stats.items()},
    'max_summary_numeric_difference': maxdiff, 'not_interior_bound_or_probability': True}))
```

Observed exit0:

```json
{"corners_independently_recomputed": 16384, "passes": {"M0": 848, "M1": 554, "B1": 1024, "B4": 0}, "max_summary_numeric_difference": 4.440892098500626e-16, "not_interior_bound_or_probability": true}
```

M0 corner nRMSE spans approximately0.00731–2.34090; M1 approximately0.01442–16.88733. These ranges demonstrate dependence on unresolved extraction choices. They are not sampling probabilities or all-interior bounds.

## Reviewed artifact hashes

| Artifact | SHA256 |
| --- | --- |
| `PROTOCOL.md` | `5f819932b054e05c41de8187ac9ce856b516e21aaf859ef55cb3d07f62eb6e44` |
| `SOURCE_AUDIT.md` | `ae4eaa26c0c85054d310a0914567c917a37e07d96c9e61f29f906266d75951c0` |
| `EXTRACTION.md` | `90edd68105b85f2b2fd7b7aa34e0f54ed75e57dd2668107f9f3d014ce7c61538` |
| `extract_figS8.py` | `3dcdb54b559cdc562543583d46d18ad781741e4acfa7e8994c29e14397c3cd22` |
| `test_models.py` | `b1e8e883a344d7069fc0680dffcf21c8d13a5be5027cebe2675adc57d0c27167` |
| `data/figS8_points.json` | `e053118b06beeb20e045f0dbc533af8b8dc56ad78808d5dfb79d8777ec52e425` |
| `results/models.json` | `7b69af287c29c10eb6c749165ee90bc6a42e20c57f7e12eb9920e177640c6609` |
| `results/models.png` | `4434d479e7184216a4c21e8ba19642edae8431eb4fa17451cf4b1b1f64d92ac3` |
| `REPORT.md` | `1ae951d7a5c1f3a3d85e4be78823392cf938c1e861da16326ecfde1e845cebf1` |
| `negative_results.json` | `c799fe8f19c02cbf97efc9e977d8b349b6acc8e4d6452cc76a7710c6c7f4deaf` |

No new experimental data, source scan-rate/background reconstruction, raw-current replication, origin-specific function or noncarbon integrated system was validated. Main article access and the missing founder-function bound remain material limitations.
