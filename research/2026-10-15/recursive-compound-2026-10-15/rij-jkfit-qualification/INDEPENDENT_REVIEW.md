# Independent terminal numerical audit

Verdict: CLEAR for `PASS_NUMERICAL_SCREEN_ONLY`, with no parent or chemical admission. A separate read-only agent recomputed the J discrepancies, Coulomb contractions, zero/additivity tests, orbital gradients from the stored direct and RI Fock matrices, electron traces and energy comparisons for all five cases. It launched no SCF and changed no artifacts.

All101 checks pass. Recomputed worst values: J2.7911080172060565e-4Eh; absolute Coulomb error/Mo1.742510526255895e-4Eh; total-energy error/Mo7.544349648469506e-5Eh; direct-Fock residual1.8679534416450065e-4; RI residual2.657395962853147e-7; trace error6.394884621840902e-14; additivity1.652011860642233e-12. Symmetry and zero-density errors are zero. Orbital gradients used the occupied/virtual projection including the RKS factor2 and the full solvent-aware Fock.

The four reused direct densities and energies match the prior campaign exactly. All30 pins still match. All148 native metric receipts report Cholesky/finite J/no stored three-index tensor; storage records contain no ERI cache. All five supervisor receipts have returncode0, no termination reason and no monitor error. Worst wall time150.6173seconds and sampled RSS624,345,088bytes remain within their declared caps.

Scope: four retrospective comparisons and one new external numerical geometry. No parent feasibility, general chemical accuracy, physical stability, experimental validation or controlled speedup was demonstrated. Original jfit and initialization failures remain separate retained evidence.
