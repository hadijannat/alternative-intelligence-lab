"""Source-only integer model; never import PySCF or evaluate an integral."""
import hashlib
import json
from collections import Counter
from decimal import Decimal
from itertools import accumulate
from pathlib import Path

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
SOURCE = LAB / 'parent-openmp/env-aligned/lib/python3.12/site-packages/pyscf'
MOCK_CACHES = (0, 10_000, 1_000_000)
SOURCE_PINS = {
    'lib/vhf/nr_direct.c': '9c181daa8ce689e312e548694f47a2935105094fab1e685e82b4bf485e0639c4',
    'lib/vhf/nr_direct_dot.c': '3db439ca3438b8291ac3510e463d8b8cb7c7ba66d8e95f305161843819745fc8',
    'lib/vhf/optimizer.c': 'bc2c1890058633ab06efe4f421e740562fe7a668dae6d6e0d42e7da7a7a4200b',
    'lib/vhf/nr_direct.h': 'df7f96a170594e1d180a44cf2f0b1b5d1b00bbadd01e3ef288c23ecc15149a8f',
    'df/df_jk.py': '7f4e8c3a930b8f55d1656b0bd6d24dcca7fe365ba5de00cfcebcebf813347cee',
    'gto/basis/parse_nwchem.py': '7725ce63ecd726a931c1ba6a978a6e8af3a2cdbe706957c6e529023f56441ad5',
    'gto/mole.py': '005bd63c5fa100a20cc264a995c38f44f2e05c7c82d37bd36eba2355dc651392',
    'scf/jk.py': '5451b70070ac813d9b9b2bdb56a13b9ee26c05c74c0bae8f72c3a6fe404f0898',
    'gto/basis/def2-svp.dat': 'cfc231fc4beffff33760af4bbd0cfaae5bf49abf0195b3d293dc05aecdff7f04',
    'gto/basis/def2-universal-jkfit.dat': '8970edf068a6010954535eb2b1ee978900dbea989b20e305c730dabb0298de5a',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def basis_dimensions(text, element):
    shells = []
    current = None
    for raw in text.splitlines():
        words = raw.split('#', 1)[0].split()
        if not words:
            continue
        if words[0].upper() == 'ECP':
            break
        if words[0][0].isalpha():
            current = None
            if words[0] == element:
                require(len(words) == 2 and len(words[1]) == 1 and words[1] in 'SPDFGHI', 'Unsupported shell header')
                current = ['SPDFGHI'.index(words[1]), []]
                shells.append(current)
        elif current is not None:
            row = tuple(Decimal(x.replace('D', 'E')) for x in words)
            require(len(row) >= 2, 'Missing contraction coefficients')
            current[1].append(row)
    require(shells, 'Element not found')
    grouped = {}
    for angular, rows in shells:
        require(rows and len({len(r) for r in rows}) == 1, 'Damaged primitive rows')
        # optimize_contraction merges before remove_zero; these pinned files have no all-zero rows.
        require(all(any(r[1:]) for r in rows), 'Unsupported all-zero primitive')
        key = angular, tuple(r[0] for r in rows)
        grouped[key] = grouped.get(key, 0) + len(rows[0]) - 1
    return [(2 * key[0] + 1) * grouped[key] for key in sorted(grouped, key=lambda k: k[0])]


def partition(dimensions):
    require(dimensions and all(type(d) is int and 0 < d <= 64 for d in dimensions),
            'Invalid shell dimensions')
    loc = [0, *accumulate(dimensions)]
    starts = [0]
    last = 0
    for shell in range(1, len(dimensions)):
        if loc[shell + 1] - last > 64:
            starts.append(shell)
            last = loc[shell]
    starts.append(len(dimensions))
    return [dimensions[a:b] for a, b in zip(starts, starts[1:])]


def allocation(cache, d=13):
    require(type(cache) is int and cache >= 0 and type(d) is int and d > 0, 'Invalid cache/dimension')
    size_limit = 400_000_000 - d**4 - cache
    require(size_limit >= 0, 'Native negative-size-limit exit condition')
    return {'mock_cache_doubles': cache, 'size_limit_doubles': size_limit,
            'data_bytes': 8 * (size_limit + 136**2),
            'workspace_bytes': 8 * (d**4 + 2*d*d + cache),
            'keys_capacity': size_limit // 64**2,
            'combined_bytes_per_thread': 8 * (400_000_000 + 136**2 + 2*d*d)}


class KeyStack:
    def __init__(self, rows, cols, nblock, size_limit):
        require(nblock >= max(len(rows), len(cols)) and size_limit >= 0, 'Invalid allocation shape')
        require(all(0 < sum(b) <= 64 for b in rows + cols), 'Damaged output block')
        self.rows, self.cols, self.nblock = rows, cols, nblock
        self.capacity = size_limit + 136**2
        self.keys_capacity = size_limit // 64**2
        self.offsets = {}
        self.stack = 0

    def locate(self, row, col):
        require(0 <= row < len(self.rows) and 0 <= col < len(self.cols), 'Invalid output block key')
        key = row * self.nblock + col
        require(key < self.nblock**2, 'outptr overflow')
        if key not in self.offsets:
            extent = sum(self.rows[row]) * sum(self.cols[col])
            require(len(self.offsets) < self.keys_capacity, 'keys_cache overflow')
            require(self.stack + extent <= self.capacity, 'data stack overflow')
            self.offsets[key] = self.stack
            self.stack += extent
        return self.offsets[key]


def writeback_bounds(rows, cols):
    nrow, ncol = sum(map(sum, rows)), sum(map(sum, cols))
    checked, max_destination, max_local = 0, -1, -1
    row_start = 0
    for rb in rows:
        col_start = 0
        for cb in cols:
            width = sum(cb)
            intervals = []
            i0 = 0
            for di in rb:
                j0 = 0
                for dj in cb:
                    begin = i0 * width + j0 * di
                    end = begin + di*dj
                    require(0 <= begin < end <= sum(rb)*width, 'LOCATE/writeback local overflow')
                    destination = (row_start+i0+di-1)*ncol + col_start+j0+dj-1
                    require(0 <= destination < nrow*ncol, 'writeback destination overflow')
                    intervals.append((begin, end))
                    max_destination = max(max_destination, destination)
                    max_local = max(max_local, end-1)
                    checked += 1
                    j0 += dj
                i0 += di
            end = 0
            for begin, next_end in sorted(intervals):
                require(begin == end, 'Packed intervals overlap or leave a gap')
                end = next_end
            require(end == sum(rb)*width, 'Incomplete packed block')
            col_start += width
        row_start += sum(rb)
    return {'shape': [nrow, ncol], 'output_doubles': nrow*ncol,
            'shell_pairs_checked': checked, 'max_destination_index': max_destination,
            'max_block_local_index': max_local, 'packed_intervals_exactly_tile_each_block': True}


def key_simulation(rows, cols, nblock, size_limit, pass_number, reverse=False):
    model = KeyStack(rows, cols, nblock, size_limit)
    if pass_number == 1:
        order = [(k, 0) for k in range(len(rows))]
    else:
        # s2ij enumerates i>=j; the lk_s2ij operator delegates to lk_s1ij and writes both.
        order = [(r, c) for j in range(len(rows)) for i in range(j, len(rows))
                 for r, c in ((i, j), (j, i))]
    if reverse:
        order.reverse()
    for row, col in order:
        model.locate(row, col)
    before = model.stack
    for row, col in order:
        model.locate(row, col)
    require(model.stack == before, 'Repeated LOCATE consumed stack')
    require(len(model.offsets) == len(rows)*len(cols), 'Incomplete output key coverage')
    require(model.stack < size_limit, 'Unexpected flush needed; schedule model must be extended')
    return {'order': 'reverse' if reverse else 'forward', 'unique_keys': len(model.offsets),
            'max_key': max(model.offsets), 'outptr_capacity': nblock**2,
            'keys_capacity': model.keys_capacity, 'stack_doubles': model.stack,
            'data_capacity_doubles': model.capacity, 'flush_required': False,
            'duplicate_locate_stack_unchanged': True}


def optimizer_indices(nbas, naux, i, j, k):
    require(nbas > 0 and naux > 0 and 0 <= i < nbas and 0 <= j < nbas and 0 <= k < naux,
            'Invalid optimizer shell index')
    return {'old_assert_k_lt_nbas': k < nbas, 'valid_aux_bound': k < naux,
            'q_ij_index': i*nbas+j, 'q_aux_index': nbas**2+k,
            'q_capacity': nbas**2+naux, 'pass1_dm_index': j*nbas+i,
            'pass1_dm_capacity': nbas**2, 'pass2_dm_index': k, 'pass2_dm_capacity': naux}


def guard_paths():
    pilot = LAB / 'parent-saved-j-pilot'
    paths = [SOURCE/name for name in SOURCE_PINS]
    paths += [LAB/'parent-inputs/P0_A.xyz', LAB/'parent-openmp-first-j-v2/run.py',
              Path(__file__), BASE/'test_allocation_model.py']
    paths += [pilot/name for name in ('run.py', 'test_run.py', 'PROTOCOL.md', 'preparation.json',
                                     'independent-root-review.json')]
    paths += sorted(p for p in (pilot/'run-v1').rglob('*') if p.is_file())
    require(all(p.is_file() for p in paths), 'Missing guarded input')
    return paths


def make_audit():
    before = {str(p.relative_to(LAB.parent)): digest(p) for p in guard_paths()}
    for name, expected in SOURCE_PINS.items():
        require(digest(SOURCE/name) == expected, 'Accompanying source changed: '+name)
    xyz = (LAB/'parent-inputs/P0_A.xyz').read_text().splitlines()
    atoms = [line.split()[0] for line in xyz[2:] if line.strip()]
    require(len(atoms) == int(xyz[0]) == 196 and Counter(atoms) == {'Mo': 36, 'O': 128, 'H': 32},
            'Wrong parent composition')
    basis = {}
    shellsets = []
    for name in ('def2-svp', 'def2-universal-jkfit'):
        text = (SOURCE/f'gto/basis/{name}.dat').read_text()
        by_element = {e: basis_dimensions(text, e) for e in ('H', 'O', 'Mo')}
        dims = [d for element in atoms for d in by_element[element]]
        basis[name] = {'shell_dimensions_by_element': by_element, 'shells': len(dims),
                       'spherical_aos': sum(dims), 'maximum_shell_dimension': max(dims)}
        shellsets.append(dims)
    ao, aux = shellsets
    require((len(ao), sum(ao), len(aux), sum(aux), max(ao+aux)) == (1260, 3068, 5156, 19612, 13),
            'Source-derived parent dimensions differ')
    ao_blocks, aux_blocks = partition(ao), partition(aux)
    nblock = max(len(ao_blocks), len(aux_blocks))
    scenarios = []
    for cache in MOCK_CACHES:
        alloc = allocation(cache, max(ao+aux))
        alloc['outptr_bytes_per_thread'] = 4*nblock**2
        alloc['keys_cache_bytes_per_thread'] = 4*alloc['keys_capacity']
        alloc['excluding_JKArray_struct_bytes_per_thread'] = (
            alloc['combined_bytes_per_thread'] + alloc['outptr_bytes_per_thread'] + alloc['keys_cache_bytes_per_thread'])
        passes = []
        for number, rows, cols in ((1, aux_blocks, [[1]]), (2, ao_blocks, ao_blocks)):
            passes.append({'pass': number, 'contraction': 'ji->kl' if number == 1 else 'lk->s2ij',
                           'orders': [key_simulation(rows, cols, nblock, alloc['size_limit_doubles'], number, rev)
                                      for rev in (False, True)]})
        scenarios.append({'allocation': alloc, 'passes': passes})
    negative_cache = 400_000_000 - 13**4 + 1
    try:
        allocation(negative_cache)
    except ValueError:
        negative_rejected = True
    else:
        negative_rejected = False
    require(negative_rejected, 'Negative size limit not rejected')
    writeback = {'pass1': writeback_bounds(aux_blocks, [[1]]),
                 'pass2': writeback_bounds(ao_blocks, ao_blocks)}
    after = {str(p.relative_to(LAB.parent)): digest(p) for p in guard_paths()}
    require(before == after, 'Guarded input changed during source-only analysis')
    return {'status': 'PASS_SOURCE_ONLY_INTEGER_MODEL',
            'evidence_boundary': 'Current hashed accompanying C sources; exact compiled-source equivalence unproven. No native validation, allocation, integral, SCF, RSS measurement or crash-cause inference.',
            'assumptions': {'n_dm': 1, 'ncomp': 1, 'OMP_threads': 4, 'sizeof_double': 8,
                            'sizeof_int': 4, 'cache_values': 'Predeclared mocks, not measured native cache sizes'},
            'coverage': 'All unique output block keys and all output shell-pair writeback intervals; forward/reverse representative insertion orders with repeats. No integral quartets enumerated. Entire output fits below every mocked size_limit, so any worker subset/reordering also fits without flush. Does not model other cache sizes, native scheduling, allocation success, operator values, libcint writes, use-after-free or concurrency.',
            'source_anchors': ['nr_direct.c:233-266,322-347,377-481', 'nr_direct_dot.c:67-120,178-197,395-488',
                               'optimizer.c:303-371', 'df/df_jk.py:420-502', 'gto/basis/parse_nwchem.py:108-154,215-254'],
            'basis': basis, 'atom_order': atoms,
            'partitions': {'AO_BLOCK_SIZE': 64, 'ao_blocks': list(map(sum, ao_blocks)),
                           'aux_blocks': list(map(sum, aux_blocks)), 'nblock_max': nblock},
            'writeback': writeback,
            'mock_scenarios': scenarios, 'negative_size_limit_control': {'mock_cache': negative_cache, 'rejected': negative_rejected},
            'allocation_observation': {'combined_bytes_per_thread_before_bookkeeping': allocation(0)['combined_bytes_per_thread'],
                                       'OMP4_bytes_before_bookkeeping': 4*allocation(0)['combined_bytes_per_thread'],
                                       'four_GiB_is_conservative_allocated_virtual_bound': False,
                                       'is_RSS_measurement_or_crash_cause': False},
            'optimizer_boundary': [optimizer_indices(len(ao), len(aux), len(ao)-1, len(ao)-1, k)
                                   for k in (0, len(ao)-1, len(ao), len(aux)-1)],
            'optimizer_observation': 'k<nbas rejects legal auxiliary-shell indices 1260..5155; real q_cond and pass2 dm_cond capacities cover these indices. No out-of-bounds access established here.',
            'guard': {'before': before, 'after': after, 'unchanged': before == after},
            'source_pins': SOURCE_PINS}


if __name__ == '__main__':
    audit = make_audit()
    with (BASE/'allocation-audit.json').open('x') as stream:
        json.dump(audit, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': audit['status'], 'guard_unchanged': audit['guard']['unchanged'],
                      'artifact': str(BASE/'allocation-audit.json')}))
