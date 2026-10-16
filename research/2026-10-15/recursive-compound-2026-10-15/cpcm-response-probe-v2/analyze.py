import hashlib
import json
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
RUN = BASE / 'run-v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((RUN / 'result.json').read_text())
supervisor = json.loads((RUN / 'supervisor.json').read_text())
checks = {row['name']: row for row in result['checks']}
assert len(checks) == len(result['checks']) == 60
assert result['status'] == 'PASS_RESPONSE_COMPONENT_ONLY'
assert all(row['pass'] is True for row in checks.values())
assert supervisor['returncode'] == 0
assert supervisor['termination_reason'] is supervisor['monitor_error'] is None
assert result['SCFs_launched'] == 0 and result['parent_run'] is False
assert result['physical_admission'] is False
assert result['runtime']['pyscf_threads'] == 1
assert result['runtime']['OMP_NUM_THREADS'] == '1'
assert (RUN / 'root-review.json').read_bytes() == (BASE / 'independent-root-review.json').read_bytes()
prepared = json.loads((BASE / 'preparation.json').read_text())
assert json.loads((RUN / 'pins.json').read_text()) == prepared['pins']
assert all(digest(Path(name)) == value for name, value in prepared['pins'].items())

expected_checks = {'actual_PySCF_threads_one', 'pins_unchanged'}
rows = []
with np.load(RUN / 'arrays.npz', allow_pickle=False) as arrays:
    assert len(arrays.files) == 93
    assert all(arrays[name].dtype == np.float64 and np.isfinite(arrays[name]).all()
               for name in arrays.files)
    assert arrays['P0'].shape == (87, 87)
    for eps in ('1.0', '78.4'):
        prefix = 'eps' + eps
        outputs = {}
        for direction in ('zero', 'positive', 'negative', 'mixed'):
            label = prefix + '/' + direction
            delta = arrays['delta/' + direction]
            actual = arrays[label + '/stock_B_dot_x/actual']
            reference = arrays[label + '/stock_B_dot_x/reference']
            assert delta.shape == actual.shape == reference.shape == (87, 87)
            assert np.array_equal(delta, delta.T)
            outputs[direction] = actual
            error = float(np.max(np.abs(actual - reference)))
            assert error == checks[label + '/stock_B_dot_x']['value'] and error <= 1e-10
            curvature = float(np.sum(delta * actual))
            assert curvature == checks[label + '/nonpositive_solvent_curvature']['value']
            assert curvature <= 1e-10
            expected_checks.update(label + '/' + name for name in
                                   ('stock_B_dot_x', 'input_unchanged', 'nonpositive_solvent_curvature'))
            row = {'epsilon': float(eps), 'direction': direction,
                   'stock_max_abs_error': error, 'curvature': curvature, 'finite_difference': {}}
            if eps == '1.0' or direction == 'zero':
                assert np.count_nonzero(actual) == 0 and curvature == 0
                expected_checks.update(label + '/' + name for name in ('exact_zero', 'exact_zero_curvature'))
            for h in (1e-3, 5e-4):
                fd_label = label + f'/FD_h{h}'
                fd = (arrays[label + f'/h{h}/plus'] - arrays[label + f'/h{h}/minus']) / (2*h)
                assert np.array_equal(fd, arrays[fd_label + '/reference'])
                assert np.array_equal(actual, arrays[fd_label + '/actual'])
                fd_error = float(np.max(np.abs(actual - fd)))
                assert fd_error == checks[fd_label]['value'] and fd_error <= 1e-8
                row['finite_difference'][str(h)] = fd_error
                expected_checks.add(fd_label)
            rows.append(row)
        linear_reference = outputs['positive'] - 2*outputs['mixed']
        assert np.array_equal(linear_reference, arrays[prefix + '/linearity/reference'])
        for name in ('linearity', 'reciprocity'):
            label = prefix + '/' + name
            error = float(np.max(np.abs(arrays[label + '/actual'] - arrays[label + '/reference'])))
            assert error == checks[label]['value'] and error <= 1e-10
        assert float(arrays[prefix + '/reciprocity/actual']) == float(np.sum(arrays['delta/positive'] * outputs['mixed']))
        assert float(arrays[prefix + '/reciprocity/reference']) == float(np.sum(arrays['delta/mixed'] * outputs['positive']))
        expected_checks.update(prefix + '/' + name for name in
                               ('linearity', 'reciprocity', 'cache_objects_bytes_unchanged', 'equilibrium_flag_false'))
assert expected_checks == set(checks)

summary = {
    'status': 'SAVED_ARRAY_COMPONENT_CHECKS_REPRODUCED',
    'checks': len(checks), 'arrays': 93, 'matching_preparation_pins': len(prepared['pins']),
    'max_stock_abs_error': max(row['stock_max_abs_error'] for row in rows),
    'max_fd_abs_error': max(value for row in rows for value in row['finite_difference'].values()),
    'max_linearity_abs_error': max(checks[f'eps{eps}/linearity']['value'] for eps in ('1.0', '78.4')),
    'max_reciprocity_abs_error': max(checks[f'eps{eps}/reciprocity']['value'] for eps in ('1.0', '78.4')),
    'wall_seconds': supervisor['wall_seconds'],
    'sampled_max_rss_bytes': supervisor['sampled_max_rss_bytes'],
    'rss_samples': len(supervisor['samples']),
    'rows': rows,
    'artifact_sha256': {str(path.relative_to(BASE)): digest(path) for path in
                       [BASE / 'preparation.json', BASE / 'independent-root-review.json',
                        BASE / 'launch-result.json', *sorted(RUN.iterdir())] if path.is_file()},
    'analysis_sha256': digest(Path(__file__)),
    'SCFs_launched': 0, 'held_out_validation': False, 'physical_admission': False,
    'scope': 'Retrospective fixed-geometry electronic solvent-response component only',
    'limits': ['Transient cache assertions are recorded harness observations, not reconstructed snapshots.',
               'Input checks used array_equal; no direct input flag/identity measurement.',
               'Stock oracle shares integral/runtime components; no independent physical accuracy claim.']
}
(BASE / 'analysis.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({key: value for key, value in summary.items()
                  if key not in ('rows', 'artifact_sha256', 'limits')}, indent=2))
