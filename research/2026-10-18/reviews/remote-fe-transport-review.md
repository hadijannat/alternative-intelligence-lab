# Independent remote-Fe transport review

Scope: `documented-scaffold-2026-10-18/remote-fe-transport/`, Zhao et al. DOI 10.1038/s41467-025-60728-y. Reviewer owns this file only and does not edit executor code, data or results. This initial review read the frozen `PROTOCOL.md` and native methods/control audit before numerical response extraction. Qualitative published outcomes and control figures were already exposed: no blind validation is implied.

## Native-source and protocol review

Read-only verification with qualified Python 3.12, `hashlib`, `json`, PyMuPDF and `zipfile` independently matches all 11 records in `sources/acquisition-checks.json`, including byte counts/SHA256. Native PDF page counts are 12 main, 27 SI, 32 peer review and one reporting-summary page. Both workbook and CIF archives pass ZIP CRC checks. The workbook SHA256 is `354731677477e5f079cf32d5248d86da0fe4ddba2d6dbfc492f70c81ebde061a`. These checks verify acquisition integrity, not scientific validity.

Native method text confirms the 4:1 NiCl2:FeCl3 preparation versus nominal Ni0.75Fe0.25 naming, and the reversed Ni0.25Fe0.75 subscripts in a loading paragraph. Exact final composition must remain unresolved. The Zn-containing formula names a precursor; electrochemical conversion and Zn leaching prevent treating it as a fixed final molecular species. DFT vacancy structures/energies do not identify kinetic coefficients.

Independent visual inspection of `sources/si-figure6-control-page.png` confirms a useful control: initial CV stabilization in SC, exposure in SC/CEM/AEM, then CV in SC with refreshed electrolyte. This addresses persistent catalyst change beyond immediate membrane/electrolyte/bubble effects. It is not valid to say the source lacks any membrane-confound control. It does not equalize prior geometry, exposure potential, loading histories or independently identify Fe-origin function. Initial pH and EIS-based iR correction do not establish time-resolved local pH or a constant corrected CA interfacial potential. Counter-deposit assays use a separate loading/substrate; acid-extract concentration cannot be merged with low-loading CA as a complete Fe inventory. Oxygen isotope labeling is not incoming-versus-founder Fe labeling. Carbon/Nafion/electrode apparatus dependencies remain explicit.

The frozen A/B/C program is defensible within its stated boundaries: an outcome-exposed directional intervention screen, a synthetic finite-mass inhibition counterexample, and within-preparation temporal reserved forecasts with frozen cycles<=40 fitting. None independently predicts new-candidate chemistry or validates active repair.

For the ka=0 model, the A/D subsystem is cooperative and reducing kc while holding common nonnegative chemistry and identical initial pools yields A_low-sink>=A_high-sink. For A>0, x=D/A obeys `x'=kd+(kd−kr−kp−kc)x−kr*x*x`; scalar comparison also yields nondecreasing relative A_low-sink/A_high-sink. Conversion to observed normalized retention adds shared current/competence coefficients, matched time/window treatment and the membrane-only-sink boundary assumption. These are jointly falsifiable assumptions, not measured membrane permeabilities. The anchor supplied from AEM is permitted initial evidence; no later AEM response may fit a parameter. Within-trace medians/envelopes are not independent replicates or confidence intervals.

All CV branches must remain in the fixed-potential crossing range; refreshed SC controls are paired within an electrode, while different condition traces do not imply identical initial specimens. Derived TOF must not be used as an independent current response. The proposed A+D→2X term is a mass-counting phenomenological inhibition process, not an established elementary chemical reaction or measured FeOOH amount. Positivity, conservation and convergence are necessary numerical checks, not mechanism selection.

## Independent extraction and observed-response reproduction

Invocation: qualified `/USER_HOME/.pyenv/versions/3.12.3/bin/python3` read-only here-document loading the native workbook with `openpyxl.load_workbook(..., data_only=True)`, `data/native_cells.json`, and `results/analysis.json`. Each stored x/y cell value and finite-validity flag was compared directly with the workbook; all **27,461 rows in 12 blocks across a 19-sheet workbook match**. All four recorded source/protocol/script/data hashes match. The script's seven pure `selftests()` also pass when imported without invoking its output-writing main function. No executor output was overwritten.

