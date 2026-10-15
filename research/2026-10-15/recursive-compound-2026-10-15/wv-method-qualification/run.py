"""Frozen W/V fixed-geometry comparison; explicit prepare/launch only."""
import importlib.util
import json
from pathlib import Path
import sys
import traceback
import types
from sources import CASES, SOURCE, verified_sources

BASE = Path(__file__).resolve().parent
LAB = BASE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


common = load('memory_qualification_driver', LAB/'cpcm-rij-memory-qualification/run.py')
save, read, sha = common.save, common.read, common.sha


def pins():
    import pyscf
    native = read(LAB/'cpcm-rij-memory/source_pins.json')
    for path, digest in native.items():
        if sha(path) != digest: raise ValueError('Native source changed: '+path)
    paths = [Path(p) for p in native]
    paths += list(BASE.glob('*.py')) + [BASE/'PROTOCOL.md', BASE/'SOURCES.md', SOURCE/'SOURCES.md']
    paths += list((SOURCE/'raw').iterdir())
    paths += [LAB/p for p in ('cpcm-rij-memory/memory.py','cpcm-rij-memory/source_pins.json',
              'cpcm-rij-memory-qualification/run.py','rij-jkfit-qualification/run.py',
              'rij-jkfit-qualification/PROTOCOL.md','parent-pilot/pilot.py')]
    paths += [Path(pyscf.__file__).parent/p for p in ('gto/basis/def2-svp.dat',
              'solvent/_attach_solvent.py','scf/hf.py','dft/rks.py','gto/mole.py')]
    return {str(p.resolve()): sha(p) for p in paths}


def molecule(meta, output=None):
    from pyscf import gto
    return gto.M(atom=meta['atoms_A'], unit='Angstrom', basis='def2-svp',
                 ecp={'W':'def2-svp'} if meta['metal']=='W' else {}, charge=meta['charge'],
                 spin=0, max_memory=512, verbose=4 if output else 0, output=output)


def prepare():
    import pyscf
    from pyscf import df
    if (BASE/'preparation.json').exists(): raise ValueError('Already prepared')
    assert pyscf.__version__ == '2.14.0'
    records = verified_sources()
    memory = load('unchanged_memory', LAB/'cpcm-rij-memory/memory.py')
    for meta in records:
        mol = molecule(meta); aux = df.addons.make_auxmol(mol,'def2-universal-jkfit')
        removed = mol.atom_nelec_core(0)
        assert removed == (60 if meta['metal']=='W' else 0)
        solvent = memory.MemoryPCM(mol); solvent._guard()
        meta.update(nao=mol.nao, naux=aux.nao, explicit_electrons=mol.nelectron, metal_core_electrons=removed)
    save(BASE/'preparation.json', {'status':'PREPARED_NOT_EXECUTED','cases':records,'pins':pins(),
                                  'SCFs_launched':0,'operators_evaluated':0})
    print('Prepared two cases; zero SCFs/operators; no launch authorization')


