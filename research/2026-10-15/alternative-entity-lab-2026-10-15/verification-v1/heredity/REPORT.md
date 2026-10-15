# Compositional transmission: official v1 results

The result concerns an investigator-supplied copying/assay network. No physical chemistry was calibrated or executed.

| Copying error | Resource budget | Seed passes | Every replicate | Wilson 95% interval |
|---:|---:|---:|:---:|:---:|
| 0.00 | 16 | 2/12 | False | 0.047 to 0.448 |
| 0.00 | 64 | 12/12 | True | 0.758 to 1.000 |
| 0.00 | 128 | 12/12 | True | 0.758 to 1.000 |
| 0.05 | 16 | 4/12 | False | 0.138 to 0.609 |
| 0.05 | 64 | 10/12 | False | 0.552 to 0.953 |
| 0.05 | 128 | 9/12 | False | 0.468 to 0.911 |
| 0.25 | 16 | 0/12 | False | 0.000 to 0.242 |
| 0.25 | 64 | 0/12 | False | 0.000 to 0.242 |
| 0.25 | 128 | 0/12 | False | 0.000 to 0.242 |

All 165,888 compartment/passage records are retained in `raw.csv`; per-seed metrics, individual gates and paired differences are in `results.json`. Runtime: 1.97 seconds.

All active controls matched F/N counts exactly in every compartment/passage. Every material balance was zero; synthesis cost and finite reporter fuel constraints passed. Founder activity was absent after the ideal purge. The no-synthesis arm had zero catalysts and activity after purge.

The strict all-seeds criterion is evaluated independently in each frozen grid cell; a failure is preserved. Wilson intervals describe seed-level variability, not physical replication. There is no test-set optimization, evolutionary selection or evidence of autonomous life/intelligence.

Limits: copying, catalytic specificity and selective founder purge are supplied rules. Synthesis and assay fuels are bookkeeping resources, with no thermodynamic calibration. New-material activity is an exact simulator attribution, not experimentally measured material-specific activity. The exchange control is whole-population pooling with exact recipient counts. Physical feasibility and a mechanism that discovers copying remain untested.
