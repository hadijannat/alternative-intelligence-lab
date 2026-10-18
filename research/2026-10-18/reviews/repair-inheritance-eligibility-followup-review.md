# Independent repair/inheritance eligibility follow-up review

Date: 18 October 2026. Read-only audit of the bounded follow-up; this reviewer owns only this evidence file. The active-attempt lookup returned ULW_LOOP_PLAN_MISSING, so evidence is recorded under .omo/evidence. No generic research, third-party code execution, scientific fit, response-array rerun or physical experiment was performed.

## Eligibility decision

No newly identifying R/H numerical test is justified by the inspected native Hou and Idrees records. This is an observation-identifiability conclusion about these source packages, not a universal impossibility claim. The new native Idrees SI acquisition is genuine source-access/evidence progress and enables direct audit of the adsorption methods. It does not provide the missing founder functional ceiling or controlled serial recipient function. The earlier resumed turn was genuine progress; historical blocked counts must not be reused.

The new SI changes the immediate access action: there is no longer a need to pursue the previously failing Figshare route merely to obtain these exact bytes. It sharpens the reason a simple seed-volume/site-count adsorption test is not admitted. The physical next discriminator remains independently justified founder capacity and serial recipient-as-parent function, or matched repair reconstruction/function/material accounting. Additional fitting of these consumed responses cannot supply either missing discriminator.

## Atom or seed-volume adsorption ceiling

The proposed shortcut is not supported by this package. A one-percent synthesis-volume transfer bounds an aliquot under preparation assumptions, not measured founder mass, exposed surface, accessible-site count or maximum functional response in the later assay. Converting even a reliable atom count into an adsorbed-molecule ceiling requires an independently justified adsorption stoichiometry or other conservative physical bound applicable to this material, medium and observable. Crystal atom count alone does not establish one molecule per site, monolayer coverage, absence of cooperative uptake or the relation between apparent solution depletion and surface-bound molecules.

This is not a rule that every bound must be empirically fitted. A rigorous conservative physical upper bound could suffice if its assumptions and inventory are independently supported. Here those assumptions are not established, and the source expressly documents limitations of the simple adsorption model:

- Idrees SI p9/FigS5 uses acid solution without the nanocrystal adsorption step as the titration reference. It is not a seed-only sample under descendant-assay conditions.
- SI p10/TableS6 discussion says adsorption is not saturated over the stated range and suggests stabilizing intermolecular interactions. A maximum measured response is therefore not a demonstrated capacity ceiling.
- SI p13 defines ideal Langmuir assumptions: finite identical sites, monolayer coverage and no lateral interactions.
- The native main text says single-enantiomer curves can be fitted but are far from saturation, while the two-adsorbate/racemate model does not fit, likely because of intermolecular interactions. A fitted single-enantiomer constant is not a validated founder-only capacity or a justified racemate occupancy limit.
- The new SI inventory contains CD calibration/spectra, adsorption/titration tables, molecule comparators and Langmuir explanation. It does not expose a seed-only capacity calibration or a recipient-as-parent functional lineage.

The review directly read TableS6 values while inspecting p10, as root also disclosed. These outcomes are consumed; no new blind test can be claimed from them. No new capacity, ratio, fit or adsorption prediction was calculated.

## Repair interpretation

Direct native Hou main/SI inspection confirms meaningful reconstruction evidence: Fig5c follows phase transformation during the treatment; Fig5b and S15 provide a separate carbonate-phase comparison. These are real component observations, not mere electrical recovery labels. The previous original FE result and post hoc mapping remain valid within their disclosed scope.

S9/S10 and the associated main methods concern initial formation, electrolyte exposure and drive removal/continuation. They are not matched damaged-electrode refresh-only, stirring-only or redox/sham intervention arms. The self-healing method bundles electrode removal, stirring, rest, reducing TPS and electrolyte renewal. No new linked material-loss/reconstitution and common-medium function discriminator was identified. Refitting phase or impedance records cannot manufacture missing interventions or specimen linkage.

