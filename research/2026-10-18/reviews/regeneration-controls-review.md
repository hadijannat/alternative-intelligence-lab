# Independent regeneration-controls review

Decision: **APPROVE the bounded negative experiment and its numerical evidence.** No blocking numerical or source-interpretation defect remains in the reviewed artifacts. This does not validate active new-material repair, resolve atom origin, establish functional inheritance, or validate an integrated life candidate.

Reviewed 2026-10-18, independently of the implementation agent. Scope: `documented-scaffold-2026-10-18/regeneration-controls/` protocol, amendment, inventory, source audit, extraction/model code, native inputs, saved numerical results, extraction notes, forecast figure, final `REPORT.md` and `negative_results.json`. Parent checks may still be edited; this decision attaches to the exact scientific artifacts below. Native sources and executor outputs were read without overwriting them. Python imports created ordinary bytecode caches only.

## Findings and limits

1. Both M0 and M1 pass 4 of 10 reserved screens at every prescribed slope; six fail. The flat baseline passes 7 of 10. Consequently this experiment does not establish improved predictive performance from the proposed restoration model. WNi99T's M1 improvement over M0 is small and its flat-baseline RMSE is lower still. Negative early voltage changes cannot be represented by the anchored `x <= 1` law; WNi78T makes this limitation particularly visible. The resulting failure is retained rather than accommodated by a post-outcome parameter change.
2. Voltage alone does not identify the old/new atom contribution under the admitted model alternatives. The finite-pool witness has identical initial inventories and conserves each origin while producing effectively identical voltage with substantially different active origins. This is a conditional non-identifiability counterexample, not experimental evidence that the proposed replacement mechanism occurs. The scalar voltage law also leaves resistance, bubbles, morphology and surface accessibility unresolved.
3. The source supports nominal metal-supply/pulse-policy comparisons at figure level. Exact six-specimen Fe-dose assignments remain unresolved at the native-file level. All 36 cross-panel assignments remain admissible; no outcome-based assignment or fit-derived dose inference was made. The model fits each specimen separately and therefore does not establish quantitative Fe-supply response rates.
4. This is a paper-informed retrospective within-specimen extrapolation. It is not blinded, independent-specimen validation or randomized intervention evidence. All specimens have only 14 training interval summaries. Several optimum parameters are at grid boundaries or have large near-optimal sets. Positive fitted restoration with negligible initial gain is not proof of repair.
5. The WNi225T-A processed export has 603 unsupported tail rows, including 12 missing voltage fields. Those rows are excluded from fitting and forecasting. The separate WNi78T 24 h followup has an unknown intervening gap/EIS and is not used as causal pulse-withdrawal validation. Unknown inter-block wall time is reported, not assigned an invented chemical phase.

A small inventory wording issue was raised and corrected: WNi78T's last regeneration record contains only 6 s despite its nominal 100 s setting. The frozen amendment and extraction already used the observed duration. No scientific threshold, grid, split or model equation changed to obtain approval.

The final report's interpretation is approved: it reports the flat baseline's advantage, calibration failures, all forecast failures, unresolved supply assignments, missing native rows, same-initial-inventory counterexample and attribution limits. The negative-results ledger parses successfully and retains 12 unique negative IDs. No statement in those reviewed documents promotes a model screen or isotope-free voltage fit into measured new-material function.

## Independently observed evidence

