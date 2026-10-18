# Independent PPKTP source and optical-model review

2026-10-18. Scope: `documented-scaffold-2026-10-18/state-template-growth/`; primary PDFs and receipts, source audit, frozen protocol, `check_optics.py`, `results/optics.json`, `results/optics.png`, final `REPORT.md` and candidate ledger. Native sources and saved outputs were not overwritten.

**Source and numerical decision: PASS, bounded component assessment.** No blocking source-geometry or numerical error was identified. The work supports source-reported patterned growth and spatially addressed nonlinear optical function in the new layer. It does not provide an independently measured founder-function bound, isolated serial descendants, or two serially inherited functional patterns. It contains no fitted model or held-out validation.

**Final interpretation decision: APPROVE the PPKTP component report.** The report preserves its positive new-layer optical assay, the 28% lower peak, 1.351-fold bandwidth product, clean 225 micrometre region versus thicker defective growth, conditional Gaussian assumptions and global-sign-only ambiguity. It explicitly leaves founder cross-talk, H/V/J and integrated life unverified. The candidate JSON parses with false heredity verification, null measured leakage bound and zero verified integrated complements. The closing scout remarks about NaClO3, tellurium and the separate Fe-redox lead were not independently reviewed here and receive no new source or scientific validation from this decision.

## Source evidence checked directly

- Both primary PDFs were opened independently with PyMuPDF. OME has eight PDF pages and DOI `10.1364/OME.1.000185` on its cover; JCG has five pages and DOI `10.1016/j.jcrysgro.2011.11.081`. Both PDF hashes and both HAL-metadata hashes/sizes agree with their acquisition receipts. This verifies the acquired bytes and source identity; the review did not independently replay earlier HTTP requests.
- Inspected rendered OME PDF pages 7 and 8, including Figure 5. The text states a **70 micrometre 1/e² diameter**, so the Gaussian radius is 35 micrometres. Figure 5/caption places the layer probe 225 micrometres beyond the interface and the seed probe 275 micrometres inside the seed. The dimension along propagation is 6.50 mm. Growth is on c faces and propagation is along a, parallel to the seed/layer interface. The layer assay is not a beam deliberately propagated through the seed and then the layer.
- OME p7 reports the domain period 38.86 micrometres, source-prepared electrical poling, inorganic KTP/KPO3/KF flux, 1005.5 K initial growth temperature and 0.05 K/h cooling. Clean propagation to 225 micrometres is distinguished from thicker growth with cracks/inclusions. Optical peaks and bandwidths in the audit match the paper. JCG's optical discussion refers to the same earlier result, so it is not independent optical replication.
- The papers provide a stronger component observation than mass retention or an etch pattern alone: a new-region SHG spectrum. However, the retained seed, unmeasured stray light/cross-talk, unspecified collection details, no isolated daughter series and no controlled alternate-pattern descendant series prevent the stipulated full heredity claim. Apparatus, externally programmed founders and high-temperature growth remain external resources.

## Optical interpretation

For an ideal transverse Gaussian intensity, integrating over the seed half-plane yields `fI = erfc(sqrt(2)*d/w)/2`. Integrating local squared intensity gives `erfc(2*d/w)/2`; a fully coherent on-axis source-amplitude proxy gives `fI²`. These are different observables. The last requires coherent phase/collection assumptions, while integrated local intensity-squared does not compute the full coherent far field. Neither is a measured stray-light upper bound.

At d=225 micrometres and w=35 micrometres, the saved values are:

| Conditional quantity | Value |
| --- | ---: |
| Pump fraction in seed half-plane | 3.9211059391074245e-38 |
| Integrated local I² fraction | 3.5351673328484648e-74 |
| Coherent on-axis relative source power | 1.5375071785703517e-75 |

The transverse profile is idealized throughout the interaction; actual beam-waist evolution, aberrations, scattering, collection and coherent seed/layer interference were not measured in this analysis. These tiny ideal-tail values must not be promoted to independent experimental founder bounds. The separately calculated `sqrt(0.72)=0.848528...` assumes identical conversion geometry and coupling; it is not a calibrated leakage requirement for arbitrary stray paths.

The 0.2 nm peak-center difference and overlap [2126.6, 2127.4] nm reproduce the stated ±0.5 nm ranges without assigning confidence levels. The bandwidth-product ratio is 12.7/9.4 = 1.35106. At 0.65 cm, the observed-product FWHM is 19.53846 nm, consistent with the rounded source 19.5 nm; ideal-product FWHM is 14.46154 nm. Lower peak output and nonideal bandwidth are preserved.

Global reversal `d33(s) -> -d33(s)` reverses the complex amplitude and leaves intensity invariant. This loses an absolute global sign in this measurement, **not all state information**. Uniform and periodic coefficients have different spectra in the same executed synthetic scan. The 20-period dimensionless scan is explicitly synthetic; it is not the physical 38.86 micrometre grating's measured wavelength spectrum, a measured copy fidelity or a prediction of descendant rates.

## Executed independent checks and artifacts

Qualified binary: `/USER_HOME/.pyenv/versions/3.12.3/bin/python3`; working directory: repository root. Invoked Python with `-c` and the program below. No `main()` call or result rewrite was performed.

