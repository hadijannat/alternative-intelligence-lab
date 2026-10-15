import copy
import unittest
from run import launch_gate


class LaunchGate(unittest.TestCase):
    def test_exact_success_and_invalid_results(self):
        receipts=[{'case':c,'returncode':0,'termination_reason':None,'monitor_error':None} for c in ('WO4','VO4')]
        results=[{'case':c,'status':'PASS_NUMERICAL_SCREEN_ONLY','SCFs_launched':2,'checks':[{'pass':True}]} for c in ('WO4','VO4')]
        self.assertTrue(launch_gate(receipts,results,True))
        for field,value in [('case','Mo'),('status','ERROR'),('SCFs_launched',1),('checks',[]),('checks',[{'pass':False}])]:
            bad=copy.deepcopy(results); bad[0][field]=value
            with self.subTest(field=field): self.assertFalse(launch_gate(receipts,bad,True))
        self.assertFalse(launch_gate(receipts,results,False))
        self.assertFalse(launch_gate(receipts,results[:1],True))
        bad=copy.deepcopy(receipts); bad[0]['returncode']=1
        self.assertFalse(launch_gate(bad,results,True))
        bad=copy.deepcopy(receipts); bad[0]['termination_reason']='WALL_LIMIT'
        self.assertFalse(launch_gate(bad,results,True))


if __name__=='__main__': unittest.main(verbosity=2)