R does not require assigning each catalytic event to incoming atoms; retained atoms may participate in rebuilt competent organization. This review neither credits full R/J nor concludes that repair is absent. It agrees that the current native package supports the previously reported combined-treatment phase/function evidence while leaving the full causal/accounting discriminator unresolved.

## Independent native checks and evidence scenarios

The new 760874-byte, 13-page SI has SHA256 3bab9ca7cc2c69a11484b795b383ce82598dbb60824340aa62f626b262359602. Its bytes match the exact EuropePMC ZIP member and the Figshare-declared MD5. The earlier 71-byte HTTP500 and zero-byte HTTP202 local bodies remain unchanged as non-PDF failure artifacts. Hou has 24 visible workbook sheets; the original numerical result hash remains unchanged.

| Scenario | Exact invocation | Binary observable | Captured artifact |
|---|---|---|---|
| New native SI identity | python3 -B - with complete script below; hashlib, zipfile and PyMuPDF | Exit0; SI matches ZIP member, deposited MD5 and expected size; 13 pages | This report script/output; serial-sources ZIP/PDF/registry |
| Proposed ceiling assumptions | PyMuPDF get_text for native SI pp9/10/13; ElementTree text of native main Langmuir/preparation paragraphs | Acid-only control, unsaturation, interaction caveat and racemate-model failure observed; independent founder ceiling not established | Exact cited native pages/paragraphs; this review and script output |
| Remaining repair controls | BeautifulSoup native Hou paragraphs mentioning carbonate/regeneration; PyMuPDF SI pp10–13,17,18,20; workbook metadata | Initial formation controls distinguished from absent post-damage factorial/linked material control; 24 visible sheets | Native main/SI/workbook; repair reasoning above and script output |
| Preserve prior outcomes/failures | Same script SHA256 and PDF signature checks | Exit0; original Hou result hash unchanged; both previous Idrees SI failures preserved | Script/output; original result and failed bodies |
| Full-goal boundary | Read follow-up PROTOCOL.md and preceding frozen scope/results | Twelve integrated requirements remain unclosed; no scientific fit/test performed in this review | Named protocols/results and this review |

Final serial-audit and report/checks/progress review is pending their readiness. Current scientific eligibility conclusion is clear; this is not yet final artifact approval.

## Reproducible independent checks

Invocation: python3 -B - with this script from the workspace cwd.

