"""Retrospective operator equivalence, then one gated SCF; no parent work."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import traceback

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
CAMPAIGN=LAB/'rij-jkfit-qualification'
MEMORY=LAB/'cpcm-rij-memory'
CASES=('anion-water','neutral-water','anion-eps1','heldout-Mo2O7','new-external')
LABELS=('initial','perturbed','direct_converged','RI_converged')


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')
def accepted(r):return r['returncode']==0 and r['termination_reason'] is None and r['monitor_error'] is None


def pinned_files():
    previous=read(CAMPAIGN/'run-v1/pins.json')
    native=read(MEMORY/'source_pins.json')
    paths=[Path(p) for p in {*previous,*native}]
    paths += [BASE/'PROTOCOL.md',BASE/'run.py',BASE/'test_run.py',MEMORY/'memory.py',MEMORY/'source_pins.json',MEMORY/'PROTOCOL.md',MEMORY/'evidence/observations.json',CAMPAIGN/'preparation.json',CAMPAIGN/'run-v1/pins.json',CAMPAIGN/'run-v1/receipts.json',CAMPAIGN/'run-v1/result.json']
    paths += [CAMPAIGN/'run-v1'/c/n for c in CASES for n in ('arrays.npz','result.json','supervisor.json')]
    return {str(p.resolve()):sha(p) for p in paths}


def validate_sources():
    import numpy as np
    for mapping in (read(CAMPAIGN/'run-v1/pins.json'),read(MEMORY/'source_pins.json')):
        for name,want in mapping.items():
            if sha(name)!=want:raise ValueError('Changed pinned source: '+name)
    summary=read(CAMPAIGN/'run-v1/result.json')
    if summary['status']!='PASS_NUMERICAL_SCREEN_ONLY' or not summary['pins_unchanged']:
        raise ValueError('Saved native JKFIT campaign not passing')
    receipts=read(CAMPAIGN/'run-v1/receipts.json')
    if tuple(r['case'] for r in receipts)!=CASES or not all(map(accepted,receipts)):
        raise ValueError('Native campaign receipts differ')
    for case in CASES:
        r=read(CAMPAIGN/'run-v1'/case/'result.json')
        if r['status']!='PASS_NUMERICAL_SCREEN_ONLY' or not all(c['pass'] for c in r['checks']):
            raise ValueError('Saved native case failed '+case)
        with np.load(CAMPAIGN/'run-v1'/case/'arrays.npz') as arrays:
            for label in LABELS:
                p,j=arrays[label+'_P'],arrays[label+'_Jri']
                if p.ndim!=2 or p.shape!=j.shape or p.shape[0]!=p.shape[1] or not np.isfinite(p).all() or not np.isfinite(j).all():
                    raise ValueError('Invalid saved operator arrays')
                if not np.allclose(p,p.T,atol=1e-12,rtol=0):raise ValueError('Asymmetric saved density')
    return {'cases':list(CASES),'densities_per_case':len(LABELS),'SCFs_launched':0}


def prepare():
    if (BASE/'preparation.json').exists():raise ValueError('Preparation already frozen')
    checked=validate_sources();save(BASE/'preparation.json',{'status':'PREPARED_NOT_EXECUTED','pins':pinned_files(),**checked})
    print('Prepared only:20 saved-density comparisons; five operator children; at most one gated SCF')


def phase1_gate(receipts,results,pins_unchanged):
    return (pins_unchanged and tuple(r['case'] for r in receipts)==CASES
            and tuple(r.get('case') for r in results)==CASES
            and all(r.get('phase')=='operators' for r in results)
            and all(accepted(r) for r in receipts)
            and all(r.get('status')=='PASS_OPERATORS' and r.get('checks') and all(c['pass'] for c in r['checks']) for r in results))


def phase2_accepted(receipt,result,pins_unchanged):
    return bool(receipt is not None and accepted(receipt) and pins_unchanged
                and result.get('case')=='new-external' and result.get('phase')=='scf'
                and result.get('SCFs_launched')==1 and result.get('status')=='PASS_SCF'
                and result.get('checks') and all(c['pass'] for c in result['checks']))


def worker(case,phase):
    import types
    import numpy as np
    from pyscf import dft,gto
    from pyscf.scf import hf
    m=load('local_memory',MEMORY/'memory.py')
    out=BASE/'run-v1'/('operators-'+case if phase=='operators' else 'scf-new-external')
    record={'case':case,'phase':phase,'checks':[],'physical_admission':False,'fresh_holdout':False,'SCFs_launched':0}
    arrays={};start=time.monotonic()
    factor_stage=['unlabelled']
    original_factor=m.factor_inplace
    def record_factor(matrix,*args,**kwargs):
        pointer=matrix.ctypes.data
        factor=original_factor(matrix,*args,**kwargs)
        row={'stage':factor_stage[0],'shape':list(matrix.shape),'input_pointer':pointer,
             'factor_pointer':factor[0].ctypes.data,'factor_id':id(factor[0]),
             'shares_memory':bool(np.shares_memory(matrix,factor[0])),
             'readonly':not factor[0].flags.writeable,'Fortran':bool(factor[0].flags.f_contiguous)}
        record.setdefault('factor_aliases',[]).append(row)
        save(out/'result.json',record)
        return factor
    m.factor_inplace=record_factor
    m.private_scipy.linalg.cho_factor=record_factor
    def flush():
        record['elapsed_seconds']=time.monotonic()-start
        save(out/'result.json',record);np.savez_compressed(out/'arrays.npz',**arrays)
    def check(name,value,passed):
        record['checks'].append({'name':name,'value':value,'pass':bool(passed)});flush()
    def metric(row):
        with (out/'metric-calls.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    try:
        if pinned_files()!=read(BASE/'run-v1/pins.json'):raise ValueError('Worker pins changed')
        if phase=='scf':
            receipts=read(BASE/'run-v1/operator-receipts.json')
            results=[read(BASE/'run-v1'/('operators-'+c)/'result.json') for c in CASES]
            if not phase1_gate(receipts,results,True):raise ValueError('Phase2 operator gate not satisfied')
        old=read(CAMPAIGN/'run-v1'/case/'result.json')
        with np.load(CAMPAIGN/'run-v1'/case/'arrays.npz') as saved:prior={k:saved[k].copy() for k in saved.files}
        if case in CASES[:3]:
            known=read(LAB/'identity/next-step/method-qualification/result.json')['results'][case]
            atoms,charge=known['atoms_A'],known['charge']
        else:
            xyz=LAB/'rij-qualification-v2/raw/Mo2O7.xyz' if case=='heldout-Mo2O7' else CAMPAIGN/'raw/new.xyz'
            lines=xyz.read_text().splitlines();atoms=[(f[0],tuple(map(float,f[1:]))) for line in lines[2:] if (f:=line.split())]
            charge=-2 if case=='heldout-Mo2O7' else read(CAMPAIGN/'raw/new-case.json')['charge']
            assert len(atoms)==int(lines[0])
        mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=charge,spin=0,max_memory=512,verbose=4,output=str(out/'native.log'))
        def solvent(cls):
            s=cls(mol);s.method='C-PCM';s.eps=1. if case=='anion-eps1' else 78.4
            s.lebedev_order=17;s.vdw_scale=1.2;s.r_probe=0.;s.frozen=False
            return s
        def configured(use_ri):
            mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
            mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=60;mf.chkfile=None
            if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
            mf.get_hcore();mf=m.qualified.attach(mf,solvent(m.MemoryPCM))
            if use_ri:return m.install(mf,metric)
            mf.get_jk=types.MethodType(hf.SCF.get_jk,mf);return mf
        mf=configured(True);s=mf.with_solvent
        factor_stage[0]='RI_metric'
        mf.get_j(dm=prior['initial_P'])
        check('metric_before_PCM',not s._intermediates,not s._intermediates)
        factor_stage[0]='PCM_surface'
        s.build()
        def storage():
            obj=mf._rij_df;factor=obj._vjopt.j2c[0];sf=s._intermediates['factor'][0]
            values={'metric_Fortran':bool(factor.flags.f_contiguous),'metric_readonly':not factor.flags.writeable,'surface_Fortran':bool(sf.flags.f_contiguous),'surface_readonly':not sf.flags.writeable,'no_S':'S' not in s._intermediates,'no_ERI':mf._eri is None,'no_3index':obj._cderi is None and obj._cderi_to_save is None,'factor_type_cd':obj._vjopt.j2c_type=='cd','AO_block1':s.ao_block==1,
                    'actual_aliases':all(r['shares_memory'] and r['input_pointer']==r['factor_pointer'] and r['readonly'] and r['Fortran'] for r in record['factor_aliases'])}
            check('factor_storage',values,all(values.values()))
        if phase=='operators':
            oracle=solvent(m.qualified.BlockedPCM);ids=None
            for label in LABELS:
                dm=prior[label+'_P'];j=mf.get_j(dm=dm);energy,v=s._get_vind(dm);q=s._intermediates['q'].copy()
                eo,vo=oracle._get_vind(dm);qo=oracle._intermediates['q'].copy()
                arrays.update({label+'_P':dm,label+'_Jmemory':j,label+'_Jnative_saved':prior[label+'_Jri'],label+'_PCM_V':v,label+'_oracle_V':vo,label+'_PCM_q':q,label+'_oracle_q':qo,label+'_energies':np.array([energy,eo])})
                errors={'J':float(np.max(np.abs(j-prior[label+'_Jri']))),'energy':abs(energy-eo),'q':float(np.max(np.abs(q-qo))),'V':float(np.max(np.abs(v-vo)))}
                for name,value in errors.items():check(label+'/'+name,value,np.isfinite(value) and value<=1e-10)
                current=(id(mf._rij_df._vjopt.j2c[0]),id(s._intermediates['factor'][0]))
                if ids is None:ids=current
                check(label+'/factor_reuse',current==ids,current==ids);storage()
                if case=='anion-eps1':check(label+'/epsilon1',max(abs(energy),float(np.max(np.abs(q))),float(np.max(np.abs(v)))),max(abs(energy),float(np.max(np.abs(q))),float(np.max(np.abs(v))))<=1e-10)
            delta=prior['deltaP'];zero=np.zeros_like(delta)
            jzero=mf.get_j(dm=zero);jdelta=mf.get_j(dm=delta)
            arrays.update(zeroJ=jzero,deltaJ=jdelta,deltaP=delta)
            err=float(np.max(np.abs(arrays['initial_Jmemory']+jdelta-arrays['perturbed_Jmemory'])))
            check('J_additivity',err,err<=1e-9);check('J_zero',float(np.max(np.abs(jzero))),np.max(np.abs(jzero))<=1e-9)
            for label,dm in [('zero',zero),('delta',delta)]:
                energy,v=s._get_vind(dm);arrays[label+'_PCM_V']=v;arrays[label+'_PCM_q']=s._intermediates['q'].copy();arrays[label+'_PCM_energy']=np.array(energy)
            for key in ('PCM_V','PCM_q'):
                difference=arrays['perturbed_'+key]-arrays['initial_'+key]-arrays['delta_'+key]+arrays['zero_'+key]
                err=float(np.max(np.abs(difference)));check('PCM_affine_'+key,err,err<=1e-10)
            before=s._intermediates['factor'][0]
            s.reset()
            check('reset_clears',None,s._intermediates is None and s.surface is None and s.v_grids_n is None and s.e is None and s.v is None and s._dm is None)
            factor_stage[0]='PCM_rebuild';s.build()
            energy,v=s._get_vind(prior['initial_P'])
            check('rebuild_new_factor',None,s._intermediates['factor'][0] is not before)
            check('rebuild_V',float(np.max(np.abs(v-arrays['initial_PCM_V']))),np.max(np.abs(v-arrays['initial_PCM_V']))<=1e-10)
            check('rebuild_energy',abs(energy-arrays['initial_energies'][0]),abs(energy-arrays['initial_energies'][0])<=1e-10)
            for obj,names in ((s,('grad','hess','_B_dot_x')),(mf,('nuc_grad_method','Hessian','gen_response','TDA','TDDFT'))):
                for name in names:
                    rejected=False
                    try:getattr(obj,name)()
                    except NotImplementedError:rejected=True
                    check('unsupported_'+type(obj).__name__+'.'+name,rejected,rejected)
            storage()
            record['status']='PASS_OPERATORS' if all(c['pass'] for c in record['checks']) else 'FAIL_OPERATORS'
        else:
            record['SCFs_launched']=1;flush()
            def cycle(env):
                with (out/'iterations.jsonl').open('a') as f:f.write(json.dumps({'cycle':int(env['cycle'])+1,'energy':float(env['e_tot']),'elapsed_seconds':time.monotonic()-start})+'\n')
            mf.callback=cycle;energy=float(mf.kernel(dm0=prior['initial_P']));dm=mf.make_rdm1()
            fock=mf.get_fock(dm=dm);residual=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,fock)))
            direct=configured(False);fd=direct.get_fock(dm=dm)
            direct_residual=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,fd)))
            overlap=mf.get_ovlp();trace=float(np.einsum('ij,ji',dm,overlap))
            arrays.update(density=dm,saved_density=prior['RI_converged_P'],initial=prior['initial_P'],mo_coeff=mf.mo_coeff,mo_occ=mf.mo_occ,memory_fock=fock,direct_fock=fd,overlap=overlap)
            record['SCF']={'energy_Eh':energy,'saved_energy_Eh':old['RI_SCF']['energy_Eh'],'cycles':mf.cycles,'converged':bool(mf.converged),'trace':trace,'electrons':mol.nelectron}
            check('converged',bool(mf.converged),mf.converged)
            check('energy_error',abs(energy-old['RI_SCF']['energy_Eh']),np.isfinite(energy) and abs(energy-old['RI_SCF']['energy_Eh'])<=1e-8)
            error=float(np.max(np.abs(dm-prior['RI_converged_P'])));check('density_error',error,error<=1e-5)
            check('full_memory_Fock_gradient',residual,residual<=1e-5);check('direct_Fock_gradient',direct_residual,direct_residual<=1e-3)
            check('electron_trace_error',abs(trace-mol.nelectron),abs(trace-mol.nelectron)<=1e-8);storage()
            check('direct_no_ERI',direct._eri is None,direct._eri is None)
            record['status']='PASS_SCF' if all(c['pass'] for c in record['checks']) else 'FAIL_SCF'
        mol.stdout.close()
    except Exception:
        record['status']='ERROR';record['exception']=traceback.format_exc()
    flush();print(json.dumps({'case':case,'phase':phase,'status':record['status']}),flush=True)
    return 0 if record['status'] in ('PASS_OPERATORS','PASS_SCF') else 1


def launch():
    pins=read(BASE/'preparation.json')['pins']
    if pinned_files()!=pins:raise ValueError('Preparation pins changed')
    destination=BASE/'run-v1';destination.mkdir(exist_ok=False);save(destination/'pins.json',pins)
    supervisor=load('original_supervisor',LAB/'parent-pilot/pilot.py')
    receipts=[];results=[]
    for case in CASES:
        r=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker','operators',case],destination/('operators-'+case),180,2*2**30)
        receipts.append({'case':case,**r});save(destination/'operator-receipts.json',receipts)
        p=destination/('operators-'+case)/'result.json';results.append(read(p) if p.exists() else {})
    gate=phase1_gate(receipts,results,pinned_files()==pins)
    save(destination/'phase1-gate.json',{'pass':gate,'SCFs_launched':0})
    phase2=None
    if gate:
        phase2=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker','scf','new-external'],destination/'scf-new-external',180,2*2**30)
    unchanged=pinned_files()==pins
    final_path=destination/'scf-new-external/result.json'
    final_record=read(final_path) if final_path.exists() else {}
    passed=gate and phase2_accepted(phase2,final_record,unchanged)
    result={'status':'PASS_RETROSPECTIVE_IMPLEMENTATION_EQUIVALENCE' if passed else 'FAIL','phase1_pass':gate,'phase2':phase2,'phase2_skipped':not gate,'pins_unchanged':unchanged,'maximum_new_SCFs':1,'parent_run':False,'physical_admission':False}
    save(destination/'result.json',result);print(json.dumps(result),flush=True)
    return 0 if passed else 1


if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--launch']:sys.exit(launch())
    elif len(args)==3 and args[0]=='--worker' and ((args[1]=='operators' and args[2] in CASES) or args[1:] == ['scf','new-external']):sys.exit(worker(args[2],args[1]))
    else:raise SystemExit('Use --prepare or --launch; no automatic execution')
