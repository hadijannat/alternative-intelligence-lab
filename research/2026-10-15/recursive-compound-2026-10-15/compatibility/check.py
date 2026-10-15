from pathlib import Path
import csv,json,hashlib,statistics
p=Path(__file__).parent
rows=list(csv.DictReader((p/'selected_rows.csv').open()))
assert len(rows)==10
assert len({(r['species'],r['medium'],r['nominal_pH'],r['stage']) for r in rows})==10
rounding_discrepancies=[]
for r in rows:
 reps=[float(r[f'parent_rep{i}']) for i in (1,2,3)]
 if abs(statistics.mean(reps)-float(r['parent_reported_percent']))>.5:
  rounding_discrepancies.append({'species':r['species'],'medium':r['medium'],'stage':r['stage'],'replicate_mean':statistics.mean(reps),'source_mean':float(r['parent_reported_percent'])})
 assert 'free phosphate excluded' in r['denominator']
 if r['medium']=='sodium phosphate':
  assert reps==([0]*3 if r['species']=='PMo12' else [100]*3)
  if r['species']=='PMo12':assert sum(float(r[k]) for k in ['parent_reported_percent','P2Mo18_reported_percent','P2Mo5_or_PMo6_reported_percent'])==100
assert len(rounding_discrepancies)==1 and rounding_discrepancies[0]['medium']=='D2O' and rounding_discrepancies[0]['stage']=='after_24h_37C'
scope=json.loads((p/'atlas_scope.json').read_text())
assert len(scope['POMs'])==10 and not scope['target_tested'] and not scope['Mo36_tested']
assert sum(len(x['pH'])*len(x['concentration_M']) for x in scope['buffers'])==27
for s in json.loads((p/'sources.json').read_text()):
 for f,h in s['sha256'].items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h
assert (p/'raw/supplement.pdf').read_bytes().startswith(b'%PDF')
# Conditional fractions do not constrain recovered total signal: two recoveries share one fraction.
assert 76/100 == 7.6/10
changes={r['species']+'_'+r['nominal_pH']:round(float(r['measured_pH_mean'])-float(r['nominal_pH']),2) for r in rows if r['stage']=='initial' and r['medium']=='sodium phosphate'}
assert changes=={'PMo12_3':-1.03,'PMo12_4':-1.9,'alpha-P2W18_3':-.01,'alpha-P2W18_4':0}
out=p/'.omo/evidence';out.mkdir(parents=True,exist_ok=True)
result={'status':'PASS_DOSSIER_CHECKS_ONLY','rows':len(rows),'buffer_conditions':27,'nominal_to_initial_pH_change':changes,'conditional_fraction_example':{'parent_signal': [76,7.6],'assigned_total_signal':[100,10],'same_fraction':.76,'total_recovery_identified':False},'raw_NMR_reprocessed':False,'integrated_compatibility_verified':False,'target_verified':False,'source_hash_checks':'PASS','source_mean_discrepancy_preserved':rounding_discrepancies}
(out/'checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
