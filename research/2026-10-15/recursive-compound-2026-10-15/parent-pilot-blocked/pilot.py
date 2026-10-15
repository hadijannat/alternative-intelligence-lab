"""Prepared bounded pilot. --launch is reserved for root review/authorization."""
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
ROOT=BASE.parents[1]
INPUT=BASE.parent/'parent-inputs'
QUAL=BASE.parent/'cpcm-blocked'
ORIGINAL=BASE.parent/'parent-pilot/pilot.py'
INTERPRETER=ROOT/'discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_pins():
    pins=json.loads((BASE/'pins.json').read_text())
    for rel,want in pins.items():
        if sha(ROOT/rel)!=want:
            raise RuntimeError('Pinned source/input/protocol changed: '+rel)
    qualification=json.loads((QUAL/'result.json').read_text())
    if qualification['status']!='PASS_IMPLEMENTATION_EQUIVALENCE_ONLY':
        raise RuntimeError('Qualification not passing')
    for rel,want in json.loads((QUAL/'SHA256SUMS.json').read_text()).items():
        if sha(QUAL/rel)!=want:
            raise RuntimeError('Qualification artifact changed: '+rel)
    return pins

def load_original():
    spec=importlib.util.spec_from_file_location('original_parent_pilot',ORIGINAL)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

original=load_original()
monitored_run=original.monitored_run
GIB=2**30

def allocation(n,nao,natm):
    terms={'S':8*n*n,'Cholesky_factor':8*n*n,'possible_factor_copy':8*n*n,
           'row_temporaries_eight_arrays':8*8*128*n,'factor_finite_check':n*n,
           'AO_surface_tensor8':8*nao*nao*8,'SCF_DIIS_output_AO_buffers_32':32*8*nao*nao,
           'nuclear_integral_block128':8*natm*128,'scratch_headroom':4*GIB}
    return {'terms_bytes':terms,'screening_estimate_bytes':sum(terms.values()),
            'screening_limit_bytes':original.RSS_BYTES,'screening_is_measured_peak':False,
            'description':'Conservative screening allowance, not certified peak RSS; includes 32 AO buffers (including output and contraction temporary) and 4 GiB scratch allowance. Integral/DFT/direct-JK library scratch and allocator retention are not analytically bounded.'}

def refuse_existing(destination):
    if destination.exists():
        raise RuntimeError(str(destination)+' already exists; no overwrite/retry')

