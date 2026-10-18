# Preserved execution and access limits

- Initial direct requests: DataCite data/software metadata and Dryad dataset
  metadata returned200. Zenodo API plus five figure scripts/helperZIP returned
  seven403 bodies. All bodies, sizes and hashes remain in `sources/attempt1/`.
- Normal browser download events timed out for Dryad and several software
  files. Subsequent exact local hashes prove acquisition of native data.zip,
  README and Fig3. A timeout alone is not a failed file transfer. Other native
  software files remain unacquired. See `sources/browser-observations.json`.
- The browser URL policy rejected a `chrome://downloads/` observation. No
  alternate browser-surface workaround was attempted. The requested source
  files were instead verified narrowly against known repository hashes.
- Default Python3.12.3 could not import scipy.io: transitive PROPACK loading
  failed for `_spropack.cpython-312-darwin.so` with
  `section '__DATA/__thread_bss' has a zero-fill section type, but offset field
  is not zero`. No installation or global-library repair was attempted.
- Existing project `parent-openmp/env-aligned/bin/python -B` imports scipy.io
  successfully. It reads all201MAT files at their storage level. For the XOR
  object, whosmat raises `TypeError("'NoneType' object is not iterable")`;
  loadmat instead exposes opaqueMCOS Experiment2 metadata and workspace bytes.
  That storage-level read is not resolved access to named learning properties.
- An exploratory schema-only inspection reconstructed an embedded mini-MAT
  header using the installed SciPy reader's documentation. It did not resolve
  property associations; no guessed MCOS mapping or new MAT parser was kept.
  No response values or numerical outcomes were calculated from this attempt.
- The current MathWorks format-document URL redirected to login in the web
  reader. No authentication was attempted; installed SciPy source comments were
  used only to interpret the unresolved storage representation.
- A separate validated MCOS reader subsequently resolves the numeric properties. HEAD source compilation failed on clang exit69 because the host Xcode license is not accepted. No license/settings changed. A public prebuilt1.0.1wheel was installed in a separate environment;12upstream class tests pass. The initial build and changed version are retained in DECODING_AMENDMENT.md/reader-runtime.json, with an unrelated inherited markdownify dependency warning left unrepaired.
- The first numerical entry-point execution preserved404archive records but stopped all191task runs before error calculation: the predeclared binary DOTEST assumption was false. Control-only diagnostics and newly acquired native helper methods identify DOTEST as a test-step schedule. The old result and exact source remain saved; REPLAY_SCHEDULE_AMENDMENT.md records a source-supported correction before scores are computed. This is not a failed learning experiment.
