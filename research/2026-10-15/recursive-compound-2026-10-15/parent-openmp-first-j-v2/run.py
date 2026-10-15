"""One independently reviewed parent first-J probe; no SCF or PCM build."""
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
QUAL=LAB/'parent-openmp-qualification-v2'
OLD=LAB/'parent-pilot-memory'
PREVIOUS=LAB/'parent-openmp-first-j'
INPUT=LAB/'parent-inputs'
WALL=300
RSS=10*2**30
NAO=3068
NAUX=19612


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


qualification=load('frozen_runtime_qualification',QUAL/'run.py')
read,save,sha,accepted=qualification.read,qualification.save,qualification.sha,qualification.accepted


def require(value,message):
    if not value:raise ValueError(message)


def owned(path):
    path=Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()) and path!=BASE.resolve(),'Output outside first-J directory')
    return path


def verify_pins(pins):
    for path,digest in pins.items():require(sha(path)==digest,'Changed frozen input: '+path)


def qualification_artifacts():
    root=QUAL/'run-v1';final=read(root/'result.json')
    require(final.get('status')=='PASS_RETROSPECTIVE_RUNTIME_EQUIVALENCE'
            and final.get('phase1_pass') is True and final.get('pins_unchanged') is True
            and final.get('phase2_skipped') is False,'Terminal v2 qualification failed')
    require(qualification.unchanged(),'Runtime qualification pins changed')
    receipts,results=qualification.operator_records()
    require(qualification.operator_gate(receipts,results,True),'Fourteen-operator qualification gate failed')
    require(read(root/'phase1-gate.json').get('pass') is True,'Saved operator gate failed')
    claim=read(root/'scf-claimed.json')
    require(claim=={'maximum_SCFs':1,'case':'new-external','threads':4},'Qualification SCF claim differs')
    paths=[QUAL/'preparation.json',root/'result.json',root/'operator-receipts.json',root/'phase1-gate.json',root/'scf-claimed.json']
    for receipt,result in zip(receipts,results):
        out=root/f"threads-{receipt['threads']}"/'run-v1'/('operators-'+receipt['case'])
        require(type(receipt.get('threads')) is int and type(result.get('threads')) is int,'Operator thread metadata differs')
        supervisor=read(out/'supervisor.json')
        require(accepted(supervisor) and {k:v for k,v in receipt.items() if k not in ('threads','case')}==supervisor,'Operator receipt mismatch')
        require(type(result.get('SCFs_launched')) is int and result['SCFs_launched']==0,'Operator SCF count differs')
        paths.extend(out/name for name in ('result.json','supervisor.json','arrays.npz','runtime-observation.json','native.log'))
    out=root/'threads-4/run-v1/scf-new-external';supervisor=read(out/'supervisor.json');result=read(out/'result.json')
    require(accepted(final.get('phase2')) and accepted(supervisor) and final['phase2']==supervisor,'SCF receipt mismatch')
    require(result.get('case')=='new-external' and result.get('phase')=='scf'
            and result.get('threads')==4 and result.get('status')=='PASS_SCF'
            and result.get('runtime_guard_pass') is True and type(result.get('SCFs_launched')) is int
            and result['SCFs_launched']==1 and result.get('checks') and all(c.get('pass') is True for c in result['checks']),'Small SCF qualification failed')
    paths.extend(out/name for name in ('result.json','supervisor.json','arrays.npz','runtime-observation.json','native.log'))
    return {str(p):sha(p) for p in paths}


