# Parent J stage-localization result

The diagnostic completed all three calls, but the ordinary repeat still fails the unchanged absolute1e-10/rtol0 screen. Reusing the first solved coefficient vector in the controlled third call passes that comparison. This narrows the next numerical investigation; it does not qualify the ordinary operator or repair parent SCF.

Authoritative records are run-v1/result.json, comparisons.json, supervisor.json and launch-result.json. Execsession80130 exited0; worker53270 is absent. Status COMPLETED_BOUNDED_STAGE_LOCALIZATION means the diagnostic recorded its outcomes. One child completed three J calls, zero SCFs and zero PCM builds in698.8856680409517seconds. Sampled maximum RSS was3643949056bytes, below the frozen10-GiB guard; it is not a certified peak. No resource termination or monitor error occurred. All30 terminal artifact hashes match. The exact preparation, approval and independent prelaunch review are preserved.

| Contrast | Maximum absolute J difference | Entries above1e-10 | Screen |
|---|---:|---:|---|
| Ordinary B minus ordinary A | 1.1883116712851916e-10 | 2 | FAIL |
| Controlled fixed-rho-A minus ordinary A | 6.536993168992922e-13 | 0 | PASS |

All nine arrays were saved before classification: three full J matrices, three auxiliary RHS vectors and three ordinary solved coefficient vectors. C preserves its ordinary RHS and solved vector separately, but supplies an independent exact copy of rho_A to pass2. Its output is J_fixed_rho_A, not ordinary J(P0). A/B preserve solver-return object identity. Runtime, density, factor and initialized optimizer guards passed. Deferred stage timestamps describe receipt flushing rather than internal factor timing.

| Saved ordinary vector contrast | Maximum RHS difference | Maximum coefficient difference |
|---|---:|---:|
| B minus A | 1.000444171950221e-11 | 0.00014680086590868058 |
| C minus A | 2.4556356947869062e-11 | 0.000893604225027822 |

saved-vector-sensitivity.json reports relative L2 changes. RHS changes are about1.17e-15 and2.09e-15 relative to A; coefficient changes are about3.02e-6 and1.25e-5. Their observed relative-response ratios are about2.58e9 and6.00e9. These are descriptive comparisons, not certified metric condition numbers: the original metric/factor is not saved, exact-system residuals and backward error are not established, and finite-precision solve behavior has not been isolated.

Different RHS vectors establish variability before the solve. The much larger coefficient response and passing fixed-coefficient contrast make RHS/solve sensitivity the next priority. One controlled contrast does not prove exclusive upstream causation or downstream determinism; the controlled difference remains nonzero. C also substitutes the rho-dependent screening input, so it does not isolate contraction arithmetic alone. Call order and common implementation remain limitations.

Freezing coefficients is not a production correction: it would ignore density changes required by SCF. The next separately reviewed diagnostic should distinguish repeated solves of identical RHS from responses to saved small RHS perturbations and measure the metric's numerical sensitivity with explicit residual/error checks. It must retain the original failing screen and qualify any proposed stabilization against independent numerical references before parent reuse. No new native attempt is authorized by this report.

Earlier signed-J and repeatability failures remain unchanged. The target molecule, chemical accuracy, active retention, functional inheritance and intelligent life remain unverified. This result contributes zero physical admissions.

Independent terminal review in INDEPENDENT_TERMINAL_REVIEW.md reproduces both matrix comparisons and four vector comparisons using seven-row blocks, verifies288 grouped pins and all30 terminal hashes, and independently agrees with the descriptive vector norms. Its CLEAR disposition applies to evidence classification; the ordinary operator remains nonpassing.
