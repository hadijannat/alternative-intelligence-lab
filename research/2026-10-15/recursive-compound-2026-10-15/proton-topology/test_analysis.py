import unittest
from analysis import atom,audit,graph,compare,balance

class GeometryControls(unittest.TestCase):
    def test_exact_cutoffs(self):
        atoms=[atom('m','Mo',(0,0,0)),atom('o','O',(2.5,0,0)),atom('h','H',(3.7,0,0))]
        self.assertEqual(audit(atoms,2.5)['heavy_edges'],1)
        self.assertEqual(audit(atoms,2.4999)['heavy_edges'],0)
        # Use exactly representable offset to isolate inclusive H threshold arithmetic.
        atoms[-1]=atom('h','H',(2.5,1.2,0))
        self.assertTrue(audit(atoms,2.5)['H_assignments'][0]['assigned'])
    def test_bridging_and_terminal(self):
        a=[atom('m1','Mo',(0,0,0)),atom('m2','Mo',(4,0,0)),atom('ob','O',(2,0,0)),atom('ot','O',(-2,0,0)),atom('hb','H',(2,1,0)),atom('ht','H',(-2,1,0))]
        result=audit(a,2.5)
        self.assertEqual(result['H_bearing_bridging_like_O'],1)
        self.assertEqual(result['H_bearing_terminal_like_O'],1)
    def test_permutation_invariance_and_symmetry_ambiguity(self):
        a=[atom('m','Mo',(0,0,0)),atom('o1','O',(2,0,0)),atom('o2','O',(-2,0,0))]
        result=compare(graph(a,2.5),graph(list(reversed(a)),2.5))
        self.assertEqual(result['status'],'UNRESOLVED_MATCHING_INVARIANTS')
        self.assertIsNone(result['mapping'])
    def test_distinct_graph_negative_control(self):
        a=[atom('m','Mo',(0,0,0)),atom('o','O',(2,0,0))]
        b=[atom('m','Mo',(0,0,0)),atom('o','O',(3,0,0))]
        self.assertEqual(compare(graph(a,2.5),graph(b,2.5))['status'],'DISTINCT_CUTOFF_GRAPHS')
    def test_regular_graph_limit(self):
        atoms=[atom(str(i),'Mo' if i%2==0 else 'O',(i,0,0)) for i in range(12)]
        connected=[{(i-1)%12,(i+1)%12} for i in range(12)]
        disconnected=[{(i//6)*6+(i-1)%6,(i//6)*6+(i+1)%6} for i in range(12)]
        result=compare((atoms,connected),(atoms,disconnected))
        self.assertEqual(result['status'],'UNRESOLVED_MATCHING_INVARIANTS')
        self.assertEqual(len(result['rounds']),12)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):atom('bad','O',(float('nan'),0,0))
    def test_tied_nearest_O_not_assigned(self):
        a=[atom('m','Mo',(0,3,0)),atom('o1','O',(-1,0,0)),atom('o2','O',(1,0,0)),atom('h','H',(0,0,0))]
        self.assertEqual(audit(a,2.6)['H_unassigned'],1)
    def test_formal_balance(self):
        a,b=balance(36,16,0,112),balance(36,4,24,100)
        self.assertEqual(a,b)
        self.assertEqual(a,{'Mo':36,'O':128,'H':32,'formal_charge':-8})

if __name__=='__main__':unittest.main(verbosity=2)
