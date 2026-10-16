import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import traceback

BASE = Path(__file__).resolve().parent
LAB = BASE.parent
GEOMETRY = LAB / 'identity/next-step/method-qualification/result.json'
DENSITY = LAB / 'cpcm-blocked/evidence/anion-water.npz'
RUN = BASE / 'run-v1'
INTERPRETER = LAB / 'parent-openmp/env-aligned/bin/python'


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pins():
    import pyscf
    from pyscf.solvent import pcm, _attach_solvent
    import response
    if Path(sys.executable).resolve() != INTERPRETER.resolve():
        raise ValueError('Require qualified env-aligned interpreter')
    native = read(LAB / 'cpcm-rij-memory/source_pins.json')
    for name, expected in native.items():
        if sha(name) != expected:
            raise ValueError('Changed memory source: ' + name)
    paths = list(native) + [GEOMETRY, DENSITY, BASE/'response.py', BASE/'run.py',
        BASE/'test_response.py', BASE/'PROTOCOL.md', LAB/'cpcm-rij-memory/memory.py',
        LAB/'cpcm-rij-memory/source_pins.json', LAB/'parent-pilot/pilot.py',
        Path(inspect.getsourcefile(pcm)), Path(inspect.getsourcefile(_attach_solvent)),
        Path(pyscf.__file__).parent/'gto/basis/def2-svp.dat', INTERPRETER.resolve(),
        LAB/'parent-openmp-qualification-v2/run.py']
    for name, expected in native.items():
        if '/site-packages/' in name:
            package, relative = name.split('/site-packages/', 1)[1].split('/', 1)
            actual = Path(importlib.import_module(package).__file__).resolve().parent / relative
            if sha(actual) != expected:
                raise ValueError('Actual imported source differs: ' + str(actual))
            paths.append(actual)
    spec = importlib.util.spec_from_file_location('runtime_helper', LAB/'parent-openmp-qualification-v2/run.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    paths.extend(helper.loaded_native_files())
    if pyscf.__version__ != '2.14.0':
        raise ValueError('Expected PySCF 2.14.0')
    return {str(Path(p).resolve()): sha(p) for p in paths}


def approval():
    path = BASE/'independent-root-review.json'
    if not path.exists():
        raise ValueError('Independent root review missing')
    reviewed = read(path)
    if (reviewed.get('status') != 'APPROVED_FOR_ONE_BOUNDED_NATIVE_CHILD' or
            reviewed.get('preparation_sha256') != sha(BASE/'preparation.json')):
        raise ValueError('Independent root review not approved for this preparation')
    return reviewed


def prepare():
    import numpy as np
    if (BASE/'preparation.json').exists() or RUN.exists():
        raise ValueError('Existing preparation/run retained; no overwrite')
    known = read(GEOMETRY)['results']['anion-water']
    if sorted(a[0] for a in known['atoms_A']) != ['Mo', 'O', 'O', 'O', 'O'] or known['charge'] != -2:
        raise ValueError('Unexpected retrospective geometry')
    with np.load(DENSITY) as fixture:
        density = fixture['initial_dm']
        if (density.ndim != 2 or density.shape[0] != density.shape[1] or
                np.iscomplexobj(density) or not np.isfinite(density).all() or
                not np.allclose(density, density.T, atol=1e-12, rtol=0)):
            raise ValueError('Invalid saved reference density')
        shape = list(density.shape)
    save(BASE/'preparation.json', {'status': 'PREPARED_NOT_EXECUTED', 'pins': pins(),
        'case': 'retrospective anion-water MoO4', 'density_key': 'initial_dm',
        'density_shape': shape, 'epsilons': [1., 78.4], 'steps': [1e-3, 5e-4],
        'native_probe_run': False, 'SCFs_launched': 0, 'physical_admission': False})


def worker():
    import numpy as np
    import response
    from pyscf import gto, lib
    from pyscf.solvent import pcm
    from pyscf.scf import hf
    from unittest.mock import patch
    arrays = {}
    record = {'status': 'RUNNING', 'checks': [], 'SCFs_launched': 0,
              'physical_admission': False, 'parent_run': False}

    def flush():
        save(RUN/'result.json', record)
        np.savez_compressed(RUN/'arrays.npz', **arrays)

    def check(name, passed, value=None):
        record['checks'].append({'name': name, 'pass': bool(passed), 'value': value})
        flush()

    def compare(name, a, b, tolerance):
        arrays[name+'/actual'] = np.asarray(a)
        arrays[name+'/reference'] = np.asarray(b)
        error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        check(name, np.isfinite(error) and error <= tolerance, error)

    def snapshot(value):
        if isinstance(value, np.ndarray):
            return (id(value), value.shape, value.dtype.str, value.flags.writeable,
                    hashlib.sha256(value.tobytes()).hexdigest())
        if isinstance(value, dict):
            return (id(value), {k: snapshot(v) for k, v in value.items()})
        if isinstance(value, (tuple, list)):
            return (id(value), [snapshot(v) for v in value])
        return value

    def state(s):
        return snapshot({k: getattr(s, k) for k in
            ('_intermediates', 'surface', 'v_grids_n', 'e', 'v', '_dm', 'equilibrium_solvation')})[1]

    try:
        if approval() != read(RUN/'root-review.json'):
            raise ValueError('Root review changed since launch')
        if not (RUN/'pins.json').exists() or pins() != read(RUN/'pins.json'):
            raise ValueError('Missing or changed launch pins')
        record['runtime'] = {'python': sys.executable, 'pyscf_threads': lib.num_threads(),
                             'OMP_NUM_THREADS': os.environ.get('OMP_NUM_THREADS')}
        check('actual_PySCF_threads_one', lib.num_threads() == 1 and os.environ.get('OMP_NUM_THREADS') == '1')
        if not record['checks'][-1]['pass']:
            raise ValueError('Actual PySCF thread getter must be one')
        known = read(GEOMETRY)['results']['anion-water']
        mol = gto.M(atom=known['atoms_A'], unit='Angstrom', basis='def2-svp',
            ecp={'Mo': 'def2-svp'}, charge=-2, spin=0, max_memory=512, verbose=0)
        with np.load(DENSITY) as fixture:
            p0 = fixture['initial_dm'].copy()
        if p0.shape != (mol.nao, mol.nao):
            raise ValueError('Fixture AO dimension mismatch')
        positive = .01 * np.eye(mol.nao) / np.sqrt(mol.nao)
        rng = np.random.default_rng(7392016)
        mixed = rng.standard_normal(p0.shape)
        mixed = (mixed + mixed.T) / 2
        mixed *= .01 / np.linalg.norm(mixed)
        deltas = {'zero': np.zeros_like(p0), 'positive': positive, 'negative': -positive, 'mixed': mixed}
        arrays.update({'P0': p0, **{'delta/'+k: v for k, v in deltas.items()}})
        with patch.object(hf.SCF, 'kernel', side_effect=AssertionError('SCF forbidden')):
            for eps in (1., 78.4):
                reference, candidate = pcm.PCM(mol), response.memory.MemoryPCM(mol)
                for s in (reference, candidate):
                    s.method = 'C-PCM'
                    s.surface_discretization_method = 'SWIG'
                    s.eps = eps
                    s.lebedev_order = 17
                    s.vdw_scale = 1.2
                    s.r_probe = 0.
                    s.build()
                candidate._get_vind(p0)
                before = state(candidate)
                outputs = {}
                for name, delta in deltas.items():
                    label = f'eps{eps}/{name}'
                    saved_delta = delta.copy()
                    outputs[name] = response.density_response(candidate, delta)
                    compare(label+'/stock_B_dot_x', outputs[name], reference._B_dot_x(delta), 1e-10)
                    check(label+'/input_unchanged', np.array_equal(delta, saved_delta))
                    curvature = float(np.sum(delta*outputs[name]))
                    check(label+'/nonpositive_solvent_curvature', np.isfinite(curvature) and curvature <= 1e-10, curvature)
                    if eps == 1. or name == 'zero':
                        check(label+'/exact_zero', np.array_equal(outputs[name], np.zeros_like(p0)))
                        check(label+'/exact_zero_curvature', curvature == 0., curvature)
                    for h in (1e-3, 5e-4):
                        plus = reference._get_vind(p0+h*delta)[1]
                        minus = reference._get_vind(p0-h*delta)[1]
                        arrays[label+f'/h{h}/plus'] = plus
                        arrays[label+f'/h{h}/minus'] = minus
                        compare(label+f'/FD_h{h}', outputs[name], (plus-minus)/(2*h), 1e-8)
                compare(f'eps{eps}/linearity', response.density_response(candidate, positive-2*mixed),
                        outputs['positive']-2*outputs['mixed'], 1e-10)
                compare(f'eps{eps}/reciprocity', np.sum(positive*outputs['mixed']),
                        np.sum(mixed*outputs['positive']), 1e-10)
                check(f'eps{eps}/cache_objects_bytes_unchanged', before == state(candidate))
                check(f'eps{eps}/equilibrium_flag_false', candidate.equilibrium_solvation is False)
        check('pins_unchanged', pins() == read(RUN/'pins.json'))
        record['status'] = 'PASS_RESPONSE_COMPONENT_ONLY' if all(c['pass'] for c in record['checks']) else 'FAIL'
    except Exception:
        record['status'] = 'ERROR'
        record['exception'] = traceback.format_exc()
    flush()
    return 0 if record['status'] == 'PASS_RESPONSE_COMPONENT_ONLY' else 1


def launch():
    reviewed = approval()
    expected = read(BASE/'preparation.json')['pins']
    if pins() != expected or RUN.exists():
        raise ValueError('Changed pins or existing run; no retry')
    RUN.mkdir()
    save(RUN/'pins.json', expected)
    save(RUN/'root-review.json', reviewed)
    spec = importlib.util.spec_from_file_location('original_supervisor', LAB/'parent-pilot/pilot.py')
    supervisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(supervisor)
    receipt = supervisor.monitored_run([sys.executable, '-B', str(BASE/'run.py'), '--worker'], RUN, 120, 2*2**30)
    passed = (receipt['returncode'] == 0 and receipt['termination_reason'] is None and
              receipt['monitor_error'] is None and pins() == expected)
    save(BASE/'launch-result.json', {'status': 'PASS_COMPONENT_RECEIPT' if passed else 'FAIL', 'receipt': receipt})
    return 0 if passed else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--launch']:
        raise SystemExit(launch())
    elif sys.argv[1:] == ['--worker']:
        raise SystemExit(worker())
    else:
        raise SystemExit('Use --prepare; --launch requires independent review and root authorization')
