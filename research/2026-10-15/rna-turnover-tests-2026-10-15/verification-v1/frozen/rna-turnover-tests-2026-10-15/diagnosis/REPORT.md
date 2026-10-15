# Remaining RNA failures after independent efficiencies and functional loss

The selected `independent_inactivation` family substantially improves the earlier reduced model but leaves **structured, opposing errors**. It overshoots the held-out highest Hyper-A curve at later times, yet an early-time fit undershoots that same curve. Functional loss improves F1 dose prediction while worsening Hyper-A dose prediction relative to the independent-efficiency model. A common reduction of reaction speed cannot resolve all these patterns.

This audit makes no new fits and selects no new candidate. Every source observation was already inspected. The outputs are retrospective diagnostics, not independent experimental validation or evidence of a unique chemical mechanism.

## Source and numerical checks

[audit.py](audit.py) independently checks **228 workbook values**: all 148 supplied means/replicate observations plus 40 S13 SDs and 40 sample sizes. It checks all 2,512 saved bulk/transport residual rows against source values and arithmetic. A separately written six-state DOP853 implementation replays 288 full-fit, whole-dose, and late-time predictions for the revised, independent, and combined families. The maximum difference from saved LSODA predictions is **0.0000711 pp**, at a revised-model Hyper-A holdout, far below the observed errors. The largest replayed full-state discrepancy is 2.58×10⁻⁸ µM. All three RNA moiety balances pass independent assertions.

The retained transport implementation reproduces all 216 transport predictions exactly at saved parameters; transport scores are independently aggregated. This is a saved-model transport replay, not an independently implemented transport simulator. Five source/code/protocol files also match the earlier pre-fit snapshot; all 261 audited input file hashes remain unchanged. [verification.json](verification.json) records checks and hashes. No previous lab was edited.

## Dose and time structure

Scores exclude deterministic t=0 values. Error means prediction minus observation; units are percentage points.

| Prediction task | Revised comparator RMSE | Independent efficiencies RMSE | Combined selected model RMSE |
|---|---:|---:|---:|
| All eight held doses | 10.631 | 3.551 | 3.145 |
| F1 held doses | 7.228 | 4.297 | 2.707 |
| Hyper-A held doses | 13.183 | 2.599 | 3.529 |
| Endpoint dose extrapolation | 10.791 | 3.544 | 3.444 |
| Interior dose interpolation | 10.468 | 3.559 | 2.815 |
| Early-fit, late-time prediction | 24.183 | 4.954 | 4.148 |

Endpoints are each branch's lowest and highest dose; each aggregation has 16 positive-time predictions. The selected model's held-dose RMSE rises across 15/30/45/60 minutes: **1.954, 2.519, 3.259, 4.333 pp**. The 2.5 µM Hyper-A holdout alone contributes **44.6%** of pooled held-dose squared error. The maximum error is 8.639 pp; the registered 2 pp RMSE / 4 pp maximum screen remains failed.

| Held-out curve | Error at 15 min | 30 min | 45 min | 60 min |
|---|---:|---:|---:|---:|
| F1 0.1 µM | +0.627 | −0.658 | −2.440 | −1.863 |
| F1 0.25 µM | +4.326 | +2.444 | +0.465 | +3.660 |
| F1 0.5 µM | −0.522 | −6.090 | +0.349 | +0.161 |
| F1 1 µM | −3.146 | −0.215 | +2.856 | +3.610 |
| Hyper-A 1 µM | +0.368 | −0.753 | −1.262 | −2.233 |
| Hyper-A 1.5 µM | +0.984 | +1.501 | +1.983 | −2.293 |
| Hyper-A 2 µM | +0.379 | −0.295 | −1.712 | −5.947 |
| Hyper-A 2.5 µM | −0.173 | +2.078 | +7.879 | +8.639 |

The high-Hyper-A failure is not uniform overprediction: omitting 2 µM undershoots its endpoint while omitting 2.5 µM overshoots its endpoint. Moreover, the independent model without loss has **better Hyper-A held-dose RMSE** despite its poorer overall score. This tradeoff cautions against treating the selected loss term as a measured biochemical property.

