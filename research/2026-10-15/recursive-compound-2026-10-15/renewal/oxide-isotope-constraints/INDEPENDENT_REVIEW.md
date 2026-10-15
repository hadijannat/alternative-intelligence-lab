# Root source-extraction check

Before publication, root executed the existing read-only `verify_source.py` from the workspace evidence directory. It exited 0 and freshly extracted SI page 3 with `pdftotext`, checked publisher metadata and both file hashes, and compared every condition and site cell with the CSV.

All 17 rows and 119 site cells agree: 74 reported value/uncertainty pairs, three entries too fast to quantify without a numerical bound, and 42 unreported entries. The saved analysis agrees with its evidence copy. The main article remains unacquired; the supporting information is the measured-data source.

The report preserves Site A as molecular transformation, unknown log-base convention as an explicit arithmetic assumption, organic-buffer conditions, and missing uncertainty/covariance information. These source observations supply no target-specific renewal rate, new-material competence or integrated complement. This check performs no chemical calculation, fitting, or physical experiment.

Evidence: `.omo/evidence/oxide-isotope-constraints/verify_source.py`, `source-comparison.json`, and the publication receipt at the workspace root.
