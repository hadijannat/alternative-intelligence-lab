import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
WALL=1000
RSS=10*2**30
NAO=3068
CHUNK_ROWS=16
ATOL=1e-10
METHOD={'atoms':196,'nao':3068,'electrons':1568,'charge':-8,'spin':0,'cart':False,
        'basis':'def2-svp','ecp':{'Mo':'def2-svp'},'xc':'PBE','grid_level':2,
        'direct_scf':True,'direct_scf_tol':1e-13,'auxbasis':'def2-universal-jkfit','naux':19612,
        'PCM_method':'C-PCM','eps':78.4,'lebedev_order':17,'vdw_scale':1.2,'r_probe':0.,'frozen':False}
PASS='PASS_BOUNDED_PARENT_J_REPEATABILITY_ONLY'
NONPASS='COMPLETED_WITH_NUMERICAL_NONPASS'
INCOMPLETE='INCOMPLETE_OR_FAILED_PARENT_J_REPEATABILITY'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


signed=load('frozen_signed_helpers',LAB/'parent-signed-j-diagnostic/run.py')
first=signed.first
qualification=signed.qualification
read,save,sha,require=signed.read,signed.save,signed.sha,signed.require
EXTERNAL=first.BASE/'run-v1/J.npy'
COMPARISONS=(('same_sign','J2-J1','J2.npy','J1.npy',1),
             ('sign_reversal','J3+J1','J3.npy','J1.npy',-1),
             ('sign_reversal','J3+J2','J3.npy','J2.npy',-1),
             ('external_run','J1-Jold','J1.npy',None,1),
             ('external_run','J2-Jold','J2.npy',None,1),
             ('external_run','J3+Jold','J3.npy',None,-1))


def owned(path):
    path=Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()) and path!=BASE.resolve(),'Output outside repeatability campaign')
    return path


def write_new(path,value):
    with owned(path).open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')


def manifest():
    pins=signed.manifest()
    root=signed.BASE
    paths=[root/name for name in ('preparation.json','independent-root-review.json','INDEPENDENT_REVIEW.md','REPORT.md')]
    paths.extend(sorted(p for p in (root/'run-v1').rglob('*') if p.is_file()))
    pins['signed_outcome']={str(p):sha(p) for p in paths}
    pins['repeatability_driver']={str(BASE/name):sha(BASE/name) for name in ('run.py','test_run.py','PROTOCOL.md')}
    pins['preparation_history']={str(p):sha(p) for p in sorted((BASE/'preparation-history').iterdir()) if p.is_file()}
    return pins


def prepare():
    require(not (BASE/'preparation.json').exists(),'Already prepared')
    pins=manifest();runtime=read(first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve()==Path(runtime['python']).resolve(),'Require qualified interpreter')
    require(qualification.runtime_pins()==runtime,'Qualified runtime changed')
    result=read(first.BASE/'run-v1/result.json')
    require(first.accepted(read(first.BASE/'run-v1/supervisor.json')) and result.get('status')=='PASS_BOUNDED_FIRST_J_ONLY'
            and result.get('J_sha256')==sha(EXTERNAL) and result.get('checks')
            and all(v is True for v in result['checks'].values()),'External first J not accepted')
    first.parent_atoms();density,summary=first.saved_density();density_sha256=array_digest(density);del density
    require(manifest()==pins,'Inputs changed during preparation')
    write_new(BASE/'preparation.json',{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins,
              'density':summary,'positive_density_sha256':density_sha256,'wall_cap_seconds':WALL,
              'sampled_RSS_guard_bytes':RSS,'maximum_children':1,'maximum_J_calls':3,
              'operators_executed':0,'SCFs_launched':0,'molecule_built':False,
              'sequence':[1,1,-1],'method':METHOD,'expected_output_payload_bytes':3*NAO*NAO*8,
              'absolute_tolerance':ATOL,'relative_tolerance':0,'physical_admission':False})


