"""One bounded parent SCF; preparation and launch require independent review."""
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
SMALL=LAB/'parent-saved-j-qualification'
WALL=1800
RSS=10*2**30
STATUS='PASS_BOUNDED_PARENT_SCF'
AUDIT=LAB.parent/'.omo/evidence/parent-saved-j-result-audit'
CHECKS={'native_converged','finite_energy','electron_trace','full_unscaled_solvent_gradient',
        'storage','both_factors','saved_hit_once','native_fallback','initial_density_unchanged',
        'pins_unchanged','runtime_unchanged','initial_potential','completed_cycle','native_final_state','two_actual_factors'}
REQUIRED_EVIDENCE=('latest-complete-cycle.npz','native-final-state.npz','final-validated-state.npz',
                   'initial-potential.json','stages.jsonl','runtime-observation.json','density-validation.json',
                   'factor-aliases.json','metric-calls.jsonl','native.log','worker-started.json')
METHOD={'xc':'PBE','basis':'def2-svp','ecp':{'Mo':'def2-svp'},'charge':-8,'spin':0,
        'atoms':196,'nao':3068,'electrons':1568,'grid_level':2,'direct_scf_tol':1e-13,
        'conv_tol':1e-11,'conv_tol_grad':1e-7,'max_cycle':20,'max_memory_MB':8000,
        'PCM_method':'C-PCM','eps':78.4,'lebedev_order':17,'vdw_scale':1.2,'r_probe':0.,
        'ao_block':1,'auxbasis':'def2-universal-jkfit','OMP_threads':4,'BLAS_threads':1}


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


small=load('qualified_saved_j_runner',SMALL/'run.py')
first,handoff=small.first,small.handoff
read,save,sha,accepted,require=small.read,small.save,small.sha,small.accepted,small.require


def owned(path):
    path=Path(path).resolve();require(path.is_relative_to(BASE.resolve()) and path!=BASE.resolve(),'Output outside parent saved-J pilot');return path


def prerequisites():
    gate=small.validate_gate();out=SMALL/'run-v1';terminal=read(out/'launch-result.json')
    require(isinstance(terminal,dict) and terminal.get('status')=='PASS_RETROSPECTIVE_SAVED_J_HANDOFF'
            and terminal.get('gate_unchanged') is True and terminal.get('SCF_skipped') is False
            and terminal.get('errors')=={} and read(out/'launch-gate.json')==gate,'Small qualification terminal gate failed')
    review_text=(SMALL/'INDEPENDENT_REVIEW.md').read_text()
    require(all(marker in review_text.splitlines() for marker in ('codeQualityStatus: CLEAR','recommendation: APPROVE','blockers: []')),
            'Completed independent saved-J result review is not clear')
    require(isinstance(read(AUDIT/'array-audit.json'),dict),'Independent array audit receipt missing')
    paths=[SMALL/n for n in ('run.py','handoff.py','test_run.py','PROTOCOL.md','preparation.json','independent-root-review.json','INDEPENDENT_REVIEW.md')]
    paths.extend(AUDIT/n for n in ('check_arrays.py','array-audit.json'))
    paths.extend(out/n for n in ('launch-result.json','launch-gate.json','operator-receipt.json'))
    for phase in ('operators','scf'):
        receipt=read(out/phase/'supervisor.json');result=read(out/phase/'result.json')
        require(small.phase_accepted(receipt,result,phase)
                and isinstance(terminal.get('receipts'),dict) and isinstance(terminal.get('results'),dict)
                and terminal['receipts'].get(phase)==receipt and terminal['results'].get(phase)==result,'Small qualification child failed: '+phase)
        paths.extend(out/phase/n for n in ('supervisor.json','result.json','arrays.npz','runtime-observation.json','native.log'))
    return {str(p):sha(p) for p in paths}


def manifest():
    return {'saved_J_qualification':prerequisites(),'first_J':small.prerequisites(),
            'runtime_qualification':first.qualification_artifacts(),'parent':first.parent_pins(),
            'driver':{str(BASE/n):sha(BASE/n) for n in ('run.py','test_run.py','PROTOCOL.md')},
            'supervisor':{str(LAB/'parent-pilot/pilot.py'):sha(LAB/'parent-pilot/pilot.py')},'method':METHOD}


