import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ENV = BASE.parent / 'parent-openmp/env-aligned'
REQUESTED = {'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE',
             'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
             'VECLIB_MAXIMUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1'}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def worker():
    import numpy as np
    import scipy.linalg as la
    import scipy.linalg._flapack as flapack
    from pyscf import lib

    assert all(os.environ.get(k) == v for k, v in REQUESTED.items())
    blas_path = ENV / 'lib/libopenblas.0.dylib'
    blas = ctypes.CDLL(str(blas_path))
    for name in ('openblas_get_num_threads', 'openblas_get_parallel'):
        function = getattr(blas, name)
        function.argtypes, function.restype = [], ctypes.c_int
    blas.openblas_get_config.argtypes = []
    blas.openblas_get_config.restype = ctypes.c_char_p
    blas.openblas_set_num_threads.argtypes = [ctypes.c_int]
    blas.openblas_set_num_threads.restype = None
    lapack = ctypes.CDLL(str(ENV / 'lib/liblapack.3.dylib'))
    address = lambda f: ctypes.cast(f, ctypes.c_void_p).value
    assert address(blas.dpotrf_) == address(lapack.dpotrf_)
    dyld = ctypes.CDLL(None)
    dyld._dyld_image_count.argtypes, dyld._dyld_image_count.restype = [], ctypes.c_uint32
    dyld._dyld_get_image_name.argtypes = [ctypes.c_uint32]
    dyld._dyld_get_image_name.restype = ctypes.c_char_p
    loaded = [dyld._dyld_get_image_name(i).decode() for i in range(dyld._dyld_image_count())]
    selected = [p for p in loaded if any(s in p.lower() for s in ('blas', 'lapack', 'libomp', 'libnp_helper'))]
    result = {'requested_environment': REQUESTED, 'config': blas.openblas_get_config().decode(),
              'parallel': blas.openblas_get_parallel(), 'loaded_images': selected,
              'binary_sha256': {p: digest(p) for p in selected},
              'same_dpotrf_symbol': True, 'dpotrf_address': address(blas.dpotrf_),
              'flapack_dependencies': subprocess.check_output(['otool', '-L', flapack.__file__], text=True),
              'source_sha256': digest(__file__), 'states': [], 'solves': []}
    try:
        import threadpoolctl
        result['threadpoolctl_probe'] = {'available': True, 'path': threadpoolctl.__file__}
    except ImportError as exc:
        result['threadpoolctl_probe'] = {'available': False, 'exception': type(exc).__name__, 'message': str(exc)}

    def state(label):
        row = {'label': label, 'blas': blas.openblas_get_num_threads(), 'pyscf': lib.num_threads()}
        result['states'].append(row)
        return row

    lower = np.array([[2., 0, 0, 0], [1, 2, 0, 0], [-1, .5, 2, 0], [.5, -.5, 1, 2]])
    matrix = lower @ lower.T
    expected = np.array([1., -2., 3., -.5])
    rhs = matrix @ expected
    answers = []

    def solve(label):
        before = state(label + '_before')
        writable = np.array(matrix, order='F', copy=True)
        factor = la.cho_factor(writable, lower=True, overwrite_a=True, check_finite=False)
        assert np.shares_memory(writable, factor[0])
        actual = la.cho_solve(factor, rhs, check_finite=False)
        residual = float(np.max(np.abs(matrix @ actual - rhs)))
        error = float(np.max(np.abs(actual - expected)))
        tolerance = float(100 * np.finfo(float).eps * max(1., np.max(np.abs(rhs))))
        assert residual <= tolerance and error <= tolerance
        after = state(label + '_after')
        assert (before['blas'], before['pyscf']) == (after['blas'], after['pyscf'])
        result['solves'].append({'label': label, 'matrix': matrix.tolist(), 'rhs': rhs.tolist(),
                                 'expected': expected.tolist(), 'answer': actual.tolist(),
                                 'residual_max_abs': residual, 'error_max_abs': error,
                                 'tolerance': tolerance, 'pass': True})
        answers.append(actual)

    initial = state('initial')
    assert initial['blas'] == initial['pyscf'] == 4
    solve('baseline')
    with lib.with_omp_threads(1):
        solve('pyscf_context_before_explicit_setter')
    state('pyscf_context_restored')
    try:
        blas.openblas_set_num_threads(1)
        solve('explicit_blas_one')
        with lib.with_omp_threads(1):
            solve('pyscf_context_after_explicit_setter')
        state('pyscf_context_restored_after_setter')
        raise RuntimeError('intentional restoration test')
    except RuntimeError as exc:
        assert str(exc) == 'intentional restoration test'
        result['intentional_exception_observed'] = True
    finally:
        blas.openblas_set_num_threads(initial['blas'])
        lib.num_threads(initial['pyscf'])
    restored = state('restored_after_exception')
    assert restored['blas'] == restored['pyscf'] == 4
    solve('restored')
    result['max_answer_difference'] = max(float(np.max(np.abs(a - answers[0]))) for a in answers)
    result['bitwise_equal_answers'] = all(np.array_equal(a, answers[0]) for a in answers)
    result['environment_unchanged'] = all(os.environ.get(k) == v for k, v in REQUESTED.items())
    assert result['environment_unchanged']
    result['completed'] = True
    (BASE / 'observed.json').write_text(json.dumps(result, indent=2) + '\n')


def launch():
    assert Path(sys.executable).resolve() == (ENV / 'bin/python').resolve()
    for name in ('observed.json', 'supervisor.json', 'stdout.txt', 'stderr.txt'):
        if (BASE / name).exists():
            raise RuntimeError('Refusing to overwrite existing evidence: ' + name)
    command = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker']
    start, peak, samples, limit = time.monotonic(), 0, 0, None
    with (BASE / 'stdout.txt').open('x') as out, (BASE / 'stderr.txt').open('x') as err:
        child = subprocess.Popen(command, stdout=out, stderr=err, env={**os.environ, **REQUESTED})
        try:
            while child.poll() is None:
                rss = subprocess.run(['ps', '-o', 'rss=', '-p', str(child.pid)], capture_output=True, text=True, timeout=2)
                if rss.returncode == 0 and rss.stdout.strip():
                    peak = max(peak, int(rss.stdout.strip()) * 1024)
                    samples += 1
                if peak > 1024 ** 3 or time.monotonic() - start > 30:
                    limit = 'sampled_rss' if peak > 1024 ** 3 else 'wall_time'
                    child.kill()
                    break
                time.sleep(.05)
            child.wait(timeout=2)
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=2)
            receipt = {'command': command, 'pid': child.pid, 'returncode': child.returncode,
                       'wall_seconds': time.monotonic() - start, 'sampled_peak_rss_bytes': peak,
                       'rss_samples': samples, 'wall_limit_seconds': 30, 'rss_limit_bytes': 1024 ** 3,
                       'limit_hit': limit, 'scope': 'one fresh child; five 4x4 SPD solves; no molecular integrals',
                       'artifacts': {p.name: digest(p) for p in BASE.iterdir() if p.is_file() and p.name != 'supervisor.json'}}
            (BASE / 'supervisor.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if child.returncode or limit:
        raise RuntimeError('Bounded child failed; inspect preserved stderr and supervisor')


if __name__ == '__main__':
    if sys.argv[1:] == ['--worker']:
        worker()
    elif not sys.argv[1:]:
        launch()
    else:
        raise SystemExit('usage: probe.py [--worker]')
