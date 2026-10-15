"""Additive retrospective runtime qualification; explicit prepare/launch only."""
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import traceback

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
MO = LAB/'cpcm-rij-memory-qualification'
WV = LAB/'wv-method-qualification'
MO_CASES = ('anion-water', 'neutral-water', 'anion-eps1', 'heldout-Mo2O7', 'new-external')
CASES = MO_CASES + ('WO4', 'VO4')
THREADS = (1, 4)
LABELS = ('initial', 'perturbed', 'direct_converged', 'RI_converged')
WALL = 180
RSS = 2*2**30


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def read(path): return json.loads(Path(path).read_text())
def save(path, value): Path(path).write_text(json.dumps(value, indent=2)+'\n')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def accepted(r):
    return (isinstance(r,dict) and all(key in r for key in ('returncode','termination_reason','monitor_error'))
            and type(r['returncode']) is int and r['returncode'] == 0
            and r['termination_reason'] is None and r['monitor_error'] is None)


def owned(path):
    path = Path(path).resolve()
    if not path.is_relative_to(BASE.resolve()) or path == BASE.resolve():
        raise ValueError('Output outside qualification directory')
    return path


def original_pins():
    common = load('original_mo', MO/'run.py')
    common.validate_sources()
    paths = set(common.pinned_files())
    for manifest in (MO/'run-v1/pins.json', WV/'run-v1/pins.json'):
        mapping = read(manifest)
        for path, digest in mapping.items():
            if sha(path) != digest: raise ValueError('Changed original pin: '+path)
        paths.update(mapping); paths.add(str(manifest))
    for root, cases in ((MO, MO_CASES), (WV, ('WO4','VO4'))):
        summary = read(root/'run-v1/result.json')
        expected = 'PASS_RETROSPECTIVE_IMPLEMENTATION_EQUIVALENCE' if root == MO else 'PASS_NUMERICAL_SCREEN_ONLY'
        if summary.get('status') != expected or summary.get('pins_unchanged') is not True:
            raise ValueError('Saved qualification summary failed: '+str(root))
        paths.update(str(p) for p in root.glob('*.py'))
        paths.update(str(root/n) for n in ('PROTOCOL.md','preparation.json','run-v1/result.json'))
        for case in cases:
            folder = root/'run-v1'/('operators-'+case if root == MO else case)
            paths.update(str(folder/n) for n in ('arrays.npz','result.json','supervisor.json'))
            if not accepted(read(folder/'supervisor.json')): raise ValueError('Saved supervisor failed: '+case)
            result = read(folder/'result.json')
            if result['status'] not in ('PASS_OPERATORS','PASS_NUMERICAL_SCREEN_ONLY') or not result['checks'] or not all(c['pass'] is True for c in result['checks']):
                raise ValueError('Saved case not passing: '+case)
    return {str(Path(p).resolve()): sha(p) for p in sorted(paths)}


def source_equivalence(original, prefix):
    prefix = Path(prefix).resolve()
    for path, digest in original.items():
        if '/site-packages/' not in path or Path(path).suffix not in ('.py','.dat'): continue
        relative = path.split('/site-packages/',1)[1]
        if not relative.startswith(('pyscf/','scipy/','numpy/')): continue
        package, remainder = relative.split('/',1)
        imported = Path(importlib.import_module(package).__file__).resolve().parent/remainder
        if not imported.resolve().is_relative_to(prefix) or sha(imported) != digest:
            raise ValueError('Actual runtime source differs from original pin: '+str(imported))


def loaded_native_files():
    import ctypes
    if sys.platform != 'darwin': raise ValueError('This runtime protocol is macOS-only')
    dyld = ctypes.CDLL(None)
    dyld._dyld_image_count.restype = ctypes.c_uint32
    dyld._dyld_get_image_name.argtypes = [ctypes.c_uint32]
    dyld._dyld_get_image_name.restype = ctypes.c_char_p
    paths = {Path(dyld._dyld_get_image_name(i).decode()).resolve() for i in range(dyld._dyld_image_count())}
    paths = {p for p in paths if not str(p).startswith(('/usr/lib/','/System/'))}
    if any(not p.is_relative_to(Path(sys.prefix).resolve()) for p in paths):
        raise ValueError('Loaded native library escaped isolated environment')
    return paths


