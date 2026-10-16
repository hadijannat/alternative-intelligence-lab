import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
spec = importlib.util.spec_from_file_location('saved_metric_control', LAB/'parent-saved-metric-solve/run.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)
s, r = replay.s, replay.r
read, require, sha = r.read, r.require, replay.sha
ARMS = ('A', 'B')
WALL, RSS = 600, 10*2**30
STATUS = 'COMPLETED_EXPLICIT_BLAS_J_DIAGNOSTIC_ONLY'
APPROVAL = 'APPROVED_ONE_EXPLICIT_BLAS_J_DIAGNOSTIC'


def write(path, value):
    path = Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()), 'Output outside diagnostic')
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def manifest():
    pins = replay.manifest()
    paths = [BASE/n for n in ('run.py', 'test_run.py', 'PROTOCOL.md', 'qualification.json')]
    paths += [replay.BASE/n for n in ('preparation.json', 'independent-root-review.json')]
    paths += sorted(p for p in (replay.BASE/'run-v1').iterdir() if p.is_file())
    paths += [LAB.parent/'.omo/evidence/saved-metric-replay-result-review.md']
    pins['explicit_blas_j'] = {str(p): sha(p) for p in paths}
    return pins


def prepare():
    require(read(BASE/'qualification.json')['passed'] is True, 'Tiny qualification failed')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    require(Path(sys.executable).resolve() == Path(runtime['python']).resolve(), 'Wrong interpreter')
    require(r.qualification.runtime_pins() == runtime, 'Runtime changed')
    require(read(replay.BASE/'run-v1/launch-result.json')['completed'] is True, 'Replay incomplete')
    density, summary = r.first.saved_density()
    digest = r.array_digest(density)
    write(BASE/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW',
        'pins': manifest(), 'positive_density_sha256': digest, 'density': summary,
        'maximum_children': 1, 'maximum_J_calls': 2, 'maximum_factorizations': 1,
        'wall_cap_seconds': WALL, 'sampled_RSS_guard_bytes': RSS,
        'sequence': ['ordinary_A_P0', 'ordinary_B_P0'], 'absolute_tolerance': 1e-10,
        'relative_tolerance': 0, 'SCFs': 0, 'PCM_builds': 0, 'operators_executed': 0,
        'physical_admission': False, 'parent_SCF_readiness': False})