The separate early-only fits see 15/30-minute values. Their combined-model late predictions have opposite branch biases: F1 **+3.663 pp**, Hyper-A **−2.747 pp**. The endpoint residuals are:

| Curve | Early-fit error at 45 min | At 60 min |
|---|---:|---:|
| F1 0.1 µM | −0.166 | +2.305 |
| F1 0.25 µM | +2.365 | +7.358 |
| F1 0.5 µM | +4.462 | +4.422 |
| F1 1 µM | +4.169 | +4.393 |
| Hyper-A 1 µM | −0.841 | −1.745 |
| Hyper-A 1.5 µM | +1.337 | −3.377 |
| Hyper-A 2 µM | −2.358 | −8.220 |
| Hyper-A 2.5 µM | −0.138 | −6.631 |

All predictions for the three audited families, including full fits and baseline errors at every dose/time, are in [residuals.csv](residuals.csv). No endpoint or intermediate anomaly is removed.

## Parameters and unobserved active inventories

The high-dose omission raises `ka` from 0.01572 to 0.02646 µM⁻¹ min⁻¹, decreases `kh` from 0.000684 to 0.000478, and increases `krh` from 0.000708 to 0.000939. The remaining doses therefore permit stronger F1-driven amplification that overshoots the unseen high dose. Across the eight single-dose omissions, `ka` ranges 0.01357–0.02646, `KB` 0.696–2.077 µM, and the effective loss half-life 47.1–62.7 minutes.

The early-only fit is more different: **`ka=0.0001` and `KB=0.01` reach their lower bounds**. Its `kd` is 0.00656 min⁻¹ versus 0.01295 in the full fit, extending the modeled half-life from 53.5 to 105.6 minutes. Early reporter observations alone therefore support a very different mixture of initiation, amplification, saturation and loss. These are effective fitted parameters, not direct rate or lifetime measurements. [parameter_changes.csv](parameter_changes.csv) preserves all full, omission and early-fit values.

At Hyper-A=2.5 µM, 60 minutes, the combined full fit predicts 3.016 µM reporter product and 0.266 µM active F1. The high-dose-omission fit predicts 3.418 and 0.399 µM; the early-only fit predicts 2.655 and 0.194 µM. Even among full fits, the independent model predicts almost the same reporter product (3.012 µM) with 0.367 µM active F1. The older revised model predicts 1.983 µM active F1 and a poor reporter trajectory. Active inventories are therefore model-dependent latent predictions. See [endpoint_inventories.csv](endpoint_inventories.csv) and the independently generated [replayed_inventories.csv](replayed_inventories.csv).

## Structural reasons to test occupied-catalyst chemistry

The present combined model uses `vr=kf F R B/(KB+B)+krh A R [B/(KB+B)]²`. A ligation event never occupies F for a finite interval. Newly formed active F becomes immediately available; inactive reporter product has no further interaction. There is no catalytic bound-substrate inventory, product-bound catalyst, release step, or feedback of accumulated reporter product on available F. Functional loss supplies only one shared irreversible clock. These are identifiable modeling omissions, not proof that any specific omitted process causes the observed discrepancies.

For F1-only reactions the combined model retains a strong restriction. With `P` in µM and the shared initial free concentrations R=5, B=7.5,

```text
F(t) = F0 exp(−kd t)
Q(P) = log[5/(5−P)]
       + (KB/2.5) {log[5/(5−P)] − log[7.5/(7.5−P)]}
Q(P)/F0 = kf [1−exp(−kd t)]/kd.
```

Thus all F1 doses still share one transformed time course. A substrate/product-only factor multiplying the same free-F law preserves this type of transformed-exposure restriction; with `kd=0` it preserves ordinary `F0*t` collapse. An explicit occupied-F state can break the restriction by placing some F outside the immediately available pool and adding a release clock. A finite-occupancy reduction can also do so if it accounts for conserved bound catalytic material; the physical approximation must be stated.

