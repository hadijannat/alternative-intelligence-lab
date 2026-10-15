import copy
import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

spec=importlib.util.spec_from_file_location('first_j_probe',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class FirstJGuards(unittest.TestCase):
    def test_density_contract_rejects_bad_shape_dtype_cycle_and_values(self):
        density=np.eye(2,dtype=np.float64);cycle=np.array(0)
        with patch.object(run,'NAO',2):
            self.assertEqual(run.validate_density(density,cycle)['cycle'],0)
            variants=[(np.eye(3),cycle),(density.astype(np.float32),cycle),(density.astype(complex),cycle),
                      (density,np.array(1)),(density,np.array(0.)),(density,np.array(False)),(density,np.array([0]))]
            for value in (np.nan,np.inf):
                bad=density.copy();bad[0,0]=value;variants.append((bad,cycle))
            bad=density.copy();bad[0,1]=1e-5;variants.append((bad,cycle))
            for dm,c in variants:
                with self.subTest(dtype=dm.dtype,shape=dm.shape,cycle=c):
                    with self.assertRaises(ValueError):run.validate_density(dm,c)

    def test_saved_density_requires_exact_cycle_zero_metadata(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'OLD',Path(directory)),patch.object(run,'NAO',2):
            out=Path(directory)/'run-v1';out.mkdir()
            for arrays in ({'density':np.eye(2),'cycle':np.array(0)},
                           {'density':np.eye(2),'cycle':np.array(0),'mo_coeff':np.eye(2)},
                           {'density':np.eye(2)}):
                np.savez(out/'partial.npz',**arrays)
                if set(arrays)=={'density','cycle'}:
                    dm,summary=run.saved_density();self.assertEqual(summary['shape'],[2,2])
                else:
                    with self.assertRaises(ValueError):run.saved_density()

    def test_output_containment_and_duplicate_worker_claim(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            out=run.owned(Path(directory)/'run-v1');out.mkdir();run.claim_worker(out)
            self.assertEqual(run.read(out/'worker-started.json')['maximum_SCFs'],0)
            with self.assertRaises(FileExistsError):run.claim_worker(out)
            for path in (run.OLD/'run-v1',run.BASE,run.BASE/'..'/'outside'):
                with self.assertRaises(ValueError):run.owned(path)

    def test_changed_source_pin_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'input';path.write_text('fixed');pins={str(path):run.sha(path)}
            run.verify_pins(pins);path.write_text('changed')
            with self.assertRaises(ValueError):run.verify_pins(pins)

    def test_one_j_route_rejects_scf_pcm_and_repeat(self):
        dm=np.eye(2);calls=[]
        mf=types.SimpleNamespace(_rij_calls=0,with_solvent=types.SimpleNamespace())
        def get_j(dm):calls.append(dm);mf._rij_calls+=1;return dm*2
        mf.get_j=get_j
        np.testing.assert_array_equal(run.single_j(mf,dm),dm*2)
        self.assertEqual(len(calls),1)
        for function in (mf.kernel,mf.scf,mf.with_solvent.build):
            with self.assertRaises(RuntimeError):function()
        with self.assertRaises(ValueError):run.single_j(mf,dm)
        self.assertEqual(len(calls),1)

    def qualification_fixture(self,root):
        root.mkdir();out=root/'run-v1';out.mkdir();receipts=[];results=[]
        run.save(root/'preparation.json',{'synthetic':True})
        for threads in (1,4):
            for case in run.qualification.CASES:
                folder=out/f'threads-{threads}'/'run-v1'/('operators-'+case);folder.mkdir(parents=True)
                supervisor={'returncode':0,'termination_reason':None,'monitor_error':None}
                result={'case':case,'threads':threads,'phase':'operators','SCFs_launched':0,'runtime_guard_pass':True,'status':'PASS_OPERATORS','checks':[{'pass':True}]}
                receipts.append({'threads':threads,'case':case,**supervisor});results.append(result)
                for name,value in (('result.json',result),('supervisor.json',supervisor)):run.save(folder/name,value)
                for name in ('arrays.npz','runtime-observation.json','native.log'):(folder/name).write_text('synthetic')
        folder=out/'threads-4/run-v1/scf-new-external';folder.mkdir()
        result={'case':'new-external','threads':4,'phase':'scf','SCFs_launched':1,'runtime_guard_pass':True,'status':'PASS_SCF','checks':[{'pass':True}]}
        for name,value in (('result.json',result),('supervisor.json',supervisor)):run.save(folder/name,value)
        for name in ('arrays.npz','runtime-observation.json','native.log'):(folder/name).write_text('synthetic')
        run.save(out/'result.json',{'status':'PASS_RETROSPECTIVE_RUNTIME_EQUIVALENCE','phase1_pass':True,'pins_unchanged':True,'phase2_skipped':False,'phase2':supervisor})
        run.save(out/'operator-receipts.json',receipts);run.save(out/'phase1-gate.json',{'pass':True})
        run.save(out/'scf-claimed.json',{'maximum_SCFs':1,'case':'new-external','threads':4})
        return receipts,results

    def test_terminal_qualification_and_all_child_receipts_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'qualification';receipts,results=self.qualification_fixture(root)
            with patch.object(run,'QUAL',root),patch.object(run.qualification,'unchanged',return_value=True),patch.object(run.qualification,'operator_records',return_value=(receipts,results)):
                self.assertEqual(len(run.qualification_artifacts()),80)
                for key in ('returncode','termination_reason','monitor_error'):
                    receipt=receipts[0].pop(key)
                    with self.assertRaises(ValueError):run.qualification_artifacts()
                    receipts[0][key]=receipt
                results[-1]['checks'][0]['pass']=False
                with self.assertRaises(ValueError):run.qualification_artifacts()
                results[-1]['checks'][0]['pass']=True
                path=root/'run-v1/threads-4/run-v1/scf-new-external/supervisor.json';original=run.read(path)
                run.save(path,{'returncode':0})
                with self.assertRaises(ValueError):run.qualification_artifacts()
                run.save(path,original)
                final=root/'run-v1/result.json';record=run.read(final);record['status']='FAIL';run.save(final,record)
                with self.assertRaises(ValueError):run.qualification_artifacts()

    def test_failed_qualification_blocks_prepare_before_parent_load(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'qualification_artifacts',side_effect=ValueError('qualification incomplete')),patch.object(run,'saved_density',side_effect=AssertionError('No parent density load')),patch.object(run,'parent_atoms',side_effect=AssertionError('No parent geometry')):
            with self.assertRaisesRegex(ValueError,'qualification incomplete'):run.prepare()
            self.assertFalse((Path(directory)/'preparation.json').exists())

    def test_review_binds_preparation_and_terminal_artifacts(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            pins={'qualification':{'terminal':'digest'},'parent':{},'driver':{}}
            run.save(run.BASE/'preparation.json',{'pins':pins})
            review={'status':'APPROVED_ONE_PARENT_FIRST_J_PROBE','independent_root_review':True,'reviewer':'synthetic-root',
                    'preparation_sha256':run.sha(run.BASE/'preparation.json'),'qualification_artifacts':pins['qualification']}
            with patch.object(run,'manifest',return_value=pins):
                run.save(run.BASE/'independent-root-review.json',review);self.assertIn('review_sha256',run.validate_gate())
                for change in ({'status':'pending'},{'independent_root_review':False},{'reviewer':''},{'preparation_sha256':'changed'},{'qualification_artifacts':{}}):
                    run.save(run.BASE/'independent-root-review.json',{**review,**change})
                    with self.assertRaises(ValueError):run.validate_gate()

    def exercise_launch(self,receipt=None,corrupt_j=False,gate_changes=False,result_failure=None,j_hash_error=False):
        calls=[];receipt=receipt if receipt is not None else {'returncode':0,'termination_reason':None,'monitor_error':None}
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            original_sha=run.sha
            def monitored(command,out,wall,rss):
                calls.append(command);self.assertEqual((wall,rss),(300,10*2**30))
                (out/'J.npy').write_bytes(b'synthetic-J')
                run.save(out/'result.json',{'status':'PASS_BOUNDED_FIRST_J_ONLY','checks':{'synthetic':True},'J_calls':1,'SCFs_launched':0,'J_sha256':'bad' if corrupt_j else original_sha(out/'J.npy')})
                if result_failure=='truncated':(out/'result.json').write_text('{\"status\":')
                if result_failure=='nonobject':run.save(out/'result.json',[])
                if result_failure=='checks_type':
                    result=run.read(out/'result.json');result['checks']=[True];run.save(out/'result.json',result)
                (out/'stages.jsonl').write_text('synthetic stage remains\n')
                return receipt
            supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'},monitored_run=monitored)
            original_read=run.read
            def read(path):
                if result_failure=='unreadable' and Path(path).resolve()==(run.BASE/'run-v1/result.json').resolve():raise PermissionError('synthetic unreadable worker result')
                return {'pins':{'runtime':{'python':'/synthetic/python'}}} if Path(path)==run.QUAL/'preparation.json' else original_read(path)
            def sha(path):
                if j_hash_error and Path(path).resolve()==(run.BASE/'run-v1/J.npy').resolve():raise OSError('synthetic J hash read failure')
                return original_sha(path)
            with patch.object(run,'validate_gate',side_effect=[{'review':'fixed'},{'review':'changed' if gate_changes else 'fixed'}]),patch.object(run,'load',return_value=supervisor),patch.object(run,'read',side_effect=read),patch.object(run,'sha',side_effect=sha):
                expected=bool(not run.accepted(receipt) or corrupt_j or gate_changes or result_failure or j_hash_error)
                self.assertEqual(run.launch(),int(expected))
            terminal=original_read(run.BASE/'run-v1/launch-result.json')
            self.assertEqual(terminal['receipt'],receipt)
            self.assertTrue((run.BASE/'run-v1/stages.jsonl').is_file())
            if result_failure in ('truncated','unreadable','nonobject'):self.assertTrue(terminal['worker_result_error'])
            if j_hash_error:self.assertIn('synthetic J hash read failure',terminal['J_hash_error'])
            self.assertEqual(len(calls),1);self.assertEqual(calls[0][-1],'--worker');self.assertEqual(supervisor.THREADS['OMP_NUM_THREADS'],'4')
            with patch.object(run,'validate_gate',return_value={'review':'fixed'}):
                with self.assertRaises(FileExistsError):run.launch()

    def test_interrupted_or_unreadable_result_preserves_terminal_receipt(self):
        for failure in ('truncated','unreadable','nonobject','checks_type'):
            self.exercise_launch(result_failure=failure)
        self.exercise_launch(receipt={'returncode':-15,'termination_reason':'WALL_LIMIT','monitor_error':None},result_failure='truncated')

    def test_J_hash_read_failure_preserves_terminal_receipt(self):self.exercise_launch(j_hash_error=True)

    def test_one_bounded_child_launch(self):self.exercise_launch()
    def test_resource_and_malformed_receipts_fail(self):
        for receipt in ({'returncode':0},{'returncode':False,'termination_reason':None,'monitor_error':None},
                        {'returncode':-15,'termination_reason':'WALL_LIMIT','monitor_error':None},
                        {'returncode':-15,'termination_reason':'RSS_LIMIT','monitor_error':None}):
            self.exercise_launch(receipt)
    def test_corrupted_J_or_changed_gate_fails(self):
        self.exercise_launch(corrupt_j=True);self.exercise_launch(gate_changes=True)


if __name__=='__main__':unittest.main(verbosity=2)