Qualified binary: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`.

| Scenario | Invocation / method | Binary observable | Captured artifact |
| --- | --- | --- | --- |
| Complete acquired-byte coverage | Python `-c`, joined receipt entries by deposit file ID; recomputed deposited checksum and SHA256 from every local byte array | 481 entries, 55,239,493 bytes, zero mismatches; 494 tables, zero width/count mismatches | This review and `file_manifest.json` |
| Source/control interpretation | Read acquired article Methods/Results and SI S19/S20/Table S1; compare `SOURCE_AUDIT.md` | 57 mA / 0.19 cm² and 76 mA / 0.095 cm² are separate cases; 36 mL anode bath; no origin-specific functional bound | This review and `SOURCE_AUDIT.md` |
| Independent interval reduction | Python `-c`, independently split native table lines and recomputed window medians; did not call the implementation's aggregate function | All 420 summaries over 217 native OER files match exactly, including median time, voltage, current, row count, anchors and interval-end split | This review and `results/analysis.json` |
| Full extraction and model selfchecks | Import `analyze`; call `extract`, `selfchecks`, `origin_counterexample` without `main` | Exit 0; all saved summaries, events, native metadata, provenance and followups reproduced; selfchecks pass | This review and `results/analysis.json` |
| Frozen fit and forecast reproduction | Python `-c` code below; refit all 60 cases using only training arrays, independently implement phase recursion/observation | Exit 0; all parameter diagnostics equal saved values; maximum prediction discrepancy 2.3592239273284576e-16 V; all screens reproduced | This review and `results/analysis.json` |
| Origin inventory/observation check | Independently sum each saved origin's three pools after each cycle; compare outputs | Minimum pools nonnegative; maximum origin conservation error 1.7763568394002505e-15; maximum output difference 1.734723475976807e-17 V | This review and `analysis.json:origin_counterexample` |
| Unsupported processed tail | Independently split native processed text; count lines and blank second fields | 8,643 processed vs 8,040 native paired rows; 603 unsupported; missing lines 8239–8242, 8440–8443, 8641–8644 | This review and `analysis.json:processed_raw_provenance` |
| Figure surface | Opened `results/forecasts.png` using `view_image` | Ten readable specimen panels; training/reserved distinction and 24 h cutoff visible; no Fe-dose relabelling; negative observations/failures remain visible | `results/forecasts.png` |

The source's S20 high-to-low Fe wording describes cleaning between experiments, not a matched founder supply-withdrawal experiment. S19 is sequential Zn then Fe addition on one wire; it lacks an old/new functional attribution assay. Separate destructively sampled SIMS wires and bulk pristine-wire ICP do not supply a founder catalytic upper bound.

Primary b = 0.040 V reproduced reserved outcomes:

| Specimen | M0 RMSE (V) | M1 RMSE (V) | M1 maximum error (V) | Screen |
| --- | ---: | ---: | ---: | --- |
| WNi175T-A | 0.087158 | 0.087158 | 0.105571 | FAIL |
| WNi176T-A | 0.092350 | 0.092350 | 0.122842 | FAIL |
| WNi194T-A | 0.028475 | 0.028475 | 0.051594 | PASS |
| WNi197T-A | 0.015188 | 0.015188 | 0.022088 | PASS |
| WNi198T-A | 0.010425 | 0.010425 | 0.021121 | PASS |
| WNi214T-A | 0.254132 | 0.254132 | 0.491818 | FAIL |
| WNi225T-A | 0.177812 | 0.177812 | 0.661980 | FAIL |
| WNi78T | 0.215147 | 0.215147 | 0.227715 | FAIL |
| WNi79T | 0.064231 | 0.064231 | 0.109327 | FAIL |
| WNi99T | 0.016452 | 0.012370 | 0.025416 | PASS |

## Reproduction invocation captured during review

Working directory was repository root. The following Python program was executed through the qualified binary's `-c` argument, with literal newlines. It imports pure functions only and writes no results:

```python
import sys, pathlib, json, numpy as np
p = pathlib.Path('documented-scaffold-2026-10-18/regeneration-controls')
sys.path.insert(0, str(p))
import analyze as a
z = json.loads((p / 'results/analysis.json').read_text())
runs = {r['specimen']: r for r in z['runs']}
maximum, counts = 0., {}
for f in z['fits']:
    r = runs[f['specimen']]
    t = np.array([v['oer_h'] for v in r['summaries']])
    y = np.array([v['delta_voltage_V'] for v in r['summaries']])
    tr = np.array([v['split'] == 'training' for v in r['summaries']])
    new = a.fit(t[tr], y[tr], r['anchor_oer_h'], r['pulse_events'],
                f['b_V'], f['model'] == 'M1' and r['pulse_run'])
    assert new == f['parameters']
    ps, pred = f['parameters'], []
    for end in t:
        state, last = 1., r['anchor_oer_h']
        for e in r['pulse_events']:
            if last <= e['oer_h'] <= end:
                state *= np.exp(-ps['d_per_h'] * (e['oer_h'] - last))
                state += (1 - state) * (-np.expm1(-ps['r_per_h'] * e['duration_h']))
                last = e['oer_h']
        state *= np.exp(-ps['d_per_h'] * (end - last))
        assert 0 <= state <= 1
        pred.append(f['b_V'] * np.log((1 + ps['g']) / (1 + ps['g'] * state)))
    pred = np.array(pred)
    maximum = max(maximum, float(abs(pred - f['predicted_delta_V']).max()))
    assert np.allclose(pred, f['predicted_delta_V'], atol=1e-12, rtol=0)
    for name, mask in [('training', tr), ('reserved', ~tr)]:
        err = pred[mask] - y[mask]
        rmse, mx = float(np.sqrt(np.dot(err, err) / len(err))), float(abs(err).max())
        assert abs(rmse - f[name]['RMSE_V']) < 1e-12
        assert abs(mx - f[name]['max_abs_error_V']) < 1e-12
        assert (rmse <= .05 and mx <= .1) == f[name]['screen_pass']
    key = str(f['b_V']) + '/' + f['model']
    counts[key] = counts.get(key, 0) + int(f['reserved']['screen_pass'])
