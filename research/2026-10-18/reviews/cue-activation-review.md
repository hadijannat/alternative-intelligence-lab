# Cue activation independent review

Reviewed 2026-10-18. Scope: `documented-scaffold-2026-10-18/cue-free-inheritance/PROTOCOL.md`, `extract_markers.py`, `assess_activation.py`, data/results, GTM3/STW findings and relevant saved primary source sections. Root REPORT/checks/progress documents were being authored concurrently and are outside this review snapshot. No ulw-loop plan exists (status returned ULW_LOOP_PLAN_MISSING); this is the fallback report location. No clean tracked diff was supplied; review uses the explicit file scope.

codeQualityStatus: CLEAR
recommendation: APPROVE
blockers: none

## Findings

CRITICAL: none.

HIGH: none.

MEDIUM: none remaining. The initial missing catalyst identifier finding was corrected: CSV rows, extraction receipt, results JSON, and plot title explicitly identify GTM-4(RS-OMBMEP). The separate PROVENANCE_ADDENDUM preserves the frozen protocol without rewriting its history.

LOW: none requiring action.

## Reproduction and numerical review

Executed both scripts using `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`, imported with BASE redirected to an isolated temporary directory containing the protocol and a symlink to immutable sources. No reviewed output was overwritten. Fresh markers.csv and activation.json were byte-identical to the supplied files.

- Extraction: A untreated/preactivated 12/12; B untreated/preactivated 10/11; four excluded legend markers. Native raster was visually inspected. The two circle-arc exceptions match visibly partially occluded red A markers near conversion 87% and 100%; they do not add observations to the substrate fitting set. Explicit partial-extraction omissions are retained.
- Rate ratio 3.9383684506776344; withheld RMSE 0.027472510446705206. Withheld conversions 0.87369 and 0.89849 have predictions 0.96712175 and 0.98217571 against raster ee 1.00107. These are two points on one resolution-limited plateau, not independent strong mechanism validation.
- Untreated unlike-product turning excursion 0.09907; after pairwise 0.04 allowance, margin 0.05907. Preactivated turning margin is negative. The ordered-triple x separation exceeds the sum of two x allowances.
- The stationary-branch argument is valid for the stated initially racemic irreversible first-order two-pool model: consumed-pool ratio is monotonic, and a fractional-linear transform with nonnegative branch weights has constant derivative sign. This does not reject arbitrary stationary multistate mechanisms or establish site activation uniquely.
- Bisection, symmetry, conservation, positivity and synthetic ratio recovery self-checks passed. Grid refinement uses only six training observations. Thresholds and split are explicitly retrospective. The coordinate-offset analysis is correctly described as a restricted sensitivity check rather than a confidence interval.

## Primary provenance and chemical scope

Verified eight GTM receipt asset hashes and all five successful STW asset hashes. Inspected 2025 native PDF Figure 1 and methods/discussion: room-temperature overnight butanol preactivation, 20 wt% catalyst relative to TSO, 1 mg/mL racemic TSO, and the GTM-4 source identity agree. Source text separately describes 50 C and 115 C humidity preparations with XRD follow-up through 168 h; it does not provide a post-humidity catalytic-survival assay. The 120 C butoxide/inactivity statement is qualitative and remains so in the reviewed protocol/findings.

Butanol is an active carbon-containing ligand/reactant. The evidence supports a bounded complement for an inorganic catalyst, with no admission as fully noncarbon active organization. No copying, founder-excluded inheritance, renewal, PMo12 coupling, or life/intelligence claim appears in the reviewed numerical artifacts. STW original SI recipes retain independently supplied chiral organic cues; absence of a qualified inheritance dataset is appropriately bounded by accessible-source limits.

## Skill perspective

Consulted `omo:remove-ai-slops` and `omo:programming` before judging relevance and maintainability. Extraction and assessment contain 118 and 135 nonblank/noncomment lines respectively. No deletion-only, prose-pinning, tautological success, or implementation-constant-only test substitutes for behavioral evidence. Exact marker counts are legitimate pinned-source extraction checks; conservation/symmetry and synthetic recovery cover distinct numerical properties. Parsing and digitization are required by this source-analysis goal. No needless framework or abstraction was found. No substantive violation of either skill perspective was identified.

## Terminal follow-up

Inspected the named provenance correction plus REPORT.md, checks.md, progress.md, negative_results.json and PROVENANCE_ADDENDUM.md. Confirmed exact catalyst identifiers agree across all 45 CSV rows and both JSON artifacts. Protocol hash matches both receipts. Verified the reported sensitivity ranges directly from saved scenarios: ratio 3.33471–4.77627 and prediction 90.37–99.79%. The report correctly does not assert that every sensitivity scenario passes. The numerical conclusions, fit/split and interpretation remain unchanged. Final narrative preserves zero integrated complements, missing inheritance, carbon dependency, qualitative thermal inactivity, source-access failures, and retrospective screening limitations. No additional overclaim or blocker found. Pending-review fields in checks/progress can now be finalized by the root.

Unchecked: inaccessible Catalysis Today full text and Kang main paper; no new experimental replication or prospective validation. The retained two-marker plateau and unreported analytical uncertainty limit the apparent ratio's scientific strength.
