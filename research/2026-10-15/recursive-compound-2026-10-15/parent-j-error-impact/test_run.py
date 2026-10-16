import importlib.util
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

spec=importlib.util.spec_from_file_location('j_error_impact',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class ErrorImpactTests(unittest.TestCase):
    def test_known_offdiagonal_contraction_and_norm_bounds(self):
        p=np.array([[2.,.5],[.5,1.]])
        delta=np.array([[.1,-.2],[-.2,.3]])
        r=run.impact(p,delta,np.zeros((2,2)))
        self.assertAlmostEqual(r['oriented_delta_E_C_hartree'],.15)
        self.assertAlmostEqual(r['delta_J_Frobenius_norm'],math.sqrt(.18))
        self.assertAlmostEqual(r['computed_maxnorm_energy_bound_hartree'],.6)
        self.assertAlmostEqual(r['computed_Frobenius_energy_bound_hartree'],.5*math.sqrt(5.5*.18))
        self.assertLess(abs(r['oriented_delta_E_C_hartree']),r['computed_maxnorm_energy_bound_hartree'])
        self.assertLess(abs(r['oriented_delta_E_C_hartree']),r['computed_Frobenius_energy_bound_hartree'])
        self.assertEqual(r['argmax'],[1,1]);self.assertEqual(r['entries_above_original_tolerance'],4)

    def test_negative_output_reorients_energy_without_changing_norm(self):
        p=np.array([[1.,.25],[.25,2.]])
        reference=np.array([[4.,2.],[2.,5.]])
        delta=np.array([[.1,.2],[.2,-.3]])
        positive=run.impact(p,reference+delta,reference)
        negative=run.impact(p,-(reference+delta),reference,-1)
        self.assertEqual(positive,negative)
        wrong=run.impact(p,-(reference+delta),reference,1)
        self.assertNotEqual(negative['oriented_delta_E_C_hartree'],wrong['oriented_delta_E_C_hartree'])

    def test_fsum_preserves_cancellation_across_row_chunks(self):
        with patch.object(run,'CHUNK_ROWS',1):
            result=run.impact(np.ones((2,2)),np.array([[1e16,1.],[-1e16,1.]]),np.zeros((2,2)))
        self.assertEqual(result['oriented_delta_E_C_hartree'],1.)

    def test_invalid_shapes_dtype_and_nonfinite_rejected(self):
        p=np.eye(2)
        for density,a,b in ((np.zeros(2),p,p),(np.zeros((0,0)),np.zeros((0,0)),np.zeros((0,0))),
                            (p,np.eye(3),p),(p,p.astype(np.float32),p)):
            with self.assertRaises(ValueError):run.impact(density,a,b)
        for slot in range(3):
            for value in (np.nan,np.inf):
                arrays=[p.copy(),p.copy(),p.copy()];arrays[slot][0,0]=value
                with self.assertRaises(ValueError):run.impact(*arrays)

    def test_unreviewed_real_analysis_is_blocked_before_output(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'manifest',return_value={'frozen':'sha'}):
            run.write_new(run.BASE/'preparation.json',{'pins':{'frozen':'sha'}})
            with self.assertRaises(FileNotFoundError):run.analyze()
            self.assertFalse((run.BASE/'analysis-v1').exists())
            review={'status':'APPROVED_SAVED_ARRAY_ERROR_IMPACT','independent_root_review':True,'reviewer':'synthetic',
                    'preparation_sha256':run.sha(run.BASE/'preparation.json')}
            run.write_new(run.BASE/'independent-root-review.json',review);run.validate_gate()
            with patch.object(run,'manifest',return_value={'frozen':'changed'}):
                with self.assertRaises(ValueError):run.validate_gate()


if __name__=='__main__':unittest.main(verbosity=2)
