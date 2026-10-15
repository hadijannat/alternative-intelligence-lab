import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parent
source=(B/'derivative.py').read_text()
old="gradient=mf.nuc_grad_method().kernel().tolist() if case=='analytic' else None"
new="grad_obj=mf.nuc_grad_method(); grad_obj.grid_response=True\n    gradient=grad_obj.kernel().tolist()"
assert source.count(old)==1
modified=source.replace(old,new).replace("f'derivative-{case}","f'grid-response-{case}")
namespace={'__file__':str(B/'derivative.py'),'__name__':'grid_response_worker'}
exec(compile(modified,str(B/'derivative.py'),'exec'),namespace)
namespace['worker']('analytic')
row=json.loads((B/'.omo/evidence/grid-response-analytic.json').read_text())
prior=json.loads((B/'derivative-result.json').read_text())
analytic=row['gradient_Eh_per_bohr'][1][0]
checks=[]
for c in prior['checks']:
    delta=abs(analytic-c['central_difference_Eh_per_bohr'])
    checks.append(dict(h_bohr=c['h_bohr'],analytic_Eh_per_bohr=analytic,central_difference_Eh_per_bohr=c['central_difference_Eh_per_bohr'],absolute_discrepancy=delta,pass_threshold=delta<=prior['threshold_Eh_per_bohr']))
out=dict(change='Only analytic nuclear gradient grid_response=True; original driver settings reused verbatim',source_derivative_sha256=hashlib.sha256(source.encode()).hexdigest(),threshold_Eh_per_bohr=prior['threshold_Eh_per_bohr'],checks=checks,pass_all=all(c['pass_threshold'] for c in checks),original_failure_preserved=not prior['pass_all'],parent_input_admitted=False)
(B/'grid-response-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['pass_all'],'Grid response diagnostic still fails; stop without tuning'
