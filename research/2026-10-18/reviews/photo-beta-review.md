# Independent photo-input and Beta review

2026-10-18. Read-only review of `documented-scaffold-2026-10-18/photo-complement` and `renewal-lead`. No production source, data, protocol, or result files changed. This artifact is the reviewer's sole write.

## Verdict

PASS for the bounded source-consistency and retrospective descriptor comparisons. No arithmetic or source-transcription defect found in the inspected inputs and results. This verdict gives **no active-material renewal (R), functional heredity (H), integrated-system, life, or intelligence credit**. It also gives no chemical identity/stability credit to Mo34WV.

## Actionable interpretation constraints

1. The 202-row photocharge/release trajectory is a charge-coordinate accounting construction with prescribed charge endpoints. It supplies neither rate constants nor a current-versus-time prediction. Calling it a validated kinetic simulation would overstate the result. Only 1.94849% of nominal two-electron inventory capacity is exercised; color return and charge recovery do not identify replacement of damaged molecules or survival of the entire inventory.
2. The SI-6 discharge potential is +0.75 V versus Ag/AgCl, not a full-cell energy integral. SI-7's 1.5 V full-cell discharge is explicitly an assumption in a different 100 C scenario. The computed 1.46019% HHV/input ratio is that illustrative scenario, not a measured 47 C-cycle efficiency. Energy from lamp wall-plug conversion and balance of plant remains excluded.
3. The oxygen assay uses a Pt-mesh counterelectrode; the source photocharge/release experiment uses carbon felt for mediator reduction. The 84 +/- 6% O2 result cannot be inserted into this trajectory as a measured same-cycle leakage rate. Unmeasured O2 equivalents remain formal predictions.
4. Beta's constrained alpha=0 rejects positive bulk-composition association **within the fitted descriptor**. It does not establish absence of seed dependence: source section 3.2 states no Beta phase without seed, and crystallinity, morphology, crystal size, and dissolution differ across seeds. Composition, size, template history and crystal perfection are confounded. The fitted environmental term is not measured gel composition or a balanced dissolution/precipitation mechanism.
5. Pure-silica parents S9/S10 are two related, retrospectively selected cases with differing preparation time/crystal quality. Their exclusion from parameter fitting is correctly recorded, but does not provide blind validation or independent lineage replication. The observed Al-containing products reject literal parent bulk-composition copying; topology-directed nucleation and founder residue contributions remain possible.
6. Oxide-ratio conversion `x_Al = 2/(r+2)` is correct. The table's 10 wt% seed addition is relative to the silica source; the reported product yield has no identified denominator in the inspected methods/table footnotes. Thus no empirical final founder fraction or founder-function bound follows. Product nitrogen-accessible micropore volume alone cannot assign catalytic function to newly formed descendants.
7. Organic templates were used to prepare seeds before calcination (540 C, 6 h). Subsequent alkaline gel growth at 140 C is not evidence of common-medium integration with acidic PMo12 electrochemistry. Both studies support particular component phenomena; neither closes renewal or functional inheritance.

## Primary inspection

Inspected Bloor SI sections SI-3, SI-6 and SI-7 in `photo-complement/sources/bloor2016-si.txt`, and visually checked `si-page-7.png`. Confirmed 25 mL, 0.5 M mediator, 47 C reduction and reoxidation, 6.0 +/- 0.2 mL H2, Ag/AgCl reference, carbon felt, Pt mesh and Nafion; confirmed the separate 100 C/1 mA/0.1 W/1.5 V efficiency assumptions.

Inspected Zheng methods 2.1-2.3, Tables 1/2 and section 3.2 in `renewal-lead/sources/zheng2014-pdf.txt`; visually checked `page-4.png` containing Table 2. Confirmed extracted numeric table entries, source cation-ratio basis, missing pore/yield fields, precursor preparation and growth conditions.

## Independent execution evidence

Invocation: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3 -` from repository root, executing a read-only inline program using only stdlib and NumPy. It independently reconstructed the arithmetic below, asserted table values against the JSON extraction, compared outputs against both `results/analysis.json` files, and asserted SHA256 matches for both analyze.py/protocol pairs, both Bloor PDFs and the Beta table JSON. Exit code 0. Captured command output:

```json
{
  "independent_photo": {
    "capacity_C": 2412.125,
    "capacity_fraction": 0.019484894024977977,
    "H2_mL": 5.845468207493393,
    "HHV_efficiency": 0.014601927709736142
  },
  "independent_beta": {
    "unconstrained_slope": -0.13633415120305076,
    "zero_slope_intercept": 0.16185897435897434,
    "composition_rmse": 0.004807692307692318,
    "copy_rmse": 0.16666666666666666,
    "pore_common_rmse": 0.009013878188659962,
    "pore_copy_rmse": 0.041231056256176596
  },
  "checks": "PASS; table cells, result arithmetic, source/code/protocol digests"
}
```

Independent calculation recipe: `F=96485; capacity=2*F*.025*.5; H2_mL=47/(2*F)*24000; efficiency=(100/(2*F)*286000)/(100/.001*.1+1.5*100)`. Beta seed oxide ratios `[11,12,23,22,31,38,30,29,inf,inf]`, product ratios `[11,11,11,10,10,10,10,10,10,10]`; convert each with `2/(r+2)`. Compute ordinary covariance/variance slope on the first eight pairs, and compare the mean product Al fraction to the last two. Micropore training products `[.18,.21,.20,.20]`, test products `[.21,.20]`, test parents `[.16,.17]`; all errors are root mean square differences in stated units. Source-consistency binary observable: computed H2 lies within [5.8,6.2] mL. Descriptor binary observable: unconstrained slope is negative, constrained positive-memory optimum is alpha=0. These are narrowly defined observations, not biological acceptance criteria.

Reviewed code/result digests: photo analyze.py `38172035ac0567e06bb6121b9977178e634fa2273ccc4b6817f1017c6438d60a`; Beta analyze.py `2a4009844878b428f292205743b0806f5f021e919bb59c38f0f302cce0f9ecf4`; Beta tables `1bf3a6fb72c7196c0beafed63553150bf3c0a33d68a062759c1447988a050b79`.

Limits: no fresh experiment, new holdout acquisition, kinetic parameter identification, or full cell voltage integration was performed. No source claims were transferred to Mo34WV, and no negative result was removed.
