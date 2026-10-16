import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback
from contextlib import contextmanager

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
spec = importlib.util.spec_from_file_location('frozen_explicit_j', LAB/'parent-explicit-blas-j/run.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
r, s, replay = e.r, e.s, e.replay
read, require, sha = e.read, e.require, e.sha
ARMS = ('A', 'B')
WALL, RSS = 1800, 10*2**30
STATUS = 'COMPLETED_SERIAL_RHS_PREFIX_DIAGNOSTIC_ONLY'
APPROVAL = 'APPROVED_ONE_SERIAL_RHS_PREFIX_DIAGNOSTIC'


def write(path, value):
    path = Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()), 'Output outside diagnostic')
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def manifest():
    from pyscf.scf import jk, _vhf
    from pyscf.lib import misc
    pins = e.manifest()
    paths = [BASE/n for n in ('run.py', 'test_run.py', 'PROTOCOL.md', 'qualification.json')]
    paths += [e.BASE/n for n in ('preparation.json', 'independent-root-review.json')]
    paths += sorted(p for p in (e.BASE/'run-v1').iterdir() if p.is_file())
    paths += [Path(module.__file__) for module in (jk, _vhf, misc)]
    pins['serial_rhs'] = {str(p): sha(p) for p in paths}
    return pins


def prepare():
    require(read(BASE/'qualification.json')['passed'] is True, 'Mock qualification failed')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve() == Path(runtime['python']).resolve(), 'Wrong interpreter')
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    require(read(e.BASE/'run-v1/launch-result.json')['completed'] is True, 'Prior diagnostic incomplete')
    pins = manifest()
    density, summary = r.first.saved_density()
    write(BASE/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW',
        'pins': pins, 'positive_density_sha256': r.array_digest(density), 'density': summary,
        'maximum_children': 1, 'maximum_prefix_attempts': 2, 'maximum_factorizations': 1,
        'wall_cap_seconds': WALL, 'sampled_RSS_guard_bytes': RSS,
        'solves': 0, 'complete_J_calls': 0, 'SCFs': 0, 'PCM_builds': 0, 'operators_executed': 0,
        'criterion': 'finite float64 (19612,1), bitwise A equals B',
        'J_absolute_tolerance': 1e-10, 'J_relative_tolerance': 0, 'J_criterion_tested': False,
        'physical_admission': False, 'parent_SCF_readiness': False, 'held_out_validation': False})


