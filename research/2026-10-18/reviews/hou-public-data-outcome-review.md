# Independent Hou native-result review

Reviewed 2026-10-18. Scope: read-only code, scientific interpretation, provenance, and independent numerical verification. This reviewer wrote only this report. No active attempt directory was returned by `omo-agent-toolkit ulw-loop status --json` (exit 1, ULW_LOOP_PLAN_MISSING), so evidence is recorded under .omo/evidence.

## Verdict and actionable finding

PASS for the frozen descriptive arithmetic, all-record retention, current-trace implementation, and synthetic checks. No calculation defect found. Physical recovery interpretation of the frozen same-index FE pairs is BLOCKED by a source-label/figure semantic mismatch. This finding must be carried into the final report; it does not require changing the frozen calculation.

Direct inspection of native publisher image `sources/hou-fig5.png` shows panel e ordered as initial high bar, deactivation low bar, twice high bar, deactivation low bar, three-times high bar, deactivation low bar. The 10-hour arrows lead down within each pair. The self-healing arrows lead from the first low bar to the second high bar and from the second low bar to the third high bar. Thus workbook labels `origina-N` and `selfhealing-N` do not themselves identify a damaged-before/healed-after intervention comparison. The literal ratios 0.8485499462943072, 0.8448087431693989, 0.8452115812917596 describe the six native values correctly, but are consistent with within-cycle decline shown in the figure, not evidence that regeneration failed. Preserve the original result and its false `nominal_recovery` flags as the frozen literal test outcome; explicitly state that the planned physical-recovery interpretation is unsupported by that pairing. Any new cross-pair calculation must be separately identified as post hoc; no such calculation was executed in this review.

The plotted axis explicitly reads FE of formate (%), while the workbook cells remain unlabeled. Original `difference_native` fields should stay literal. No precision, specimen pairing, independent replication, statistical uncertainty, or new causal claim follows from reconciling the figure.

## Verified scope and bounds

All eleven retentions are below one. This establishes lower recorded current magnitude in the late window relative to the early window for each included record. It does not independently establish catalyst damage, formate production loss, full-transient removal, autonomous repair, or failure of physical regeneration. No timepoint-derived confidence intervals or p-values, cross-column current-amplitude comparison, FE-times-current trajectory, decay-rate fit, prediction, or physical replication is present in the reviewed calculation.

The exact same three FE pairs and all eleven prescribed time/current pairs are retained. The native result has no parsing errors or excluded traces, and retains the documented blank tails. All protocol/result hashes and acquisition receipt sizes/hashes match current bytes, including the frozen TEST_PROTOCOL SHA256 0aa3857b762953d98358f405e139538efa622f61b0f7bbed7dd1a4f0174dc825. The image resource name and workbook download URL are linked directly in the captured publisher HTML. Image bytes match the independent acquisition receipt SHA256 9a076caf64e9c24ecd1aa2810c1cf4bf10983368cf5e360ab7e8f4b99018d8f4.

The earlier protocol review records clarification hash d12bb737e6b09273e489a1b7978b40c39a66cb2dcdabf16d705ba9c81511f1dc; the native result and current clarification match 9d6ebb159ac81eca4f1413e453ebd6b41dd1a181e1b4a545bac74ad4287d8dc2. The current clarification includes the reviewer’s interpretation bounds. This report approves that current text retrospectively; it does not independently establish the order of historical filesystem writes. Do not claim that the older review attests to the exact later clarification bytes.

Methods directly describe electrode removal, mechanical stirring/redispersion, 30-minute rest, reduction potential, and electrolyte renewal every cycle. Initial preparation states 0.2 g Bi2O3 with 4 g Ga, while regeneration states 0.2 g Bi2O3 with 4.5 g Ga; those conditions cannot silently be pooled as identical. PLA apparatus and external electrical/mechanical/thermal inputs are explicit. The protocol additionally records Nafion separator, bicarbonate/CO2 medium, unestablished specimen linkage and absent matched refresh/stir-only comparisons. Source structural phase evidence supports a Bi-regeneration interpretation under the combined treatment; it does not establish integrated R/J or independent H/V.

All twelve I/E/T/B/R/H/V/S/M/A/J/C integrated requirements remain unclosed. The result’s `full_integrated_requirements_closed` is the empty list, as independently asserted. No PMo12 integration or serial functional inheritance was tested.

## Verification scenarios

All paths below are relative to the workspace; base B is `documented-scaffold-2026-10-18/public-primary-datasets-resumed`. This report is the captured artifact for the invocations and actual outputs. Native source paths and result JSON are retained artifacts.

