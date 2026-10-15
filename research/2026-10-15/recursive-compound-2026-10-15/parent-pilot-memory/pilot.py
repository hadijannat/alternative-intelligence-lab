"""One explicitly reviewed parent attempt; preparation imports no chemistry libraries."""
import hashlib
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
ROOT=LAB.parent
INPUT=LAB/'parent-inputs'
QUAL=LAB/'cpcm-rij-memory-qualification'
MEMORY=LAB/'cpcm-rij-memory'
INTERPRETER=ROOT/'discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python'
CASES=('anion-water','neutral-water','anion-eps1','heldout-Mo2O7','new-external')
GIB=2**30

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')
def require(value,message):
    if not value:raise ValueError(message)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj

def original_pins():
    pins=read(QUAL/'preparation.json')['pins']
    require(len(pins)==57,'Expected exactly 57 original qualification pins')
    require(read(QUAL/'run-v1/pins.json')==pins,'Qualification run pin mapping differs')
    for path,want in pins.items():require(sha(path)==want,'Changed original pin: '+path)
    return pins

def preparation_pins():
    pins=original_pins()
    paths=[BASE/'pilot.py',BASE/'test_pilot.py',BASE/'PROTOCOL.md',QUAL/'preparation.json',QUAL/'run-v1/pins.json',MEMORY/'allocation.json',INPUT/'P0_A.xyz',INPUT/'metadata.json',LAB/'identity/site_mapping.json']
    return {**pins,**{str(p):sha(p) for p in paths}}

def accepted(receipt):
    return receipt.get('returncode')==0 and receipt.get('termination_reason') is None and receipt.get('monitor_error') is None

def qualification_manifest():
    original_pins()
    final=read(QUAL/'run-v1/result.json')
    require(final.get('status')=='PASS_RETROSPECTIVE_IMPLEMENTATION_EQUIVALENCE' and final.get('pins_unchanged') is True and final.get('phase1_pass') is True and final.get('phase2_skipped') is False,'Qualification terminal gate failed')
    receipts=read(QUAL/'run-v1/operator-receipts.json')
    require(tuple(r.get('case') for r in receipts)==CASES,'Expected five operator receipts in order')
    paths=[QUAL/'run-v1/result.json',QUAL/'run-v1/operator-receipts.json',QUAL/'run-v1/phase1-gate.json']
    require(read(paths[-1]).get('pass') is True,'Operator gate failed')
    children=[('operators-'+c,c,'operators',r) for c,r in zip(CASES,receipts)]
    children.append(('scf-new-external','new-external','scf',final.get('phase2') or {}))
    for folder,case,phase,receipt in children:
        out=QUAL/'run-v1'/folder
        supervisor=read(out/'supervisor.json');result=read(out/'result.json')
        require(accepted(receipt) and accepted(supervisor),'Unaccepted child '+folder)
        require({k:v for k,v in receipt.items() if k!='case'}==supervisor,'Receipt mismatch '+folder)
        require(result.get('case')==case and result.get('phase')==phase,'Wrong child '+folder)
        require(result.get('status')==('PASS_OPERATORS' if phase=='operators' else 'PASS_SCF') and result.get('checks') and all(c.get('pass') is True for c in result['checks']),'Failed checks '+folder)
        require(result.get('SCFs_launched')==(0 if phase=='operators' else 1),'SCF count differs '+folder)
        paths.extend(out/name for name in ('result.json','supervisor.json','arrays.npz','metric-calls.jsonl','native.log'))
    return {str(p):sha(p) for p in paths}

def validate_gate():
    prep=read(BASE/'preparation.json')
    require(prep['pins']==preparation_pins(),'Parent preparation pins changed')
    manifest=qualification_manifest()
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_ONE_PARENT_PILOT' and review.get('independent_root_review') is True and bool(review.get('reviewer')),'Independent root approval missing')
    require(review.get('preparation_sha256')==sha(BASE/'preparation.json') and review.get('qualification_artifacts')==manifest,'Root review does not bind current preparation and terminal qualification')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json'),'qualification_artifacts':manifest}

def prepare():
    require(not (BASE/'preparation.json').exists(),'Preparation already frozen')
    save(BASE/'preparation.json',{'status':'PREPARED_PENDING_TERMINAL_QUALIFICATION_AND_INDEPENDENT_ROOT_REVIEW','pins':preparation_pins(),'parent_molecule_built':False,'parent_arrays_allocated':False,'SCFs_launched':0})

