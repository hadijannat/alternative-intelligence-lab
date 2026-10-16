import importlib.util
from pathlib import Path
from unittest.mock import patch
import numpy as np
from pyscf import dft, gto
from pyscf.df import addons

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('metric_v1', BASE.parent/'parent-metric-solve-diagnostic/run.py')
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
r = v1.r


def probe():
    memory = r.load('probe_frozen_memory', BASE.parent/'cpcm-rij-memory/memory.py')
    mol = gto.M(atom=r.first.parent_atoms(), unit='Angstrom', basis={e: 'def2-svp' for e in ('O', 'Mo', 'H')}, ecp={'Mo': 'def2-svp'}, charge=-8, spin=0, verbose=0, max_memory=8000)
    before = mol._env.copy()
    fresh = r.molecule_state(mol)
    mf = dft.RKS(mol)
    mf.xc = 'PBE'
    mf.grids.level = 2
    mf.direct_scf = True
    mf.direct_scf_tol = 1e-13
    solvent = memory.MemoryPCM(mol)
    solvent.method = 'C-PCM'
    solvent.eps = 78.4
    solvent.lebedev_order = 17
    solvent.vdw_scale = 1.2
    solvent.r_probe = 0.
    solvent.frozen = False
    solvent.build = r.signed.forbidden
    mf = memory.qualified.attach(mf, solvent)
    r.signed.restrict(mf)
    calls = []
    def sentinel(name, *args, **kwargs):
        calls.append(name)
        return np.zeros((1, 1))
    with patch.object(gto.moleintor, 'getints', side_effect=sentinel):
        mf = memory.install(mf)
    changed = np.flatnonzero(before != mol._env)
    expected = r.read(v1.SOURCE/'molecule-state.json')
    aux = addons.make_auxmol(mol, {e: 'def2-universal-jkfit' for e in ('O', 'Mo', 'H')})
    result = {'fresh_state': fresh, 'after_setup_state': r.molecule_state(mol), 'prior_state': expected, 'exact_prior_match': r.molecule_state(mol) == expected, 'aux_exact_prior_match': r.molecule_state(aux) == r.read(v1.SOURCE/'optimizer-baseline.json')['auxmol'], 'changed_env_slots': [{'index': int(i), 'before': float(before[i]), 'after': float(mol._env[i])} for i in changed], 'mocked_integral_calls': calls, 'native_integral_calls': 0, 'J_calls': mf._rij_calls, 'PCM_unbuilt': r.first.pcm_unbuilt(solvent), 'ecp_basis_offset': len(mol._bas), 'ecp_basis_count': len(mol._ecpbas)}
    return result


if __name__ == '__main__':
    v1.BASE = BASE
    result = probe()
    v1.write(BASE/'metadata-probe.json', result)
    print(result['changed_env_slots'])
    assert result['exact_prior_match'] and result['aux_exact_prior_match']
    assert [row['index'] for row in result['changed_env_slots']] == [18, 19]
