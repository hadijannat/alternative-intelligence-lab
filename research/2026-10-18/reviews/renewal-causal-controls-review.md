# Renewal causal controls independent review

Scope: `documented-scaffold-2026-10-18/renewal-causal-controls/` scientific audit, report, R clarification, protocol, negative results, three source scripts and their receipts. Read-only review of target artifacts; only this review artifact was written. No ulw-loop plan exists (status returned `ULW_LOOP_PLAN_MISSING`); report location follows the assigned scoped review path.

## Findings by severity

- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: `REPORT.md` final paragraph links to local `checks.md`, which was absent during inspection. Add the promised check record or correct the reference before final handoff. Source receipts and `sources/verification.json` do exist, so this is a navigation gap rather than unsupported success reporting.

## Evidence and scientific assessment

Independently read the actual native `sources/nishioka-browser-main.pdf` using PyMuPDF, with focused inspection of PDF pages 2, 3, 6-10. Viewed the page 6 and 7 renders: 0.399 C/cm2 and 0.399 mC/cm2 are visibly printed. The reported literal 1000-fold discrepancy is genuine; no corrected numerical capacity is silently selected.

Fresh read-only Python checks confirm all five stored payload sizes and SHA256 hashes match the receipts. Four initial HTTP403 bodies lack PDF signatures; only the later 1,069,448-byte main is a PDF, with 11 pages and SHA256 cc0a2f41fb99889e0b28cebe2d21270e3c532823f515727b89f53953862ce825. The frozen origin-function protocol still hashes to 45b71ca66ad444a71586a53bb6174fd51fc3c9d81eb56b58e72314ae904908b2.

Fig. 6 explicitly assays the recovered electrode's first CV back in 1 M phosphate. Methods specify repeated externally programmed oxidation in KOH. The audit accurately distinguishes persistent recovery under a common assay medium from an immediate electrolyte change. Methods also explicitly distinguish the quartz-supported Ti/304SS sputtered EQCM coating from the bulk functional sheet. Fig. 7's sheet wording does not establish matched specimen identity; the audit preserves this limitation.

The native source supports dissolution-consistent observations and a conditional Ni/Fe mass attribution, while reporting reconstruction/removal and re-exposure possibilities. Rejecting a claim of *known pure* deblocking is justified. This does not experimentally exclude retained-site exposure as a contributor, and the report correctly leaves that rival unresolved. XPS similarity cannot establish atom inventories, and no same-specimen origin/function reconstruction series is present.

Compared R clarification directly to row R of `recursive-compound-2026-10-15/PROTOCOL.md`: new competent material, restored function, accounted feed/founders, and the specified controls remain required. Allowing a validated causal/material bound instead of exclusive atom-by-atom current attribution is consistent with that contract. The factorial interaction alone is explicitly insufficient. None of the twelve integrated requirements is promoted.

Missing SI, Stevens and Cimino native bytes are disclosed throughout. The transient primary-reader leads are labeled as such and no numerical result is used from them. Their scientific details were not independently reacquired in this review and are not elevated to native-source-verified evidence.

## Code and skill perspectives

Consulted `omo:remove-ai-slops` and `omo:programming` SKILL.md review criteria. Read all three new scripts and the reused origin-function acquisition helper. No material violation found in the scoped additions. The source integrity checks exercise real stored bytes, PDF structure, DOI and the explicitly relevant source-unit conflict. They are not deletion-only, tautological or phrase-pinning prompt tests. Text extraction and render generation serve the requested source audit; no unnecessary numerical model, parsing layer or new abstraction is introduced.

The shared helper's pre-existing broad exception handling records acquisition failures rather than fabricating success; it was not changed here. Cross-directory helper reuse is explicit and needs that helper included wherever scripts are published. The browser acquisition script's HTTP success assertion is complemented by actual PDF-signature and identity verification in the separate verifier.

The existing eleven-check verification artifact and verifier implementation were inspected. A separate read-only byte/hash/page check was executed; acquisition scripts and the artifact-writing verifier were not rerun, preserving target files. Integrity checks are not empirical renewal validation.

## Verdict

- codeQualityStatus: WATCH
- recommendation: APPROVE
- blockers: none
- reportPath: `.omo/evidence/renewal-causal-controls-review.md`

Approval is bounded to the source-audit checkpoint and its scripts. It does not establish active-material renewal, inheritance, integration or the full objective. Residual limitations are the missing native supplements/other leads, unmatched material/function specimens, absent causal material-origin controls, and the low-severity checks-link gap above.

## Follow-up resolution

Inspected the newly created `documented-scaffold-2026-10-18/renewal-causal-controls/checks.md`. The report link now resolves to a substantive check table distinguishing source integrity, common-medium recovery, missing native inputs, unresolved material-function attribution and unclosed integrated requirements. The LOW navigation finding is resolved. Updated codeQualityStatus: CLEAR; recommendation: APPROVE; blockers: none. Earlier review and its evidence remain preserved above. No source acquisition or native checks were rerun for this documentation-only follow-up, and no remote publication claim was independently verified.