| Scenario | Exact invocation | Binary observable | Captured artifact |
|---|---|---|---|
| Native FE arithmetic and all eleven estimators | `python3 -B -` with the complete script below, workspace cwd | Exit 0; 3 exact FE matches; 11 traces match with rel_tol=1e-12, abs_tol=1e-14; maximum absolute difference across means and retentions 3.552713678800501e-15 | This report, script and raw output; B/sources/hou-source.xlsx; B/results/hou-test.json |
| Source/result/protocol provenance | Same script: SHA256/byte-length assertions against source receipts and every result provenance entry | Exit 0; all receipt and provenance predicates true | This report raw output; B/sources/receipt.json; B/sources/figure5-acquisition.json |
| Every intended record and failure handling | Same script count/tail assertions; `python3 -B -m unittest -v test_analyze_hou` from B | Exit 0; 3+11 records; malformed/header/hash/nonpositive/missing-sheet cases retained without partial estimates | This report full unittest output; B/test_analyze_hou.py |
| Integration correctness under sparse, irregular, sign-changing samples | Same unittest invocation | Exit 0; linear-time invariance, piecewise kink, magnitude-before-interpolation and window-coverage tests pass | This report full unittest output |
| Frozen output immutability | Same unittest invocation | Exit 0; output exclusive-create and finite-JSON tests pass; frozen protocol change blocks source access | This report full unittest output |
| Published FE semantics | `tools.view_image({path: absolute B/sources/hou-fig5.png})`; inspect panel e; BeautifulSoup find image/link targets in B/sources/hou-main.html | PASS for identified deactivation/self-healing arrow direction; FAIL for the planned physical recovery interpretation of same-index native pairs | B/sources/hou-fig5.png; B/sources/hou-main.html; this report finding |
| Full-goal and scientific scope | Read PROTOCOL.md, TEST_PROTOCOL.md, TEST_CLARIFICATION.md, analyze_hou.py, native result and prior protocol review | PASS: no integrated requirements credited; no CI/p-values/FE-current trajectory/prediction/physical replication | Named files and this report |

The independent arithmetic implementation uses only standard-library ZIP/XML parsing and NumPy interpolation/trapezoidal integration. It never imports or calls the analyzer’s estimator for native data. The separate synthetic-suite subprocess does import the analyzer, as expected. Its fifteen test cases exercise branch behavior and malformed inputs without counting synthetic successes as chemical evidence. The numerical comparison tolerance is floating-point verification tolerance only, not a scientific effect threshold.

## Reproducible independent script

Invocation: `python3 -B - <<'PY'` followed by the code below and closing `PY`, from workspace cwd.

```python
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET,subprocess,sys,math
import numpy as np
B=Path("documented-scaffold-2026-10-18/public-primary-datasets-resumed")
R=json.loads((B/"results/hou-test.json").read_text())
N={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
audit={"runtime":{"python":sys.version,"numpy":np.__version__},"provenance":[],"efficiency":[],"traces":[]}
for name,item in R["provenance"].items():
 actual=hashlib.sha256((B/name).read_bytes()).hexdigest()
 assert actual==item["sha256"],name
 audit["provenance"].append({"path":str(B/name),"sha256":actual,"matches_result":True})
for receipt_name in ("receipt.json","figure5-acquisition.json"):
 rec=json.loads((B/"sources"/receipt_name).read_text())
 for item in rec.get("requests",[rec]):
  p=B/"sources"/item["name"]; data=p.read_bytes()
  assert len(data)==item["bytes"] and hashlib.sha256(data).hexdigest()==item["sha256"],str(p)
audit["receipts_match_bytes"]=True
audit["result_sha256"]=hashlib.sha256((B/"results/hou-test.json").read_bytes()).hexdigest()
audit["workbook_sha256"]=hashlib.sha256((B/"sources/hou-source.xlsx").read_bytes()).hexdigest()
assert audit["workbook_sha256"]==R["workbook"]["expected_sha256"]
with zipfile.ZipFile(B/"sources/hou-source.xlsx") as z:
 shared=["".join(e.itertext()) for e in ET.fromstring(z.read("xl/sharedStrings.xml"))]
 rel={e.attrib["Id"]:e.attrib["Target"] for e in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
 sheets={}
 for e in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets",N):
  t=rel[e.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
  sheets[e.attrib["name"]]=t.lstrip("/") if t.startswith("/") else "xl/"+t
 def rows(name):
  with z.open(sheets[name]) as stream:
   for _,e in ET.iterparse(stream,events=("end",)):
    if e.tag!="{"+N["m"]+"}row": continue
    cells={}
    for c in e:
     if c.tag!="{"+N["m"]+"}c": continue
     v=c.find("m:v",N)
     if v is None: continue
     assert c.find("m:f",N) is None,"formula"
     cells[c.attrib["r"]]=shared[int(v.text)] if c.attrib.get("t")=="s" else float(v.text)
    yield int(e.attrib["r"]),cells
    e.clear()
 fe=dict(rows("Fig. 5e"))
 for k,row in enumerate((3,6,9),1):
  a,b=fe[row][f"B{row}"],fe[row+1][f"B{row+1}"]
  assert fe[row][f"A{row}"]==f"origina-{k}" and fe[row+1][f"A{row+1}"]==f"selfhealing-{k}"
  old=R["efficiency"][k-1]
  assert b/a==old["healed_original_ratio"] and b-a==old["difference_native"]
  audit["efficiency"].append({"pair":k,"original":a,"selfhealing":b,"ratio":b/a,"difference_native":b-a,"exact_match":True})
 for name,count in (("Supplementary Fig. 16",3),("Supplementary Fig. 18",8)):
  pairs=[(chr(65+3*i),chr(66+3*i)) for i in range(count)]
  coords={p:[] for p in pairs};tails={p:0 for p in pairs};seen={p:False for p in pairs}
  for row,c in rows(name):
   if row<5: continue
   for p in pairs:
    a,b=c.get(p[0]+str(row)),c.get(p[1]+str(row))
    if a is None and b is None:
     tails[p]+=1; seen[p]=True; continue
    assert not seen[p],"internal empty row"
    assert isinstance(a,float) and isinstance(b,float) and math.isfinite(a) and math.isfinite(b)
    coords[p].append((a,b))
  for p,data in coords.items():
   v=np.asarray(data);t=v[:,0];m=np.abs(v[:,1]);assert np.all(np.diff(t)>0)
   u=(t-t[0])/(t[-1]-t[0])
   means=[]
   for lo,hi in ((.1,.2),(.9,1.)):
    x=np.concatenate(([lo],u[(u>lo)&(u<hi)],[hi]))
    y=np.interp(x,u,m)
    means.append(float(np.trapezoid(y,x)/(hi-lo)))
   retention=means[1]/means[0]
   old=next(x for x in R["traces"] if x["sheet"]==name and x["time_column"]==p[0])
   deltas=[abs(a-b) for a,b in zip(means+[retention],[old["early_mean_magnitude_native"],old["late_mean_magnitude_native"],old["retention"]])]
   assert all(math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-14) for a,b in zip(means+[retention],[old["early_mean_magnitude_native"],old["late_mean_magnitude_native"],old["retention"]]))
   assert len(data)==old["finite_pair_count"] and tails[p]==old["trailing_fully_empty_rows"]
   audit["traces"].append({"sheet":name,"columns":"/".join(p),"count":len(data),"trailing_empty":tails[p],"early":means[0],"late":means[1],"retention":retention,"max_abs_difference":max(deltas),"match":True})
assert len(audit["traces"])==11 and len(audit["efficiency"])==3
assert R["errors"]==[] and R["excluded_traces"]==[] and R["full_integrated_requirements_closed"]==[]
assert R["counts"]=={"efficiency_attempted":3,"traces_attempted":11,"efficiency_valid":3,"traces_valid":11}
audit["all_records_and_limits"]=True
run=subprocess.run([sys.executable,"-B","-m","unittest","-v","test_analyze_hou"],cwd=B,capture_output=True,text=True)
audit["synthetic_tests"]={"invocation":"python3 -B -m unittest -v test_analyze_hou","cwd":str(B),"returncode":run.returncode,"stdout":run.stdout,"stderr":run.stderr}
assert run.returncode==0
print(json.dumps(audit,indent=2))

```

