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
WALL=600
RSS=10*2**30
NAO=3068
NAUX=19612
CHUNK_ROWS=16
SELECTED=(0,1,1534,3067)
AMPLITUDE=.01/math.sqrt(2)
STATUS='PASS_BOUNDED_SIGNED_PARENT_J_ONLY'
CHECKS={'first_sign','first_finite','first_symmetric','second_finite','second_symmetric',
        'selected_oracle','two_J','two_metric_calls','one_factor','one_oracle_solve',
        'factor_unchanged','no_ERI','no_3index','no_PCM','gate_unchanged'}


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


first=load('immutable_first_j_helpers',LAB/'parent-openmp-first-j-v2/run.py')
read,save,sha,require=first.read,first.save,first.sha,first.require
qualification=first.qualification


def owned(path):
    path=Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()) and path!=BASE.resolve(),'Output outside signed diagnostic')
    return path


def write_new(path,value):
    with owned(path).open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')


def manifest():
    pins=first.manifest()
    paths=[]
    for folder in ('parent-openmp-first-j-v2','parent-saved-j-pilot'):
        root=LAB/folder
        paths.extend(root/name for name in ('run.py','test_run.py','PROTOCOL.md','preparation.json','independent-root-review.json'))
        paths.extend(sorted(p for p in (root/'run-v1').rglob('*') if p.is_file()))
    crash=LAB/'parent-saved-j-crash-diagnostic'
    paths.extend(crash/name for name in ('PROTOCOL.md','REPORT.md','NATIVE_ALLOCATION_AUDIT.md','crash-excerpt.json',
                 'extract.py','test_extract.py','allocation_model.py','test_allocation_model.py','allocation-audit.json'))
    paths.append(LAB/'parent-pilot/pilot.py')
    pins['diagnostic_history']={str(p):sha(p) for p in paths}
    pins['signed_driver']={str(BASE/name):sha(BASE/name) for name in ('run.py','test_run.py','PROTOCOL.md')}
    return pins


def prepare():
    require(not (BASE/'preparation.json').exists(),'Already prepared')
    pins=manifest();runtime=read(first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve()==Path(runtime['python']).resolve(),'Require qualified interpreter')
    require(qualification.runtime_pins()==runtime,'Qualified runtime changed')
    original=read(first.BASE/'run-v1/result.json');receipt=read(first.BASE/'run-v1/supervisor.json')
    require(first.accepted(receipt) and original.get('status')=='PASS_BOUNDED_FIRST_J_ONLY'
            and original.get('J_sha256')==sha(first.BASE/'run-v1/J.npy')
            and original.get('checks') and all(v is True for v in original['checks'].values()),'Saved first J not accepted')
    first.parent_atoms();density,summary=first.saved_density();del density
    require(manifest()==pins,'Inputs changed during preparation')
    write_new(BASE/'preparation.json',{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins,
              'density':summary,'wall_cap_seconds':WALL,'sampled_RSS_guard_bytes':RSS,
              'maximum_children':1,'maximum_J_calls':2,'SCFs_launched':0,'operators_executed':0,
              'molecule_built':False,'selected_AOs':list(SELECTED),'fixed_D01':AMPLITUDE,
              'absolute_tolerance':1e-10,'relative_tolerance':0,'physical_admission':False})


def validate_gate():
    preparation=read(BASE/'preparation.json');current=manifest()
    require(preparation.get('status')=='PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW' and preparation['pins']==current,'Preparation pins changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_SIGNED_PARENT_J_DIAGNOSTIC'
            and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent root approval missing')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json')
            and review.get('qualification_artifacts')==current['qualification'],'Review binding differs')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json'),
            'qualification_artifacts':current['qualification']}


def claim_worker(out):
    write_new(out/'worker-started.json',{'pid':os.getpid(),'maximum_J_calls':2,'maximum_SCFs':0})


def forbidden(*args,**kwargs):raise RuntimeError('SCF, PCM build and initial guesses are forbidden')


def restrict(mf):
    for name in ('kernel','scf','run','get_init_guess','make_rdm1','get_veff','init_guess_by_minao',
                 'init_guess_by_atom','init_guess_by_1e','init_guess_by_chkfile','init_guess_by_huckel'):
        setattr(mf,name,forbidden)
    mf.with_solvent.build=forbidden


def call_j(mf,density,number):
    require(type(number) is int and number in (1,2) and mf._rij_calls==number-1,'Invalid native J call order/count')
    restrict(mf);answer=mf.get_j(dm=density)
    require(mf._rij_calls==number,'Native J counter differs')
    return answer


