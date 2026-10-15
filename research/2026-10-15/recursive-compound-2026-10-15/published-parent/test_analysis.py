import unittest
import xml.etree.ElementTree as ET
from analysis import atoms_from_molecule,array_values,frequencies,NS

class ParserGuards(unittest.TestCase):
    def test_malformed_xml(self):
        with self.assertRaises(ET.ParseError):ET.fromstring('<molecule>')
    def test_atom_count(self):
        m=ET.fromstring('<molecule xmlns="http://www.xml-cml.org/schema"><atomArray><atom id="a1" elementType="H" x3="0" y3="0" z3="0"/></atomArray></molecule>')
        with self.assertRaises(ValueError):atoms_from_molecule(m,2)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):array_values(ET.fromstring('<array size="1">nan</array>'))
    def test_declared_array_size(self):
        with self.assertRaises(ValueError):array_values(ET.fromstring('<array size="2">1</array>'))
    def test_incomplete_frequency_scope(self):
        r=ET.fromstring('<module><array dictRef="cc:frequency" units="nonsi:cm-1" size="2">-1 3</array></module>')
        f=frequencies(r,3)
        self.assertFalse(f['records'][0]['full_3N_minus6_count'])
        self.assertEqual(f['reconciliation']['status'],'UNRESOLVED')
    def test_missing_scanfreq_pair(self):
        r=ET.fromstring('<module xmlns:cmlx="http://www.xml-cml.org/schema/cmlx"><list cmlx:templateRef="scanfreq"/></module>')
        with self.assertRaises(ValueError):frequencies(r,3)

if __name__=='__main__':unittest.main(verbosity=2)
