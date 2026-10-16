import csv
import hashlib
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent


def summarize(observed, predicted):
    if len(observed) != len(predicted) or not observed:
        raise ValueError('Nonempty paired observations required')
    if not all(math.isfinite(x) and 0 <= x <= 100 for x in observed + predicted):
        raise ValueError('Finite percentages required')
    residuals = [p - y for y, p in zip(observed, predicted)]
    return {'model_minus_observed_percentage_points': residuals,
            'max_absolute_percentage_points': max(map(abs, residuals)),
            'RMS_percentage_points': math.sqrt(sum(x*x for x in residuals)/len(residuals)),
            'within_authors_three_unit_estimate': sum(abs(x) <= 3 for x in residuals)}


if __name__ == '__main__':
    assert summarize([0, 3, 10], [3, 0, 14])['within_authors_three_unit_estimate'] == 2
    assert summarize([5], [2])['model_minus_observed_percentage_points'] == [-3]
    for bad in (([], []), ([1], [1, 2]), ([float('nan')], [1]), ([101], [1])):
        try:
            summarize(*bad)
        except ValueError:
            continue
        raise AssertionError('Invalid pair accepted')
    path = BASE/'observations.csv'
    with path.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    observed = [float(r['experimental_monomer_percent_V']) for r in rows]
    models = {key: summarize(observed, [float(r[key]) for r in rows])
              for key in rows[0] if key.startswith('model_')}
    print(json.dumps({'source_table_rows': len(rows), 'source_table_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'models': models, 'uncertainty_is_formal_confidence_interval': False,
        'parameters_fitted': 0, 'retrospective_only': True, 'held_out_validation': False,
        'target_tested': False, 'new_roles': 0, 'physical_admission': False}, indent=2, allow_nan=False))
