import hashlib
import json
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
RUN = BASE.parent / 'run-v1'
CRASH = Path.home() / 'Library/Logs/DiagnosticReports/python3.12-2026-10-16-065749.ips'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def inspect(matrix, rows=32):
    assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
    finite, symmetry, norm = True, 0.0, 0.0
    for start in range(0, len(matrix), rows):
        block = matrix[start:start + rows]
        finite = finite and bool(np.isfinite(block).all())
        if finite:
            symmetry = max(symmetry, float(np.max(np.abs(block - matrix[:, start:start + rows].T))))
            norm = max(norm, float(np.max(np.sum(np.abs(block), axis=1))))
    diagonal = np.diag(matrix)
    return {'all_finite': finite, 'symmetry_max': symmetry if finite else None,
            'infinity_norm': norm if finite else None,
            'diagonal_min': float(diagonal.min()) if finite else None,
            'diagonal_max': float(diagonal.max()) if finite else None,
            'positive_definiteness_established': False}


def main():
    assert inspect(np.array([[2., 1.], [1., 3.]]), 1)['infinity_norm'] == 4.
    assert inspect(np.array([[2., 0.], [1., 3.]]), 1)['symmetry_max'] == 1.
    assert inspect(np.array([[np.nan]]))['all_finite'] is False
    launch = json.loads((RUN / 'launch-result.json').read_text())
    assert launch['completed'] is False and launch['receipt']['pid'] == 73957
    hashes = {name: digest(RUN / name) for name in launch['artifact_hashes']}
    assert hashes == launch['artifact_hashes']
    metric = np.load(RUN / 'original_metric.npy', mmap_mode='r', allow_pickle=False)
    assert metric.shape == (19612, 19612) and metric.dtype == np.float64
    summary = inspect(metric)
    summary.update(shape=list(metric.shape), dtype=str(metric.dtype),
                   fortran_contiguous=bool(metric.flags.f_contiguous),
                   file_bytes=(RUN / 'original_metric.npy').stat().st_size)
    metric._mmap.close()
    raw = CRASH.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '12cb3ad364faf3eb656ebed8de97c4fc73374b13bdc52d57a3b04e96000a2647'
    crash = json.loads(raw.split(b'\n', 1)[1])
    assert crash['pid'] == launch['receipt']['pid']
    fault = crash['threads'][crash['faultingThread']]
    frames = [{k: frame.get(k) for k in ('symbol', 'symbolLocation', 'imageIndex')}
              for frame in fault['frames']]
    (BASE / 'raw').mkdir(exist_ok=True)
    with (BASE / 'raw' / CRASH.name).open('xb') as stream:
        stream.write(raw)
    result = {'status': 'POSTMORTEM_OBSERVATIONS_ONLY', 'tiny_checks_passed': 3,
              'terminal_artifacts_verified': hashes, 'saved_metric': summary,
              'crash_original_sha256': hashlib.sha256(raw).hexdigest(),
              'crash_preserved_path': 'raw/' + CRASH.name,
              'exception': crash['exception'], 'termination': crash['termination'],
              'faulting_thread_frames': frames,
              'parent_metric_recomputed': False, 'factorizations': 0, 'solves': 0,
              'J_calls': 0, 'SCFs': 0, 'root_cause_established': False,
              'physical_admission': False}
    with (BASE / 'result.json').open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'saved_metric': summary, 'verified_artifacts': len(hashes),
                      'exception': crash['exception'], 'tiny_checks_passed': 3}))


if __name__ == '__main__':
    main()
