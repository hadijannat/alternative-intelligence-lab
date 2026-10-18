# STW: functional chirality is documented; cue-free functional inheritance is unresolved

Scope: three primary papers, checked 2026-10-18. Completion means locating growth cues, seed amount, transfer count, founder exclusion and descendant-function evidence. It does not mean that STW meets an inheritance criterion. No simulation or fit was performed. Prior Beta and GTM-3 conclusions are unchanged.

## Primary evidence

| Paper | Seed and growth cue | Function and lineage | Decision |
|---|---|---|---|
| Brand et al. 2017, [10.1073/pnas.1704638114](https://doi.org/10.1073/pnas.1704638114) | Racemic, as-synthesized pure-silica STW seeds about 1 micrometre; 10 wt% relative to SiO2 feed. Growth at 433 K uses independently supplied R, S or racemic organic OSDA2. | Organic removal precedes bulk catalytic testing. Epoxyoctane product b ee is +9.85% for R-STW, -10.65% for S-STW, -0.86% for racemic STW. 2-butanol adsorption also discriminates. No successive functional transfer series. | Demonstrates inorganic functional state after organic removal. Handedness follows the organic growth cue; no comparison of opposite seeds under one achiral/shared cue. |
| Kang et al. 2021, [10.1021/acs.chemmater.0c04573](https://doi.org/10.1021/acs.chemmater.0c04573) | Acquired SI p28 specifies chiral (R,R)-DQ at 0.5 per SiO2, GeO2 0.5, HF 0.5, water 4, growth 160 C. This R-STW recipe does not specify seed addition. Separate pure-silica synthesis table S4 contains a seeded achiral-OSDA condition. | The acquired SI concerns synthesis and structural characterization. It does not establish an opposite-seed, common-cue descendant catalytic assay or serial functional transfers. Main-paper download unavailable; abstract available from Caltech. | Structural follow-up, not evidence of cue-free inheritance. Do not splice the separate achiral seeded synthesis into the chiral functional lineage. |
| Sala et al. 2024, [10.1038/s41467-024-49659-2](https://doi.org/10.1038/s41467-024-49659-2) | Sugar-derived chiral OSDA3; 30 crystals from three synthesis batches share handedness. Seed additions failed to appreciably shrink pure-phase crystals. Pure-silica attempts also failed with Ge-STW seeds. | Al-S-STW batch 2-STW-25 has 6% butane-epoxide conversion and 2% hexane-epoxide conversion after 48 h; maximum tabulated ee 4%. No documented serial functional inheritance. | High structural purity does not remove transport limitations. Functions remain weak; no evidence the tested batch descended through an achiral growth stage. |

Exact locations: `sources/stw/brand2017_si.pdf` pp8-9; `brand2017.pdf` pp4-6, Tables2-3; `kang2021_si.pdf` p28 and TableS4; `sugar2024.html` Results/Methods and `sugar2024_si.pdf` pp13,17-19,24. Source URLs, sizes and SHA256 values are in `sources/stw/receipt.json`.

## Founder bound and organic dependencies

The 2017 10% is a feed-relative seed mass, not a measured final founder fraction. It cannot be used as 10% founder contribution to catalytic activity: isolated inorganic yield, seed dissolution, differential activity and seed/product separation are not established for this purpose. Original seeds were as-synthesized, and authors acknowledge a wrong-handed crystal could be a surviving seed. Function measurements apply to resulting bulk batches, not independently identified newly grown material.

For 2021/2024, no qualified seed-to-final founder bound or count of successive *cue-free functional* transfers was found in acquired methods. This is missing evidence, not an estimate of zero physical growth. All three chiral production routes retain an external organic stereochemical cue during synthesis. Removing that cue before an assay establishes durable inorganic function; it does not establish copying after cue removal. No same-system PMo12/Mo34WV coupling is tested here.

## Negative results and numerical conflicts

2024 SI Table9 gives butane-epoxide A/B selectivity 67/33, ee 0/2.5%, and hexane-epoxide A/B 49/51, ee 4/3.6%. Nearby prose instead says a roughly 1:2 hexane-product ratio and butane ee 1.5-2.5%. Both versions are retained. Use the table only as explicitly table-derived data; precise kinetic fitting is unjustified. FAU gives 94% conversion with zero ee. SI Fig12 is non-equilibrated: sugar-STW butanol uptake stays below 1 wt%, versus approximately 15 wt% for a smaller racemic pure-silica comparator; composition and particle size differ. These are not matched equilibrium selectivity measurements.

There is also a nomenclature hazard: the 2017 paper maps R-STW to P6_1 22, whereas the 2024 paper calls P6_1 22 S-STW. Compare absolute space group and source conventions; do not pool R/S labels as identical states.

## Check and next decision

All source claims above were checked against saved PDFs/HTML. Visual checks of Tables2-3, Table9 and the R-STW recipe are saved as PNGs. No additional candidate is admitted as a verified inheritance complement. A decisive future experiment would compare opposite inorganic seed states under the same achiral feed, identify newly formed material, bound original seed activity after dilution, and measure the descendant's function through repeated transfers. Current data cannot calibrate that transfer model.

Acquisition invocation: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/cue-free-inheritance/sources/stw/acquire.py`. Successful files are checked for PDF headers, parseability, nonempty extracted text and SHA256 consistency. Failures are preserved in `sources/stw/access_limits.md` and `receipt.json`. The full Kang paper remains unacquired after two OSTI host routes timed out; its SI is acquired. No author contact, experiments or broad review occurred.
