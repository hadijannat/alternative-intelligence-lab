import importlib.util
import io
from pathlib import Path
import tempfile
import types
import unittest
from contextlib import contextmanager
from unittest.mock import patch
import numpy as np

spec = importlib.util.spec_from_file_location('serial_rhs', Path(__file__).with_name('run.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Tests(unittest.TestCase):
    def fixture(self):
        lib = types.SimpleNamespace(n=4)
        lib.num_threads = lambda: lib.n
        @contextmanager
        def with_threads(n):
            old = lib.n
            lib.n = n
            try: yield
            finally: lib.n = old
        lib.with_omp_threads = with_threads
        opt = types.SimpleNamespace(fakemol=object(), prescreen=42)
        mf = types.SimpleNamespace(mol=types.SimpleNamespace(nbas=2), _rij_calls=0,
            _rij_df=types.SimpleNamespace(_vjopt=opt, auxmol=types.SimpleNamespace(nbas=3)),
            with_solvent=types.SimpleNamespace())
        kwargs = {'aosym': 's2ij', 'hermi': 0, 'shls_slice': (0,2,0,2,2,5,5,6), 'vhfopt': opt}
        capture = m.RHSCapture(lambda *a: self.fail('Solver executed'), lambda: {'fixed': True}, 3)
        capture.arm = 'A'
        def native(*a, **k):
            self.assertEqual(lib.n, 1)
            return np.ones((3,1))
        jk = types.SimpleNamespace(get_jk=native)
        return lib, mf, kwargs, capture, jk

    def test_serial_restore_and_pass2_rejection(self):
        lib, mf, kwargs, capture, jk = self.fixture()
        native = jk.get_jk
        with m.serial_pass1(mf, capture, lambda *a, **k: None, lib, jk, 42) as count:
            with self.assertRaisesRegex(ValueError, 'Unexpected contraction'):
                jk.get_jk(mf._rij_df._vjopt.fakemol, None, ['ijkl,lk->ij'], 'int3c2e', **kwargs)
            result = jk.get_jk(mf._rij_df._vjopt.fakemol, None, ['ijkl,ji->kl'], 'int3c2e', **kwargs)
            self.assertEqual(lib.n, 4)
            with self.assertRaisesRegex(ValueError, 'Unexpected contraction'):
                jk.get_jk(mf._rij_df._vjopt.fakemol, None, ['ijkl,ji->kl'], 'int3c2e', **kwargs)
            self.assertEqual(count, [1])
        self.assertIs(jk.get_jk, native)
        np.testing.assert_array_equal(result, np.ones((3,1)))

    def test_native_error_restores_interception_and_threads(self):
        lib, mf, kwargs, capture, jk = self.fixture()
        def fail(*a, **k): raise RuntimeError('native failure')
        jk.get_jk = fail
        with self.assertRaisesRegex(RuntimeError, 'native failure'):
            with m.serial_pass1(mf, capture, lambda *a, **k: None, lib, jk, 42):
                jk.get_jk(mf._rij_df._vjopt.fakemol, None, ['ijkl,ji->kl'], 'int3c2e', **kwargs)
        self.assertEqual(lib.n, 4)
        self.assertIs(jk.get_jk, fail)

    def test_capture_stops_without_solve_and_rejects_duplicates(self):
        _, _, _, capture, _ = self.fixture()
        rhs = np.ones((3,1))
        with self.assertRaises(m.PrefixStop) as caught: capture(None, rhs)
        self.assertIs(caught.exception, capture.stop)
        rhs[0] = 9
        self.assertEqual(capture.data['A'][0,0], 1)
        with self.assertRaisesRegex(ValueError, 'duplicate'): capture(None, rhs)
        capture.arm = 'B'
        with self.assertRaisesRegex(ValueError, 'layout'): capture(None, np.ones(3))
        self.assertEqual(capture.sentinel_count, 1)

    def exercise(self, out, mode='ok'):
        lib, mf, kwargs, capture, jk = self.fixture()
        def get_j(dm):
            if mode == 'other_sentinel': raise m.PrefixStop()
            if mode == 'real_error': raise RuntimeError('real failure')
            rhs = jk.get_jk(mf._rij_df._vjopt.fakemol, dm, ['ijkl,ji->kl'], 'int3c2e', **kwargs)
            capture(None, rhs)
            self.fail('Reached solve/pass2')
        mf.get_j = get_j
        def classify(directory):
            self.assertEqual(sorted(p.name for p in directory.glob('*.npy')), ['b_A.npy','b_B.npy'])
            self.assertEqual(capture.sentinel_count, 2)
            return {'serial_RHS_repeat_pass': True}
        def storage(number):
            self.assertEqual(number, 0)
            return {'mock': True}
        with patch.object(m, 'BASE', out), patch.object(m, 'classify', side_effect=classify):
            result = m.run_calls(mf, out, capture, lambda: (np.eye(2), {}), lambda: None, storage,
                lambda: None, lambda label: None, lambda *a, **k: None, m.r.array_digest(np.eye(2)), lib, jk, 42)
        self.assertEqual(mf._rij_calls, 0)
        return result

    def test_two_prefixes_save_before_classification(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.exercise(Path(directory))
            self.assertEqual(len(result[0]), 2)
            self.assertEqual(result[0][-1]['pass1_calls'], 2)

    def test_other_sentinel_and_real_error_escape(self):
        for mode, error in [('other_sentinel', m.PrefixStop), ('real_error', RuntimeError)]:
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(error): self.exercise(Path(directory), mode)
                self.assertFalse(list(Path(directory).glob('*.npy')))

    def test_bitwise_classifier_distinguishes_signed_zero_and_tiny_delta(self):
        a = np.zeros((3,1)); b = a.copy(); b[0] = -0.0
        self.assertFalse(m.difference(a,b)['bitwise_equal'])
        self.assertTrue(m.difference(a,b)['exact_equal'])
        b[0] = 1e-14
        self.assertEqual(m.difference(a,b)['unequal_entries'], 1)
        self.assertTrue(m.difference(a,a)['bitwise_equal'])
        with self.assertRaises(ValueError): m.difference(a, np.full_like(a,np.nan))

    def test_gate_requires_binding_and_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); pins = {'qualification': {'mock': 'pin'}}
            with patch.object(m, 'BASE', out), patch.object(m, 'manifest', return_value=pins):
                m.write(out/'preparation.json', {'status': 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW', 'pins': pins})
                with self.assertRaises(FileNotFoundError): m.gate()
                m.write(out/'independent-root-review.json', {'status': m.APPROVAL, 'independent_root_review': True,
                    'reviewer': 'mock', 'preparation_sha256': m.sha(out/'preparation.json'), 'qualification_artifacts': pins['qualification']})
                self.assertIn('review_sha256', m.gate())
                with patch.object(m, 'manifest', return_value={}):
                    with self.assertRaisesRegex(ValueError, 'Preparation changed'): m.gate()


if __name__ == '__main__':
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    print(stream.getvalue())
    if args := __import__('sys').argv[1:]:
        if args != ['--record']: raise SystemExit('Use --record or no arguments')
        m.write(m.BASE/'qualification.json', {'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
            'failures': len(result.failures), 'errors': len(result.errors), 'output': stream.getvalue(),
            'native_parent_calls': 0, 'mock_only': True})
    raise SystemExit(0 if result.wasSuccessful() else 1)