def parent_proof(density):
    out=first.BASE/'run-v1';paths={'artifact':out/'J.npy','receipt':out/'supervisor.json','result':out/'result.json'}
    proof={**{k:str(p) for k,p in paths.items()},**{k+'_sha256':sha(p) for k,p in paths.items()},
           'j_key':None,'density_cycle':0,'density_sha256':handoff.density_digest(density),
           'density_archive':str(first.OLD/'run-v1/partial.npz'),'density_archive_sha256':sha(first.OLD/'run-v1/partial.npz'),
           'method':METHOD,'input_sha256':sha(first.INPUT/'P0_A.xyz')}
    handoff.verify_provenance(proof);return proof


def prepare():
    target=owned(BASE/'preparation.json');require(not target.exists(),'Already prepared');pins=manifest()
    runtime=read(first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve()==Path(runtime['python']).resolve(),'Require qualified interpreter')
    first.parent_atoms();density,summary=first.saved_density();proof=parent_proof(density);del density
    save(target,{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins,'proof':proof,'density':summary,
                 'maximum_children':1,'maximum_SCFs':1,'wall_cap_seconds':WALL,'sampled_RSS_guard_bytes':RSS,
                 'parent_molecule_built':False,'SCFs_launched':0})


def validate_gate():
    prep=read(BASE/'preparation.json');current=manifest();require(prep['pins']==current,'Frozen pilot pins changed')
    proof=prep['proof'];out=first.BASE/'run-v1'
    require(proof['method']==METHOD and proof['j_key'] is None and type(proof['density_cycle']) is int and proof['density_cycle']==0
            and proof['artifact']==str(out/'J.npy') and proof['receipt']==str(out/'supervisor.json') and proof['result']==str(out/'result.json')
            and proof['density_archive']==str(first.OLD/'run-v1/partial.npz')
            and proof['density_archive_sha256']==sha(proof['density_archive'])
            and proof['input_sha256']==sha(first.INPUT/'P0_A.xyz'),'Parent density/J/input/method binding differs')
    handoff.verify_provenance(proof)
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_PARENT_SAVED_J_PILOT' and review.get('independent_root_review') is True
            and bool(review.get('reviewer')) and review.get('preparation_sha256')==sha(BASE/'preparation.json')
            and review.get('saved_J_qualification_artifacts')==current['saved_J_qualification'],'Independent pilot root review binding differs')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json')}


def claim_worker(out):
    with owned(out/'worker-started.json').open('x') as f:json.dump({'pid':os.getpid(),'maximum_children':1,'maximum_SCFs':1},f)


def atomic_npz(path,**arrays):
    import numpy as np
    path=owned(path);temporary=owned(path.with_suffix('.tmp'))
    try:
        with temporary.open('wb') as stream:
            np.savez(stream,**arrays);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if temporary.exists():temporary.unlink()


def checkpoint(mf,env,path,kind):
    """Use callback references and its existing full Fock; never call get_fock/J."""
    import numpy as np
    dm,coeff,occ,fock,overlap=(env[k] for k in ('dm','mo_coeff','mo_occ','fock','s1e'))
    energy=float(env['e_tot']);cycle=int(env['cycle'])+1
    require(1<=cycle<=METHOD['max_cycle'],'Completed cycle outside original bound')
    gradient=float(np.linalg.norm(mf.get_grad(coeff,occ,fock)))
    trace=float(np.einsum('ij,ji',dm,overlap))
    require(all(np.isfinite(x).all() for x in (dm,coeff,occ,fock,overlap))
            and all(np.isfinite(x) for x in (energy,gradient,trace)),'Nonfinite completed SCF state')
    atomic_npz(path,density=dm,mo_coeff=coeff,mo_occ=occ,fock=fock,overlap=overlap,
               cycle=cycle,energy_Eh=energy,electron_trace=trace,full_gradient=gradient,kind=kind)
    return {'cycle':cycle,'energy_Eh':energy,'electron_trace':trace,'trace_error':abs(trace-mf.mol.nelectron),
            'full_unscaled_solvent_gradient':gradient,'kind':kind}


def converged_residual(mf,overlap,path):
    """A fresh full Fock is permitted only after native convergence."""
    require(mf.converged is True,'Native convergence required before fresh residual')
    dm=mf.make_rdm1();fock=mf.get_fock(dm=dm)
    return checkpoint(mf,{'dm':dm,'mo_coeff':mf.mo_coeff,'mo_occ':mf.mo_occ,'fock':fock,'s1e':overlap,
                         'cycle':mf.cycles-1,'e_tot':mf.e_tot},path,'fresh_final_residual')


