# Serialization repair after first run

The first frozen run `results-v1` completed every chemical fit, transport calibration and sensitivity case, then failed before completion when JSON tried to serialize a NumPy boolean in the integration-refinement check. The partial directory, frozen code and `run-v1.log` are preserved. It has no final manifest and is not the completed experiment.

The only numerical-program change for `results-v2` converts the scalar PAGE observer to native Python `float` at its return boundary. This preserves the identical IEEE754 numerical value while making downstream comparisons native booleans. Unit tests now verify the scalar type and JSON serialization of the actual refinement comparison. No model, equation, candidate, bound, start, fold, criterion or fitting budget changed. The full registered scenario is rerun from source in a fresh output directory. README examples point to the completed rerun.
