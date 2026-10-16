import importlib.util
import json
import os
import shutil
from pathlib import Path
import sys
import traceback

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
spec = importlib.util.spec_from_file_location('stage_helpers', LAB/'parent-j-stage-localization/run.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
r = s.r
read, sha, require = r.read, r.sha, r.require
SOURCE = s.BASE/'run-v1'
STATUS = 'COMPLETED_METRIC_SOLVE_DIAGNOSTIC_ONLY'


def write(path, value):
    path = Path(path).resolve()
    require(path.is_relative_to(BASE), 'Output outside diagnostic')
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def manifest():
    pins = s.manifest()
    paths = [SOURCE/n for n in ('factor-states.json', 'result.json', 'launch-result.json', 'molecule-state.json', 'optimizer-baseline.json')]
    paths += [SOURCE/f'{field}_{arm}.npy' for field in ('b', 'rho_ordinary') for arm in 'ABC']
    paths += [s.BASE/'run.py', s.BASE/'preparation.json', BASE/'run.py', BASE/'test_run.py', BASE/'PROTOCOL.md', BASE/'qualification.json']
    pins['metric_diagnostic'] = {str(p): sha(p) for p in paths}
    return pins


def prepare():
    require(read(BASE/'qualification.json')['passed'] is True, 'Tiny qualification failed')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve() == Path(runtime['python']).resolve(), 'Wrong interpreter')
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    require(read(SOURCE/'launch-result.json')['completed'] is True, 'Prior diagnostic incomplete')
    write(BASE/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW', 'pins': manifest(), 'wall_cap_seconds': 1000, 'sampled_RSS_guard_bytes': 10*2**30, 'maximum_children': 1, 'parent_metric_builds': 1, 'factorizations': 1, 'explicit_solves': 4, 'condition_estimator_internal_solves': 'LAPACK controlled; wall capped', 'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0, 'physical_admission': False})


def gate():
    prep = read(BASE/'preparation.json')
    require(prep['pins'] == manifest(), 'Preparation inputs changed')
    approval = read(BASE/'independent-root-review.json')
    require(approval.get('status') == 'APPROVED_ONE_PARENT_METRIC_SOLVE_DIAGNOSTIC' and approval.get('independent_root_review') is True and bool(approval.get('reviewer')), 'Independent root review required')
    require(approval.get('preparation_sha256') == sha(BASE/'preparation.json') and approval.get('qualification_artifacts') == prep['pins']['qualification'], 'Approval binding changed')
    return {'preparation_sha256': sha(BASE/'preparation.json'), 'review_sha256': sha(BASE/'independent-root-review.json')}


def norms_and_errors(matrix, rhs, answer, rows=32):
    import numpy as np
    n = len(rhs)
    require(matrix.shape == (n, n) and answer.shape == rhs.shape == (n, 1), 'Dimension mismatch')
    rowsums = np.empty(n)
    residual = np.empty_like(rhs)
    component_scale = np.empty_like(rhs)
    symmetry = 0.
    for a in range(0, n, rows):
        block = matrix[a:a+rows]
        require(np.isfinite(block).all(), 'Nonfinite metric')
        absolute = np.abs(block)
        rowsums[a:a+rows] = absolute.sum(axis=1)
        residual[a:a+rows] = rhs[a:a+rows] - block @ answer
        component_scale[a:a+rows] = absolute @ np.abs(answer) + np.abs(rhs[a:a+rows])
        symmetry = max(symmetry, float(np.max(np.abs(block-matrix[:, a:a+rows].T))))
    require(np.isfinite(residual).all() and np.isfinite(component_scale).all(), 'Nonfinite residual')
    norm = float(rowsums.max())
    resid = float(np.max(np.abs(residual)))
    denom = norm*float(np.max(np.abs(answer))) + float(np.max(np.abs(rhs)))
    ratio = np.divide(np.abs(residual), component_scale, out=np.zeros_like(residual), where=component_scale != 0)
    require(not np.any((component_scale == 0) & (residual != 0)), 'Undefined component residual')
    return {'matrix_infinity_norm': norm, 'matrix_symmetry_max': symmetry, 'residual_infinity_norm': resid, 'normwise_backward_error': resid/denom if denom else 0., 'componentwise_backward_error': float(ratio.max()), 'certified_error_bound': False}, residual


def condition_estimate(factor, norm):
    from scipy.linalg.lapack import dpocon
    reciprocal, info = dpocon(factor[0], norm, uplo='L')
    require(info == 0 and 0 <= reciprocal <= 1, 'DPOCON failed')
    return {'reciprocal_one_norm_condition_estimate': float(reciprocal), 'one_norm_condition_estimate': float(1/reciprocal) if reciprocal else None, 'info': int(info), 'certified_bound': False}


