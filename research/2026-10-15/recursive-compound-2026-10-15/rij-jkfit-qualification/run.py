import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
RETROSPECTIVE = ('anion-water', 'neutral-water', 'anion-eps1', 'heldout-Mo2O7')
CASES = RETROSPECTIVE + ('new-external',)
PREVIOUS = LAB / 'rij-qualification-v2'
OLD = LAB / 'identity/next-step/method-qualification/result.json'
sys.path.insert(0, str(LAB / 'cpcm-blocked'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def accepted(receipt):
    return (receipt['returncode']==0 and receipt['termination_reason'] is None
            and receipt['monitor_error'] is None)


def pinned_files():
    from pyscf.df import df_jk
    from pyscf.solvent import pcm
    import pyscf
    paths = [BASE/'PROTOCOL.md', BASE/'run.py', BASE/'rij.py', BASE/'test_rij.py',
             PREVIOUS/'raw/Mo2O7.xyz', PREVIOUS/'raw/Mo2O7.in', OLD,
             BASE/'raw/new-case.json', BASE/'raw/new.xyz', BASE/'raw/new.in',
             BASE/'raw/new-output.cml', BASE/'SOURCE.md',
             PREVIOUS/'run-v1/pins.json', PREVIOUS/'run-v1/result.json',
             LAB/'cpcm-blocked/blocked_pcm.py', LAB/'parent-pilot/pilot.py',
             Path(inspect.getsourcefile(df_jk)), Path(inspect.getsourcefile(pcm)),
             Path(pyscf.__file__).parent/'gto/basis/def2-universal-jkfit.dat']
    paths += [PREVIOUS/'run-v1'/case/name for case in RETROSPECTIVE for name in ('arrays.npz','result.json')]
    paths += [LAB/'cpcm-blocked/evidence'/f'{case}.npz' for case in CASES[:3]]
    return {str(p): sha(p) for p in paths}


def validate_charge(input_text, output_text, charge):
    import re
    import xml.etree.ElementTree as ET
    lines = [line.strip() for line in input_text.splitlines() if re.match(r'^\s*Charge\b', line, re.I)]
    if lines:
        if len(lines) != 1 or re.fullmatch(r'Charge\s+-?\d+', lines[0], re.I) is None or int(lines[0].split()[1]) != charge:
            raise ValueError('Primary input charge mismatch')
    elif charge != 0:
        raise ValueError('Missing explicit nonzero input charge')
    root = ET.fromstring(output_text)
    values = [node.text.strip() for node in root.iter() if node.get('dictRef') == 'a:charge']
    spins = [node.text.strip() for node in root.iter() if node.get('dictRef') == 'cc:spinMolecule']
    if values != [str(charge)] or spins != ['Restricted']:
        raise ValueError('Primary output charge or restricted-spin evidence mismatch')


def validate_new_case():
    import math
    from collections import Counter
    meta=json.loads((BASE/'raw/new-case.json').read_text())
    xyz,source=BASE/'raw/new.xyz',BASE/'raw/new.in'
    if sha(xyz)!=meta['xyz_sha256'] or sha(source)!=meta['input_sha256']:
        raise ValueError('New primary input/geometry hash mismatch')
    output=BASE/'raw/new-output.cml'
    if sha(output)!=meta['output_sha256']:
        raise ValueError('New primary output hash mismatch')
    if not all(meta.get(k) for k in ('item_url','xyz_url','input_url','output_url')):
        raise ValueError('Primary-source provenance required')
    lines=xyz.read_text().splitlines()
    atoms=[line.split() for line in lines[2:] if line.strip()]
    counts=Counter(a[0] for a in atoms)
    if counts not in (Counter(Mo=2,O=7,H=1),Counter(Mo=2,O=7,H=2)):
        raise ValueError('Unexpected external composition')
    if int(lines[0])!=len(atoms) or any(len(a)!=4 or not all(math.isfinite(float(v)) for v in a[1:]) for a in atoms):
        raise ValueError('Invalid external geometry')
    charge=counts['H']-2
    if meta['charge']!=charge:
        raise ValueError('Metadata charge mismatch')
    validate_charge(source.read_text(),output.read_text(),charge)
    return meta


def validate_retrospective():
    import numpy as np
    original_pins=json.loads((PREVIOUS/'run-v1/pins.json').read_text())
    for name,want in original_pins.items():
        if sha(Path(name))!=want:
            raise ValueError('Retrospective source hash changed: '+name)
    known=json.loads(OLD.read_text())['results']
    records=[]
    for case in RETROSPECTIVE:
        result_path=PREVIOUS/'run-v1'/case/'result.json'
        result=json.loads(result_path.read_text())
        with np.load(PREVIOUS/'run-v1'/case/'arrays.npz') as arrays:
            for name in ('initial_P','deltaP','direct_converged_P'):
                value=arrays[name]
                if value.ndim!=2 or value.shape[0]!=value.shape[1] or not np.isfinite(value).all() or not np.allclose(value,value.T,atol=1e-12,rtol=0):
                    raise ValueError('Invalid reused density '+case+'/'+name)
            if case in CASES[:3]:
                with np.load(LAB/'cpcm-blocked/evidence'/f'{case}.npz') as old:
                    for current,prior in (('initial_P','initial_dm'),('deltaP','deltaP'),('direct_converged_P','converged_dm')):
                        if not np.array_equal(arrays[current],old[prior]):raise ValueError('Reused density provenance differs')
                energy=known[case]['energy_Eh']
            else:
                if not result['direct_SCF']['converged']:raise ValueError('Old external direct SCF not converged')
                energy=result['direct_SCF']['energy_Eh']
            if result['RI_SCF']['reference_energy_Eh']!=energy:
                raise ValueError('Reused direct energy provenance differs')
        records.append({'case':case,'reference_energy_Eh':energy,'previous_numerical_status':result['status'],
                        'arrays_sha256':sha(PREVIOUS/'run-v1'/case/'arrays.npz'),'result_sha256':sha(result_path)})
    return records


def prepare():
    if (BASE/'preparation.json').exists():raise ValueError('Preparation already frozen')
    references=validate_retrospective()
    metadata=validate_new_case()
    save(BASE/'preparation.json',{'status':'PREPARED_NOT_EXECUTED','pins':pinned_files(),
                                'retrospective':references,'new_case':metadata,'SCFs_launched':0})
    print('PREPARED_NOT_EXECUTED: five cases; at most six SCFs; no run-v1 created')


def worker(case):
    import types
    import numpy as np
    import pyscf
    from pyscf import dft, gto
    from pyscf.scf import hf
    from blocked_pcm import BlockedPCM, attach
    from rij import install
    out = BASE/'run-v1'/case
    record = {'case': case, 'checks': [], 'physical_admission': False,
              'experimental_validation': False, 'heldout_numerical_case': case == CASES[-1]}
    arrays = {}
    def record_call(row):
        with (out/'metric-calls.jsonl').open('a') as stream:
            stream.write(json.dumps(row)+'\n')
    def check(name, value, passed):
        record['checks'].append({'name': name, 'value': value, 'pass': bool(passed)})
        save(out/'result.json', record)
    try:
        assert pyscf.__version__ == '2.14.0'
        assert pinned_files() == json.loads((BASE/'run-v1/pins.json').read_text())
        known = json.loads(OLD.read_text())['results']
        if case in ('heldout-Mo2O7', 'new-external'):
            xyz = PREVIOUS/'raw/Mo2O7.xyz' if case == 'heldout-Mo2O7' else BASE/'raw/new.xyz'
            lines = xyz.read_text().splitlines()
            atoms = [(s.split()[0], tuple(map(float, s.split()[1:]))) for s in lines[2:] if s.strip()]
            if case == 'heldout-Mo2O7':
                assert sha(xyz) == 'd3ede09e3ed012e74e45613b061bf4e2d73ddc946621869e5e481b91ea2d1cc3'
                charge = -2
            else:
                metadata = validate_new_case()
                charge = metadata['charge']
                record['new_external_source'] = metadata
            assert int(lines[0]) == len(atoms)
        else:
            atoms, charge = known[case]['atoms_A'], known[case]['charge']
        mol = gto.M(atom=atoms, unit='Angstrom', basis='def2-svp', ecp={'Mo':'def2-svp'},
                    charge=charge, spin=0, max_memory=512, verbose=4, output=str(out/'native.log'))
        def configured(ri=False):
            m = dft.RKS(mol); m.xc='PBE'; m.grids.level=2
            m.direct_scf=True; m.direct_scf_tol=1e-13; m.chkfile=None
            if getattr(m,'_chkfile',None) is not None:m._chkfile.close()
            m.conv_tol=1e-11; m.conv_tol_grad=1e-7; m.max_cycle=60
            m.get_hcore()
            s=BlockedPCM(mol); s.method='C-PCM'; s.eps=1.0 if case.endswith('eps1') else 78.4
            s.lebedev_order=17; s.vdw_scale=1.2; s.r_probe=0.0
            m=attach(m,s)
            if ri:
                return install(m,record_call)
            m.get_jk=types.MethodType(hf.SCF.get_jk,m)
            return m
        direct, ri = configured(), configured(True)
        if case == CASES[-1]:
            initial=direct.get_init_guess()
            rng=np.random.default_rng(7392016)
            delta=rng.standard_normal(initial.shape); delta=(delta+delta.T)/2
            delta*=.01/np.linalg.norm(delta)
            start=time.monotonic(); reference_energy=float(direct.kernel(dm0=initial))
            record['direct_SCF']={'energy_Eh':reference_energy,'cycles':direct.cycles,
                                  'seconds':time.monotonic()-start,'converged':bool(direct.converged)}
            check('direct SCF converged',bool(direct.converged),direct.converged)
            ref_density=direct.make_rdm1()
            arrays.update(initial_P=initial,deltaP=delta,direct_converged_P=ref_density)
            np.savez_compressed(out/'arrays.npz',**arrays)
            save(out/'result.json',record)
        else:
            previous_result=json.loads((PREVIOUS/'run-v1'/case/'result.json').read_text())
            with np.load(PREVIOUS/'run-v1'/case/'arrays.npz') as old:
                initial=old['initial_P'].copy(); delta=old['deltaP'].copy(); ref_density=old['direct_converged_P'].copy()
            reference_energy=previous_result['RI_SCF']['reference_energy_Eh']
            record['reused_direct_reference']={'case':case,'energy_Eh':reference_energy,
                'arrays_sha256':sha(PREVIOUS/'run-v1'/case/'arrays.npz'),
                'result_sha256':sha(PREVIOUS/'run-v1'/case/'result.json'),'new_direct_SCF':False}
        nmo=sum(e=='Mo' for e,_ in atoms)
        def compare(label, density):
            start=time.monotonic(); jd=direct.get_j(dm=density); td=time.monotonic()-start
            start=time.monotonic(); jr=ri.get_j(dm=density); tr=time.monotonic()-start
            error=float(np.max(np.abs(jr-jd)))
            energy_error=float(.5*np.einsum('ij,ji',density,jr-jd))
            arrays[label+'_P']=density; arrays[label+'_Jdirect']=jd; arrays[label+'_Jri']=jr
            np.savez_compressed(out/'arrays.npz',**arrays)
            check(label+'/max_J_error_Eh',error,error<=1e-3)
            check(label+'/Coulomb_energy_error_Eh_per_Mo',energy_error/nmo,abs(energy_error)/nmo<=1e-3)
            asym=float(np.max(np.abs(jr-jr.T)))
            check(label+'/symmetric_finite',asym,np.isfinite(jr).all() and asym<=1e-10)
            record.setdefault('J_timings',{})[label]={'direct_seconds':td,'RI_seconds':tr}
            return jr
        j0=compare('initial',initial)
        jp=compare('perturbed',initial+delta)
        compare('direct_converged',ref_density)
        jd=ri.get_j(dm=delta)
        arrays['deltaP']=delta; arrays['deltaJ']=jd
        additive=float(np.max(np.abs(j0+jd-jp)))
        check('incremental_additivity',additive,additive<=1e-9)
        arrays['zeroJ']=ri.get_j(dm=np.zeros_like(initial))
        np.savez_compressed(out/'arrays.npz',**arrays)
        zero=float(np.max(np.abs(arrays['zeroJ'])))
        check('zero_density',zero,zero<=1e-9)
        start=time.monotonic(); energy=float(ri.kernel(dm0=initial)); elapsed=time.monotonic()-start
        density=ri.make_rdm1()
        compare('RI_converged',density)
        fri=ri.get_fock(dm=density); fd=direct.get_fock(dm=density)
        residual=float(np.linalg.norm(ri.get_grad(ri.mo_coeff,ri.mo_occ,fri)))
        direct_residual=float(np.linalg.norm(ri.get_grad(ri.mo_coeff,ri.mo_occ,fd)))
        trace=float(np.einsum('ij,ji',density,ri.get_ovlp()))
        arrays.update(RI_mo_coeff=ri.mo_coeff,RI_mo_occ=ri.mo_occ,RI_fock=fri,direct_fock_at_RI=fd,overlap=ri.get_ovlp())
        np.savez_compressed(out/'arrays.npz',**arrays)
        record['RI_SCF']={'energy_Eh':energy,'reference_energy_Eh':reference_energy,'cycles':ri.cycles,
                          'seconds':elapsed,'converged':bool(ri.converged),'direct_residual':direct_residual,
                          'RI_residual':residual,'electron_trace':trace,'explicit_electrons':mol.nelectron}
        check('RI SCF converged',bool(ri.converged),ri.converged)
        check('total_energy_error_Eh_per_Mo',abs(energy-reference_energy)/nmo,abs(energy-reference_energy)/nmo<=1e-3)
        check('direct_Fock_residual',direct_residual,direct_residual<=1e-3)
        check('RI_Fock_residual',residual,residual<=1e-5)
        check('electron_trace_error',abs(trace-mol.nelectron),abs(trace-mol.nelectron)<=1e-8)
        obj=ri._rij_df
        record['storage']={'nao':mol.nao,'naux':obj.auxmol.nao,'metric_factor_shape':list(obj._vjopt.j2c[0].shape),
                           'factor_type':obj._vjopt.j2c_type,'J_calls':ri._rij_calls,
                           'cached_ERI':ri._eri is not None,'cached_3index':obj._cderi is not None,
                           'tensor_output':obj._cderi_to_save is not None}
        check('no_ERI_or_three_index_cache',record['storage'],ri._eri is None and obj._cderi is None and obj._cderi_to_save is None)
        record['status']='PASS_NUMERICAL_SCREEN_ONLY' if all(c['pass'] for c in record['checks']) else 'FAIL_NUMERICAL_SCREEN'
        mol.stdout.close()
    except Exception:
        record['status']='ERROR'; record['exception']=traceback.format_exc()
    save(out/'result.json',record); np.savez_compressed(out/'arrays.npz',**arrays)
    print(json.dumps({'case':case,'status':record['status'],'failed_checks':[c for c in record['checks'] if not c['pass']]}),flush=True)
    return 0 if record['status']=='PASS_NUMERICAL_SCREEN_ONLY' else 1


def launch():
    validate_new_case()
    validate_retrospective()
    pins=pinned_files()
    if pins!=json.loads((BASE/'preparation.json').read_text())['pins']:
        raise ValueError('Prepared source pins changed; do not launch')
    out=BASE/'run-v1'; out.mkdir(exist_ok=False)
    save(out/'pins.json',pins)
    spec=importlib.util.spec_from_file_location('parent_supervisor',LAB/'parent-pilot/pilot.py')
    supervisor=importlib.util.module_from_spec(spec); spec.loader.exec_module(supervisor)
    receipts=[]
    for case in CASES:
        receipt=supervisor.monitored_run([sys.executable,'-B',str(BASE/'run.py'),'--worker',case],out/case,180,2*2**30)
        receipts.append({'case':case,**receipt}); save(out/'receipts.json',receipts)
        print(case,receipt['returncode'],receipt['termination_reason'],flush=True)
    unchanged=pinned_files()==pins
    result={'status':'PASS_NUMERICAL_SCREEN_ONLY' if unchanged and all(accepted(r) for r in receipts) else 'FAIL_NUMERICAL_SCREEN',
            'pins_unchanged':unchanged,'parent_SCF_run':False,'physical_admission':False,
            'experimental_validation':False,'cases':[{k:r[k] for k in ('case','returncode','termination_reason','wall_seconds','sampled_max_rss_bytes')} for r in receipts]}
    save(out/'result.json',result)
    print(json.dumps(result),flush=True)
    return 0 if result['status'].startswith('PASS') else 1


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:
        prepare(); sys.exit(0)
    if sys.argv[1:2]==['--worker'] and sys.argv[2:] and sys.argv[2] in CASES:
        sys.exit(worker(sys.argv[2]))
    if sys.argv[1:]==['--launch']:
        sys.exit(launch())
    raise SystemExit('Specify --launch (fresh run only)')