## Captured output

Process exit code: 0.

```json
{
  "runtime": {
    "python": "3.12.3 (main, May  9 2025, 22:01:02) [Clang 17.0.0 (clang-1700.0.13.3)]",
    "numpy": "2.4.1"
  },
  "provenance": [
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/PROTOCOL.md",
      "sha256": "1f3eb5253caf78a8a12e8d0a655c05f47b5907b0f9d083b9687a3920fb5ea70b",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/TEST_PROTOCOL.md",
      "sha256": "0aa3857b762953d98358f405e139538efa622f61b0f7bbed7dd1a4f0174dc825",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/TEST_CLARIFICATION.md",
      "sha256": "9d6ebb159ac81eca4f1413e453ebd6b41dd1a181e1b4a545bac74ad4287d8dc2",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/analyze_hou.py",
      "sha256": "fae0f24dae7def6833d898f3a1ec7ac536f80665dc76364fbf2689f2dc5b9899",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/test_analyze_hou.py",
      "sha256": "f1c08844f50ae23c4e1ed87b32281a1e543cf58dade5101d5eec894a1e9f0d09",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/native-inventory.json",
      "sha256": "7d024337bdb4d9dff3829f7fb404fb712659820edcd71b9380635621f4ae59bd",
      "matches_result": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/time-axis-schema.json",
      "sha256": "fa27ecd46be8911f86ca217839cd3efaffaa5242d1e5ede9f92bc10cfe25d8ad",
      "matches_result": true
    }
  ],
  "efficiency": [
    {
      "pair": 1,
      "original": 93.1,
      "selfhealing": 79,
      "ratio": 0.8485499462943072,
      "difference_native": -14.099999999999994,
      "exact_match": true
    },
    {
      "pair": 2,
      "original": 91.5,
      "selfhealing": 77.3,
      "ratio": 0.8448087431693989,
      "difference_native": -14.200000000000003,
      "exact_match": true
    },
    {
      "pair": 3,
      "original": 89.8,
      "selfhealing": 75.9,
      "ratio": 0.8452115812917596,
      "difference_native": -13.899999999999991,
      "exact_match": true
    }
  ],
  "traces": [
    {
      "sheet": "Supplementary Fig. 16",
      "columns": "A/B",
      "count": 180003,
      "trailing_empty": 0,
      "early": 8.628328714322715,
      "late": 5.231749024731033,
      "retention": 0.6063455853329415,
      "max_abs_difference": 1.7763568394002505e-15,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 16",
      "columns": "D/E",
      "count": 180001,
      "trailing_empty": 2,
      "early": 0.006723820382014021,
      "late": 0.005598844421944247,
      "retention": 0.8326879815113675,
      "max_abs_difference": 1.1102230246251565e-16,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 16",
      "columns": "G/H",
      "count": 180001,
      "trailing_empty": 2,
      "early": 0.008207189352863062,
      "late": 0.0051584284770237725,
      "retention": 0.6285255835146858,
      "max_abs_difference": 0,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "A/B",
      "count": 20000,
      "trailing_empty": 4,
      "early": 7.411408082518194,
      "late": 6.549794192294611,
      "retention": 0.8837449131621923,
      "max_abs_difference": 0,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "D/E",
      "count": 20000,
      "trailing_empty": 4,
      "early": 7.156492123136504,
      "late": 6.376411648218696,
      "retention": 0.8909968094010954,
      "max_abs_difference": 1.7763568394002505e-15,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "G/H",
      "count": 20004,
      "trailing_empty": 0,
      "early": 9.980512145293746,
      "late": 6.74176577573132,
      "retention": 0.6754929684555678,
      "max_abs_difference": 0,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "J/K",
      "count": 20000,
      "trailing_empty": 4,
      "early": 7.247601555454006,
      "late": 6.460473543736327,
      "retention": 0.8913946902716604,
      "max_abs_difference": 8.881784197001252e-16,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "M/N",
      "count": 20000,
      "trailing_empty": 4,
      "early": 8.545054976217214,
      "late": 5.633093745133663,
      "retention": 0.6592226452388913,
      "max_abs_difference": 1.7763568394002505e-15,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "P/Q",
      "count": 20004,
      "trailing_empty": 0,
      "early": 8.273271837296107,
      "late": 7.285768806299485,
      "retention": 0.8806393588392762,
      "max_abs_difference": 0,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "S/T",
      "count": 20000,
      "trailing_empty": 4,
      "early": 13.165070067424601,
      "late": 9.346015682143566,
      "retention": 0.7099100600511933,
      "max_abs_difference": 3.552713678800501e-15,
      "match": true
    },
    {
      "sheet": "Supplementary Fig. 18",
      "columns": "V/W",
      "count": 20004,
      "trailing_empty": 0,
      "early": 7.991653299034194,
      "late": 6.638258750830456,
      "retention": 0.8306489911959396,
      "max_abs_difference": 0,
      "match": true
    }
  ],
  "receipts_match_bytes": true,
  "result_sha256": "52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36",
  "workbook_sha256": "3319d65a2cfc4fa43f1ea78b906b5be2a5987d5efa928f1312beaeb38f843315",
  "all_records_and_limits": true,
  "synthetic_tests": {
    "invocation": "python3 -B -m unittest -v test_analyze_hou",
    "cwd": "documented-scaffold-2026-10-18/public-primary-datasets-resumed",
    "returncode": 0,
    "stdout": "",
    "stderr": "test_bad_trace_value_and_header_remain_visible (test_analyze_hou.HouAnalysisTests.test_bad_trace_value_and_header_remain_visible) ... ok\ntest_cli_provenance_and_frozen_protocols (test_analyze_hou.HouAnalysisTests.test_cli_provenance_and_frozen_protocols) ... ok\ntest_hash_mismatch_never_opens_workbook_and_retains_failures (test_analyze_hou.HouAnalysisTests.test_hash_mismatch_never_opens_workbook_and_retains_failures) ... ok\ntest_linear_trace_irregular_grid_and_time_unit_invariance (test_analyze_hou.HouAnalysisTests.test_linear_trace_irregular_grid_and_time_unit_invariance) ... ok\ntest_malformed_traces_are_refused_without_partial_estimates (test_analyze_hou.HouAnalysisTests.test_malformed_traces_are_refused_without_partial_estimates) ... ok\ntest_missing_sheet_retains_all_eight_attempts (test_analyze_hou.HouAnalysisTests.test_missing_sheet_retains_all_eight_attempts) ... ok\ntest_nonpositive_fe_and_separator_refusal (test_analyze_hou.HouAnalysisTests.test_nonpositive_fe_and_separator_refusal) ... ok\ntest_output_is_finite_json_and_cannot_overwrite (test_analyze_hou.HouAnalysisTests.test_output_is_finite_json_and_cannot_overwrite) ... ok\ntest_piecewise_kink_requires_area_integration (test_analyze_hou.HouAnalysisTests.test_piecewise_kink_requires_area_integration) ... ok\ntest_protocol_change_blocks_before_workbook_access (test_analyze_hou.HouAnalysisTests.test_protocol_change_blocks_before_workbook_access) ... ok\ntest_sign_changes_use_sampled_magnitudes_before_interpolation (test_analyze_hou.HouAnalysisTests.test_sign_changes_use_sampled_magnitudes_before_interpolation) ... ok\ntest_synthetic_workbook_all_records_and_single_sheet_passes (test_analyze_hou.HouAnalysisTests.test_synthetic_workbook_all_records_and_single_sheet_passes) ... ok\ntest_trailing_empty_rows_counted_but_leading_blank_is_invalid (test_analyze_hou.HouAnalysisTests.test_trailing_empty_rows_counted_but_leading_blank_is_invalid) ... ok\ntest_window_coverage_is_required (test_analyze_hou.HouAnalysisTests.test_window_coverage_is_required) ... ok\ntest_wrong_efficiency_label_fails_only_corresponding_pair (test_analyze_hou.HouAnalysisTests.test_wrong_efficiency_label_fails_only_corresponding_pair) ... ok\n\n----------------------------------------------------------------------\nRan 15 tests in 0.048s\n\nOK\n"
  }
}
```

