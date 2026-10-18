from pathlib import Path
import hashlib
import json
import math
import csv

import fitz
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources/cs2c03898_si_001.pdf"
EXPECTED = "fa82d1784dbd4257238e31a3a907e1b7fbc07c0849b3be2663b6350c63d857ab"
DATA = ROOT / "data"


def interpolate(pixel, anchors):
    (p0, v0), (p1, v1) = anchors
    if not min(p0, p1) <= pixel <= max(p0, p1) or p0 == p1:
        raise ValueError("Pixel outside the distinct calibration anchors")
    return v0 + (pixel - p0) * (v1 - v0) / (p1 - p0)


def calibrated_interval(bounds, anchors):
    return sorted(interpolate(pixel, anchors) for pixel in bounds)


def self_check():
    assert interpolate(20, [(10, 2), (30, 6)]) == 4
    assert interpolate(20, [(30, 6), (10, 2)]) == 4
    assert interpolate(20, [(10, 6), (30, 2)]) == 4
    assert calibrated_interval([15, 25], [(10, 6), (30, 2)]) == [3, 5]
    try:
        interpolate(31, [(10, 6), (30, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("Out-of-range calibration accepted")
    synthetic = np.full((101, 101), 255, dtype=np.uint8)
    for x in range(101):
        synthetic[100 - x, x] = 0
    rows = np.flatnonzero(synthetic[:, 40] == 0)
    assert rows.tolist() == [60]
    assert math.isclose(interpolate(float(rows[0]), [(0, 10), (100, 0)]), 4)
    assert np.allclose(calibrated_interval([59, 61], [(0, 10), (100, 0)]), [3.9, 4.1], rtol=0, atol=1e-12)


def main():
    self_check()
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
    document = fitz.open(SOURCE)
    assert len(document[8].get_drawings()) == 0
    image_record = next(record for record in document[8].get_images() if record[0] == 65)
    assert image_record[2:4] == (540, 412)
    pixmap = fitz.Pixmap(document, 65)
    native = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    DATA.mkdir(exist_ok=True)
    native.save(DATA / "figS8_native.png")

    x_anchors = [(50.5, 1.2), (247.5, 1.6)]
    j_anchors = [(152.0, 0.0), (14.0, 50.0)]
    n_anchors = [(381.0, 0.0), (223.0, 10.0)]
    x_target = interpolate(1.52, [(v, p) for p, v in x_anchors])
    x_band = [207, 210]
    assert x_band[0] <= x_target <= x_band[1]
    current_bands = {1: [75, 127], 2: [75, 127], 3: [40, 112], 4: [40, 112],
                     5: [25, 86], 6: [14, 74], 7: [14, 74]}
    groups = {1: "olive-1-or-2", 2: "olive-1-or-2", 3: "yellow-3-or-4",
              4: "yellow-3-or-4", 5: "orange-5", 6: "red-6-or-7", 7: "red-6-or-7"}
    density_bounds = {1: [353, 370], 2: [351, 360], 3: [337, 347], 4: [297, 307],
                      5: [273, 283], 6: [254, 264], 7: [245, 255]}
    density_x = {1: 334, 2: 358, 3: 383, 4: 407, 5: 432, 6: 456, 7: 481}
    points = []
    for cycle in range(1, 8):
        j_interval = calibrated_interval(current_bands[cycle], j_anchors)
        n_interval = calibrated_interval(density_bounds[cycle], n_anchors)
        legend_y = 62 + (cycle - 1) * 12
        palette = np.asarray(native)[legend_y, 75:92].mean(axis=0).tolist()
        points.append({"cycle": cycle, "j_mA_cm2": sum(j_interval) / 2,
                       "n_nmol_cm2": sum(n_interval) / 2,
                       "j_interval_mA_cm2": j_interval, "n_interval_nmol_cm2": n_interval,
                       "j_pixel_y_interval": current_bands[cycle],
                       "j_pixel_x_interval": x_band,
                       "j_legend_group": groups[cycle],
                       "n_pixel_y_interval": density_bounds[cycle], "n_pixel_x": density_x[cycle],
                       "legend_sample_xy": [75, legend_y, 91, legend_y],
                       "legend_mean_rgb": palette,
                       "current_unique_cycle_assignment": cycle == 5,
                       "nominal_rule": "midpoint of full conservative manual raster interval"})
    result = {
        "source_sha256": EXPECTED,
        "method": "Manual native-JPEG color-compatible interval selection followed by affine axis calibration; no raw traces or vector paths",
        "points": points,
        "provenance": {
            "source": str(SOURCE.relative_to(ROOT)), "pdf_page_1based": 9,
            "image_xref": 65, "native_dimensions_px": [540, 412], "source_filter": "DCTDecode",
            "x_anchors_pixel_V_RHE": x_anchors, "j_anchors_pixel_mA_cm2": j_anchors,
            "n_anchors_pixel_nmol_cm2": n_anchors, "x_target_pixel": x_target,
            "target_V_RHE": 1.52, "direction": "not identified; no sweep branch selected",
            "interval_basis": "Manually selected visible stroke, marker, JPEG and color-assignment envelopes, including horizontal calibration band; not exhaustive bounds or experimental confidence intervals",
            "current_color_ambiguity": "Cycles1/2,3/4,6/7 share interval bounds because their individual colors/intersections cannot reliably be separated in this raster",
            "density_cycle1_ambiguity": "Overlapping green strokes/markers against orange bar; interval spans full visible extent rather than assuming a single center",
            "excluded_observable": "TOF bars not read or multiplied by site density to reconstruct current",
            "manual_verification": "Compared all selected intervals to native-image enlarged inspection and annotated boxes; every candidate matching trace/symbol visually lies inside its reported envelope",
            "independence_limit": "Repeated cycles from one figure; group-shared intervals are correlated and their midpoints are not distinct resolved observations",
            "experiment_uncertainty": "Unknown; no zero experimental uncertainty assumed",
        },
        "self_checks": {"affine_axes": "PASS", "reversed_axis": "PASS",
                        "out_of_range_rejection": "PASS", "synthetic_line_interpolation": "PASS",
                        "source_identity": "PASS"},
    }
    (DATA / "figS8_points.json").write_text(json.dumps(result, indent=2) + "\n")
    with (DATA / "point_provenance.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cycle", "j_group", "j_x_min", "j_x_max", "j_y_min", "j_y_max", "n_x", "n_y_min", "n_y_max"])
        for point in points:
            writer.writerow([point["cycle"], point["j_legend_group"], *x_band, *point["j_pixel_y_interval"],
                             point["n_pixel_x"], *point["n_pixel_y_interval"]])
    annotated = native.resize((1620, 1236), resample=Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(annotated)
    draw.line([(x_target * 3, 14 * 3), (x_target * 3, 152 * 3)], fill="blue", width=2)
    for cycle in [1, 3, 5, 6]:
        lo, hi = current_bands[cycle]
        offset = {1: 0, 3: 6, 5: 12, 6: 18}[cycle]
        x = 210 * 3 + offset
        draw.line([(x, lo * 3), (x, hi * 3)], fill="blue", width=2)
        draw.text((x + 3, (lo + hi) * 1.5), {1: "1/2", 3: "3/4", 5: "5", 6: "6/7"}[cycle], fill="blue")
    for cycle in range(1, 8):
        x = density_x[cycle]
        lo, hi = density_bounds[cycle]
        draw.rectangle([(3 * (x - 4), 3 * lo), (3 * (x + 4), 3 * hi)], outline="blue", width=2)
    annotated.save(DATA / "figS8_calibration.png")
    print(json.dumps({"source_verified": True, "self_checks": result["self_checks"], "points": len(points),
                      "unique_current_groups": 4, "unique_cycle_current_readings": 1,
                      "artifact": str(DATA / "figS8_points.json")}, indent=2))


if __name__ == "__main__":
    main()