for b in [.04, .02, .08]:
    for r in runs.values():
        fs = [f for f in z['fits'] if f['specimen'] == r['specimen'] and f['b_V'] == b]
        assert fs[1]['parameters']['training_SSE'] <= fs[0]['parameters']['training_SSE'] + 1e-12
cons, output = 0., 0.
for x in z['origin_counterexample']['history']:
    for key in ['retention_pools', 'replacement_pools']:
        v = np.array(x[key])
        assert v.min() >= 0
        cons = max(cons, float(abs(v.sum(axis=1) - [1, 10]).max()))
    output = max(output, abs(x['retention_delta_V'] - x['replacement_delta_V']))
print(json.dumps({'fit_reproductions': len(z['fits']),
    'independent_prediction_max_error_V': maximum, 'pass_counts_of_10': counts,
    'origin_conservation_max_error': cons, 'origin_voltage_max_difference_V': output,
    'reserved_not_passed_to_fit': True}))
```

Observed exit 0. Output:

```json
{"fit_reproductions": 60, "independent_prediction_max_error_V": 2.3592239273284576e-16, "pass_counts_of_10": {"0.04/M0": 4, "0.04/M1": 4, "0.02/M0": 4, "0.02/M1": 4, "0.08/M0": 4, "0.08/M1": 4}, "origin_conservation_max_error": 1.7763568394002505e-15, "origin_voltage_max_difference_V": 1.734723475976807e-17, "reserved_not_passed_to_fit": true}
```

The separate aggregation/extraction invocation also exited 0 and produced:

```json
{"independent_interval_medians": 420, "runs": 10, "native_oer_files": 217, "all_saved_anchors_splits_match": true, "all_four_provenance_hashes_match": true, "selfchecks_and_origin_counterexample": "PASS", "extraction_reproduced": true}
```

Source code inspection verifies that only `times[train]` and `y[train]` enter every `fit` call. The fixed future pulse schedule is an input, not a reserved response. The observed current-deviation diagnostic is at most 0.00014735446115632378 relative to each record median after time zero. Unknown wall gaps and time-zero currents remain explicitly recorded.

## Exact reviewed artifact hashes

| Artifact | SHA256 |
| --- | --- |
| `analyze.py` | `18c09948d5adfb1da9b4c9ff82c16492f38f673534428d4be0d4c13ae7e59450` |
| `results/analysis.json` | `c9f3a2a18fed457d8842318c10d43c1557d21e34fe7f7bb092842351a695412c` |
| `results/forecasts.png` | `bac789256c144b100df899aaaa3f4eb4635a0972e8f9a56a9c79db0e552ded3f` |
| `PROTOCOL.md` | `ebc997e3afc8f248c7bae8cfb8b70ed3c9b501f56550cbefe6ea3f0c3892275d` |
| `AMENDMENTS.md` | `566604bb0067a4bdfc388a42a1614eb44381803305a1d3af85dda90dc6ccdd33` |
| `file_manifest.json` | `c576a995d383506f4fae32aadcaaf07bcc11bb9a63951dac51e9b587bc677358` |
| `REPORT.md` | `a3542136d70b41c1259f431222823119de281bcc2b2cd4403407ffea9d9aec33` |
| `negative_results.json` | `5579fa4adcdd1c696b96e3e5084c56fcc46feb8a82c17618ad72ab4b13c4c1e9` |

No wet-lab work, new origin-specific functional assay, supported Origin binary plot decoder, or independent-specimen replication was performed. Those missing measurements limit causal attribution; they do not erase the executed model failures or byte-level reproducibility.