def gate():
    prep = read(BASE/'preparation.json')
    require(prep['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW' and prep['pins'] == manifest(), 'Preparation changed')
    approval = read(BASE/'independent-root-review.json')
    require(approval.get('status') == APPROVAL and approval.get('independent_root_review') is True
            and bool(approval.get('reviewer')), 'Independent root review required')
    require(approval.get('preparation_sha256') == sha(BASE/'preparation.json')
            and approval.get('qualification_artifacts') == prep['pins']['qualification'], 'Approval binding changed')
    return {'preparation_sha256': sha(BASE/'preparation.json'), 'review_sha256': sha(BASE/'independent-root-review.json')}


class OrdinaryCapture(s.SolveCapture):
    def __call__(self, factor, rhs, **kwargs):
        require(self.arm in ARMS, 'Only ordinary A and B allowed')
        return super().__call__(factor, rhs, **kwargs)


def setup(out, stage, runtime):
    original_load, original_capture, original_save = r.load, s.SolveCapture, r.save
    factor_records = []
    def load(name, path):
        memory = original_load(name, path)
        original_factor = memory.factor_inplace
        def factor(matrix, *args, **kwargs):
            require(not factor_records, 'Second factorization forbidden')
            row = {'metric_array_sha256': r.array_digest(matrix)}
            prior = read(replay.BASE/'run-v1/matrix-factor.json')['metric_array_sha256']
            row.update({'saved_metric_array_sha256': prior, 'matches_saved_metric': row['metric_array_sha256'] == prior,
                        'causal_comparison_established': False})
            factor_records.append(row)
            write(out/'metric-before-factor.json', row)
            return original_factor(matrix, *args, **kwargs)
        memory.factor_inplace = factor
        return memory
    r.load, s.SolveCapture = load, OrdinaryCapture
    try:
        result = s.setup(out, stage, runtime)
    finally:
        r.load, s.SolveCapture = original_load, original_capture
    mf, capture, guard, storage, flush = result
    def close():
        r.save = original_save
        mf.mol.stdout.close()
    return mf, capture, guard, storage, flush, close


def classify(out):
    import numpy as np
    matrices = {arm: np.load(out/f'J_{arm}.npy', mmap_mode='r', allow_pickle=False) for arm in ARMS}
    previous = np.load(r.EXTERNAL, mmap_mode='r', allow_pickle=False)
    try:
        repeat = r.compare(matrices['B'], matrices['A'], 1)
        symmetry = {arm: r.signed.matrix_checks(matrix) for arm, matrix in matrices.items()}
        historical = {arm: r.compare(matrix, previous, 1) for arm, matrix in matrices.items()}
        vectors = {field: s.vector_difference(np.load(out/f'{field}_B.npy'), np.load(out/f'{field}_A.npy'))
                   for field in ('b', 'rho_ordinary')}
        return {'repeat': repeat, 'symmetry': symmetry, 'historical_reference': historical,
                'vectors': vectors, 'repeat_and_symmetry_pass': repeat['pass'] and all(v['symmetric'] for v in symmetry.values()),
                'historical_reference_pass': all(v['pass'] for v in historical.values()),
                'historical_reference_is_independent_oracle': False, 'physical_admission': False}
    finally:
        for array in [*matrices.values(), previous]: array._mmap.close()


def run_calls(mf, out, capture, loader, guard, storage, flush, threads, expected):
    records = []
    for number, arm in enumerate(ARMS, 1):
        guard(); r.signed.restrict(mf)
        require(mf._rij_calls == number-1 and len(capture.data) == number-1, 'Call count differs')
        density, source = loader()
        require(r.array_digest(density) == expected, 'P0 changed')
        capture.arm = arm
        threads('before_J_'+arm)
        matrix = mf.get_j(dm=density)
        hashes = {'J_'+arm: s.save_array(out, 'J_'+arm, matrix)}
        require(arm in capture.data, 'Missing solve capture')
        for field, array in capture.data[arm].items(): hashes[field+'_'+arm] = s.save_array(out, field+'_'+arm, array)
        write(out/f'closed-output-hashes-{arm}.json', hashes)
        flush(); threads('after_J_'+arm)
        require(mf._rij_calls == number and len(capture.data) == number, 'Return count differs')
        require(r.array_digest(density) == expected, 'Native call mutated P0')
        require(capture.state() == capture.baseline, 'Optimizer changed')
        require(capture.returned_ids[arm]['ordinary_returned_unchanged'], 'Substituted rho forbidden')
        state = storage(number); guard()
        records.append({'arm': arm, 'hashes': hashes, 'storage': state, 'source': source, 'capture': capture.returned_ids[arm]})
        write(out/f'call-{arm}.json', records[-1])
        del density, matrix
    require(mf._rij_calls == 2 and tuple(capture.data) == ARMS, 'Exactly two ordinary calls required')
    result = classify(out)
    write(out/'comparisons.json', result)
    return records, result


def worker():
    out = BASE/'run-v1'; token = gate()
    require(read(out/'launch-gate.json') == token, 'Launch gate changed')
    write(out/'worker-started.json', {'pid': os.getpid(), 'maximum_J_calls': 2, 'SCFs': 0, 'PCM_builds': 0})
    start = time.monotonic()
    def stage(name, **fields):
        with (out/'stages.jsonl').open('a') as stream: stream.write(json.dumps({'stage': name, 'elapsed_seconds': time.monotonic()-start, **fields})+'\n')
    runtime = read(r.first.QUAL/'preparation.json')['pins']['runtime']
    with replay.single_blas_fresh_child(lambda label, row: write(out/('threads-'+label+'.json'), row)) as threads:
        threads('before_setup')
        mf, capture, guard, storage, flush, close = setup(out, stage, runtime)
        try:
            threads('after_setup')
            records, comparisons = run_calls(mf, out, capture, r.first.saved_density, guard, storage, flush,
                                             threads, read(BASE/'preparation.json')['positive_density_sha256'])
        finally: close()
    require(gate() == token, 'Final gate changed')
    write(out/'result.json', {'status': STATUS, 'J_calls': 2, 'factor_count': 1, 'SCFs': 0, 'PCM_builds': 0,
        'comparisons': comparisons, 'output_hashes': {k: v for row in records for k, v in row['hashes'].items()},
        'physical_admission': False, 'parent_SCF_readiness': False, 'held_out_validation': False})


def launch():
    token = gate(); out = BASE/'run-v1'; out.mkdir(exist_ok=False)
    write(out/'launch-gate.json', token)
    supervisor = r.load('explicit_blas_j_supervisor', LAB/'parent-pilot/pilot.py')
    supervisor.THREADS = {**supervisor.THREADS, 'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE'}
    python = read(r.first.QUAL/'preparation.json')['pins']['runtime']['python']
    receipt = supervisor.monitored_run([python, '-B', str(BASE/'run.py'), '--worker'], out, WALL, RSS)
    result = read(out/'result.json') if (out/'result.json').exists() else {}
    hashes = {p.name: sha(p) for p in out.iterdir() if p.is_file()}
    same = False
    try: same = gate() == token
    except Exception: pass
    complete = r.first.accepted(receipt) and same and result.get('status') == STATUS and result.get('output_hashes') == {
        name: hashes.get(name+'.npy') for arm in ARMS for name in ('J_'+arm, 'b_'+arm, 'rho_ordinary_'+arm)}
    write(out/'launch-result.json', {'completed': complete, 'receipt': receipt, 'artifact_hashes': hashes,
        'gate_unchanged': same, 'physical_admission': False, 'parent_SCF_readiness': False})
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
