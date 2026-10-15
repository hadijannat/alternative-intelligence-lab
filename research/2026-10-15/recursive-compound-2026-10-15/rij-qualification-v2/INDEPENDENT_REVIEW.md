# Independent numerical review

The read-only numerical reviewer independently recomputed saved arrays without launching new SCFs. The installed RKS convention g=2*C_virtual.T*F*C_occupied reproduces all four direct-Fock residual norms to approximately 1e-15. Neutral MoO3 and external Mo2O7 fail 0.001 Eh; the two MoO4 controls pass. Independent energy-error, matrix-error, incremental-additivity and electron-trace calculations agree with the report. Every recorded metric call reports Cholesky, finite J and no stored three-index tensor. Both campaigns' pinned source files still match; original failure records remain present.

Verdict: **FAIL_NUMERICAL_SCREEN confirmed.** Numerical consistency does not override failed method-admission criteria. Kernel times are not a controlled cold-start speed comparison.

Before launch the reviewer identified three software issues: aggregate acceptance ignored supervisor termination reasons; per-call metric status was not persisted; completed arrays could be lost on capped termination. All were corrected and checked before v1. The subsequent ECP metadata failure is preserved. Installed source confirms get_hcore/ECPscalar initializes environment slots18/19; v2 initializes these before the unchanged fingerprint. The real-ECP regression and ten other unit tests pass.

The next accuracy candidate is installed def2-universal-jkfit (basis registry line187 in this runtime), with spherical counts H18/O77/Mo255 rather than J-fit11/49/89. No calculation using that candidate has run. For the parent it would require19,612 auxiliary functions and3,077,044,352 bytes for one metric, or6,154,088,704 bytes for metric plus factor. Increased basis size does not guarantee accuracy and imposes a substantial resource penalty. It is not admitted and cannot reuse the prior parent preflight.

The same reviewer independently reproduced proton-topology edge counts212/220,212/220,216/220 and GUI declarations162Mo-O/32H-O/6Mo-Mo. Original topology result bytes remain unchanged; no physical bond or solution-identity conclusion follows.