No new third-party source code, scientific data download, outcome rewriting, or numerical post hoc recovery contrast was performed. The figure was already acquired by the root worker; this reviewer inspected its saved bytes. The final root report/plot/registry were still being composed and are not audited here. A lightweight memory search supplied no source premise or historical claim used in this review; all conclusions above derive from current inspected artifacts.



## Post-execution stage-reconciliation audit

Additional review requested by root. Read STAGE_MAPPING_AMENDMENT.md, reconcile_hou_stages.py, results/hou-stage-mapping.json, REPORT.md and DATASET_REGISTRY.md. Independent Decimal arithmetic confirms all six original FE values, all three start/initial-start ratios, all three within-cycle ratios, and exactly two source-defined recovery transitions. Both increments are 12.5 percentage points; their next-start/deactivated ratios are 1.1582278481012658 and 1.1617076326002587. No third recovery endpoint is invented. The original result hash remains 52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36. Every stage result provenance hash matches its current artifact.

The amendment explicitly identifies post-execution timing and preserves the original mistaken physical interpretation rather than converting it into a blinded success. The current report gives the combined treatment interpretation, known source limitations, no predictive/independent physical validation, and twelve unclosed integrated requirements. These changes address the original scientific interpretation blocker.

A concrete bibliographic error was sent to root: DOI 10.1021/jacs.4c16883 is authored by Idrees, Reuven and Markovich, not Hananel. Native main XML and Figshare author metadata independently agree. Directory names may retain historical labels; human-facing author references should be corrected. Final resolution and final plot/checks/handoff approval are recorded below when ready.

