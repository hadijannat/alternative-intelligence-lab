import json
from pathlib import Path
from types import SimpleNamespace
import unittest
import tempfile
from unittest.mock import patch

import numpy as np
import response as r
import run


class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.s = object.__new__(r.memory.MemoryPCM)
        self.s.mol = SimpleNamespace(nao=2)
        self.s.method = 'C-PCM'
        self.s.surface_discretization_method = 'SWIG'
        self.s.frozen = self.s.equilibrium_solvation = False
        self.s.state_id = 0
        self.s.eps = 78.4
        self.matrix = np.array([[2., .3], [.3, 1.]], order='F')
        self.s._intermediates = {'factor': r.memory.factor_inplace(self.matrix.copy(order='F')),
                                 'q': np.array([7., 9.])}
        self.g = np.array([[[1., .2], [.2, 2.]], [[-.4, .3], [.3, .5]]])
        self.calls = []
        def contract(density=None, charges=None):
            self.calls.append('density' if density is not None else 'charges')
            return (np.einsum('Lij,ij->L', self.g, density) if density is not None
                    else -np.einsum('Lij,L->ij', self.g, charges))
        self.s._contract = contract

    def test_signed_response_linearity_reciprocity_and_preservation(self):
        a = np.array([[1., -.2], [-.2, -.5]])
        b = np.array([[.4, .1], [.1, .2]])
        original = a.copy()
        cache = self.s._intermediates
        factor = cache['factor'][0]
        saved_factor = factor.copy()
        q = cache['q']
        expected = -np.einsum('Lij,L->ij', self.g, np.linalg.solve(
            self.matrix, (self.s.eps - 1) / self.s.eps * np.einsum('Lij,ij->L', self.g, a)))
        actual = r.density_response(self.s, a)
        np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
        self.assertLessEqual(float(np.sum(a*actual)), 1e-10)
        rb = r.density_response(self.s, b)
        np.testing.assert_allclose(r.density_response(self.s, a - 2*b), actual - 2*rb, atol=1e-12, rtol=0)
        self.assertAlmostEqual(float(np.sum(a*rb)), float(np.sum(b*actual)), places=12)
        np.testing.assert_array_equal(a, original)
        np.testing.assert_array_equal(factor, saved_factor)
        self.assertIs(cache, self.s._intermediates)
        self.assertIs(factor, cache['factor'][0])
        self.assertIs(q, cache['q'])
        np.testing.assert_array_equal(q, [7., 9.])

    def test_exact_epsilon_one_without_contractions(self):
        self.s.eps = 1
        self.assertTrue(np.array_equal(r.density_response(self.s, np.eye(2)), np.zeros((2, 2))))
        self.assertEqual(self.calls, [])

    def test_rejected_inputs_do_not_contract_or_change_density(self):
        for bad in (np.eye(2, dtype=complex), np.ones((1, 2, 2)), np.ones((3, 3)),
                    np.array([[1., 1e-15], [0., 1.]]), np.full((2, 2), np.nan),
                    np.full((2, 2), np.inf), np.full((2, 2), 'x'), [[1., 0.], [0., 1.]]):
            with self.subTest(input=repr(bad)), self.assertRaises(ValueError):
                r.density_response(self.s, bad)
        self.assertEqual(self.calls, [])

    def test_build_required_and_original_guards_remain(self):
        with self.assertRaises(TypeError):
            r.density_response(SimpleNamespace(), np.eye(2))
        self.s._intermediates = None
        with self.assertRaises(ValueError):
            r.density_response(self.s, np.eye(2))
        for obj, names in ((self.s, ('_B_dot_x', 'grad', 'hess', 'nuc_grad_method', 'Hessian')),
                           (r.memory.qualified.GroundStateOnly(), ('gen_response', 'stability', 'TDA', 'TDDFT', 'newton'))):
            for name in names:
                with self.assertRaises(NotImplementedError):
                    getattr(obj, name)()
        self.s.equilibrium_solvation = True
        with self.assertRaises(NotImplementedError):
            r.density_response(self.s, np.eye(2))

    def test_launch_rejects_changed_pins_and_existing_run(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            run.save(base/'preparation.json', {'pins': {'fixture': 'original'}})
            run.save(base/'independent-root-review.json', {'status': 'APPROVED_FOR_ONE_BOUNDED_NATIVE_CHILD',
                'preparation_sha256': run.sha(base/'preparation.json')})
            with (patch.object(run, 'BASE', base), patch.object(run, 'RUN', base/'run-v1'),
                  patch.object(run, 'pins', return_value={'fixture': 'changed'})):
                with self.assertRaises(ValueError):
                    run.launch()
                self.assertFalse((base/'run-v1').exists())
            (base/'run-v1').mkdir()
            with (patch.object(run, 'BASE', base), patch.object(run, 'RUN', base/'run-v1'),
                  patch.object(run, 'pins', return_value={'fixture': 'original'})):
                with self.assertRaises(ValueError):
                    run.launch()

    def test_launch_requires_matching_root_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            run.save(base/'preparation.json', {'pins': {}})
            with patch.object(run, 'BASE', base), patch.object(run, 'RUN', base/'run-v1'):
                with self.assertRaises(ValueError):
                    run.launch()
                for status, digest in (('REJECTED', run.sha(base/'preparation.json')),
                                       ('APPROVED_FOR_ONE_BOUNDED_NATIVE_CHILD', 'wrong')):
                    run.save(base/'independent-root-review.json', {'status': status, 'preparation_sha256': digest})
                    with self.assertRaises(ValueError):
                        run.launch()
                self.assertFalse((base/'run-v1').exists())

    def test_prepare_rejects_existing_preparation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            run.save(base/'preparation.json', {'status': 'sentinel'})
            with patch.object(run, 'BASE', base), self.assertRaises(ValueError):
                run.prepare()
            self.assertEqual(run.read(base/'preparation.json'), {'status': 'sentinel'})


if __name__ == '__main__':
    from pyscf.scf import hf
    from pyscf import gto
    with (patch.object(hf.SCF, 'kernel', side_effect=AssertionError('No SCF')),
          patch.object(gto, 'M', side_effect=AssertionError('No native molecule'))):
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ResponseTests))
    out = Path(__file__).parent / 'evidence'
    out.mkdir(exist_ok=True)
    (out / 'mock-tests.json').write_text(json.dumps({'tests_run': result.testsRun,
        'success': result.wasSuccessful(), 'native_probe_run': False, 'SCFs_launched': 0}, indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
