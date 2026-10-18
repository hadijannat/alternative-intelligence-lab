# Pre-execution observation safeguards

Independent protocol review approved the retrospective design before any numerical response execution. These clarifications resolve ordering/encoding ambiguity, without changing `REPLAY_PROTOCOL.md`, its endpoints, inclusion, tolerances or baselines.

- Apply raw-target versus stored-TestMeasurements equality only on structurally complete snapshots. Retain placeholder/missing rows and their reasons; they are not a failed physical prediction.
- DEL1 requires an even positive TAR so every second-minus-first pair is defined. Any other DEL encoding fails the affected run.
- Require DOTEST to be a finite binary0/1 array of the declared snapshot length. A complete test uses flag1; arbitrary numeric truthiness and NaN are not accepted. If actual encoding is different, preserve the failed rule and seek source semantics before changing it.
- A run with zero complete snapshots remains in the result as failed/unresolved. It cannot silently disappear from the191-run inventory or a summary denominator.
- Generated replay results retain per-snapshot validity, reasons and derived errors, plus mapping/drive/state diagnostics. Original node tensors remain in the native archive rather than being duplicated as one-to-one published source cells.

These are pre-outcome safeguards suggested by `.omo/evidence/analog-learning-protocol-review.md`. No raw response outcome has been read to choose them.
