"""Offline source checks, exact witnesses, tests and complete independent replay."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import numpy as np

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')


def previous_files():
    return {str(p.relative_to(HERE.parent)): digest(p)
            for name in ('rna-mechanism-2026-10-15', 'measured-coupling-2026-10-15')
            for p in (HERE.parent/name).rglob('*')
            if p.is_file() and not any(part.startswith('.') or part == '__pycache__'
                                      for part in p.relative_to(HERE.parent/name).parts)}


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    commands, checks = [], {}
    old = previous_files()
    freezes = {lab: json.loads((HERE/lab/'results-v1/freeze.json').read_text())
               for lab in ('assay', 'lineage')}
    inputs = {str(HERE/'assay'/name): sha for name, sha in freezes['assay']['hashes'].items()}
    inputs.update({str(HERE/name): sha for name, sha in freezes['lineage']['sources'].items()})
    inputs.update({str(HERE/name): digest(HERE/name) for name in ('run_suite.py', 'counterexamples.py')})
    assert all(digest(Path(p)) == sha for p, sha in inputs.items()), 'source differs from frozen campaign'
    write(out/'inputs.json', inputs)
    with zipfile.ZipFile(out/'integration-source.zip', 'w') as archive:
        for p in inputs:
            archive.write(p, str(Path(p).relative_to(HERE)))

    def run(label, args, cwd=HERE):
        with (out/f'{label}.log').open('w') as log:
            result = subprocess.run([sys.executable, *map(str, args)], cwd=cwd,
                                    stdout=log, stderr=subprocess.STDOUT)
        commands.append(dict(label=label, args=list(map(str, args)), cwd=str(cwd),
                             exit_code=result.returncode))
        if result.returncode:
            write(out/'failure.json', dict(status='FAIL', commands=commands))
            raise RuntimeError(f'{label} failed; inspect {out/f"{label}.log"}')

    run('assay-tests', ['-m', 'unittest', '-v', 'test_model'], HERE/'assay')
    run('lineage-tests', ['-m', 'unittest', '-v', 'test_model'], HERE/'lineage')
    run('source-identities', ['research/assays/verify.py'])
    run('counterexamples', ['counterexamples.py'])
    counterexamples = json.loads((out/'counterexamples.log').read_text())
    assert counterexamples['status'] == 'PASS' and counterexamples['checks'] == 4
    checks['four_exact_counterexamples'] = True

    lineage_design = HERE/'research/lineage'
    receipt = json.loads((lineage_design/'verification.json').read_text())
    assert all(digest(lineage_design/name) == sha for name, sha in receipt['artifacts'].items())
    assert all(receipt['checks'].values()) and len(receipt['checks']) == 6
    checks['lineage_design_receipt_and_source_hashes'] = True

    # Run the exact assay snapshot: later reports must not change its source discovery.
    frozen_source = out/'assay-source'
    frozen_source.mkdir()
    with zipfile.ZipFile(HERE/'assay/results-v1/source.zip') as archive:
        assert set(archive.namelist()) == set(freezes['assay']['hashes'])
        for name in archive.namelist():
            assert Path(name).name == name, 'snapshot must contain only top-level files'
            data = archive.read(name)
            assert hashlib.sha256(data).hexdigest() == freezes['assay']['hashes'][name]
            (frozen_source/name).write_bytes(data)
    run('assay-replay', [frozen_source/'run.py', '--output', out/'assay'])
    for name in ('freeze.json', 'observations.jsonl', 'retention_observations.jsonl',
                 'summary.json', 'retention.json', 'material_budget.csv',
                 'nonidentifiability.json', 'power.png', 'verification.json'):
        checks[f'assay/{name}'] = digest(out/'assay'/name) == digest(HERE/'assay/results-v1'/name)
    with zipfile.ZipFile(out/'assay/source.zip') as archive:
        checks['assay/source-members'] = all(hashlib.sha256(archive.read(name)).hexdigest() == sha
                                            for name, sha in freezes['assay']['hashes'].items())

    run('lineage-replay', [HERE/'lineage/run.py', '--replay', HERE/'lineage/results-v1',
                           '--output', out/'lineage'])
    replay = json.loads((out/'lineage/replay.json').read_text())
    assert replay['passed'] and all(replay['checks'].values())
    checks.update({f'lineage/{name}': value for name, value in replay['checks'].items()})
    checks['lineage/freeze.json'] = digest(out/'lineage/freeze.json') == digest(HERE/'lineage/results-v1/freeze.json')
    for folder in (HERE/'lineage/results-v1', out/'lineage'):
        with zipfile.ZipFile(folder/'sources.zip') as archive:
            assert set(archive.namelist()) == set(freezes['lineage']['sources'])
            assert all(hashlib.sha256(archive.read(name)).hexdigest() == sha
                       for name, sha in freezes['lineage']['sources'].items())
    checks['lineage/source-members'] = True
    raw_digests = json.loads((HERE/'lineage/results-v1/numerical-digests.json').read_text())
    for name, sha in raw_digests.items():
        with np.load(HERE/'lineage/results-v1'/name) as original, np.load(out/'lineage'/name) as replayed:
            a, b = original['observations'], replayed['observations']
            checks[f'lineage/{name}'] = (np.array_equal(a, b, equal_nan=True)
                                         and hashlib.sha256(a.tobytes()).hexdigest() == sha)
    assert all(checks.values()), 'replay mismatch'
    assert all(digest(Path(p)) == sha for p, sha in inputs.items()), 'input changed during checks'
    assert old == previous_files(), 'previous laboratory changed'
    import scipy, matplotlib, openpyxl
    write(out/'verification.json', dict(status='PASS', commands=commands, checks=checks,
        input_hashes_unchanged=True, previous_files_unchanged=len(old),
        versions=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__,
                      matplotlib=matplotlib.__version__, openpyxl=openpyxl.__version__),
        exclusions='ZIP container timestamps and execution elapsed times; scientific data are compared exactly.',
        limits='Computational/source verification only. Physical assays, rates and division remain unqualified.'))
    print(json.dumps(dict(status='PASS', checks=len(checks), previous_files_unchanged=len(old))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args().output.resolve())
