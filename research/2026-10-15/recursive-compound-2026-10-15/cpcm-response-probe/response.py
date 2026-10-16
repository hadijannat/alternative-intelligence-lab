import importlib.util
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location(
    'response_memory', Path(__file__).resolve().parent.parent / 'cpcm-rij-memory/memory.py')
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


def density_response(solvent, delta):
    """Return -G.T f S^-1 G delta without nuclear offsets or cache writes."""
    if type(solvent) is not memory.MemoryPCM:
        raise TypeError('Expected the source-pinned MemoryPCM object')
    solvent._guard()
    if (not isinstance(delta, np.ndarray) or delta.dtype.kind not in 'fi' or
            delta.shape != (solvent.mol.nao, solvent.mol.nao) or
            not np.isfinite(delta).all() or not np.array_equal(delta, delta.T)):
        raise ValueError('Expected finite real exactly symmetric AO density perturbation')
    if not solvent._intermediates or 'factor' not in solvent._intermediates:
        raise ValueError('Build the fixed-geometry solvent before requesting response')
    if solvent.eps == 1:
        return np.zeros(delta.shape, dtype=float)
    f = 1.0 if np.isinf(solvent.eps) else (solvent.eps - 1) / solvent.eps
    charges = memory.solve_checked(
        solvent._intermediates['factor'], f * solvent._contract(density=delta))
    return solvent._contract(charges=charges)