def parent_pins():
    original=read(OLD/'preparation.json')['pins'];verify_pins(original)
    paths=[OLD/'preparation.json',INPUT/'P0_A.xyz',INPUT/'metadata.json',LAB/'identity/site_mapping.json']
    paths.extend(OLD/'run-v1'/name for name in ('partial.npz','preflight.json','stages.jsonl','supervisor.json','launch-result.json','factor-aliases.json'))
    paths.extend(PREVIOUS/name for name in ('run.py','test_run.py','PROTOCOL.md','preparation.json','independent-root-review.json'))
    paths.extend(PREVIOUS/'run-v1'/name for name in ('launch-gate.json','worker-started.json','runtime-observation.json',
                 'density-validation.json','native.log','stages.jsonl','stdout.txt','stderr.txt','supervisor.json','failure.json','launch-result.json'))
    return {**original,**{str(p):sha(p) for p in paths}}


def manifest():
    return {'qualification':qualification_artifacts(),'parent':parent_pins(),
            'driver':{str(BASE/name):sha(BASE/name) for name in ('run.py','test_run.py','PROTOCOL.md')}}


def parent_atoms():
    from collections import Counter
    candidate=next(c for c in read(INPUT/'metadata.json')['candidates'] if c['id']=='P0_A')
    require(candidate['checks']['computational_input_admitted'] is True and candidate['physical_admission'] is False and candidate['charge']==-8,'Parent metadata differs')
    require(sha(INPUT/'P0_A.xyz')==candidate['xyz_sha256'],'Parent geometry digest differs')
    lines=(INPUT/'P0_A.xyz').read_text().splitlines()
    atoms=[(s[0],tuple(map(float,s[1:]))) for line in lines[2:] if (s:=line.split())]
    require(int(lines[0])==len(atoms)==196 and Counter(e for e,_ in atoms)=={'Mo':36,'O':128,'H':32},'Parent composition differs')
    require(all(len(xyz)==3 and all(map(math.isfinite,xyz)) for _,xyz in atoms),'Invalid parent coordinates')
    require(atoms[:164]==[(s['element'],tuple(s['cartesian_A'])) for s in read(LAB/'identity/site_mapping.json')],'Parent heavy sites differ')
    return atoms


def validate_density(density,cycle):
    import numpy as np
    require(density.dtype==np.float64 and density.shape==(NAO,NAO),'Saved density dtype/shape differs')
    require(cycle.shape==() and np.issubdtype(cycle.dtype,np.integer) and int(cycle)==0,'Require saved integer cycle zero')
    require(np.isfinite(density).all(),'Nonfinite saved density')
    asymmetry=float(np.max(np.abs(density-density.T)))
    require(asymmetry<=1e-12,'Asymmetric saved density')
    return {'shape':list(density.shape),'dtype':str(density.dtype),'cycle':0,'max_asymmetry':asymmetry}


def saved_density():
    import numpy as np
    with np.load(OLD/'run-v1/partial.npz',allow_pickle=False) as arrays:
        require(set(arrays.files)=={'density','cycle'},'Unexpected cycle-zero array metadata')
        density=arrays['density'];summary=validate_density(density,arrays['cycle'])
    return density,summary


def prepare():
    target=owned(BASE/'preparation.json');require(not target.exists(),'Already prepared')
    pins=manifest()
    runtime=read(QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve()==Path(runtime['python']).resolve(),'Require qualified interpreter')
    parent_atoms();density,summary=saved_density();del density
    save(target,{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins,'density':summary,
                 'parent_molecule_built':False,'J_calls':0,'SCFs_launched':0,'wall_cap_seconds':WALL,'rss_guard_bytes':RSS})


def validate_gate():
    preparation=read(BASE/'preparation.json');current=manifest()
    require(preparation['pins']==current,'First-J preparation pins changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_PARENT_FIRST_J_PROBE'
            and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent first-J root review missing')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json')
            and review.get('qualification_artifacts')==current['qualification'],'Root review binding differs')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json'),
            'qualification_artifacts':current['qualification']}


def claim_worker(out):
    with owned(out/'worker-started.json').open('x') as claim:json.dump({'pid':os.getpid(),'maximum_J_calls':1,'maximum_SCFs':0},claim)