def runtime_pins():
    import pyscf
    import numpy
    import scipy
    import h5py
    if pyscf.__version__ != '2.14.0': raise ValueError('Require PySCF 2.14.0')
    prefix = Path(sys.prefix).resolve()
    if not prefix.is_relative_to((LAB/'parent-openmp').resolve()):
        raise ValueError('Require isolated parent-openmp environment')
    names = ('pyscf.df.df_jk','pyscf.solvent.pcm','scipy.linalg._decomp_cholesky',
             'pyscf.solvent._attach_solvent','pyscf.scf.hf','pyscf.dft.rks','pyscf.gto.mole')
    modules = {name: Path(importlib.import_module(name).__file__).resolve() for name in names}
    if any(not p.is_relative_to(prefix) for p in modules.values()): raise ValueError('Imported source escaped isolated environment')
    # Freeze all package source/native files, including lazy imports used by operators.
    paths = {Path(sys.executable).resolve()}
    for package in (pyscf, numpy, scipy, h5py):
        root = Path(package.__file__).resolve().parent
        if not root.is_relative_to(prefix): raise ValueError('Package escaped isolated environment')
        paths.update(p for p in root.rglob('*') if p.is_file() and p.suffix in ('.py','.so','.dylib','.dat'))
    paths.update(p.resolve() for p in (prefix/'lib').glob('*.dylib'))
    paths.update(loaded_native_files())
    source_equivalence(original_pins(), prefix)
    return {'python':str(Path(sys.executable).resolve()), 'prefix':str(prefix),
            'versions':{'pyscf':pyscf.__version__,'numpy':numpy.__version__,'scipy':scipy.__version__,'h5py':h5py.__version__},
            'imported_sources':{n:str(p) for n,p in modules.items()},
            'files':{str(p):sha(p) for p in sorted(paths)}}


def manifest():
    return {'original':original_pins(), 'runtime':runtime_pins(),
            'driver':{str(BASE/name):sha(BASE/name) for name in ('run.py','test_run.py','PROTOCOL.md')}}


def prepare(python):
    if Path(python).resolve() != Path(sys.executable).resolve():
        raise ValueError('Explicit interpreter differs from actual interpreter')
    target = owned(BASE/'preparation.json')
    if target.exists(): raise ValueError('Already prepared')
    pins = manifest()
    save(target, {'status':'PREPARED_NOT_EXECUTED','pins':pins,'SCFs_launched':0,
                  'operators_evaluated':0,'maximum_SCFs':1,'parent_run':False})


def unchanged(): return manifest() == read(BASE/'preparation.json')['pins']


def operator_gate(receipts, results, same):
    expected = [(t,c) for t in THREADS for c in CASES]
    return bool(same and [(r.get('threads'),r.get('case')) for r in receipts] == expected
        and [(r.get('threads'),r.get('case')) for r in results] == expected
        and all(accepted(r) for r in receipts)
        and all(r.get('phase') == 'operators' and r.get('SCFs_launched') == 0
                and r.get('status') == 'PASS_OPERATORS' and r.get('runtime_guard_pass') is True
                and r.get('checks') and all(c.get('pass') is True for c in r['checks']) for r in results))


def operator_records():
    root = BASE/'run-v1'
    receipts = read(root/'operator-receipts.json')
    results = [read(root/f'threads-{t}'/'run-v1'/('operators-'+c)/'result.json')
               for t in THREADS for c in CASES]
    return receipts, results


def redirected_mo(threads):
    module = load('retargeted_mo', MO/'run.py')
    module.BASE = owned(BASE/'run-v1'/f'threads-{threads}')
    # The unchanged worker compares this adapter's complete manifest to its local copy.
    module.pinned_files = manifest
    return module