def worker():
    import numpy as np
    from pyscf import gto, lib
    from pyscf.df import addons
    out = BASE/'run-v1'
    token = gate()
    require(read(out/'launch-gate.json') == token, 'Launch gate changed')
    write(out/'worker-started.json', {'pid': os.getpid(), 'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0})
    require(shutil.disk_usage(out).free >= 19612**2*8 + 4*2**30, 'Need metric storage plus 4 GiB free reserve')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(lib.num_threads() == 4 and os.environ.get('OMP_NUM_THREADS') == '4' and os.environ.get('OMP_DYNAMIC') == 'FALSE', 'OpenMP controls changed')
    require(all(os.environ.get(k) == '1' for k in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')), 'BLAS controls changed')
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    memory = r.load('frozen_memory_metric_only', LAB/'cpcm-rij-memory/memory.py')
    mol = gto.M(atom=r.first.parent_atoms(), unit='Angstrom', basis='def2-svp', ecp={'Mo': 'def2-svp'}, charge=-8, spin=0, verbose=4, max_memory=8000, output=str(out/'native.log'))
    r.molecule_state(mol, read(SOURCE/'molecule-state.json'))
    aux = addons.make_auxmol(mol, 'def2-universal-jkfit')
    r.molecule_state(aux, read(SOURCE/'optimizer-baseline.json')['auxmol'])
    matrix = aux.intor('int2c2e', hermi=1)
    require(matrix.shape == (19612, 19612) and matrix.flags.f_contiguous, 'Metric layout changed')
    metric_hash = r.array_digest(matrix)
    s.save_array(out, 'original_metric', matrix)
    matrix.flags.writeable = False
    factor = memory.factor_inplace(matrix.copy(order='F'))
    factor_hash = r.array_digest(factor[0])
    prior = read(SOURCE/'factor-states.json')[0]['content_sha256']
    write(out/'matrix-factor.json', {'metric_sha256': metric_hash, 'factor_sha256': factor_hash, 'prior_factor_sha256': prior, 'factor_matches_prior': factor_hash == prior, 'metric_saved': True, 'factor_saved': False})
    answers = {}
    for name, arm in (('A1', 'A'), ('A2', 'A'), ('B', 'B'), ('C', 'C')):
        rhs = np.load(SOURCE/f'b_{arm}.npy', allow_pickle=False)
        require(rhs.shape == (19612, 1), 'Unexpected saved RHS')
        before = r.array_digest(rhs)
        answer = memory.solve_checked(factor, rhs)
        require(r.array_digest(rhs) == before, 'Solve mutated RHS')
        s.save_array(out, 'rho_'+name, answer)
        errors, residual = norms_and_errors(matrix, rhs, answer)
        s.save_array(out, 'residual_'+name, residual)
        errors['versus_prior_rho'] = s.vector_difference(answer, np.load(SOURCE/f'rho_ordinary_{arm}.npy', allow_pickle=False))
        write(out/f'errors-{name}.json', errors)
        answers[name] = answer
    require(errors['matrix_symmetry_max'] == 0, 'Metric not exactly symmetric; infinity norm not accepted as one norm')
    condition = condition_estimate(factor, errors['matrix_infinity_norm'])
    comparisons = {name: s.vector_difference(answer, answers['A1']) for name, answer in answers.items() if name != 'A1'}
    require(r.array_digest(factor[0]) == factor_hash and r.array_digest(matrix) == metric_hash, 'Metric/factor mutated')
    require(gate() == token and r.qualification.runtime_pins() == runtime, 'Final gate/runtime changed')
    write(out/'result.json', {'status': STATUS, 'comparisons': comparisons, 'condition': condition, 'factor_matches_prior': factor_hash == prior, 'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0, 'physical_admission': False, 'parent_SCF_readiness': False, 'prior_J_tolerance_unchanged': 1e-10})
    mol.stdout.close()


def launch():
    token = gate()
    out = BASE/'run-v1'
    out.mkdir(exist_ok=False)
    write(out/'launch-gate.json', token)
    supervisor = r.load('metric_supervisor', LAB/'parent-pilot/pilot.py')
    supervisor.THREADS = {**supervisor.THREADS, 'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE'}
    python = read(r.first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt = supervisor.monitored_run([python, '-B', str(BASE/'run.py'), '--worker'], out, 1000, 10*2**30)
    result = read(out/'result.json') if (out/'result.json').exists() else {}
    complete = r.first.accepted(receipt) and result.get('status') == STATUS and gate() == token
    write(out/'launch-result.json', {'completed': complete, 'receipt': receipt, 'artifact_hashes': {p.name: sha(p) for p in out.iterdir() if p.is_file()}, 'physical_admission': False})
    return 0 if complete else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']: prepare()
    elif sys.argv[1:] == ['--gate-check']: print(json.dumps(gate()))
    elif sys.argv[1:] == ['--launch']: sys.exit(launch())
    elif sys.argv[1:] == ['--worker']:
        try: worker()
        except Exception:
            write(BASE/'run-v1/failure.json', {'exception': traceback.format_exc(), 'physical_admission': False})
            raise
    else: raise SystemExit('Use --prepare, --gate-check or --launch')
