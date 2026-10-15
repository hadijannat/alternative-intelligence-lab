import unittest
from dataclasses import replace
import numpy as np
from model import Parameters,MOIETIES,react,rates,initial,exchange,reporter,serial,single_cycle,bulk_curve

class ModelTests(unittest.TestCase):
    def setUp(self): self.p=Parameters(kf=.1,kh=.001,q=.7,hroute=1)
    def test_stoichiometry_and_nonnegative(self):
        x=np.array([[2,1,5,.2,0,0,.3]],float)
        for family in ["saturation","original"]:
            for regen in [True,False]:
                y=react(x,60,replace(self.p,family=family),regen)
                np.testing.assert_allclose(y@MOIETIES.T,x@MOIETIES.T,atol=1e-7)
                self.assertTrue(np.all(y>=0))
    def test_inactive_reporter_and_zero_b(self):
        for x in [np.array([[0,1,5,0,2,0,3]],float),np.array([[2,1,0,1,2,0,3]],float)]:
            np.testing.assert_allclose(react(x,60,self.p),x)
    def test_saturation_limit(self):
        low=np.array([[2,1,0,.2,0,0,0]],float);high=low.copy();high[0,2]=1e10
        np.testing.assert_allclose(rates(low,self.p),0)
        va,vr=rates(high,self.p)
        self.assertAlmostEqual(va[0],.1*.2*2+.001*4,places=10)
        self.assertAlmostEqual(vr[0],.1*.2+.001*2,places=10)
    def test_q_observer_reservoir(self):
        x,w=initial(1,self.p)
        self.assertAlmostEqual((w@x)[1]+(w@x)[6],2.5/3)
        saturated=np.array([[0,0,0,0,7,0,3]],float)
        self.assertEqual(reporter(saturated,np.array([1.])),70)
        self.assertLessEqual(max(bulk_curve(self.p,seed=1)),70+1e-8)
    def test_both_exchanges_and_species_loss(self):
        for mode in ["fractional","contact"]:
            p=replace(self.p,transport=mode,retention_f=.8)
            x,w=initial(2,p);y,v,lost=exchange(x,w,p,3)
            expected=w@x*.55;expected[3]=(w@x)[3]*.8
            np.testing.assert_allclose(v@y,expected,atol=1e-12)
            np.testing.assert_allclose(v@y+lost,w@x,atol=1e-12)
            self.assertAlmostEqual(v.sum(),1)
    def test_contact_limits(self):
        for mixing in [0,1]:
            p=replace(self.p,mixing=mixing)
            x,w=initial(1,p)
            a,wa,_=exchange(x,w,p,3)
            b,wb,_=exchange(x,w,replace(p,transport="contact"),3)
            self.assertAlmostEqual(reporter(react(a,60,p),wa),reporter(react(b,60,p),wb),places=7)
    def test_no_exchange_separation(self):
        for mode in ["fractional","contact"]:
            self.assertEqual(single_cycle(replace(self.p,mixing=0,transport=mode),1,3),0)
    def test_founder_and_resource_balances(self):
        for mode in ["fractional","contact"]:
            p=replace(self.p,transport=mode,retention_f=.8)
            rows=serial(p,2,regeneration=False)
            for row in rows[1:]:
                g=row["generation"]
                self.assertAlmostEqual(row["F1_uM"],2/3*.8**g*.5**(g-1),places=8)
                self.assertLess(row["moiety_balance_max_error_uM"],1e-6)
    def test_refinement_and_bounded_observer(self):
        for mode in ["fractional","contact"]:
            p=replace(self.p,transport=mode)
            a=serial(p,2);b=serial(p,2,rtol=1e-10)
            self.assertLess(max(abs(x["yield_percent"]-y["yield_percent"]) for x,y in zip(a,b)),1e-4)
            self.assertTrue(all(0<=x["yield_percent"]<=100 for x in a))
            self.assertLess(max(x["moiety_balance_max_error_uM"] for x in a),1e-6)
    def test_invalid_parameters_and_inputs(self):
        for change in [{"q":0},{"mixing":2},{"kf":-1},{"retention_f":0},{"transport":"unknown"}]:
            with self.assertRaises(ValueError): replace(self.p,**change)
        with self.assertRaises(ValueError): react(np.array([[-1]*7]),60,self.p)
        with self.assertRaises(ValueError): react(np.zeros((1,7)),60,self.p,times=[10,5])

if __name__=="__main__": unittest.main()
