import unittest
from guibonds import parse

ATOMS='Atoms\n1 O 0 0 0\n2 H 0 1 0\n3 Mo 2 0 0\nEnd\n'
def source(rows):return ATOMS+'GUIBonds\n'+rows+'\nEnd\n'
class BondGuards(unittest.TestCase):
    def test_valid_orders_and_ids(self):
        atoms,bonds=parse(source('1 1 2 1.0\n2 1 3 2.0'))
        self.assertEqual(len(atoms),3);self.assertEqual(bonds[1]['declared_order'],2.)
    def test_malformed_rejected(self):
        for rows in ('1 1 9 1','1 1 1 1','1 1 2 nan','1 1 2 0','1 1 2','1 1 2 1\n2 2 1 1','1 1 2 1\n1 1 3 1'):
            with self.subTest(rows=rows),self.assertRaises(ValueError):parse(source(rows))
    def test_unterminated_block(self):
        with self.assertRaises(ValueError):parse(ATOMS+'GUIBonds\n1 1 2 1')
    def test_duplicate_atom(self):
        with self.assertRaises(ValueError):parse(source('1 1 2 1').replace('2 H','1 H'))

if __name__=='__main__':unittest.main(verbosity=2)