def pcm_unbuilt(solvent):
    return (all(value is None or (type(value) is dict and not value)
                for value in (solvent.surface,solvent._intermediates))
            and solvent.v_grids_n is None)


def forbidden(*args,**kwargs):raise RuntimeError('SCF and PCM build are outside first-J scope')


def single_j(mf,density):
    mf.kernel=mf.scf=forbidden;mf.with_solvent.build=forbidden
    require(mf._rij_calls==0,'Only a fresh single-J request is allowed')
    result=mf.get_j(dm=density)
    require(mf._rij_calls==1,'Expected exactly one J request')
    return result


def worker():
    out=owned(BASE/'run-v1');gate=validate_gate()
    require(read(out/'launch-gate.json')==gate,'Launch gate differs');claim_worker(out)
    start=time.monotonic()
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (out/'stages.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    stage('worker_started',J_calls=0,SCFs_launched=0)
    from pyscf import dft,gto,lib
    import numpy as np
    require(lib.num_threads()==4 and os.environ.get('OMP_NUM_THREADS')=='4','Actual OpenMP thread count differs')
    require(all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'BLAS thread controls differ')
    runtime=read(QUAL/'preparation.json')['pins']['runtime']
    require(qualification.runtime_pins()==runtime,'Actual runtime differs from qualified runtime')
    save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,
         'loaded_native_files':{str(p):sha(p) for p in sorted(qualification.loaded_native_files())}})
    memory=load('unchanged_parent_memory',LAB/'cpcm-rij-memory/memory.py');aliases=[]
    original_factor=memory.factor_inplace
    def factor(matrix,*args,**kwargs):
        pointer=matrix.ctypes.data;stage('RI_factor_start',shape=list(matrix.shape))
        answer=original_factor(matrix,*args,**kwargs)
        row={'shape':list(matrix.shape),'input_pointer':pointer,'factor_pointer':answer[0].ctypes.data,
             'shares_memory':bool(np.shares_memory(matrix,answer[0])),'readonly':not answer[0].flags.writeable,'Fortran':bool(answer[0].flags.f_contiguous)}
        aliases.append(row);save(out/'factor-aliases.json',aliases)
        require(row['shape']==[NAUX,NAUX] and row['shares_memory'] and pointer==row['factor_pointer'] and row['readonly'] and row['Fortran'],'Factor storage contract differs')
        stage('RI_factor_complete');return answer
    memory.factor_inplace=factor;memory.private_scipy.linalg.cho_factor=factor
    stage('saved_density_load_start');density,density_summary=saved_density();save(out/'density-validation.json',density_summary)
    stage('basis_build_start')
    mol=gto.M(atom=parent_atoms(),unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,verbose=4,max_memory=8000,output=str(out/'native.log'))
    require((mol.natm,mol.nao,mol.nelectron)==(196,NAO,1568) and sum(mol.atom_charges())-mol.nelectron==-8,'Parent dimensions differ')
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
    mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=20;mf.chkfile=None
    if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
    solvent=memory.MemoryPCM(mol);solvent.method='C-PCM';solvent.eps=78.4;solvent.lebedev_order=17;solvent.vdw_scale=1.2;solvent.r_probe=0.;solvent.frozen=False
    solvent.build=forbidden;mf.kernel=mf.scf=forbidden
    def metric(row):
        with (out/'metric-calls.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    mf=memory.install(memory.qualified.attach(mf,solvent),metric)
    stage('setup_complete');require(pcm_unbuilt(solvent),'PCM allocated during setup')
    stage('first_J_start');jstart=time.monotonic();j=single_j(mf,density);elapsed=time.monotonic()-jstart
    stage('first_J_returned',first_J_seconds=elapsed,J_calls=mf._rij_calls,SCFs_launched=0)
    obj=mf._rij_df;rf=obj._vjopt.j2c[0]
    asymmetry=float(np.max(np.abs(j-j.T)))
    checks={'J_shape':j.shape==(NAO,NAO),'J_finite':bool(np.isfinite(j).all()),'J_symmetric':bool(asymmetry<=1e-10),
            'one_J':mf._rij_calls==1,'one_factor':len(aliases)==1,'no_ERI':mf._eri is None,
            'no_3index':obj._cderi is None and obj._cderi_to_save is None,'metric_cd':obj._vjopt.j2c_type=='cd',
            'metric_shape':rf.shape==(NAUX,NAUX),'factor_immutable_Fortran':not rf.flags.writeable and rf.flags.f_contiguous,
            'auxbasis':obj.auxbasis=='def2-universal-jkfit','no_PCM':pcm_unbuilt(solvent)}
    save(out/'checks.json',checks);np.save(out/'J.npy',j,allow_pickle=False)
    require(validate_gate()==gate,'Gate changed during first-J probe')
    result={'status':'PASS_BOUNDED_FIRST_J_ONLY' if all(checks.values()) else 'FAIL_FIRST_J_CHECKS','checks':checks,
            'first_J_seconds':elapsed,'J_max_asymmetry':asymmetry,'J_calls':mf._rij_calls,'SCFs_launched':0,'J_sha256':sha(out/'J.npy'),
            'physical_admission':False,'parent_SCF_readiness':False,'whole_SCF_performance_claim':False}
    save(out/'result.json',result);mol.stdout.close();return 0 if all(checks.values()) else 1


def launch():
    gate=validate_gate();out=owned(BASE/'run-v1');out.mkdir(exist_ok=False);save(out/'launch-gate.json',gate)
    supervisor=load('unchanged_supervisor',LAB/'parent-pilot/pilot.py')
    supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':'4','OMP_DYNAMIC':'FALSE'}
    python=read(QUAL/'preparation.json')['pins']['runtime']['python']
    receipt=supervisor.monitored_run([python,'-B',str(BASE/'run.py'),'--worker'],out,WALL,RSS)
    result={};result_error=None;j_digest=None;j_hash_error=None
    try:
        if (out/'result.json').exists():result=read(out/'result.json')
        require(isinstance(result,dict),'Worker result must be a JSON object')
    except Exception:result_error=traceback.format_exc()
    try:
        if (out/'J.npy').is_file():j_digest=sha(out/'J.npy')
    except Exception:j_hash_error=traceback.format_exc()
    gate_error=None
    try:same=validate_gate()==gate
    except Exception:
        same=False;gate_error=traceback.format_exc()
    passed=result_error is None and j_hash_error is None and same and accepted(receipt) and j_digest is not None and result.get('J_sha256')==j_digest and result.get('status')=='PASS_BOUNDED_FIRST_J_ONLY' and type(result.get('J_calls')) is int and result['J_calls']==1 and type(result.get('SCFs_launched')) is int and result['SCFs_launched']==0 and isinstance(result.get('checks'),dict) and bool(result['checks']) and all(v is True for v in result['checks'].values())
    save(out/'launch-result.json',{'status':'PASS_BOUNDED_FIRST_J_ONLY' if passed else 'INCOMPLETE_OR_FAILED_FIRST_J',
         'receipt':receipt,'worker_result':result,'worker_result_error':result_error,
         'J_sha256_observed':j_digest,'J_hash_error':j_hash_error,'gate_unchanged':same,'gate_error':gate_error,'maximum_children':1,'maximum_J_calls':1,'maximum_SCFs':0,
         'physical_admission':False,'parent_SCF_readiness':False})
    return 0 if passed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif args==['--worker']:
        try:sys.exit(worker())
        except Exception:
            out=owned(BASE/'run-v1')
            if out.exists():save(out/'failure.json',{'exception':traceback.format_exc(),'SCFs_launched':0,'physical_admission':False})
            raise
    else:raise SystemExit('Use --prepare, --gate-check or --launch; no default execution')
