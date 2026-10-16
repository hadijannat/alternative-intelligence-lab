import importlib.util
from pathlib import Path
import sys
import traceback
from unittest.mock import patch

BASE = Path(__file__).resolve().parent
V1 = BASE.parent/'parent-metric-solve-diagnostic'
spec = importlib.util.spec_from_file_location('frozen_metric_v1', V1/'run.py')
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
v1.BASE = BASE
original_manifest = v1.manifest


def manifest():
    result = original_manifest()
    paths = [V1/n for n in ('run.py', 'test_run.py', 'PROTOCOL.md', 'preparation.json', 'qualification.json', 'independent-root-review.json')]
    paths += [p for p in sorted((V1/'run-v1').iterdir()) if p.is_file()]
    paths += [BASE/n for n in ('probe.py', 'metadata-probe.json', 'order_probe.py', 'ordering-probe.json', 'qualification-failed-v1.json')]
    result['v1_failure_and_v2_probe'] = {str(p): v1.sha(p) for p in paths}
    return result


v1.manifest = manifest


def initialize_ecp_metadata(mol):
    from pyscf.gto.mole import AS_ECPBAS_OFFSET, AS_NECPBAS
    v1.require((AS_ECPBAS_OFFSET, AS_NECPBAS) == (18, 19), 'ECP slots changed')
    v1.require(mol._env[18] == mol._env[19] == 0, 'Expected fresh parent ECP metadata')
    mol._env[AS_ECPBAS_OFFSET] = len(mol._bas)
    mol._env[AS_NECPBAS] = len(mol._ecpbas)
    v1.r.molecule_state(mol, v1.read(v1.SOURCE/'molecule-state.json'))
    return mol


def worker():
    from pyscf import gto
    from pyscf.df import addons
    original = gto.M
    original_aux = addons.make_auxmol
    calls = []
    def factory(*args, **kwargs):
        v1.require(not calls, 'Only one parent construction allowed')
        calls.append(True)
        v1.require(kwargs['basis'] == 'def2-svp', 'Unexpected parent basis')
        kwargs['basis'] = {e: 'def2-svp' for e in ('O', 'Mo', 'H')}
        return initialize_ecp_metadata(original(*args, **kwargs))
    def auxiliary(mol, basis):
        v1.require(basis == 'def2-universal-jkfit', 'Unexpected auxiliary basis')
        return original_aux(mol, {e: basis for e in ('O', 'Mo', 'H')})
    with patch.object(gto, 'M', side_effect=factory), patch.object(addons, 'make_auxmol', side_effect=auxiliary):
        v1.worker()
    v1.require(len(calls) == 1, 'Missing parent construction')


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']: v1.prepare()
    elif sys.argv[1:] == ['--gate-check']: print(v1.gate())
    elif sys.argv[1:] == ['--launch']: sys.exit(v1.launch())
    elif sys.argv[1:] == ['--worker']:
        try: worker()
        except Exception:
            v1.write(BASE/'run-v1/failure.json', {'exception': traceback.format_exc(), 'physical_admission': False})
            raise
    else: raise SystemExit('Use --prepare, --gate-check or --launch')