def gate():
    prep = read(BASE/'preparation.json')
    require(prep['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW' and prep['pins'] == manifest(), 'Preparation changed')
    approval = read(BASE/'independent-root-review.json')
    require(approval.get('status') == APPROVAL and approval.get('independent_root_review') is True
            and bool(approval.get('reviewer')), 'Independent root review required')
    require(approval.get('preparation_sha256') == sha(BASE/'preparation.json')
            and approval.get('qualification_artifacts') == prep['pins']['qualification'], 'Approval binding changed')
    return {'preparation_sha256': sha(BASE/'preparation.json'), 'review_sha256': sha(BASE/'independent-root-review.json')}


class PrefixStop(BaseException):
    pass


class RHSCapture:
    def __init__(self, unused_solve, state, naux=19612):
        self.state, self.naux = state, naux
        self.arm, self.baseline = None, None
        self.data = {}
        self.stop = PrefixStop()
        self.sentinel_count = 0

    def __call__(self, factor, rhs, **kwargs):
        import numpy as np
        require(self.arm in ARMS and self.arm not in self.data, 'Unexpected or duplicate sentinel')
        current = self.state()
        if self.baseline is None: self.baseline = current
        require(current == self.baseline, 'Optimizer changed at sentinel')
        require(rhs.dtype == np.float64 and rhs.shape == (self.naux, 1)
                and (rhs.flags.c_contiguous or rhs.flags.f_contiguous), 'Unexpected RHS layout')
        self.data[self.arm] = rhs.copy(order='K')
        self.sentinel_count += 1
        raise self.stop


@contextmanager
def serial_pass1(mf, capture, stage, lib, jk, prescreen):
    native = jk.get_jk
    count = [0]
    def contract(fakemol, dm, scripts, intor, **kwargs):
        opt = mf._rij_df._vjopt
        nbas, nbas1 = mf.mol.nbas, mf.mol.nbas + mf._rij_df.auxmol.nbas
        require(count[0] == 0 and scripts == ['ijkl,ji->kl'] and intor == 'int3c2e'
                and kwargs == {'aosym': 's2ij', 'hermi': 0,
                    'shls_slice': (0, nbas, 0, nbas, nbas, nbas1, nbas1, nbas1+1), 'vhfopt': opt}
                and fakemol is opt.fakemol and opt.prescreen == prescreen,
                'Unexpected contraction or pass 2')
        require(lib.num_threads() == 4, 'Pass 1 entry threads differ')
        count[0] += 1
        with lib.with_omp_threads(1):
            require(lib.num_threads() == 1, 'Pass 1 not serial')
            stage('pass1_enter', arm=capture.arm, threads=lib.num_threads())
            answer = native(fakemol, dm, scripts, intor, **kwargs)
            stage('pass1_return', arm=capture.arm, threads=lib.num_threads())
        require(lib.num_threads() == 4, 'Pass 1 threads not restored')
        return answer
    jk.get_jk = contract
    try: yield count
    finally:
        jk.get_jk = native
        require(lib.num_threads() == 4, 'Interception exit threads differ')


def difference(a, b):
    import numpy as np
    result = s.vector_difference(a, b)
    result.update({'bitwise_equal': a.tobytes(order='C') == b.tobytes(order='C'),
                   'unequal_entries': int(np.count_nonzero(a != b))})
    return result


def classify(out):
    import numpy as np
    arrays = {arm: np.load(out/f'b_{arm}.npy', allow_pickle=False) for arm in ARMS}
    require(all(a.shape == (19612, 1) and a.dtype == np.float64 and np.isfinite(a).all()
                for a in arrays.values()), 'Invalid captured RHS')
    repeat = difference(arrays['B'], arrays['A'])
    history = {arm+'-old-'+old: difference(arrays[arm], np.load(e.BASE/f'run-v1/b_{old}.npy', allow_pickle=False))
               for arm in ARMS for old in ARMS}
    return {'repeat': repeat, 'historical_OMP4': history, 'serial_RHS_repeat_pass': repeat['bitwise_equal'],
            'exclusive_causality_established': False, 'J_criterion_tested': False,
            'J_absolute_tolerance': 1e-10, 'J_relative_tolerance': 0}


def run_calls(mf, out, capture, loader, guard, storage, flush, threads, stage, expected, lib, jk, prescreen):
    records = []
    for number, arm in enumerate(ARMS, 1):
        guard(); r.signed.restrict(mf)
        require(mf._rij_calls == 0 and len(capture.data) == number-1, 'Prefix count differs')
        density, source = loader()
        require(r.array_digest(density) == expected, 'P0 changed')
        capture.arm = arm
        threads('before_prefix_'+arm)
        if capture.baseline is not None: require(capture.state() == capture.baseline, 'Optimizer changed before prefix')
        stage('prefix_attempt', arm=arm)
        with serial_pass1(mf, capture, stage, lib, jk, prescreen) as count:
            try: mf.get_j(dm=density)
            except PrefixStop as exc:
                if exc is not capture.stop: raise
            else: raise ValueError('Prefix returned without sentinel')
        require(count[0] == 1 and arm in capture.data and capture.sentinel_count == number, 'Prefix counters differ')
        hashes = {'b_'+arm: s.save_array(out, 'b_'+arm, capture.data[arm])}
        write(out/f'closed-output-hashes-{arm}.json', hashes)
        flush(); threads('after_prefix_'+arm)
        require(mf._rij_calls == 0 and r.array_digest(density) == expected, 'Unexpected completed J or density mutation')
        require(capture.state() == capture.baseline, 'Optimizer changed after prefix')
        state = storage(0); guard()
        records.append({'arm': arm, 'prefix_attempts': number, 'pass1_calls': number,
            'sentinel_count': capture.sentinel_count, 'complete_J_calls': 0, 'solves': 0,
            'hashes': hashes, 'storage': state, 'source': source})
        write(out/f'call-{arm}.json', records[-1])
    comparisons = classify(out)
    write(out/'comparisons.json', comparisons)
    return records, comparisons


def worker():
    from pyscf import lib
    from pyscf.scf import jk, _vhf
    out = BASE/'run-v1'; token = gate()
    require(read(out/'launch-gate.json') == token, 'Launch gate changed')
    write(out/'worker-started.json', {'pid': os.getpid(), 'maximum_prefix_attempts': 2, 'solves': 0})
    start = time.monotonic()
    def stage(name, **fields):
        with (out/'stages.jsonl').open('a') as stream:
            stream.write(json.dumps({'stage': name, 'elapsed_seconds': time.monotonic()-start, **fields})+'\n')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    with replay.single_blas_fresh_child(lambda label, row: write(out/('threads-'+label+'.json'), row)) as threads:
        old_write, old_capture = e.write, e.OrdinaryCapture
        e.write, e.OrdinaryCapture = write, RHSCapture
        try:
            threads('before_setup')
            mf, capture, guard, storage, flush, close = e.setup(out, stage, runtime)
            try:
                threads('after_setup')
                records, comparisons = run_calls(mf, out, capture, r.first.saved_density, guard, storage, flush,
                    threads, stage, read(BASE/'preparation.json')['positive_density_sha256'], lib, jk,
                    _vhf._fpointer('CVHFnr3c2e_vj_pass1_prescreen').value)
            finally: close()
        finally: e.write, e.OrdinaryCapture = old_write, old_capture
    require(gate() == token, 'Final gate changed')
    write(out/'result.json', {'status': STATUS, 'prefix_attempts': 2, 'pass1_calls': 2, 'sentinel_count': 2,
        'complete_J_calls': 0, 'solves': 0, 'factor_count': 1, 'SCFs': 0, 'PCM_builds': 0,
        'comparisons': comparisons, 'output_hashes': {k: v for row in records for k, v in row['hashes'].items()},
        'physical_admission': False, 'parent_SCF_readiness': False, 'held_out_validation': False})


def launch():
    token = gate(); out = BASE/'run-v1'; out.mkdir(exist_ok=False)
    write(out/'launch-gate.json', token)
    supervisor = r.load('serial_rhs_supervisor', LAB/'parent-pilot/pilot.py')
    supervisor.THREADS = {**supervisor.THREADS, 'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE'}
    python = read(r.first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt = supervisor.monitored_run([python, '-B', str(BASE/'run.py'), '--worker'], out, WALL, RSS)
    result = read(out/'result.json') if (out/'result.json').exists() else {}
    hashes = {p.name: sha(p) for p in out.iterdir() if p.is_file()}
    same, error = False, None
    try: same = gate() == token
    except Exception: error = traceback.format_exc()
    complete = r.first.accepted(receipt) and same and result.get('status') == STATUS and result.get('output_hashes') == {
        'b_'+arm: hashes.get('b_'+arm+'.npy') for arm in ARMS}
    write(out/'launch-result.json', {'completed': complete, 'receipt': receipt, 'artifact_hashes': hashes,
        'gate_unchanged': same, 'gate_error': error, 'physical_admission': False, 'parent_SCF_readiness': False})
    return 0 if complete else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']: prepare()
    elif sys.argv[1:] == ['--gate-check']: print(json.dumps(gate()))
    elif sys.argv[1:] == ['--launch']: sys.exit(launch())
    elif sys.argv[1:] == ['--worker']:
        try: worker()
        except BaseException:
            write(BASE/'run-v1/failure.json', {'exception': traceback.format_exc(), 'physical_admission': False})
            raise
    else: raise SystemExit('Use --prepare, --gate-check or --launch')