def validate_gate():
    preparation=read(BASE/'preparation.json');current=manifest()
    require(preparation.get('status')=='PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
            and preparation['pins']==current,'Preparation pins changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_PARENT_J_REPEATABILITY_DIAGNOSTIC'
            and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent root approval missing')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json')
            and review.get('qualification_artifacts')==current['qualification'],'Review binding differs')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json'),
            'qualification_artifacts':current['qualification']}


def array_digest(array):
    import numpy as np
    require(array.dtype==np.float64 and (array.flags.c_contiguous or array.flags.f_contiguous),'Hash requires contiguous float64')
    flat=array.ravel(order='K');require(np.shares_memory(flat,array),'Array hash would copy storage')
    view=memoryview(flat).cast('B');digest=hashlib.sha256()
    for offset in range(0,len(view),1024*1024):digest.update(view[offset:offset+1024*1024])
    return digest.hexdigest()


def molecule_state(mol,expected=None):
    arrays={}
    for name in ('_atm','_bas','_env'):
        array=getattr(mol,name)
        require(array.flags.c_contiguous,'Molecule fingerprint requires contiguous native storage')
        arrays[name]={'shape':list(array.shape),'dtype':str(array.dtype),
                      'sha256':hashlib.sha256(memoryview(array).cast('B')).hexdigest()}
    state={'arrays':arrays,'natm':mol.natm,'nao':mol.nao,'nelectron':mol.nelectron,
           'charge':mol.charge,'spin':mol.spin,'cart':mol.cart}
    require(expected is None or state==expected,'Molecule state changed')
    return state


def compare(matrix,reference,multiplier):
    import numpy as np
    require(matrix.dtype==reference.dtype==np.float64 and matrix.shape==reference.shape==(NAO,NAO),'Comparison shape/dtype differs')
    require(multiplier in (-1,1),'Invalid reference sign')
    maximum=-1.;argmax=None;above=0;matrix_magnitude=0.;reference_magnitude=0.;values=None
    for start in range(0,NAO,CHUNK_ROWS):
        a=matrix[start:start+CHUNK_ROWS];b=reference[start:start+CHUNK_ROWS]
        require(np.isfinite(a).all() and np.isfinite(b).all(),'Nonfinite comparison input')
        difference=np.abs(a-multiplier*b);index=int(np.argmax(difference));row,col=np.unravel_index(index,difference.shape)
        local=float(difference[row,col]);above+=int(np.count_nonzero(difference>ATOL))
        matrix_magnitude=max(matrix_magnitude,float(np.max(np.abs(a))))
        reference_magnitude=max(reference_magnitude,float(np.max(np.abs(b))))
        if local>maximum:
            maximum=local;argmax=[start+int(row),int(col)]
            values={'actual':float(a[row,col]),'reference':float(b[row,col]),'expected':float(multiplier*b[row,col])}
    return {'pass':maximum<=ATOL,'max_absolute_error':maximum,'argmax':argmax,
            'values_at_argmax':values,'entries_above_tolerance':above,
            'matrix_max_abs':matrix_magnitude,'reference_max_abs':reference_magnitude,
            'reference_multiplier':multiplier,'absolute_tolerance':ATOL,'relative_tolerance':0,'chunk_rows':CHUNK_ROWS}


def recompute(out):
    import numpy as np
    results={};missing={};errors={}
    for category,name,a,b,multiplier in COMPARISONS:
        paths=[out/a,out/b if b is not None else EXTERNAL]
        absent=[str(p) for p in paths if not p.is_file()]
        if absent:missing[name]=absent;continue
        matrices=[]
        try:
            for p in paths:matrices.append(np.load(p,allow_pickle=False,mmap_mode='r'))
            results[name]={'category':category,**compare(*matrices,multiplier)}
        except Exception:errors[name]=traceback.format_exc()
        finally:
            for matrix in matrices:
                if getattr(matrix,'_mmap',None) is not None:matrix._mmap.close()
    categories={}
    for category in ('same_sign','sign_reversal','external_run'):
        names=[name for cat,name,*rest in COMPARISONS if cat==category]
        categories[category]=('INCOMPLETE' if any(n not in results for n in names) else
                              'PASS' if all(results[n]['pass'] for n in names) else 'NONPASS')
    return {'comparisons':results,'categories':categories,'missing':missing,'errors':errors,
            'external_reference_is_independent_algorithm':False,'sign_and_call_order_confounded':True}


