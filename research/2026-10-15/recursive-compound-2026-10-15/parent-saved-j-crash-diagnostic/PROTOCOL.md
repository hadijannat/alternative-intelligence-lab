# Terminal crash diagnostic

Objective: narrow the failure boundary of the sole saved-J parent pilot without changing its frozen implementation, suppressing checks or treating its failed result as chemical evidence.

Inputs: the PID94528 macOS report named python3.12-2026-10-16-005859.ips, the immutable parent-saved-j-pilot/run-v1 receipts and stages, pinned Python implementation files and runtime binaries, and separately hashed installed C source accompanying that runtime. The C files were not included in the earlier runtime pins; exact compiled-source equivalence is unproven. Raw system reports remain outside the research export; preserve a selected excerpt with original digest, timestamps, exception, binary identities and stack frames. Omit device identifiers, registers, unrelated processes and local image paths.

Acceptance: confirm PID/process match; compare signal to the supervisor; identify the immediate native stack and source ordering; distinguish observed return from absent enclosing return; retain unknown origin explicitly. Test the excerpt filter using synthetic reports including wrong-PID and invalid-index controls. No chemical operator, SCF, production retry, allocator setting change or runtime substitution is authorized by this diagnostic protocol. A prospective reproducer requires a separate bounded protocol.

The source report's stack may identify where corruption was detected, without identifying the earlier write. A success here is a better diagnostic boundary, not restoration of numerical or chemical validity. Preserve all previous failures and the full unresolved life-function requirements.
