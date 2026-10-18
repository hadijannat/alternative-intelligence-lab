# Figure S8 extraction

The public SI is a plotted-data source, not raw electrochemical data. Page 9 contains zero native vector drawings. Its Figure S8 is the embedded JPEG at xref 65, 540 by 412 pixels. The script validates the original PDF SHA256 before extracting that image. `data/figS8_native.png` is a lossless PNG of those decoded JPEG pixels; it adds no information. `data/figS8_calibration.png` uses nearest-neighbor enlargement solely to show the selected intervals and marker boxes.

Run from repository root:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 documented-scaffold-2026-10-18/fe-site-observation/extract_figS8.py
```

Observable success is a zero exit and `source_verified: true` with five self-checks `PASS`. The durable output is `data/figS8_points.json`, plus `data/point_provenance.csv` and the two PNGs. The calibration tests verify increasing and reversed axes, interval direction, rejected extrapolation and a known synthetic raster line sampled at its declared coordinate. These check the numerical mapping; they do not validate unknown experimental uncertainty.

## Current and site-density measurements

Panel a x calibration: pixel 50.5 = 1.2 V versus RHE; pixel 247.5 = 1.6 V. Thus 1.52 V maps to pixel 208.1. The selected horizontal band is pixels 207–210 to include stroke, axis-position, and interpolation uncertainty. Current-axis anchors are y=152 for zero and y=14 for 50 mA cm⁻². Steep current curves amplify horizontal-pixel uncertainty substantially.

Each current interval is manually selected from color-compatible visible strokes across that band. The legend explicitly labels cycles 1–7. Neighboring shades and merged branches prevent unique assignments for the olive 1/2, yellow/beige 3/4, and red 6/7 pairs. Each of these pairs therefore shares its full interval; no activity ordering or fitted result is used to split it. Orange cycle 5 has its own broad color-compatible interval. Sweep direction is not documented, so no forward/reverse branch is selected. Nominal values are interval midpoints, not resolved raw observations. Pair sharing and baseline reuse create correlated uncertainty. The box is a conservative manual digitization envelope, not a formally exhaustive image-likelihood set or an experimental confidence interval.

Panel d uses only the green Fe-density symbols and its **left** axis: y=381 is zero; y=223 is 10 nmol cm⁻². All seven selected marker boxes are overlaid in the calibration image. Cycle 1 has overlapping green marks/strokes against an orange bar, so its interval spans their full visible extent. Marker resolution and reading uncertainty are preserved. The orange TOF bars are excluded: no current is reconstructed from density times TOF, and no TOF value is used as a model response.

The code contains the exact manual pixel selections, sampled legend colors, x-band, calibrations and density-marker centers. `point_provenance.csv` repeats them for independent inspection. Source units already normalize both current and the density proxy by electrode geometric area; no additional area conversion is applied to these two panels.

## Verification and limits

The extractor visually checked the native source and enlarged annotation. Candidate strokes and markers are enclosed in the final displayed envelopes. An initial calibration-envelope failure was found during that inspection and corrected before model fitting; the original intervals and failed floating-point self-check are retained in `extraction_failures.txt`. This is a reproducible manual interpretation of a low-resolution published figure. A second reviewer can audit or reject the selections using the retained native pixels; the script cannot recover source information absent from the JPEG.

There are seven cycle rows but only four distinguishable current color groups. Six nominal current entries belong to ambiguous pairs. Consequently a numerical fit to the midpoint table can be computed but cannot establish seven independently resolved current observations. A successful midpoint screen must be qualified by interval sensitivity and image limitations. Fe density is the authors' redox-derived proxy; the extraction does not independently recover the underlying integrated charge, background correction, scan rate, or Faradaic efficiency. It provides no founder/new-material functional attribution.
