import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
import pyscf
from pyscf import gto

BASE=Path(__file__).resolve().parent
atoms={}
for element,spin in [('Mo',6),('W',6),('V',3),('O',2),('H',1)]:
    m=gto.M(atom=f'{element} 0 0 0',basis='def2-svp',ecp='def2-svp' if element in ('Mo','W') else {},spin=spin,verbose=0)
    aux=gto.basis.load('def2-universal-jkfit',element)
    naux=sum((2*shell[0]+1)*(len(shell[1])-1) for shell in aux)
    atoms[element]={'Z':gto.charge(element),'ecp_core':m.atom_nelec_core(0),'spherical_AOs':m.nao_nr(),'jkfit_spherical_AOs':naux}
models=[]
for name,composition,charge in [('parent',{'Mo':36,'O':128,'H':32},-8),('target_VV',{'Mo':34,'W':1,'V':1,'O':128,'H':32},-9),('target_one_electron_reduced',{'Mo':34,'W':1,'V':1,'O':128,'H':32},-10)]:
    ne=sum(atoms[e]['Z']*n for e,n in composition.items())-charge
    core=sum(atoms[e]['ecp_core']*n for e,n in composition.items())
    nao=sum(atoms[e]['spherical_AOs']*n for e,n in composition.items())
    naux=sum(atoms[e]['jkfit_spherical_AOs']*n for e,n in composition.items())
    pair=nao*(nao+1)//2
    models.append(dict(name=name,composition=composition,charge=charge,all_electron_count=ne,ecp_core_electrons=core,explicit_electrons=ne-core,electron_parity=(ne-core)%2,spherical_AOs=nao,jkfit_AOs=naux,
      storage_GiB={'one_dense_float64_AO_matrix':8*nao**2/2**30,'eightfold_packed_four_center_ERI':8*pair*(pair+1)//2/2**30,'full_three_center_pair_aux_float64':8*pair*naux/2**30},
      geometry_generated=False,scf_run=False))
assert [(m['all_electron_count'],m['explicit_electrons'],m['spherical_AOs']) for m in models]==[(2576,1568,3068),(2590,1578,3069),(2591,1579,3069)]
assert models[0]['charge']==36*6-112*2
assert models[1]['charge']==34*6+6+5-112*2
mapping=json.loads((BASE.parent/'site_mapping.json').read_text())
waters=[s for s in mapping if s['element']=='O' and int(s['label'][1:])>=57]
framework=[s for s in mapping if s['element']=='O' and int(s['label'][1:])<57]
pairs=[]
for w in waters:
    o=min(framework,key=lambda o:np.linalg.norm(np.array(w['cartesian_A'])-o['cartesian_A']))
    pairs.append({'donor':w['label']+'@'+str(w['symmetry_index']),'acceptor':o['label']+'@'+str(o['symmetry_index']),'distance_A':float(np.linalg.norm(np.array(w['cartesian_A'])-o['cartesian_A']))})
physical_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True))
out=dict(pyscf=pyscf.__version__,basis='def2-svp',aux_basis_for_storage_only='def2-universal-jkfit',atomic_builds=atoms,models=models,nearest_framework_O_candidates=sorted(pairs,key=lambda x:x['distance_A']),physical_memory_GiB=physical_bytes/2**30,logical_cpu_count=int(subprocess.check_output(['sysctl','-n','hw.logicalcpu'],text=True)),geometry_sha256=hashlib.sha256((BASE.parent/'site_mapping.json').read_bytes()).hexdigest(),notes=['AO sums use spherical basis functions and atomic builds, not a full cluster build.','Storage arithmetic is not actual peak memory or runtime; no timing extrapolation.','No geometry, integrals, SCF, gradients or optimization for any full cluster.'])
(BASE/'feasibility.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
