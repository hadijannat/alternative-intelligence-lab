import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import traceback

BASE=Path(__file__).resolve().parent
LAB=BASE.parent
REPEAT=LAB/'parent-j-repeatability/run-v1'
EXTERNAL=LAB/'parent-openmp-first-j-v2/run-v1/J.npy'
CHUNK_ROWS=16
ATOL=1e-10
PAIRS=(('J2-J1','J2.npy','J1.npy',1,'J2-J1'),
       ('J3+J1','J3.npy','J1.npy',-1,'(-J3)-J1'),
       ('J3+J2','J3.npy','J2.npy',-1,'(-J3)-J2'),
       ('J1-Jold','J1.npy',None,1,'J1-Jold'),
       ('J2-Jold','J2.npy',None,1,'J2-Jold'),
       ('J3+Jold','J3.npy',None,-1,'(-J3)-Jold'))


def require(value,message):
    if not value:raise ValueError(message)


def read(path):return json.loads(Path(path).read_text())


def sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def write_new(path,value):
    with Path(path).open('x') as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')


def manifest():
    paths=[BASE/name for name in ('run.py','test_run.py','PROTOCOL.md')]
    paths += [REPEAT/name for name in ('J1.npy','J2.npy','J3.npy','comparisons.json','result.json','launch-result.json','supervisor.json')]
    paths += [EXTERNAL,LAB/'parent-pilot-memory/run-v1/partial.npz',
              LAB/'parent-openmp-first-j-v2/run.py',LAB/'parent-openmp-qualification-v2/run.py']
    return {str(p):sha(p) for p in paths}


def prepare():
    write_new(BASE/'preparation.json',{'status':'PREPARED_SAVED_ARRAY_ANALYSIS_NOT_RUN','pins':manifest(),
              'real_arrays_analyzed':False,'operators_executed':0,'SCFs_launched':0})


def validate_gate():
    preparation=read(BASE/'preparation.json')
    require(preparation['pins']==manifest(),'Frozen analysis inputs/source changed')
    review=read(BASE/'independent-root-review.json')
    require(review.get('status')=='APPROVED_SAVED_ARRAY_ERROR_IMPACT' and review.get('independent_root_review') is True
            and bool(review.get('reviewer')) and review.get('preparation_sha256')==sha(BASE/'preparation.json'),'Root review binding missing')
    return {'preparation_sha256':sha(BASE/'preparation.json'),'review_sha256':sha(BASE/'independent-root-review.json')}


def impact(density,matrix,reference,orientation=1):
    import numpy as np
    require(density.ndim==2 and density.shape[0]==density.shape[1] and density.size>0,'Density must be nonempty square')
    require(orientation in (-1,1) and all(a.dtype==np.float64 and a.shape==density.shape for a in (density,matrix,reference)),
            'Invalid orientation, shape or dtype')
    maxima={'value':-1.,'index':None};above=0;delta_squares=[];density_squares=[];density_absolute=[]
    def products():
        nonlocal above
        for start in range(0,len(density),CHUNK_ROWS):
            p=density[start:start+CHUNK_ROWS];a=matrix[start:start+CHUNK_ROWS];b=reference[start:start+CHUNK_ROWS]
            require(all(np.isfinite(x).all() for x in (p,a,b)),'Nonfinite input')
            delta=orientation*a-b;terms=p*delta
            require(np.isfinite(delta).all() and np.isfinite(terms).all(),'Nonfinite difference/product')
            absolute=np.abs(delta);flat=int(np.argmax(absolute));i,j=np.unravel_index(flat,absolute.shape)
            local=float(absolute[i,j])
            if local>maxima['value']:maxima.update(value=local,index=[start+int(i),int(j)])
            above+=int(np.count_nonzero(absolute>ATOL))
            delta_squares.append(math.fsum(float(x)*float(x) for x in delta.flat))
            density_squares.append(math.fsum(float(x)*float(x) for x in p.flat))
            density_absolute.append(math.fsum(abs(float(x)) for x in p.flat))
            yield from (float(x) for x in terms.flat)
    energy=.5*math.fsum(products())
    delta_norm=math.sqrt(math.fsum(delta_squares));density_norm=math.sqrt(math.fsum(density_squares))
    bound_max=.5*math.fsum(density_absolute)*maxima['value']
    bound_frobenius=.5*density_norm*delta_norm
    require(all(math.isfinite(x) for x in (energy,delta_norm,density_norm,bound_max,bound_frobenius)),'Nonfinite norm/energy')
    return {'oriented_delta_E_C_hartree':energy,'absolute_delta_E_C_hartree':abs(energy),
            'max_absolute_entry':maxima['value'],'argmax':maxima['index'],'delta_J_Frobenius_norm':delta_norm,
            'density_Frobenius_norm':density_norm,'density_entrywise_L1_norm':math.fsum(density_absolute),
            'computed_maxnorm_energy_bound_hartree':bound_max,'computed_Frobenius_energy_bound_hartree':bound_frobenius,
            'entries_above_original_tolerance':above,'original_threshold_pass_recomputed':maxima['value']<=ATOL,
            'absolute_tolerance_unchanged':ATOL,'relative_tolerance_unchanged':0}


