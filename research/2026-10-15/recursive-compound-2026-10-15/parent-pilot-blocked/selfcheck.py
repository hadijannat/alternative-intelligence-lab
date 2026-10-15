"""No SCF: arithmetic, supervisor binding, hash pins and overwrite guard."""
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import pilot

checks=[]
def check(name,passed,value):
    checks.append({'scenario':name,'pass':bool(passed),'observable':value})
n,nao,natm=9284,3068,196
expected=3*8*n*n+8*128*n*8+n*n+8*nao*nao*8+32*nao*nao*8+natm*128*8+4*2**30
actual=pilot.allocation(n,nao,natm)
check('exact frozen allocation arithmetic',actual['screening_estimate_bytes']==expected,actual)
check('known upstream AO400 and replacement AO8',8*nao*nao*400==30120396800 and actual['terms_bytes']['AO_surface_tensor8']==602407936,{'AO400':8*nao*nao*400,'AO8':actual['terms_bytes']['AO_surface_tensor8']})
check('original supervisor same function object',pilot.monitored_run is pilot.original.monitored_run,str(pilot.monitored_run.__code__.co_filename))
check('same resource caps and requested threads',pilot.original.WALL_SECONDS==900 and pilot.original.RSS_BYTES==10*2**30 and set(pilot.original.THREADS.values())=={'1'},{'wall':pilot.original.WALL_SECONDS,'RSS':pilot.original.RSS_BYTES,'threads':pilot.original.THREADS})
pins=pilot.validate_pins()
check('all frozen source input protocol qualification pins verified',bool(pins),pins)
with tempfile.TemporaryDirectory() as tmp:
    rejected=False
    try: pilot.refuse_existing(Path(tmp))
    except RuntimeError: rejected=True
    check('existing run refused',rejected,str(Path(tmp)))
    pilot.refuse_existing(Path(tmp)/'fresh')
    check('fresh run accepted without creation',not (Path(tmp)/'fresh').exists(),True)
with patch.object(pilot,'sha',return_value='deliberately mismatched'):
    rejected=False
    try: pilot.validate_pins()
    except RuntimeError: rejected=True
    check('source hash mismatch fails closed',rejected,True)
check('no parent SCF artifact exists',not (pilot.BASE/'run-v1').exists(),True)
result={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','SCFs_launched':0,'checks':checks}
(pilot.BASE/'selfcheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['status']=='PASS'
