import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('saved_metric_replay', BASE/'run.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


def thread_worker():
    out = BASE/'qualification-thread'
    fixture = out/'fixture'
    fixture.mkdir()
    lower = np.array([[2., 0, 0, 0], [1, 2, 0, 0], [-1, .5, 2, 0], [.5, -.5, 1, 2]])
    matrix = np.array(lower @ lower.T, order='F')
    expected = np.array([[1.], [-2.], [3.], [-.5]])
    d.save_array(fixture, 'metric', matrix)
    for arm, shift in (('A', 0), ('B', 1e-8), ('C', -1e-8)):
        d.save_array(fixture, 'b_'+arm, matrix @ (expected+shift))
        d.save_array(fixture, 'rho_ordinary_'+arm, expected+shift)
    d.write(fixture/'factor-states.json', [{'content_sha256': 'tiny-fixture-no-prior-native-factor'}])
    memory = d.r.load('frozen_tiny_memory', d.LAB/'cpcm-rij-memory/memory.py')
    try:
        with d.single_blas_fresh_child(lambda label, row: d.write(out/('threads-'+label+'.json'), row)) as state:
            mapped = d.checked_matrix(fixture/'metric.npy', n=4)
            result = d.solve_sequence(mapped, memory, out, state, source=fixture, matrix_file_sha=d.sha(fixture/'metric.npy'))
            mapped._mmap.close()
            assert result['comparisons']['A2']['exact_equal']
            actual = np.load(out/'rho_A1.npy')
            assert np.max(np.abs(actual-expected)) < 1e-13
            condition = result['condition']['one_norm_condition_estimate']
            assert 1 <= condition <= np.linalg.cond(matrix, 1)*(1+1e-12)
            raise RuntimeError('intentional restoration test')
    except RuntimeError as exc:
        assert str(exc) == 'intentional restoration test'
    d.write(out/'tiny-result.json', {'passed': True, 'result': result,
        'max_answer_error': float(np.max(np.abs(actual-expected))), 'intentional_exception_observed': True,
        'parent_native_execution': False})


class Tests(unittest.TestCase):
    def test_wrong_answer(self):
        errors, residual = d.v1.norms_and_errors(np.array([[2., 1.], [1., 3.]]), np.ones((2, 1)), np.zeros((2, 1)))
        self.assertEqual(errors['normwise_backward_error'], 1)
        np.testing.assert_array_equal(residual, np.ones((2, 1)))

    def test_nonfinite(self):
        with self.assertRaises((ValueError, RuntimeError, AssertionError)):
            d.v1.norms_and_errors(np.array([[np.nan]]), np.ones((1, 1)), np.ones((1, 1)))

    def test_zero_rhs(self):
        errors, _ = d.v1.norms_and_errors(np.eye(2), np.zeros((2, 1)), np.zeros((2, 1)))
        self.assertEqual(errors['componentwise_backward_error'], 0)

    def test_missing_approval(self):
        with patch.object(d, 'manifest', return_value={}), patch.object(d, 'read', side_effect=[{'pins': {}}, {}]):
            with self.assertRaises((ValueError, RuntimeError, AssertionError)):
                d.gate()

    def test_changed_pins(self):
        with patch.object(d, 'manifest', return_value={'changed': 1}), patch.object(d, 'read', return_value={'pins': {}}):
            with self.assertRaises((ValueError, RuntimeError, AssertionError)):
                d.gate()

    def test_wrong_approval_binding(self):
        review = {'status': d.APPROVAL, 'independent_root_review': True, 'reviewer': 'test', 'preparation_sha256': 'wrong'}
        with patch.object(d, 'manifest', return_value={'qualification': {}}), patch.object(d, 'sha', return_value='correct'), patch.object(d, 'read', side_effect=[{'pins': {'qualification': {}}}, review]):
            with self.assertRaises((ValueError, RuntimeError, AssertionError)):
                d.gate()

    def test_exclusive_output_and_stream_hash(self):
        with tempfile.TemporaryDirectory(dir=BASE) as temp:
            path = Path(temp)/'a.json'
            d.write(path, {'value': 1})
            with self.assertRaises(FileExistsError):
                d.write(path, {'value': 2})
            with patch.object(Path, 'read_bytes', side_effect=AssertionError('Buffered hash forbidden')):
                self.assertEqual(len(d.sha(path)), 64)

    def test_bad_layout(self):
        with tempfile.TemporaryDirectory(dir=BASE) as temp:
            path = Path(temp)/'matrix.npy'
            np.save(path, np.eye(2, dtype=np.float32), allow_pickle=False)
            with self.assertRaises((ValueError, RuntimeError, AssertionError)):
                d.checked_matrix(path, 2)


if __name__ == '__main__':
    if sys.argv[1:] == ['--thread-worker']:
        thread_worker()
    elif not sys.argv[1:]:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)
        out = BASE/'qualification-thread'
        out.mkdir(exist_ok=False)
        supervisor = d.r.load('tiny_supervisor', d.LAB/'parent-pilot/pilot.py')
        supervisor.THREADS = {**supervisor.THREADS, 'OMP_NUM_THREADS': '4', 'OMP_DYNAMIC': 'FALSE'}
        receipt = supervisor.monitored_run([sys.executable, '-B', str(Path(__file__).resolve()), '--thread-worker'], out, 30, 2**30)
        passed = d.r.first.accepted(receipt) and (out/'tiny-result.json').exists() and d.read(out/'tiny-result.json')['passed'] is True
        d.write(BASE/'qualification.json', {'passed': passed, 'tests_run': result.testsRun, 'tiny_child': receipt,
            'test_names': [str(t) for t in unittest.defaultTestLoader.loadTestsFromTestCase(Tests)],
            'tiny_artifact_hashes': {str(p.relative_to(BASE)): d.sha(p) for p in out.rglob('*') if p.is_file()},
            'parent_native_execution': False, 'J_calls': 0, 'SCFs': 0})
        raise SystemExit(0 if passed else 1)
    else:
        raise SystemExit('usage: test_run.py [--thread-worker]')
