"""Audit transcribed source arithmetic; no chemical rates or joint-system prediction."""
import csv
import json
from decimal import Decimal as D
from pathlib import Path

BASE = Path(__file__).resolve().parent


def efficiency_percent(output_j, input_j):
    if input_j <= 0 or output_j < 0:
        raise ValueError('positive input and nonnegative output required')
    return 100 * output_j / input_j


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    assert efficiency_percent(D(1), D(10)) == 10
    for output, energy in [(D(1), D(0)), (D(-1), D(2))]:
        try:
            efficiency_percent(output, energy)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid energy input accepted')
    rows = list(csv.DictReader((BASE / 'ceria_cycles.csv').open()))
    assert len(rows) == 9
    assert {(r['test'], r['cycle']) for r in rows} == {(str(t), str(c)) for t in range(1, 4) for c in range(1, 4)}
    for row in rows:
        energy = 270 * D(row['time_270W_s']) + 135 * D(row['time_135W_s'])
        assert energy == D(row['reported_Qsolar_J'])
        eta = efficiency_percent(D(row['reported_HHV_H2_J']), energy)
        assert abs(eta - D(row['reported_cycle_efficiency_percent'])) <= D('.0005')
    summaries = []
    for test in ('1', '2', '3'):
        subset = [r for r in rows if r['test'] == test]
        output = sum(D(r['reported_HHV_H2_J']) for r in subset)
        energy = sum(D(r['reported_Qsolar_J']) for r in subset)
        reported = D(subset[0]['reported_test_efficiency_percent'])
        eta = efficiency_percent(output, energy)
        assert reported == sum(D(r['reported_cycle_efficiency_percent']) for r in subset)
        assert abs(eta - reported) > D('.0005')
        assert 0 < eta < 1
        # The source does not provide covariance; do not combine its volume errors statistically.
        summaries.append(dict(test=test,output_HHV_J=str(output),incident_energy_J=str(energy),
                              aggregate_efficiency_percent=str(eta),reported_test_percent=str(reported),
                              reported_equals_sum_of_rounded_cycle_percent=True,
                              incident_energy_per_HHV_J=str(energy/output)))
    # Source benchmark: equal 2e charge per half-cycle; all potentials already on the source NHE scale.
    reduction, oxidation, oer, her = map(D, ('0.46', '0.85', '2.17', '-0.38'))
    charge, discharge = oer-reduction, oxidation-her
    direct = oer-her
    assert (charge, discharge, charge+discharge, direct) == (D('1.71'),D('1.23'),D('2.94'),D('2.55'))
    assert charge+discharge-direct == oxidation-reduction == D('.39')
    result = dict(status='PASS_BOUNDED_ARITHMETIC',ceria_nine_cycle_power_sums_pass=True,
                  ceria_cycle_efficiency_rounding_pass=True,ceria=summaries,
                  pmo12=dict(charge_step_V=str(charge),discharge_step_V=str(discharge),
                             sum_equivalent_V=str(charge+discharge),direct_V=str(direct),
                             relative_energy_efficiency=str(direct/(charge+discharge)),
                             extra_energy_fraction=str((charge+discharge)/direct-1)),
                  limits='Source-table arithmetic only. No raw sensor reanalysis, uncertainty interval, same-medium transfer, reaction rate, or organism prediction.')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