CA windows were independently filtered with `[5,10)` and `[295,300]`, and median ratios recomputed. Results:

| Condition | Native finite points | Time extent, min | Anchor/end counts | Descriptive median retention | Strict full-edge result |
|---|---:|---|---|---:|---|
| SC | 18001 | 1.54773–301.53027 | 300 / 301 | 0.845608029379 | Supported for specified windows |
| AEM | 1800 | 0–299.83333 | 30 / 30 | 0.162476176613 | Null |
| CEM | 3600 | 0–299.91667 | 60 / 60 | 0.732184642718 | Null |

SC's appended 300-minute row occurs after later times, producing exactly one decreasing-time pair. It remains in the native records and endpoint window. The metadata-triggered handling is documented in `AMENDMENTS.md`; no endpoint is shifted or filled. The AEM/CEM descriptive contrast cannot become a completed strict 300-minute screen. This is an explicitly conservative coverage interpretation disclosed after clock metadata, not a claim of prospective/blind testing.

Independent CV interpolation used every adjacent finite source pair bracketing the fixed potential, preserved disjoint branches, and deduplicated equal crossing currents only at numerical tolerance. Each of the six before/after curves yields **two distinct crossings** at each potential (12 curve/potential evaluations). Arithmetic crossing means and all-extrema ratios reproduce the saved values within 1e−12:

| Potential (V_RHE) | Condition | Mean post/pre ratio | All-crossing ratio bounds |
|---|---|---:|---|
| 1.53 | SC | 0.849556547290 | 0.818241012117–0.881971502193 |
| 1.53 | CEM | 1.266341429292 | 1.262521782962–1.270176553411 |
| 1.53 | AEM | 0.400723346785 | 0.381951091849–0.420186268749 |
| 1.55 | SC | 0.860346730492 | 0.856974141370–0.863734887790 |
| 1.55 | CEM | 1.281432698829 | 1.279028261141–1.283839622394 |
| 1.55 | AEM | 0.432358720126 | 0.428621548716–0.436142103511 |

These branch envelopes are not uncertainty intervals or biological/experimental replicates. The matched refreshed assay supports persistent activity differences after exposure. It contradicts the combined lower-sink/common-competence/identical-start simplification conditionally; it does not uniquely select aggregation or demonstrate active incoming Fe. Normalized CA and post/pre CV need not agree numerically, because their normalization, measurement program and environment differ.

All three candidate series independently have cycles `[20,30,50,70,80,100,150,200]`, exactly two training observations and six reserved observations. All saved statuses are `insufficient_data`, with empty fit dictionaries. This correctly retains the frozen minimum-three rule. No actual material fit, prediction residual or held-out score is available. Synthetic fitter self-tests verify code behavior only; they cannot substitute for the missing empirical forecast.

## Independent synthetic model checks

Loaded `results/synthetic_trajectories.npz` read-only. Coarse/fine arrays have shapes `(5001,10,4)` and `(10001,10,4)`, with steps 0.001/0.0005 h. Independently computing `max(abs(coarse-fine[::2]),axis=(0,2))` reproduces every saved scenario difference. Maximum mass error is **1.2656542481e−14**, minimum pool is zero, and the ka=0 lower-sink ordering holds. The largest all-time/all-pool step difference is **1.15277465694e−5**, so the implementation's 1e−5 convergence flag **fails**. That tolerance was not specified in the frozen protocol; the two prescribed step sizes were. Both facts must remain explicit, without retroactively calling this fully converged.

The frozen parameter grid does produce transient reversals, while every five-hour endpoint remains positive:

| ka | Minimum coarse A(kc=0)−A(kc=2) | Time of minimum, h | Fine-grid minimum | Difference at 5 h |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0.408769410446 |
| 0.1 | 0 | 0 | 0 | 0.328087476229 |
| 1 | −3.86025e−13 | 0.001 | −2.40918e−14 | 0.111492787910 |
| 10 | −0.0251332445082 | 0.835 | −0.0251330800497 | 0.0122235509355 |
| 100 | −0.00681855635790 | 1.015 | −0.00681775667487 | 0.000931965008339 |