def save_returned(out,number,matrix,stage):
    import numpy as np
    path=owned(out/f'J{number}.npy')
    stage('returned_J_save_start',call=number)
    with path.open('xb') as stream:np.save(stream,matrix,allow_pickle=False)
    digest=sha(path);stage('returned_J_saved_closed',call=number,sha256=digest)
    return digest


def post_call_file(out,number,stage):
    stage('post_call_file_start',call=number)
    with owned(out/f'post-call-{number}.bin').open('xb',buffering=4096) as stream:
        stream.write(b'parent J repeatability post-call checkpoint\n')
    stage('post_call_file_closed',call=number)


def checked_factor(obj,creation,previous=None):
    state=signed.factor_state(obj)
    state['content_sha256']=array_digest(obj._vjopt.j2c[0])
    require(state['pointer']==creation['factor_pointer']
            and state['content_sha256']==creation['content_sha256'],'Factor content/storage changed')
    require(previous is None or state==previous,'Factor state changed between calls')
    return state


def run_calls(mf,out,density_loader,runtime_guard,storage_guard,stage,expected_positive_digest):
    import numpy as np
    records=[]
    for number,multiplier in enumerate((1,1,-1),1):
        runtime_guard();signed.restrict(mf)
        require(mf._rij_calls==number-1,'Native call counter before request differs')
        density,summary=density_loader();positive=array_digest(density)
        require(positive==expected_positive_digest,'Reloaded positive P0 differs')
        if multiplier==-1:density*=-1
        requested=array_digest(density)
        write_new(out/f'input-{number}.json',{'source':summary,'multiplier':multiplier,'positive_sha256':positive,'requested_sha256':requested})
        stage('native_J_start',call=number,multiplier=multiplier)
        matrix=mf.get_j(dm=density)
        stage('native_J_returned',call=number)
        digest=save_returned(out,number,matrix,stage);del matrix
        record={'call':number,'multiplier':multiplier,'J_sha256':digest}
        records.append(record);save(out/'call-records.json',records)
        require(mf._rij_calls==number,'Native call counter after return differs')
        require(array_digest(density)==requested,'Native call mutated requested density');del density
        matrix=np.load(out/f'J{number}.npy',allow_pickle=False,mmap_mode='r')
        try:record['matrix_checks']=signed.matrix_checks(matrix)
        finally:matrix._mmap.close();del matrix
        save(out/'call-records.json',records)
        require(record['matrix_checks']['finite'],'Nonfinite returned J')
        record['storage']=storage_guard(number);runtime_guard()
        save(out/'call-records.json',records)
        comparisons=recompute(out);save(out/'comparisons.json',comparisons)
        require(not comparisons['errors'],'Comparison invariant failed')
        post_call_file(out,number,stage);stage('full_arrays_released',call=number)
    return records,comparisons


