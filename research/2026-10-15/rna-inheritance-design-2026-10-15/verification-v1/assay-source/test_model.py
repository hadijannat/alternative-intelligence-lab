import unittest
import numpy as np
from model import calibration, observe, infer, material_budget, ratio_interval, wilson

class ObserverTests(unittest.TestCase):
    def test_material(self):
        self.assertAlmostEqual(material_budget(10)['amount_fmol'],.0005235987755982989)
    def test_marginals_not_joint(self):
        worlds=[{'founder_active':10,'new_active':0},{'founder_active':0,'new_active':10}]
        outputs=[observe({'founder':10,'new':10},{'native':sum(w.values()),'refolded':10},np.random.default_rng(17)) for w in worlds]
        self.assertEqual(outputs[0],outputs[1])
        self.assertEqual(infer(outputs[0])['new_capacity_lower']['native'],0)
    def test_positive_and_null(self):
        for active,status in [(0,'unresolved'),(1000,'detected')]:
            result=infer(observe({'founder':10,'new':1000},{'native':10+active,'refolded':10+active},np.random.default_rng(17)))
            self.assertEqual(result['status']['native'],status)
    def test_censoring(self):
        result=infer(observe({'new':.0005},{'native':.0005,'refolded':.0005},np.random.default_rng(17)))
        self.assertEqual(result['status']['native'],'unresolved')
        self.assertGreater(result['intervals']['new'][1],0)
    def test_gates_and_refolding(self):
        c=calibration(); c['label_qualified']=False
        result=infer(observe({'new':1000},{'native':1000,'refolded':1000},np.random.default_rng(17),c))
        self.assertFalse(result['qualified'])
        self.assertEqual(result['status']['native'],'unresolved')
        result=infer(observe({'new':1000},{'native':0,'refolded':1000},np.random.default_rng(17)))
        self.assertEqual(result['status'],{'native':'unresolved','refolded':'detected'})
    def test_units_and_validation(self):
        with self.assertRaises(ValueError):
            observe({'new':-1},{'native':0,'refolded':0},np.random.default_rng(17))
        self.assertIsNone(ratio_interval([1,2],[0,1]))
        self.assertLess(wilson(0,256)[1],.05)
    def test_contaminants_and_import(self):
        result=infer(observe({'new':100,'hyper':1000,'reporter':1000,'imported':100},
                             {'native':185,'refolded':185},np.random.default_rng(19)))
        self.assertEqual(result['status']['native'],'unresolved')
    def test_calibration_budget(self):
        c=calibration();c['identity_fraction']=1
        with self.assertRaises(ValueError):
            observe({},dict(native=0,refolded=0),np.random.default_rng(17),c)
    def test_inconsistent_capacity(self):
        result=infer(observe({'new':1},{'native':1000,'refolded':1000},np.random.default_rng(17)))
        self.assertEqual(result['status']['native'],'unresolved')
        self.assertIn('inconsistent capacity and identity intervals',result['mode_reasons']['native'])

if __name__=='__main__': unittest.main()