def worker(case):
    import numpy as np
    from pyscf import dft
    from pyscf.scf import hf
    out = BASE/'run-v1'/case
    result = {'case':case,'checks':[], 'SCFs_launched':0, 'physical_admission':False,
              'experimental_validation':False,'fresh_fixed_geometry_numerical_challenge':True}
    arrays = {}
    def flush():
        save(out/'result.json',result); np.savez_compressed(out/'arrays.npz',**arrays)
    def check(name, value, limit):
        result['checks'].append({'name':name,'value':float(value),'limit':limit,
                                 'pass':bool(np.isfinite(value) and value <= limit)}); flush()
    def metric(row):
        with (out/'metric-calls.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')
    try:
        if pins()!=read(BASE/'run-v1/pins.json'): raise ValueError('Pins changed')
        meta = next(m for m in verified_sources() if m['case']==case)
        mol = molecule(meta,str(out/'native.log'))
        memory = load('unchanged_memory', LAB/'cpcm-rij-memory/memory.py')
        def configured(ri):
            mf=dft.RKS(mol); mf.xc='PBE'; mf.grids.level=2; mf.direct_scf=True
            mf.direct_scf_tol=1e-13; mf.conv_tol=1e-11; mf.conv_tol_grad=1e-7; mf.max_cycle=60
            mf.chkfile=None
            if getattr(mf,'_chkfile',None) is not None: mf._chkfile.close()
            mf.get_hcore()
            solvent=memory.MemoryPCM(mol); solvent.method='C-PCM'; solvent.eps=78.4
            solvent.lebedev_order=17; solvent.vdw_scale=1.2; solvent.r_probe=0.; solvent.frozen=False
            mf=memory.qualified.attach(mf,solvent)
            if ri: return memory.install(mf,metric)
            mf.get_jk=types.MethodType(hf.SCF.get_jk,mf); return mf
        direct, ri = configured(False), configured(True)
        initial=direct.get_init_guess(); arrays['initial_P']=initial.copy()
        rng=np.random.default_rng(7392016); delta=rng.standard_normal(initial.shape)
        delta=(delta+delta.T)/2; delta*=.01/np.linalg.norm(delta); arrays['deltaP']=delta; flush()
        def compare(label, dm):
            jd=direct.get_j(dm=dm); jr=ri.get_j(dm=dm)
            arrays.update({label+'_P':dm.copy(),label+'_Jdirect':jd,label+'_Jri':jr}); flush()
            check(label+'/max_J_error_Eh',np.max(np.abs(jr-jd)),1e-3)
            check(label+'/Coulomb_energy_error_Eh_per_metal',abs(.5*np.einsum('ij,ji',dm,jr-jd)),1e-3)
            check(label+'/J_asymmetry',np.max(np.abs(jr-jr.T)),1e-10)
        compare('initial',initial); compare('perturbed',initial+delta)
        for label, mf in [('direct',direct),('RI',ri)]:
            # Build the RI metric before the surface; initial compare already did so.
            result['SCFs_launched']+=1; arrays[label+'_initial_P']=initial.copy(); flush()
            def callback(env, label=label):
                with (out/'iterations.jsonl').open('a') as f:
                    f.write(json.dumps({'method':label,'cycle':int(env['cycle'])+1,'energy_Eh':float(env['e_tot'])})+'\n')
            mf.callback=callback; energy=float(mf.kernel(dm0=initial.copy())); dm=mf.make_rdm1()
            fock=mf.get_fock(dm=dm)
            arrays.update({label+'_mo_coeff':mf.mo_coeff,label+'_mo_occ':mf.mo_occ,
                           label+'_mo_energy':mf.mo_energy,label+'_fock':fock,
                           label+'_PCM_V':mf.with_solvent.v.copy(),label+'_PCM_q':mf.with_solvent._intermediates['q'].copy()})
            result[label+'_SCF']={'energy_Eh':energy,'cycles':mf.cycles,'converged':bool(mf.converged),'PCM_energy_Eh':float(mf.with_solvent.e)}
            check(label+'/not_converged',not mf.converged,0); compare(label+'_converged',dm)
        dm=arrays['RI_converged_P']; overlap=ri.get_ovlp(); fd=direct.get_fock(dm=dm)
        arrays.update(overlap=overlap,direct_fock_at_RI=fd,direct_PCM_V_at_RI=direct.with_solvent.v.copy())
        check('total_energy_error_Eh_per_metal',abs(result['RI_SCF']['energy_Eh']-result['direct_SCF']['energy_Eh']),1e-3)
        check('direct_full_Fock_residual',np.linalg.norm(ri.get_grad(ri.mo_coeff,ri.mo_occ,fd)),1e-3)
        check('RI_full_Fock_gradient',np.linalg.norm(ri.get_grad(ri.mo_coeff,ri.mo_occ,arrays['RI_fock'])),1e-5)
        for label in ('direct','RI'):
            check(label+'/electron_trace_error',abs(np.einsum('ij,ji',arrays[label+'_converged_P'],overlap)-mol.nelectron),1e-8)
        obj=ri._rij_df
        good=(direct._eri is None and ri._eri is None and obj._cderi is None and obj._cderi_to_save is None
              and obj._vjopt.j2c_type=='cd' and all('S' not in m.with_solvent._intermediates for m in (direct,ri)))
        check('storage_contract_violated',not good,0)
        result['status']='PASS_NUMERICAL_SCREEN_ONLY' if all(c['pass'] for c in result['checks']) else 'FAIL_NUMERICAL_SCREEN'
        mol.stdout.close()
    except Exception:
        result.update(status='ERROR',exception=traceback.format_exc())
    flush()
    return 0 if result['status']=='PASS_NUMERICAL_SCREEN_ONLY' else 1


def launch_gate(receipts, results, unchanged):
    return bool(unchanged and tuple(r.get('case') for r in receipts)==tuple(CASES)
                and tuple(r.get('case') for r in results)==tuple(CASES)
                and all(common.accepted(r) for r in receipts)
                and all(r.get('status')=='PASS_NUMERICAL_SCREEN_ONLY' and r.get('SCFs_launched')==2
                        and r.get('checks') and all(c.get('pass') is True for c in r['checks'])
                        for r in results))


def launch():
    frozen=read(BASE/'preparation.json')['pins']
    if pins()!=frozen: raise ValueError('Preparation pins changed')
    verified_sources(); out=BASE/'run-v1'; out.mkdir(exist_ok=False); save(out/'pins.json',frozen)
    supervisor=load('original_supervisor',LAB/'parent-pilot/pilot.py'); receipts=[]
    for case in CASES:
        if pins()!=frozen: raise ValueError('Worker pins changed')
        receipt=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker',case],out/case,180,2*2**30)
        receipts.append({'case':case,**receipt}); save(out/'receipts.json',receipts)
    unchanged=pins()==frozen
    results=[read(out/case/'result.json') if (out/case/'result.json').exists() else {} for case in CASES]
    passed=launch_gate(receipts,results,unchanged)
    counts=[r.get('SCFs_launched') for r in results]
    actual=sum(counts) if all(isinstance(n,int) for n in counts) else None
    save(out/'result.json',{'status':'PASS_NUMERICAL_SCREEN_ONLY' if passed else 'FAIL_NUMERICAL_SCREEN',
                           'pins_unchanged':unchanged,'maximum_SCFs':4,'actual_SCFs_launched':actual,
                           'case_SCFs_launched':dict(zip(CASES,counts)),'physical_admission':False})
    return 0 if passed else 1


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']: prepare()
    elif sys.argv[1:]==['--launch']: sys.exit(launch())
    elif len(sys.argv)==3 and sys.argv[1]=='--worker' and sys.argv[2] in CASES: sys.exit(worker(sys.argv[2]))
    else: raise SystemExit('Use --prepare or --launch')
