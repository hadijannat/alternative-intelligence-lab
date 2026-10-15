import json
import os
from pathlib import Path
import subprocess
import sys
import time

B=Path(__file__).resolve().parent
CASES={'analytic':0.0,'plus1':0.001,'minus1':-0.001,'plus2':0.0005,'minus2':-0.0005}
THRESHOLD=1e-4


def worker(case):
    import types
    import numpy as np
    from pyscf import gto,dft,solvent,lib
    from pyscf.scf import hf
    start=time.monotonic()
    reference=json.loads((B/'.omo/evidence/anion-water.json').read_text())
    atoms=reference['atoms_A']
    atoms[1][1][0]+=CASES[case]*lib.param.BOHR
    mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-2,spin=0,verbose=4,max_memory=512,output=str(B/'.omo/evidence'/f'derivative-{case}.log'))
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=60;mf.direct_scf=True;mf.chkfile=None
    mf=solvent.PCM(mf);mf.with_solvent.method='C-PCM';mf.with_solvent.eps=78.4;mf.with_solvent.lebedev_order=17;mf.with_solvent.vdw_scale=1.2;mf.with_solvent.r_probe=0.0;mf.with_solvent.frozen=False
    mf.get_jk=types.MethodType(hf.SCF.get_jk,mf)
    energy=float(mf.kernel())
    orbital=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,mf.get_fock(dm=mf.make_rdm1()))))
    assert mf.converged and orbital<1e-5
    gradient=mf.nuc_grad_method().kernel().tolist() if case=='analytic' else None
    out=dict(case=case,delta_O1_x_bohr=CASES[case],energy_Eh=energy,orbital_gradient_norm=orbital,converged=bool(mf.converged),gradient_Eh_per_bohr=gradient,wall_seconds=time.monotonic()-start)
    (B/'.omo/evidence'/f'derivative-{case}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));mol.stdout.close()


if __name__=='__main__':
    if len(sys.argv)>1:worker(sys.argv[1])
    else:
        receipts=[]
        for case in CASES:
            cmd=[sys.executable,'-B',str(Path(__file__).resolve()),case]
            try:
                p=subprocess.run(cmd,text=True,capture_output=True,timeout=90,env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}})
                rec=dict(argv=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
            except subprocess.TimeoutExpired as e:rec=dict(argv=cmd,timeout=True,stdout=str(e.stdout),stderr=str(e.stderr))
            receipts.append(rec);(B/'.omo/evidence/derivative-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
            print(case,rec.get('returncode','TIMEOUT'),flush=True)
            assert rec.get('returncode')==0,rec
        rows={c:json.loads((B/'.omo/evidence'/f'derivative-{c}.json').read_text()) for c in CASES}
        analytic=rows['analytic']['gradient_Eh_per_bohr'][1][0]
        checks=[]
        for tag,h in [('1',0.001),('2',0.0005)]:
            fd=(rows['plus'+tag]['energy_Eh']-rows['minus'+tag]['energy_Eh'])/(2*h)
            checks.append(dict(h_bohr=h,analytic_Eh_per_bohr=analytic,central_difference_Eh_per_bohr=fd,absolute_discrepancy=abs(analytic-fd),pass_threshold=abs(analytic-fd)<=THRESHOLD))
        result=dict(threshold_Eh_per_bohr=THRESHOLD,checks=checks,pass_all=all(c['pass_threshold'] for c in checks),runtime_only=True,parent_input_admitted=False)
        (B/'derivative-result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
        assert result['pass_all'],'Predeclared derivative threshold failed; preserve result'
