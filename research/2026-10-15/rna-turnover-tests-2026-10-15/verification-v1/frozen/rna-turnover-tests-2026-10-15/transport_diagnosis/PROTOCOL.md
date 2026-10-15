# Retrospective transport diagnostic

Scope: audit the already selected `independent_inactivation` chemistry and the two saved transport fits. No optimizer, no new parameter estimation, no benchmark-based selection, and no changes to earlier laboratories.

1. Hash all read inputs; verify the 108 Figure 2/3 observations directly against their workbook coordinates. Recompute saved residuals and replay both transport parameter sets.
2. Report prediction-minus-observation residuals by figure, initial seed, FT count/generation, with dynamic rows separate from structural zeros. Keep the original Figure 2 seeds 0/1 calibration and Figure 2 seed 2 plus all Figure 3 benchmark labels.
3. Verify initial weights, feed, transfer counts, analytic founder survival, moiety conservation, and the identity of Figure 2 FT3 predictions with Figure 3 G1 predictions. Compare the independent experiments descriptively, without resolving their discrepancy by fitting offsets.
4. Demonstrate aggregate-loss non-identifiability using two prespecified, equal-inventory loss maps for a synthetic homogeneous mixture: concentration thinning and whole-content loss in a fraction of fixed-volume cohorts. Use the selected chemistry unchanged. This is a mathematical counterexample, not a fitted alternative or evidence for catastrophic vesicle loss.
5. Demonstrate the existing differential-retention implementation's treatment of Cy5-F1 with a synthetic state only; the saved baseline has equal retention, so this cannot explain its failure.
6. Record source-supported conditions and unmeasured closures. Recommend the smallest future tests, preserving the existing benchmark as untuned retrospective transport evaluation.

Runtime: Python 3.12.3, numpy 2.4.1, scipy 1.16.1, matplotlib 3.10.8, openpyxl 3.1.3 through the existing offline uv cache. The new script includes assert-based checks and verifies unchanged input hashes on completion. All prior measurements and outcomes have been inspected, so no result is fresh experimental validation.
