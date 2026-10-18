import hashlib
import json
from pathlib import Path, PurePosixPath

import build_archive as archive
import curate_archive as curator
from export_followup import strip_signed_urls
from export_october18 import FAILURES, LAB, REVIEWS, exclusion


def verify(base):
    manifest = json.loads((base / 'manifest.json').read_text())
    assert manifest['scientific_validation'] is False
    assert manifest['date'] == '2026-10-18'
    records = manifest['files']
    assert len({r['path'] for r in records}) == len(records)
    included = [r for r in records if r['status'] == 'included']
    assert len(included) == manifest['included_files']
    assert sum(r['published_size'] for r in included) == manifest['published_bytes']
    assert sum(r['status'] == 'excluded' for r in records) == manifest['excluded_entries']
    actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
    expected = {r['path'] for r in included} | {'manifest.json'} | set(manifest['generated_files'])
    assert actual == expected, (actual - expected, expected - actual)
    for record in included:
        name = PurePosixPath(record['path'])
        assert not name.is_absolute() and '..' not in name.parts
        assert name.parts[0] in {LAB, 'reviews', 'GOAL_CONTRACT.md'}
        if name.parts[0] == LAB:
            assert exclusion(Path(*name.parts[1:])) is None, name
        elif name.parts[0] == 'reviews':
            assert name.name in REVIEWS
        path = base / name
        assert not path.is_symlink()
        raw = path.read_bytes()
        assert len(raw) == record['published_size'] < 100 * 1024 * 1024
        assert hashlib.sha256(raw).hexdigest() == record['published_sha256'], name
        assert len(record['source_sha256']) == 64 and record['source_size'] >= 0
        assert isinstance(record['transformations'], list)
        if path.suffix in archive.TEXT or path.suffix == '.log':
            text = raw.decode('utf-8')
            assert not archive.HOST.search(text) and not archive.KEY.search(text), name
            assert strip_signed_urls(text)[1] == 0, name
            if path.suffix == '.json':
                assert not curator.tool_envelope(json.loads(text), str(name)), name
    for name, digest in manifest['generated_files'].items():
        assert name == 'README.md'
        assert hashlib.sha256((base / name).read_bytes()).hexdigest() == digest
    paths = {r['path'] for r in included}
    assert {LAB + '/' + name for name in FAILURES} <= paths
    assert LAB + '/NEXT_SESSION_PROMPT.md' in paths
    assert 'GOAL_CONTRACT.md' in paths
    ledger = (base / LAB / 'CONTINUATION_LEDGER.md').read_text()
    assert '../GOAL_CONTRACT.md' in ledger
    for path in (base / LAB).rglob('negative_results.json'):
        negative = json.loads(path.read_text())
        if 'verified_integrated_complements_added' in negative:
            assert negative['verified_integrated_complements_added'] == 0
        if 'origin_specific_repair_verified' in negative:
            assert negative['origin_specific_repair_verified'] is False
    remote = json.loads((base / LAB / 'remote-fe-transport/negative_results.json').read_text())
    assert remote['chemical_rates_identified'] is False
    assert remote['candidate_forecast_validated'] is False
    assert remote['previous_results_preserved'] is True
    assert {'convergence-diagnostic-failure', 'candidate-training-insufficient',
            'five-hour-aggregation-failure'} <= {r['id'] for r in remote['negatives']}
    result = json.loads((base / LAB / 'remote-fe-transport/results/analysis.json').read_text())
    assert result['checks']['step_convergence_below_1e_minus_5'] is False
    assert set(result['candidate']) == {'LDH', 'NiFeCl', 'NiFeZnCl'}
    for candidate in result['candidate'].values():
        assert candidate['status'] == 'insufficient_data'
        assert candidate['fits'] == {}
        assert candidate['training_count'] == 2 and candidate['reserved_count'] == 6
    for membrane in ('AEM', 'CEM'):
        assert result['CA'][membrane]['strict_full_edge_retention'] is None
    reversals = result['synthetic']['lower_sink_minus_higher_sink_A_5h']
    assert len(reversals) == 5 and {row['ka'] for row in reversals} == {0, 0.1, 1, 10, 100}
    assert all(row['reversal'] is False for row in reversals)
    spatial = base / LAB / 'spatial-fe-function'
    spatial_result = json.loads((spatial / 'results/analysis.json').read_text())
    empirical = spatial_result['empirical_held_out_validation']
    assert empirical['status'] == 'INSUFFICIENT_DATA'
    assert empirical['training_points'] == 0 and empirical['held_out_points'] == 0
    assert spatial_result['classification'] == 'source-informed analytical/synthetic identifiability test'
    assert spatial_result['main_case']['identified_under_assumptions'] is False
    assert 'No active repair, inheritance, life or integrated complement established.' in spatial_result['limitations']
    spatial_run = json.loads((spatial / 'results/run-output.json').read_text())
    assert spatial_run['empirical_status'] == 'INSUFFICIENT_DATA'
    spatial_negative = json.loads((spatial / 'NEGATIVE_RESULTS.json').read_text())
    assert {r['id'] for r in spatial_negative['negative_results']} == {f'SF{i:02}' for i in range(1, 12)}
    assert next(r['result'] for r in spatial_negative['negative_results'] if r['id'] == 'SF11') == (
        'No same-specimen active repair, founder-bounded inheritance, integrated complement, life or intelligence has been demonstrated.')
    regeneration = json.loads((base / LAB / 'regeneration-controls/file_manifest.json').read_text())
    assert regeneration
    return dict(status='PASS_OCTOBER18_PUBLICATION_ONLY', verified_files=len(included),
                published_bytes=manifest['published_bytes'], scientific_reruns=0,
                missing_reviews=manifest['missing_reviews'])


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1] / 'research/2026-10-18'), indent=2))
