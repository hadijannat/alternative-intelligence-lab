import unittest
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
from pyscf import dft, gto
from rij import install
from run import accepted


class AdapterGuards(unittest.TestCase):
    def setUp(self):
        self.mol=gto.M(atom='H 0 0 0; H 0 0 .74',basis='sto-3g',verbose=0)
        self.mf=dft.RKS(self.mol); self.mf.xc='PBE'; self.mf.direct_scf=True
        self.mf.chkfile=None
        if getattr(self.mf,'_chkfile',None) is not None:self.mf._chkfile.close()
        install(self.mf)
        self.dm=np.eye(self.mol.nao)
        self.factor=(np.eye(2),True)

    def backend(self,obj,dm,hermi,tolerance):
        obj._vjopt=SimpleNamespace(j2c_type='cd',j2c=self.factor)
        return dm*2

    def test_valid_call_reuses_factor_and_counts(self):
        with patch('rij.df_jk.get_j',side_effect=self.backend) as backend:
            np.testing.assert_array_equal(self.mf.get_j(dm=self.dm),self.dm*2)
            np.testing.assert_array_equal(self.mf.get_j(dm=-self.dm),-self.dm*2)
            self.assertEqual(backend.call_count,2)
            self.assertEqual(self.mf._rij_calls,2)

    def test_unsupported_requests_never_call_backend(self):
        with patch('rij.df_jk.get_j') as backend:
            for options in ({'with_k':True},{'with_j':False,'with_k':False},
                            {'with_k':False,'omega':.1},{'with_k':False,'hermi':0},
                            {'with_k':False,'mol':self.mol.copy()}):
                with self.subTest(options=options),self.assertRaises(ValueError):
                    self.mf.get_jk(dm=self.dm,**options)
            self.assertFalse(backend.called)

    def test_bad_density_never_calls_backend(self):
        values=(np.zeros((3,3)),self.dm.astype(complex),np.array([[1.,1.],[0.,1.]]),
                np.full((2,2),np.nan),np.full((2,2),np.inf))
        with patch('rij.df_jk.get_j') as backend:
            for density in values:
                with self.subTest(density=density),self.assertRaises(ValueError):
                    self.mf.get_j(dm=density)
            self.assertFalse(backend.called)

    def test_changed_geometry_rejected(self):
        self.mol.set_geom_('H 0 0 0; H 0 0 .80')
        with self.assertRaises(ValueError):self.mf.get_j(dm=self.dm)

    def test_changed_functional_and_auxbasis_rejected(self):
        self.mf.xc='B3LYP'
        with self.assertRaises(ValueError):self.mf.get_j(dm=self.dm)
        self.mf.xc='PBE'; self.mf._rij_df.auxbasis='def2-svp-jkfit'
        with self.assertRaises(ValueError):self.mf.get_j(dm=self.dm)

    def test_regular_fallback_rejected(self):
        def regular(obj,*args):
            obj._vjopt=SimpleNamespace(j2c_type='regular',j2c=np.eye(2))
            return self.dm
        with patch('rij.df_jk.get_j',side_effect=regular),self.assertRaises(ValueError):
            self.mf.get_j(dm=self.dm)

    def test_tensor_storage_rejected(self):
        for name in ('_cderi','_cderi_to_save'):
            with self.subTest(name=name):
                setattr(self.mf._rij_df,name,'unqualified.h5')
                with self.assertRaises(ValueError):self.mf.get_j(dm=self.dm)
                setattr(self.mf._rij_df,name,None)

    def test_factor_replacement_rejected(self):
        with patch('rij.df_jk.get_j',side_effect=self.backend):
            self.mf.get_j(dm=self.dm)
            old=self.factor; self.factor=(np.eye(2),True)
            with self.assertRaises(ValueError):self.mf.get_j(dm=self.dm)
            self.assertIsNot(old[0],self.factor[0])

    def test_nonfinite_backend_result_rejected(self):
        def nonfinite(obj,*args):
            obj._vjopt=SimpleNamespace(j2c_type='cd',j2c=self.factor)
            return np.full((2,2),np.nan)
        with patch('rij.df_jk.get_j',side_effect=nonfinite),self.assertRaises(ValueError):
            self.mf.get_j(dm=self.dm)

    def test_supervisor_guard_reason_overrides_zero_exit(self):
        good={'returncode':0,'termination_reason':None,'monitor_error':None}
        self.assertTrue(accepted(good))
        for changed in ({'returncode':1},{'termination_reason':'WALL_LIMIT'},
                        {'termination_reason':'RSS_LIMIT'},{'monitor_error':'ps failure'}):
            with self.subTest(changed=changed):self.assertFalse(accepted({**good,**changed}))


if __name__=='__main__':unittest.main()