def analyze():
    gate=validate_gate();out=BASE/'analysis-v1';out.mkdir(exist_ok=False)
    write_new(out/'analysis-gate.json',gate)
    try:
        import numpy as np
        spec=importlib.util.spec_from_file_location('frozen_error_density_loader',LAB/'parent-openmp-first-j-v2/run.py')
        first=importlib.util.module_from_spec(spec);spec.loader.exec_module(first)
        density,density_summary=first.saved_density()
        original=read(REPEAT/'comparisons.json');results={}
        require(set(original['comparisons'])=={p[0] for p in PAIRS},'Original comparison set differs')
        for name,a,b,orientation,expression in PAIRS:
            arrays=[]
            try:
                arrays.append(np.load(REPEAT/a,allow_pickle=False,mmap_mode='r'))
                arrays.append(np.load(REPEAT/b if b is not None else EXTERNAL,allow_pickle=False,mmap_mode='r'))
                result=impact(density,*arrays,orientation)
            finally:
                for array in arrays:
                    if getattr(array,'_mmap',None) is not None:array._mmap.close()
            prior=original['comparisons'][name]
            require(prior['absolute_tolerance']==ATOL and prior['relative_tolerance']==0
                    and result['max_absolute_entry']==prior['max_absolute_error'] and result['argmax']==prior['argmax']
                    and result['entries_above_original_tolerance']==prior['entries_above_tolerance']
                    and result['original_threshold_pass_recomputed'] is prior['pass'],'Original comparison does not reproduce: '+name)
            results[name]={'oriented_expression':expression,'original_comparison':prior,**result}
        require(sum(not r['original_comparison']['pass'] for r in results.values())==5,'Expected five original nonpasses changed')
        del density
        require(validate_gate()==gate,'Analysis pins/review changed')
        report={'status':'COMPLETE_FIXED_DENSITY_SENSITIVITY_ONLY','comparisons':results,'density':density_summary,
                'original_categories_unchanged':original['categories'],'original_nonpasses':5,'original_passes':1,
                'AO_element_localization':None,'localization_omitted_reason':'Full exact AO-to-atom map was not saved; four labels do not validate a full reconstruction.',
                'summation':'math.fsum over all binary64 Pij*deltaJij products; not a certified exact-real or outward-rounded calculation',
                'interpretation':'Fixed-density Coulomb-energy sensitivity only; no relaxed SCF, chemical-accuracy or crash-cause conclusion',
                'tolerance_relaxed':False,'operators_executed':0,'SCFs_launched':0,'physical_admission':False,
                'parent_SCF_readiness':False,'input_pins_unchanged':True,'numpy_version':np.__version__}
        write_new(out/'result.json',report)
        lines=['# Fixed-density Coulomb-energy sensitivity','',
               'Five of six original J comparisons remain nonpassing at absolute 1e-10, rtol=0. Energy sensitivity does not relax that result or establish SCF/chemical accuracy.','',
               '| Original comparison | Oriented delta | Original pass | delta E_C (Hartree) | Frobenius norm |',
               '|---|---|---|---|---|']
        for name,r in results.items():
            lines.append(f"| {name} | {r['oriented_expression']} | {r['original_comparison']['pass']} | {r['oriented_delta_E_C_hartree']:.17g} | {r['delta_J_Frobenius_norm']:.17g} |")
        lines+=['','Bounds and full original comparison records are in result.json. J3 is oriented back to positive density. AO/element localization is omitted because a full exact mapping was not saved. No new operators, SCFs or fits were run.']
        with (out/'REPORT.md').open('x') as stream:stream.write('\n'.join(lines)+'\n')
        return 0
    except Exception:
        write_new(out/'failure.json',{'exception':traceback.format_exc(),'operators_executed':0,'SCFs_launched':0})
        raise


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:prepare()
    elif sys.argv[1:]==['--gate-check']:print(json.dumps(validate_gate(),indent=2))
    elif sys.argv[1:]==['--analyze']:sys.exit(analyze())
    else:raise SystemExit('Use --prepare, --gate-check or --analyze; no implicit analysis')
