"""Evidence checks; no fitted target chemistry or synthetic learning trajectory."""
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '.omo/evidence'
OUT.mkdir(parents=True, exist_ok=True)
assert __debug__
results = {}
for key, relative in {
    'counterion': 'discovery-loop/experiments/manganese-mo36-counterion-transport-v1/runner.py',
    'wo3_capacity': 'discovery-loop/experiments/wo3-mn-ce-redox-capacity-v1/runner.py',
}.items():
    path = ROOT / relative
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, cwd=ROOT)
    (OUT / (key + '.stdout.json')).write_text(proc.stdout)
    (OUT / (key + '.stderr.txt')).write_text(proc.stderr or '(empty stderr)\n')
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    if key == 'counterion':
        assert data['checks']['case_count'] == 24
        assert data['checks']['voltage_decomposition_count'] == 72
        assert data['checks']['all_assertions_passed']
        observable = data['checks']
    else:
        assert data['totals']['initial_states'] == 63
        assert all(x['rejected'] for x in data['negative_controls'])
        assert not data['canonical_admission']
        observable = data['totals']
    results[key] = {'scenario': 'Replay existing conditional conservation model without editing it',
                    'invocation': [sys.executable, str(path)], 'exit_code': proc.returncode,
                    'observable': observable, 'artifact': str(OUT / (key+'.stdout.json')),
                    'code_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'physical_validation': False}
# Eq. 1 and coefficient are source-derived; these are model evaluations, not new measurements.
a = D('3.40e12')
tau = {str(g): str(a*g**4) for g in [D('.001'), D('.0035')]}
ratio = D(tau['0.0035']) / D(tau['0.001'])
assert tau == {'0.001': '3.40', '0.0035': '510.212500'}
assert ratio == D('150.0625')
# Deliberately wrong milliSiemens-to-Siemens input must differ by 10^12.
assert a*D('1')**4 / D(tau['0.001']) == D('1e12')
results['ag2s_power_law'] = {
    'scenario': 'Evaluate published Eq.1 at reported conductance endpoints; audit SI-unit conversion',
    'equation': 'tau_fac_s=3.40e12*(G_final_S**4)',
    'tau_s_by_conductance_S': tau, 'ratio': str(ratio),
    'wrong_mS_as_S_factor': '1000000000000',
    'observable': 'source-model arithmetic and unit negative control passed',
    'source': 'https://doi.org/10.1038/srep39216',
    'scope': 'Published fit evaluation only. Not a retention measurement or held-out model validation; model V1 misses paired-pulse potentiation.'}
results['dryad_replay'] = {'scenario': 'Download and replay public nonlinear analog learning measurements',
                          'observable': 'NOT_EXECUTED_DOWNLOAD_BLOCKED',
                          'artifact': str(BASE/'raw/acquisition.json'), 'success': False}
(OUT/'checks.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
