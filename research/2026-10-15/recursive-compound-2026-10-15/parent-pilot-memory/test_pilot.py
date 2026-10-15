import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('pilot',Path(__file__).with_name('pilot.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
EVIDENCE=p.BASE/'.omo/evidence'

class PilotTests(unittest.TestCase):
    def test_allocation_and_dimensions(self):
        self.assertEqual(p.allocation(9284,3068,196,19612)['sum_bytes'],10622806400)
        for counts in [(9283,3068,196,19612),(9284,3069,196,19612),(9284,3068,195,19612),(9284,3068,196,19611)]:
            with self.assertRaises(ValueError):p.allocation(*counts)

    def test_original_57_pins(self):
        pins={str(i):'hash' for i in range(57)}
        with patch.object(p,'read',side_effect=[{'pins':pins},pins]),patch.object(p,'sha',return_value='hash'):
            self.assertEqual(p.original_pins(),pins)
        with patch.object(p,'read',return_value={'pins':{}}):
            with self.assertRaises(ValueError):p.original_pins()
        with patch.object(p,'read',side_effect=[{'pins':pins},pins]),patch.object(p,'sha',return_value='changed'):
            with self.assertRaises(ValueError):p.original_pins()

    def fixture(self):
        receipt={'returncode':0,'termination_reason':None,'monitor_error':None}
        data={'result.json':{'status':'PASS_RETROSPECTIVE_IMPLEMENTATION_EQUIVALENCE','pins_unchanged':True,'phase1_pass':True,'phase2_skipped':False,'phase2':receipt},'operator-receipts.json':[{'case':c,**receipt} for c in p.CASES],'phase1-gate.json':{'pass':True}}
        for folder,case,phase in [('operators-'+c,c,'operators') for c in p.CASES]+[('scf-new-external','new-external','scf')]:
            data[folder+'/supervisor.json']=copy.deepcopy(receipt)
            data[folder+'/result.json']={'case':case,'phase':phase,'SCFs_launched':int(phase=='scf'),'status':'PASS_SCF' if phase=='scf' else 'PASS_OPERATORS','checks':[{'pass':True}]}
        return data

    def manifest(self,data):
        with patch.object(p,'original_pins',return_value={}),patch.object(p,'read',side_effect=lambda path:data[str(path.relative_to(p.QUAL/'run-v1'))]),patch.object(p,'sha',return_value='hash'):
            return p.qualification_manifest()

    def test_six_child_gate(self):
        data=self.fixture();self.assertEqual(len(self.manifest(data)),33)
        for folder in ['operators-'+c for c in p.CASES]+['scf-new-external']:
            bad=copy.deepcopy(data);bad[folder+'/supervisor.json']['returncode']=1
            with self.assertRaises(ValueError):self.manifest(bad)
            bad=copy.deepcopy(data);bad[folder+'/result.json']['checks'][0]['pass']=False
            with self.assertRaises(ValueError):self.manifest(bad)
        for field,value in [('status','FAIL'),('pins_unchanged',False),('phase1_pass',False),('phase2_skipped',True)]:
            bad=copy.deepcopy(data);bad['result.json'][field]=value
            with self.assertRaises(ValueError):self.manifest(bad)

    def test_independent_review_gate(self):
        manifest={'terminal':'digest'};review={'status':'APPROVED_ONE_PARENT_PILOT','independent_root_review':True,'reviewer':'synthetic','preparation_sha256':'hash','qualification_artifacts':manifest}
        def run(r):
            with patch.object(p,'preparation_pins',return_value={}),patch.object(p,'qualification_manifest',return_value=manifest),patch.object(p,'sha',return_value='hash'),patch.object(p,'read',side_effect=[{'pins':{}},r]):
                return p.validate_gate()
        self.assertEqual(run(review)['qualification_artifacts'],manifest)
        for field,value in [('status','PENDING'),('independent_root_review',False),('reviewer',''),('preparation_sha256','old'),('qualification_artifacts',{})]:
            bad={**review,field:value}
            with self.assertRaises(ValueError):run(bad)

    def test_launch_refuses_existing(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(p,'BASE',Path(temp)),patch.object(p,'validate_gate',return_value={}):
            (Path(temp)/'run-v1').mkdir()
            with self.assertRaises(FileExistsError):p.launch()

    def test_supervisor_success_and_timeout(self):
        supervisor=p.load('supervisor_test',p.LAB/'parent-pilot/pilot.py')
        EVIDENCE.mkdir(parents=True,exist_ok=True)
        good=supervisor.monitored_run([sys.executable,'-c','import os,json; print(json.dumps({k:os.environ[k] for k in '+repr(list(supervisor.THREADS))+'}))'],EVIDENCE/'synthetic-success',5,100*2**20)
        self.assertTrue(p.accepted(good))
        self.assertEqual(json.loads((EVIDENCE/'synthetic-success/stdout.txt').read_text()),supervisor.THREADS)
        timeout=supervisor.monitored_run([sys.executable,'-c','import time;time.sleep(10)'],EVIDENCE/'synthetic-timeout',0.3,100*2**20)
        self.assertEqual(timeout['termination_reason'],'WALL_LIMIT');self.assertFalse(p.accepted(timeout))
        self.assertNotEqual(timeout['returncode'],0)

if __name__=='__main__':unittest.main(verbosity=2)