```python
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as E
import fitz
from bs4 import BeautifulSoup
B=Path("documented-scaffold-2026-10-18/public-primary-datasets-resumed")
F=B/"eligibility-followup"
S=F/"serial-sources"
report={"artifacts":[]}
for p in [F/"PROTOCOL.md",F/"repair-audit.md",B/"sources/hou-main.html",B/"sources/hou-si.pdf",B/"sources/hou-source.xlsx",S/"europepmc-supplementary.zip",S/"ja4c16883_si_001.pdf",S/"idrees2025-main.xml",S/"figshare-28823413.json"]:
 data=p.read_bytes();assert data
 report["artifacts"].append({"path":str(p),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
native=(S/"ja4c16883_si_001.pdf").read_bytes()
deposit=json.loads((S/"figshare-28823413.json").read_text())
entry=next(x for x in deposit["files"] if x["name"]=="ja4c16883_si_001.pdf")
assert len(native)==entry["size"] and hashlib.md5(native).hexdigest()==entry["computed_md5"]
with zipfile.ZipFile(S/"europepmc-supplementary.zip") as z:
 names=[n for n in z.namelist() if n.endswith("ja4c16883_si_001.pdf")]
 assert len(names)==1 and z.read(names[0])==native
report["new_si_matches_zip_and_deposit"]=True
d=fitz.open(stream=native,filetype="pdf");assert len(d)==13
texts=[p.get_text() for p in d]
report["si_page_inventory"]=[{"page":i+1,"heading":t.splitlines()[0]} for i,t in enumerate(texts)]
assert "control sample" in texts[8] and "rac-TA" in texts[8]
assert "saturation is not yet achieved" in texts[9]
assert "inter-molecular" in texts[9]
assert "without any lateral interactions" in texts[12]
main=E.fromstring((S/"idrees2025-main.xml").read_bytes())
paras=["".join(x.itertext()) for x in main.findall(".//p")]
assert any("Racemate adsorption" in p and "could not be modeled" in p for p in paras)
assert any("100" in p and "11 mL" in p and "For seeding" in p for p in paras)
report["source_checks"]={"acid_only_titration_reference_present":True,"unsaturated_adsorption_text_present":True,"interaction_caveat_present":True,"ideal_langmuir_assumptions_present":True,"racemate_model_failure_present":True,"seed_aliquot_not_capacity_measurement":True}
with zipfile.ZipFile(B/"sources/hou-source.xlsx") as z:
 wb=E.fromstring(z.read("xl/workbook.xml"))
 sheets=wb.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets")
 assert len(sheets)==24 and all(s.attrib.get("state","visible")=="visible" for s in sheets)
 report["hou_sheet_names"]=[s.attrib["name"] for s in sheets]
report["original_hou_result_preserved"]=hashlib.sha256((B/"results/hou-test.json").read_bytes()).hexdigest()=="52c8a954e1b33c40643930d20c859202966e483ca7b370b3a7648838e60bcd36"
assert report["original_hou_result_preserved"]
failed=B/"sources/hananel2025"
report["preserved_previous_failed_si_bodies"]=[{"path":str(p),"bytes":p.stat().st_size,"is_pdf":p.read_bytes().startswith(b"%PDF")} for p in failed.rglob("si.pdf")]
assert len(report["preserved_previous_failed_si_bodies"])==2 and all(not x["is_pdf"] for x in report["preserved_previous_failed_si_bodies"])
report["numerical_fit_or_new_scientific_test_executed"]=False
print(json.dumps(report,indent=2))

```

Captured exit code: 0.