def allocation(n,nao,natm,naux):
    require((n,nao,natm,naux)==(9284,3068,196,19612),'Parent dimensions differ')
    terms={'surface_factor':8*n*n,'RI_metric_factor':8*naux*naux,'AO_block1':8*nao*nao,'row_temporary_eight_arrays':8*8*128*n,'finite_validation_chunk_boolean':65536,'SCF_DIIS_output_AO_buffers_32':32*8*nao*nao,'nuclear_integral_block128':8*natm*128,'scratch_headroom_4GiB':4*GIB}
    expected=read(MEMORY/'allocation.json')
    require(terms==expected['terms_bytes'] and sum(terms.values())==expected['sum_bytes'],'Allocation estimate changed')
    require(sum(terms.values())<10*GIB,'Arithmetic screening failed')
    return {'terms_bytes':terms,'sum_bytes':sum(terms.values()),'sum_GiB':sum(terms.values())/GIB,'certified_peak_RSS':False}


def worker():
    out=BASE/'run-v1';gate=validate_gate()
    require(read(out/'launch-gate.json')==gate,'Launch gate differs')
    with (out/'worker-started.json').open('x') as f:json.dump({'pid':os.getpid()},f)
    from collections import Counter
    import numpy as np
    from pyscf import dft,gto,df
    from pyscf.dft import gen_grid
    from pyscf.solvent import pcm
    m=load('parent_memory',MEMORY/'memory.py')
    start=time.monotonic();factor_stage=['unlabelled'];aliases=[]
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (out/'stages.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    original_factor=m.factor_inplace
    def record_factor(matrix,*args,**kwargs):
        pointer=matrix.ctypes.data;factor=original_factor(matrix,*args,**kwargs)
        row={'stage':factor_stage[0],'shape':list(matrix.shape),'input_pointer':pointer,'factor_pointer':factor[0].ctypes.data,'shares_memory':bool(np.shares_memory(matrix,factor[0])),'readonly':not factor[0].flags.writeable,'Fortran':bool(factor[0].flags.f_contiguous)}
        aliases.append(row);save(out/'factor-aliases.json',aliases)
        require(row['shares_memory'] and pointer==row['factor_pointer'] and row['readonly'] and row['Fortran'],'Factor storage contract failed')
        return factor
    m.factor_inplace=record_factor;m.private_scipy.linalg.cho_factor=record_factor
    metadata=read(INPUT/'metadata.json');candidate=next(c for c in metadata['candidates'] if c['id']=='P0_A')
    require(candidate['checks']['computational_input_admitted'] and candidate['physical_admission'] is False and candidate['charge']==-8,'Parent identity mismatch')
    require(sha(INPUT/'P0_A.xyz')==candidate['xyz_sha256'],'Parent XYZ mismatch')
    lines=(INPUT/'P0_A.xyz').read_text().splitlines();atoms=[(s[0],tuple(map(float,s[1:]))) for line in lines[2:] if (s:=line.split())]
    require(int(lines[0])==len(atoms)==196 and Counter(e for e,_ in atoms)=={'Mo':36,'O':128,'H':32},'Parent atom count differs')
    require(atoms[:164]==[(s['element'],tuple(s['cartesian_A'])) for s in read(LAB/'identity/site_mapping.json')],'Heavy sites differ')
    stage('basis_build_start')
    mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,verbose=4,max_memory=8000,output=str(out/'native.log'))
    require((mol.natm,mol.nao,mol.nelectron)==(196,3068,1568) and sum(mol.atom_charges())-mol.nelectron==-8,'Parent dimensions differ')
    stage('basis_build_complete')
    aux=df.addons.make_auxmol(mol,'def2-universal-jkfit');naux=aux.nao;del aux
    stage('surface_preflight_start')
    surface=pcm.gen_surface(mol,ng=gen_grid.LEBEDEV_ORDER[17],rad=1.2*pcm.modified_Bondi,surface_discretization_method='SWIG')
    n=len(surface['grid_coords']);estimate=allocation(n,mol.nao,mol.natm,naux);del surface
    save(out/'preflight.json',{'input':'P0_A','atoms':196,'AOs':3068,'electrons':1568,'auxiliary_AOs':naux,'surface_points':n,**estimate})
    stage('preflight_complete',**estimate)
    mf=dft.RKS(mol);mf.xc='PBE';mf.grids.level=2;mf.direct_scf=True;mf.direct_scf_tol=1e-13
    mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=20;mf.chkfile=str(out/'native.chk')
    solvent=m.MemoryPCM(mol);solvent.method='C-PCM';solvent.eps=78.4;solvent.lebedev_order=17;solvent.vdw_scale=1.2;solvent.r_probe=0.;solvent.frozen=False
    mf=m.install(m.qualified.attach(mf,solvent),lambda row: metric(row))
    def metric(row):
        with (out/'metric-calls.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    def checkpoint(dm,cycle,mo_coeff=None,mo_occ=None):
        values={'density':dm,'cycle':np.array(cycle)}
        if mo_coeff is not None:values.update(mo_coeff=mo_coeff,mo_occ=mo_occ)
        with (out/'partial.tmp').open('wb') as f:np.savez(f,**values)
        os.replace(out/'partial.tmp',out/'partial.npz')
    stage('initial_density_start');dm=mf.get_init_guess();checkpoint(dm,0)
    factor_stage[0]='RI_metric';stage('RI_metric_build_start')
    mf.get_j(dm=dm)
    require(not solvent._intermediates,'PCM allocated before metric')
    stage('RI_metric_build_complete',metric_before_PCM=True)
    factor_stage[0]='PCM_surface';stage('PCM_build_start');solvent.build();stage('PCM_build_complete')
    def storage():
        require((mf.xc,mf.grids.level,mf.conv_tol,mf.conv_tol_grad,mf.max_cycle,mf.direct_scf,mf.direct_scf_tol)==('PBE',2,1e-11,1e-7,20,True,1e-13),'SCF settings differ')
        require((solvent.method,solvent.eps,solvent.lebedev_order,solvent.vdw_scale,solvent.r_probe,solvent.frozen,solvent.ao_block)==('C-PCM',78.4,17,1.2,0.,False,1),'PCM settings differ')
        obj=mf._rij_df;require(obj.auxbasis=='def2-universal-jkfit','Auxiliary basis differs')
        sf=solvent._intermediates['factor'][0];rf=obj._vjopt.j2c[0]
        checks={'no_S':'S' not in solvent._intermediates,'no_ERI':mf._eri is None,'no_3index':obj._cderi is None and obj._cderi_to_save is None,'AO_block1':solvent.ao_block==1,'metric_cd':obj._vjopt.j2c_type=='cd','surface_shape':sf.shape==(9284,9284),'metric_shape':rf.shape==(19612,19612),'immutable_Fortran':all(not a.flags.writeable and a.flags.f_contiguous for a in (sf,rf)),'two_actual_aliases':[a['stage'] for a in aliases]==['RI_metric','PCM_surface']}
        save(out/'storage.json',checks);require(all(checks.values()),'Storage contract failed')
    storage()
    def cycle(env):
        row={'cycle':int(env['cycle'])+1,'energy_Eh_unqualified':float(env['e_tot']),'orbital_gradient_norm':float(env['norm_gorb']),'elapsed_seconds':time.monotonic()-start}
        with (out/'iterations.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        checkpoint(env['dm'],row['cycle'],env['mo_coeff'],env['mo_occ']);storage()
    mf.callback=cycle;validate_gate();stage('SCF_start',max_cycles=20)
    energy=float(mf.kernel(dm0=dm));del dm
    stage('SCF_returned',converged=bool(mf.converged),cycles=mf.cycles)
    density=mf.make_rdm1();checkpoint(density,mf.cycles,mf.mo_coeff,mf.mo_occ)
    residual=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,mf.get_fock(dm=density))))
    trace=float(np.einsum('ij,ji',density,mf.get_ovlp()));storage();validate_gate()
    passed=bool(mf.converged and math.isfinite(energy) and residual<1e-5 and abs(trace-1568)<1e-6)
    save(out/'SCF-result.json',{'numerical_SCF_pass':passed,'converged':bool(mf.converged),'cycles':mf.cycles,'energy_Eh':energy,'orbital_gradient_norm':residual,'electron_trace':trace,'physical_admission':False,'goal_verified':False,'orbital_stability_checked':False,'geometry_optimized':False,'relative_chemistry_comparison_performed':False})
    stage('numerical_checks_complete',numerical_SCF_pass=passed);mol.stdout.close()
    return 0 if passed else 3


def launch():
    gate=validate_gate();out=BASE/'run-v1';out.mkdir(exist_ok=False);save(out/'launch-gate.json',gate)
    supervisor=load('original_supervisor',LAB/'parent-pilot/pilot.py')
    receipt=supervisor.monitored_run([str(INTERPRETER),'-B',str(BASE/'pilot.py'),'--worker'],out,900,10*GIB)
    save(out/'launch-result.json',receipt)
    return 0 if accepted(receipt) else 1

if __name__=='__main__':
    args=sys.argv[1:]
    if args==['--prepare']:prepare()
    elif args==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif args==['--launch']:sys.exit(launch())
    elif args==['--worker']:
        try:sys.exit(worker())
        except Exception:
            out=BASE/'run-v1'
            if out.exists():save(out/'failure.json',{'exception':traceback.format_exc(),'physical_admission':False})
            raise
    else:raise SystemExit('Use --prepare, --gate-check or --launch; no default execution')