Direct native Idrees verification confirms the main XML and repository JSON byte hashes, main CC BY 4.0 license and repository CC BY-NC 4.0 SI license. The primary methods/results connect seed-produced, purified nanocrystals with the adsorption assay, describe approximately 1% synthesis-volume seed transfer, and give an estimated residual-TA concentration below 10µM. This does not independently bound surviving-founder functional adsorption. The root SI file is a 71-byte HTTP500 JSON body; the alternate route is a zero-byte HTTP202 body. Neither is a PDF. The review did not independently reacquire scout-only transient PDFs, restricted files or the large Dryad archive; registry wording preserves those access distinctions. Bibliographic/metadata claims for other scout-screened entries are not fresh acquisition checks by this reviewer.

Additional native Hou checks directly confirm 21 SI pages, 24 workbook sheets, CC BY4.0 link, and the main-methods lowercase nafion117 separator text. Root methods/figure claims are consistent with inspected native records.

### Stage-audit invocation and artifact

Scenario: ensure post hoc correction changes mapping, not original observations, and verify source-access distinctions. Invocation: `python3 -B -` with the following script, workspace cwd. Binary observable: exit0 and all assertions pass. Captured artifact: this script/output section, results/hou-stage-mapping.json, unchanged results/hou-test.json, native main.xml/deposit.json/receipt.json and failed SI body. This independent arithmetic check executes no new scientific fit and never changes the original JSON.

```python
from pathlib import Path
import json,hashlib,math,xml.etree.ElementTree as E
from decimal import Decimal
B=Path("documented-scaffold-2026-10-18/public-primary-datasets-resumed")
r=json.loads((B/"results/hou-stage-mapping.json").read_text())
old=(B/"results/hou-test.json").read_bytes()
assert hashlib.sha256(old).hexdigest()=="52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36"
for p,h in r["provenance"].items(): assert hashlib.sha256((B/p).read_bytes()).hexdigest()==h,p
starts=["93.1","91.5","89.8"];ends=["79.0","77.3","75.9"]
for i,c in enumerate(r["cycles"]):
 assert c["cycle"]==i+1 and c["start_percent"]==float(starts[i]) and c["after_ten_hours_percent"]==float(ends[i])
 assert math.isclose(c["within_cycle_fe_retention"],float(Decimal(ends[i])/Decimal(starts[i])),rel_tol=1e-15)
 assert math.isclose(c["start_initial_start_ratio"],float(Decimal(starts[i])/Decimal(starts[0])),rel_tol=1e-15)
assert len(r["cycles"])==3 and len(r["displayed_recovery_arrows"])==2
transitions=[]
for i,t in enumerate(r["displayed_recovery_arrows"]):
 before=Decimal(ends[i]);after=Decimal(starts[i+1])
 assert t["deactivated_row"]==[4,7][i] and t["next_start_row"]==[6,9][i]
 assert t["before_percent"]==float(before) and t["after_percent"]==float(after)
 assert math.isclose(t["next_start_deactivated_ratio"],float(after/before),rel_tol=1e-15)
 assert t["difference_percentage_points"]==float(after-before)
 transitions.append({"rows":[t["deactivated_row"],t["next_start_row"]],"decimal_ratio":str(after/before),"decimal_difference":str(after-before),"pass":True})
assert r["unobserved_third_recovery"] is None and r["full_integrated_requirements_closed"]==[] and not r["predictive_validation"] and r["fitted_parameters"]==0
H=B/"sources/hananel2025"
rec=json.loads((H/"receipt.json").read_text())
for item in rec["requests"]:
 data=(H/item["name"]).read_bytes()
 assert len(data)==item["bytes"] and hashlib.sha256(data).hexdigest()==item["sha256"]
assert not (H/"si.pdf").read_bytes().startswith(b"%PDF")
m=E.fromstring((H/"main.xml").read_bytes())
authors=[" ".join("".join(x.itertext()) for x in c.findall("name/*")) for c in m.findall(".//article-meta/contrib-group/contrib")]
licenses=[" ".join(x.itertext()) for x in m.findall(".//license")]
texts=["".join(x.itertext()) for x in m.findall(".//p")]
selected=[t for t in texts if any(x in t for x in ("1%","10 μM","10 μ","seeding stage","seeds were","seed solution"))]
print(json.dumps({"original_preserved":True,"all_stage_hashes_match":True,"six_values_preserved":True,"transitions":transitions,"no_unobserved_recovery_or_closure":True,"idrees_receipts_match":True,"local_si_is_error_body":True,"main_authors":authors,"main_licenses":licenses,"source_preparation_passages":selected,"stage_result_sha256":hashlib.sha256((B/"results/hou-stage-mapping.json").read_bytes()).hexdigest()},indent=2))

```

Captured exit code: 0.