```json
{
  "artifacts": [
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/PROTOCOL.md",
      "bytes": 3056,
      "sha256": "5d749082e186f1000bc88780bf5bd53c0f2d2b6654f5b188dc83d0c8c8b10596"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/repair-audit.md",
      "bytes": 15516,
      "sha256": "a05a6ebe22f331334c09f56fb15b26facb719627782caf0251559066bfbed6da"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/hou-main.html",
      "bytes": 423265,
      "sha256": "e7fd5c1f4ddd5557c51fe53a81fa4f5e7fd9d387b81ec9f8e76128d6edbdf8f3"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/hou-si.pdf",
      "bytes": 3811836,
      "sha256": "adf9763a2b1f2f6d31695fb78b05ef342e07b1186aa5df9f60418a368826c246"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/hou-source.xlsx",
      "bytes": 29687651,
      "sha256": "3319d65a2cfc4fa43f1ea78b906b5be2a5987d5efa928f1312beaeb38f843315"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/europepmc-supplementary.zip",
      "bytes": 1202571,
      "sha256": "ccc97cff0220fca801293a474a196f2e18c51a81d48e1e93b94535f83beb689a"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/ja4c16883_si_001.pdf",
      "bytes": 760874,
      "sha256": "3bab9ca7cc2c69a11484b795b383ce82598dbb60824340aa62f626b262359602"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/idrees2025-main.xml",
      "bytes": 80907,
      "sha256": "f132e272fa0e34b76600454fc94fc5c716064d47506d01224eca15a12f6e6ac7"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/figshare-28823413.json",
      "bytes": 6764,
      "sha256": "2a99c1dc9f882160508bfa6baee7410db0e2d6299c409321256afac8bf94f8fd"
    }
  ],
  "new_si_matches_zip_and_deposit": true,
  "si_page_inventory": [
    {
      "page": 1,
      "heading": "Supporting Information for:"
    },
    {
      "page": 2,
      "heading": "TEM Analysis of TbPO4\u22c5H2O NCs"
    },
    {
      "page": 3,
      "heading": "Use of CD for analysis of enantioselective adsorption of TA and ASP onto the chiral "
    },
    {
      "page": 4,
      "heading": "Raw CD data after adsorption of single enantiomers of ASP to the NCs"
    },
    {
      "page": 5,
      "heading": "CD data on free ASP single enantiomer concentrations after adsorption to NCs "
    },
    {
      "page": 6,
      "heading": "CD data on free TA single enantiomer concentrations after adsorption to NCs extracted "
    },
    {
      "page": 7,
      "heading": "Raw CD data after adsorption experiments of racemic mixtures of ASP "
    },
    {
      "page": 8,
      "heading": "Raw CD data after adsorption experiments of racemic mixtures of TA"
    },
    {
      "page": 9,
      "heading": "Potentiometric titration curves to determine the equivalent adsorbed concentration of "
    },
    {
      "page": 10,
      "heading": "Summary of potentiometric titration results"
    },
    {
      "page": 11,
      "heading": "Glutamic acid adsorption on the TbPO4\u22c5H2O NCs "
    },
    {
      "page": 12,
      "heading": "Methyl succinic acid adsorption on the NCs"
    },
    {
      "page": 13,
      "heading": "Langmuir model fits"
    }
  ],
  "source_checks": {
    "acid_only_titration_reference_present": true,
    "unsaturated_adsorption_text_present": true,
    "interaction_caveat_present": true,
    "ideal_langmuir_assumptions_present": true,
    "racemate_model_failure_present": true,
    "seed_aliquot_not_capacity_measurement": true
  },
  "hou_sheet_names": [
    "Fig. 2a",
    "Fig. 2b",
    "Fig. 2c",
    "Fig. 4a",
    "Fig. 4b",
    "Fig. 4c",
    "Fig. 4d",
    "Fig. 5a",
    "Fig. 5b",
    "Fig. 5c",
    "Fig. 5e",
    "Fig. 5f",
    "Supplementary Fig. 3a",
    "Supplementary Fig. 3b",
    "Supplementary Fig. 4",
    "Supplementary Fig. 8",
    "Supplementary Fig. 9a",
    "Supplementary Fig. 9b",
    "Supplementary Fig. 11",
    "Supplementary Fig. 13",
    "Supplementary Fig. 14",
    "Supplementary Fig. 15",
    "Supplementary Fig. 16",
    "Supplementary Fig. 18"
  ],
  "original_hou_result_preserved": true,
  "preserved_previous_failed_si_bodies": [
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/hananel2025/si.pdf",
      "bytes": 71,
      "is_pdf": false
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/sources/hananel2025/alternate/si.pdf",
      "bytes": 0,
      "is_pdf": false
    }
  ],
  "numerical_fit_or_new_scientific_test_executed": false
}
```

Skipped: new adsorption/phase fitting, movie playback, generic source searching and physical assays. Risk: the source evidence remains insufficient for founder-bounded serial inheritance or uniquely identified repair contribution; all integrated requirements remain open.


## Final verdict: APPROVE bounded eligibility audit

Final serial-audit.md, REPORT.md, checks.md and progress.md were read after root readiness. No actionable blocker remains. The saved decision correctly distinguishes access/source-model progress from a new empirical repair/inheritance result and admits no new identifying numerical R/H test. All twelve integrated requirements remain unclosed; the full goal remains active/unachieved. No historical blocked count is reused.

Final source-chain checks also directly inspected the Idrees adsorption/ICP-MS paragraphs, Schwartz2023 seed-method paragraphs and Hananel preprint SI pp17–19. These support the serial audit's distinctions: the adsorption assay uses a purified secondary batch; water/ASP ICP-MS is a solution/material-response measurement rather than founder-specific functional allocation; the older optical seed experiment and its assumption-based TA estimate are not an independent adsorption-capacity calibration or serial recipient-functional lineage. The native Idrees main explicitly reports phosphate release under ASP exposure; this supports the final report's surface-change caveat without supplying a missing founder bound. Published quantitative prose and the preprint bound expressions seen during these readings are consumed; no new calculation was executed from them.