def wv_operators(case, out):
    import numpy as np
    from pyscf import dft
    sources = load('saved_wv_sources', WV/'sources.py')
    meta = next(x for x in sources.verified_sources() if x['case'] == case)
    memory = load('unchanged_memory', LAB/'cpcm-rij-memory/memory.py')
    from pyscf import gto
    mol = gto.M(atom=meta['atoms_A'],unit='Angstrom',basis='def2-svp',
                ecp={'W':'def2-svp'} if case=='WO4' else {},charge=meta['charge'],spin=0,
                max_memory=512,verbose=4,output=str(out/'native.log'))
    result={'case':case,'phase':'operators','SCFs_launched':0,'checks':[],'fresh_holdout':False,'physical_admission':False}
    arrays={}
    def check(name, value, limit=1e-10):
        result['checks'].append({'name':name,'value':float(value),'limit':limit,'pass':bool(np.isfinite(value) and value<=limit)})
        save(out/'result.json',result)
    def solvent(cls):
        s=cls(mol);s.method='C-PCM';s.eps=78.4;s.lebedev_order=17;s.vdw_scale=1.2;s.r_probe=0.;s.frozen=False
        return s
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
    mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=60;mf.chkfile=None
    if getattr(mf,'_chkfile',None) is not None: mf._chkfile.close()
    mf.get_hcore();mf=memory.install(memory.qualified.attach(mf,solvent(memory.MemoryPCM)))
    oracle=solvent(memory.qualified.BlockedPCM);s=mf.with_solvent
    with np.load(WV/'run-v1'/case/'arrays.npz') as prior:
        for label in LABELS:
            dm=prior[label+'_P'];j=mf.get_j(dm=dm);energy,v=s._get_vind(dm);q=s._intermediates['q'].copy()
            eo,vo=oracle._get_vind(dm);qo=oracle._intermediates['q']
            arrays.update({label+'_P':dm,label+'_Jmemory':j,label+'_PCM_V':v,label+'_PCM_q':q,label+'_energies':np.array([energy,eo])})
            check(label+'/saved_J',np.max(np.abs(j-prior[label+'_Jri'])))
            check(label+'/oracle_energy',abs(energy-eo));check(label+'/oracle_V',np.max(np.abs(v-vo)));check(label+'/oracle_q',np.max(np.abs(q-qo)))
            if label in ('direct_converged','RI_converged'):
                prefix=label.removesuffix('_converged')
                check(label+'/saved_PCM_V',np.max(np.abs(v-prior[prefix+'_PCM_V'])))
                check(label+'/saved_PCM_q',np.max(np.abs(q-prior[prefix+'_PCM_q'])))
        delta=prior['deltaP'];jdelta=mf.get_j(dm=delta);jzero=mf.get_j(dm=np.zeros_like(delta))
        check('J_additivity',np.max(np.abs(arrays['initial_Jmemory']+jdelta-arrays['perturbed_Jmemory'])),1e-9)
        check('J_zero',np.max(np.abs(jzero)),1e-9)
    obj=mf._rij_df;factor=obj._vjopt.j2c[0];sf=s._intermediates['factor'][0]
    good=(mf._eri is None and obj._cderi is None and obj._cderi_to_save is None and obj._vjopt.j2c_type=='cd'
          and 'S' not in s._intermediates and factor.flags.f_contiguous and not factor.flags.writeable
          and sf.flags.f_contiguous and not sf.flags.writeable and s.ao_block==1)
    check('storage_contract_violated',not good,0)
    result['status']='PASS_OPERATORS' if all(c['pass'] for c in result['checks']) else 'FAIL_OPERATORS'
    save(out/'result.json',result);np.savez_compressed(out/'arrays.npz',**arrays);mol.stdout.close()
    return 0 if result['status']=='PASS_OPERATORS' else 1


