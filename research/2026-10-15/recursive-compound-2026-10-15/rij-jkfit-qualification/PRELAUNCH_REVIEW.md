# Prelaunch review

Independent read-only review cleared exactly one five-case run after the preparation freeze. All 30 preparation pins and original v2 pins matched. `preparation.json` recorded zero SCFs and `run-v1` did not exist. The new XYZ matches all eleven atoms of the deposited output final geometry exactly; the ADF input contains earlier coordinates. Output charge zero and restricted spin support the neutral input guard.

Four cases reuse direct references; only the new external case computes a new direct reference. The maximum is six new SCFs. Accuracy thresholds, full solvent-aware direct-Fock residual, cache/fallback receipts and terminal supervisor acceptance were reviewed without a numerical run. No parent resource or chemical admission follows.

Root ran the updated tests once: 14 passed in 0.049 seconds, exit 0. The earlier `evidence/tests.txt` records 13 and remains historical. The exact updated command/output is saved in workspace `.omo/evidence/jkfit-source-preparation.json`. The added charge guard has eight negative subcases.
