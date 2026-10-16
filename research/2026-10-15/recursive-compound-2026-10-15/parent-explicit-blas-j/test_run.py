import importlib.util
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

spec = importlib.util.spec_from_file_location('explicit_j', Path(__file__).with_name('run.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Tests(unittest.TestCase):
    def test_both_ordinary_and_no_C(self):
        answers = []
        def solve(factor, rhs, **kwargs):
            answers.append(rhs*2)
            return answers[-1]
        hook = m.OrdinaryCapture(solve, lambda: {'fixed': True}, 3)
        for arm in m.ARMS:
            hook.arm = arm
            answer = hook(None, np.ones((3, 1))*ord(arm))
            self.assertIs(answer, answers[-1])
            self.assertFalse(np.shares_memory(answer, hook.data[arm]['rho_ordinary']))
        hook.arm = 'C'
        with self.assertRaisesRegex(ValueError, 'Only ordinary'): hook(None, np.ones((3, 1)))
        self.assertEqual(len(answers), 2)

    def synthetic(self, out, bad_storage=False):
        mf = types.SimpleNamespace(_rij_calls=0, with_solvent=types.SimpleNamespace())
        hook = m.OrdinaryCapture(lambda factor, rhs, **kwargs: rhs*2, lambda: {'fixed': True}, 3)
        def native(dm):
            rho = hook(None, np.ones((3, 1))*(mf._rij_calls+1))
            mf._rij_calls += 1
            return np.eye(2)*rho[0, 0]
        mf.get_j = native
        def classify(out):
            self.assertEqual(mf._rij_calls, 2)
            self.assertEqual(len(list(out.glob('*.npy'))), 6)
            for arm in m.ARMS:
                for name, digest in m.read(out/f'closed-output-hashes-{arm}.json').items():
                    self.assertEqual(m.sha(out/(name+'.npy')), digest)
            return {'repeat_and_symmetry_pass': False}
        def storage(number):
            if bad_storage: raise ValueError('bad storage')
            return {'number': number}
        with patch.object(m, 'BASE', out), patch.object(m, 'classify', side_effect=classify):
            result = m.run_calls(mf, out, hook, lambda: (np.eye(2), {}), lambda: None,
                storage, lambda: None, lambda label: None, m.r.array_digest(np.eye(2)))
        return mf, hook, result

    def test_two_calls_save_before_nonpass(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); mf, hook, result = self.synthetic(out)
            self.assertEqual(mf._rij_calls, 2)
            self.assertFalse(result[1]['repeat_and_symmetry_pass'])
            self.assertFalse(np.array_equal(np.load(out/'J_A.npy'), np.load(out/'J_B.npy')))
            with self.assertRaisesRegex(ValueError, 'Call count'):
                m.run_calls(mf, out, hook, lambda: (np.eye(2), {}), lambda: None, lambda n: {},
                            lambda: None, lambda label: None, m.r.array_digest(np.eye(2)))
            with self.assertRaises(FileExistsError): m.s.save_array(out, 'J_A', np.eye(2))

    def test_failure_retains_first_arrays(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with self.assertRaisesRegex(ValueError, 'bad storage'): self.synthetic(out, True)
            self.assertEqual(len(list(out.glob('*.npy'))), 3)
            self.assertFalse((out/'comparisons.json').exists())

    def test_gate_rejects_missing_approval_and_changed_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); pins = {'qualification': {'test': 'value'}}
            with patch.object(m, 'BASE', out), patch.object(m, 'manifest', return_value=pins):
                m.write(out/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW', 'pins': pins})
                with self.assertRaises(FileNotFoundError): m.gate()
                m.write(out/'independent-root-review.json', {'status': m.APPROVAL, 'independent_root_review': True,
                    'reviewer': 'mock', 'preparation_sha256': m.sha(out/'preparation.json'), 'qualification_artifacts': pins['qualification']})
                self.assertIn('review_sha256', m.gate())
                with patch.object(m, 'manifest', return_value={'changed': True}):
                    with self.assertRaisesRegex(ValueError, 'Preparation changed'): m.gate()

    def test_one_factor_metric_before_destructive_call(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); factors = []
            def factor(matrix, **kwargs):
                self.assertEqual(m.read(out/'metric-before-factor.json')['metric_array_sha256'], m.r.array_digest(matrix))
                factors.append(matrix); matrix[0, 0] = 9
                return matrix, True
            memory = types.SimpleNamespace(factor_inplace=factor)
            def setup(out, stage, runtime):
                loaded = m.r.load('fake', 'fake')
                loaded.factor_inplace(np.eye(2))
                with self.assertRaisesRegex(ValueError, 'Second factorization'): loaded.factor_inplace(np.eye(2))
                mf = types.SimpleNamespace(mol=types.SimpleNamespace(stdout=io.StringIO()))
                return mf, None, None, None, lambda: None
            real_read = m.read
            def read(path):
                return {'metric_array_sha256': 'different'} if Path(path).name == 'matrix-factor.json' else real_read(path)
            with patch.object(m, 'BASE', out), patch.object(m, 'read', side_effect=read), patch.object(m.r, 'load', return_value=memory), patch.object(m.s, 'setup', side_effect=setup):
                result = m.setup(out, lambda *a, **k: None, {})
                result[-1]()
            self.assertEqual(len(factors), 1)
            self.assertFalse(real_read(out/'metric-before-factor.json')['matches_saved_metric'])

    def test_launcher_exact_limits_and_exclusive_output(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); calls = []
            def monitored(argv, directory, wall, rss):
                calls.append((argv, wall, rss)); return {'mock': True}
            supervisor = types.SimpleNamespace(THREADS={}, monitored_run=monitored)
            original_read = m.read
            def read(path):
                if Path(path) == m.r.first.QUAL/'preparation.json': return {'pins': {'runtime': {'python': '/mock/python'}}}
                return original_read(path)
            with patch.object(m, 'BASE', out), patch.object(m, 'gate', return_value={'mock': True}), patch.object(m.r, 'load', return_value=supervisor), patch.object(m, 'read', side_effect=read), patch.object(m.r.first, 'accepted', return_value=False):
                self.assertEqual(m.launch(), 1)
                with self.assertRaises(FileExistsError): m.launch()
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1:], (600, 10*2**30))


if __name__ == '__main__':
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    print(stream.getvalue())
    if sys_args := __import__('sys').argv[1:]:
        if sys_args != ['--record']: raise SystemExit('Use --record or no arguments')
        m.write(m.BASE/'qualification.json', {'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
            'failures': len(result.failures), 'errors': len(result.errors), 'output': stream.getvalue(),
            'native_parent_calls': 0, 'mock_only': True})
    raise SystemExit(0 if result.wasSuccessful() else 1)
