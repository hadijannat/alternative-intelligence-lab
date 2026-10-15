import unittest
from unittest.mock import patch
import run

class FrozenGate(unittest.TestCase):
    def setUp(self):
        self.receipts=[{'case':c,'returncode':0,'termination_reason':None,'monitor_error':None} for c in run.CASES]
        self.results=[{'case':c,'phase':'operators','status':'PASS_OPERATORS','checks':[{'pass':True}]} for c in run.CASES]
    def test_all_five_required(self):
        self.assertTrue(run.phase1_gate(self.receipts,self.results,True))
        self.assertFalse(run.phase1_gate(self.receipts[:-1],self.results[:-1],True))
        self.assertFalse(run.phase1_gate(self.receipts[::-1],self.results,True))
    def test_wrong_case_or_phase_blocks_SCF(self):
        self.assertFalse(run.phase1_gate(self.receipts,self.results[::-1],True))
        self.results[-1]['phase']='scf'
        self.assertFalse(run.phase1_gate(self.receipts,self.results,True))

    def test_comparison_failure_blocks_SCF(self):
        self.results[2]['checks'][0]['pass']=False
        self.assertFalse(run.phase1_gate(self.receipts,self.results,True))
    def test_bad_receipt_or_hash_blocks_SCF(self):
        self.assertFalse(run.phase1_gate(self.receipts,self.results,False))
        for field,value in [('returncode',1),('termination_reason','WALL_LIMIT'),('termination_reason','RSS_LIMIT'),('monitor_error','ps failure')]:
            changed=[dict(x) for x in self.receipts];changed[0][field]=value
            with self.subTest(field=field,value=value):self.assertFalse(run.phase1_gate(changed,self.results,True))
    def test_missing_or_error_result_blocks_SCF(self):
        for value in ({},{'case':'new-external','phase':'operators','status':'ERROR','checks':[{'pass':True}]},{'case':'new-external','phase':'operators','status':'PASS_OPERATORS','checks':[]}):
            results=self.results.copy();results[-1]=value
            with self.subTest(value=value):self.assertFalse(run.phase1_gate(self.receipts,results,True))
    def test_phase2_needs_exact_case_status_checks_and_receipt(self):
        receipt=self.receipts[-1]
        result={'case':'new-external','phase':'scf','SCFs_launched':1,'status':'PASS_SCF','checks':[{'pass':True}]}
        self.assertTrue(run.phase2_accepted(receipt,result,True))
        for changed in ({'case':'anion-water'},{'phase':'operators'},{'SCFs_launched':0},{'status':'ERROR'},{'checks':[]},{'checks':[{'pass':False}]}):
            with self.subTest(changed=changed):self.assertFalse(run.phase2_accepted(receipt,{**result,**changed},True))
        self.assertFalse(run.phase2_accepted(None,result,True))
        self.assertFalse(run.phase2_accepted({**receipt,'termination_reason':'RSS_LIMIT'},result,True))
        self.assertFalse(run.phase2_accepted(receipt,result,False))

    def test_saved_sources_without_operator_or_SCF(self):
        from pyscf.scf import hf
        from pyscf.df import df_jk
        with patch.object(hf.SCF,'kernel',side_effect=AssertionError('No SCF')),patch.object(df_jk,'get_j',side_effect=AssertionError('No J')):
            result=run.validate_sources()
        self.assertEqual(result['cases'],list(run.CASES));self.assertEqual(result['densities_per_case'],4)
        self.assertEqual(result['SCFs_launched'],0)

if __name__=='__main__':unittest.main(verbosity=2)
