import csv
import hashlib
import json
import shutil
from collections import deque
from pathlib import Path

import fitz
import numpy as np

BASE = Path(__file__).resolve().parent
PDF = BASE / "sources/gtm3/2025-main.pdf"
SHA = "f83754d9317c0fd177471fb0d18f1ae9a78d02bdcdc3a472433f9bff8afe36f6"
# Native image pixels, from black axis-line projections and printed 0/100 labels.
AXES = {"A": (129.0, 723.0, 14.5, 530.5),
        "B": (873.5, 1471.0, 14.5, 530.5)}


def holes(mask):
    seen = mask.copy()
    height, width = seen.shape
    result = []
    for y in range(height):
        for x in range(width):
            if seen[y, x]:
                continue
            queue = deque([(x, y)])
            seen[y, x] = True
            points = []
            edge = False
            while queue:
                px, py = queue.popleft()
                points.append((px, py))
                edge |= px == 0 or py == 0 or px == width - 1 or py == height - 1
                for nx, ny in ((px-1, py), (px+1, py), (px, py-1), (px, py+1)):
                    if 0 <= nx < width and 0 <= ny < height and not seen[ny, nx]:
                        seen[ny, nx] = True
                        queue.append((nx, ny))
            if not edge and 20 <= len(points) <= 180:
                xx, yy = zip(*points)
                w, h = max(xx)-min(xx)+1, max(yy)-min(yy)+1
                if 5 <= w <= 18 and 5 <= h <= 18 and abs(w-h) <= 3:
                    result.append((float(np.mean(xx)), float(np.mean(yy)), len(points)))
    return result


def main():
    assert hashlib.sha256(PDF.read_bytes()).hexdigest() == SHA
    with fitz.open(PDF) as document:
        images = document[2].get_images(full=True)
        assert len(images) == 1 and images[0][2:4] == (1500, 1285)
        pix = fitz.Pixmap(document, images[0][0])
        pixels = np.frombuffer(pix.samples, dtype=np.uint8).reshape(1285, 1500, 3)
        raw_image = pix.tobytes("png")
    red, green, blue = np.moveaxis(pixels.astype(float), 2, 0)
    masks = {"untreated": (red > 120) & (red > 1.6*green) & (red > 1.5*blue),
             "preactivated": (blue > 100) & (blue > 1.3*red) & (blue > 0.9*green)
             & (red < 220) & (green < 230)}
    rows, exclusions = [], []
    # Pad axes so markers centered at 0/100 remain enclosed in the crop.
    for panel, (left, right, top, bottom) in AXES.items():
        x0, x1 = int(left)-14, min(1500, int(right)+15)
        for treatment, mask in masks.items():
            found = holes(mask[:550, x0:x1])
            for cx, cy, area in found:
                cx += x0
                # Legends: A lower-left, B upper-left, visually verified.
                is_legend = (panel == "A" and 170 < cx < 280 and cy > 380) or (
                    panel == "B" and 900 < cx < 1030 and cy < 140)
                record = {"catalyst": "GTM-4(RS-OMBMEP)", "panel": panel, "treatment": treatment,
                          "pixel_x": round(cx, 3), "pixel_y": round(cy, 3),
                          "hole_area_pixels": area}
                if is_legend:
                    exclusions.append(record)
                    continue
                record.update(conversion_pct=round(100*(cx-left)/(right-left), 3),
                              ee_pct=round(100*(bottom-cy)/(bottom-top), 3))
                if panel == "A":
                    record["ee_pct"] *= -1
                record["coordinate_allowance_pp"] = 2.0
                record["method"] = "enclosed_hole"
                rows.append(record)
    # Blue overlaps break two red marker outlines; fit their remaining red arcs.
    yy, xx = np.where(masks["untreated"])
    for approximate_x, approximate_y in ((645, 245), (723, 275)):
        radius_squared = (xx-approximate_x)**2+(yy-approximate_y)**2
        selected = (radius_squared > 25) & (radius_squared < 121)
        px, py = xx[selected], yy[selected]
        cx, cy, offset = np.linalg.lstsq(np.column_stack((2*px, 2*py, np.ones(len(px)))),
                                        px**2+py**2, rcond=None)[0]
        radius = np.sqrt(offset+cx**2+cy**2)
        assert selected.sum() > 80 and 6 < radius < 11
        left, right, top, bottom = AXES["A"]
        rows.append({"catalyst": "GTM-4(RS-OMBMEP)", "panel": "A", "treatment": "untreated", "pixel_x": round(cx, 3),
                     "pixel_y": round(cy, 3), "hole_area_pixels": None,
                     "conversion_pct": round(100*(cx-left)/(right-left), 3),
                     "ee_pct": round(-100*(bottom-cy)/(bottom-top), 3),
                     "coordinate_allowance_pp": 2.0, "method": "red_arc_circle_fit"})
    rows.sort(key=lambda r: (r["panel"], r["treatment"], r["conversion_pct"]))
    out = BASE / "data"
    out.mkdir(exist_ok=True)
    if (out / "markers.csv").exists() and not (out / "initial_markers.csv").exists():
        shutil.copyfile(out / "markers.csv", out / "initial_markers.csv")
        shutil.copyfile(out / "extraction.json", out / "initial_extraction.json")
    (out / "figure1-native.png").write_bytes(raw_image)
    with (out / "markers.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = {f"{p}/{t}": sum(r["panel"] == p and r["treatment"] == t for r in rows)
              for p in AXES for t in masks}
    assert counts == {"A/untreated": 12, "A/preactivated": 12,
                      "B/untreated": 10, "B/preactivated": 11}
    assert len(exclusions) == 4
    receipt = {"source_sha256": SHA, "doi": "10.1021/jacs.5c12567",
               "catalyst": "GTM-4(RS-OMBMEP)",
               "page_zero_based": 2, "image_size": [1500, 1285], "axes_pixels": AXES,
               "method": "Enclosed white centers of colored hollow circles; separate panels and legend exclusion.",
               "data_class": "Published raster digitization, not original measurements",
               "allowance": "2 percentage points on x/y, analyst allowance; experimental uncertainty unknown",
               "partial_extraction": "Overlapping near-origin B markers and one overlapping 100%-ee B marker are not recovered. No fit-region blue markers are missing; withheld plateau retains two distinct recoverable markers. Unrecovered points are not imputed.",
               "fallback": "Two visually located red A markers have partial blue overlap; remaining red arcs fitted to circles, centers within 1 pixel of initial visual locations.",
               "counts": counts, "excluded_legends": exclusions,
               "csv_sha256": hashlib.sha256((out / "markers.csv").read_bytes()).hexdigest(),
               "protocol_sha256": hashlib.sha256((BASE / "PROTOCOL.md").read_bytes()).hexdigest()}
    (out / "extraction.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"counts": counts, "excluded_legends": len(exclusions)}))


if __name__ == "__main__":
    main()