```json
{
  "original_preserved": true,
  "all_stage_hashes_match": true,
  "six_values_preserved": true,
  "transitions": [
    {
      "rows": [
        4,
        6
      ],
      "decimal_ratio": "1.158227848101265822784810127",
      "decimal_difference": "12.5",
      "pass": true
    },
    {
      "rows": [
        7,
        9
      ],
      "decimal_ratio": "1.161707632600258732212160414",
      "decimal_difference": "12.5",
      "pass": true
    }
  ],
  "no_unobserved_recovery_or_closure": true,
  "idrees_receipts_match": true,
  "local_si_is_error_body": true,
  "main_authors": [
    "Idrees Abdullah",
    "Reuven Bar",
    "Markovich Gil"
  ],
  "main_licenses": [
    "https://creativecommons.org/licenses/by/4.0/ Permits the broadest form of re-use including for commercial purposes, provided that author attribution and integrity are maintained ( https://creativecommons.org/licenses/by/4.0/ )."
  ],
  "source_preparation_passages": [
    "The NC seed particles were synthesized enantioselectively\nfollowing a procedure of Schwartz et al.24 To 10 mL of water, we added 285 \u03bcL of 100 mM Terbium chloride\nsolution at acidic pH (pH\u223c 2) heated to 50 \u00b0C, followed\nby the rapid addition of 600 \u03bcL of 100 mM Na2HPO4 solution, also heated to 50 \u00b0C, to the terbium chloride\nsolution under stirring. The solution was stirred for 1 h at 50 \u00b0C,\nattaining a milky appearance. The obtained enantio-pure NCs were labeled\n\u039b-NCs if prepared with l-Tartaric acid (l-TA),\nand \u0394-NCs if prepared with d-Tartaric acid (d-TA). For seeding experiments, 100 \u03bcL of the NC solution out\nof the total \u223c11 mL synthesized, which is \u223c1% of the\ntotal synthesis quantity was taken. Enantio-pure NCs without ligands\nwere prepared by repeating the same procedure as the above synthesis,\nonly without any TA, but with the addition of the enantiopure \u039b-NCs\nor \u0394-NCs. The NCs were purified by centrifugation. Considering\nthat the added seed particle solution contained \u223c1% of the\noriginal TA quantity, their concentration at the \u201cligand-less\u201d\nsynthesis was about 0.1 mM. After the final purification of the resulting\n\u201cligand-less\u201d NCs which removed practically all the\ndissolved residual TA, we estimate that <10% of the above concentration\nremains adsorbed to the NCs (see also Supporting Information, Table S6). Hence, a very small amount of TA,\nof equivalent concentration <10 \u03bcM, is left in the purified\nNC sample.",
    "The initial NC synthesis, performed at 50 \u00b0C, contained either l- or d-tartaric acid (TA), which has previously been\nshown to lead to the formation of enantiopure \u039b- or \u0394-NCs,\nrespectively.23 Then, 1% of the total prepared\nNCs were used as seed particles for a new NC synthesis, without added\nTA, at 50 \u00b0C, which was previously shown to yield enantiopure\nNC samples, following the handedness of the seed NCs.22,24 After purifying this secondary NC sample by centrifugation, only\ntraces of TA (<10 \u03bcM) were left at the NC sample. Figure 1a shows a TEM image\nof the final ligand-less NCs. Figure 1b presents a high-magnification TEM image revealing\ntwo single crystal nanorods. Fast Fourier transform (FFT) analysis\nof the HRTEM image shown in Figure 1b reveals the crystallographic planes present in the\nTbPO4\u00b7H2O NCs. Specifically, the FFT pattern\nindicates the presence of (100) type and (001) planes, consistent\nwith the hexagonal phase structure of TbPO4\u00b7H2O NCs. This observation agrees with the X-ray diffraction\nresults provided in Table S1 (Supporting\nInformation). Analysis of many similar HRTEM images implies that all\nlateral facets of the NCs seem to correspond to the (100) type.",
    "Figure 4 shows the\nresults for the ee of both TA and ASP racemate adsorption\nexperiments. For rac-ASP, the ee climbs to \u223c42%\nat an initial racemate concentration of 0.4 mM and sharply declines\nto about 8% at 3 mM. The ee of the ASP at an initial\nconcentration of 0.2 mM is higher than 50% but was difficult to properly\nquantify due to relatively noisy CD signal and low total adsorbed L + D, which was difficult to determine\naccurately using potentiometric titration. Racemic TA starts with\na lower ee of 13% at 0.4 mM which decreases to about\n1% at 3 mM, revealing a weaker but still noticeable enantioselective\ninteraction. This trend demonstrates that enantiomeric selection in\nadsorption is higher at lower concentrations for both compounds. A\npossible reason for this phenomenon would be a reduction in adsorption\nsites per molecule. While at low concentrations, each molecule would\nmaximize the interactions of its functional groups (carboxyl, hydroxyl,\nand ammine/ammonium) with surface sites (Tb3+, \u2212P\u2013O\u2013), at higher concentrations, neighboring sites may\nbe occupied by other molecules, reducing the possibility for enantioselective\nadsorption. Another plausible factor with increasing influence at\nhigh concentrations is the cooperative effects of interactions between\nthe adsorbed molecules at nearest-neighbor sites, of the same or opposite\nenantiomers. This effect might be somewhat different between TA and\nASP, as TA is known to prefer crystallization as a racemate,26 i.e l-TA - d-TA interactions\nare relatively strong, while ASP shows kinetic preference to crystallization\nas a conglomerate of single enantiomer crystals,27 perhaps indicating weaker interenantiomer interactions.\nThis is also implied by the stronger racemate adsorption of TA relative\nto ASP at the higher racemate concentrations (see initial concentrations\nof 2.0\u20133.0 mM, Table S5)."
  ],
  "stage_result_sha256": "fd48c49dd4a728d7032769e09c75b408b431290498a2cfc4c2f07fee957f23ea"
}
```


