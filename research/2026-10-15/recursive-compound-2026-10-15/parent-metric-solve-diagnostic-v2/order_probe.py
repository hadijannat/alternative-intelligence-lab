import itertools
import importlib.util
from pathlib import Path
from pyscf import gto
from pyscf.df import addons

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('v2', BASE/'run.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
records = []
for order in itertools.permutations(('H', 'Mo', 'O')):
    mol = gto.M(atom=d.v1.r.first.parent_atoms(), unit='Angstrom', basis={e: 'def2-svp' for e in order}, ecp={'Mo': 'def2-svp'}, charge=-8, spin=0, verbose=0)
    mol._env[18] = len(mol._bas)
    mol._env[19] = len(mol._ecpbas)
    aux = addons.make_auxmol(mol, {e: 'def2-universal-jkfit' for e in order})
    records.append({'order': list(order), 'parent_match': d.v1.r.molecule_state(mol) == d.v1.read(d.v1.SOURCE/'molecule-state.json'), 'aux_match': d.v1.r.molecule_state(aux) == d.v1.read(d.v1.SOURCE/'optimizer-baseline.json')['auxmol'], 'native_integrals': 0})
d.v1.write(BASE/'ordering-probe.json', {'permutations': records})
print(records)
