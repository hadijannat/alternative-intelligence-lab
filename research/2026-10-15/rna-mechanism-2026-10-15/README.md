# RNA mechanism revision

This investigation diagnoses the failed R3C/POPC model, compares a frozen set of reduced chemical mechanisms, and reviews new public retention/inheritance data. Previous models and results remain intact in [the preceding laboratory](../measured-coupling-2026-10-15/REPORT.md).

Entry points:

- [Investigation report](REPORT.md): diagnosis, revised models, measured outcomes, new datasets and remaining measurements.
- [WORKPLAN.md](WORKPLAN.md): scope and completion requirements.
- [Diagnosis](diagnosis-v1/diagnosis.json): exact replay and condition-level decomposition of the old bulk failure.
- [Model protocol](model/PROTOCOL.md): whole-dose cross-validation, source-supported reaction candidates and historical benchmark limits.
- [Salibi source audit](sources/salibi/audit.md): verified old extraction, additional workbook observations and chemical interpretation.
- [Retention data](sources/retention/REPORT.md): new partition/function and exchange datasets with explicit observation limits.
- [Inheritance data](sources/inheritance/REPORT.md): sequence/function and network-composition data, acquisition limits and condition ledger.
- [Model results and reproduction](model/README.md): executable chemistry, preserved attempts and completed results-v2.
- [Verification](checks.md): complete offline extraction/refit/replay and numerical evidence.
- [Independent review](review-independent.md): no blockers for the bounded investigation.
- [Progress](progress.md): current completion state.

Outcome: whole-dose CV RMSE changes from 9.798 to 9.509 pp, while bulk fit worsens from 7.866 to 7.893 pp. Both exchange models and all eight active-retention scenarios fail the declared historical accuracy screen. The revised mechanism is not validated; active-F1 retention and functional compartment inheritance remain unidentified. Old holdouts are now development information.

Keep this directory next to `measured-coupling-2026-10-15`, whose retained workbook and original baseline are read without modification. From the workspace root, the tested full replay command is:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-mechanism-2026-10-15/run_suite.py --output rna-mechanism-2026-10-15/verification-reproduction
```

Use an unused output directory. The installed PyMuPDF 1.27.2.3 is also required for source extraction; all observed versions are in `requirements.txt` and the verification receipt. The completed full replay took about six minutes on this machine and used no network downloads.
