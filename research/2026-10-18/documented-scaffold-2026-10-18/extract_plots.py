import csv
import hashlib
import json
from pathlib import Path

import fitz


BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "recursive-compound-2026-10-15/energy/raw/symes2013.pdf"
SOURCE_SHA256 = "cba5ee525fdfba67185b30180dae2b3ae201cb89e2bed40e66b42e831dd9d9a6"
COORDINATE_ALLOWANCE_PT = 0.1

AXES = {
    "fig4a": {
        "x": [(0, -2.5), (2, -2), (4, -1.5), (6, -1), (8, -0.5)],
        "y": [(10, -120), (12, -100), (14, -80), (16, -60),
              (18, -40), (20, -20), (22, 0), (24, 20)],
        "units": ["V_iR_corrected", "mA_per_cm2"], "digits": [3, 1],
    },
    "fig5a": {
        "x": [(646, -3), (648, -2), (650, -1), (652, 0)],
        "y": [(654, -0.3), (656, -0.2), (658, -0.1), (660, 0)],
        "units": ["V_iR_corrected", "A_per_cm2"], "digits": [3, 4],
    },
    "fig5b": {
        "x": [(566, 0), (568, 200), (570, 400), (572, 600)],
        "y": [(575, 0), (577, 1), (579, 2), (581, 3), (583, 4),
              (585, 5), (587, 6), (589, 7), (591, 8)],
        "units": ["min", "headspace_H2_percent"], "digits": [1, 2],
    },
}
SERIES = [
    ("fig4a", "Pt_ECPB", list(range(105, 120, 2)), "red"),
    ("fig5a", "Pt_ECPB", list(range(710, 727, 2)), "red"),
    ("fig5b", "H2_charge_calculated", list(range(620, 631, 2)), "red"),
    ("fig5b", "H2_GC_measured", list(range(633, 639)), "cyan"),
]


def calibrate(drawings, ticks, dimension):
    coords = []
    for index, value in ticks:
        drawing = drawings[index]
        rect = drawing["rect"]
        if len(drawing["items"]) != 1 or drawing["items"][0][0] != "l":
            raise ValueError(f"Expected single tick line at drawing {index}")
        if (rect.width if dimension == "x" else rect.height) > 0.01:
            raise ValueError(f"Tick {index} has unexpected orientation")
        coords.append((rect.x0 if dimension == "x" else rect.y0, value))
    mean_coord = sum(c for c, _ in coords) / len(coords)
    mean_value = sum(v for _, v in coords) / len(coords)
    slope = sum((c - mean_coord) * (v - mean_value) for c, v in coords) / sum(
        (c - mean_coord) ** 2 for c, _ in coords
    )
    intercept = mean_value - slope * mean_coord
    residual = max(abs(slope * c + intercept - v) for c, v in coords)
    if residual / abs(slope) > 0.05:
        raise ValueError("Axis linearity exceeds the 0.05 PDF-point self-check bound")
    return {
        "slope": slope, "intercept": intercept, "max_tick_residual": residual,
        "ticks": [{"drawing_index": i, "coordinate_pt": c, "value": v}
                  for (i, _), (c, v) in zip(ticks, coords)],
    }