## Final artifact verdict: APPROVE bounded local step

Final artifact review completed after root signaled readiness. No remaining scientific, calculation, provenance, source-attribution, or presentation blocker was found for this bounded retrospective step. Approval applies to the current files/hashes captured below; it does not close any integrated requirement or certify external publication, physical repair causality, serial inheritance, prediction or replication.

The Idrees2025 attribution is corrected in REPORT.md and DATASET_REGISTRY.md and matches directly inspected main/deposit authors. Both documents retain exact DOI/download links and distinguish local bytes, advertised files, scout-only transient reads, restricted/on-request material and failed/error downloads. The REPORT clearly preserves the original FE-pairing failure, documents post hoc source-stage reconciliation, reports all six native values and exactly two displayed regeneration steps, and maintains current-only interpretation for the eleven retentions. Its table contains exactly I/E/T/B/R/H/V/S/M/A/J/C, each Unclosed. All local Markdown links in the final report/registry resolve, and the report embeds the final rather than preview PNG.

Direct visual inspection of results/hou-comparisons-final.png via view_image found six correctly labeled FE endpoints, three operation-decline segments, two combined-treatment recovery segments, and eleven separate current-retention bars. Both duration groups and the persistence=1 reference are explicit. Footer notes are legible and separated from tick labels; they disclose post-execution mapping, fixed windows, absent uncertainty/independent specimen identities and bundled treatment. No error bars, fit, fabricated third recovery or cross-current amplitude comparison appears. plot_hou.py reads the preserved JSON outputs and does not alter the scientific estimators. This is a static saved scientific artifact, not an independently observed laboratory result.

Read-only handoff consistency checks confirm the resumed attempt appears in NEXT_SESSION_PROMPT.md, parent progress.md, CONTINUATION_LEDGER.md and publication/origin-function-local-checkpoint.json. Current text/locator state is active_unachieved, local/uncommitted/unpublished, with no closed integrated requirements and historical blocked/checkpoint state preserved separately. This review did not independently revalidate live goal-service state or remote Git refs. The inspected checks/progress/checkpoint still contain pending final-review labels; root may replace those administrative labels with this completed approval. That update must not change scientific values, provenance or claims.

### Final scenarios, invocation and captured artifact

| Scenario | Exact invocation | Binary observable | Artifact |
|---|---|---|---|
| Final report/source attribution and links | python3 -B - with script below; read REPORT.md and DATASET_REGISTRY.md | Exit0; correct Idrees attribution; four local Markdown links exist; final PNG embedded | This section/script/output; hashed report/registry |
| Twelve unchanged integrated verdicts | Same script, regex extraction and exact ordered list assertion | Exit0; exactly twelve Unclosed rows | This section raw output; REPORT.md |
| Original data and stage outputs preserved | Same script SHA256; prior Decimal script and stage provenance assertions | Exit0; original result SHA unchanged; six native values and two transitions verified | This section and stage-audit section; both result JSONs |
| Final plot visual QA | tools.view_image of absolute B/results/hou-comparisons-final.png; inspect both panels and footer | PASS: legible 2025x825 PNG; six FE values and eleven bars; scientific bounds visible | Final PNG with hash below; this visual observation |
| Handoff consistency | Same script; read named parent handoffs and checkpoint JSON | Exit0; resumed attempt referenced; active/local/unpublished flags consistent | This section raw output and hashed handoffs |

### Final validation script

```python
from pathlib import Path
import hashlib,json,re
from PIL import Image
B=Path("documented-scaffold-2026-10-18/public-primary-datasets-resumed")
files=["STAGE_MAPPING_AMENDMENT.md","reconcile_hou_stages.py","results/hou-stage-mapping.json","REPORT.md","DATASET_REGISTRY.md","checks.md","progress.md","plot_hou.py","results/hou-comparisons-final.png","results/hou-test.json"]
out={"files":[],"local_markdown_links":[]}
for name in files:
 p=B/name;data=p.read_bytes();assert data
 out["files"].append({"path":str(p),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
for name in ("REPORT.md","DATASET_REGISTRY.md"):
 text=(B/name).read_text()
 assert "Idrees" in text and not re.search(r"Hananel(?: et al\.)?\s*2025",text)
 for link in re.findall(r"\]\(([^)]+)\)",text):
  if not link.startswith(("http:","https:","#")):
   p=B/link;assert p.exists(),str(p)
   out["local_markdown_links"].append({"document":name,"target":link,"exists":True})
report=(B/"REPORT.md").read_text()
expected=list("IETBRHVSMAJC")
rows=re.findall(r"^\| ([IETBRHVSMAJC]) \|.*\| Unclosed \|$",report,re.M)
assert rows==expected,(rows,expected)
assert "results/hou-comparisons-final.png" in report
assert "results/hou-comparisons.png)" not in report
p=B/"results/hou-comparisons-final.png"
with Image.open(p) as im: out["final_png"]={"format":im.format,"size":list(im.size)}; assert im.format=="PNG";im.verify()
assert hashlib.sha256((B/"results/hou-test.json").read_bytes()).hexdigest()=="52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36"
checkpoint=json.loads(Path("publication/origin-function-local-checkpoint.json").read_text())
assert checkpoint["full_goal_status"]=="active_unachieved"
assert checkpoint["resumed_dataset_attempt"]["full_integrated_requirements_closed"]==[]
assert not checkpoint["resumed_dataset_attempt"]["published"] and not checkpoint["resumed_dataset_attempt"]["committed"]
for path in ["documented-scaffold-2026-10-18/NEXT_SESSION_PROMPT.md","documented-scaffold-2026-10-18/progress.md","documented-scaffold-2026-10-18/CONTINUATION_LEDGER.md","publication/origin-function-local-checkpoint.json"]:
 p=Path(path);text=p.read_text();assert "public-primary-datasets-resumed" in text
 out["files"].append({"path":str(p),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
out.update({"twelve_unclosed_rows":rows,"author_attribution_corrected":True,"original_result_still_unchanged":True,"handoff_active_local_unpublished_consistent":True})
print(json.dumps(out,indent=2))

```

