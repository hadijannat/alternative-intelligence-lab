# Independent MCOS decoding-stage review

Date: 2026-10-18. codeQualityStatus: CLEAR. recommendation: APPROVE for named-property/schema inventory only. blockers: none for this stage. Scientific response replay is not approved by this report.

Scope: `analog-learning-replay/DECODING_PROTOCOL.md`, `DECODING_AMENDMENT.md`, `reader-runtime.json`, `inspect_properties.py`, reused archive-boundary checker, native-source provenance, and saved XOR/all-object property schemas. No measured response values were printed or analyzed. No downloads, package changes or research-file edits were performed by this reviewer.

## Findings by severity

- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: no correction required for the bounded schema stage. Future replay must validate DEL against its actual supported output conventions and require a nonempty valid evaluation set; schema qualification alone does not do that.

## Independent verification

1. Recomputed native ZIP SHA256 `f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c` and prebuilt wheel SHA256 `ea9583e7c234bbc7d2f38390f249b46b1813cf8ca24f065706db1b996fb09a4a`: both match the recorded artifacts.
2. Verified release checkout HEAD `b1a08584245ae4cec094be61b5ecb42b75ad3252`, installed package version 1.0.1, and byte equality for installed `subsystem/subsys.py`, `v5/matreader5.py` and `matio.py` versus that release. This checks those Python sources, not independent native-binary rebuild equivalence.
3. Inspected release-to-302efd source diff. The MCOS change caches the same padded variable-length record walk; the HDF5 handle branch is separate from these v5 objects. The amendment accurately describes the changed version and does not pretend the failed HEAD build was installed.
4. Independently reran the exact upstream `TestLoadMatlabUserDefined` selection in the isolated runtime: **12 passed in 0.63s**. These inspect known MATLAB-produced properties, defaults, array indexing and nested objects; they are useful decoder fixtures, not tests mirroring this experiment's desired outcome.
5. Independently reran `inspect(XOR, native_member_bytes)` without overwriting outputs. The resulting metadata/schema record exactly equals the saved XOR record, qualifies, and emits no warnings. No response calculations occur in that function.
6. Inspected all-object metadata output: all 200 records retained, 191 qualified, nine unqualified because DEL is absent. The qualified count families match the documented regression and XOR dimensions; the nine failures remain explicit rather than being silently repaired or discarded. The full 200-object decode was not independently rerun.

## Correctness and evidence boundaries

The upstream decoder associates class/property names with property type/value metadata through `get_property_idxs` and `get_saved_properties`; it does not guess property positions from experiment values. `raw_data=True` is explicitly supplied. The local stage records class, every property's type/shape/dtype, metadata scalars and allowed location checks. Finite integer counts, positive finite scales, documented array dimensions and in-range integral 4x4 locations are checked. Warnings and exceptions make qualification false and are retained per object. No free/clamped response values, performance errors, fitted models or favorable epochs are selected.

The wrapper's broad catch is a deliberate per-file inventory boundary with a persisted error and failed qualification. The unchanged frozen protocol plus explicit tool-version amendment preserve the failed-build history. Actual initial-row validity, time-array values, source/target orientation, TRAIN/TEST independence and physical output fidelity remain future analysis questions; passing dimensions cannot prove them. The absence of a reconstructed original MATLAB object-method execution is correctly not promoted into scientific replication.

## Skill-perspective review and remaining limits

Programming and remove-ai-slops perspectives were consulted in this review session. External MCOS parsing is required to access the source's documented named fields; reuse of the existing reader avoids speculative custom decoding. Metadata checks are at the native-input boundary. No tautological, removal-only, prose-pinning or outcome-pinning tests were added. No material violation of either perspective was found.

The script remains a bounded inventory tool. No repository-wide linter/typechecker/security scan was run. The Xcode-license failure is preserved as the executor's recorded event; this reviewer did not reproduce the failed build or accept a license. This approval adds no chemical maintenance, inheritance, integrated A/C, or full-goal credit. Freeze a separate response protocol before numerical replay.
