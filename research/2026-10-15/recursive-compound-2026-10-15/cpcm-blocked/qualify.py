"""Frozen small-reference qualification; never launches a parent calculation."""
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
EVID = BASE / 'evidence'
REFERENCE = BASE.parent / 'identity/next-step/method-qualification/result.json'
ENV = {k: '1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}
CASES = ('anion-water', 'neutral-water', 'anion-eps1')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def worker(case):
    import types
    import numpy as np
    import pyscf
    from pyscf import dft, gto
    from pyscf.scf import hf
    from pyscf.solvent import pcm
    from blocked_pcm import BlockedPCM, attach
    rec = {'case': case, 'checks': [], 'thread_environment': {k: os.environ.get(k) for k in ENV}}
    arrays = {}
    def save():
        (EVID/f'{case}.json').write_text(json.dumps(rec, indent=2)+'\n')
        np.savez_compressed(EVID/f'{case}.npz', **arrays)
    def check(name, value, passed):
        rec['checks'].append({'scenario': name, 'value': value, 'pass': bool(passed)})
        save()
    try:
        source = Path(inspect.getsourcefile(pcm))
        rec['pyscf'] = pyscf.__version__
        rec['source_sha256'] = digest(source)
        assert rec['source_sha256'] == '97bb24fb2e607745c444c36b6c3e649ffca66f808ec2965137a871061b3b9fed'
        old = json.loads(REFERENCE.read_text())['results'][case]
        mol = gto.M(atom=old['atoms_A'], unit='Angstrom', basis='def2-svp', ecp={'Mo':'def2-svp'}, charge=old['charge'], spin=0, max_memory=512, verbose=4, output=str(EVID/f'{case}.scf.log'))
        def configured(cls):
            s = cls(mol)
            s.method='C-PCM'; s.eps=1.0 if case.endswith('eps1') else 78.4
            s.lebedev_order=17; s.vdw_scale=1.2; s.r_probe=0.0
            return s
        ref, blocked = configured(pcm.PCM), configured(BlockedPCM)
        ref.build(); blocked.build()
        def diff(name, x, y, tolerance=1e-10):
            error = float(np.max(np.abs(np.asarray(x)-np.asarray(y))))
            check(name, error, error<tolerance)
        diff('surface S', blocked._intermediates['S'], ref._intermediates['S'])
        diff('nuclear surface potential', blocked.v_grids_n, ref.v_grids_n)
        arrays['S_blocked']=blocked._intermediates['S']; arrays['S_reference']=ref._intermediates['S']
        arrays['nuclear_blocked']=blocked.v_grids_n; arrays['nuclear_reference']=ref.v_grids_n
        mf=dft.RKS(mol); mf.xc='PBE'; mf.grids.level=2
        dm0=mf.get_init_guess()
        rng=np.random.default_rng(7392016)
        delta=rng.standard_normal(dm0.shape); delta=(delta+delta.T)/2
        delta *= .01/np.linalg.norm(delta)
        arrays['deltaP']=delta
        def compare(label, dm):
            er, vr=ref._get_vind(dm)
            re=ref._get_v(dm[None,:,:])
            arrays[label+'_dm']=dm
            arrays[label+'_reference_V']=vr
            arrays[label+'_reference_q']=ref._intermediates['q'].copy()
            arrays[label+'_reference_electronic']=re
            for size in (1,7,8):
                blocked.ao_block=size
                eb,vb=blocked._get_vind(dm)
                be=blocked._get_v(dm[None,:,:])
                prefix=f'{label}/block{size}'
                diff(prefix+'/electronic potential',be,re)
                diff(prefix+'/q',blocked._intermediates['q'],ref._intermediates['q'])
                diff(prefix+'/energy',eb,er)
                diff(prefix+'/AO potential',vb,vr)
                S=blocked._intermediates['S']; q=blocked._intermediates['q']; v=blocked._intermediates['v_grids']
                f=(blocked.eps-1)/blocked.eps
                denom=np.linalg.norm(S,np.inf)*np.linalg.norm(q,np.inf)+np.linalg.norm(f*v,np.inf)
                backward=float(np.linalg.norm(S@q+f*v,np.inf)/denom) if denom else 0.
                check(prefix+'/normalized backward error',backward,backward<1e-12)
                arrays[prefix+'_V']=vb; arrays[prefix+'_q']=q.copy(); arrays[prefix+'_electronic']=be
                arrays[prefix+'_energies']=np.array([eb,er])
            blocked.ao_block=8
        compare('initial',dm0); compare('perturbed',dm0+delta)
        _,v0=blocked._get_vind(dm0)
        analytic=float(np.einsum('ij,ji',v0,delta))
        for h in (1e-4,5e-5):
            plus=blocked._get_vind(dm0+h*delta)[0]; minus=blocked._get_vind(dm0-h*delta)[0]
            numerical=(plus-minus)/(2*h)
            check(f'density derivative h={h}',{'analytic':analytic,'centered':numerical,'error':abs(analytic-numerical)},abs(analytic-numerical)<1e-7)
        first=blocked._intermediates['factor'][0]
        blocked._get_vind(dm0)
        check('factor reused',blocked._intermediates['factor'][0] is first,blocked._intermediates['factor'][0] is first)
        blocked.build()
        diff('repeat build S',blocked._intermediates['S'],ref._intermediates['S'])
        moved=mol.copy(); coords=moved.atom_coords(); coords[-1,0]+=.02
        moved.set_geom_(coords,unit='Bohr')
        blocked.reset(moved)
        check('reset invalidates caches',None,blocked._intermediates is None and blocked.surface is None and blocked.v_grids_n is None and blocked.e is None and blocked.v is None and blocked._dm is None)
        blocked.build(); moved_ref=configured(pcm.PCM); moved_ref.reset(moved); moved_ref.build()
        diff('geometry reset S',blocked._intermediates['S'],moved_ref._intermediates['S'])
        diff('geometry reset nuclear',blocked.v_grids_n,moved_ref.v_grids_n)
        blocked.reset(mol); blocked.build()
        for attr,value in [('method','COSMO'),('method','IEF-PCM'),('method','SS(V)PE'),('frozen',True),('state_id',1),('surface_discretization_method','ISWIG'),('equilibrium_solvation',True)]:
            original=getattr(blocked,attr); setattr(blocked,attr,value)
            rejected=False
            try: blocked._get_vind(dm0)
            except NotImplementedError: rejected=True
            finally: setattr(blocked,attr,original)
            check(f'guard {attr}={value}',rejected,rejected)
        mf=attach(mf,blocked)
        for obj,names in [(blocked,('grad','hess','nuc_grad_method','Hessian','_B_dot_x','to_gpu')),(mf,('nuc_grad_method','Gradients','Hessian','gen_response','stability','TDA','TDHF','TDDFT','MP2','CISD','CCSD','CASCI','CASSCF','to_gpu','newton'))]:
            for name in names:
                rejected=False
                try: getattr(obj,name)()
                except NotImplementedError: rejected=True
                check(f'API guard {type(obj).__name__}.{name}',rejected,rejected)
        mf.conv_tol=1e-11; mf.conv_tol_grad=1e-7; mf.max_cycle=60
        mf.direct_scf=True; mf.chkfile=None
        mf.get_jk=types.MethodType(hf.SCF.get_jk,mf)
        energy=float(mf.kernel())
        dm=mf.make_rdm1()
        residual=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,mf.get_fock(dm=dm))))
        trace=float(np.einsum('ij,ji',dm,mf.get_ovlp()))
        rec['SCF']={'energy_Eh':energy,'original_energy_Eh':old['energy_Eh'],'cycles':mf.cycles,'orbital_residual':residual,'electron_trace':trace,'cached_ERI':mf._eri is not None,'surface_points':len(blocked.v_grids_n),'nao':mol.nao}
        check('SCF converged',bool(mf.converged),mf.converged)
        check('total energy vs recorded reference',abs(energy-old['energy_Eh']),abs(energy-old['energy_Eh'])<1e-8)
        check('solvent aware residual',residual,residual<1e-5)
        check('electron trace error',abs(trace-mol.nelectron),abs(trace-mol.nelectron)<1e-6)
        check('no cached four center ERI',mf._eri is None,mf._eri is None)
        compare('converged',dm)
        rec['status']='PASS_IMPLEMENTATION_EQUIVALENCE_ONLY' if all(c['pass'] for c in rec['checks']) else 'FAIL'
        mol.stdout.close()
    except Exception:
        rec['status']='FAIL'; rec['exception']=traceback.format_exc()
    save()
    print(json.dumps(rec,indent=2),flush=True)
    return 0 if rec['status'].startswith('PASS') else 1


