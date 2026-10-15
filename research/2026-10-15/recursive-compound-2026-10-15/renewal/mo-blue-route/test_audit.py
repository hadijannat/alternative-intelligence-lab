import unittest
from decimal import Decimal
from audit import implied_molar_mass


class RecipeAccounting(unittest.TestCase):
    def test_consistent_synthetic_molybdate_recipe(self):
        self.assertEqual(implied_molar_mass(2, 5, 1, 1), Decimal(200))

    def test_invalid_quantities_rejected(self):
        for value in (0, -1, "NaN", "Infinity"):
            for index in range(4):
                inputs = [2, 5, 1, 1]
                inputs[index] = value
                with self.subTest(value=value, index=index), self.assertRaises(ValueError):
                    implied_molar_mass(*inputs)


if __name__ == "__main__":
    unittest.main()
