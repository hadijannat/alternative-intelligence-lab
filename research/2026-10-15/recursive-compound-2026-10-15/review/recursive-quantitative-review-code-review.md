# Independent quantitative review

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []

Scope: current untracked `recursive-compound-2026-10-15/{identity,energy,heredity,adaptation,boundary}` deliverables, specifically the six requested scientific/arithmetic claims. No supplied baseline diff or notepad; `git status` reports the whole directory untracked. No ulw-loop plan exists (`ULW_LOOP_PLAN_MISSING`), so this uses the prescribed fallback report location. This is approval of the bounded accounting dossier, not approval of target identity, joint function, physics, or life/intelligence claims.

## Findings by severity

CRITICAL: none found in scope.

HIGH: none found in scope.

MEDIUM — `heredity/check.py:28–29`: the two purported synthetic controls evaluate literal Fraction identities and never invoke the actual bound calculation. Changing the bound logic would leave these controls green. They provide no behavioral coverage. Remove those two assertions or test the bound calculation with changed seed/end-point inputs if a reusable calculation is introduced for a real need. Do not introduce an abstraction solely to justify these tests. The numerical result remains independently correct, and the report explicitly limits it to accounting; this is not a scientific blocker.

LOW — `energy/REPORT.md` PMo12 quantitative paragraph omits a useful separate measured comparator. Retained primary `energy/raw/symes2013.txt:378–387` reports 79% relative efficiency for the two-step, two-electrode configuration and distinguishes it from the approximately 87% three-electrode benchmark. The current wording correctly scopes its 86.73% calculation. Adding the separate 79% result would improve selection of an engineering benchmark and prevent later reuse of 86.73% as full-cell performance. It supplies no shared-medium target coupling.

LOW — several reviewed functions are unannotated and the identity extractor loads a namespace via AST/exec. This falls short of the programming skill's strict typing perspective. Its documented purpose is to reuse pure legacy parsing without executing output writes; for this frozen, bounded extraction there is no demonstrated result error. Do not generalize it into a reusable CIF parser without a proper parser boundary and typed interfaces.

## Independent checks and evidence

A fresh `python3 -B` standard-library calculation read the CIF, site mapping, CSV and primary XML; it did not import or execute agent output-generating scripts. All values below were independently recomputed, not accepted from PASS fields.

| Claim | Source inspected and independent result | Scientific boundary |
|---|---|---|
| Parent heavy atoms | Original `noncarbon-discovery-2026-10-15/research/structure/raw/cod2107026.cif` cell and four symmetry operations; reconstructed all 164 mapped Cartesian positions from source fractional coordinates and mapping shifts. Maximum difference 7.1607e-15 Å; 36 Mo, 128 O; minimum pair 1.664453262 Å; Mo coordination 32 six-neighbor and 4 seven-neighbor sites at 2.6 Å. | Hydrogen coordinates absent; sixteen long-contact O sites are an inferred water assignment. Complete hydrated input, solution identity and substituted target remain unverified. |
| Ceria | Retained primary text Table 3 lines 492–525 matches nine CSV rows. Independent power/time sums: 535005, 419715, 645435 J; H2 HHV sums: 53.03, 48.17, 60.36 J; ratios: 0.0099120568967%, 0.0114768354717%, 0.0093518324851%. | Source test percentages equal sums of rounded cycle percentages; they are not aggregate energy ratios. No propagated uncertainty or kinetic fit. |
| PMo12 | Symes primary Fig. 3 text and potential accounting; 2.17−0.46=1.71 V, 0.85−(−0.38)=1.23 V, total 2.94 equivalent V; 2.55/2.94=0.86734694 and 2.94/2.55−1=0.15294118. | Benchmark is 100 mA/cm², three-electrode, source NHE scale. Separate two-electrode 79% result exists. Neither predicts target coupling. |
| CHA | Primary XML Table 1 endpoint 24 h / 530 / 434 / 0.24, seed paragraph approximately 0.001 cm³/g. Ratio 0.001/0.24=1/240. | F≤M, unchanged seed capacity and additive accessibility are explicit assumptions. 239/240 is altered-or-new accessible capacity, not a new-atom or inherited-function fraction. Source explicitly discusses both crystallization and ion exchange. Samples were vacuum-treated at 300°C for 6 h and measured with N2 at 77 K. |
| Ag2S | Viewed retained Eq. 1 image directly; primary text supplies a=3.40e12 s/S^b, b=4. Independent evaluations: 3.40 s at .001 S, 510.2125 s at .0035 S; ratio 150.0625. | Fit evaluations only. The 1–3.5 mS range also appears in paired-pulse data; model V1 limitations prevent treating these as validated paired-pulse retention predictions. Existing report discloses this limitation. |
| Zirconia | Primary HTML methods specify 0.05 g, 10 mL and 100 mg/L, with separate 50–700 mg/L isotherm feed series and capacities 7–51 mg/g. Independent ceiling 20 mg/g; removal fractions 0.70 and 0.364285714. | The 66.70 mg/g fitted maximum belongs to an isotherm, not the 100 mg/L kinetic run. Total-Mo uptake does not establish intact-Mo36 retention. |

Also inspected the main/SI PMo12 preparation passages: main 1.4 M molybdate with phosphate and 4 M HClO4 versus SI 0.7 M molybdate and 0.06 M HCl. The report's equal-volume nominal 2 M versus 0.03 M comparison is correctly conditional and not a proton-activity claim.

Inspected recorded evidence: `identity/.omo/evidence/{checks.json,runtime.json}`, `energy/.omo/evidence/checks.json`, and `identity/next-step/feasibility.json`. Existing build-only PySCF records explicitly report `scf_run=false`; no runtime or electronic-structure result was newly claimed by this review. Files were present at inspection, not inferred from summaries.

## Skill-perspective check

Ran the read-only remove-ai-slops and programming perspectives after loading both SKILL.md files and the Python reference. Checked for deletion-only tests, requested-removal assertions, tautological checks, implementation-constant mirroring, unnecessary extraction/normalization and untyped escape hatches. The two literal heredity synthetic controls violate test-relevance criteria. Source transcription assertions are useful source-data checks, although they are not independent physical validation. Extraction of the parent graph and source tables serves the actual scientific task. No prompt-prose tests or removal-only tests were found in inspected code. The AST namespace and unannotated interfaces are limited programming-perspective deviations, without a demonstrated numerical failure here.

## Next action and limits

The next meaningful action remains identified-parent shared-medium measurement, including molecular speciation and active function, before joint-target modeling. For CHA, distinguish founder accessibility changes from new material and measure the same function over serial generations. For energy, retain the three-electrode and two-electrode efficiency results separately. No reviewed numerical check licenses a DFT-derived existence claim, substituted-target admission, integrated organism model or intelligence conclusion.

Skipped whole-repository testing, destructive/output-writing reruns, fresh source downloads, hydrogen placement, electronic calculations and wet experiments. This review did not independently rederive every periodic connected component or repeat the prior runners. Main risk: correct source arithmetic can still be misused as evidence of joint physical function.

## Finalized compatibility/site extension

The later extension report is `recursive-compound-2026-10-15/review/extended-quantitative-review.md`. It supersedes the initial medium finding about literal heredity controls: the revised calculation now has real input-dependent controls and passed fresh independent inputs. The extension confirms six primary NMR table images and all 324 BVS sums, with no scientific blocker. Status remains WATCH / APPROVE because of nonblocking unnecessary unit/type interface validation in the heredity helper. PROTOCOL.md:38 should say bond-valence mismatch rather than substitution strain. The root synthesis REPORT remained pending during this review.
