# Original RI-J campaign: software failure retained

All four children terminated normally with returncode1 and ERROR outcomes; no resource guard was triggered. Protocol and code pins remained unchanged. This is an implementation failure, not rejection of the proposed chemistry or demonstrated RI-J inadequacy.

The three known small references completed their initial, perturbed and direct-converged density comparisons, zero-density and incremental-additivity checks. All completed checks passed the predeclared screens. Maximum J error across these records was0.0005275551Eh and maximum absolute Coulomb energy error perMo0.0001826489Eh. None completed an RI SCF: the first core-Hamiltonian evaluation initializes PySCF's ECP routing metadata, and the strict unchanged-environment guard rejected that internal bookkeeping change.

The external Mo2O7 direct reference converged in24cycles at−662.8343295753588Eh,52.907seconds. Its first RI operator call was rejected by the same guard, so no external RI prediction or error was obtained. This geometry is a numerical challenge, not a measured species/minimum or experimental holdout.

A separate diagnostic on the MoO4 case found exactly two changed environment indices:18/19, named AS_ECPBAS_OFFSET/AS_NECPBAS, from0/0 to35/4. These are native ECP routing fields; they do not encode changed atom coordinates or exponents. The separately frozen sibling rij-qualification-v2 initializes get_hcore before installing the unchanged guard. Its limits and numerical thresholds are unchanged. This original driver, wrapper, protocol, partial arrays, exceptions, native logs and supervisor receipts remain intact. No automatic retry occurred.

Prior design review found and repaired aggregate supervisor acceptance and partial-evidence persistence before this run. Ten synthetic/mocked software tests passed; they did not expose the ECP initialization interaction. An added ECP regression belongs to v2. No parent calculation or chemical-function admission follows from either software tests or completed matrix comparisons.
