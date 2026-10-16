import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

spec=importlib.util.spec_from_file_location('localization',Path(__file__).with_name('run.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class LocalizationTests(unittest.TestCase):
    def test_transparent_AB_exact_C_and_preserved_C(self):
        solved=[]
        def solve(factor,rhs,**kwargs):
            a=np.array(rhs*2,order='F');solved.append(a);return a
        hook=m.SolveCapture(solve,lambda:{'fixed':True},3)
        rhs=np.arange(3,dtype=np.float64).reshape(3,1)
        for arm in ('A','B','C'):
            hook.arm=arm;out=hook(None,rhs+ord(arm))
            if arm!='C':self.assertIs(out,solved[-1])
            else:
                np.testing.assert_array_equal(out,hook.data['A']['rho_ordinary'])
                self.assertFalse(np.shares_memory(out,hook.data['A']['rho_ordinary']))
                np.testing.assert_array_equal(hook.data['C']['rho_ordinary'],solved[-1])
                self.assertFalse(np.array_equal(out,solved[-1]))
            self.assertFalse(np.shares_memory(hook.data[arm]['rho_ordinary'],solved[-1]))
            self.assertFalse(hook.returned_ids[arm]['capture_aliases_rhs'])
            self.assertTrue(out.flags.f_contiguous)
        with self.assertRaises(ValueError):hook(None,rhs)

    def test_layout_and_invariant_rejection(self):
        state={'cutoff':1e-13};hook=m.SolveCapture(lambda f,b,**k:b.copy(),lambda:state.copy(),3)
        hook.arm='A'
        with self.assertRaises(ValueError):hook(None,np.ones((3,1),dtype=np.float32))
        with self.assertRaises(ValueError):hook(None,np.ones((6,1))[::2])
        hook(None,np.ones((3,1)));state['cutoff']=2e-13;hook.arm='B'
        with self.assertRaisesRegex(ValueError,'Optimizer'):hook(None,np.ones((3,1)))

    def synthetic(self,out,fail_storage=False,mutate=False):
        state={'fixed':True};factor=np.eye(3);mf=types.SimpleNamespace(_rij_calls=0,with_solvent=types.SimpleNamespace())
        hook=m.SolveCapture(lambda f,b,**k:b*2,lambda:state.copy(),3)
        def get_j(dm):
            rho=hook(factor,np.ones((3,1))*(mf._rij_calls+1));mf._rij_calls+=1
            if mutate:dm[0,0]+=1
            return np.eye(2)*float(rho[0,0])
        mf.get_j=get_j;density=np.eye(2);digest=m.r.array_digest(density)
        def storage(number):
            if fail_storage:raise ValueError('storage changed')
            return {'fixed':True}
        events=[]
        def classify(out):
            self.assertEqual(mf._rij_calls,3)
            for arm,label in zip(m.ARMS,m.OUTPUTS):
                hashes=m.read(out/f'closed-output-hashes-{arm}.json')
                for name,digest in hashes.items():self.assertEqual(m.sha(out/(name+'.npy')),digest)
            events.append('classify')
            return {'numerical_nonpass':True}
        with patch.object(m,'BASE',out),patch.object(m.r.signed,'NAO',2),patch.object(m,'classify',side_effect=classify):
            answer=m.run_calls(mf,out,hook,lambda:(density.copy(),{}),lambda:None,storage,lambda:None,lambda *a,**k:events.append(a[0]),digest)
        return mf,hook,answer,events

    def test_three_calls_nonpass_and_save_before_classification(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);mf,hook,answer,events=self.synthetic(out)
            self.assertEqual(mf._rij_calls,3);self.assertEqual(len(answer[0]),3)
            self.assertEqual(events[-1],'classify')
            self.assertEqual(len(list(out.glob('*.npy'))),9)
            np.testing.assert_array_equal(np.load(out/'J_fixed_rho_A.npy'),np.load(out/'J_A.npy'))
            self.assertFalse(np.array_equal(np.load(out/'J_A.npy'),np.load(out/'J_B.npy')))
            self.assertFalse(np.array_equal(np.load(out/'rho_ordinary_C.npy'),np.load(out/'rho_ordinary_A.npy')))
            with self.assertRaises(FileExistsError):m.save_array(out,'J_A',np.eye(2))

    def test_invariant_failure_aborts_after_retaining_returned_arrays(self):
        for kind in ('storage','density'):
            with tempfile.TemporaryDirectory() as directory:
                out=Path(directory)
                with self.assertRaises(ValueError):self.synthetic(out,fail_storage=kind=='storage',mutate=kind=='density')
                self.assertTrue((out/'J_A.npy').exists());self.assertFalse((out/'J_B.npy').exists())
                self.assertFalse((out/'comparisons.json').exists())

    def test_reused_setup_defers_receipts_until_return(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);events=[]
            memory=types.SimpleNamespace(private_scipy=types.SimpleNamespace(linalg=types.SimpleNamespace(cho_solve=lambda f,b,**k:b.copy())))
            def install(mf,record):
                def native(dm):
                    result=memory.private_scipy.linalg.cho_solve(None,np.ones((19612,1)))
                    m.r.save(out/'factor.json',{'factor':True});record({'call':1})
                    self.assertFalse((out/'factor.json').exists());self.assertEqual(events,[])
                    return result
                mf.get_j=native;return mf
            memory.install=install
            def frozen_setup(out,stage,runtime):
                loaded=m.r.load('memory','unused');mf=types.SimpleNamespace()
                loaded.install(mf,lambda row:events.append('metric'))
                return mf,lambda:None,lambda n:{}
            old_save=m.r.save
            try:
                with patch.object(m.r,'setup',side_effect=frozen_setup),patch.object(m.r,'load',return_value=memory),patch.object(m,'optimizer_state',return_value={'fixed':True}):
                    mf,capture,guard,storage,flush=m.setup(out,lambda *a,**k:None,{})
                    capture.arm='A';mf.get_j(None)
                    self.assertFalse((out/'factor.json').exists());self.assertEqual(events,[])
                    flush();self.assertTrue((out/'factor.json').exists());self.assertEqual(events,['metric'])
            finally:m.r.save=old_save

    def test_fourth_call_request_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);mf,hook,answer,events=self.synthetic(out)
            with self.assertRaisesRegex(ValueError,'Call count before'):
                m.run_calls(mf,out,hook,lambda:(np.eye(2),{}),lambda:None,lambda n:{},lambda:None,lambda *a,**k:None,m.r.array_digest(np.eye(2)))

    def test_vector_reporting_has_no_threshold(self):
        row=m.vector_difference(np.array([1.,3.]),np.array([1.,1.]))
        self.assertEqual(row['max_absolute_difference'],2);self.assertAlmostEqual(row['RMS_difference'],2**.5)
        self.assertFalse(row['exact_equal']);self.assertIsNone(row['acceptance_threshold'])

    def test_optimizer_fingerprints_mutation(self):
        def mol():return types.SimpleNamespace(_atm=np.zeros((1,6),dtype=np.int32),_bas=np.zeros((1,8),dtype=np.int32),_env=np.zeros(4),natm=1,nao=1,nelectron=2,charge=0,spin=0,cart=False)
        opt=types.SimpleNamespace(q_cond=np.ones(3),direct_scf_tol=1e-13,fakemol=mol())
        mf=types.SimpleNamespace(mol=mol(),_rij_df=types.SimpleNamespace(_vjopt=opt,auxmol=mol()))
        before=m.optimizer_state(mf);opt.q_cond[0]=2
        self.assertNotEqual(before,m.optimizer_state(mf));opt.q_cond[0]=1
        self.assertEqual(before,m.optimizer_state(mf));opt.direct_scf_tol=2e-13
        self.assertNotEqual(before,m.optimizer_state(mf))

if __name__=='__main__':unittest.main(verbosity=2)
