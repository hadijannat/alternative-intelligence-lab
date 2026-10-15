import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parent
ENV={k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}


def worker(case):
    import inspect
    import types
    import numpy as np
    import pyscf
    from pyscf import dft,gto,solvent
    from pyscf.scf import hf
    from pyscf.solvent import pcm
    start=time.monotonic()
    if case.startswith('anion'):
        coords=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],float)*1.75/np.sqrt(3)
        charge=-2
    else:
        angles=np.array([0,120,240])*np.pi/180
        coords=np.column_stack([1.75*np.cos(angles),1.75*np.sin(angles),np.zeros(3)])
        charge=0
    atoms=[('Mo',(0,0,0))]+[('O',tuple(p)) for p in coords]
    mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=charge,spin=0,verbose=4,max_memory=512,output=str(BASE/'.omo/evidence'/f'{case}.scf.log'))
    mf=dft.RKS(mol)
    mf.xc='PBE'
    mf.grids.level=2
    mf.conv_tol=1e-9
    mf.conv_tol_grad=1e-5
    mf.max_cycle=60
    mf.direct_scf=True
    mf.chkfile=None
    if not case.endswith('gas'):
        mf=solvent.PCM(mf)
        mf.with_solvent.method='C-PCM'
        mf.with_solvent.eps=1.0 if case.endswith('eps1') else 78.4
        mf.with_solvent.lebedev_order=17
        mf.with_solvent.vdw_scale=1.2
        mf.with_solvent.r_probe=0.0
        mf.with_solvent.frozen=False
    mf.get_jk=types.MethodType(hf.SCF.get_jk,mf)
    energy=float(mf.kernel())
    grad=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ)))
    overlap=mf.get_ovlp()
    electron_trace=float(np.einsum('ij,ji',mf.make_rdm1(),overlap))
    info=dict(case=case,geometry_kind='EXPLICITLY_HYPOTHETICAL_FIXED_GEOMETRY_NOT_EXPERIMENT',atoms_A=atoms,charge=charge,spin_2S=0,Mo_formal_oxidation_assumption=6,explicit_electrons=mol.nelectron,ecp_core=mol.atom_nelec_core(0),nao=mol.nao_nr(),pyscf=pyscf.__version__,converged=bool(mf.converged),cycles=mf.cycles,energy_Eh=energy,orbital_gradient_norm=grad,electron_trace=electron_trace,wall_seconds=time.monotonic()-start,direct_JK_bound_to='pyscf.scf.hf.SCF.get_jk',cached_four_center_ERI=mf._eri is not None,direct_optimizer_created=mf._opt.get(None) is not None,thread_environment={k:os.environ.get(k) for k in ENV},method='PBE/def2-SVP; Mo def2 ECP',grid_level=2,PCM=None)
    if hasattr(mf,'with_solvent'):
        s=mf.with_solvent
        info['PCM']=dict(api='pyscf.solvent.PCM(mf)',method=s.method,eps=s.eps,lebedev_order=s.lebedev_order,vdw_scale=s.vdw_scale,r_probe_A=s.r_probe,electrostatic_energy_Eh=float(s.e),surface_points=len(s.surface['grid_coords']),Mo_default_modified_Bondi_bohr=float(pcm.modified_Bondi[42]),source_file=inspect.getsourcefile(pcm),source_sha256=hashlib.sha256(Path(inspect.getsourcefile(pcm)).read_bytes()).hexdigest())
    (BASE/'.omo/evidence'/f'{case}.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info,indent=2))
    assert mf.converged and np.isfinite(energy) and grad<1e-5
    assert abs(electron_trace-mol.nelectron)<1e-6
    assert mol.atom_nelec_core(0)==28 and mol.nelectron==(48 if charge==-2 else 38)
    assert mf._eri is None and mf._opt.get(None) is not None
    mol.stdout.close()


if __name__=='__main__':
    if len(sys.argv)>1:
        worker(sys.argv[1])
    else:
        receipts=[]
        for case in ('anion-gas','anion-eps1','anion-water','neutral-water'):
            cmd=[sys.executable,'-B',str(Path(__file__).resolve()),case]
            start=time.monotonic()
            try:
                p=subprocess.run(cmd,text=True,capture_output=True,timeout=90,env={**os.environ,**ENV})
                rec=dict(argv=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,wall_seconds=time.monotonic()-start)
            except subprocess.TimeoutExpired as e:
                rec=dict(argv=cmd,timeout=True,wall_seconds=time.monotonic()-start,stdout=str(e.stdout),stderr=str(e.stderr))
            receipts.append(rec)
            (BASE/'.omo/evidence/receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
            print(case,rec.get('returncode','TIMEOUT'),round(rec['wall_seconds'],3),flush=True)
            assert rec.get('returncode')==0,rec
        rows={case:json.loads((BASE/'.omo/evidence'/f'{case}.json').read_text()) for case in ('anion-gas','anion-eps1','anion-water','neutral-water')}
        assert abs(rows['anion-gas']['energy_Eh']-rows['anion-eps1']['energy_Eh'])<1e-8
        assert abs(rows['anion-eps1']['PCM']['electrostatic_energy_Eh'])<1e-12
        assert rows['anion-water']['PCM']['electrostatic_energy_Eh']<0
        (BASE/'result.json').write_text(json.dumps(dict(status='PASS_RUNTIME_ONLY',checks=['four converged SCFs','electron trace and core count','direct JK no cached ERI','epsilon-one vacuum equivalence','negative charged-solute polarization energy'],results=rows,parent_input_admitted=False,parent_SCF_run=False),indent=2)+'\n')
        print('PASS runtime-only; parent input remains unbuilt and unqualified')
