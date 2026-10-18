# Analog-learning acquisition/inventory review

Verdict: `codeQualityStatus: WATCH`; `recommendation: APPROVE` for the completed local acquisition/inventory stage only. `blockers: []` for that scope. The MEDIUM export finding below was corrected and independently rechecked. No MCOS reader or scientific replay approval is given.

## Findings

- CRITICAL: none.
- HIGH: none.
- MEDIUM: `tools/export_october18.py:34-42,63-68` in the clean publication clone omits authored `sources/native-inventory.json` and `sources/browser-observations.json` from `SOURCE_METADATA`. Both are referenced by the acquisition documentation; both currently fall through to source-payload exclusion. Preserve these authored evidence records in the curated handoff, while continuing to exclude native payloads. The new `browser-native` rule itself correctly prevents the third-party README from slipping through the Markdown allowance. This is a portable-evidence gap, not a failure of the locally verified acquisition.
- LOW: new scripts diverge from the loaded programming skill's strict typing/tooling conventions: e.g. unannotated `inventory.py:15,29` and `sources/import_browser_files.py:19,34`, plus the per-file broad catch at `inventory.py:58`. The catch explicitly records a parse error, and the verifier rejects any such record; it does not conceal a successful scientific calculation. Existing unittest and acquisition-helper conventions are reused. No demonstrated correctness defect follows for the frozen archive. A future generalized reader should use typed boundaries and explicit parser errors rather than copy these conventions.

## Independently inspected evidence

Scope was the complete new acquisition/inventory files under `documented-scaffold-2026-10-18/analog-learning-replay/`: PROTOCOL, REPORT, SOURCE_AUDIT, checks, progress, execution failures, inventory.py, test_sources.py, three acquisition/import wrappers, source verifier, receipts and native metadata. The clean clone's actual exporter diff was also read. Notepad: that directory's `progress.md`. `omo-agent-toolkit ulw-loop status --json` returned `ULW_LOOP_PLAN_MISSING`; this report therefore uses the fallback evidence path.

- Ran `python3 -B documented-scaffold-2026-10-18/analog-learning-replay/test_sources.py`: five tests passed. They exercise wrong bytes, overwrite refusal, traversal/symlink rejection, metadata path rejection with an error receipt, and partial-import failure preserving prior success. They are behavioral adversarial tests, not deletion-only, prose, constant-mirroring or tautological coverage.
- Ran `python3 -B documented-scaffold-2026-10-18/analog-learning-replay/sources/verify_sources.py`: 24/24 checks passed. Native metadata binds Dryad version 4, DOI `10.5061/dryad.8w9ghx3vx`, article `10.1073/pnas.2319718121`, CC0 data and separately MIT software. Eleven request records retain seven 403 bodies.
- Native archive is 15,756,671 bytes, SHA256 `f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c`; repository metadata and retained bytes agree. README and native Fig3 script hashes also pass. Missing software is explicitly recorded, not represented as downloaded.
- Independently reran inventory.main in a fresh temporary output root using the existing `parent-openmp/env-aligned/bin/python -B`, pointing only to the retained native archive and frozen protocol. Compared archive/protocol hashes, complete member list, sizes, CRC/safety flags and complete MATLAB schema records against the saved inventory: identical. Observed 404 ZIP entries, 201 MAT files and 16,237,245 expanded bytes. Original inventory was not overwritten.
- Top-level SciPy representation remains opaque for 200 Experiment2 files. The transparent oscilloscope schema is `(100,3)` float64. No array response values were printed, interpreted or replayed in this review. No source download or downloaded-code execution occurred.

## Skill perspective and limits

Resolution check: root added `native-inventory.json` and `browser-observations.json` to the metadata allowlist and this review to REVIEWS. A fresh `python3 -B` import of the actual exporter confirmed inclusion of both authored files and browser-receipt.json, exclusion of browser-native/README.md and browser-native/data.zip, and inclusion of this review. The MEDIUM finding is resolved. Full export and manifest checks remain the checkpoint owner's responsibility.

