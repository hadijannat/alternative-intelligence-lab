import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import weakref
import numpy as np

spec=importlib.util.spec_from_file_location('saved_j_test_driver',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
h=run.handoff


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.dm=np.array([[2.,.1],[.1,1.]]);self.dm.flags.writeable=False
        self.j=np.array([[3.,.2],[.2,4.]])
        self.mol=types.SimpleNamespace(nao=2,_bas=np.array([[1,2]]),_env=np.array([0.,1.]),coordinates=np.zeros((1,3)))
        self.mol.atom_coords=lambda:self.mol.coordinates
        obj=types.SimpleNamespace(mol=self.mol,_vjopt=None,_cderi=None,_cderi_to_save=None,auxbasis='def2-universal-jkfit')
        self.mf=types.SimpleNamespace(mol=self.mol,_rij_df=obj,_rij_calls=0,xc='PBE',direct_scf=True,direct_scf_tol=1e-13)
        self.calls=[]
        def native(**kwargs):self.calls.append(kwargs);self.mf._rij_calls+=1;return np.asarray(kwargs['dm'])*7,None
        self.mf.get_jk=native
        np.savez(self.root/'arrays.npz',initial_P=self.dm,initial_Jmemory=self.j)
        run.save(self.root/'supervisor.json',{'returncode':0,'termination_reason':None,'monitor_error':None})
        run.save(self.root/'result.json',{'case':'new-external','phase':'operators','status':'PASS_OPERATORS','SCFs_launched':0,'checks':[{'pass':True}]})
        self.proof={'artifact':str(self.root/'arrays.npz'),'receipt':str(self.root/'supervisor.json'),'result':str(self.root/'result.json'),
                    'j_key':'initial_Jmemory','density_key':'initial_P','case':'new-external','density_sha256':h.density_digest(self.dm)}
        self.rehash()
    def tearDown(self):self.temp.cleanup()
    def rehash(self):
        for key in ('artifact','receipt','result'):self.proof[key+'_sha256']=h.sha(self.proof[key])
    def install(self):return h.install(self.mf,self.dm,self.proof)
    def get(self,dm=None,**kw):return self.mf.get_jk(dm=self.dm if dm is None else dm,with_k=False,**kw)

    def test_lazy_exact_hit_writable_independence_and_native_fallback(self):
        with patch.object(np,'load',wraps=np.load) as loader:
            self.install();self.assertEqual(loader.call_count,0)
            answer,k=self.get();self.assertEqual(loader.call_count,1)
        np.testing.assert_array_equal(answer,self.j);self.assertIsNone(k)
        self.assertTrue(answer.flags.writeable and h.owns_storage(answer));self.assertFalse(np.shares_memory(answer,self.dm))
        self.assertEqual((self.mf.saved_J_hits,self.mf._rij_calls,len(self.calls)),(1,0,0))
        answer+=100
        with np.load(self.proof['artifact']) as source:np.testing.assert_array_equal(source['initial_Jmemory'],self.j)
        delta=np.eye(2)*.01;fallback,_=self.get(delta)
        np.testing.assert_array_equal(fallback,delta*7);self.assertIs(self.calls[0]['dm'],delta)
        self.assertEqual((self.mf.saved_J_hits,self.mf._rij_calls),(1,1))
        self.assertFalse(self.mf._saved_J_pending)

    def test_cache_releases_density_reference_after_consumption(self):
        self.install();ref=weakref.ref(self.dm);self.get();self.dm=None
        self.assertIsNone(ref())

    def test_first_mismatch_does_not_consume_or_fallback(self):
        self.install()
        for value in (self.dm+.01,self.dm.astype(np.float32),np.eye(3),np.array([[np.nan,0.],[0.,1.]])):
            with self.assertRaises(ValueError):self.get(value)
            self.assertTrue(self.mf._saved_J_pending);self.assertEqual(self.calls,[])
        with self.assertRaises(ValueError):self.mf.get_jk(dm=None,with_k=False)
        self.get();self.assertEqual(self.mf.saved_J_hits,1)

    def test_mutated_readonly_reference_and_cutoff_rejected(self):
        self.install();self.dm.flags.writeable=True;self.dm[0,0]+=1;self.dm.flags.writeable=False
        with self.assertRaises(ValueError):self.get()
        self.assertEqual(self.calls,[])

    def test_request_molecule_and_storage_guards(self):
        self.install()
        for kwargs in ({'omega':0.},{'hermi':0},{'with_j':False},{'with_k':True},{'mol':object()}):
            with self.assertRaises(ValueError):self.mf.get_jk(dm=self.dm,**{'with_k':False,**kwargs})
        changes=[(self.mf,'xc','B3LYP'),(self.mf,'direct_scf',False),(self.mf,'direct_scf_tol',1e-8),
                 (self.mf._rij_df,'auxbasis','other'),(self.mf._rij_df,'_cderi',object()),
                 (self.mf._rij_df,'_cderi_to_save','file'),(self.mf._rij_df,'_vjopt',object()),(self.mf,'mol',object())]
        for obj,key,value in changes:
            original=getattr(obj,key);setattr(obj,key,value)
            with self.assertRaises(ValueError):self.get()
            setattr(obj,key,original)
        for array in (self.mol.coordinates,self.mol._bas,self.mol._env):
            old=array.copy();array.flat[0]+=1
            with self.assertRaises(ValueError):self.get()
            array[:]=old
        self.get();self.mf.direct_scf_tol=1e-8
        with self.assertRaises(ValueError):self.get(np.eye(2))

    def test_provenance_digest_status_case_keys_and_density_binding(self):
        for field,value in (('artifact_sha256','0'*64),('receipt_sha256','0'*64),('result_sha256','0'*64),
                            ('case','other'),('j_key','RI_Jmemory'),('density_key','other'),('density_sha256','0'*64)):
            old=self.proof[field];self.proof[field]=value
            with self.assertRaises((ValueError,KeyError)):self.install()
            self.proof[field]=old
        receipt=run.read(self.proof['receipt'])
        for key in receipt:
            changed=dict(receipt);del changed[key];run.save(self.proof['receipt'],changed);self.rehash()
            with self.assertRaises(ValueError):self.install()
        run.save(self.proof['receipt'],receipt);self.rehash()
        for change in ({'case':'other'},{'phase':'scf'},{'SCFs_launched':1},{'checks':[{'pass':False}]}):
            result={'case':'new-external','phase':'operators','status':'PASS_OPERATORS','SCFs_launched':0,'checks':[{'pass':True}],**change}
            run.save(self.proof['result'],result);self.rehash()
            with self.assertRaises(ValueError):self.install()

    def test_artifact_change_between_install_and_first_hit_rejected(self):
        self.install();Path(self.proof['artifact']).write_bytes(b'changed')
        with self.assertRaises(ValueError):self.get()
        self.assertEqual(self.calls,[]);self.assertTrue(self.mf._saved_J_pending)

    def test_npy_owned_load_requires_result_digest_and_cycle_zero_binding(self):
        np.save(self.root/'J.npy',self.j);self.proof.update(artifact=str(self.root/'J.npy'),j_key=None,density_cycle=0)
        self.rehash();run.save(self.proof['result'],{'status':'PASS_BOUNDED_FIRST_J_ONLY','SCFs_launched':0,'J_sha256':self.proof['artifact_sha256'],'checks':{'finite':True}});self.rehash()
        original=run.read(self.proof['result'])
        run.save(self.proof['result'],{**original,'J_sha256':'0'*64});self.rehash()
        with self.assertRaises(ValueError):self.install()
        run.save(self.proof['result'],original);self.rehash()
        for cycle in (1,False,None):
            self.proof['density_cycle']=cycle
            with self.assertRaises(ValueError):self.install()
        self.proof['density_cycle']=0;self.install();answer,_=self.get();answer[0,0]=99
        np.testing.assert_array_equal(np.load(self.proof['artifact']),self.j)
        self.assertTrue(h.owns_storage(answer) and answer.flags.writeable);self.assertFalse(isinstance(answer,np.memmap))


class RunnerGuards(unittest.TestCase):
    def test_phase_gate_rejects_bad_receipts_counts_and_checks(self):
        receipt={'returncode':0,'termination_reason':None,'monitor_error':None}
        result={'case':'new-external','phase':'operators','status':'PASS_OPERATORS','SCFs_launched':0,'checks':[{'pass':True}]}
        self.assertTrue(run.phase_accepted(receipt,result,'operators'))
        for key in receipt:
            changed=dict(receipt);del changed[key];self.assertFalse(run.phase_accepted(changed,result,'operators'))
        for change in ({'case':'parent'},{'phase':'scf'},{'SCFs_launched':False},{'SCFs_launched':1},{'checks':[]},{'checks':['bad']},{'checks':[None]},{'checks':{'pass':True}},{'checks':[{'pass':False}]}):
            self.assertFalse(run.phase_accepted(receipt,{**result,**change},'operators'))

    def test_output_and_root_review_binding(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            for path in (run.BASE,run.FIRST/'run-v1',run.BASE/'..'/'escape'):
                with self.assertRaises(ValueError):run.owned(path)
            run.save(run.BASE/'preparation.json',{'pins':{'fixed':True}})
            review={'status':'APPROVED_SMALL_SAVED_J_QUALIFICATION','independent_root_review':True,'reviewer':'synthetic-root','preparation_sha256':run.sha(run.BASE/'preparation.json')}
            with patch.object(run,'manifest',return_value={'fixed':True}):
                for change in ({},{'preparation_sha256':'changed'},{'independent_root_review':False},{'reviewer':''}):
                    run.save(run.BASE/'independent-root-review.json',{**review,**change})
                    if change:
                        with self.assertRaises(ValueError):run.validate_gate()
                    else:self.assertIn('review_sha256',run.validate_gate())

    def test_failed_prerequisite_prevents_preparation(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'prerequisites',side_effect=ValueError('first J incomplete')),patch.object(run,'proof',side_effect=AssertionError('No scientific data load')):
            with self.assertRaises(ValueError):run.prepare()
            self.assertFalse((run.BASE/'preparation.json').exists())

    def launch_case(self,broken=None):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            calls=[]
            def monitored(command,out,wall,rss):
                phase=command[-1];calls.append(phase);self.assertEqual((wall,rss),(180,2*2**30))
                if broken=='supervisor':raise OSError('synthetic supervisor launch failure')
                out.mkdir()
                result={'case':'new-external','phase':phase,'status':'PASS_'+phase.upper(),'SCFs_launched':int(phase=='scf'),'checks':[{'pass':True}]}
                if broken=='operator_check' and phase=='operators':result['checks'][0]['pass']=False
                run.save(out/'result.json',result)
                if broken=='truncated_scf' and phase=='scf':(out/'result.json').write_text('{')
                return {'returncode':0,'termination_reason':None,'monitor_error':None}
            supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'},monitored_run=monitored)
            original=run.read
            def read(path):return {'pins':{'runtime':{'python':'/synthetic/python'}}} if Path(path)==run.QUAL/'preparation.json' else original(path)
            with patch.object(run,'validate_gate',return_value={'review':'fixed'}),patch.object(run,'load',return_value=supervisor),patch.object(run,'read',side_effect=read):
                self.assertEqual(run.launch(),int(broken is not None))
                with self.assertRaises(FileExistsError):run.launch()
            self.assertEqual(calls,['operators'] if broken in ('operator_check','supervisor') else ['operators','scf'])
            terminal=original(run.BASE/'run-v1/launch-result.json');self.assertEqual(len(terminal['receipts']),len(calls))
            if broken=='truncated_scf':self.assertTrue(terminal['errors']['scf'])
            if broken=='supervisor':self.assertEqual(terminal['receipts']['operators']['termination_reason'],'SUPERVISOR_ERROR')
    def test_bounded_two_child_one_scf_route(self):self.launch_case()
    def test_failed_operator_blocks_scf(self):self.launch_case('operator_check')
    def test_supervisor_error_preserves_failed_terminal(self):self.launch_case('supervisor')
    def test_truncated_scf_preserves_receipts(self):self.launch_case('truncated_scf')


if __name__=='__main__':unittest.main(verbosity=2)