The six native source artifacts match every saved SHA256 receipt. The new SI matches both the ZIP member and deposit MD5; the archive-container difference noted in serial-audit is not incorrectly promoted to identical ZIP bytes. Five local report links resolve. The final serial audit now explicitly discloses root/reviewer TableS6 exposure while correctly stating that no new response dataset was assembled or fitted. The report permits a rigorous conservative physical bound in principle and rejects only the unsupported inventory-to-capacity conversion for this package.

The current checks/progress files still mark final review pending. Root may replace those administrative statuses with this approval; no scientific conclusions, values, provenance or source-access distinctions should change. Live remote/publication and goal-service state were outside this independent review; its scope is the native source packages, saved eligibility decision and local artifact consistency. Root's separate reported live checks are not recertified here.

| Final scenario | Invocation | Binary observable | Captured artifact |
|---|---|---|---|
| Final source/report consistency | Read final four documents and native main/preprint paragraphs; python3 -B - script below | APPROVE: no unsupported founder ceiling or new identifying test; consumed outcomes explicit; all twelve preserved | This verdict, final documents and source artifacts |
| All six saved source receipts | Same script: SHA256 each serial-sources file, assert hash occurs in serial-audit | Exit0; six matching native artifacts | Script/output below; six source files |
| Final report links and handoff | Same script: resolve relative Markdown links and assert report/serial scope text | Exit0; five links exist; active/no-test scope and consumed outcomes present | Script/output below; REPORT/checks/progress |
| New source content | ElementTree paragraphs of idrees2025-main.xml and schwartz2023-main.xml; PyMuPDF hananel-preprint.pdf pp17–19 | Seed-produced adsorption link and independent founder/serial gaps confirmed within inspected scope | Native artifacts; reasoning above |

### Final validation invocation and captured output

Invocation: python3 -B - with this script from workspace cwd.

```python
from pathlib import Path
import hashlib,json,re
B=Path("documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup")
out={"artifacts":[],"local_links":[]}
for name in ("PROTOCOL.md","repair-audit.md","serial-audit.md","REPORT.md","checks.md","progress.md"):
 p=B/name;data=p.read_bytes();assert data
 out["artifacts"].append({"path":str(p),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
 for link in re.findall(r"\]\(([^)]+)\)",data.decode()):
  if not link.startswith(("http:","https:","#")):
   assert (p.parent/link).exists(),link
   out["local_links"].append({"source":name,"target":link,"exists":True})
serial=(B/"serial-audit.md").read_text()
for p in sorted((B/"serial-sources").iterdir()):
 assert p.is_file()
 data=p.read_bytes();h=hashlib.sha256(data).hexdigest()
 assert h in serial,p.name
 out["artifacts"].append({"path":str(p),"bytes":len(data),"sha256":h,"matches_audit_receipt":True})
assert len(list((B/"serial-sources").iterdir()))==6
report=(B/"REPORT.md").read_text()
for token in ("I, E, T, B, R, H, V, S, M, A, J and C","conservative physical bound could suffice","All Table S6"):
 if token=="All Table S6": assert "all Table S6" in report
 else: assert token in report,token
assert "Root and reviewer consumed Table S6" in serial
assert "No newly identifying numerical R/H test" in report
assert "active/unachieved" in report
out.update({"six_native_receipts_match":True,"all_twelve_preserved":True,"consumed_outcomes_disclosed":True,"no_new_identifying_test_and_active_goal":True})
print(json.dumps(out,indent=2))

```

Exit code: 0.

