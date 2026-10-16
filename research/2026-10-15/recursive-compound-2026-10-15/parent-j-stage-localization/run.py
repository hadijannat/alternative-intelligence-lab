"""Three saved-density J calls; arm C substitutes rho_A only at the private solve boundary."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
spec=importlib.util.spec_from_file_location('frozen_repeatability',LAB/'parent-j-repeatability/run.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
read,save,sha,require=r.read,r.save,r.sha,r.require
ARMS=('A','B','C')
OUTPUTS=('J_A','J_B','J_fixed_rho_A')
STATUS='COMPLETED_BOUNDED_STAGE_LOCALIZATION'


def write_new(path,value):
    path=Path(path).resolve();require(path.is_relative_to(BASE.resolve()),'Output outside localization')
    with path.open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')


def manifest():
    pins=r.manifest()
    paths=[r.BASE/n for n in ('preparation.json','independent-root-review.json','INDEPENDENT_REVIEW.md','REPORT.md')]
    paths.extend(p for p in sorted((r.BASE/'run-v1').rglob('*')) if p.is_file())
    pins['repeatability_outcome']={str(p):sha(p) for p in paths}
    pins['localization']={str(BASE/n):sha(BASE/n) for n in ('run.py','test_run.py','PROTOCOL.md')}
    return pins


def prepare():
    require(not (BASE/'preparation.json').exists(),'Preparation already frozen')
    pins=manifest();runtime=read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve()==Path(runtime['python']).resolve(),'Require qualified interpreter')
    require(r.qualification.runtime_pins()==runtime,'Runtime differs')
    previous=read(r.BASE/'run-v1/result.json')
    require(r.accepted_result(previous) and r.first.accepted(read(r.BASE/'run-v1/supervisor.json')),'Repeatability did not complete')
    density,summary=r.first.saved_density();digest=r.array_digest(density);del density
    require(manifest()==pins,'Preparation inputs changed')
    write_new(BASE/'preparation.json',{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins,'density':summary,'positive_density_sha256':digest,'maximum_children':1,'maximum_J_calls':3,'SCFs_launched':0,'PCM_builds':0,'operators_executed':0,'molecule_built':False,'wall_cap_seconds':1000,'sampled_RSS_guard_bytes':10*2**30,'sequence':['ordinary_A_P0','ordinary_B_P0','controlled_C_fixed_rho_A'],'method':r.METHOD,'J_absolute_tolerance':1e-10,'J_relative_tolerance':0,'physical_admission':False})


def validate_gate():
    current=manifest();prep=read(BASE/'preparation.json')
    require(prep['pins']==current and prep['status']=='PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','Preparation changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_PARENT_J_STAGE_LOCALIZATION' and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent review required')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json') and review.get('qualification_artifacts')==current['qualification'],'Review binding changed')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json'),'qualification_artifacts':current['qualification']}


def optimizer_state(mf):
    opt=mf._rij_df._vjopt;require(opt is not None,'Optimizer not initialized')
    q=opt.q_cond
    return {'optimizer_id':id(opt),'q_cond_shape':list(q.shape),'q_cond_pointer':q.ctypes.data,'q_cond_sha256':r.array_digest(q),'cutoff':float(opt.direct_scf_tol),'molecule':r.molecule_state(mf.mol),'auxmol':r.molecule_state(mf._rij_df.auxmol),'fakemol':r.molecule_state(opt.fakemol)}


class SolveCapture:
    def __init__(self,solve,state,naux=19612):
        self.solve,self.state,self.naux=solve,state,naux
        self.arm=None;self.data={};self.baseline=None;self.returned_ids={}

    def __call__(self,factor,rhs,**kwargs):
        import numpy as np
        arm=self.arm
        require(arm in ARMS and arm not in self.data,'Unexpected or duplicate solve')
        current=self.state()
        if self.baseline is None:self.baseline=current
        require(current==self.baseline,'Optimizer invariant changed at solve')
        require(rhs.dtype==np.float64 and rhs.shape==(self.naux,1) and (rhs.flags.c_contiguous or rhs.flags.f_contiguous),'Unexpected RHS layout')
        # Native pass 1 has returned; copies stay small and no capture disk IO occurs here.
        b=rhs.copy(order='K');ordinary=self.solve(factor,rhs,**kwargs)
        require(ordinary.dtype==np.float64 and ordinary.shape==rhs.shape and (ordinary.flags.c_contiguous or ordinary.flags.f_contiguous),'Unexpected rho layout')
        self.data[arm]={'b':b,'rho_ordinary':ordinary.copy(order='K')}
        if arm=='C':
            require('A' in self.data and 'B' in self.data,'Controlled arm requires completed ordinary arms')
            answer=self.data['A']['rho_ordinary'].copy(order='K')
            require(np.array_equal(answer,self.data['A']['rho_ordinary']) and not np.shares_memory(answer,self.data['A']['rho_ordinary']),'Controlled rho copy differs')
        else:answer=ordinary
        self.returned_ids[arm]={'ordinary_returned_unchanged':answer is ordinary,'returned_pointer':answer.ctypes.data,'ordinary_pointer':ordinary.ctypes.data,'shape':list(answer.shape),'strides':list(answer.strides),'Fortran':bool(answer.flags.f_contiguous),'C_contiguous':bool(answer.flags.c_contiguous),'capture_aliases_rhs':bool(np.shares_memory(b,rhs)),'capture_aliases_ordinary':bool(np.shares_memory(self.data[arm]['rho_ordinary'],ordinary))}
        return answer


def save_array(out,name,array):
    import numpy as np
    path=out/(name+'.npy')
    with path.open('xb') as stream:np.save(stream,array,allow_pickle=False)
    return sha(path)


def vector_difference(a,b):
    import numpy as np
    require(a.shape==b.shape and a.dtype==b.dtype==np.float64 and np.isfinite(a).all() and np.isfinite(b).all(),'Invalid vectors')
    delta=a-b
    return {'exact_equal':bool(np.array_equal(a,b)),'max_absolute_difference':float(np.max(np.abs(delta))),'RMS_difference':float(np.sqrt(np.mean(delta*delta))),'acceptance_threshold':None}


def classify(out):
    import numpy as np
    results={}
    for name,other in [('J_B_minus_J_A','J_B'),('J_fixed_rho_A_minus_J_A','J_fixed_rho_A')]:
        a=np.load(out/(other+'.npy'),mmap_mode='r');b=np.load(out/'J_A.npy',mmap_mode='r')
        try:results[name]=r.compare(a,b,1)
        finally:a._mmap.close();b._mmap.close()
    vectors={}
    for field in ('b','rho_ordinary'):
        for arm in ('B','C'):
            vectors[field+'_'+arm+'_minus_A']=vector_difference(np.load(out/f'{field}_{arm}.npy'),np.load(out/f'{field}_A.npy'))
    return {'J_comparisons':results,'vector_comparisons':vectors,'controlled_output_is_ordinary_J_P0':False,'stage_causality_proven':False}


def run_calls(mf,out,capture,density_loader,runtime_guard,storage_guard,flush,stage,expected_digest):
    import numpy as np
    records=[]
    for number,(arm,label) in enumerate(zip(ARMS,OUTPUTS),1):
        runtime_guard();r.signed.restrict(mf)
        require(mf._rij_calls==number-1 and len(capture.data)==number-1,'Call count before request differs')
        density,source=density_loader();require(r.array_digest(density)==expected_digest,'P0 changed')
        if capture.baseline is not None:require(capture.state()==capture.baseline,'Optimizer changed before call')
        capture.arm=arm;stage('native_J_start',arm=arm)
        matrix=mf.get_j(dm=density)
        # Save all returned arrays, close and hash before inspecting numerical outcomes.
        hashes={label:save_array(out,label,matrix)}
        require(arm in capture.data,'Missing solve capture')
        for field,array in capture.data[arm].items():hashes[field+'_'+arm]=save_array(out,field+'_'+arm,array)
        write_new(out/f'closed-output-hashes-{arm}.json',hashes)
        flush();stage('outputs_saved_closed_hashed',arm=arm,hashes=hashes)
        require(mf._rij_calls==number and len(capture.data)==number,'Call count after return differs')
        require(r.array_digest(density)==expected_digest,'Native call mutated P0');del density
        require(capture.state()==capture.baseline,'Optimizer changed after call')
        checks=r.signed.matrix_checks(matrix);del matrix
        require(checks['finite'],'Nonfinite J')
        require(all(np.isfinite(v).all() for v in capture.data[arm].values()),'Nonfinite captured vectors')
        state=storage_guard(number);runtime_guard()
        record={'arm':arm,'output':label,'ordinary_J_P0':arm!='C','hashes':hashes,'matrix_checks':checks,'storage':state,'solve_capture':capture.returned_ids[arm],'density_source':source}
        records.append(record);write_new(out/f'call-{arm}.json',record)
    require(tuple(capture.data)==ARMS and mf._rij_calls==3,'Exactly three calls required')
    comparisons=classify(out);write_new(out/'comparisons.json',comparisons)
    return records,comparisons


def setup(out,stage,runtime):
    # Reuse frozen setup while buffering its Python receipts until the enclosing J returns.
    original_load,original_save=r.load,r.save
    pending=[];memory_holder=[];active=[False]
    def defer_save(path,value):
        if active[0]:pending.append(lambda path=path,value=value:save(path,value))
        else:save(path,value)
    def defer_stage(name,**fields):
        if active[0]:pending.append(lambda name=name,fields=fields:stage(name,**fields))
        else:stage(name,**fields)
    def load_memory(name,path):
        memory=original_load(name,path);memory_holder.append(memory)
        install=memory.install
        def deferred_install(mf,record):
            def metric(row):pending.append(lambda row=row:record(row))
            return install(mf,metric)
        memory.install=deferred_install;return memory
    r.load=load_memory;r.save=defer_save
    try:mf,guard,storage=r.setup(out,defer_stage,runtime)
    finally:r.load=original_load
    require(len(memory_holder)==1,'Unexpected setup module count')
    capture=SolveCapture(memory_holder[0].private_scipy.linalg.cho_solve,lambda:optimizer_state(mf))
    memory_holder[0].private_scipy.linalg.cho_solve=capture
    native=mf.get_j
    def call(*args,**kwargs):
        active[0]=True
        try:return native(*args,**kwargs)
        finally:active[0]=False
    mf.get_j=call
    def flush():
        while pending:pending.pop(0)()
    return mf,capture,guard,storage,flush


def worker():
    out=BASE/'run-v1';gate=validate_gate();require(read(out/'launch-gate.json')==gate,'Launch gate differs')
    write_new(out/'worker-started.json',{'pid':os.getpid(),'maximum_J_calls':3,'SCFs_launched':0})
    start=time.monotonic()
    def stage(name,**fields):
        with (out/'stages.jsonl').open('a') as stream:stream.write(json.dumps({'stage':name,'elapsed_seconds':time.monotonic()-start,**fields})+'\n')
    runtime=read(r.first.QUAL/'preparation.json')['pins']['runtime']
    mf,capture,guard,storage,flush=setup(out,stage,runtime)
    records,comparisons=run_calls(mf,out,capture,r.first.saved_density,guard,storage,flush,stage,read(BASE/'preparation.json')['positive_density_sha256'])
    require(validate_gate()==gate,'Gate changed')
    write_new(out/'optimizer-baseline.json',capture.baseline)
    write_new(out/'result.json',{'status':STATUS,'calls':3,'SCFs_launched':0,'PCM_builds':0,'invariants_passed':True,'gate_unchanged':True,'output_hashes':{k:v for record in records for k,v in record['hashes'].items()},'comparisons':comparisons,'physical_admission':False,'parent_SCF_readiness':False,'controlled_output_is_ordinary_J_P0':False})
    mf.mol.stdout.close();return 0


def launch():
    gate=validate_gate();out=BASE/'run-v1';out.mkdir(exist_ok=False);write_new(out/'launch-gate.json',gate)
    supervisor=r.load('frozen_supervisor',LAB/'parent-pilot/pilot.py')
    supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':'4','OMP_DYNAMIC':'FALSE'}
    python=read(r.first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt=supervisor.monitored_run([python,'-B',str(BASE/'run.py'),'--worker'],out,1000,10*2**30)
    result=read(out/'result.json') if (out/'result.json').exists() else {}
    hashes={p.name:sha(p) for p in out.iterdir() if p.is_file()};same=False
    try:same=validate_gate()==gate
    except Exception:pass
    complete=(r.first.accepted(receipt) and same and result.get('status')==STATUS and result.get('calls')==3 and result.get('invariants_passed') is True and result.get('SCFs_launched')==0 and result.get('PCM_builds')==0 and result.get('controlled_output_is_ordinary_J_P0') is False and result.get('output_hashes')=={name:hashes.get(name+'.npy') for name in [*OUTPUTS,*[f'{field}_{arm}' for arm in ARMS for field in ('b','rho_ordinary')]]})
    write_new(out/'launch-result.json',{'completed':complete,'receipt':receipt,'worker_result':result,'artifact_hashes':hashes,'gate_unchanged':same,'physical_admission':False,'parent_SCF_readiness':False})
    return 0 if complete else 1

if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif args==['--worker']:
        try:sys.exit(worker())
        except Exception:
            out=BASE/'run-v1'
            if out.exists():save(out/'failure.json',{'exception':traceback.format_exc(),'SCFs_launched':0,'physical_admission':False})
            raise
    else:raise SystemExit('Use --prepare, --gate-check or --launch')