def worker(evidence,scf_enabled):
    pins=validate_pins()
    from collections import Counter
    import types
    import numpy as np
    import pyscf
    from pyscf import dft,gto
    from pyscf.dft import gen_grid
    from pyscf.scf import hf
    from pyscf.solvent import pcm
    sys.path.insert(0,str(QUAL))
    from blocked_pcm import BlockedPCM,attach
    start=time.monotonic()
    def stage(name,**fields):
        row={'stage':name,'elapsed_seconds':time.monotonic()-start,**fields}
        with (evidence/'stages.jsonl').open('a') as stream:
            stream.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    metadata=json.loads((INPUT/'metadata.json').read_text())
    candidate=next(c for c in metadata['candidates'] if c['id']=='P0_A')
    assert candidate['checks']['computational_input_admitted'] and not candidate['physical_admission']
    xyz=INPUT/'P0_A.xyz'
    assert sha(xyz)==candidate['xyz_sha256'] and candidate['charge']==-8
    lines=xyz.read_text().splitlines()
    atoms=[(line.split()[0],tuple(map(float,line.split()[1:]))) for line in lines[2:]]
    assert int(lines[0])==len(atoms)==196
    assert Counter(e for e,_ in atoms)=={'Mo':36,'O':128,'H':32}
    mapping=json.loads((BASE.parent/'identity/site_mapping.json').read_text())
    assert atoms[:164]==[(s['element'],tuple(s['cartesian_A'])) for s in mapping]
    stage('basis_build_start')
    mol=gto.M(atom=atoms,unit='Angstrom',basis='def2-svp',ecp={'Mo':'def2-svp'},charge=-8,spin=0,verbose=4,max_memory=8000,output=str(evidence/'native.log'))
    assert mol.nao==3068 and mol.nelectron==1568 and sum(mol.atom_charges())-mol.nelectron==-8
    stage('basis_build_complete',atoms=mol.natm,AOs=mol.nao,electrons=mol.nelectron)
    stage('surface_preflight_start')
    surface=pcm.gen_surface(mol,ng=gen_grid.LEBEDEV_ORDER[17],rad=1.2*pcm.modified_Bondi,surface_discretization_method='SWIG')
    n=len(surface['grid_coords'])
    assert n==9284
    estimate=allocation(n,mol.nao,mol.natm)
    preflight={'input_id':'P0_A','atoms':mol.natm,'AOs':mol.nao,'explicit_electrons':mol.nelectron,'charge':-8,'spin_2S_trial':0,'surface_points':n,'pyscf':pyscf.__version__,'pins':pins,**estimate,'physical_admission':False,'SCF_requested':scf_enabled,'parent_input_hypothetical':True}
    (evidence/'preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
    stage('surface_preflight_complete',**estimate,surface_points=n)
    del surface
    if estimate['screening_estimate_bytes']>original.RSS_BYTES:
        stage('RESOURCE_PREFLIGHT_REJECTED',SCF_launched=False)
        return 2
    if not scf_enabled:
        stage('PREFLIGHT_ONLY_COMPLETE',SCF_launched=False)
        mol.stdout.close()
        return 0
    mf=dft.RKS(mol); mf.xc='PBE'; mf.grids.level=2
    mf.conv_tol=1e-11; mf.conv_tol_grad=1e-7; mf.max_cycle=20
    mf.direct_scf=True; mf.chkfile=None
    solvent=BlockedPCM(mol)
    solvent.method='C-PCM'; solvent.eps=78.4; solvent.lebedev_order=17
    solvent.vdw_scale=1.2; solvent.r_probe=0.0; solvent.frozen=False
    stage('blocked_surface_matrix_factor_build_start')
    solvent.build()
    stage('blocked_surface_matrix_factor_build_complete',surface_points=len(solvent.v_grids_n),S_bytes=solvent._intermediates['S'].nbytes,factor_bytes=solvent._intermediates['factor'][0].nbytes)
    mf=attach(mf,solvent)
    mf.get_jk=types.MethodType(hf.SCF.get_jk,mf)
    def record_cycle(env):
        row={'cycle':int(env['cycle'])+1,'elapsed_seconds':time.monotonic()-start,'energy_Eh_unqualified':float(env['e_tot']),'orbital_gradient_norm':float(env['norm_gorb'])}
        with (evidence/'iterations.jsonl').open('a') as stream:
            stream.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)
    mf.callback=record_cycle
    stage('SCF_start',max_cycles=20)
    energy=float(mf.kernel())
    stage('SCF_returned',converged=bool(mf.converged),cycles=mf.cycles)
    dm=mf.make_rdm1()
    residual=float(np.linalg.norm(mf.get_grad(mf.mo_coeff,mf.mo_occ,mf.get_fock(dm=dm))))
    electrons=float(np.einsum('ij,ji',dm,mf.get_ovlp()))
    passed=bool(mf.converged and math.isfinite(energy) and residual<1e-5 and abs(electrons-1568)<1e-6 and mf._eri is None)
    result={'numerical_SCF_pass':passed,'converged':bool(mf.converged),'cycles':mf.cycles,'energy_Eh':energy,'orbital_gradient_norm':residual,'electron_trace':electrons,'cached_four_center_ERI':mf._eri is not None,'elapsed_seconds':time.monotonic()-start,'pins':pins,'orbital_stability_checked':False,'geometry_optimized':False,'relative_chemistry_comparison_performed':False,'physical_admission':False,'goal_verified':False}
    (evidence/'SCF-result.json').write_text(json.dumps(result,indent=2)+'\n')
    stage('numerical_checks_complete',**result)
    mol.stdout.close()
    return 0 if passed else 3

def main():
    args=sys.argv[1:]
    if args in (['--worker'],['--preflight-worker']):
        destination=BASE/('run-v1' if args==['--worker'] else 'preflight-v1')
        try:
            return worker(destination,args==['--worker'])
        except Exception:
            failure={'terminal_exception':traceback.format_exc(),'physical_admission':False}
            (destination/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
            raise
    if args not in (['--launch'],['--preflight']):
        raise SystemExit('Use --preflight for surface-only screening; --launch only after root review')
    pins=validate_pins()
    launching=args==['--launch']
    destination=BASE/('run-v1' if launching else 'preflight-v1')
    refuse_existing(destination)
    result=monitored_run([str(INTERPRETER),'-B',str(Path(__file__).resolve()),'--worker' if launching else '--preflight-worker'],destination,original.WALL_SECONDS,original.RSS_BYTES)
    result['pins']=pins
    (destination/'launch-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2))
    return 0 if result['returncode']==0 and result['termination_reason'] is None else 1

if __name__=='__main__':
    sys.exit(main())