def supervisor():
    EVID.mkdir(exist_ok=True)
    if (BASE/'result.json').exists():
        raise RuntimeError('Existing results retained; no automatic rerun')
    receipts=[]
    for case in CASES:
        cmd=[sys.executable,'-B',str(Path(__file__).resolve()),case]
        start=time.monotonic()
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=90,env={**os.environ,**ENV})
            stdout,stderr=p.stdout,p.stderr
            receipt={'case':case,'argv':cmd,'returncode':p.returncode}
        except subprocess.TimeoutExpired as e:
            stdout=e.stdout or b''; stderr=e.stderr or b''
            stdout=stdout.decode() if isinstance(stdout,bytes) else stdout
            stderr=stderr.decode() if isinstance(stderr,bytes) else stderr
            receipt={'case':case,'argv':cmd,'timeout':True}
        receipt['wall_seconds']=time.monotonic()-start
        (EVID/f'{case}.stdout.txt').write_text(stdout)
        (EVID/f'{case}.stderr.txt').write_text(stderr or '(no stderr)\n')
        receipts.append(receipt)
        (EVID/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
        print(case,receipt,flush=True)
    paths=[BASE/'blocked_pcm.py',BASE/'qualify.py',BASE/'PROTOCOL.md',REFERENCE]+list(EVID.iterdir())
    result={'status':'PASS_IMPLEMENTATION_EQUIVALENCE_ONLY' if all(r.get('returncode')==0 for r in receipts) else 'FAIL','receipts':receipts,'sha256':{str(p):digest(p) for p in paths if p.is_file()},'parent_SCF_run':False,'physical_admission':False}
    (BASE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['status'].startswith('PASS') else 1

if __name__=='__main__':
    sys.exit(worker(sys.argv[1]) if len(sys.argv)>1 else supervisor())
