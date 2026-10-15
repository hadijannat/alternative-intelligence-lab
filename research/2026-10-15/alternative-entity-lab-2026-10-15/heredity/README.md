# Conditional compositional transmission lab

Official result: only the two zero-copying-error conditions with synthesis
budgets 64 and 128 passed the strict 12/12-seed criterion. The 5% error conditions
passed 4/12, 10/12 and 9/12 seeds for budgets 16, 64 and 128 respectively. All 25%
error conditions failed. The low-resource zero-error condition passed 2/12.
See [the full report](results-v1/REPORT.md), [per-seed results](results-v1/results.json)
and [all 165,888 raw records](results-v1/raw.csv).

This is a finite-resource model of an explicitly supplied copying mechanism.
It is useful for locating transmission failures and separating founder carryover
from activity attributable to newly paid material. It supplies no measured
chemistry, physical replication, evolution, autonomous life or intelligence.

## Reproduction and tests

Requires Python and NumPy (official environment: Python 3.12.3, NumPy 2.4.1).
From this directory:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 -B -m unittest -v test_lab.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 -B lab.py --help
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 -B lab.py --output replay-v1
```

The official output is `results-v1`; a replay must use another, nonexistent
directory. Replaying frozen seeds checks deterministic repeatability and does
not add independent evidence. `freeze.json` captures the exact protocol,
configuration, model and test hashes before the run, verified unchanged after.

## Integration contract

`lab.partition_counts(counts, rng)` accepts a nonnegative integer NumPy array of
shape `(2,)` and a NumPy `Generator`. It returns two integer arrays with the same
shape; their elementwise sum equals the input exactly. Every molecule is assigned
to one daughter with probability 1/2. No input is mutated.

`lab.mutate_counts(counts, probability, rng)` takes the same inventory and a
finite probability in `[0,1]`. Each molecule switches to the other type with that
probability. The returned array conserves the total molecule count, and the input
is unchanged. Mutation here changes type, not amount; calling code must supply
its own energetics if type conversion has an energy cost.

The standalone population model uses conditional hypergeometric partition to
couple control arms at identical per-compartment counts. This is distributionally
equivalent to fair independent molecule partition conditioned on retained totals.
It does not import or execute previous repository experiments.

## Verification record

2026-10-15: all 11 synthetic unit tests passed in 0.080 seconds; CLI help exited 0.
The single official run exited 0 after 1.944487 seconds. All 165,888 material
balance checks passed, active arms matched F/N totals exactly, finite feed/fuel
constraints passed, and no-synthesis activity was zero after the ideal founder
purge. No official simulation was rerun or tuned after observing these results.

Unverified: real rate constants, thermodynamics, physical type-specific copying,
selective founder purge, experimentally separable new-material activity, and
organism-level traits. The model's imposed mechanisms remain its central limit.
