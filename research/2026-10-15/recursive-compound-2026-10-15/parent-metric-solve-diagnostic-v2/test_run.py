import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np

BASE = Path(__file__).resolve().parent
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

v2 = load('v2', BASE/'run.py')
old = load('old_tests', BASE.parent/'parent-metric-solve-diagnostic/test_run.py')
probe = load('metadata_probe', BASE/'probe.py')


class MetadataTests(unittest.TestCase):
    def test_real_metadata_matches_frozen(self):
        result = probe.probe()
        self.assertEqual(result, v2.v1.read(BASE/'metadata-probe.json'))
        self.assertTrue(result['exact_prior_match'])
        self.assertTrue(result['aux_exact_prior_match'])
        self.assertEqual(result['mocked_integral_calls'], ['int1e_kin_sph', 'int1e_nuc_sph', 'ECPscalar_sph'])

    def test_initializer_matches_same_full_state(self):
        from pyscf import gto
        mol = gto.M(atom=v2.v1.r.first.parent_atoms(), unit='Angstrom', basis={e: 'def2-svp' for e in ('O', 'Mo', 'H')}, ecp={'Mo': 'def2-svp'}, charge=-8, spin=0, verbose=0)
        v2.initialize_ecp_metadata(mol)
        self.assertEqual(v2.v1.r.molecule_state(mol), v2.v1.read(v2.v1.SOURCE/'molecule-state.json'))
        with self.assertRaises(ValueError): v2.initialize_ecp_metadata(mol)

    def test_setup_happens_before_worker_fingerprint(self):
        from pyscf import gto
        mol = object()
        events = []
        with patch.object(gto, 'M', return_value=mol), patch.object(v2, 'initialize_ecp_metadata', side_effect=lambda m: events.append('metadata') or m), patch.object(v2.v1, 'worker', side_effect=lambda: (gto.M(basis='def2-svp'), events.append('worker_check'))):
            v2.worker()
        self.assertEqual(events, ['metadata', 'worker_check'])


if __name__ == '__main__':
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(old.Tests), unittest.defaultTestLoader.loadTestsFromTestCase(MetadataTests)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    v2.v1.write(BASE/'qualification.json', {'passed': result.wasSuccessful(), 'tests_run': result.testsRun, 'cases': old.qualification(), 'metadata_probe_sha256': v2.v1.sha(BASE/'metadata-probe.json'), 'native_parent_integrals': 0, 'J_calls': 0, 'SCFs': 0})
    raise SystemExit(0 if result.wasSuccessful() else 1)