```json
{
  "artifacts": [
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/PROTOCOL.md",
      "bytes": 3056,
      "sha256": "5d749082e186f1000bc88780bf5bd53c0f2d2b6654f5b188dc83d0c8c8b10596"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/repair-audit.md",
      "bytes": 15516,
      "sha256": "a05a6ebe22f331334c09f56fb15b26facb719627782caf0251559066bfbed6da"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-audit.md",
      "bytes": 12041,
      "sha256": "ad408ee0df63ea7f505ff4a2ef711b20df3d184d73feeaa57dc43cb634eed387"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/REPORT.md",
      "bytes": 6011,
      "sha256": "189d4bdd3d3ef1f9051a338c417a49a4a8dfb860582ed9717b3eaf9fcde9656c"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/checks.md",
      "bytes": 2647,
      "sha256": "e8aa0e003e3170b66759e53bfd103d40ae2293c82428f84b5b50739557acbeeb"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/progress.md",
      "bytes": 2378,
      "sha256": "7043d5421e7be9afb190838197e6c9b8ae4a45fa92841ca5f1750a96f29e980a"
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/europepmc-supplementary.zip",
      "bytes": 1202571,
      "sha256": "ccc97cff0220fca801293a474a196f2e18c51a81d48e1e93b94535f83beb689a",
      "matches_audit_receipt": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/figshare-28823413.json",
      "bytes": 6764,
      "sha256": "2a99c1dc9f882160508bfa6baee7410db0e2d6299c409321256afac8bf94f8fd",
      "matches_audit_receipt": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/hananel-preprint.pdf",
      "bytes": 1978587,
      "sha256": "6ce5b54efff8dfb6cdf81481da039855082955399a280653f561f2b56d6e44f2",
      "matches_audit_receipt": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/idrees2025-main.xml",
      "bytes": 80907,
      "sha256": "f132e272fa0e34b76600454fc94fc5c716064d47506d01224eca15a12f6e6ac7",
      "matches_audit_receipt": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/ja4c16883_si_001.pdf",
      "bytes": 760874,
      "sha256": "3bab9ca7cc2c69a11484b795b383ce82598dbb60824340aa62f626b262359602",
      "matches_audit_receipt": true
    },
    {
      "path": "documented-scaffold-2026-10-18/public-primary-datasets-resumed/eligibility-followup/serial-sources/schwartz2023-main.xml",
      "bytes": 57460,
      "sha256": "bc69defd71703e0ae08800020b80c3e5aea35724b793ab5c6b99178e22bf558f",
      "matches_audit_receipt": true
    }
  ],
  "local_links": [
    {
      "source": "REPORT.md",
      "target": "serial-sources/ja4c16883_si_001.pdf",
      "exists": true
    },
    {
      "source": "REPORT.md",
      "target": "serial-audit.md",
      "exists": true
    },
    {
      "source": "REPORT.md",
      "target": "repair-audit.md",
      "exists": true
    },
    {
      "source": "REPORT.md",
      "target": "checks.md",
      "exists": true
    },
    {
      "source": "REPORT.md",
      "target": "progress.md",
      "exists": true
    }
  ],
  "six_native_receipts_match": true,
  "all_twelve_preserved": true,
  "consumed_outcomes_disclosed": true,
  "no_new_identifying_test_and_active_goal": true
}
```

Skipped: live external state refresh, movie playback, new fitting and physical testing. Remaining risk: scientifically discriminating founder-capacity/serial-function and matched reconstruction/control/accounting observations remain unavailable in the inspected packages.

Final administrative delta: root added only the saved-source/artifact-consistency row to checks.md. Direct read confirms its scope; current checks.md is 2940 bytes, SHA256 c3906c1f71eae3dc9b6dd52597d721864932466d3956314996dd8222b5ce1d47. The corrected serial-audit.md remains SHA256 ad408ee0df63ea7f505ff4a2ef711b20df3d184d73feeaa57dc43cb634eed387. Final APPROVE remains valid. Administrative pending-status replacements and parent handoff references may follow this verdict without altering scientific claims.
