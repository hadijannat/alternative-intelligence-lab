"""One exact saved Coulomb request, then unchanged MemoryRI delegation."""
import hashlib
import json
from pathlib import Path
import types
import numpy as np


def sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def density_digest(density):
    digest=hashlib.sha256()
    for row in density:digest.update(np.ascontiguousarray(row).view(np.uint8))
    return digest.hexdigest()


def require(value,message):
    if not value:raise ValueError(message)


def verify_provenance(proof):
    for name in ('artifact','receipt','result'):
        require(sha(proof[name])==proof[name+'_sha256'],'Saved-J provenance digest changed: '+name)
    receipt=json.loads(Path(proof['receipt']).read_text());result=json.loads(Path(proof['result']).read_text())
    require(all(k in receipt for k in ('returncode','termination_reason','monitor_error'))
            and type(receipt['returncode']) is int and receipt['returncode']==0
            and receipt['termination_reason'] is None and receipt['monitor_error'] is None,'Saved-J receipt not accepted')
    checks=result.get('checks');checks=list(checks.values()) if isinstance(checks,dict) else [c.get('pass') for c in checks] if isinstance(checks,list) else []
    require(checks and all(v is True for v in checks) and type(result.get('SCFs_launched')) is int and result['SCFs_launched']==0,'Saved-J result not accepted')
    require(isinstance(proof.get('density_sha256'),str) and len(proof['density_sha256'])==64,'Missing exact density digest')
    if proof['j_key'] is None:
        require(result.get('status')=='PASS_BOUNDED_FIRST_J_ONLY' and result.get('J_sha256')==proof['artifact_sha256']
                and type(proof.get('density_cycle')) is int and proof['density_cycle']==0,'Parent first-J/density binding differs')
    else:
        require(proof.get('case')==result.get('case')=='new-external' and result.get('phase')=='operators'
                and result.get('status')=='PASS_OPERATORS' and proof.get('density_key')=='initial_P'
                and proof['j_key']=='initial_Jmemory','Small saved-J case/key binding differs')


def owns_storage(array):
    root=array
    while isinstance(root.base,np.ndarray):root=root.base
    return root.base is None and root.flags.owndata and not isinstance(root,np.memmap)


def load_verified(proof):
    verify_provenance(proof)
    loaded=np.load(proof['artifact'],allow_pickle=False)
    if isinstance(loaded,np.lib.npyio.NpzFile):
        try:saved=loaded[proof['j_key']]
        finally:loaded.close()
    else:
        require(proof['j_key'] is None,'Unexpected key for saved NPY');saved=loaded
    require(saved.dtype==np.float64 and saved.ndim==2 and saved.shape[0]==saved.shape[1]
            and np.isfinite(saved).all() and np.allclose(saved,saved.T,atol=1e-10,rtol=0),'Invalid saved J')
    require(owns_storage(saved) and saved.flags.writeable and not isinstance(saved,np.memmap),'Saved J must be an independent writable load')
    return saved


def install(mf,initial_density,proof):
    obj=mf._rij_df;mol=mf.mol
    require(obj.mol is mol and mf._rij_calls==0 and obj._vjopt is None,'Require fresh unchanged MemoryRI instance')
    require(not hasattr(mf,'saved_J_hits'),'Handoff already installed')
    require(mf.direct_scf and mf.direct_scf_tol==1e-13,'Qualified screening cutoff differs')
    require(initial_density.dtype==np.float64 and initial_density.shape==(mol.nao,mol.nao)
            and not initial_density.flags.writeable and np.isfinite(initial_density).all()
            and np.allclose(initial_density,initial_density.T,atol=1e-12,rtol=0),'Require immutable finite symmetric initial density')
    verify_provenance(proof)
    coordinates=mol.atom_coords().copy();basis=mol._bas.copy();environment=mol._env.copy()
    original=mf.get_jk;digest=density_digest(initial_density)
    require(digest==proof['density_sha256'],'Density differs from artifact-bound provenance')
    state={'density':initial_density,'proof':dict(proof)}
    mf.saved_J_hits=0;mf._saved_J_pending=True
    def get_jk(self,mol=None,dm=None,hermi=1,with_j=True,with_k=True,omega=None):
        require(self.direct_scf_tol==1e-13,'Qualified screening cutoff changed')
        if not self._saved_J_pending:return original(mol=mol,dm=dm,hermi=hermi,with_j=with_j,with_k=with_k,omega=omega)
        require((mol is None or mol is obj.mol) and self.mol is obj.mol,'Different molecule')
        require(with_j and not with_k and omega is None and hermi==1
                and self.xc.upper()=='PBE' and self.direct_scf and self.direct_scf_tol==1e-13
                and obj.auxbasis=='def2-universal-jkfit','Unsupported saved Coulomb request')
        require(np.array_equal(coordinates,obj.mol.atom_coords()) and np.array_equal(basis,obj.mol._bas)
                and np.array_equal(environment,obj.mol._env),'Molecule changed before saved J')
        require(self._rij_df is obj and self._rij_calls==0 and obj._vjopt is None
                and obj._cderi is None and obj._cderi_to_save is None,'Unexpected native metric/tensor state before saved J')
        reference=state['density'];request=np.asarray(dm) if dm is not None else None
        require(request is not None and request.dtype==np.float64 and request.shape==reference.shape
                and not reference.flags.writeable and density_digest(reference)==digest
                and np.array_equal(request,reference) and density_digest(request)==digest,'First density differs from frozen initial density')
        working=load_verified(state['proof']);require(working.shape==request.shape,'Saved J and density shapes differ')
        state.clear();reference=None;self.saved_J_hits=1;self._saved_J_pending=False
        return working,None
    mf.get_jk=types.MethodType(get_jk,mf)
    return mf