The retained [primary-source review](../../rna-reaction-tests-2026-10-15/research/REPORT.md) motivates distinguishing ligation, product release and substrate sequestration in these related RNA ligases. It does not establish Salibi-specific microscopic rates or identify a particular bound state. A new finite-turnover hypothesis should conserve F-containing complexes, separate ligation from release, and count ligated Cy5 material while bound in the denaturing-PAGE observer. Zero product release must not erase already ligated reporter product. Binding of an inactive product must never grant that product catalytic competence. Free initial states and any pre-equilibrated alternatives remain preparation assumptions.

The 60-minute measurements do not establish infinite-time plateaus. Reported SDs and n=3 are available for S13, but raw replicate time trajectories/covariance and systematic assay errors are not. A better reporter fit can still conceal incorrect active chemistry; no kinetic omission should be declared uniquely identified from these residuals.

## Transport failure is concentrated at the larger founder dose

Both closures hold chemistry fixed, fit mixing using Figure 2 seeds 0/1, and assume 0.55 retention across three freeze/thaw cycles for all material classes. Seed 2 is concentration extrapolation. The benchmark includes all positive Figure 3 generations.

| Benchmark subset | Fractional RMSE, pp | Contact RMSE, pp |
|---|---:|---:|
| Figure 2 seed 2 | 5.922 | 6.524 |
| Figure 3 seed 0 | 2.151 | 1.347 |
| Figure 3 seed 1 | 1.499 | 2.128 |
| Figure 3 seed 2 | 6.848 | 7.763 |
| All 72 observations | 4.479 | 4.975 |

Seed-2 subsets contribute **90.0%/92.5%** of fractional/contact benchmark squared error. At Figure 3 generation 5, seed 2 is underpredicted by **9.207/10.147 pp** in group mean. Fractional transport overpredicts seed-0 group means throughout Figure 3 while underpredicting seed 2. Raising a shared global rate or retention may therefore improve one branch while damaging another.

The closure also forces Figure 2 at three cycles and Figure 3 generation 1 to have identical predictions. Their observed means differ: seed 2 is **12.943 versus 10.115%**; seed 0 is 0.823 versus 1.873%, and seed 1 is 6.554 versus 5.234%. These are observed between-assay differences, not proof of a particular batch effect or a newly fitted correction. All replicate-level errors and group means remain in [transport_group_residuals.csv](transport_group_residuals.csv).

Bulk chemistry, transport closure, species-specific retention and compartment conditions remain confounded. Neither equal retention of active catalyst and fragments nor equal retention of any proposed complex is measured here. Chemistry improvements should be frozen before the transport challenge; historical benchmark failures must remain visible.

## Optimization scope and reproduction

The earlier campaign contains 248 resolved fits and 1,488 starts; 22 starts reached their evaluation cap, and six fits lack two-start agreement. Those six are three trapping-free dose subsets, both trapping early-only fits, and the fixed high-`kd` profile. **The selected full fit, all eight single-dose fits and its early-only fit each have six successful, agreeing starts.** Their residual failures cannot be attributed to the campaign's known capped starts. Agreement among starts does not certify a global optimum. Full optimization records are summarized without selective retries in [summary.json](summary.json).

Run from the workspace root:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 --with matplotlib==3.10.8 --with openpyxl==3.1.3 python rna-turnover-tests-2026-10-15/diagnosis/audit.py
```

Development note: the initial workbook audit also encountered the earlier export's separate S13 zero-control row (`C6`), absent from the selected 148-row dataset. Its assertion lookup stopped before any output or fitting. The audit was corrected to check the exact S13_F1/S13_HyperA datasets and all 148 selected source observations; the corrected checks pass. No scientific model, observation, fit, or previous result was changed.

Skipped: new fitting, new data acquisition, and independent transport reimplementation. The remaining risk is mechanistic non-identifiability from reporter-only, previously inspected data.
