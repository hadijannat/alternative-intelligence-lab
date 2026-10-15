"""Exact witnesses for measurements that cannot identify the desired quantity."""
from fractions import Fraction as F
import json


def witnesses():
    # Coordinates are old active, old inactive, new active, new inactive.
    activity_worlds = [(F(10), F(0), F(0), F(10)),
                       (F(0), F(10), F(10), F(0))]
    observations = [(a+b, c+d, a+c) for a, b, c, d in activity_worlds]
    assert observations[0] == observations[1]
    assert activity_worlds[0][2] != activity_worlds[1][2]

    recovery_worlds = [(F(4, 5), F(5, 8)), (F(1, 2), F(1))]
    assert recovery_worlds[0][0] != recovery_worlds[1][0]
    assert {retained*recovery for retained, recovery in recovery_worlds} == {F(1, 2)}

    # Coordinates are lumen, membrane/apparatus-bound, outside, degraded.
    fraction_worlds = [(F(4, 5), F(0), F(1, 10), F(1, 10)),
                       (F(1, 2), F(3, 10), F(1, 10), F(1, 10))]
    assert all(sum(w) == 1 for w in fraction_worlds)
    assert {(lumen+surface, outside) for lumen, surface, outside, _ in fraction_worlds} == {(F(4, 5), F(1, 10))}
    assert fraction_worlds[0][0] != fraction_worlds[1][0]

    # With a pure lumen assay, unmeasured fractions still hide the loss mechanism.
    loss_worlds = [(F(1, 2), F(2, 5), F(1, 10), F(0)),
                   (F(1, 2), F(0), F(1, 10), F(2, 5))]
    assert all(sum(w) == 1 for w in loss_worlds)
    assert {(w[0], w[2]) for w in loss_worlds} == {(F(1, 2), F(1, 10))}
    assert loss_worlds[0][3] != loss_worlds[1][3]
    return dict(status='PASS', exact_arithmetic='fractions.Fraction', checks=4,
        marginal_age_and_activity=dict(worlds=activity_worlds, observed=observations[0],
            fields=['old_active', 'old_inactive', 'new_active', 'new_inactive'],
            conclusion='Age totals and total capacity do not identify new capacity.'),
        unknown_recovery=dict(worlds=recovery_worlds, measured_fraction=F(1, 2),
            fields=['true_retention', 'extraction_recovery'],
            conclusion='Independent recovery calibration is required.'),
        unresolved_surface=dict(worlds=fraction_worlds, measured_pellet=F(4, 5),
            measured_outside=F(1, 10), fields=['lumen', 'surface', 'outside', 'degraded'],
            conclusion='Unresolved surface binding can mimic lumen retention.'),
        missing_fraction=dict(worlds=loss_worlds, measured_lumen=F(1, 2),
            measured_outside=F(1, 10), fields=['lumen', 'surface', 'outside', 'degraded'],
            conclusion='Missing surface fractions confound adsorption and degradation even with a pure lumen assay.'))


if __name__ == '__main__':
    print(json.dumps(witnesses(), default=str, indent=2))
