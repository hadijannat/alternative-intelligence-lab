# Deliverable evidence

No active attempt directory was returned by `omo-agent-toolkit ulw-loop status --json` (ULW_LOOP_PLAN_MISSING); evidence is under this owned directory's `.omo/evidence/`.

| Criterion/scenario | Exact invocation or inspection | Binary observable | Captured artifact |
|---|---|---|---|
| Bounded primary acquisition | `requests.get('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10284552/fullTextXML')`; `requests.get('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10284552/supplementaryFiles')` | HTTP200; supplementary member begins `%PDF`; hash verified | `raw/access.json`, `raw/article.xml`, `raw/supplements.zip`, `raw/supplement.pdf`, `sources.json` |
| Exact tested scope | Read main Methods/Table1 and SI captions; `python recursive-compound-2026-10-15/compatibility/check.py` | Ten listed POM entries;27 medium conditions; target/Mo36 absent; MES discrepancy explicit | `atlas_scope.json`, `.omo/evidence/checks.json`, `REPORT.md` |
| New phosphate failure constraint | Inspect SI S17/S18/S19 pages144/157/160; same checker invocation | Four selected phosphate PMo12 condition/stage rows have replicates0,0,0;99+1 assigned products; free phosphate excluded | `selected_rows.csv`, `raw/table-page-144.png`, `raw/table-page-157.png`, `raw/table-page-160.png` |
| Concrete recursive replacement | Inspect SI S8/S10/S11 pages67/83/87; same checker invocation | Four selected Dawson rows have replicates100,100,100; exact K salt identified; distinct actual pH retained | `selected_rows.csv`, `raw/table-page-67.png`, `raw/table-page-83.png`, `raw/table-page-87.png`, `REPORT.md` |
| Meaningful arithmetic and normalization guard | `python recursive-compound-2026-10-15/compatibility/check.py > recursive-compound-2026-10-15/compatibility/check-output.txt` | Exit0; exact nominal-to-measured pH differences; same conditional fraction with tenfold different recovery | `.omo/evidence/checks.json`, `check-output.txt` |
| Failed transfer and next test | Read REPORT sections Recursive decision and Next test | Full-system intersection explicitly unverified; differentiates observed starting-buffer comparator from common final mixture; proposed staged test present | `REPORT.md` |
| Access limitation | Attempt PHAIDRA object and metadata routes | No metadata/spectra acquired; empty HTTP200 not represented as data | `raw/access.json` |

First checker run failed because published D2O after-incubation mean74 differs from arithmetic mean(71,76,77)=74.6667 by more than normal integer rounding. The full check was rerun after recording this exact source discrepancy and requiring it to remain identified. The numerical phosphate and Dawson findings are unaffected. No chemical data were altered to make the test pass.

Automated checks validate dossier accounting and known limits only. Manual source table inspection, particularly denominator and material identity, remains separate from independent NMR integration; no raw integration was performed.