def result_accepted(receipt,result):
    return bool(accepted(receipt) and isinstance(result,dict) and result.get('status')==STATUS
                and result.get('native_converged') is True and result.get('final_validation_complete') is True
                and type(result.get('SCFs_launched')) is int and result['SCFs_launched']==1
                and isinstance(result.get('checks'),dict) and set(result['checks'])==CHECKS
                and all(v is True for v in result['checks'].values()))


def worker():
    out=owned(BASE/'run-v1');gate=validate_gate();require(read(out/'launch-gate.json')==gate,'Launch review changed');claim_worker(out)
    start=time.monotonic();record={'status':'RUNNING','SCFs_launched':0,'checks':{},'native_converged':False,
          'final_validation_complete':False,'physical_admission':False,'fresh_holdout':False,'geometry_optimization':False}
    def flush():record['elapsed_seconds']=time.monotonic()-start;save(out/'result.json',record)
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (out/'stages.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    flush();stage('worker_entry')
    import numpy as np
    from pyscf import dft,gto,lib
    require(lib.num_threads()==4 and os.environ.get('OMP_NUM_THREADS')=='4' and os.environ.get('OMP_DYNAMIC')=='FALSE','OpenMP differs')
    require(all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'BLAS differs')
    runtime=first.qualification.runtime_pins();require(runtime==read(first.QUAL/'preparation.json')['pins']['runtime'],'Actual runtime inventory/interpreter differs')
    save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,'runtime':runtime})
    density,summary=first.saved_density();density.flags.writeable=False;proof=read(BASE/'preparation.json')['proof']
    require(handoff.density_digest(density)==proof['density_sha256'],'Original cycle-zero density digest differs');save(out/'density-validation.json',summary)
    m=load('unchanged_memory_parent',LAB/'cpcm-rij-memory/memory.py');aliases=[];factor=m.factor_inplace
    def factored(matrix,*args,**kwargs):
        role={(19612,19612):'RI_metric',(9284,9284):'PCM_surface'}.get(matrix.shape)
        require(role is not None,'Unexpected parent factor dimensions')
        stage(role+'_factor_entry',shape=list(matrix.shape));pointer=matrix.ctypes.data;answer=factor(matrix,*args,**kwargs)
        row={'role':role,'shape':list(matrix.shape),'shares_memory':bool(np.shares_memory(matrix,answer[0])),
             'same_pointer':pointer==answer[0].ctypes.data,'readonly':not answer[0].flags.writeable,'Fortran':bool(answer[0].flags.f_contiguous)}
        aliases.append(row);save(out/'factor-aliases.json',aliases)
        require(all(row[k] for k in ('shares_memory','same_pointer','readonly','Fortran')),'Factor alias failed');stage(role+'_factor_return',**row);return answer
    m.factor_inplace=factored;m.private_scipy.linalg.cho_factor=factored
    stage('molecule_entry');mol=gto.M(atom=first.parent_atoms(),unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,verbose=4,max_memory=8000,output=str(out/'native.log'))
    require((mol.natm,mol.nao,mol.nelectron,mol.charge,mol.spin)==(196,3068,1568,-8,0),'Parent molecule dimensions differ');stage('molecule_return')
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
    mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=20;mf.chkfile=None
    if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
    s=m.MemoryPCM(mol);s.method='C-PCM';s.eps=78.4;s.lebedev_order=17;s.vdw_scale=1.2;s.r_probe=0.;s.frozen=False
    def metric(row):
        with (out/'metric-calls.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
        stage('native_metric_return',**row)
    mf=m.install(m.qualified.attach(mf,s),metric);factor_ids={}
    require(mf.with_solvent is s and mf._rij_df.auxbasis==METHOD['auxbasis'] and s.ao_block==1,'RI/PCM implementation settings differ')
    def method_guard():
        require((mf.xc,mf.grids.level,mf.conv_tol,mf.conv_tol_grad,mf.max_cycle,mf.direct_scf,mf.direct_scf_tol)==
                ('PBE',2,1e-11,1e-7,20,True,1e-13),'SCF method changed')
        require((s.method,s.eps,s.lebedev_order,s.vdw_scale,s.r_probe,s.frozen,s.ao_block)==
                ('C-PCM',78.4,17,1.2,0.,False,1),'PCM method changed')
        require(mf._rij_df.auxbasis==METHOD['auxbasis'],'Auxiliary basis changed')
    method_guard()
    def storage():
        obj=mf._rij_df;solvent=mf.with_solvent;values={'no_ERI':mf._eri is None,'no_3index':obj._cderi is None and obj._cderi_to_save is None,'no_S':'S' not in (solvent._intermediates or {})}
        if obj._vjopt is not None:
            f=obj._vjopt.j2c[0];m.finite_chunks(f)
            values.update(RI_cd=obj._vjopt.j2c_type=='cd',RI_shape=f.shape==(obj.auxmol.nao,)*2 and obj.auxmol.nao==19612,RI_immutable_Fortran=not f.flags.writeable and f.flags.f_contiguous,RI_reuse=factor_ids.setdefault('RI',id(f))==id(f))
        if solvent._intermediates and 'factor' in solvent._intermediates:
            f=solvent._intermediates['factor'][0];m.finite_chunks(f)
            values.update(PCM_shape=f.shape==(len(solvent.surface['grid_coords']),)*2 and len(solvent.surface['grid_coords'])==9284,PCM_immutable_Fortran=not f.flags.writeable and f.flags.f_contiguous,PCM_reuse=factor_ids.setdefault('PCM',id(f))==id(f))
        require(all(values.values()),'Storage invariant failed: '+str(values));return values
    def instrument(obj,name,label):
        original=getattr(obj,name)
        def wrapped(self,*args,**kwargs):
            stage(label+'_entry');answer=original(*args,**kwargs);stage(label+'_return');return answer
        setattr(obj,name,types.MethodType(wrapped,obj))
    instrument(s,'build','PCM_build');instrument(s,'_get_vind','PCM_potential')
    native=mf.get_jk;first_native=True
    def audited_native(self,*args,**kwargs):
        nonlocal first_native
        method_guard();stage('native_J_entry',native_calls=self._rij_calls,PCM_present=bool(s._intermediates),RI_present=self._rij_df._vjopt is not None)
        if first_native:
            require(bool(s._intermediates) and self._rij_df._vjopt is None,'First fallback must follow PCM and precede RI metric');first_native=False
        answer=native(*args,**kwargs);storage();stage('native_J_return',native_calls=self._rij_calls);return answer
    mf.get_jk=types.MethodType(audited_native,mf);handoff.install(mf,density,proof)
    veff=mf.get_veff
    def audited_veff(self,*args,**kwargs):
        method_guard();stage('get_veff_entry',saved_J_hits=self.saved_J_hits,native_calls=self._rij_calls)
        answer=veff(*args,**kwargs);storage();stage('get_veff_return',saved_J_hits=self.saved_J_hits,native_calls=self._rij_calls);return answer
    mf.get_veff=types.MethodType(audited_veff,mf)
    overlap=None
    def initial(env):
        nonlocal overlap
        stage('initial_potential_pre_kernel_entry');overlap=env['s1e']
        require(env['dm'] is density and mf.saved_J_hits==1 and mf._rij_calls==0 and mf._rij_df._vjopt is None
                and bool(s._intermediates),'Initial potential cache/PCM/RI ordering differs')
        require(np.isfinite(env['e_tot']) and np.isfinite(env['vhf'].e_solvent) and np.isfinite(env['vhf'].v_solvent).all(),'Nonfinite initial potential')
        trace=float(np.einsum('ij,ji',env['dm'],env['s1e']))
        require(np.isfinite(trace),'Nonfinite initial density electron trace')
        save(out/'initial-potential.json',{'energy_Eh':float(env['e_tot']),'PCM_energy_Eh':float(env['vhf'].e_solvent),
              'electron_trace':trace,'saved_J_hits':mf.saved_J_hits,'native_calls':mf._rij_calls,'storage':storage()})
        record['initial_potential_complete']=True;flush();stage('initial_potential_pre_kernel_return',electron_trace=trace)
    mf.pre_kernel=initial
    def callback(env):
        row=checkpoint(mf,env,out/'latest-complete-cycle.npz','completed_callback');row['storage']=storage()
        record['latest_complete_cycle']=row;flush();stage('completed_cycle',**row)
    mf.callback=callback
    def post_kernel(env):
        stage('native_post_kernel_entry',converged=bool(env['scf_conv']))
        row=checkpoint(mf,env,out/'native-final-state.npz','native_post_kernel')
        row.update(native_converged=bool(env['scf_conv']),storage=storage())
        record['native_final_state']=row;flush();stage('native_post_kernel_return',**row)
    mf.post_kernel=post_kernel
    record['SCFs_launched']=1;flush();stage('kernel_entry');energy=float(mf.kernel(dm0=density));stage('kernel_return',converged=bool(mf.converged),cycles=mf.cycles,energy_Eh=energy)
    record.update(native_converged=bool(mf.converged),cycles=int(mf.cycles),energy_Eh=energy,saved_J_hits=mf.saved_J_hits,native_calls=mf._rij_calls);flush()
    if not mf.converged:
        record['status']='SCF_NOT_CONVERGED';record['storage']=storage();flush();return 1
    stage('final_validation_entry');final=converged_residual(mf,overlap,out/'final-validated-state.npz');record['final']=final
    record['storage']=storage();record['checks']={'native_converged':bool(mf.converged),'finite_energy':bool(np.isfinite(energy)),
        'electron_trace':final['trace_error']<1e-6,'full_unscaled_solvent_gradient':final['full_unscaled_solvent_gradient']<1e-5,
        'storage':all(record['storage'].values()),'both_factors':set(factor_ids)=={'PCM','RI'},
        'saved_hit_once':mf.saved_J_hits==1 and not mf._saved_J_pending,'native_fallback':mf._rij_calls>0,
        'initial_density_unchanged':not density.flags.writeable and handoff.density_digest(density)==proof['density_sha256'],
        'pins_unchanged':validate_gate()==gate,'runtime_unchanged':first.qualification.runtime_pins()==runtime,
        'initial_potential':record.get('initial_potential_complete') is True,
        'completed_cycle':'latest_complete_cycle' in record,'native_final_state':'native_final_state' in record,
        'two_actual_factors':[a['role'] for a in aliases]==['PCM_surface','RI_metric']}
    record['native_calls']=mf._rij_calls;record['final_validation_complete']=True
    record['status']=STATUS if all(record['checks'].values()) else 'FINAL_VALIDATION_FAILED';flush();stage('final_validation_return',status=record['status']);mol.stdout.close()
    return 0 if record['status']==STATUS else 1


def launch():
    gate=validate_gate();out=owned(BASE/'run-v1');out.mkdir(exist_ok=False);save(out/'launch-gate.json',gate)
    supervisor=load('unchanged_parent_supervisor',LAB/'parent-pilot/pilot.py');supervisor.THREADS={**supervisor.THREADS,'OMP_NUM_THREADS':'4','OMP_DYNAMIC':'FALSE'}
    python=read(first.QUAL/'preparation.json')['pins']['runtime']['python'];errors={};result={};evidence={}
    try:receipt=supervisor.monitored_run([python,'-B',str(BASE/'run.py'),'--worker'],out,WALL,RSS)
    except Exception:
        errors['supervisor']=traceback.format_exc();receipt={'returncode':None,'termination_reason':'SUPERVISOR_ERROR','monitor_error':errors['supervisor']}
    try:result=read(out/'result.json')
    except Exception:errors['result']=traceback.format_exc()
    for name in (*REQUIRED_EVIDENCE,'failure.json'):
        path=out/name
        try:
            if path.exists():evidence[name]={'sha256':sha(path),'bytes':path.stat().st_size}
        except Exception:errors[name]=traceback.format_exc()
    try:unchanged=validate_gate()==gate
    except Exception:unchanged=False;errors['gate']=traceback.format_exc()
    required_present=all(name in evidence and evidence[name]['bytes']>0 for name in REQUIRED_EVIDENCE)
    passed=unchanged and required_present and not errors and result_accepted(receipt,result)
    save(out/'launch-result.json',{'status':STATUS if passed else 'FAIL_OR_INCOMPLETE','receipt':receipt,'result':result,'errors':errors,
         'available_evidence':evidence,'required_evidence_present':required_present,'gate_unchanged':unchanged,'maximum_children':1,'maximum_SCFs':1,'wall_cap_seconds':WALL,
         'sampled_RSS_guard_bytes':RSS,'physical_admission':False,'geometry_optimization':False,'full_parent_oracle':False})
    return 0 if passed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif args==['--worker']:
        try:sys.exit(worker())
        except Exception:
            save(owned(BASE/'run-v1/failure.json'),{'exception':traceback.format_exc(),'status':'FAILED_OR_INCOMPLETE'});raise
    else:raise SystemExit('Explicit --prepare, --gate-check or --launch required')
