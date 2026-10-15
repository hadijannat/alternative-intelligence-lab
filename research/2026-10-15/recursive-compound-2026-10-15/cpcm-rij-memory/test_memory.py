import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import numpy as np
import scipy.linalg
from pyscf import df,gto
from pyscf.df import df_jk
import memory as m

OBS=[]

class TinyMechanics(unittest.TestCase):
    def test_synthetic_alias_and_solve(self):
        rng=np.random.default_rng(7392016);a=rng.standard_normal((16,16))
        original=a@a.T+np.eye(16);matrix=np.array(original,order='F')
        pointer=matrix.ctypes.data;factor=m.factor_inplace(matrix)
        self.assertEqual(pointer,factor[0].ctypes.data)
        self.assertFalse(factor[0].flags.writeable)
        rhs=np.arange(16,dtype=float);solution=m.solve_checked(factor,rhs)
        error=float(np.max(np.abs(original@solution-rhs)))
        self.assertLess(error,1e-10)
        OBS.append({'scenario':'16x16 SPD alias/solve','same_pointer':True,'immutable':True,'residual':error})
    def test_layout_and_nonfinite_guards(self):
        for a in (np.eye(3,order='C'),np.full((3,3),np.nan,order='F')):
            with self.assertRaises(ValueError):m.factor_inplace(a)
        factor=m.factor_inplace(np.eye(3,order='F'))
        with self.assertRaises(ValueError):m.solve_checked(factor,np.array([1.,np.inf,2.]))
        with self.assertRaises(ValueError):m.solve_checked(factor,np.ones(2))
        factor[0].flags.writeable=True
        with self.assertRaises(ValueError):m.solve_checked(factor,np.ones(3))
    def test_indefinite_aborts(self):
        with self.assertRaises(m.FactorizationAborted):m.factor_inplace(np.array([[1.,2.],[2.,1.]],order='F'))
    def test_bounded_finite_slices(self):
        self.assertLessEqual(m.CHUNK,65536)
        sizes=[];original=np.isfinite
        values=np.ones(2*65536+3)
        facade=SimpleNamespace(ndarray=np.ndarray,float64=np.float64,
                               isfinite=lambda a:(sizes.append(a.size) or original(a)))
        with patch.object(m,'np',facade):
            m.finite_chunks(values)
        self.assertEqual(sum(sizes),131075)
        self.assertGreaterEqual(len(sizes),3)
        self.assertLessEqual(max(sizes),65536)
        finite_sizes=sizes.copy();sizes.clear()
        values[-1]=np.inf
        with patch.object(m,'np',facade),self.assertRaises(ValueError):
            m.finite_chunks(values)
        self.assertEqual(sum(sizes),131075)
        self.assertLessEqual(max(sizes),65536)
        OBS.append({'scenario':'bounded finite validation','literal_ceiling':65536,
                    'observed_chunk_sizes':finite_sizes,'last_nonfinite_rejected':True,
                    'nonfinite_chunk_sizes':sizes.copy()})
    def test_tiny_native_RIJ_and_private_globals(self):
        original_get_j=df_jk.get_j;original_cho=scipy.linalg.cho_factor
        mol=gto.M(atom='He 0 0 0',basis='sto-3g',verbose=0)
        density=np.ones((1,1));reference=df_jk.get_j(df.DF(mol,'def2-universal-jkfit'),density,1)
        obj=df.DF(mol,'def2-universal-jkfit');alias=[]
        def recording(a,**kwargs):
            pointer=a.ctypes.data;factor=m.factor_inplace(a,**kwargs)
            alias.append({'shape':list(a.shape),'Fortran':bool(a.flags.f_contiguous),'same_pointer':pointer==factor[0].ctypes.data})
            return factor
        with patch.object(m.private_scipy.linalg,'cho_factor',recording):
            result=m.native_get_j(obj,density,1)
            factor=obj._vjopt.j2c[0]
            again=m.native_get_j(obj,density,1)
        error=float(np.max(np.abs(result-reference)))
        self.assertLess(error,1e-10);np.testing.assert_allclose(result,again,atol=1e-10,rtol=0)
        self.assertIs(obj._vjopt.j2c[0],factor);self.assertFalse(factor.flags.writeable)
        self.assertIs(df_jk.get_j,original_get_j);self.assertIs(scipy.linalg.cho_factor,original_cho)
        self.assertIsNot(m.native_get_j.__globals__,df_jk.get_j.__globals__)
        self.assertIsNone(obj._cderi)
        OBS.append({'scenario':'He sto3g native two-pass JKFIT operator','max_error':error,'metric':alias,'reuse':True,'original_global_callables_unchanged':True})
    def test_guarded_adapter_keeps_local_backend(self):
        from pyscf import dft
        mol=gto.M(atom='He 0 0 0',basis='sto-3g',verbose=0)
        mf=dft.RKS(mol);mf.xc='PBE';mf.chkfile=None
        if getattr(mf,'_chkfile',None) is not None:mf._chkfile.close()
        calls=[];m.install(mf,calls.append)
        value=mf.get_j(dm=np.ones((1,1)))
        self.assertTrue(np.isfinite(value).all());self.assertEqual(len(calls),1)
        self.assertEqual(calls[0]['factor_type'],'cd')
        self.assertFalse(mf._rij_df._vjopt.j2c[0].flags.writeable)
        mf.xc='B3LYP'
        with self.assertRaises(ValueError):mf.get_j(dm=np.ones((1,1)))
        OBS.append({'scenario':'guarded private RI adapter','metric_calls':calls,'changed_method_rejected':True})
    def test_native_failure_bypasses_regular_fallback(self):
        mol=gto.M(atom='He 0 0 0',basis='sto-3g',verbose=0)
        obj=df.DF(mol,'def2-universal-jkfit');mutated=[]
        def corrupt(a,**kwargs):
            a[0,0]=-123.;mutated.append(True)
            raise scipy.linalg.LinAlgError('Injected destructive failure')
        facade=SimpleNamespace(linalg=SimpleNamespace(cho_factor=corrupt,LinAlgError=scipy.linalg.LinAlgError))
        with patch.object(m,'scipy',facade),patch.object(m.private_scipy.linalg,'solve') as fallback:
            with self.assertRaises(m.FactorizationAborted):m.native_get_j(obj,np.ones((1,1)),1)
            self.assertFalse(fallback.called)
        self.assertTrue(mutated);self.assertIsNone(obj._vjopt)
        OBS.append({'scenario':'injected destructive native factor failure','matrix_mutated':True,'regular_fallback_calls':0,'optimizer_published':False,'exception':'FactorizationAborted'})
    def test_tiny_PCM_factor_only_equivalence_and_reset(self):
        mol=gto.M(atom='He 0 0 0',basis='sto-3g',verbose=0)
        old=m.qualified.BlockedPCM(mol);new=m.MemoryPCM(mol)
        old.eps=new.eps=78.4;old.build(ng=6);new.build(ng=6)
        self.assertNotIn('S',new._intermediates)
        self.assertEqual(new.ao_block,1)
        factor=new._intermediates['factor'][0]
        original=old._intermediates['S']
        reconstructed=np.tril(factor)@np.tril(factor).T
        serror=float(np.max(np.abs(reconstructed-original)))
        e0,v0=old._get_vind(np.ones((1,1)));e1,v1=new._get_vind(np.ones((1,1)))
        self.assertLess(serror,1e-10);self.assertLess(abs(e0-e1),1e-10)
        self.assertLess(float(np.max(np.abs(v0-v1))),1e-10)
        self.assertIs(new._intermediates['factor'][0],factor)
        new.reset();self.assertIsNone(new._intermediates)
        OBS.append({'scenario':'He six-surface-point factor-only PCM','factor_shape':list(factor.shape),'S_reconstruction_error':serror,'energy_error':abs(e0-e1),'AO_potential_error':float(np.max(np.abs(v0-v1))),'retained_S':False,'reset_cleared_factor':True})

if __name__=='__main__':
    from pyscf.scf import hf
    with patch.object(hf.SCF,'kernel',side_effect=AssertionError('SCF forbidden')):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(TinyMechanics)
        result=unittest.TextTestRunner(verbosity=2).run(suite)
    (Path(__file__).parent/'evidence/observations.json').write_text(json.dumps({'observations':OBS,'tests_run':result.testsRun,'success':result.wasSuccessful(),'SCFs_launched':0,'parent_arrays_allocated':False},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
