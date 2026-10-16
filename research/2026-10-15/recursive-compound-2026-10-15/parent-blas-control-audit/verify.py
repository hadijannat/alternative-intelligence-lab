from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
observed = json.loads((base / 'observed.json').read_text())
supervisor = json.loads((base / 'supervisor.json').read_text())
assert supervisor['returncode'] == 0 and supervisor['limit_hit'] is None
assert supervisor['wall_seconds'] < 30 and supervisor['sampled_peak_rss_bytes'] < 1024 ** 3
assert supervisor['rss_samples'] > 0
for name, expected in supervisor['artifacts'].items():
    assert hashlib.sha256((base / name).read_bytes()).hexdigest() == expected
for folder in ('failed-v1', 'failed-v2'):
    receipt = json.loads((base / folder / 'supervisor.json').read_text())
    assert receipt['returncode'] == 1
    for name, expected in receipt['artifacts'].items():
        assert hashlib.sha256((base / folder / name).read_bytes()).hexdigest() == expected
assert observed['same_dpotrf_symbol'] and observed['flapack_dpotrf_symbol_matches_blas']
assert observed['completed'] and observed['environment_unchanged'] and observed['intentional_exception_observed']
assert observed['threadpoolctl_probe']['exception'] == 'ModuleNotFoundError'
states = {s['label']: (s['blas'], s['pyscf']) for s in observed['states']}
assert states['initial'] == states['restored_after_exception'] == (4, 4)
assert states['explicit_blas_one_before'] == states['explicit_blas_one_after'] == (1, 4)
assert states['pyscf_context_before_explicit_setter_before'] == (4, 1)
assert states['pyscf_context_after_explicit_setter_before'] == (1, 1)
lower = [[F(x) for x in row] for row in [[2, 0, 0, 0], [1, 2, 0, 0], [-1, .5, 2, 0], [.5, -.5, 1, 2]]]
matrix = [[sum(lower[i][k] * lower[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
assert all(lower[i][i] > 0 for i in range(4))
assert len(observed['solves']) == 5
for solve in observed['solves']:
    assert [[F(x) for x in row] for row in solve['matrix']] == matrix
    actual = [F(x) for x in solve['answer']]
    assert actual == [F(x) for x in solve['expected']]
    assert [sum(matrix[i][j] * actual[j] for j in range(4)) for i in range(4)] == [F(x) for x in solve['rhs']]
    assert solve['residual_max_abs'] == solve['error_max_abs'] == 0
receipt = {'status': 'PASS_TINY_CONTROL_PROBE_ONLY', 'native_solves_verified': 5,
           'failed_setup_attempts_preserved': 2, 'verification': 'exact Fraction arithmetic and frozen file hashes',
           'sha256': {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted(base.rglob('*')) if p.is_file() and p.name != 'verification.json'}}
(base / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'sha256'}))
