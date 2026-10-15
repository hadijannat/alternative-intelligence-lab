"""Two bounded retrospective small-case children; no parent operator or SCF."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback
import types

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
FIRST=LAB/'parent-openmp-first-j-v2'
QUAL=LAB/'parent-openmp-qualification-v2'
WALL=180
RSS=2*2**30
CASE='new-external'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


first=load('completed_first_j',FIRST/'run.py')
handoff=load('single_use_handoff',BASE/'handoff.py')
read,save,accepted,require=first.read,first.save,first.accepted,first.require
sha=handoff.sha


def owned(path):
    path=Path(path).resolve();require(path.is_relative_to(BASE.resolve()) and path!=BASE.resolve(),'Output outside saved-J qualification');return path


def prerequisites():
    gate=first.validate_gate();out=FIRST/'run-v1';launch=read(out/'launch-result.json');result=read(out/'result.json');receipt=read(out/'supervisor.json')
    require(launch.get('status')=='PASS_BOUNDED_FIRST_J_ONLY' and launch.get('gate_unchanged') is True
            and launch.get('receipt')==receipt and accepted(receipt) and read(out/'launch-gate.json')==gate,'First-J terminal provenance failed')
    require(result.get('status')=='PASS_BOUNDED_FIRST_J_ONLY' and type(result.get('J_calls')) is int and result['J_calls']==1
            and type(result.get('SCFs_launched')) is int and result['SCFs_launched']==0
            and result.get('checks') and all(v is True for v in result['checks'].values())
            and sha(out/'J.npy')==result.get('J_sha256')==launch.get('J_sha256_observed'),'First-J result/digest failed')
    paths=[FIRST/name for name in ('run.py','test_run.py','PROTOCOL.md','preparation.json','independent-root-review.json','NEXT_STEP.md')]
    paths.extend(out/name for name in ('launch-result.json','result.json','supervisor.json','launch-gate.json','J.npy','density-validation.json','runtime-observation.json','factor-aliases.json','stages.jsonl'))
    return {str(p):sha(p) for p in paths}


def proof():
    out=QUAL/'run-v1/threads-4/run-v1/operators-new-external'
    paths={'artifact':out/'arrays.npz','receipt':out/'supervisor.json','result':out/'result.json'}
    import numpy as np
    with np.load(paths['artifact'],allow_pickle=False) as archive:
        digest=handoff.density_digest(archive['initial_P'])
    return {**{k:str(p) for k,p in paths.items()},**{k+'_sha256':sha(p) for k,p in paths.items()},
            'case':CASE,'density_key':'initial_P','density_sha256':digest,'j_key':'initial_Jmemory'}


def manifest():
    previous=prerequisites();small_proof=proof();handoff.verify_provenance(small_proof)
    paths=[QUAL/'run-v1/threads-4/run-v1/scf-new-external'/n for n in ('arrays.npz','result.json','supervisor.json')]
    paths.extend(LAB/'rij-jkfit-qualification/raw'/n for n in ('new.xyz','new-case.json'))
    return {'first_J':previous,'runtime_qualification':first.qualification_artifacts(),'proof':small_proof,
            'small_reference':{str(p):sha(p) for p in paths},
            'driver':{str(BASE/n):sha(BASE/n) for n in ('run.py','handoff.py','test_run.py','PROTOCOL.md')}}


def prepare():
    path=owned(BASE/'preparation.json');require(not path.exists(),'Already prepared');pins=manifest()
    save(path,{'status':'PREPARED_PENDING_ROOT_REVIEW','pins':pins,'maximum_children':2,'maximum_SCFs':1,'parent_run':False,'fresh_holdout':False})


def validate_gate():
    preparation=read(BASE/'preparation.json');require(preparation['pins']==manifest(),'Frozen preparation changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_SMALL_SAVED_J_QUALIFICATION' and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent root review missing')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json'),'Review preparation binding differs')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json')}


def phase_accepted(receipt,result,phase):
    return bool(accepted(receipt) and isinstance(result,dict) and result.get('case')==CASE and result.get('phase')==phase
                and result.get('status')=='PASS_'+phase.upper() and type(result.get('SCFs_launched')) is int
                and result['SCFs_launched']==(1 if phase=='scf' else 0)
                and isinstance(result.get('checks'),list) and result['checks']
                and all(isinstance(c,dict) and c.get('pass') is True for c in result['checks']))


def worker(phase):
    out=owned(BASE/'run-v1'/phase);gate=validate_gate();require(read(BASE/'run-v1/launch-gate.json')==gate,'Launch review changed')
    if phase=='scf':
        receipt=read(BASE/'run-v1/operator-receipt.json')
        require(receipt==read(BASE/'run-v1/operators/supervisor.json') and phase_accepted(receipt,read(BASE/'run-v1/operators/result.json'),'operators'),'Operator gate failed')
    with (out/'worker-started.json').open('x') as f:json.dump({'phase':phase},f)
    import numpy as np
    from pyscf import dft,gto,lib
    from pyscf.scf import hf
    require(lib.num_threads()==4 and os.environ.get('OMP_NUM_THREADS')=='4','OpenMP thread mismatch')
    require(all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'BLAS thread mismatch')
    runtime=first.qualification.runtime_pins()
    require(runtime==read(QUAL/'preparation.json')['pins']['runtime'],'Actual runtime inventory/interpreter differs')
    save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,'runtime':runtime})
    m=load('unchanged_memory',LAB/'cpcm-rij-memory/memory.py');start=time.monotonic()
    record={'case':CASE,'phase':phase,'checks':[],'SCFs_launched':0,'parent_run':False,'fresh_holdout':False,'physical_admission':False,'native_requests':[],'veff_stages':[],'aliases':[]};arrays={}
    def flush():record['elapsed_seconds']=time.monotonic()-start;save(out/'result.json',record)
    def check(name,value,passed):record['checks'].append({'name':name,'value':value,'pass':bool(passed)});flush()
    factor=m.factor_inplace
    def factor_record(matrix,*args,**kwargs):
        pointer=matrix.ctypes.data;answer=factor(matrix,*args,**kwargs)
        row={'shape':list(matrix.shape),'shares_memory':bool(np.shares_memory(matrix,answer[0])),'same_pointer':pointer==answer[0].ctypes.data,'readonly':not answer[0].flags.writeable,'Fortran':bool(answer[0].flags.f_contiguous)}
        record['aliases'].append(row);flush();require(all(row[k] for k in ('shares_memory','same_pointer','readonly','Fortran')),'Factor alias contract failed');return answer
    m.factor_inplace=factor_record;m.private_scipy.linalg.cho_factor=factor_record
    frozen_proof=read(BASE/'preparation.json')['pins']['proof']
    with np.load(frozen_proof['artifact'],allow_pickle=False) as saved:
        initial=saved['initial_P'];delta=saved['deltaP']
    initial.flags.writeable=False;initial_digest=handoff.density_digest(initial)
    lines=(LAB/'rij-jkfit-qualification/raw/new.xyz').read_text().splitlines();atoms=[(s[0],tuple(map(float,s[1:]))) for line in lines[2:] if (s:=line.split())]
    require(len(atoms)==int(lines[0])==11,'Small-case geometry differs')
    require(read(LAB/'rij-jkfit-qualification/raw/new-case.json')['charge']==0,'Small-case charge differs')
    mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=0,spin=0,max_memory=512,verbose=4,output=str(out/'native.log'))
    factor_ids={}
    def storage(mf,name):
        obj=getattr(mf,'_rij_df',None);s=mf.with_solvent;values={'no_ERI':mf._eri is None,'no_S':'S' not in (s._intermediates or {})}
        if obj is not None:
            values['no_3index']=obj._cderi is None and obj._cderi_to_save is None
            if obj._vjopt is not None:
                values['metric_cd']=obj._vjopt.j2c_type=='cd';f=obj._vjopt.j2c[0];m.finite_chunks(f)
                values['RI_immutable_Fortran']=not f.flags.writeable and f.flags.f_contiguous
                values['RI_shape']=f.shape==(obj.auxmol.nao,obj.auxmol.nao)
                key=(name,'RI');values['RI_reuse']=factor_ids.setdefault(key,id(f))==id(f)
        if s._intermediates and 'factor' in s._intermediates:
            f=s._intermediates['factor'][0];m.finite_chunks(f);values['PCM_immutable_Fortran']=not f.flags.writeable and f.flags.f_contiguous
            values['PCM_shape']=f.shape==(len(s.surface['grid_coords']),len(s.surface['grid_coords']))
            key=(name,'PCM');values['PCM_reuse']=factor_ids.setdefault(key,id(f))==id(f)
        check(name+'/storage',values,all(values.values()))
    def configured(name,cached=False,direct=False):
        mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
        mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=60;mf.chkfile=None
        if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
        s=m.MemoryPCM(mol);s.method='C-PCM';s.eps=78.4;s.lebedev_order=17;s.vdw_scale=1.2;s.r_probe=0.;s.frozen=False
        mf=m.qualified.attach(mf,s)
        if direct:mf.get_hcore();mf.get_jk=types.MethodType(hf.SCF.get_jk,mf);return mf
        def metric(row):
            with (out/'metric-calls.jsonl').open('a') as f:f.write(json.dumps({'object':name,**row})+'\n')
        mf=m.install(mf,metric);native=mf.get_jk
        def audited(self,mol=None,dm=None,hermi=1,with_j=True,with_k=True,omega=None):
            record['native_requests'].append({'object':name,'density_sha256':handoff.density_digest(np.asarray(dm)),
                 'PCM_present':bool(self.with_solvent._intermediates),'RI_present':self._rij_df._vjopt is not None});flush()
            return native(mol=mol,dm=dm,hermi=hermi,with_j=with_j,with_k=with_k,omega=omega)
        mf.get_jk=types.MethodType(audited,mf)
        if cached:handoff.install(mf,initial,frozen_proof)
        veff=mf.get_veff
        def audited_veff(self,*args,**kwargs):
            value=veff(*args,**kwargs)
            record['veff_stages'].append({'object':name,'saved_J_hits':getattr(self,'saved_J_hits',0),'native_calls':self._rij_calls,
                 'PCM_present':bool(self.with_solvent._intermediates),'RI_present':self._rij_df._vjopt is not None});storage(self,name);return value
        mf.get_veff=types.MethodType(audited_veff,mf);return mf
    def compare_veff(label,a,b):
        for role,value in (('cached',a),('uncached',b)):
            arrays[label+'_'+role+'_veff']=np.asarray(value)
            arrays[label+'_'+role+'_PCM_V']=value.v_solvent
            arrays[label+'_'+role+'_PCM_energy']=np.array(value.e_solvent)
            arrays[label+'_'+role+'_ecoul']=np.array(value.ecoul)
            arrays[label+'_'+role+'_exc']=np.array(value.exc)
        for name,x,y in (('veff',a,b),('PCM_V',a.v_solvent,b.v_solvent),('PCM_energy',np.array(a.e_solvent),np.array(b.e_solvent)),('ecoul',np.array(a.ecoul),np.array(b.ecoul)),('exc',np.array(a.exc),np.array(b.exc))):
            error=float(np.max(np.abs(x-y)));check(label+'/'+name,error,np.isfinite(error) and error<=1e-10)
    cached=configured('cached',cached=True)
    if phase=='operators':
        uncached=configured('uncached');v0=cached.get_veff(dm=initial);u0=uncached.get_veff(dm=initial)
        compare_veff('initial',v0,u0);perturbed=initial+delta
        v1=cached.get_veff(dm=perturbed,dm_last=initial,vhf_last=v0);u1=uncached.get_veff(dm=perturbed,dm_last=initial,vhf_last=u0)
        compare_veff('incremental',v1,u1)
        arrays.update(initial_P=initial,perturbed_P=perturbed,deltaP=delta,initial_cached_veff=v0,initial_uncached_veff=u0,incremental_cached_veff=v1,incremental_uncached_veff=u1)
        requests=[r for r in record['native_requests'] if r['object']=='cached']
        check('incremental_density',requests[0]['density_sha256'],requests[0]['density_sha256']==handoff.density_digest(perturbed-initial))
        cached.get_veff(dm=perturbed,dm_last=perturbed,vhf_last=v1)
    else:
        reference=read(QUAL/'run-v1/threads-4/run-v1/scf-new-external/result.json')
        record['SCFs_launched']=1;flush()
        def callback(env):
            with (out/'iterations.jsonl').open('a') as f:f.write(json.dumps({'cycle':int(env['cycle'])+1,'energy_Eh':float(env['e_tot'])})+'\n')
            storage(cached,'cached')
        cached.callback=callback;energy=float(cached.kernel(dm0=initial));dm=cached.make_rdm1();fock=cached.get_fock(dm=dm)
        residual=float(np.linalg.norm(cached.get_grad(cached.mo_coeff,cached.mo_occ,fock)))
        direct=configured('direct',direct=True);fd=direct.get_fock(dm=dm)
        direct_residual=float(np.linalg.norm(cached.get_grad(cached.mo_coeff,cached.mo_occ,fd)))
        with np.load(QUAL/'run-v1/threads-4/run-v1/scf-new-external/arrays.npz',allow_pickle=False) as saved:dm_error=float(np.max(np.abs(dm-saved['density'])))
        energy_error=abs(energy-reference['SCF']['energy_Eh']);overlap=cached.get_ovlp();trace_error=abs(np.einsum('ij,ji',dm,overlap)-mol.nelectron)
        for name,value,limit in (('energy_error',energy_error,1e-8),('density_error',dm_error,1e-5),('full_memory_Fock_gradient',residual,1e-5),('direct_Fock_gradient',direct_residual,1e-3),('electron_trace',float(trace_error),1e-8)):
            check(name,value,np.isfinite(value) and value<=limit)
        check('converged',bool(cached.converged),cached.converged);storage(direct,'direct')
        record['SCF']={'energy_Eh':energy,'cycles':cached.cycles,'converged':bool(cached.converged)}
        arrays.update(initial_P=initial,density=dm,overlap=overlap,mo_coeff=cached.mo_coeff,mo_occ=cached.mo_occ,fock=fock,direct_fock=fd)
    stages=[r for r in record['veff_stages'] if r['object']=='cached'];requests=[r for r in record['native_requests'] if r['object']=='cached']
    check('initial_PCM_before_RI',stages[0],stages[0]['saved_J_hits']==1 and stages[0]['native_calls']==0 and stages[0]['PCM_present'] and not stages[0]['RI_present'])
    check('first_native_with_PCM_no_metric',requests[0],requests[0]['PCM_present'] and not requests[0]['RI_present'])
    check('one_saved_hit_native_fallback',{'hits':cached.saved_J_hits,'native_calls':cached._rij_calls,'pending':cached._saved_J_pending},cached.saved_J_hits==1 and cached._rij_calls>0 and not cached._saved_J_pending)
    storage(cached,'cached');check('initial_density_unchanged',None,not initial.flags.writeable and handoff.density_digest(initial)==initial_digest)
    require(validate_gate()==gate,'Gate changed during worker');np.savez_compressed(out/'arrays.npz',**arrays)
    record['status']='PASS_'+phase.upper() if all(c['pass'] for c in record['checks']) else 'FAIL';flush();mol.stdout.close();return 0 if record['status'].startswith('PASS_') else 1


def launch():
    gate=validate_gate();out=owned(BASE/'run-v1');out.mkdir(exist_ok=False);save(out/'launch-gate.json',gate)
    supervisor=load('unchanged_supervisor',LAB/'parent-pilot/pilot.py');supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':'4','OMP_DYNAMIC':'FALSE'}
    python=read(QUAL/'preparation.json')['pins']['runtime']['python'];receipts={};results={};errors={}
    for phase in ('operators','scf'):
        if phase=='scf' and not phase_accepted(receipts['operators'],results['operators'],'operators'):break
        try:receipt=supervisor.monitored_run([python,'-B',str(BASE/'run.py'),'--worker',phase],out/phase,WALL,RSS)
        except Exception:
            errors[phase+'/supervisor']=traceback.format_exc()
            receipt={'returncode':None,'termination_reason':'SUPERVISOR_ERROR','monitor_error':errors[phase+'/supervisor']}
        receipts[phase]=receipt
        if phase=='operators':save(out/'operator-receipt.json',receipt)
        try:results[phase]=read(out/phase/'result.json')
        except Exception:results[phase]={};errors[phase]=traceback.format_exc()
        save(out/'terminal-progress.json',{'receipts':receipts,'results':results,'errors':errors})
    try:unchanged=validate_gate()==gate
    except Exception:unchanged=False;errors['gate']=traceback.format_exc()
    passed=unchanged and all(p in receipts and phase_accepted(receipts[p],results[p],p) for p in ('operators','scf'))
    save(out/'launch-result.json',{'status':'PASS_RETROSPECTIVE_SAVED_J_HANDOFF' if passed else 'FAIL_OR_INCOMPLETE',
         'receipts':receipts,'results':results,'errors':errors,'gate_unchanged':unchanged,'SCF_skipped':'scf' not in receipts,
         'maximum_children':2,'maximum_SCFs':1,'parent_run':False,'fresh_holdout':False,'physical_admission':False})
    return 0 if passed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif len(args)==2 and args[0]=='--worker' and args[1] in ('operators','scf'):
        try:sys.exit(worker(args[1]))
        except Exception:
            out=owned(BASE/'run-v1'/args[1]);save(out/'failure.json',{'exception':traceback.format_exc(),'parent_run':False});raise
    else:raise SystemExit('Explicit --prepare, --gate-check or --launch required')
