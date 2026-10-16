import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
from scipy.linalg import cho_factor, cho_solve

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('metric_diagnostic', BASE/'run.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


def qualification():
    records = []
    for diagonal in ([1., 2., 4.], [1., 1e-8, 1e-12]):
        matrix = np.diag(diagonal)
        factor = cho_factor(np.array(matrix, order='F'), lower=True)
        rhs = np.array([[1.], [2.], [3.]])
        answer = cho_solve(factor, rhs)
        errors, residual = d.norms_and_errors(matrix, rhs, answer, rows=2)
        estimate = d.condition_estimate(factor, max(diagonal))
        exact = max(diagonal)/min(diagonal)
        assert abs(estimate['one_norm_condition_estimate']/exact-1) < 1e-12
        assert errors['normwise_backward_error'] < 1e-15
        assert np.allclose(residual, rhs-matrix@answer, atol=0, rtol=0)
        assert np.array_equal(answer, cho_solve(factor, rhs.copy()))
        records.append({'diagonal': diagonal, 'analytic_condition': exact, 'estimate': estimate, 'errors': errors})
    return records


class Tests(unittest.TestCase):
    def test_known_conditions(self):
        self.assertEqual(len(qualification()), 2)

    def test_bad_answer_detected(self):
        matrix = np.array([[2., 1.], [1., 3.]])
        rhs = np.array([[1.], [2.]])
        answer = np.zeros_like(rhs)
        errors, residual = d.norms_and_errors(matrix, rhs, answer, 1)
        self.assertEqual(errors['normwise_backward_error'], 1.)
        np.testing.assert_array_equal(residual, rhs)

    def test_zero_system_rhs(self):
        errors, _ = d.norms_and_errors(np.eye(2), np.zeros((2, 1)), np.zeros((2, 1)))
        self.assertEqual(errors['componentwise_backward_error'], 0.)

    def test_nonfinite_metric_rejected(self):
        with self.assertRaises((RuntimeError, ValueError, AssertionError)):
            d.norms_and_errors(np.array([[np.nan]]), np.ones((1, 1)), np.ones((1, 1)))

    def test_gate_rejects_missing_approval(self):
        with patch.object(d, 'manifest', return_value={}), patch.object(d, 'read', side_effect=[{'pins': {}}, {}]):
            with self.assertRaises((RuntimeError, ValueError, AssertionError)):
                d.gate()

    def test_gate_rejects_changed_inputs(self):
        with patch.object(d, 'manifest', return_value={'changed': 1}), patch.object(d, 'read', return_value={'pins': {}}):
            with self.assertRaises((RuntimeError, ValueError, AssertionError)):
                d.gate()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    d.write(BASE/'qualification.json', {'passed': result.wasSuccessful(), 'tests_run': result.testsRun, 'tests': [str(test) for test in unittest.defaultTestLoader.loadTestsFromTestCase(Tests)], 'cases': qualification(), 'parent_native_execution': False, 'J_calls': 0, 'SCFs': 0})
    raise SystemExit(0 if result.wasSuccessful() else 1)
