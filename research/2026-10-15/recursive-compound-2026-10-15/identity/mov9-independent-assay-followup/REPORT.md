# Moreira 2026: bounded MoV9 assay follow-up

The official supplement could not be acquired. This pass adds **zero quantitative speciation, calibration, active-retention or independent-validation rows**. The available [primary article page](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/cmdc.70354) supports an assay lead; it does not supply the methods or spectra needed to reassess the earlier Kostenkova measurements.

The page identifies [MoV9O28]5− and labels the substituent Mo(VI). It reports culture-medium 51V NMR, lists the supplement `cmdc70354-sup-0001-SuppData-S1.pdf` (1.1 MB), and places supporting data in that file. The abstract's 8.1 µM EC50 for V9Mo and V9Pt concerns trypomastigote biological response. It provides no chemical abundance or active-catalyst-retention measurement. See receipt R2, source lines236–256.

Research-family independence cannot be claimed: Debbie C. Crans coauthors both Moreira2026 and Kostenkova2023, and Moreira cites Kostenkova2021/2023 (R2 lines65–71 and308–311; existing Kostenkova HTML author metadata). Shared authorship and citations establish overlap; they do not establish reused experiments. Independent collection and the provenance of spectra or modeled curves remain unresolved.

## Retrieval outcome

| Route | Observed result |
| --- | --- |
| R1, stale numbered link | Unintended Wiley sharing-help navigation; counted conservatively against the cap. This says nothing about SI access. |
| R2, fresh official article page | Abstract, author metadata, references and SI link retrieved. |
| R3, official supplement link | Explicit HTTP403; no PDF bytes or methods retrieved. |
| R4, official full-text link | Redirected from `/doi/full/` to `/doi/abs/`; no response status or access-block cause supplied. |

Four targeted queries found publisher metadata and discovery records. One author-profile result claimed full-text availability; its article file and version remain unverified because the four-route budget was exhausted. No equivalent failed route was retried. All tool responses and queries are preserved in `acquisition.json` and `raw/`. These are tool-rendered receipts, **not downloaded publisher HTML or the SI PDF**; the PDF hash remains null.

## Effect on the chemical hypothesis

No actual method, spectral figure or table was accessible in this pass. Chemical shifts, total concentrations, pH, temperature, ionic strength, medium recipe, counterions, integration denominator, overlap correction, uncertainty, detection limits and time points remain null in `evidence.json`.

MoV9 has Mo:V = 1:9, while the proposed Mo34WV target has Mo:V = 34:1 and a different framework. This page cannot establish competition under ordinary low-pH Mo36 conditions or identify the target. Biological EC50 and whole-cell uptake statements cannot supply species-resolved inorganic catalytic retention. This negative access result also does not establish that the unavailable source measurements are unusable.

The next decision-changing evidence is legitimate access to the exact supplement/full article, followed by inspection of actual NMR methods and spectral assignments. Any reported fractions require a defined observable denominator, response and overlap treatment, uncertainty and detection limit. Any simulated distributions require their original formation reactions and conditions. Compare the underlying measurements with Kostenkova2021/2023 before treating them as independent validation.

No fit, simulation, candidate admission, target revision or publication change was performed. Prior artifacts remain frozen. Local receipt hashes and checks are in `validation.json`; an independent read-only source-scope check is recorded separately when returned.
