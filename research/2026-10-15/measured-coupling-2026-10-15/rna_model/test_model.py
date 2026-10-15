import unittest
import numpy as np
from model import Parameters, MOIETIES, react, serial, single_cycle, exchange, initial

class ModelTests(unittest.TestCase):
    def setUp(self): self.p=Parameters(.03,1e-5,3)
    def test_reaction_stoichiometry(self):
        x=np.array([[2,1,5,.2,0,0]],float)
        for regen in [True,False]:
            y=react(x,60,self.p,regen)
            np.testing.assert_allclose(y@MOIETIES.T,x@MOIETIES.T,atol=1e-7)
            self.assertTrue(np.all(y>=0))
    def test_reporter_cannot_catalyse(self):
        x=np.array([[0,1,5,0,2,0]],float)
        np.testing.assert_allclose(react(x,60,self.p),x)
    def test_no_exchange_no_reaction(self):
        p=Parameters(.03,1e-5,3,mixing=0)
        self.assertEqual(single_cycle(p,1,3),0)
    def test_no_regeneration_seed_conservation(self):
        rows=serial(self.p,1,regeneration=False)
        for row in rows[1:]:
            g=row["generation"]
            self.assertAlmostEqual(row["F1_uM"],(1/3)*(.55**g)*(.5**(g-1)),places=8)
    def test_exchange_and_inventory(self):
        x,w=initial(1)
        y,lost=exchange(x,w,self.p,3)
        np.testing.assert_allclose(w@y,.55*(w@x),atol=1e-12)
        np.testing.assert_allclose(w@y+lost,w@x,atol=1e-12)
    def test_serial_resource_balance_and_refinement(self):
        a=serial(self.p,2);b=serial(self.p,2,rtol=1e-10)
        self.assertLess(max(r["moiety_balance_max_error_uM"] for r in a),1e-6)
        self.assertLess(max(abs(x["yield_percent"]-y["yield_percent"]) for x,y in zip(a,b)),1e-5)
        self.assertTrue(all(0<=r["yield_percent"]<=100 for r in a))
    def test_data_exact_cells(self):
        import csv
        from pathlib import Path
        import openpyxl
        root=Path(__file__).resolve().parent.parent/"rna_sources"
        wb=openpyxl.load_workbook(root/"raw/salibi_data.xlsx",data_only=True)
        with (root/"observations.csv").open() as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),148)
        for row in rows:
            self.assertEqual(float(row["value_percent"]),wb[row["source_sheet"]][row["source_cell"]].value)

if __name__=="__main__": unittest.main()
