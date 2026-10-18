from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parent
with fitz.open(ROOT / 'cs-2026-01228g.pdf') as document:
    drawings = document[4].get_drawings()
ticks = {'left': [], 'right': []}
for path in drawings:
    rect = path['rect']
    if not (330 < rect.y0 < rect.y1 < 410 and 0.5 < rect.height < 0.6 and 2.1 < rect.width < 2.3):
        continue
    if abs(rect.x0 - 91.12) < 0.02:
        ticks['left'].append((rect.y0 + rect.y1) / 2)
    elif abs(rect.x1 - 258.32) < 0.02:
        ticks['right'].append((rect.y0 + rect.y1) / 2)
for values in ticks.values():
    values.sort(reverse=True)
assert len(ticks['left']) == 4
assert len(ticks['right']) == 5
assert abs(ticks['left'][0] - ticks['right'][0]) < 0.01
left_points_per_unit = (ticks['left'][0] - ticks['left'][-1]) / 15
right_points_per_unit = (ticks['right'][0] - ticks['right'][-1]) / 8
conversion = right_points_per_unit / left_points_per_unit
assert 1.60 < conversion < 1.63
result = {'source': 'Main PDF page5 Fig6a; black major tick rectangles only; labels verified visually',
          'left_axis_label': 'Fe / microgram cm^-2', 'right_axis_label': '[Fe] / ppb',
          'left_tick_values': [0,5,10,15], 'right_tick_values': [0,2,4,6,8],
          'tick_center_pdf_y_points': ticks,
          'microgram_per_cm2_per_ppb': conversion,
          'expected_using_50mL_and_area_0_02835cm2': 0.05 / 0.02835,
          'effective_volume_mL_using_area_0_02835cm2': conversion * 0.02835 * 1000,
          'relative_difference_from_50mL_factor': conversion / (0.05 / 0.02835) - 1,
          'response_points_extracted': 0,
          'scope': 'Graphic axis conversion audit; ppb interpreted as microgram/L. Effective volume is a conditional calculation, not a measured reservoir volume.'}
(ROOT / 'fig6-axis-calibration.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
