"""Reproduce descriptive arithmetic from ja900023k SI prose; no digitization or fit."""
import hashlib, json
from pathlib import Path
p = Path(__file__).resolve().parent
meta = json.loads((p/'raw/figshare-2869057.json').read_text())
f = meta['files'][0]
b = (p/'raw'/f['name']).read_bytes()
assert len(b) == f['size'] == 294449
assert hashlib.md5(b).hexdigest() == f['computed_md5']
assert meta['resource_doi'] == '10.1021/ja900023k'
assert b.startswith(b'%PDF')
result = {
 'source': 'ja900023k_si_001.pdf pp S4,S7-S8',
 'CoPi_open_circuit_30h': {'reported_leached_percent_two_runs':[1.6,1.3], 'complement_percent':[100-1.6,100-1.3], 'interpretation':'98.4 and 98.7% original label not accounted as leached; not intact founder organization or new-active-material fraction'},
 'CoX_open_circuit_phosphate_rescue_5h': {'approx_start_percent':0.25,'approx_end_percent':0.05,'approx_drop_percentage_points':round(0.25-0.05,2),'approx_relative_pool_drop':(0.25-0.05)/0.25,'interpretation':'about 80% decline of small dissolved founder-derived label pool; no fitted kinetic constant'},
 'newly_competent_activity':{'positive_lower_bound_identified':False,'trivial_nonnegative_lower_bound':0,'upper_bound':None,'reason':'No separate new-material activity and no founder-specific maximum activity supplied'},
 'uncertainty': {'source_CPM_two_standard_deviations':'<5%','source_between_run_estimate':'~20%','derived_confidence_interval':None},
 'status':'INSUFFICIENT_EVIDENCE_FOR_ISOTOPE_RESOLVED_NEWLY_COMPETENT_ACTIVITY'
}
assert abs(result['CoX_open_circuit_phosphate_rescue_5h']['approx_relative_pool_drop']-.8)<1e-12
assert result['CoPi_open_circuit_30h']['complement_percent']==[98.4,98.7]
(p/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':'PASS','si_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'result':result},indent=2))
