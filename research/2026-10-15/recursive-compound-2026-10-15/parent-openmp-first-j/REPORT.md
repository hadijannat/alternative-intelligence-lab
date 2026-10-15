# Parent first-J diagnostic: setup guard failure

The single launch ended INCOMPLETE_OR_FAILED_FIRST_J after 10.324156 seconds with return code 1. There was no wall/RSS termination or monitor error. Sampled maximum RSS was 505413632 bytes, not a certified peak. All frozen pins and the bound review remained unchanged. Stage history reaches setup_complete, then failure.json records `ValueError: PCM allocated during setup`; no first_J_start, completed J, or SCF exists. The original code, preparation and run are preserved.

Root source inspection finds that pinned PySCF 2.14.0 PCM.__init__ initializes `surface={}`, `_intermediates={}`, and `v_grids_n=None`; reset instead uses `surface=None`. This driver incorrectly required `surface is None` at setup and after J. The failure therefore cannot be interpreted as evidence of an actual allocated solvent surface, chemical failure or parent Coulomb infeasibility. A separate repair must verify the native unbuilt state while continuing to reject populated surface/matrix state; it requires fresh tests, preparation and review before any new launch. No original negative result is overwritten.

The earlier prepared-only report is preserved as REPORT-prelaunch.md. The following describes that historical preparation and the scope retained for this attempt.

Status: PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW. The saved preparation freezes 156 entries: 80 completed v2 qualification artifacts, 73 parent artifacts and three driver/protocol/test files. It validates the original saved cycle-zero density as float64, shape (3068, 3068), maximum asymmetry 2.220446049250313e-16. Preparation built no parent molecule and performed zero J calls or SCFs.

At the earlier publication checkpoint there was no independent-root-review.json, launch gate or run directory. Preparation session 6682 completed exit 0; publication did not launch the diagnostic. A later goal continuation bound root review to preparation SHA256 7cf62ef812fab3a3dadb0d74a19d3a311dc3a5aa9b419e6ea05fac638dd0cfae, passed the gate and launched exactly once (session 25950, child PID 63824). The frozen PROTOCOL.md retains its implementation-stage state without alteration.

The proposed single first-J call has a 300-second wall limit and 10-GiB sampled-RSS guard. It requires a separately bound root review before launch. Even a future PASS_BOUNDED_FIRST_J_ONLY would establish only completion of that Coulomb request within its checks, not parent SCF convergence, whole-SCF performance, chemical identity or physical admission.

The completed OpenMP v2 qualification supports retrospective agreement on saved small-reference inputs. The original failed runtime campaign, earlier parent wall limits and all partial results remain preserved. This attempt supplied setup-failure evidence, with zero verified integrated complements added.
