# Conditional measurement execution

Invocation from the repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/dissolution-observation/test_measurement.py
```

Observed exit code: 0. `measurement.json` contains all 12 binary self-checks as `PASS`, six conditional 50 mL scenarios, two hypothetical 50 microlitre scenarios, and the protocol, script, native PDF and native DOCX SHA256 values. The maximum absolute conservation residual across the eight saved scenarios is 1.7763568394002505e-15 normalized mass units.

| Flow (microlitres/s) | Operator | Final liquid (units) | Exported (units) | Final liquid volume (mL) |
| --- | --- | --- | --- | --- |
| 3.2 | Unreplenished | 5.7634184431 | 0.2365815569 | 46.16 |
| 3.2 | Clean replenishment | 5.7753799037 | 0.2246200963 | 50 |
| 3.2 | Complete reset comparison | 0 | 6 | 50 |
| 3.5 | Unreplenished | 5.7405714258 | 0.2594285742 | 45.8 |
| 3.5 | Clean replenishment | 5.7549014041 | 0.2450985959 | 50 |
| 3.5 | Complete reset comparison | 0 | 6 | 50 |

Every scenario ends with four solid mass units after six polarization hours and four five-minute source-free sampling windows. Complete reset requires an assumed 50 mL removal/refill per window, independent of nominal flow; its cumulative exported volume is 200 mL. Its zero-flow behavior therefore differs intentionally from the two flow-governed operators.

The first native-volume window removes only 1.92% or 2.10% of liquid mass without replenishment, and 1.9016854% or 2.0781035% with continuous clean replenishment. The hypothetical 50 microlitre case gives first-window residual mass fractions approximately 4.5872e-9 and 7.5826e-10. That sensitivity does not establish the native circulating volume.

No runtime check failed. Before execution, the comment checker flagged the new module docstring and the explanatory complete-reset comment. The redundant docstring was removed; the comment explaining why this operator ignores nominal flow was retained. No numerical result or test criterion changed in that edit.

These are normalized measurement calculations with arbitrary source strength. No chemical rate, observed response, held-out chemical prediction, active repair, or verified complement is established. A separate plot was omitted because the eight short tabulated trajectories are available directly in the JSON.