def matrix_checks(matrix,reference=None):
    import numpy as np
    require(matrix.dtype==np.float64 and matrix.shape==(NAO,NAO),'J dtype/shape differs')
    if reference is not None:require(reference.dtype==np.float64 and reference.shape==matrix.shape,'Reference dtype/shape differs')
    finite=True;asymmetry=0.;sign_error=0.
    for start in range(0,NAO,CHUNK_ROWS):
        stop=min(start+CHUNK_ROWS,NAO);part=matrix[start:stop]
        transpose=matrix[:,start:stop].T
        block_finite=bool(np.isfinite(part).all() and np.isfinite(transpose).all())
        finite=block_finite and finite
        if block_finite:asymmetry=max(asymmetry,float(np.max(np.abs(part-transpose))))
        if reference is not None:
            reference_finite=bool(np.isfinite(reference[start:stop]).all())
            finite=reference_finite and finite
            if block_finite and reference_finite:sign_error=max(sign_error,float(np.max(np.abs(part+reference[start:stop]))))
    return {'finite':finite,'symmetric':finite and asymmetry<=1e-10,'max_asymmetry':asymmetry,
            'sign_pass':reference is not None and finite and sign_error<=1e-10,
            'max_sign_error':sign_error if reference is not None else None,'chunk_rows':CHUNK_ROWS}


def ao_metadata(mol,selected):
    import numpy as np
    require(not mol.cart and mol.nao==NAO,'Require scalar spherical parent AO layout')
    loc=mol.ao_loc_nr();require(loc[0]==0 and loc[-1]==NAO and np.all(np.diff(loc)>0),'Invalid AO shell offsets')
    labels=mol.ao_labels(fmt=False);rows=[]
    for ao in selected:
        require(type(ao) is int and 0<=ao<NAO,'Selected AO out of range')
        shell=int(np.searchsorted(loc,ao,side='right')-1);atom=int(mol.bas_atom(shell))
        require(mol.bas_kappa(shell)==0,'Spinor shell outside scalar protocol')
        rows.append({'ao':ao,'shell':shell,'within_shell':int(ao-loc[shell]),
                     'shell_dimension':int(loc[shell+1]-loc[shell]),'atom':atom,
                     'element':mol.atom_symbol(atom),'label':list(labels[ao])})
    return rows


def indefinite_density(mol):
    import numpy as np
    rows=ao_metadata(mol,(0,1))
    require(all(r['atom']==0 and r['element']=='Mo' for r in rows),'AO0/AO1 must belong to atom0 Mo')
    density=np.zeros((NAO,NAO),dtype=np.float64);density[0,1]=density[1,0]=AMPLITUDE
    return density,{'nonzero_entries':[[0,1,AMPLITUDE],[1,0,AMPLITUDE]],
                    'analytic_nonzero_eigenvalues':[-AMPLITUDE,AMPLITUDE],
                    'analytic_Frobenius_norm':.01,'AO_metadata':rows}


def selected_oracle(mol,auxmol,factor,j,aux_e2,solve):
    import numpy as np
    rows=ao_metadata(mol,SELECTED);by_ao={r['ao']:r for r in rows};buffers=[]
    require(auxmol.nao==NAUX,'Auxiliary dimension differs')
    def pair(a,b):
        ra,rb=by_ao[a],by_ao[b];sa,sb=ra['shell'],rb['shell']
        shape=(ra['shell_dimension'],rb['shell_dimension'],NAUX)
        buffer=aux_e2(mol,auxmol,shls_slice=(sa,sa+1,sb,sb+1,0,auxmol.nbas),
                      intor=mol._add_suffix('int3c2e'),aosym='s1')
        bound=8*math.prod(shape)
        require(buffer.dtype==np.float64 and buffer.shape==shape and buffer.nbytes==bound,'Shell oracle buffer shape/size differs')
        require(np.isfinite(buffer).all(),'Nonfinite shell oracle integrals')
        vector=buffer[ra['within_shell'],rb['within_shell'],:].copy()
        buffers.append({'pair':[a,b],'shells':[sa,sb],'shape':list(shape),'bytes':bound})
        del buffer
        return vector
    rhs=pair(0,1);rhs*=2*AMPLITUDE
    rho=solve(factor,rhs);del rhs
    require(rho.shape==(NAUX,) and np.isfinite(rho).all(),'Invalid oracle metric solution')
    comparisons=[]
    for i,a in enumerate(SELECTED):
        for b in SELECTED[:i+1]:
            vector=pair(a,b);expected=float(vector@rho);del vector
            actual=float(j[a,b]);error=abs(actual-expected)
            comparisons.append({'pair':[a,b],'native':actual,'oracle':expected,'absolute_error':error,
                                'pass':math.isfinite(actual) and math.isfinite(expected) and error<=1e-10})
    return {'pass':all(r['pass'] for r in comparisons),'comparisons':comparisons,'AO_metadata':rows,
            'buffers':buffers,'maximum_buffer_bytes':max(r['bytes'] for r in buffers),'oracle_metric_solves':1,
            'shared_metric_and_integral_library':True,'direct_JK_bypassed':True}


