# Fixed-parent-geometry metal bond-valence test

**Outcome: a reproducible geometric prioritization only; target remains unverified.** All 36 metal positions (18 crystallographic labels, two inversion-related copies each) were tested with fixed 2.5, 2.6 and 2.7 Å coordination cutoffs. The proposed [MoVI34 WVI VV O112(H2O)16]9− structure is not established by this calculation.

## Primary parameter qualification

Source: [Gagné & Hawthorne (2015), DOI 10.1107/S2052520615016297](https://doi.org/10.1107/S2052520615016297), Table 4, journal page 573, [author-hosted electronic reprint](https://www.frankhawthorne.com/_files/ugd/70a3a9_6d2fb8aaf48e437eab87bbcd3798ab59.pdf). Downloaded PDF and extracted text are in `sources/`; byte counts, timestamps and SHA256 are captured in `.omo/evidence/author-retrieval.json` and `validation.json`. Direct IUCr retrieval returned HTTP403 (`iucr-retrieval.log`); author retrieval returned HTTP200 and repeated download matched bytes.

| Ion–O pair | R0 / Å | B / Å | Coordination polyhedra | Published RMSD / vu |
|---|---:|---:|---:|---:|
| Mo(VI)–O | 1.903 | 0.349 | 970 | 0.143 |
| W(VI)–O | 1.909 | 0.339 | 436 | 0.188 |
| V(V)–O | 1.799 | 0.388 | 714 | 0.105 |

One publication supplies three parameter rows, not three independent sources. W has the fewest calibration polyhedra and largest tabulated RMSD. These are inorganic oxygen-ion parameters, not target-specific hydrated polyoxometalate validation. The source uses first coordination shells and includes long first-shell bonds; it supplies no universal 2.6 Å prescription. Source RMSDs are calibration summaries, not site uncertainties or statistical significance thresholds. Parameters were parsed from the saved Table 4 text; none were fitted here.

## Calculation and fixed decisions

For each metal and each oxygen within the prescribed cutoff, compute `s = exp((R0 − distance)/B)`, then `BVS = sum(s)`. Rank by `abs(BVS − formal oxidation number)` separately for Mo6, W6 and V5. Dense ranks group scores at 1e−8 vu to prevent floating-point inversion-copy differences from creating false preferences. All distances use the original parent coordinates. No optimization or cutoff tuning occurred.

The original CIF is `noncarbon-discovery-2026-10-15/research/structure/raw/cod2107026.cif`. Original extractor was independently executed from that CIF at all three cutoffs and its 2.6 Å mapping exactly matched the supplied mapping. The XYZ matched mapping coordinates within its printed precision. Every cutoff retains the same 164-atom heavy fragment and gives the same contact counts and scores; coordination is 6 or 7. Largest included distance is 2.440658 Å. Nearest excluded oxygen **within the extracted fragment** is 3.383745 Å. `contacts_through_3_5A.csv` retains nearby excluded fragment contacts. This diagnostic is not an all-crystal contact inventory, although original periodic extraction verifies coordination counts at every tested cutoff.

## Numerical outcome

| Fixed cutoff / Å | Parent BVS range / vu | Parent RMSD from 6 / vu | W best labels | V best labels |
|---|---|---:|---|---|
| 2.5 | 5.903477–6.312166 | 0.144677 | Mo8@0, Mo8@2 | Mo7@0, Mo7@2 |
| 2.6 | 5.903477–6.312166 | 0.144677 | Mo8@0, Mo8@2 | Mo7@0, Mo7@2 |
| 2.7 | 5.903477–6.312166 | 0.144677 | Mo8@0, Mo8@2 | Mo7@0, Mo7@2 |

W substitution at Mo8 gives BVS 6.004790 (absolute mismatch 0.004790 vu). The next distinct W label is Mo9, 6.052544. V substitution at Mo7 gives BVS 4.719064 (absolute mismatch 0.280936 vu). The next distinct V label is Mo18, 4.677169. All V-site sums are below 5 (range 4.452898–4.719064).

**The V-best label Mo7 is also the parent-worst label:** Mo BVS 6.312166, mismatch +0.312166 vu. Its V ranking therefore depends on an already overbonded parent geometry. Retain this disagreement; do not interpret ranking as independent evidence of favorable V incorporation. Parent RMSD happens to be close to the published Mo calibration RMSD, but these quantities do not prove accurate local oxidation states or model transferability.

The two best element-specific labels differ, so distinct substitutions could be named Mo8→W and Mo7→V for a future structural hypothesis. No coupled pair calculation is performed: these ranks omit oxygen valence redistribution, W–V interactions, protonation, counterions and relaxation. They cannot distinguish relative placement of inversion copies. No pair energy or synthesis recommendation follows.

## Boundaries and concrete next experiment

Hydrogens are absent. Oxide versus coordinated-water identity and protonation remain unresolved; the same oxygen-ion parameter law was used for every selected O donor. Its transfer to unidentified aqua donors is a substantive limitation. Long contacts outside the fixed cutoffs and the missing surrounding solvent/ionic environment may affect interpretation. First-shell completeness and aqua identity require inspection of the parent refinement and ultimately a chemically complete structural model.

This test neither establishes target existence, thermodynamic or kinetic stability, oxidation localization, electronic structure, novelty, function nor life/intelligence. No probability is assigned. The next computational gate is an explicit, chemically justified protonated/hydrated target model followed by a method-qualified geometry comparison; the next empirical gate is structural/spectroscopic identification of actual incorporation and oxidation states. Neither gate was run here.

## Reproduction and evidence criteria

Invocation from workspace root:

`python3 recursive-compound-2026-10-15/site_chemistry/evaluate.py > recursive-compound-2026-10-15/site_chemistry/.omo/evidence/run.log`

- Primary qualification: three Table 4 rows parsed; observable is complete exact parameter records in `parameters.json`; captured source PDF/text and SHA256 in `.omo/evidence/validation.json`.
- Geometry provenance: rerun original CIF extractor; observable is exact mapping equality plus 164 XYZ atom matches; captured assertions and input hashes in `validation.json` and `run.log`.
- Complete sensitivity: 36 sites × 3 cutoffs; observable is 108 rows in `site_scores.csv`, all cutoffs represented, with parent agreement retained in `cutoff_summary.csv`.
- Arithmetic: scalar `math.dist`/`math.fsum` versus vectorized NumPy distances/exponential sums; observable is maximum difference <1e−12 vu across all 324 sums. Inversion-copy sums agree within 1e−10 vu. Captured in `validation.json` and the executable assertions in `evaluate.py`.
- No target admission: observable `target_admitted: false` in `validation.json`.

All source and input hashes are retained. Runtime outputs are generated only inside this directory; identity files and the original CIF are read-only inputs.
