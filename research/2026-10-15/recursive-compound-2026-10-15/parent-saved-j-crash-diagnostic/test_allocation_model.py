import unittest

import allocation_model as m


class AllocationModelTests(unittest.TestCase):
    def test_two_pass_shapes_and_representative_orders(self):
        ao = m.partition([1, 3, 5]*10)
        aux = m.partition([1, 3, 5, 7, 9, 11, 13]*4)
        nblock = max(len(ao), len(aux))
        self.assertEqual(m.writeback_bounds(aux, [[1]])['shape'], [196, 1])
        bounds = m.writeback_bounds(ao, ao)
        self.assertEqual(bounds['shape'], [90, 90])
        self.assertEqual(bounds['max_destination_index'], 90**2-1)
        self.assertEqual(bounds['shell_pairs_checked'], 30**2)
        for cache in m.MOCK_CACHES:
            limit = m.allocation(cache)['size_limit_doubles']
            for number, rows, cols in ((1, aux, [[1]]), (2, ao, ao)):
                forward, reverse = [m.key_simulation(rows, cols, nblock, limit, number, rev)
                                    for rev in (False, True)]
                self.assertEqual(forward['stack_doubles'], reverse['stack_doubles'])
                self.assertEqual(forward['stack_doubles'], 196 if number == 1 else 8100)
                self.assertEqual(forward['unique_keys'], reverse['unique_keys'])
                self.assertEqual(forward['unique_keys'], len(rows)*len(cols))
                self.assertFalse(forward['flush_required'])

    def test_cache_cancellation_and_negative_bound(self):
        for cache in m.MOCK_CACHES:
            a = m.allocation(cache)
            self.assertEqual(a['data_bytes'] + a['workspace_bytes'], 3_200_150_672)
            self.assertEqual(a['combined_bytes_per_thread']*4, 12_800_602_688)
        for bad in (-1, 400_000_000-13**4+1):
            with self.assertRaises(ValueError):
                m.allocation(bad)

    def test_basis_merging_sort_and_damaged_rows(self):
        self.assertEqual(m.basis_dimensions('H P\n2 1\nH S\n1 1\nH S\n1 1\n', 'H'), [2, 3])
        for text in ('H SP\n1 1 1', 'H S\n1', 'H S\n1 1\n2 1 0', 'H S\n1 0'):
            with self.assertRaises(ValueError):
                m.basis_dimensions(text, 'H')

    def test_partition_boundaries_and_damaged_sizes(self):
        self.assertEqual(m.partition([32, 32, 1, 63, 13]), [[32, 32], [1, 63], [13]])
        for dims in ([], [0], [-1], [65], [1.5]):
            with self.assertRaises(ValueError):
                m.partition(dims)

    def test_key_bounds_repeat_and_capacity_failures(self):
        stack = m.KeyStack([[32], [32]], [[64]], 2, 8192)
        self.assertEqual(stack.locate(1, 0), 0)
        self.assertEqual(stack.locate(1, 0), 0)
        self.assertEqual(stack.stack, 2048)
        for row, col in ((-1, 0), (2, 0), (0, 1)):
            with self.assertRaises(ValueError):
                stack.locate(row, col)
        limited = m.KeyStack([[64], [64]], [[64]], 2, 4096)
        limited.locate(0, 0)
        with self.assertRaisesRegex(ValueError, 'keys_cache'):
            limited.locate(1, 0)
        stack.capacity = stack.stack
        with self.assertRaisesRegex(ValueError, 'data stack'):
            stack.locate(0, 0)
        with self.assertRaises(ValueError):
            m.KeyStack([[65]], [[1]], 1, 4096)

    def test_packed_shell_intervals(self):
        bounds = m.writeback_bounds([[1, 3], [5]], [[2, 3], [1]])
        self.assertEqual(bounds['shape'], [9, 6])
        self.assertEqual(bounds['max_destination_index'], 53)
        self.assertEqual(bounds['shell_pairs_checked'], 9)

    def test_wrong_assert_is_not_buffer_overflow(self):
        for k in (1260, 5155):
            r = m.optimizer_indices(1260, 5156, 1259, 1259, k)
            self.assertFalse(r['old_assert_k_lt_nbas'])
            self.assertTrue(r['valid_aux_bound'])
            self.assertLess(r['q_aux_index'], r['q_capacity'])
            self.assertLess(r['pass1_dm_index'], r['pass1_dm_capacity'])
            self.assertLess(r['pass2_dm_index'], r['pass2_dm_capacity'])
        for k in (-1, 5156):
            with self.assertRaises(ValueError):
                m.optimizer_indices(1260, 5156, 0, 0, k)


if __name__ == '__main__':
    unittest.main()