def setup(out,stage,runtime):
    import numpy as np
    from pyscf import dft,gto,lib
    molecule_baseline=None
    def runtime_guard():
        require(lib.num_threads()==4 and os.environ.get('OMP_NUM_THREADS')=='4'
                and os.environ.get('OMP_DYNAMIC')=='FALSE','OpenMP controls differ')
        require(all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'BLAS controls differ')
        require(qualification.runtime_pins()==runtime,'Runtime changed')
        if molecule_baseline is not None:molecule_state(mol,molecule_baseline)
    runtime_guard()
    save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,
         'loaded_native_files':{str(p):sha(p) for p in sorted(qualification.loaded_native_files())}})
    memory=load('immutable_repeatability_memory',LAB/'cpcm-rij-memory/memory.py');aliases=[];metrics=[]
    original=memory.factor_inplace
    def factor(matrix,*args,**kwargs):
        require(not aliases,'Second factorization forbidden');pointer=matrix.ctypes.data
        stage('RI_factor_start',shape=list(matrix.shape));answer=original(matrix,*args,**kwargs)
        row={'shape':list(matrix.shape),'input_pointer':pointer,'factor_pointer':answer[0].ctypes.data,
             'shares_memory':bool(np.shares_memory(matrix,answer[0])),
             'readonly':not answer[0].flags.writeable,'Fortran':bool(answer[0].flags.f_contiguous),
             'content_sha256':array_digest(answer[0])}
        aliases.append(row);save(out/'factor-aliases.json',aliases)
        require(row['shape']==[signed.NAUX,signed.NAUX] and row['shares_memory']
                and pointer==row['factor_pointer'] and row['readonly'] and row['Fortran'],'Factor alias contract differs')
        stage('RI_factor_complete');return answer
    memory.factor_inplace=factor;memory.private_scipy.linalg.cho_factor=factor
    stage('basis_build_start')
    mol=gto.M(atom=first.parent_atoms(),unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,
              verbose=4,max_memory=8000,output=str(out/'native.log'))
    require((mol.natm,mol.nao,mol.nelectron,mol.charge,mol.spin)==(196,NAO,1568,-8,0) and not mol.cart,'Parent dimensions differ')
    molecule_baseline=molecule_state(mol);save(out/'molecule-state.json',molecule_baseline)
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13;mf.chkfile=None
    if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
    solvent=memory.MemoryPCM(mol);solvent.method='C-PCM';solvent.eps=78.4;solvent.lebedev_order=17
    solvent.vdw_scale=1.2;solvent.r_probe=0.;solvent.frozen=False;solvent.build=signed.forbidden
    def metric(row):
        metrics.append(row)
        with (out/'metric-calls.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
    mf=memory.qualified.attach(mf,solvent);signed.restrict(mf)
    mf=memory.install(mf,metric);signed.restrict(mf)
    require(first.pcm_unbuilt(solvent) and mf._rij_calls==0 and mf._rij_df._vjopt is None,'Setup not fresh')
    states=[]
    def storage_guard(number):
        require(len(aliases)==1,'Factor count differs')
        state=checked_factor(mf._rij_df,aliases[0],states[0] if states else None)
        require(len(metrics)==number and [r['call'] for r in metrics]==list(range(1,number+1)),'Metric call count differs')
        require(mf._eri is None and mf._rij_df._cderi is None and mf._rij_df._cderi_to_save is None
                and first.pcm_unbuilt(solvent),'Unexpected ERI/three-index/PCM state')
        require(mf.xc.upper()=='PBE' and mf.direct_scf and mf.direct_scf_tol==1e-13
                and mf.grids.level==2 and mf._rij_df.auxbasis=='def2-universal-jkfit'
                and (solvent.method,solvent.eps,solvent.lebedev_order,solvent.vdw_scale,solvent.r_probe,solvent.frozen)
                ==('C-PCM',78.4,17,1.2,0.,False),'Method changed')
        states.append(state);save(out/'factor-states.json',states);return state
    stage('setup_complete')
    return mf,runtime_guard,storage_guard


def worker():
    out=owned(BASE/'run-v1');gate=validate_gate()
    require(read(out/'launch-gate.json')==gate,'Launch gate differs')
    write_new(out/'worker-started.json',{'pid':os.getpid(),'maximum_J_calls':3,'maximum_SCFs':0})
    start=time.monotonic()
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (out/'stages.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    stage('worker_started',J_calls=0,SCFs_launched=0)
    runtime=read(first.QUAL/'preparation.json')['pins']['runtime']
    mf,runtime_guard,storage_guard=setup(out,stage,runtime)
    records,comparisons=run_calls(mf,out,first.saved_density,runtime_guard,storage_guard,stage,
                                  read(BASE/'preparation.json')['positive_density_sha256'])
    require(validate_gate()==gate,'Gate changed during work')
    passed=(all(row['matrix_checks']['symmetric'] for row in records)
            and all(v=='PASS' for v in comparisons['categories'].values()))
    result={'status':PASS if passed else NONPASS,'J_calls':mf._rij_calls,'metric_calls':len(records),
            'factor_count':1,'SCFs_launched':0,'gate_unchanged':True,'invariants_passed':True,
            'numerical_pass':passed,'categories':comparisons['categories'],'J_sha256':{f'J{r["call"]}.npy':r['J_sha256'] for r in records},
            'physical_admission':False,'parent_SCF_readiness':False,'sign_and_call_order_confounded':True}
    save(out/'result.json',result);mf.mol.stdout.close();return 0


def collect_artifacts(out):
    required=['J1.npy','J2.npy','J3.npy','post-call-1.bin','post-call-2.bin','post-call-3.bin',
              'input-1.json','input-2.json','input-3.json','call-records.json','comparisons.json','factor-aliases.json',
              'factor-states.json','metric-calls.jsonl','runtime-observation.json','molecule-state.json','stages.jsonl','result.json']
    hashes={};missing=[];errors={}
    existing=[str(p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file()]
    for name in dict.fromkeys(required+existing):
        path=out/name
        if not path.is_file():missing.append(name);continue
        try:
            hashes[name]=sha(path)
            if name in required:require(path.stat().st_size>0,'Empty artifact')
        except Exception:errors[name]=traceback.format_exc()
    return {'sha256':hashes,'missing':missing,'errors':errors}


def accepted_result(result):
    return (isinstance(result,dict) and result.get('status') in (PASS,NONPASS)
            and result.get('invariants_passed') is True and result.get('gate_unchanged') is True
            and result.get('physical_admission') is False and result.get('parent_SCF_readiness') is False
            and result.get('sign_and_call_order_confounded') is True
            and type(result.get('numerical_pass')) is bool and (result['status']==PASS)==result['numerical_pass']
            and isinstance(result.get('categories'),dict)
            and set(result['categories'])=={'same_sign','sign_reversal','external_run'}
            and all(v in ('PASS','NONPASS') for v in result['categories'].values())
            and (not result['numerical_pass'] or all(v=='PASS' for v in result['categories'].values()))
            and all(type(result.get(k)) is int and result[k]==v for k,v in
                    {'J_calls':3,'metric_calls':3,'factor_count':1,'SCFs_launched':0}.items()))


def launch():
    gate=validate_gate();out=owned(BASE/'run-v1');out.mkdir(exist_ok=False);write_new(out/'launch-gate.json',gate)
    supervisor=load('immutable_repeatability_supervisor',LAB/'parent-pilot/pilot.py')
    supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':'4','OMP_DYNAMIC':'FALSE'}
    python=read(first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt=supervisor.monitored_run([python,'-B',str(BASE/'run.py'),'--worker'],out,WALL,RSS)
    result={};errors={}
    try:
        if (out/'result.json').exists():result=read(out/'result.json')
        require(isinstance(result,dict),'Malformed worker result')
    except Exception:errors['result']=traceback.format_exc()
    try:same=validate_gate()==gate
    except Exception:same=False;errors['gate']=traceback.format_exc()
    artifacts=collect_artifacts(out)
    completed=(not errors and same and first.accepted(receipt) and accepted_result(result)
               and not artifacts['missing'] and not artifacts['errors']
               and result.get('J_sha256')=={name:artifacts['sha256'].get(name) for name in ('J1.npy','J2.npy','J3.npy')})
    save(out/'launch-result.json',{'status':result['status'] if completed else INCOMPLETE,
         'receipt':receipt,'worker_result':result,'errors':errors,'artifacts':artifacts,'gate_unchanged':same,
         'maximum_children':1,'maximum_J_calls':3,'maximum_SCFs':0,'physical_admission':False,'parent_SCF_readiness':False})
    return 0 if completed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--recompute']:print(json.dumps(recompute(BASE/'run-v1'),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif args==['--worker']:
        try:sys.exit(worker())
        except Exception:
            out=owned(BASE/'run-v1')
            if out.exists():save(out/'failure.json',{'exception':traceback.format_exc(),'SCFs_launched':0,'physical_admission':False})
            raise
    else:raise SystemExit('Use --prepare, --gate-check, --recompute or --launch; no default execution')