The ka=1 tiny sign change is numerical noise relative to the admitted tolerances, not a mechanism reversal. The ka=10/100 reversals are many orders larger than their step differences and persist in the saved fine arrays. They establish a conditional transient counterexample only. The grid does **not** reproduce the late-time experimental ordering, and no rates were fitted to do so.

Additional independent numerical cross-check, without changing or replacing saved results: integrate the full simultaneous ODE using classic RK4, dt=0.0001 h for 50000 steps, starting from `(1,0,0,0)` for all ten `(ka,kc)` pairs. The independently written derivative is:

```python
A, D, X, C = state.T
aggregation = ka*A*D
rhs = np.stack([-A+D-aggregation,
                A-(1.05+kc)*D-aggregation,
                0.05*D+2*aggregation,
                kc*D], axis=1)
```

Binary observables: all reference endpoint pools nonnegative; mass residual <=1.1214e−14; maximum endpoint difference from saved fine result **1.0793819956e−6** (saved coarse 4.3172258568e−6). This independently supports the finite-pool implementation's scale but does not replace the frozen step-halving failure or prove a measured mechanism. No reference trajectory/result file was substituted into the experiment.

The saved `results/observations.png` was visually inspected: all four panels are legible; the candidate panel explicitly reports no fit; the paired-assay bounds and synthetic transients are visible. The CA title uses reserved terminology, which must be read together with the explicit exposure and strict-null qualifications rather than as blind validation.

## Final interpretation review and terminal verdict

Reviewed final `REPORT.md`, `EXTRACTION.md`, `negative_results.json`, and `checks.md` against the native sources and independent calculations. The final report correctly preserves the strict CA null, matched-assay conditional contradiction, transient synthetic counterexample, five-hour grid failure, and insufficient candidate training data. It does not infer Zn-specific superiority from descriptive retention, transfer DFT energies into rates, or equate oxygen labels with Fe origins. Source correction of the initially missed paired-control block is preserved. The report's next primary lead is discovery-only and outside this review; no finding from that unacquired package is approved.

The extraction notes retain two reported execution failures (integer-buffer issue and initial convergence assertion stop) and explain that exit 0 means result emission. This reviewer reproduced the final pure tests and false convergence flag, not those historical failed invocations. No final scientific criterion was changed in this review, and the additional independent ODE reference did not replace any frozen output or failed result.

Final read-only JSON/hash assertions pass: exactly 15 unique negative IDs; no identified chemical rates, origin-specific repair, validated candidate forecast or added integrated complement; exactly 11 true checks and one false convergence check; all four input/data hashes and all four recorded artifact hashes match. This is a scoped ledger/integrity audit, not an independent global-history audit.

Final SHA256:

- `PROTOCOL.md`: `5b0883b22a6e410cbac92d6cbe274c9aee24a34ca02216b3df8444e703f340fb`
- `AMENDMENTS.md`: `7f8fe83b0227e1cc854a08abf6ec94aa6ea3d1460639fe8027a4ffbe846afd8d`
- `analyze.py`: `fece55b1129420937c47397f16fa9fbf3fa0abba384fc70d9233a341c1be5fa6`
- `data/native_cells.json`: `bafd500be3ddf99cd144970d29dedfa6eef59fc91aa301f3414f462fbcae56b2`
- `results/analysis.json`: `3765cca352b898b9333818fda5c653e065c208abedd783df46870e068c1d76cc`
- `results/synthetic_trajectories.npz`: `366a9d50f7d55774792921b97c1601310bf91c36907bd17d271a22a18cb81ae9`
- `REPORT.md`: `8e228801e90d50e28a77b29ec8d4133059de0da94afbac67109f967740de840e`
- `negative_results.json`: `eaa95e94f4a75c076362f5d1bbd8f23ad2766fd6b278b8fd6446f38387fbd6d2`
- `EXTRACTION.md`: `26138b9280e09119d9ee78e9102918f46dc6b0b0835af21cefbf8803bfd74721`

**APPROVE — bounded retrospective intervention analysis and synthetic coupled-chemistry test with explicit negative outcomes.** This approves faithful analysis/reporting of the failed and incomplete tests, not the proposed late-time mechanism, convergence tolerance, held-out candidate performance, active repair, inheritance or integrated life objective. No blocking correctness or interpretation issue remains in this bounded artifact. Parent may mark independent review complete; no further model run is needed.
