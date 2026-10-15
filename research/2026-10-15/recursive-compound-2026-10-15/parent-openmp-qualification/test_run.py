import copy
import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('qualification',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.receipts=[{'threads':t,'case':c,'returncode':0,'termination_reason':None,'monitor_error':None} for t in run.THREADS for c in run.CASES]
        self.results=[{'threads':t,'case':c,'phase':'operators','SCFs_launched':0,'status':'PASS_OPERATORS','runtime_guard_pass':True,'checks':[{'pass':True}]} for t in run.THREADS for c in run.CASES]

    def test_all_fourteen_required(self):
        self.assertTrue(run.operator_gate(self.receipts,self.results,True))
        self.assertFalse(run.operator_gate(self.receipts,self.results,False))
        for index in range(14):
            self.assertFalse(run.operator_gate(self.receipts[:index]+self.receipts[index+1:],self.results,True))
            for change in ({'case':'parent'},{'threads':2},{'SCFs_launched':1},{'phase':'scf'},{'checks':[]},{'checks':[{'pass':False}]},{'runtime_guard_pass':False},{'status':'ERROR'}):
                rows=copy.deepcopy(self.results);rows[index].update(change)
                self.assertFalse(run.operator_gate(self.receipts,rows,True))
        self.assertFalse(run.operator_gate(self.receipts,self.results[::-1],True))
        self.assertFalse(run.operator_gate(self.receipts,self.results+[self.results[0]],True))

    def test_resource_and_monitor_failure(self):
        for change in ({'returncode':1},{'termination_reason':'WALL_LIMIT'},{'termination_reason':'RSS_LIMIT'},{'monitor_error':'ps unavailable'}):
            rows=copy.deepcopy(self.receipts);rows[0].update(change)
            self.assertFalse(run.operator_gate(rows,self.results,True))

    def test_incomplete_or_wrong_type_receipt_rejected(self):
        for value in (None,[],0,'receipt'):
            self.assertFalse(run.accepted(value))
        for key in ('returncode','termination_reason','monitor_error'):
            with self.subTest(missing=key):
                rows=copy.deepcopy(self.receipts);del rows[0][key]
                self.assertFalse(run.accepted(rows[0]))
                self.assertFalse(run.operator_gate(rows,self.results,True))
        for value in (False,True,0.0,'0',None,[],{}):
            with self.subTest(returncode=value):
                rows=copy.deepcopy(self.receipts);rows[0]['returncode']=value
                self.assertFalse(run.accepted(rows[0]))
                self.assertFalse(run.operator_gate(rows,self.results,True))
        for key in ('termination_reason','monitor_error'):
            for value in (False,0,'',[],{}):
                with self.subTest(key=key,value=value):
                    rows=copy.deepcopy(self.receipts);rows[0][key]=value
                    self.assertFalse(run.accepted(rows[0]))
                    self.assertFalse(run.operator_gate(rows,self.results,True))

    def test_actual_source_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);package=root/'scipy';package.mkdir();source=package/'source.py';source.write_text('original')
            with patch.object(run.importlib,'import_module',return_value=types.SimpleNamespace(__file__=str(package/'__init__.py'))):
                pins={'/old/site-packages/scipy/source.py':run.sha(source)}
                run.source_equivalence(pins,root)
                source.write_text('changed')
                with self.assertRaisesRegex(ValueError,'Actual runtime source differs'):run.source_equivalence(pins,root)

    def test_driver_manifest_pins_only_executable_inputs(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'original_pins',return_value={}),patch.object(run,'runtime_pins',return_value={}):
            for name in ('run.py','test_run.py','PROTOCOL.md'):(run.BASE/name).write_text(name)
            frozen=run.manifest()
            (run.BASE/'FINAL_REPORT.md').write_text('post-run audit')
            self.assertEqual(run.manifest(),frozen)
            self.assertEqual({Path(p).name for p in frozen['driver']},{'run.py','test_run.py','PROTOCOL.md'})
            (run.BASE/'PROTOCOL.md').write_text('changed protocol')
            self.assertNotEqual(run.manifest(),frozen)

    def test_output_boundary(self):
        self.assertEqual(run.owned(run.BASE/'run-v1'),run.BASE/'run-v1')
        for path in (run.MO/'run-v1',run.BASE,run.BASE/'..'/'escape'):
            with self.assertRaises(ValueError):run.owned(path)

    def test_unchanged_mo_failure_writes_only_redirected_output(self):
        original_before=run.sha(run.MO/'run.py')
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            adapter=run.redirected_mo(1);out=adapter.BASE/'run-v1'/'operators-anion-water';out.mkdir(parents=True)
            self.assertEqual(adapter.CAMPAIGN,run.LAB/'rij-jkfit-qualification')
            self.assertEqual(adapter.MEMORY,run.LAB/'cpcm-rij-memory')
            fake_np=types.ModuleType('numpy');fake_np.savez_compressed=lambda p,**kw:Path(p).write_bytes(b'synthetic-no-numerical-arrays')
            fake_pyscf=types.ModuleType('pyscf');fake_pyscf.dft=object();fake_pyscf.gto=object()
            fake_scf=types.ModuleType('pyscf.scf');fake_scf.hf=object()
            fake_memory=types.SimpleNamespace(factor_inplace=lambda *a:None,private_scipy=types.SimpleNamespace(linalg=types.SimpleNamespace()))
            adapter.pinned_files=lambda:{};run.save(adapter.BASE/'run-v1/pins.json',{'force':'mismatch'})
            with patch.object(adapter,'load',return_value=fake_memory),patch.dict('sys.modules',{'numpy':fake_np,'pyscf':fake_pyscf,'pyscf.scf':fake_scf}):
                self.assertEqual(adapter.worker('anion-water','operators'),1)
            self.assertEqual(run.read(out/'result.json')['status'],'ERROR')
            self.assertTrue((out/'arrays.npz').is_file())
        self.assertEqual(run.sha(run.MO/'run.py'),original_before)

    def test_actual_thread_mismatch_stops_before_operator(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            out=Path(directory)/'run-v1/threads-4/run-v1/operators-anion-water';out.mkdir(parents=True)
            fake=types.ModuleType('pyscf');fake.lib=types.SimpleNamespace(num_threads=lambda:1)
            with patch.object(run,'unchanged',return_value=True),patch.dict('sys.modules',{'pyscf':fake}),patch.object(run,'redirected_mo',side_effect=AssertionError('must not enter operator')):
                self.assertEqual(run.worker(4,'operators','anion-water'),1)
            self.assertIn('Actual OpenMP thread setting differs',run.read(out/'result.json')['exception'])

    def test_scf_exclusive_claim_prevents_repeat(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            out=Path(directory)/'run-v1/threads-4/run-v1/scf-new-external';out.mkdir(parents=True)
            fake=types.ModuleType('pyscf');fake.lib=types.SimpleNamespace(num_threads=lambda:4)
            env={k:'1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')};env['OMP_NUM_THREADS']='4'
            calls=[]
            def small_worker(case,phase):
                calls.append((case,phase));run.save(out/'result.json',{'status':'PASS_SCF'});return 0
            adapter=types.SimpleNamespace(worker=small_worker)
            with patch.object(run,'unchanged',return_value=True),patch.dict('sys.modules',{'pyscf':fake}),patch.dict('os.environ',env),patch.object(run,'operator_records',return_value=(self.receipts,self.results)),patch.object(run,'loaded_native_files',return_value=set()),patch.object(run,'redirected_mo',return_value=adapter):
                self.assertEqual(run.worker(4,'scf','new-external'),0)
                self.assertEqual(run.worker(4,'scf','new-external'),1)
            self.assertEqual(calls,[('new-external','scf')])
            self.assertEqual(run.read(out.parents[2]/'scf-claimed.json')['maximum_SCFs'],1)

    def exercise_launch(self, fail=False, malformed_scf=False):
        calls=[]
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            root=Path(directory);run.save(root/'preparation.json',{'pins':{}})
            actual_load=run.load
            def monitored(command,out,wall,rss):
                calls.append(command);self.assertEqual((wall,rss),(180,2*2**30));out.mkdir(parents=True,exist_ok=True)
                phase,case=command[-2:];threads=int(command[-3])
                result={'threads':threads,'case':case,'phase':phase,'SCFs_launched':int(phase=='scf'),'runtime_guard_pass':True,
                        'status':'PASS_OPERATORS' if phase=='operators' else 'PASS_SCF','checks':[{'pass':not(fail and case=='WO4')}]}
                run.save(out/'result.json',result)
                if phase=='scf' and malformed_scf:return {'returncode':0}
                return {'returncode':0,'termination_reason':None,'monitor_error':None}
            supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1'},monitored_run=monitored)
            def load(name,path):return supervisor if name=='existing_supervisor' else actual_load(name,path)
            with patch.object(run,'unchanged',return_value=True),patch.object(run,'load',side_effect=load):
                self.assertEqual(run.launch(),int(fail or malformed_scf))
            self.assertEqual(len(calls),14 if fail else 15)
            self.assertEqual(sum(c[-2]=='scf' for c in calls),0 if fail else 1)
            with self.assertRaises(FileExistsError),patch.object(run,'unchanged',return_value=True):run.launch()

    def test_incomplete_scf_receipt_fails_final_result(self):self.exercise_launch(malformed_scf=True)
    def test_failure_blocks_single_scf(self):self.exercise_launch(True)
    def test_success_launches_exactly_one_small_scf(self):self.exercise_launch(False)


if __name__=='__main__':unittest.main(verbosity=2)
