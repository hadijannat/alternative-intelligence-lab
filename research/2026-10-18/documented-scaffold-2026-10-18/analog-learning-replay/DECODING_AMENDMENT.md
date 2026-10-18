# Reader build failure and prebuilt-release alternative

This amendment is recorded before experimental named-property inspection. `DECODING_PROTOCOL.md` remains unchanged. Its selected HEAD source `302efd30727473fa1a47ffd425b85d738be414e5` was cloned and verified. An isolated Python3.12 environment was created outside the publication checkout and build dependencies installed there; no global environment was repaired.

The HEAD wheel build failed with clang exit69: the host reports that Xcode license agreements have not been accepted. No license was accepted, no privileged setting changed, and that build did not produce an installed reader or experimental decode. The dependency installer also reported an inherited unrelated markdownify/BeautifulSoup inconsistency; that package is not used by this reader and was not repaired.

PyPI provides an existing macOS-arm64 Python3.12 wheel for `mat-io==1.0.1`, associated with release commit `b1a08584245ae4cec094be61b5ecb42b75ad3252`. Use this prebuilt release in the isolated environment, with its archive SHA256 and installed versions recorded. This is a changed tool version, not the inspected HEAD binary. Compare its Python reader source against the release checkout; no independent binary rebuild equivalence is claimed.

The exact source diff from release to HEAD was inspected. It adds cached MCOS record-offset walking (replacing the same uncached recurrence), an HDF5 `handle` type branch, and tests. The recorded data are v5 MCOS Experiment2 objects. No changed property-name/type/value association rule was found for this case. This justifies testing the released reader; it does not establish compatibility in advance.

All original acceptance criteria stay in force: upstream class-fixture load tests must pass first, raw_data=True only, named property association, warnings/exceptions retained, required dimensions/metadata, and no response values or numerical replay before a separate frozen analysis protocol. If any criterion fails, keep the failure and stop the affected step.
