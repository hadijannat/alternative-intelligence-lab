import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import traceback
from contextlib import contextmanager

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
spec = importlib.util.spec_from_file_location('frozen_metric_helpers', LAB/'parent-metric-solve-diagnostic/run.py')
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
r, s = v1.r, v1.s
read, require = r.read, r.require
SOURCE = v1.SOURCE
V2 = LAB/'parent-metric-solve-diagnostic-v2'
MATRIX = V2/'run-v1/original_metric.npy'
MATRIX_SHA = '00a6c22b1bbf0d90ae9d4905b4dd4fa9edc864bb27c2af9a93ca2ce1b40aa3af'
STATUS = 'COMPLETED_SAVED_METRIC_SOLVE_DIAGNOSTIC_ONLY'
APPROVAL = 'APPROVED_ONE_SAVED_METRIC_SOLVE_DIAGNOSTIC'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path = Path(path).resolve()
    require(path.is_relative_to(BASE), 'Output outside diagnostic')
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def manifest():
    v1.sha = s.sha = r.sha = sha
    pins = v1.manifest()
    paths = [BASE/name for name in ('run.py', 'test_run.py', 'PROTOCOL.md', 'qualification.json')]
    paths += [p for p in sorted((BASE/'qualification-thread').rglob('*')) if p.is_file()]
    paths += [V2/name for name in ('run.py', 'preparation.json', 'qualification.json', 'independent-root-review.json')]
    paths += [p for p in sorted((V2/'run-v1').iterdir()) if p.is_file()]
    paths += [p for p in sorted((V2/'postmortem').rglob('*')) if p.is_file()]
    paths += [p for p in sorted((LAB/'parent-blas-control-audit').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    pins['saved_metric_replay'] = {str(p): sha(p) for p in paths}
    require(pins['saved_metric_replay'][str(MATRIX)] == MATRIX_SHA, 'Saved metric bytes changed')
    return pins


def prepare():
    require(read(BASE/'qualification.json')['passed'] is True, 'Tiny qualification failed')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve() == Path(runtime['python']).resolve(), 'Wrong interpreter')
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    write(BASE/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW', 'pins': manifest(),
        'wall_cap_seconds': 1000, 'sampled_RSS_guard_bytes': 10*2**30, 'maximum_children': 1,
        'parent_metric_builds': 0, 'factorizations': 1, 'explicit_solves': 4,
        'matrix_access': 'read-only mmap; one writable Fortran factor copy; no new saved metric',
        'condition_estimator_internal_solves': 'LAPACK controlled; wall capped',
        'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0, 'physical_admission': False})


def gate():
    prep = read(BASE/'preparation.json')
    require(prep['pins'] == manifest(), 'Preparation inputs changed')
    approval = read(BASE/'independent-root-review.json')
    require(approval.get('status') == APPROVAL and approval.get('independent_root_review') is True
            and bool(approval.get('reviewer')), 'Independent root review required')
    require(approval.get('preparation_sha256') == sha(BASE/'preparation.json')
            and approval.get('qualification_artifacts') == prep['pins']['qualification'], 'Approval binding changed')
    return {'preparation_sha256': sha(BASE/'preparation.json'), 'review_sha256': sha(BASE/'independent-root-review.json')}


def save_array(out, name, array):
    import numpy as np
    with (out/(name+'.npy')).open('xb') as stream:
        np.save(stream, array, allow_pickle=False)


def checked_matrix(path, n=19612):
    import numpy as np
    matrix = np.load(path, mmap_mode='r', allow_pickle=False)
    require(matrix.shape == (n, n) and matrix.dtype == np.float64
            and matrix.flags.f_contiguous and not matrix.flags.writeable, 'Saved matrix layout changed')
    return matrix


@contextmanager
def single_blas_fresh_child(emit):
    from pyscf import lib
    import scipy.linalg._flapack as flapack
    control = r.load('frozen_blas_probe', LAB/'parent-blas-control-audit/probe.py')
    require(all(os.environ.get(k) == value for k, value in control.REQUESTED.items()), 'Thread environment changed')
    blas = ctypes.CDLL(str(control.ENV/'lib/libopenblas.0.dylib'))
    for name in ('openblas_get_num_threads', 'openblas_get_parallel'):
        function = getattr(blas, name)
        function.argtypes, function.restype = [], ctypes.c_int
    blas.openblas_get_config.argtypes, blas.openblas_get_config.restype = [], ctypes.c_char_p
    blas.openblas_set_num_threads.argtypes, blas.openblas_set_num_threads.restype = [ctypes.c_int], None
    lapack = ctypes.CDLL(str(control.ENV/'lib/liblapack.3.dylib'))
    scipy_binary = ctypes.CDLL(flapack.__file__)
    address = lambda function: ctypes.cast(function, ctypes.c_void_p).value
    require(address(scipy_binary.dpotrf_) == address(lapack.dpotrf_) == address(blas.dpotrf_), 'LAPACK symbol differs')
    frozen = read(LAB/'parent-blas-control-audit/observed.json')
    identity = {p: sha(p) for p in frozen['binary_sha256']}
    require(identity == frozen['binary_sha256'] and sha(flapack.__file__) == frozen['flapack_sha256'], 'BLAS binary differs')
    emit('identity', {'binary_sha256': identity, 'flapack_binary': flapack.__file__,
         'flapack_sha256': sha(flapack.__file__), 'same_dpotrf_symbol': True,
         'dpotrf_address': address(blas.dpotrf_), 'config': blas.openblas_get_config().decode(),
         'parallel': blas.openblas_get_parallel(), 'counts_are_configured_limits_not_measured_team_sizes': True})
    initial = (blas.openblas_get_num_threads(), lib.num_threads())
    require(initial == (4, 4), 'Fresh child configured counts differ')
    emit('initial', {'blas': initial[0], 'pyscf': initial[1]})
    def snapshot(label):
        row = {'label': label, 'blas': blas.openblas_get_num_threads(), 'pyscf': lib.num_threads()}
        emit(label, row)
        require((row['blas'], row['pyscf']) == (1, 4), 'Configured thread counts changed')
    try:
        blas.openblas_set_num_threads(1)
        snapshot('explicit_setter')
        yield snapshot
    finally:
        blas.openblas_set_num_threads(initial[0])
        lib.num_threads(initial[1])
        row = {'blas': blas.openblas_get_num_threads(), 'pyscf': lib.num_threads(), 'explicit_control_mode_restored': False}
        emit('restored_getter_counts', row)
        require((row['blas'], row['pyscf']) == initial, 'Getter count restoration failed')


def solve_sequence(matrix, memory, out, thread_state, source=SOURCE, matrix_file_sha=MATRIX_SHA):
    import numpy as np
    matrix_hash = r.array_digest(matrix)
    thread_state('before_factor')
    factor = memory.factor_inplace(matrix.copy(order='F'))
    thread_state('after_factor')
    factor_hash = r.array_digest(factor[0])
    prior = read(source/'factor-states.json')[0]['content_sha256']
    write(out/'matrix-factor.json', {'metric_array_sha256': matrix_hash, 'metric_file_sha256': matrix_file_sha,
        'factor_sha256': factor_hash, 'prior_factor_sha256': prior, 'factor_matches_prior': factor_hash == prior,
        'factor_saved': False, 'prior_call_causality_established': False})
    answers = {}
    for name, arm in (('A1', 'A'), ('A2', 'A'), ('B', 'B'), ('C', 'C')):
        rhs = np.load(source/f'b_{arm}.npy', allow_pickle=False)
        require(rhs.shape == (len(matrix), 1), 'Unexpected saved RHS')
        before = r.array_digest(rhs)
        thread_state('before_solve_'+name)
        answer = memory.solve_checked(factor, rhs)
        thread_state('after_solve_'+name)
        require(r.array_digest(rhs) == before, 'Solve mutated RHS')
        save_array(out, 'rho_'+name, answer)
        errors, residual = v1.norms_and_errors(matrix, rhs, answer)
        save_array(out, 'residual_'+name, residual)
        errors['versus_prior_rho'] = s.vector_difference(answer, np.load(source/f'rho_ordinary_{arm}.npy', allow_pickle=False))
        write(out/f'errors-{name}.json', errors)
        answers[name] = answer
    require(errors['matrix_symmetry_max'] == 0, 'Metric not exactly symmetric')
    thread_state('before_condition_estimate')
    condition = v1.condition_estimate(factor, errors['matrix_infinity_norm'])
    thread_state('after_condition_estimate')
    comparisons = {name: s.vector_difference(answer, answers['A1']) for name, answer in answers.items() if name != 'A1'}
    require(r.array_digest(factor[0]) == factor_hash and r.array_digest(matrix) == matrix_hash, 'Metric/factor mutated')
    return {'comparisons': comparisons, 'condition': condition, 'factor_matches_prior': factor_hash == prior}


def worker():
    out = BASE/'run-v1'
    token = gate()
    require(read(out/'launch-gate.json') == token, 'Launch gate changed')
    write(out/'worker-started.json', {'pid': os.getpid(), 'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0})
    require(shutil.disk_usage(out).free >= 4*2**30, 'Need 4 GiB free reserve')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    memory = r.load('frozen_memory_saved_metric', LAB/'cpcm-rij-memory/memory.py')
    with single_blas_fresh_child(lambda label, row: write(out/('threads-'+label+'.json'), row)) as state:
        state('before_matrix_load')
        matrix = checked_matrix(MATRIX)
        result = solve_sequence(matrix, memory, out, state)
        matrix._mmap.close()
        state('after_matrix_close')
    require(gate() == token and r.qualification.runtime_pins() == runtime, 'Final gate/runtime changed')
    write(out/'result.json', {'status': STATUS, **result, 'J_calls': 0, 'SCFs': 0, 'PCM_builds': 0,
        'physical_admission': False, 'parent_SCF_readiness': False, 'prior_J_tolerance_unchanged': 1e-10,
        'thread_counts_are_configured_getters_not_measured_team_sizes': True,
        'prior_call_causality_established': False})


def launch():
    token = gate()
    out = BASE/'run-v1'
    out.mkdir(exist_ok=False)
    write(out/'launch-gate.json', token)
    supervisor = r.load('saved_metric_supervisor', LAB/'parent-pilot/pilot.py')
    supervisor.THREADS = {**supervisor.THREADS, 'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE'}
    python = read(r.first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt = supervisor.monitored_run([python, '-B', str(BASE/'run.py'), '--worker'], out, 1000, 10*2**30)
    result = read(out/'result.json') if (out/'result.json').exists() else {}
    complete = r.first.accepted(receipt) and result.get('status') == STATUS and gate() == token
    write(out/'launch-result.json', {'completed': complete, 'receipt': receipt,
        'artifact_hashes': {p.name: sha(p) for p in out.iterdir() if p.is_file()}, 'physical_admission': False})
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