Loaded `omo:remove-ai-slops`, `omo:programming`, its Python reference and network reference. The slop/overfit pass found no useless tests, gratuitous scientific parsing/normalization, or needless abstraction. Hash verification, metadata identity checks and archive guards operate at actual source boundaries required by the task. The programming perspective found the LOW conventions gap recorded above; this is not an assertion of strict toolchain compliance. No lint/type-check gate was run because this bounded review used the existing project's runtime/tests and did not introduce a toolchain migration.

The 24 checks include frozen artifact assertions and declared scope flags; they establish source integrity, not independent proof that no prior human/agent exposure occurred. Browser observations are preserved reports rather than a browser session replay. Default SciPy import failure remains documented; the independent run used the explicitly identified working environment. Native payload omission means the curated checkout alone cannot reproduce acquisition checks without reacquiring inputs.

DECODING_PROTOCOL and any forthcoming inspect_properties.py, installed matio source/build, property mapping, TRAIN/TEST independence, numerical validation and scientific generalization are outside this verdict. All twelve integrated requirements remain unclosed; zero verified integrated complements and no physical verification follow from source access.

## Follow-up: native helper attachment and source methods

Scope extension: inspected `sources/import_helper_attachment.py`, `verify_helper_attachment.py`, `attachment-receipt.json`, `attachment-verification.json`, `HELPER_METHODS_AUDIT.md`, the six retained MATLAB source files' archive provenance, relevant Experiment2 source passages, and `REPLAY_SCHEDULE_AMENDMENT.md`. The original acquisition verdict/history above is preserved. This extension approves source acquisition and the documented interpretation of methods; it does not approve amended replay code or metrics.

Findings: CRITICAL none; HIGH none; MEDIUM none newly introduced; LOW the previously recorded typing conventions also apply to these small wrappers. `codeQualityStatus: WATCH`, `recommendation: APPROVE`, `blockers: []` for this scope.

Independently reran the helper verifier: 9/9 pass. Reran the existing source boundary tests: 5/5 pass. Independently called `checked_members` on the retained ZIP: 14 entries, 237,772 expanded bytes, no unsafe members or CRC failures. Its 50,569 bytes match repository MD5 `b9b06b71f3b709445f97d4386366fe76` and SHA256 `7c65cecb1b2cf19b7bb5f665c9b44695bb805d47214f38a9945ddffd5202cd46`. Earlier metadata verification binds the exact software DOI to MIT licensing. Six extracted file bodies match their archive entries and receipt hashes. Import reuses the existing verified-copy and archive boundaries, checks an exact six-basename set, writes only local basenames, refuses overwrite, and saves errors with partial evidence. This is justified boundary handling; no new parser or execution of deposited code is introduced.

Directly inspected source confirms:

- `Experiment2.m:69` declares DOTEST as test-schedule indices. Lines 425–427 require a row; line 724 uses DOTEST(m)-1 in cyclic training-index calculation. Lines 1280–1290 locate a requested step by equality. The former binary-flag interpretation is contradicted by this source.
- Lines 138–140 and 168–175 support the documented stored-measurement and raw-state axes. Lines 4140–4162 and 4198–4218 compare TestMeasurements with TestFreeState at TLOC+1 and the same snapshot index. These are intended consistency relations, not proof of agreement for all native data.
- Lines 781–787 apply first-minus-second to both labels and predictions; a consistent joint sign reversal preserves squared error. Lines 86 and 613–650 send schedule data to the controller; they do not establish its acquisition/save ordering. The audit appropriately leaves initial-row ordering unresolved and records the incomplete getDimensions declaration.

The amendment explicitly preserves the prior failed binary-rule replay and distinguishes an encoding-assumption failure from a physical-learning failure. Positive-integer/strictly-increasing schedule acceptance and rejection of an entirely zero grid are declared replay screening choices, not additional facts proved by the cited sender code. Their application and any excluded snapshots need the separate numerical review. No response values or metrics were inspected or calculated here, and source methods cannot by themselves prove the historical timing of all prior exposure.

Focused exporter invocation confirms inclusion of `attachment-receipt.json`, `attachment-verification.json` and `HELPER_METHODS_AUDIT.md`; the native `.m` files and ZIP remain excluded. Full exported-manifest validation remains pending with the checkpoint owner. Skill perspectives remained active: no needless data transformation or implementation-mirroring tests were added. All twelve integrated requirements retain their unresolved status.
