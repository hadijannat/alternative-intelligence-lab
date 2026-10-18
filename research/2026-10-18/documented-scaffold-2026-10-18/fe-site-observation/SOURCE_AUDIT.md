# Primary source acquisition and observation audit

Source: Haitao Qian et al., *In Situ Quantification of the Active Sites, Turnover Frequency, and Stability of Ni–Fe (Oxy)hydroxides for the Oxygen Evolution Reaction*, ACS Catalysis 12 (2022), 14280–14289. Main DOI [10.1021/acscatal.2c03898](https://doi.org/10.1021/acscatal.2c03898); publisher-deposited SI DOI [10.1021/acscatal.2c03898.s001](https://doi.org/10.1021/acscatal.2c03898.s001).

## Acquisition evidence

Executed from repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/fe-site-observation/sources/acquire.py
```

The binary observable is `byte_verification: PASS`, with assertions requiring the deposited file count, PDF HTTP 200, byte count, and MD5 equality. Captured output is summarized by `sources/receipt.json`; the source bytes, metadata, full extraction, and rendered pages are preserved alongside it. The PDF has 11 pages. The acquisition script is an auxiliary source-receipt tool, not a scientific model or a held-out validation test.

| Route | Observed result | Artifact |
|---|---|---|
| `https://api.figshare.com/v2/articles/21509957` | HTTP 200, 8,782 bytes; exactly one deposited file | `sources/figshare.json` |
| `https://ndownloader.figshare.com/files/38122559` | HTTP 200, 644,572 bytes; matching deposited MD5 `873f9d0e1b058f7be27f508f518657c5` | `sources/cs2c03898_si_001.pdf` |
| `https://pubs.acs.org/doi/10.1021/acscatal.2c03898` | Direct HTTP 403, 5,454-byte error page; not article full text | `sources/acs-landing.html` |
| `https://www.sigs.tsinghua.edu.cn/gl_en/list.htm` | HTTP 200, 82,442 bytes; author institutional bibliography lists exact title, journal, year, pages, and authors; no article attachment identified for this entry | `sources/author-institution.html` |

All SHA256 and MD5 hashes, resolved URLs, content types, and acquisition timestamp are in the receipt. A web search rendered the official ACS abstract and Supporting Information description, explicitly marking the body as available to purchase. Searches for the exact DOI/title and institutional/repository routes did not identify a public author manuscript. This is a limited access result, not proof that no manuscript exists. No author contact or purchase occurred.

The complete Figshare file list is one file: `38122559`, `cs2c03898_si_001.pdf`, `application/pdf`, 644,572 bytes. The deposit identifies CC BY-NC 4.0 for this SI. That record does not confer the same rights on the unavailable main article. No native CSV, spreadsheet, electrochemical trace, replicate table, or analysis code is included in this deposit. The full text extraction is `sources/supporting-information.txt`. Rendered pages 6, 7, 9, and 10 were visually inspected and contain Figures S4, S5, S8, and S9 respectively (page 6 also S3; page 9 also S7).

## Acquisition agent exposure and numeric boundary

The acquisition agent viewed native figures to identify the series, axes, and assay limitations, so this agent is response-exposed. It has not digitized endpoints or fitted models. Initial messages to the root agent contained only independent-variable labels, units, conditions, and qualitative limitations. This audit likewise omits numerical response endpoints. The study's abstract and qualitative findings were known before the current test. Any subsequent reserve is a retrospective figure-derived condition reserve, not a new experiment or a prospectively unseen study.

## Observable map for a frozen test

| Panel | Independent variable and series | Response units | Conditions / limits |
|---|---|---|---|
| S8a | E versus RHE; cycles `1st`, `2th` [source spelling], `3rd`, `4th`, `5th`, `6th`, `7th` | Current density mA cm⁻² | OER curves during continuous cycling; panel shown over 1.2–1.6 V |
| S8b | E versus RHE; same color progression, no second legend | Current density mA cm⁻² | Ni redox enlargement; displayed 1.2–1.6 V |
| S8c | E versus RHE; same color progression, no second legend | Current density mA cm⁻² | Fe redox enlargement; displayed −0.4–1.0 V |
| S8d | Cycle numbers 1–7 | Fe site-density proxy, ×10⁻⁹ mol cm⁻²; apparent TOF, s⁻¹ | Fe reduction charge for density; current at 1.52 V versus RHE for TOF |
| S9a,b | E versus RHE, multiple unlabeled colored cycle traces | Current mA, **not** mA cm⁻² | Fe/Ni versus Ni₃Fe; exact cycle indices and scan rate absent from caption |
| S4a–d | E versus RHE; Ni₃Fe, Ni₂Fe, NiFe, NiFe₂ | Current mA | Shaded Fe oxidation A1 and reduction A2; separate Ni reduction B |
| S5 | E versus RHE; four mixed compositions plus pure Ni | Current mA | N₂-saturated 1 M KOH, −0.4–1.0 V, 10 mV s⁻¹ |

S8 uses Ni (oxy)hydroxide initially and **1 M KOH containing 2 µM Fe³⁺**, continuously cycling **−0.4 to 1.6 V**. The caption groups a–d as one adsorption experiment. It provides no replicate identities, uncertainty description, raw records, or gas production series. The S8 caption and general electrochemical methods do **not** specify its scan rate. S5 explicitly uses 10 mV s⁻¹, and S6 examines a range from 100 to 10 mV s⁻¹; neither licenses an unqualified transfer of a specific scan rate to S8.

The exact numerical Fe integration limits are not stated in the acquired methods or captions. S4 depicts the integration regions graphically. A redox integration reconstructed from the image would need declared background and window assumptions, as well as scan rate, and cannot be represented as an independently recovered native charge record. S8d can instead be used as the authors' reported redox-derived proxy, carrying these unresolved assumptions.

## Measurement equations and assumptions

SI page 4 defines the site number as `n = Q/e = (integral i dt − Qdl)/e`, using one electron per Fe²⁺/Fe³⁺ redox event. Here `n` is an atomic count, while the S8d axis reports amount per geometric area. The appropriate conversion is `Gamma_Fe = Q/(F A)` in mol cm⁻². `Qdl` can be estimated from pure Ni or a linear background. The methods point to **Figure S6** for the pure-Ni background, whereas **S5** actually depicts it; S6 is the scan-rate experiment. This is a verified figure-reference error, not evidence of an incorrect reference-electrode voltage.

The apparent TOF equation is `NA I/(4 n F)`, numerically equivalent to `I/(4Q)` when `F = NA e`. With density variables it is `j/(4 F Gamma_Fe)`. The authors give 290 or 300 mV overpotential generally; S8 specifies 1.52 V versus RHE. A redox-derived site proxy and a TOF computed using the same proxy are mathematically coupled. Their reciprocal relationship is not two independent measurements of mechanism. Testing plotted current against the reported site proxy avoids treating the derived TOF as an independent response, although the site proxy itself remains model-dependent.

The equation assumes the current attributed to oxygen evolution corresponds to four electrons per O₂. No independent Faradaic-efficiency or isotope-resolved product assay is supplied in this SI. One must distinguish the authors' apparent turnover metric from independently measured product turnover. Pure-Ni subtraction assumes the double-layer response of the control represents that of each mixed/evolving catalyst; the document does not establish invariant capacitance or subtraction uncertainty. Fe redox accessibility also need not equal the number of catalytically competent Fe sites at the OER potential. Ni reduction at a separate potential and changing material state during the wide diagnostic sweep limit a simple unchanged-site interpretation.

## Materials, normalization, and origin

The standard working electrode uses a **5 mm diameter glassy-carbon disk** (geometric area `pi*(0.25 cm)^2`) and a reported **0.08 mg cm⁻² catalyst loading**. The preparation disperses 2 mg catalyst powder in water/isopropanol with Nafion binder, then deposits 10 µL of ink. The separate XPS preparation uses 0.48 mg cm⁻²; that loading must not be substituted into the electrochemical series. S8 explicitly reports geometric current density, while S4/S5/S9 use total mA. Matching their plotted numbers without converting the axes would be wrong.

Ni–Fe (oxy)hydroxides are synthesized on **Vulcan XC-72 carbon black**, with carbon-supported pure-Ni material prepared by the same route without Fe precursor. The electrode also contains Nafion and uses glassy carbon. These are material components in the tested electrode, not merely manufacturing solvents. The study supports an observation-model comparator; it does not establish an admissible wholly inorganic integrated complement or the same behavior without these components.

The mixed materials span precursor Ni:Fe ratios 3:1, 2:1, 1:1 and 1:2; ICP-OES is provided as a composition check. Purified KOH is prepared by Ni(OH)₂ scavenging, but the acquired SI provides no quantitative residual-Fe concentration or time-resolved metal balance for the S8 series. S8 supplies soluble Fe externally to a retained Ni-based host. It lacks an origin label, founder depletion/removal arm, independently measured founder-specific activity ceiling, or an isolated new-material product assay. The increase of a redox-visible population cannot by itself assign catalytic current to newly supplied Fe rather than retained host activity or a changed environment. No serial inheritance is tested.

## Retained limitations and next decision

The source adds a meaningful second electrochemical observable, Fe-associated redox charge, beyond voltage/current alone. It can test whether a constant activity per counted Fe site describes the figure-derived series and whether an occupancy-dependent alternative forecasts reserved cycles. It cannot alone identify atom-origin functional contributions, prove active repair beyond retained founders, or supply a universal founder-activity upper bound for Han, Poli, PMo₁₂, or the hypothetical Mo₃₄WV cluster. Main-body access, native traces, exact integration/background protocol, S8 scan rate, matched Fe-withdrawal controls, and source-specific functional attribution remain unresolved.
