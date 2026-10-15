import json
from pathlib import Path

B=Path(__file__).resolve().parent
r=json.loads((B/'result.json').read_text());d=json.loads((B/'derivative-result.json').read_text());g=json.loads((B/'grid-response-result.json').read_text())
assert r['status']=='PASS_RUNTIME_ONLY' and not r['parent_input_admitted']
for row in r['results'].values():
    assert row['converged'] and row['orbital_gradient_norm']<1e-5
    assert row['effective_nuclear_charge_sum']-row['explicit_electrons']==row['charge']
    assert abs(row['electron_trace']-row['explicit_electrons'])<1e-6
    assert not row['cached_four_center_ERI'] and row['direct_optimizer_created']
assert abs(r['results']['anion-gas']['energy_Eh']-r['results']['anion-eps1']['energy_Eh'])<1e-8
assert r['results']['anion-eps1']['PCM']['electrostatic_energy_Eh']==0
assert not d['pass_all'] and g['pass_all'] and g['original_failure_preserved']
assert d['threshold_Eh_per_bohr']==g['threshold_Eh_per_bohr']==1e-4
for failed,passed in zip(d['checks'],g['checks']):
    assert failed['absolute_discrepancy']>1e-4 and passed['absolute_discrepancy']<=1e-4
    assert failed['central_difference_Eh_per_bohr']==passed['central_difference_Eh_per_bohr']
    assert failed['h_bohr']==passed['h_bohr']
for name in ('attempt1/receipts.json','attempt2/receipts.json'):
    assert (B/'.omo/evidence'/name).stat().st_size>40
assert all(rec['returncode']==0 for rec in json.loads((B/'.omo/evidence/derivative-receipts.json').read_text()))
assert json.loads((B/'.omo/evidence/grid-response-receipt.json').read_text())['returncode']==0
assert not g['parent_input_admitted']
print('PASS artifact audit: four converged direct-PBE/PCM/ECP controls; correct charge/electron trace; epsilon1 equals vacuum; original derivative FAIL preserved; grid_response=True PASS unchanged 1e-4 threshold at both steps. Parent input remains unadmitted; no parent calculation.')
