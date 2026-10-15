# Implementation correction before accepted result

Independent review identified two defects in version 1.0, after its campaign completed. `results-v1/` retains its raw outputs, summary and original source/config/protocol snapshots. Those results are superseded by `results-v1.2/` for final interpretation.

1. Feedback used the world's correctness bit even if resource stock was exhausted. The frozen v1 campaign did not exhaust stock, but a reproduced zero-stock case still updated 6, 5, 4 and 3 carrier labels in its first four episodes with no observed harvest. Version 1.1 obtains feedback only from observed harvest magnitude with sufficient uncapped stock, and withholds it otherwise.
2. Independent binomial label loss could remove more labels than actual structure decay, then fill the vacant count with new copying labels even when structural renewal was disabled. Version 1.1 fixes the surviving carrier count from actual surviving structure, samples identities without replacement, and adds labels only in the count increment associated with actual structural renewal.

Regression tests cover both counterexamples. Model parameters, seeds, scenarios, acceptance thresholds, number of runs and horizon remain unchanged. This is a correction of implementation, not outcome-driven tuning. The retained v1 source allows inspection of the discrepancy; no positive claim is rescued by changing the criterion.

Version 1.1 completed with the same seed-level scenario verdicts. A final input-validation correction, version 1.2, rejects a horizon with no evaluation episodes and invalid seed/arm lists before output creation. Version 1.1 is retained; v1.2 has identical default numerical rules and must reproduce its numerical outputs. These versions are repeated calculations, not additional independent histories.