Captured process exit code: 0.

```json
{
  "files": [
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/STAGE_MAPPING_AMENDMENT.md",
      "bytes": 3634,
      "sha256": "370ea0d5dba473e342dd8d4f21164b325ed8e5cc22f8b78a7b3336c663029166"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/reconcile_hou_stages.py",
      "bytes": 2299,
      "sha256": "7ac32156e5e8ed07b8136c0adfead10cefa70f898e3c8e2dca84b197acdd24a7"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/results/hou-stage-mapping.json",
      "bytes": 2048,
      "sha256": "fd48c49dd4a728d7032769e09c75b408b431290498a2cfc4c2f07fee957f23ea"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/REPORT.md",
      "bytes": 10743,
      "sha256": "5a1d4c495de5ccd37218ef160b8c58958f3c7f69a4768204106fbfcefac7cf4a"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/DATASET_REGISTRY.md",
      "bytes": 5547,
      "sha256": "1ad81d3a8828ca0182354f1c7d55adee11d3d21af19762ceaea8379bc511b41f"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/checks.md",
      "bytes": 5083,
      "sha256": "9e334f3896ec8c917729e67f2f0a5c49cfd65c35225a37cbc42263bfcf707932"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/progress.md",
      "bytes": 3584,
      "sha256": "aa7538269753ba8f4a92cdab2e5de3147636c1859e61112c1d6af7d076b1b9e5"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/plot_hou.py",
      "bytes": 2915,
      "sha256": "51e6bf580bab9e819dea330678d6ae34cdfedcc123ea2fa9a31369b2dbfc5a86"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/results/hou-comparisons-final.png",
      "bytes": 156577,
      "sha256": "fadd5e8fd94f6a07599d72361d992eaa9ab1730b679dab3aedd2490f501fc198"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/results/hou-test.json",
      "bytes": 16653,
      "sha256": "52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36"
    },
    {
      "path": "documented-scaffold-2026-10-18/NEXT_SESSION_PROMPT.md",
      "bytes": 20641,
      "sha256": "814b0f91fb1e4ebc85b88ea05d9fcb870d2f58d26cc81a27de888ea249f5764d"
    },
    {
      "path": "documented-scaffold-2026-10-18/progress.md",
      "bytes": 22750,
      "sha256": "f10a1f0266bff3af983b015df44bafb5922dc19c5f0502c63109037ddc0325a0"
    },
    {
      "path": "documented-scaffold-2026-10-18/CONTINUATION_LEDGER.md",
      "bytes": 28043,
      "sha256": "8958a8aa47c7ce50efcd1401f6de17ed02b71354c71412a69460328af182a6ab"
    },
    {
      "path": "publication/origin-function-local-checkpoint.json",
      "bytes": 7207,
      "sha256": "01efaf3e3b64f44018d7c9b409adb0caaaa522abf8aedb43a404e79cb5fe4418"
    }
  ],
  "local_markdown_links": [
    {
      "document": "REPORT.md",
      "target": "DATASET_REGISTRY.md",
      "exists": true
    },
    {
      "document": "REPORT.md",
      "target": "TEST_PROTOCOL.md",
      "exists": true
    },
    {
      "document": "REPORT.md",
      "target": "STAGE_MAPPING_AMENDMENT.md",
      "exists": true
    },
    {
      "document": "REPORT.md",
      "target": "results/hou-comparisons-final.png",
      "exists": true
    }
  ],
  "final_png": {
    "format": "PNG",
    "size": [
      2025,
      825
    ]
  },
  "twelve_unclosed_rows": [
    "I",
    "E",
    "T",
    "B",
    "R",
    "H",
    "V",
    "S",
    "M",
    "A",
    "J",
    "C"
  ],
  "author_attribution_corrected": true,
  "original_result_still_unchanged": true,
  "handoff_active_local_unpublished_consistent": true
}
```

Skipped: fresh retrieval of scout-only sources, remote publication/goal-state revalidation and physical experimentation. Remaining risk: combined intervention and missing material/lineage controls prevent full R/H/J or integrated-system inference; the report makes these limits explicit.


Final administrative delta checked after readiness: checks.md adds the root cross-artifact consistency row; execution_failures.md records routine patch-context/LSP invocation failures. Directly read both additions; no scientific result, stage mapping or interpretation changed. Final-review pending labels may still be updated by root to this completed approval. Current artifacts:
- documented-scaffold-2026-10-18/public-primary-datasets-resumed/checks.md: 5481 bytes; SHA256 8fc2a3f6270743ff1413794967e34bffbd54fc88c558cf7522e39213bdfe7ef1
- documented-scaffold-2026-10-18/public-primary-datasets-resumed/execution_failures.md: 3244 bytes; SHA256 fe1b430d6615ce0a74fe34da9b8002d249d25b68dbba5a9a2caa3361fc087710