def worker(threads, phase, case):
    out=owned(BASE/'run-v1'/f'threads-{threads}'/'run-v1'/('operators-'+case if phase=='operators' else 'scf-new-external'))
    try:
        if not unchanged(): raise ValueError('Frozen manifest changed')
        from pyscf import lib
        if (lib.num_threads() != threads or os.environ.get('OMP_NUM_THREADS') != str(threads)
                or any(os.environ.get(k) != '1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))):
            raise ValueError('Actual OpenMP thread setting differs')
        if phase=='scf':
            if not operator_gate(*operator_records(),True): raise ValueError('All fourteen operators required')
            with owned(BASE/'run-v1/scf-claimed.json').open('x') as claim:
                json.dump({'maximum_SCFs':1,'case':'new-external','threads':4},claim)
        save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,
             'loaded_native_files':{str(p):sha(p) for p in sorted(loaded_native_files())}})
        code=redirected_mo(threads).worker(case,phase) if case in MO_CASES else wv_operators(case,out)
        result=read(out/'result.json');result.update(threads=threads,runtime_guard_pass=unchanged())
        if not result['runtime_guard_pass']: result['status']='ERROR';code=1
        save(out/'result.json',result)
        return code
    except Exception:
        save(out/'result.json',{'case':case,'threads':threads,'phase':phase,'status':'ERROR','exception':traceback.format_exc()})
        return 1


def launch():
    if not unchanged(): raise ValueError('Preparation pins changed')
    root=owned(BASE/'run-v1');root.mkdir(exist_ok=False)
    supervisor=load('existing_supervisor',LAB/'parent-pilot/pilot.py')
    pins=read(BASE/'preparation.json')['pins'];receipts=[];results=[]
    for threads in THREADS:
        target=owned(root/f'threads-{threads}'/'run-v1');target.mkdir(parents=True)
        save(target/'pins.json',pins)
        supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':str(threads),'OMP_DYNAMIC':'FALSE'}
        for case in CASES:
            out=target/('operators-'+case)
            receipt=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker',str(threads),'operators',case],out,WALL,RSS)
            receipts.append({'threads':threads,'case':case,**receipt});save(root/'operator-receipts.json',receipts)
            result=read(out/'result.json') if (out/'result.json').exists() else {};results.append(result)
    gate=operator_gate(receipts,results,unchanged());save(root/'phase1-gate.json',{'pass':gate,'SCFs_launched':0})
    phase2=None;final={}
    if gate:
        target=root/'threads-4'/'run-v1'
        # Existing Mo SCF's own five-case gate remains active in addition to the full gate.
        save(target/'operator-receipts.json',[r for r in receipts if r['threads']==4 and r['case'] in MO_CASES])
        phase2=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker','4','scf','new-external'],target/'scf-new-external',WALL,RSS)
        p=target/'scf-new-external/result.json';final=read(p) if p.exists() else {}
    same=unchanged();common=load('original_mo_gate',MO/'run.py')
    passed=gate and accepted(phase2) and common.phase2_accepted(phase2,final,same) and final.get('runtime_guard_pass') is True
    result={'status':'PASS_RETROSPECTIVE_RUNTIME_EQUIVALENCE' if passed else 'FAIL','phase1_pass':gate,
            'phase2':phase2,'phase2_skipped':not gate,'pins_unchanged':same,'maximum_SCFs':1,
            'parent_run':False,'fresh_holdout':False,'physical_admission':False}
    save(root/'result.json',result);print(json.dumps(result));return 0 if passed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if len(args)==3 and args[:2]==['--prepare','--python']: prepare(args[2])
    elif args==['--launch']: sys.exit(launch())
    elif len(args)==4 and args[0]=='--worker' and args[1] in ('1','4') and ((args[2]=='operators' and args[3] in CASES) or args[1:]==['4','scf','new-external']):
        sys.exit(worker(int(args[1]),args[2],args[3]))
    else: raise SystemExit('Use --prepare --python /exact/interpreter or --launch; no automatic execution')