def post_call_file(out,number,stage):
    stage('post_call_file_start',call=number)
    with owned(out/f'post-call-{number}.bin').open('xb',buffering=4096) as stream:
        stream.write(b'signed-parent-J diagnostic post-call checkpoint\n')
    stage('post_call_file_closed',call=number)


def factor_state(obj):
    factor,lower=obj._vjopt.j2c
    require(obj._vjopt.j2c_type=='cd' and lower and factor.shape==(NAUX,NAUX)
            and not factor.flags.writeable and factor.flags.f_contiguous,'Metric storage contract differs')
    return {'identity':id(factor),'pointer':factor.ctypes.data,'shape':list(factor.shape),
            'readonly':True,'Fortran':True}


def worker():
    out=owned(BASE/'run-v1');gate=validate_gate()
    require(read(out/'launch-gate.json')==gate,'Launch gate differs');claim_worker(out)
    start=time.monotonic()
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (out/'stages.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    stage('worker_started',J_calls=0,SCFs_launched=0)
    import numpy as np
    from pyscf import dft,gto,lib
    from pyscf.df import incore
    require(lib.num_threads()==4 and os.environ.get('OMP_NUM_THREADS')=='4'
            and os.environ.get('OMP_DYNAMIC')=='FALSE','OpenMP controls differ')
    require(all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'BLAS controls differ')
    runtime=read(first.QUAL/'preparation.json')['pins']['runtime']
    require(qualification.runtime_pins()==runtime,'Runtime changed')
    save(out/'runtime-observation.json',{'actual_threads':lib.num_threads(),'python':sys.executable,
         'loaded_native_files':{str(p):sha(p) for p in sorted(qualification.loaded_native_files())}})
    memory=load('unchanged_signed_memory',LAB/'cpcm-rij-memory/memory.py');aliases=[];metrics=[]
    original=memory.factor_inplace
    def factor(matrix,*args,**kwargs):
        require(not aliases,'Second factorization forbidden');pointer=matrix.ctypes.data
        stage('RI_factor_start',shape=list(matrix.shape));answer=original(matrix,*args,**kwargs)
        row={'shape':list(matrix.shape),'input_pointer':pointer,'factor_pointer':answer[0].ctypes.data,
             'shares_memory':bool(np.shares_memory(matrix,answer[0])),
             'readonly':not answer[0].flags.writeable,'Fortran':bool(answer[0].flags.f_contiguous)}
        aliases.append(row);save(out/'factor-aliases.json',aliases)
        require(row['shape']==[NAUX,NAUX] and row['shares_memory'] and pointer==row['factor_pointer']
                and row['readonly'] and row['Fortran'],'Factor alias contract differs')
        stage('RI_factor_complete');return answer
    memory.factor_inplace=factor;memory.private_scipy.linalg.cho_factor=factor
    stage('basis_build_start')
    mol=gto.M(atom=first.parent_atoms(),unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,
              verbose=4,max_memory=8000,output=str(out/'native.log'))
    require((mol.natm,mol.nao,mol.nelectron)==(196,NAO,1568) and not mol.cart,'Parent dimensions differ')
    save(out/'AO-metadata.json',{'selected':ao_metadata(mol,SELECTED),'maximum_primary_shell_dimension':int(max(np.diff(mol.ao_loc_nr())))})
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13;mf.chkfile=None
    if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
    solvent=memory.MemoryPCM(mol);solvent.method='C-PCM';solvent.eps=78.4;solvent.lebedev_order=17
    solvent.vdw_scale=1.2;solvent.r_probe=0.;solvent.frozen=False;solvent.build=forbidden
    def metric(row):
        metrics.append(row)
        with (out/'metric-calls.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
    mf=memory.qualified.attach(mf,solvent);restrict(mf)
    mf=memory.install(mf,metric);restrict(mf)
    require(first.pcm_unbuilt(solvent) and mf._rij_calls==0 and mf._rij_df._vjopt is None,'Setup must be fresh and PCM unbuilt')
    stage('setup_complete')
    density,summary=first.saved_density();density*=-1
    save(out/'first-density.json',{'source':summary,'multiplier':-1})
    reference=np.load(first.BASE/'run-v1/J.npy',allow_pickle=False,mmap_mode='r')
    stage('native_J_start',call=1);j=call_j(mf,density,1);stage('native_J_returned',call=1)
    one=matrix_checks(j,reference);save(out/'first-checks.json',one)
    state=factor_state(mf._rij_df);save(out/'factor-states.json',[state])
    require(len(metrics)==1 and metrics[0]['call']==1 and len(aliases)==1
            and mf._eri is None and mf._rij_df._cderi is None and mf._rij_df._cderi_to_save is None
            and first.pcm_unbuilt(solvent),'First-call storage/call count differs')
    post_call_file(out,1,stage)
    require(one['finite'] and one['symmetric'] and one['sign_pass'],'First sign/finite/symmetry check failed')
    del density,j;reference._mmap.close();del reference
    stage('first_full_arrays_released')
    density,summary=indefinite_density(mol);save(out/'second-density.json',summary)
    stage('native_J_start',call=2);j=call_j(mf,density,2);stage('native_J_returned',call=2)
    two=matrix_checks(j);save(out/'second-checks.json',two)
    second_state=factor_state(mf._rij_df);save(out/'factor-states.json',[state,second_state])
    require(state==second_state,'Factor changed after second native call')
    oracle=selected_oracle(mol,mf._rij_df.auxmol,mf._rij_df._vjopt.j2c,j,incore.aux_e2,memory.solve_checked)
    save(out/'selected-oracle.json',oracle);post_call_file(out,2,stage)
    final_state=factor_state(mf._rij_df);save(out/'factor-states.json',[state,second_state,final_state])
    checks={'first_sign':one['sign_pass'],'first_finite':one['finite'],'first_symmetric':one['symmetric'],
            'second_finite':two['finite'],'second_symmetric':two['symmetric'],'selected_oracle':oracle['pass'],
            'two_J':mf._rij_calls==2,'two_metric_calls':len(metrics)==2 and [r['call'] for r in metrics]==[1,2],
            'one_factor':len(aliases)==1,'one_oracle_solve':oracle['oracle_metric_solves']==1,
            'factor_unchanged':state==second_state==final_state,'no_ERI':mf._eri is None,
            'no_3index':mf._rij_df._cderi is None and mf._rij_df._cderi_to_save is None,
            'no_PCM':first.pcm_unbuilt(solvent),'gate_unchanged':validate_gate()==gate}
    save(out/'checks.json',checks)
    result={'status':STATUS if all(checks.values()) else 'FAIL_SIGNED_J_CHECKS','checks':checks,
            'J_calls':mf._rij_calls,'metric_calls':len(metrics),'factor_count':len(aliases),'oracle_metric_solves':1,
            'SCFs_launched':0,'physical_admission':False,'parent_SCF_readiness':False}
    save(out/'result.json',result);mol.stdout.close();return 0 if all(checks.values()) else 1


def accepted_result(result):
    return (isinstance(result,dict) and result.get('status')==STATUS
            and isinstance(result.get('checks'),dict) and set(result['checks'])==CHECKS
            and all(v is True for v in result['checks'].values())
            and all(type(result.get(k)) is int and result[k]==v for k,v in
                    {'J_calls':2,'metric_calls':2,'factor_count':1,'oracle_metric_solves':1,'SCFs_launched':0}.items()))


def launch():
    gate=validate_gate();out=owned(BASE/'run-v1');out.mkdir(exist_ok=False);write_new(out/'launch-gate.json',gate)
    supervisor=load('immutable_signed_supervisor',LAB/'parent-pilot/pilot.py')
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
    artifacts=('first-checks.json','second-checks.json','selected-oracle.json','factor-aliases.json','factor-states.json',
               'metric-calls.jsonl','post-call-1.bin','post-call-2.bin','runtime-observation.json','stages.jsonl','checks.json')
    try:
        hashes={name:sha(out/name) for name in artifacts}
        require(all((out/name).stat().st_size>0 for name in artifacts),'Empty required artifact')
    except Exception:hashes={};errors['artifacts']=traceback.format_exc()
    passed=not errors and same and first.accepted(receipt) and accepted_result(result)
    save(out/'launch-result.json',{'status':STATUS if passed else 'INCOMPLETE_OR_FAILED_SIGNED_J',
         'receipt':receipt,'worker_result':result,'errors':errors,'artifact_sha256':hashes,
         'gate_unchanged':same,'maximum_children':1,'maximum_J_calls':2,'maximum_SCFs':0,
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
