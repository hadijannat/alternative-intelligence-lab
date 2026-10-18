# Qualified reader route, before experimental decoding

Read-only librarian research,2026-10-18. The acquired learning archive contains200opaque Experiment2 objects under ordinary SciPy loading. No numerical response values were read in this source-research step. No MATLAB/Octave runtime was found by the scout in ordinary executable/application locations.

The primary candidate is `mat-io` from foreverallama/matio, exact commit `302efd30727473fa1a47ffd425b85d738be414e5`, BSD-3-Clause. This is distinct from released v1.0.1 at `b1a08584245ae4cec094be61b5ecb42b75ad3252`. Do not silently substitute release bytes for the inspected source.

- [MCOS property names and typed value references](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/matio/subsystem/subsys.py#L418-L434) are decoded from stored metadata.
- [Default/saved/dynamic properties](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/matio/subsystem/subsys.py#L482-L502) are combined explicitly.
- The [`raw_data=True` branch](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/matio/subsystem/subsys.py#L992-L1020) retains a wrapper and `.properties` instead of invoking Experiment2 MATLAB methods.
- [User-defined-class tests](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/tests/test_user_defined.py#L38-L57) compare exact dtype/shape/value arrays. [MATLAB fixture generation](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/tests/data/generators/test_user_defined_gen.m#L1-L28) supplies known object cases.
- The [build/runtime manifest](https://github.com/foreverallama/matio/blob/302efd30727473fa1a47ffd425b85d738be414e5/pyproject.toml#L1-L26) declares Python>=3.11, SciPy>=1.15, NumPy>=2.2.2, pandas>=2.2 and h5py>=3.13, with Cython/setuptools build requirements. Actual dependency compatibility and Experiment2 decoding remain untested at this research stage.

The scout's textual scan found no eval/exec/pickle/subprocess/os.system/loadobj/__import__ matches in current reader Python/Cython files; this limited screen is not a security guarantee. MATLAB's own [load documentation](https://www.mathworks.com/help/matlab/ref/load.html) warns of possible code execution, so running the external MATLAB class is not the selected shortcut.

Next: pin/inspect local source, isolated installation, upstream fixture tests, then named property/schema inspection only. Stop on unresolved fields, unexpected custom serialization, warnings or inconsistent dimensions. Do not guess MCOS array positions. Numerical replay requires a separate frozen response-analysis protocol after the observation mapping is qualified. Successful parsing would be data accessibility, not learning or full-goal validation.
