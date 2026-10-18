# Independent functional-carrier review

Date: 2026-10-18. Scope: `documented-scaffold-2026-10-18/functional-carrier-search/PROTOCOL.md`, `extract_gtm3.py`, `assess.py`, `results/assessment.json`, and acquired primary packages. Read-only review of implementation and scientific source claims; only this review artifact was authored. No blocking defect found for the stated evidence/identifiability assessment. This is not approval of functional inheritance, integration, or the full goal.

## Findings

1. **Exact-source table parsing is correct.** Native primary XML Table 1 has catalyst cells with `rowspan="2"` for SS and RR. The saved JSON omits span attributes, but the source XML retains them and the current four-/three-cell parser correctly reconstructs this specific table. All four observations were independently checked against XML: SS `(50.7,-28.8,+23.8)`, `(99.4,-28.5,+17.5)`; RR `(60.2,+28.8,-22.3)`, `(99.5,+30.3,-19.0)`, in conversion/inversion-ee/retention-ee percent. No general rowspan parser is claimed or required.
2. **Seed recognition is distinguished from copied function.** Primary body lines 199-235 describe Si/Ge=8 secondary growth with both seed and EMPS handedness, 5%/10% seeds, 100 C for 72 h. The source describes higher crystallization rates; using endpoint progress as ordinal evidence is appropriately conservative. Table 1 is not identified as catalytic assays of these crossed offspring lots. Eight conditions, four sign disagreements, and zero observed offspring functions resolving them are internally correct. No copying rate or fidelity is estimated. The counterfactual sign convention is the **inversion-product ee** sign: retention-product signs are opposite. Keep that qualification in any short summary.
3. **Founder mixing uses product flux.** `weighted_ee` and the protocol correctly require the fraction of catalytic product flux, not starting seed mass. The function is valid for a common product category and common sign convention. No numeric founder fraction is inferred from 5%/10% feed-relative seeds. Parent-priority and cue-priority are logical witnesses of non-identifiability, not reaction kinetics or an exhaustive mechanism set.
4. **Boundary dataset quarantine is justified.** Native accepted PDF identifies DOI 10.1016/j.memsci.2020.117855 and links data DOI 10.25405/data.ncl.9610601. Native README names the different dendritic-silver paper and states drilled-channel area 0.18 cm2 after a 41.37% porosity correction. This source mapping ambiguity is retained; hashes alone do not resolve it. Independent column-pair inventory matches assessment exactly. Raw missing entries, negative fluxes, and late observations remain in the source bytes. The executable does not invent timestamps, clamp flux, fit kinetics, or label late rises spontaneous failure.
5. **No result promotes a complement or completes the goal.** Assessment explicitly records `fit_allowed=false`, `functional_inheritance_identified=false`, null `copying_fidelity`, zero integrated additions, and `full_goal_complete=false`. GTM-3 SI confirms 550 C/12 h calcination and inert handling to avoid ambient humidity; these constraints preclude casually assuming aqueous POM compatibility. Source SI also reports catalyst reuse, which is not new-material inheritance.

## Executed verification and captured observables

Interpreter: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`. Calls used `-c` with standard-library imports, existing PyMuPDF, and importlib loading of `assess.py`; `main()` was not called, so assessment/source files were not regenerated.

Scenario: source and frozen-analysis integrity. Invocation operations: `assert digest(PROTOCOL.md)==PROTOCOL_SHA==assessment["protocol_sha256"]`; `assert digest(assess.py)==assessment["analysis_sha256"]`; recompute SHA256 for every GTM receipt and boundary checksum entry and MD5 against the three repository expected values. Binary observable: all assertions passed, exit 0. Protocol SHA256: `2e8fc310cbe13cdd163f7cb9a54f703cdd85ed44bff66501e7a7cfac7494749c`; analysis SHA256: `349faaad455ea2d12e4299cef4c4af7eecb24511ed207e347377f23bb30b6884`. Captured artifact: this review; comparison artifacts: `sources/gtm3/receipt.json`, `sources/boundary/checksums.json`, `results/assessment.json` under the scoped directory.

Scenario: native table and document validation. Invocation operations: `ElementTree.parse(article.xml).findall(".//table-wrap/table/tbody/tr")`, asserting first-cell rowspans `["2","1","2","1"]`; compare `catalytic_rows()` to saved rows and the four explicit triples above; `fitz.open` page counts. Binary observable: all assertions passed, SI 24 pages, accepted boundary PDF 20 pages. Captured artifact: this review; native evidence: `sources/gtm3/article.xml`, `sources/gtm3/supporting-information.pdf`, `sources/boundary/kazakli2020.pdf`.

Scenario: independent CSV inventory. Invocation: a separate `python3 -c` standard-library CSV pass, independently looping the two time/value pairs, classifying empty/`--` as missing, counting orphan fields and valid pairs, and asserting the resulting dictionaries equal saved assessment inventory. No call to `csv_inventory` was used in this independent pass. Binary observable: exit 0 and the following captured counts:

| File/channel | Valid pairs | Orphan fields | Negative flux pairs | Maximum time | Pairs after 83 h |
|---|---:|---:|---:|---:|---:|
| Figure4 N2 | 2963 | 0 | 887 | 52.75261 | 0 |
| Figure4 CO2 | 6331 | 0 | 0 | 52.75 | 0 |
| Figure5 N2 | 43536 | 3 | 6793 | 111.32667 | 11079 |
| Figure5 CO2 | 13273 | 30266 | 0 | 110.68333 | 3322 |

All minimum times are 0.0. Figure4 has 7679 data rows; Figure5 has 43539. First orphan source lines, including header, are Figure5 N2 29728 and CO2 12. Captured artifact: this table; source bytes and expected values: boundary CSVs plus assessment inventory.

Scenario: admission boundaries. Invocation operations: assert eight crossed conditions, four disagreements, all measured offspring signs null; assert no fitted boundary model, no full completion, no integrated addition. Binary observable: all assertions passed, exit 0. Captured artifact: this review and scoped `results/assessment.json`.

Scenario: fresh AuPd primary accessibility. Invocation: `web.run` opens of `https://pubs.rsc.org/en/content/articlehtml/2021/nr/d1nr04400a` and `https://www.rsc.org/suppdata/d1/nr/d1nr04400a/d1nr04400a1.pdf`. Binary observable: publisher article 403; SI 404. The prior indexed-source assertions in `sources/nanoparticle/SCREEN.md` were therefore not independently reproduced in this review. Its explicit access limitations and absence of local native PDF are correctly disclosed. Do not elevate this screen to a newly acquired native primary package or use it for a fitted daughter rate.

Scenario: active attempt lookup. Invocation: `omo-agent-toolkit ulw-loop status --json`. Observable: exit 1, `ULW_LOOP_PLAN_MISSING`; no current attempt directory returned. Review evidence saved in `.omo/evidence/` accordingly.

## Limits

No physical experiments, held-out chemical validation, general parser robustness claim, or quantitative parent-to-descendant kinetic model was checked. The AuPd indexed source could not be refreshed; raw boundary provenance remains unresolved. The evidence supports unresolved inheritance and rejected integration, with all source negatives preserved.
