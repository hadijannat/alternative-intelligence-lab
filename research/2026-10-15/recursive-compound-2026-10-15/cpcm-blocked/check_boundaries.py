"""Non-SCF trust-boundary and factorization-failure checks."""
import json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from pyscf import dft, gto, scf
from blocked_pcm import BlockedPCM, attach

base=Path(__file__).resolve().parent
mol=gto.M(atom='He 0 0 0',basis='sto-3g',verbose=0)
s=BlockedPCM(mol); s.lebedev_order=17
checks=[]
def rejects(name, function, exception):
    try:
        function()
    except exception as e:
        checks.append({'scenario':name,'pass':True,'exception':type(e).__name__,'message':str(e)})
    else:
        checks.append({'scenario':name,'pass':False})
for factory in (scf.RHF,dft.UKS):
    rejects(factory.__name__+' attach rejected',lambda:attach(factory(mol),s),NotImplementedError)
for name,dm in [('complex',np.ones((1,1),complex)),('batch',np.ones((2,1,1))),('nonfinite',np.full((1,1),np.nan))]:
    rejects(name+' density rejected',lambda:s._get_vind(dm),ValueError)
s.build()
from pyscf.solvent import pcm
bad={k:(v.copy() if isinstance(v,np.ndarray) else v) for k,v in s.surface.items()}
bad['switch_fun'] *= -1
with patch.object(pcm,'gen_surface',return_value=bad):
    rejects('non-positive-definite S fails without fallback',s.build,np.linalg.LinAlgError)
checks.append({'scenario':'failed build leaves no factor','pass':s._intermediates is None})
mf=attach(dft.RKS(mol),s)
s.build(); s.e=1.; s.v=np.ones((1,1)); s._dm=np.ones((1,1))
mf.reset(mol)
checks.append({'scenario':'attached RKS reset invalidates all solvent caches','pass':s._intermediates is None and s.surface is None and s.v_grids_n is None and s.e is None and s.v is None and s._dm is None})
result={'checks':checks,'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','SCFs_launched':0}
(base/'evidence/boundaries.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['status']=='PASS'
