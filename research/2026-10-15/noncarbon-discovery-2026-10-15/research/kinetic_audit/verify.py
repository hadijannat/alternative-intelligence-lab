"""Independent arithmetic replay of saved Mo36 forecasts; no fitting or new rates."""
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAL = ROOT / 'metal-oxide/published/calibration'
SOURCE = HERE.parent / 'pom/raw/mo36_seed_timeseries.csv'


def rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a, b, absolute=1e-16):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=absolute), (a, b)


def prediction(fit, time):
    p = fit['parameters']
    x = (time - fit['time_origin']) / fit['time_scale']
    model = fit['model']
    if model == 'last_value':
        return p['held_value']
    if model == 'linear_last10':
        return p['intercept_at_training_origin'] + p['slope_per_training_span'] * x
    if model == 'single_relaxation':
        return p['offset'] + p['amplitude'] * -math.expm1(-p['relaxation_shape'] * x)
    if model == 'double_relaxation':
        return (p['offset'] + p['slow_amplitude'] * -math.expm1(-p['slow_shape'] * x)
                + p['fast_amplitude'] * -math.expm1(-p['fast_shape'] * x))
    assert model == 'offset_logistic'
    z = p['steepness'] * (x - p['midpoint'])
    sigmoid = 1 / (1 + math.exp(-z)) if z >= 0 else math.exp(z) / (1 + math.exp(z))
    return p['offset'] + p['amplitude'] * sigmoid


def main():
    manifest = json.loads((CAL / 'results/manifest.json').read_text())
    for path, expected in manifest['sha256'].items():
        assert sha(CAL / path) == expected, path
    assert sha(SOURCE) == 'b9cfcb759f2140d61a7b21a984f3c5c761958d7d93ac9c815289596fae4520a7'
    source = rows(SOURCE)
    extracted = rows(CAL.parent / 'mo36-observations.csv')
    assert len(source) == len(extracted) == 480
    series = defaultdict(list)
    for original, local in zip(source, extracted):
        assert original['Exp'] == local['condition']
        for a, b in [('Time', 'source_time'), ('Concentration', 'source_concentration'), ('seed_value', 'source_seed_value')]:
            assert float(original[a]) == float(local[b])
        series[original['Exp']].append(original)
    assert all(len(points) == 80 for points in series.values()) and len(series) == 6
    assert all(float(row['seed_value']) > 0 for row in source)
    fits = json.loads((CAL / 'results/fits.json').read_text())
    points = rows(CAL / 'results/predictions.csv')
    metrics = rows(CAL / 'results/metrics.csv')
    key = lambda r: (r['condition'], r['split'], r['model'], r['bounds'])
    fitted = {key(f): f for f in fits}
    metric_map = {key(m): m for m in metrics}
    assert len(fitted) == len(metric_map) == len(fits) == 96
    assert len(points) == 7680
    residuals = defaultdict(lambda: {'train': [], 'heldout': []})
    max_difference = 0.
    for point in points:
        fit = fitted[key(point)]
        index = int(point['point_index']) - 1
        original = series[point['condition']][index]
        assert float(point['source_time']) == float(original['Time'])
        assert float(point['observed_native']) == float(original['Concentration'])
        expected_phase = 'train' if index < fit['train_count'] else 'heldout'
        assert point['phase'] == expected_phase
        expected = prediction(fit, float(point['source_time']))
        max_difference = max(max_difference, abs(expected - float(point['predicted_native'])))
        close(expected, float(point['predicted_native']))
        error = expected - float(original['Concentration'])
        close(error, float(point['residual_native']))
        residuals[key(point)][expected_phase].append(error)
    means = defaultdict(list)
    for fit in fits:
        n = {'primary': 40, 'stress': 20}[fit['split']]
        assert fit['train_count'] == n
        own_source = series[fit['condition']]
        assert fit['time_origin'] == float(own_source[0]['Time'])
        assert fit['time_scale'] == float(own_source[n - 1]['Time']) - float(own_source[0]['Time'])
        own = residuals[key(fit)]
        assert len(own['train']) == n and len(own['heldout']) == 80 - n
        errors = own['heldout']
        recomputed = {'train_sse': sum(e * e for e in own['train']),
                      'heldout_mae': sum(map(abs, errors)) / len(errors),
                      'heldout_rmse': math.sqrt(sum(e * e for e in errors) / len(errors)),
                      'heldout_bias': sum(errors) / len(errors)}
        for name, value in recomputed.items():
            close(value, fit[name], 1e-22 if name == 'train_sse' else 1e-16)
            close(value, float(metric_map[key(fit)][name]), 1e-22 if name == 'train_sse' else 1e-16)
        if fit['starts']:
            selected = min((s for s in fit['starts'] if s['status'] == 'success'), key=lambda s: (s['train_sse'], s['index']))
            assert selected['index'] == fit['selected_start']
            assert selected['parameters'] == fit['parameters']
        if fit['bounds'] == 'main':
            means[fit['split'] + '/' + fit['model']].append(recomputed['heldout_mae'])
    result = {
        'status': 'PASS independent source and saved-formula replay; no new fitting',
        'source_rows': 480, 'seed_settings': sorted({float(r['seed_value']) for r in source}),
        'unseeded_rows': 0, 'stored_manifest_hashes_verified': len(manifest['sha256']),
        'fit_records': len(fits), 'prediction_rows': len(points),
        'optimizer_start_records': sum(len(f['starts']) for f in fits),
        'optimizer_start_status_counts': dict(Counter(s['status'] for f in fits for s in f['starts'])),
        'max_saved_formula_difference_native_units': max_difference,
        'mean_heldout_mae_native_units': {k: sum(v) / len(v) for k, v in sorted(means.items())},
        'double_relaxation_main_fast_shape_upper_hits': sum(f['model'] == 'double_relaxation' and f['bounds'] == 'main' and 'fast_shape:upper' in f['boundary_flags'] for f in fits),
        'offset_logistic_offset_lower_hits': sum(f['model'] == 'offset_logistic' and 'offset:lower' in f['boundary_flags'] for f in fits),
        'inputs_sha256': {str(p.relative_to(ROOT)): sha(p) for p in [SOURCE, CAL / 'results/manifest.json', CAL / 'results/fits.json', CAL / 'results/predictions.csv', CAL / 'results/metrics.csv']},
        'verification_script_sha256': sha(Path(__file__)),
        'limits': ['Numerical replay is not optimizer refitting or experimental replication.',
                   'Chronological holdouts are within previously available seeded traces, not new batches or doses.',
                   'No verified physical units, zero-seed control, functional descendants or derivative rates are present.']
    }
    (HERE / 'checks.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