```python
import sys, pathlib, json, math, hashlib, numpy as np, fitz
p = pathlib.Path('documented-scaffold-2026-10-18/state-template-growth')
sys.path.insert(0, str(p))
import check_optics as c
a = json.loads((p / 'results/optics.json').read_text())
c.self_check()
for name, digest in a['hashes'].items():
    assert hashlib.sha256((p / name).read_bytes()).hexdigest() == digest
for f, doi, pages in [('ome2011.pdf', '10.1364/OME.1.000185', 8),
                       ('jcg2012.pdf', '10.1016/j.jcrysgro.2011.11.081', 5)]:
    doc = fitz.open(p / 'sources' / f)
    assert len(doc) == pages and doi in doc[0].get_text()
q = np.array(a['synthetic_phase_matching']['scan_q'])
centers = np.arange(.25, 20, .5)
signs = np.tile([1., -1.], 20)
amps = np.sinc(q*.25/np.pi) * np.mean(signs[None, :] * np.exp(1j*q[:, None]*centers), axis=1)
uniform = np.sinc(q*10/np.pi) * np.exp(1j*q*10)
err = max(float(abs(abs(amps)**2-a['synthetic_phase_matching']['periodic_intensity']).max()),
          float(abs(abs(uniform)**2-a['synthetic_phase_matching']['uniform_intensity']).max()))
assert err < 1e-13
assert np.array_equal(a['synthetic_phase_matching']['periodic_intensity'],
                      a['synthetic_phase_matching']['global_sign_reversed_intensity'])
assert max(abs(abs(amps)**2-abs(uniform)**2)) > .9
u = np.linspace(0, 12, 1000001)
errors = []
for power, key in [(1, 'pump_fraction_in_seed'), (2, 'integrated_I_squared_fraction')]:
    az = math.sqrt(2*power)*225/35
    integral = math.exp(-az*az) * np.trapezoid(np.exp(-2*az*u-u*u), u) / math.sqrt(math.pi)
    rel = abs(integral/a['nominal_geometry'][key]-1)
    assert rel < 2e-8
    errors.append(rel)
assert a['spectral_consistency']['overlap_of_quoted_intervals_nm'] == [2126.6, 2127.4]
assert math.isclose(a['spectral_consistency']['bandwidth_broadening_factor'], 12.7/9.4)
assert math.isclose(a['spectral_consistency']['FWHM_from_reported_product_nm'], 12.7/.65)
assert math.isclose(a['nominal_geometry']['coherent_on_axis_relative_power'],
                    a['nominal_geometry']['pump_fraction_in_seed']**2, rel_tol=1e-14, abs_tol=0)
assert len(a['geometry_sensitivity']) == 21
```

Observed exit 0. The independent sinc/segment-center expression reproduced all 2,001 synthetic scan points with maximum intensity discrepancy **6.661338147750939e-16**. Direct transformed Gaussian-tail quadrature agreed with saved pump/I² fractions to relative discrepancies **3.991058372676548e-09** and **7.958548486897143e-09**. All implementation selfchecks passed. Exact global-sign intensity arrays matched; uniform versus periodic spectra remained distinguishable.

A second read-only `python3 -c` invocation recomputed all 21 fixed sensitivity scenarios, joined all four acquisition receipt records to local payloads and recomputed byte sizes/SHA256. Observable: exit 0, all scenarios and hashes/sizes match. Captured numerical evidence is this review plus `results/optics.json`; source evidence is the native PDFs, receipts and `sources/ome2011-page7.png` / `sources/ome2011-page8.png`.

The three images were opened using `view_image`. Figure 5's geometry/axes were readable. `results/optics.png` displays the ideal Gaussian comparison and exactly overlaid global-sign curves with a distinct uniform-medium curve. The figure is a conditional analytic illustration, not an experimental founder-origin measurement.

## Exact reviewed hashes

| Artifact | SHA256 |
| --- | --- |
| `PROTOCOL.md` | `650ea8f41da7df62c29b1e5a1b41a9a5cd8a1991fb9a5f16db06e5b35b522822` |
| `SOURCE_AUDIT.md` | `4807abf233b94f08ee4f8f108ddcdf4be60d69b6a79c86ada89155e275784ed0` |
| `check_optics.py` | `615fdf9ad362af42a5ff187c9e4502eb601db617cbe7aa58673f9626b5324e2f` |
| `results/optics.json` | `d03f13d0c63ba897422859d71795cd2a9e108257e9cec7c002d1df6077509c9c` |
| `results/optics.png` | `09674588dcdf5cb9df301bbe86c6848187ebd7b127021b8669e102f897d850f8` |
| `sources/ome2011.pdf` | `8edd175ce10cdbe22c2d0387da1fcdc23857d49bf0358367ab92fd26a6ecfc1c` |
| `sources/jcg2012.pdf` | `27ba4dd347b377eaad316f0e8b02bfca4ec7f4423b9587a0a33920ae92d4a256` |
| `REPORT.md` | `42eb705a9d902276268814463d96fd1ff491a0cdc94cc20840c1e8921a117f6e` |
| `candidates.json` | `7c0fa56809dd18b6cc4d95d555e2ea23a4fc0af57dce76c42f1ae17280cc15be` |

No raw experimental dataset, new specimen measurement, measured optical leakage calibration, detached-daughter series or validated chemical coupling was obtained by this review. These limits block full functional-heredity admission while preserving the positive bounded source observation.