def main():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("PDF source hash changed; drawing indices require review")
    with fitz.open(SOURCE) as document:
        page = document[3]
        drawings = page.get_drawings()
        if len(drawings) != 1038:
            raise ValueError("Unexpected PDF drawing inventory")
        calibrations = {
            figure: {axis: calibrate(drawings, spec[axis], axis) for axis in ("x", "y")}
            for figure, spec in AXES.items()
        }
        rows = []
        markers = []
        for figure, series, ids, color in SERIES:
            for marker_number, index in enumerate(ids):
                drawing = drawings[index]
                fill = drawing["fill"]
                expected = (0.931258, 0.129946, 0.141039) if color == "red" else (
                    0.436851, 0.802152, 0.867094
                )
                if fill is None or max(abs(a - b) for a, b in zip(fill, expected)) > 1e-5:
                    raise ValueError(f"Unexpected marker color at drawing {index}")
                kinds = [item[0] for item in drawing["items"]]
                if kinds != (["re"] if color == "red" else ["c"] * 4):
                    raise ValueError(f"Unexpected marker shape at drawing {index}")
                rect = drawing["rect"]
                if not 1.9 < rect.width < 2.8 or abs(rect.width - rect.height) > 0.01:
                    raise ValueError(f"Unexpected marker geometry at drawing {index}")
                center = {"x": (rect.x0 + rect.x1) / 2, "y": (rect.y0 + rect.y1) / 2}
                row = {"figure": figure, "series": series, "marker_index": marker_number,
                       "pdf_drawing_index": index}
                for axis, digits, units in zip(("x", "y"), AXES[figure]["digits"], AXES[figure]["units"]):
                    cal = calibrations[figure][axis]
                    row[axis] = round(cal["slope"] * center[axis] + cal["intercept"], digits)
                    row[f"{axis}_unit"] = units
                    row[f"{axis}_digitization_allowance"] = round(
                        abs(cal["slope"]) * COORDINATE_ALLOWANCE_PT
                        + cal["max_tick_residual"] + 0.5 * 10 ** -digits, 6
                    )
                rows.append(row)
                markers.append({"figure": figure, "series": series, "drawing_index": index,
                                "bbox_pt": list(rect), "center_pt": center})
    if len(rows) != 29 or len({r["pdf_drawing_index"] for r in rows}) != 29:
        raise ValueError("Marker count or uniqueness self-check failed")
    if max(r["y_digitization_allowance"] for r in rows if r["figure"] == "fig5b") >= 0.1:
        raise ValueError("Gas digitization allowance exceeds requested precision")
    output = BASE / "data"
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "plot_points.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    receipt = {
        "source": str(SOURCE.relative_to(BASE.parent)), "source_sha256": SOURCE_SHA256,
        "source_doi": "10.1038/nchem.1621", "pdf_page_zero_based": 3,
        "printed_page": 406, "pymupdf_version": fitz.VersionBind,
        "method": "Affine axis calibration from labeled vector tick paths; filled marker bounding-box centers.",
        "data_class": "digitized published figure, not raw experimental data",
        "coordinate_allowance_pt": COORDINATE_ALLOWANCE_PT,
        "uncertainty_definition": "Conservative digitization allowance = 0.1 PDF point times axis scale + maximum tick residual + half rounding interval. This is an analyst allowance, not measured experimental uncertainty or a confidence interval.",
        "experimental_error_bars": {
            "fig4a_and_fig5a": "Source caption: horizontal error associated with iR compensation (+/-3%); vertical error is standard deviation of currents. Individual bars were not extracted.",
            "fig5b": "Source caption: error bars within markers correspond to +/-2%; convention retained verbatim, no invented per-point SD.",
        },
        "limitations": [
            "Markers and axes have finite plotting precision; derived coordinates are not original author measurements.",
            "Near-zero negative GC concentration caused by marker placement is preserved; no clipping or baseline correction applied.",
            "Different series' time coordinates differ slightly because of artwork placement; no snapping to nominal times.",
            "Legend symbols 642 and 645 excluded; only explicitly listed primary data markers retained.",
            "No fitting, chemistry inference, or experimental replicate reconstruction performed.",
        ],
        "axis_calibrations": calibrations, "markers": markers,
        "series_counts": {f"{fig}/{name}": len(ids) for fig, name, ids, _ in SERIES},
        "self_check": "PASS: source hash, drawing inventory, tick orientation/linearity, marker shape/color/geometry, count/uniqueness and gas allowance",
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (output / "extraction_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"self_check": "PASS", "markers": len(rows), "csv": str(csv_path)}))


if __name__ == "__main__":
    main()
