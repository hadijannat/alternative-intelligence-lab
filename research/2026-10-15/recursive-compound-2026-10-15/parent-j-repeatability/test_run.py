import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

spec=importlib.util.spec_from_file_location('repeatability_probe',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class RepeatabilityTests(unittest.TestCase):
    def test_chunk_argmax_values_counts_and_sign(self):
        a=np.arange(25,dtype=np.float64).reshape(5,5);b=a.copy();a[1,4]+=2;a[4,1]+=2
        with patch.object(run,'NAO',5),patch.object(run,'CHUNK_ROWS',2):
            r=run.compare(a,b,1)
            self.assertEqual(r['max_absolute_error'],2);self.assertEqual(r['argmax'],[1,4])
            self.assertEqual(r['entries_above_tolerance'],2)
            self.assertEqual(r['values_at_argmax'],{'actual':11.,'reference':9.,'expected':9.})
            self.assertEqual(r['matrix_max_abs'],24.)
            self.assertTrue(run.compare(-b,b,-1)['pass'])
            self.assertFalse(run.compare(-b,b,1)['pass'])
            with self.assertRaises(ValueError):run.compare(a,np.full_like(a,np.nan),1)
            with self.assertRaises(ValueError):run.compare(a.astype(np.float32),b,1)

    def test_no_copy_factor_digest_and_mutation_detection(self):
        matrix=np.array([[2.,0.],[1.,3.]],order='F');matrix.flags.writeable=False
        obj=types.SimpleNamespace(_vjopt=types.SimpleNamespace(j2c=(matrix,True),j2c_type='cd'))
        creation={'factor_pointer':matrix.ctypes.data,'content_sha256':run.array_digest(matrix)}
        self.assertEqual(creation['content_sha256'],hashlib.sha256(matrix.T.tobytes()).hexdigest())
        with patch.object(run.signed,'NAUX',2):
            before=run.checked_factor(obj,creation)
            self.assertEqual(run.checked_factor(obj,creation,before),before)
            matrix.flags.writeable=True;matrix[0,0]+=1;matrix.flags.writeable=False
            with self.assertRaisesRegex(ValueError,'content/storage'):run.checked_factor(obj,creation,before)
        with self.assertRaises(ValueError):run.array_digest(np.ones((4,4))[:,::2])

    def test_molecule_array_and_metadata_mutations_rejected(self):
        mol=types.SimpleNamespace(_atm=np.zeros((2,6),dtype=np.int32),_bas=np.zeros((3,8),dtype=np.int32),
                                  _env=np.arange(12,dtype=np.float64),natm=2,nao=5,nelectron=4,charge=-1,spin=0,cart=False)
        baseline=run.molecule_state(mol)
        self.assertEqual(run.molecule_state(mol,baseline),baseline)
        for name in ('_atm','_bas','_env'):
            array=getattr(mol,name);array.flat[0]+=1
            with self.assertRaisesRegex(ValueError,'Molecule state'):run.molecule_state(mol,baseline)
            array.flat[0]-=1
        for name,value in (('natm',3),('nao',6),('nelectron',5),('charge',0),('spin',1),('cart',True)):
            old=getattr(mol,name);setattr(mol,name,value)
            with self.assertRaisesRegex(ValueError,'Molecule state'):run.molecule_state(mol,baseline)
            setattr(mol,name,old)

    def test_setup_fingerprints_after_allowed_ECP_initialization(self):
        mol=types.SimpleNamespace(_atm=np.zeros((1,6),dtype=np.int32),_bas=np.zeros((1,8),dtype=np.int32),
                                  _env=np.zeros(24),natm=196,nao=2,nelectron=1568,charge=-8,spin=0,cart=False)
        mf=types.SimpleNamespace(mol=mol,grids=types.SimpleNamespace(),_eri=None)
        calls=[]
        def attach(obj,solvent):obj.with_solvent=solvent;return obj
        def install(obj,metric):
            calls.append('install');obj.mol._env[18:20]=[3.,7.]
            obj._rij_calls=0;obj._rij_df=types.SimpleNamespace(_vjopt=None)
            return obj
        memory=types.SimpleNamespace(factor_inplace=lambda *a,**k:None,
             private_scipy=types.SimpleNamespace(linalg=types.SimpleNamespace()),
             qualified=types.SimpleNamespace(attach=attach),install=install,
             MemoryPCM=lambda m:types.SimpleNamespace(surface={},_intermediates={},v_grids_n=None))
        fake_pyscf=types.SimpleNamespace(gto=types.SimpleNamespace(M=lambda **kwargs:mol),
             dft=types.SimpleNamespace(RKS=lambda m:mf),lib=types.SimpleNamespace(num_threads=lambda:4))
        env={name:'1' for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}
        env.update(OMP_NUM_THREADS='4',OMP_DYNAMIC='FALSE')
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'NAO',2),patch.dict(sys.modules,{'pyscf':fake_pyscf}),patch.dict(os.environ,env),patch.object(run,'load',return_value=memory),patch.object(run.first,'parent_atoms',return_value=[]),patch.object(run.qualification,'runtime_pins',return_value={'fixed':True}),patch.object(run.qualification,'loaded_native_files',return_value=[]):
            out=run.BASE/'run-v1';out.mkdir()
            result,guard,storage=run.setup(out,lambda *a,**k:None,{'fixed':True})
            self.assertIs(result,mf);self.assertEqual(calls,['install'])
            self.assertEqual(run.read(out/'molecule-state.json'),run.molecule_state(mol))
            guard();mol._env[18]+=1
            with self.assertRaisesRegex(ValueError,'Molecule state changed'):guard()

    def exercise_calls(self,mode=None):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'NAO',2),patch.object(run.signed,'NAO',2),patch.object(run,'CHUNK_ROWS',1):
            out=run.BASE/'run-v1';out.mkdir();external=run.BASE/'external.npy';np.save(external,2*np.eye(2))
            mf=types.SimpleNamespace(_rij_calls=0,with_solvent=types.SimpleNamespace());calls=[];stages=[]
            def native(dm):
                calls.append(dm.copy());number=len(calls)
                if mode=='mutate_density':dm[0,0]+=1
                answer=dm*2
                if mode=='same_nonpass' and number==2:answer[0,0]+=1e-5
                if mode=='sign_nonpass' and number==3:answer[0,0]+=1e-5
                if mode=='nonfinite':answer[0,0]=np.nan
                if mode!='counter':mf._rij_calls+=1
                return answer
            mf.get_j=native
            def storage(number):
                if mode=='storage':raise ValueError('changed factor')
                return {'fixed':True}
            with patch.object(run,'EXTERNAL',external):
                args=(mf,out,lambda:(np.eye(2),{'cycle':0}),lambda:None,storage,
                      lambda name,**kw:stages.append(name),run.array_digest(np.eye(2)))
                if mode in ('mutate_density','nonfinite','counter','storage'):
                    with self.assertRaises(ValueError):run.run_calls(*args)
                    self.assertEqual(len(calls),1);self.assertTrue((out/'J1.npy').is_file())
                    self.assertFalse((out/'J2.npy').exists())
                    self.assertIn('returned_J_saved_closed',stages)
                    self.assertEqual(run.read(out/'call-records.json')[0]['J_sha256'],run.sha(out/'J1.npy'))
                else:
                    records,comparisons=run.run_calls(*args)
                    self.assertEqual(len(calls),3);self.assertEqual(len(records),3)
                    np.testing.assert_array_equal(calls[0],calls[1]);np.testing.assert_array_equal(calls[2],-calls[0])
                    self.assertEqual(len(comparisons['comparisons']),6)
                    self.assertEqual(comparisons,run.recompute(out))
                    if mode=='same_nonpass':
                        self.assertEqual(comparisons['categories']['same_sign'],'NONPASS')
                        self.assertTrue(comparisons['comparisons']['J3+J1']['pass'])
                    elif mode=='sign_nonpass':
                        self.assertEqual(comparisons['categories']['same_sign'],'PASS')
                        self.assertEqual(comparisons['categories']['sign_reversal'],'NONPASS')
                    else:self.assertEqual(set(comparisons['categories'].values()),{'PASS'})
                    for n in (1,2,3):self.assertTrue((out/f'post-call-{n}.bin').is_file())
                    with self.assertRaises(ValueError):run.run_calls(*args)

    def test_three_calls_continue_on_numerical_nonpass(self):
        for mode in (None,'same_nonpass','sign_nonpass'):
            with self.subTest(mode=mode):self.exercise_calls(mode)

    def test_returned_matrix_preserved_before_abort(self):
        for mode in ('mutate_density','nonfinite','counter','storage'):
            with self.subTest(mode=mode):self.exercise_calls(mode)

    def test_exclusive_outputs_and_partial_artifact_hashes(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            out=run.BASE/'run-v1';out.mkdir()
            digest=run.save_returned(out,1,np.eye(2),lambda *a,**k:None)
            with self.assertRaises(FileExistsError):run.save_returned(out,1,np.zeros((2,2)),lambda *a,**k:None)
            self.assertEqual(run.sha(out/'J1.npy'),digest)
            (out/'failure.json').write_text('recorded failure');(out/'stderr.txt').write_text('')
            artifacts=run.collect_artifacts(out)
            self.assertEqual(artifacts['sha256']['J1.npy'],digest)
            self.assertIn('failure.json',artifacts['sha256']);self.assertIn('stderr.txt',artifacts['sha256'])
            self.assertIn('J2.npy',artifacts['missing']);self.assertIn('J3.npy',artifacts['missing'])
            original_sha=run.sha
            with patch.object(run,'sha',side_effect=lambda p:(_ for _ in ()).throw(OSError('unreadable')) if Path(p).name=='failure.json' else original_sha(p)):
                artifacts=run.collect_artifacts(out)
            self.assertEqual(artifacts['sha256']['J1.npy'],digest)
            self.assertIn('failure.json',artifacts['errors'])

    def test_read_only_recompute_preserves_files_and_reports_missing(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'NAO',2):
            out=Path(directory);np.save(out/'J1.npy',np.eye(2));external=out/'old.npy';np.save(external,np.eye(2))
            before={str(p):run.sha(p) for p in out.iterdir()}
            with patch.object(run,'EXTERNAL',external):result=run.recompute(out)
            self.assertTrue(result['comparisons']['J1-Jold']['pass'])
            self.assertEqual(len(result['missing']),5)
            self.assertEqual(before,{str(p):run.sha(p) for p in out.iterdir()})

    def test_approval_binding_and_fresh_claim(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            pins={'qualification':{'terminal':'fixed'}}
            run.save(run.BASE/'preparation.json',{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins})
            review={'status':'APPROVED_ONE_PARENT_J_REPEATABILITY_DIAGNOSTIC','independent_root_review':True,
                    'reviewer':'synthetic','preparation_sha256':run.sha(run.BASE/'preparation.json'),'qualification_artifacts':pins['qualification']}
            with patch.object(run,'manifest',return_value=pins):
                with self.assertRaises(FileNotFoundError):run.launch()
                self.assertFalse((run.BASE/'run-v1').exists())
                run.save(run.BASE/'independent-root-review.json',review);run.validate_gate()
                for change in ({'status':'pending'},{'preparation_sha256':'wrong'},{'qualification_artifacts':{}},{'independent_root_review':False},{'reviewer':''}):
                    run.save(run.BASE/'independent-root-review.json',{**review,**change})
                    with self.assertRaises(ValueError):run.validate_gate()
            run.write_new(run.BASE/'claim.json',{'once':True})
            with self.assertRaises(FileExistsError):run.write_new(run.BASE/'claim.json',{'once':False})

    def success_result(self,nonpass=False):
        return {'status':run.NONPASS if nonpass else run.PASS,'invariants_passed':True,'gate_unchanged':True,
                'numerical_pass':not nonpass,'J_calls':3,'metric_calls':3,'factor_count':1,'SCFs_launched':0,
                'physical_admission':False,'parent_SCF_readiness':False,'sign_and_call_order_confounded':True,
                'categories':{'same_sign':'PASS','sign_reversal':'NONPASS' if nonpass else 'PASS','external_run':'PASS'}}

    def test_completed_nonpass_is_not_numerical_pass(self):
        for nonpass in (False,True):self.assertTrue(run.accepted_result(self.success_result(nonpass)))
        good=self.success_result()
        for key,value in (('J_calls',2),('metric_calls',False),('factor_count',2),('SCFs_launched',1),
                          ('numerical_pass',False),('invariants_passed',False),('categories',{}),
                          ('physical_admission',True),('parent_SCF_readiness',True),('sign_and_call_order_confounded',False)):
            self.assertFalse(run.accepted_result({**good,key:value}))
        for name in ('physical_admission','parent_SCF_readiness','sign_and_call_order_confounded'):
            missing=copy.deepcopy(good);del missing[name];self.assertFalse(run.accepted_result(missing))

    def test_supervisor_failure_keeps_partial_hashes(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            calls=[]
            def monitored(command,out,wall,rss):
                calls.append(command);self.assertEqual((wall,rss),(1000,10*2**30))
                np.save(out/'J1.npy',np.eye(2));(out/'failure.json').write_text('preserved')
                return {'returncode':-15,'termination_reason':'WALL_LIMIT','monitor_error':None}
            supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1'},monitored_run=monitored)
            original_read=run.read
            def read(path):
                if Path(path)==run.first.QUAL/'preparation.json':return {'pins':{'runtime':{'python':'/synthetic/python'}}}
                return original_read(path)
            with patch.object(run,'validate_gate',return_value={'fixed':True}),patch.object(run,'load',return_value=supervisor),patch.object(run,'read',side_effect=read):
                self.assertEqual(run.launch(),1)
                with self.assertRaises(FileExistsError):run.launch()
            result=run.read(run.BASE/'run-v1/launch-result.json')
            self.assertEqual(result['status'],run.INCOMPLETE);self.assertEqual(len(calls),1)
            self.assertIn('J1.npy',result['artifacts']['sha256']);self.assertIn('J2.npy',result['artifacts']['missing'])
            self.assertIn('failure.json',result['artifacts']['sha256'])


if __name__=='__main__':unittest.main(verbosity=2)
