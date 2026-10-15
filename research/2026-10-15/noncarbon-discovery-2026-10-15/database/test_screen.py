import unittest
import screen


def row(jid, elements, **fields):
    return {'jid': f'JVASP-{jid}', 'atoms': {'elements': elements}, 'formula': ''.join(elements), **fields}


class ScreenTests(unittest.TestCase):
    def test_actual_carbon_distinct_from_calcium_cobalt_chlorine(self):
        for elements in [['Ca', 'O'], ['Co', 'O'], ['Na', 'Cl']]:
            self.assertIsNone(screen.identity(row(1, elements))[1])
        self.assertEqual(screen.identity(row(1, ['Ca', 'C', 'O']))[1], 'contains_carbon')

    def test_finite_missing_bool_and_nonfinite(self):
        for value in [None, 'na', '', float('nan'), float('inf'), False, {}, []]:
            self.assertIsNone(screen.finite(value))
        self.assertEqual(screen.finite('0'), 0.0)
        self.assertEqual(screen.finite('-2.1'), -2.1)

    def test_strata_precedence(self):
        for elements, expected in [(['Si', 'P', 'O'], 'phosphorus_oxygen'),
                                   (['Si', 'O', 'S'], 'silicon_oxygen'),
                                   (['N', 'S'], 'sulfur_no_oxygen'),
                                   (['Mg', 'N'], 'nitrogen_no_oxygen_sulfur'),
                                   (['Fe', 'O'], 'other_oxygen'), (['Na', 'Cl'], 'other')]:
            self.assertEqual(screen.stratum(elements), expected)

    def test_selection_properties_and_order_do_not_matter(self):
        data = [row(i, ['Fe', 'O'], formation_energy_peratom=i) for i in range(10)]
        first = screen.select_records(data, {'other_oxygen': 4})
        second = screen.select_records([{**r, 'formation_energy_peratom': -1000} for r in reversed(data)], {'other_oxygen': 4})
        self.assertEqual(first, second)

    def test_shortage_and_duplicate_exclusion(self):
        data = [row(i, ['Fe', 'O']) for i in range(10)] + [row(9, ['Na', 'Cl'])]
        _, chosen, excluded = screen.select_records(data, {'other': 2, 'other_oxygen': 2})
        self.assertEqual(len(chosen), 4)
        self.assertEqual(excluded['duplicate_jid'], 2)
        self.assertNotIn('JVASP-9', [r['jid'] for r in chosen])
        with self.assertRaises(ValueError):
            screen.select_records([], {'other': 1})

    def test_classification_boundaries(self):
        self.assertEqual(screen.formation_class(None), 'unknown')
        self.assertEqual(screen.formation_class(0), 'nonpositive_formation')
        self.assertEqual(screen.formation_class(0.001), 'positive_formation')
        self.assertEqual(screen.hull_class(None), 'unknown')
        self.assertEqual(screen.hull_class(-0.01), 'negative_invalid')
        self.assertEqual(screen.hull_class(0.1), 'within_screen_threshold')
        self.assertEqual(screen.hull_class(0.10001), 'above_screen_threshold')

    def test_composition_reduction(self):
        a, _ = screen.identity(row(1, ['Fe', 'Fe', 'O', 'O', 'O']))
        b, _ = screen.identity(row(2, ['Fe', 'Fe', 'O', 'O', 'O'] * 2))
        self.assertEqual(a['composition_key'], b['composition_key'])

    def test_invalid_id_elements_formula_and_elemental_records(self):
        self.assertEqual(screen.identity({'jid': 'bad'})[1], 'invalid_jid')
        self.assertEqual(screen.identity({'jid': 'JVASP-1'})[1], 'invalid_elements')
        self.assertEqual(screen.identity(row(1, ['Fe']))[1], 'elemental_not_compound')
        self.assertEqual(screen.identity(row(1, ['Fe', 'O'], formula=''))[1], 'missing_formula')


if __name__ == '__main__':
    unittest.main()
