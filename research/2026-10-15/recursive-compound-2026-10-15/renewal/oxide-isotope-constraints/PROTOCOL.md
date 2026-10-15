# Oxygen-isotope measurement constraint

This is a retrospective source extraction and arithmetic check, not a preregistered experiment, fitted model, or holdout test. Scope is the acquired original SI to DOI [10.1021/ja905166c](https://doi.org/10.1021/ja905166c), selected because its site-resolved signals distinguish oxygen exchange from molecular transformation. Main-article bytes are unavailable and supply no numeric input.

1. Check the SI's exact SHA256 and 513,814-byte size. Retain the original PDF and publisher metadata unchanged.
2. Extract all 17 rows and seven sites from Table S-1-2 (S3). Check the rendered table. Preserve both pH 8.03 rows and their distinct concentrations. The table's `log(k) s^-1` does not explicitly define its base. Use reported log differences as primary quantities; CSV `log_base=10` is a declared conventional arithmetic assumption, with fold ratios conditional on that assumption.
3. Keep rate and reported uncertainty separately. Preserve source `--` as blank numeric fields. Mark only the three Site D entries at 35.5 C and pH <=7.5 as `too_fast_no_numeric_bound`; no zero, numerical limit, or missing-rate imputation is allowed. Other absent entries are `not_reported`.
4. Keep Site A's transformation endpoint explicit. Compute only same-row log differences, with conditional base-10 point ratios `10 ** (log_k_numerator - log_k_denominator)`: F/A for the three reported A rows; D/E for rows S3-05 and S3-06. These are descriptive contrasts, not parameter estimates for the target.
5. Preserve source uncertainties: temperature +/-0.2 C, concentration +/-1%, and log-rate regression error or repeated-trial standard deviation, whichever is larger. The source supplies no confidence level or joint covariance; calculate no ratio confidence interval.
6. Test altered SI/CSV input, invalid units/nonfinite values, missing rows, censored values, endpoints, and inference limits. Record complete command output and a source-to-CSV comparison in `.omo/evidence/oxide-isotope-constraints/`.

Run from the workspace root:

```sh
python3 recursive-compound-2026-10-15/renewal/oxide-isotope-constraints/test_analysis.py
python3 recursive-compound-2026-10-15/renewal/oxide-isotope-constraints/analysis.py
```

Acceptance means source fidelity and reproducible arithmetic. It does not mean oxygen labels identify retained molecular organization, new competent activity, target renewal, or life. No target rates, candidate increment, compatible complement, SCF, or physical observation are added.
