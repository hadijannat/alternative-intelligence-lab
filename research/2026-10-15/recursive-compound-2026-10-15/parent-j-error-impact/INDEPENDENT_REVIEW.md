# Independent saved-array J-error impact review

codeQualityStatus: CLEAR
recommendation: APPROVE
blockers: []
Scope: COMPLETE_FIXED_DENSITY_SENSITIVITY_ONLY; original repeatability failures remain unchanged.

## Integrity and independent method

All14 preparation file hashes matched before and after this audit. The independent approval status/reviewer and preparation SHA match analysis-gate.json; the approval file digest also matches that gate. All six original comparison dictionaries and categories agree exactly with the preserved comparison report. same_sign, sign_reversal and external_run remain NONPASS. Five individual comparisons fail and only J2-Jold passes the unchanged absolute1e-10/rtol0 threshold.

This reviewer did not call run.impact or import the scientific helper chain. P0 was loaded directly from the saved NPZ, retaining just that one full float64(3068,3068) array and verifying cycle0. Each pair used read-only J memory maps and seven-row blocks (different from the implementation's16). Differences/products were computed in binary64; math.fsum reduced products within each block and then the block sums. Independent norm reductions used the same different block partition. Each map was closed. Native thread variables were limited to1; no PySCF import, molecule, integral, operator, PCM or SCF ran, and no full difference/product matrix was allocated.

## Precise recomputed results

| Original name | Oriented expression | Signed delta E_C (Hartree) | Frobenius deltaJ | Max absolute entry | First argmax | Entries >1e-10 | Original pass |
|---|---|---:|---:|---:|---|---:|---|
| J2-J1 | J2-J1 | -4.0090968424324936e-11 | 4.763252807384829e-9 | 4.844054046770907e-10 | [2972,2972] | 284 | false |
| J3+J1 | (-J3)-J1 | 3.6796504298973436e-11 | 4.4628367741939295e-9 | 4.420286359163583e-10 | [2972,2972] | 231 | false |
| J3+J2 | (-J3)-J2 | 7.688747272329835e-11 | 2.2840689340323172e-9 | 4.142748366575688e-10 | [3022,3022] | 31 | false |
| J1-Jold | J1-Jold | -1.7423967359701155e-11 | 4.833060938041598e-9 | 4.718572199635673e-10 | [1882,1882] | 304 | false |
| J2-Jold | J2-Jold | -5.7514935784026085e-11 | 1.3577927182894635e-9 | 9.484324436925817e-11 | [3007,3007] | 0 | true |
| J3+Jold | (-J3)-Jold | 1.9372536939272274e-11 | 1.9576723440132433e-9 | 3.2159164220502134e-10 | [3022,3022] | 14 | false |

J3 is explicitly negated before subtraction. For each sign-reversal comparison, this oriented delta is the negative of the original J3+reference difference: the signed energy reverses orientation, while maxima, argmax, Frobenius norm, exceedances and pass flag remain unchanged. All original max/argmax/exceedance/pass values reproduce exactly.

P0 entrywise L1 norm is9366.407519201193 and Frobenius norm50.931127600029754. Recomputed energy bounds:

| Original name | 0.5*L1(P0)*max(deltaJ) | 0.5*F(P0)*F(deltaJ) |
|---|---:|---:|
| J2-J1 | 2.2685692123545996e-6 | 1.2129891826205834e-7 |
| J3+J1 | 2.0701101695746126e-6 | 1.136486546022881e-7 |
| J3+J2 | 1.9401334725426493e-6 | 5.8165103163231946e-8 |
| J1-Jold | 2.2098035065280643e-6 | 1.2307662166705805e-7 |
| J2-Jold | 4.44170238602828e-7 | 3.457695709479596e-8 |
| J3+Jold | 1.506079187830686e-6 | 4.985322997599392e-8 |

Both norm bounds agree with recorded values within four binary64 spacings, used solely as an arithmetic comparison check. They are computed norm inequalities, not certified outward-rounded intervals.

## Rounding assessment

The independent seven-row/two-level fsum energies differ from the recorded single-global-fsum energies only for J2-J1 (-1.9387045606711586e-26Hartree) and J1-Jold (+6.462348535570529e-27Hartree); the other four agree exactly as binary64 values. DeltaJ norms differ by at most a few binary64 spacings.

Sums of absolute binary64 products range2.91214621931697e-9 to8.42547853101659e-9. With u=2^-53, the illustrative arithmetic scale4*u*0.5*sum(abs(products)) ranges6.466263567521602e-25 to1.8708320517239117e-24Hartree, comfortably above the observed regrouping changes. This is a rounding diagnostic for the already formed binary64 products, not a new scientific tolerance, certified exact-real interval, or bound on error introduced when the original J arrays were generated. It does not certify subtraction/product formation relative to exact physical operators or restore the five failed repeatability comparisons.

## Findings and skill perspectives

CRITICAL: none.
HIGH: none.
MEDIUM: none.
LOW: compact/untyped script conventions remain as in neighboring diagnostics; no demonstrated numerical regression follows here.

Programming/remove-ai-slops perspectives were consulted earlier in this review session and applied to run.py and test_run.py. The five synthetic tests cover an off-diagonal contraction, sign orientation, catastrophic cancellation, malformed/nonfinite inputs and pre-output approval failure. These are meaningful arithmetic/admission behaviors, not removal-only, prose-pinning or implementation-mirroring tests. Tests were inspected rather than rerun during this independent real-saved-array review. Bounded blocks, input validation and sign normalization are required by the declared task; no needless abstraction or extra parsing was identified.

No AO/element localization was invented: the absence of a complete saved AO map remains explicit. No production source, preparation, comparison or result file was changed.

This evaluates 0.5*sum(P0_ij*deltaJ_ij) at the same saved cycle-zero density only. Small signed contractions may reflect cancellation and establish neither relaxed-density/SCF accuracy, chemical accuracy, final parent convergence, crash cause nor integrated function. All prior failures and scientific admission limits remain in force.

