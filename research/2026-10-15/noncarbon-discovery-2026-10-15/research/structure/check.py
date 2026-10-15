"""Audit acquired parent CIFs; no new molecular geometry or energy is predicted."""
import hashlib
import itertools
import json
import re
import shlex
from collections import Counter
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent


def number(text):
    return float(text.split("(")[0])


def loop(text, field):
    # shortcut: these two deposited loops have single-line rows; use a CIF library for other files.
    lines = text.splitlines()
    start = lines.index(field)
    while lines[start - 1].startswith("_"):
        start -= 1
    stop = start
    while lines[stop].startswith("_"):
        stop += 1
    headers = lines[start:stop]
    rows = []
    for line in lines[stop:]:
        if line.startswith(("loop_", "_", "data_")):
            break
        if line.strip() and not line.startswith("#"):
            values = shlex.split(line)
            assert len(values) == len(headers), (headers, values)
            rows.append(dict(zip(headers, values)))
    return rows


def scalar(text, key):
    return shlex.split(re.search(r"^" + key + r"\s+(.+)$", text, re.M)[1])[0]


def transformed(point, expression):
    values = dict(zip("xyz", point))
    out = []
    for coordinate in expression.split(","):
        terms = re.findall(r"[+-]?[^+-]+", coordinate)
        assert "".join(terms) == coordinate
        value = 0.0
        for term in terms:
            sign = -1 if term.startswith("-") else 1
            term = term.lstrip("+-")
            if term in values:
                value += sign * values[term]
            else:
                parts = term.split("/")
                assert len(parts) <= 2 and all(p.isdigit() for p in parts)
                value += sign * int(parts[0]) / (int(parts[1]) if len(parts) == 2 else 1)
        out.append(value % 1)
    return tuple(round(v, 8) for v in out)


def audit(name):
    text = (BASE / "raw" / name).read_text()
    atoms = loop(text, "_atom_site_label")
    ops = [r["_symmetry_equiv_pos_as_xyz"] for r in loop(text, "_symmetry_equiv_pos_as_xyz")]
    metals = [r for r in atoms if r["_atom_site_type_symbol"].startswith("Mo")]
    assert len(metals) == 18
    assert not any(r["_atom_site_type_symbol"] == "H" for r in atoms)
    mo_positions = set()
    oxygens = []
    for row in atoms:
        point = tuple(number(row[f"_atom_site_fract_{axis}"]) for axis in "xyz")
        for op in ops:
            pos = transformed(point, op)
            if row in metals:
                mo_positions.add(pos)
            elif row["_atom_site_type_symbol"].startswith("O"):
                oxygens.append((row["_atom_site_label"], pos))
    z = number(scalar(text, "_cell_formula_units_Z"))
    assert len(mo_positions) / z == 36
    a, b, c = [number(scalar(text, f"_cell_length_{v}")) for v in "abc"]
    beta = np.deg2rad(number(scalar(text, "_cell_angle_beta")))
    assert number(scalar(text, "_cell_angle_alpha")) == number(scalar(text, "_cell_angle_gamma")) == 90
    cell = np.array([[a, 0, 0], [0, b, 0], [c * np.cos(beta), 0, c * np.sin(beta)]])
    images = np.array(list(itertools.product((-1, 0, 1), repeat=3)))
    oxygen_positions = np.array([p for _, p in oxygens])
    nearest = {}
    for row in metals:
        p = np.array([number(row[f"_atom_site_fract_{axis}"]) % 1 for axis in "xyz"])
        distances = np.linalg.norm((oxygen_positions[:, None, :] + images[None, :, :] - p) @ cell, axis=2).min(axis=1)
        nearest[row["_atom_site_label"]] = {"nearest_O_distance_A": round(float(distances.min()), 4), "O_neighbors_within_2_6_A": int(sum(distances <= 2.6))}
    return {
        "formula_in_deposit": scalar(text, "_chemical_formula_sum"),
        "asymmetric_unit_atom_rows_by_type": dict(Counter(r["_atom_site_type_symbol"] for r in atoms)),
        "symmetry_operations": ops,
        "unit_cell_Mo_positions": len(mo_positions), "Z": z,
        "Mo_per_formula": len(mo_positions) / z,
        "hydrogen_positions_present": False,
        "partially_occupied_rows": [r["_atom_site_label"] for r in atoms if number(r["_atom_site_occupancy"]) < 1],
        "geometric_audit_only_not_bond_assignment": nearest,
    }


assert transformed((0.2, 0.3, 0.4), "1/2-x,y,-z") == (0.3, 0.3, 0.6)
assert number("95.73(2)") == 95.73
acquisition = json.loads((BASE / "acquisition.json").read_text())
for record in acquisition:
    if "sha256" in record:
        assert hashlib.sha256((BASE / "raw" / record["filename"]).read_bytes()).hexdigest() == record["sha256"]
checks = {name: audit(name) for name in ("cod2107026.cif", "cod4030345.cif")}
k_neighbors = checks["cod2107026.cif"]["geometric_audit_only_not_bond_assignment"]
assert Counter(r["O_neighbors_within_2_6_A"] for r in k_neighbors.values()) == {6: 16, 7: 2}
na_mo6 = checks["cod4030345.cif"]["geometric_audit_only_not_bond_assignment"]["Mo6"]
assert abs(na_mo6["nearest_O_distance_A"] - 1.335) < 0.001
assert na_mo6["O_neighbors_within_2_6_A"] == 4
checks["hypothetical_target"] = {
    "formula": "[Mo(VI)34W(VI)V(V)O112(H2O)16]9-",
    "formal_charge": 34 * 6 + 6 + 5 - 112 * 2,
    "V_IV_counterpart_formal_charge": 34 * 6 + 6 + 4 - 112 * 2,
    "atoms_including_explicit_water_H": 34 + 1 + 1 + 112 + 16 * 3,
    "all_electron_count_formal_minus9_state": 34 * 42 + 74 + 23 + 128 * 8 + 32 + 9,
    "ordered_W_V_site_assignments_before_symmetry_reduction": 36 * 35,
    "target_coordinates_generated": False,
    "electronic_structure_calculations_run": False,
}
assert checks["hypothetical_target"]["formal_charge"] == -9
assert checks["hypothetical_target"]["V_IV_counterpart_formal_charge"] == -10
assert checks["hypothetical_target"]["atoms_including_explicit_water_H"] == 196
assert checks["hypothetical_target"]["all_electron_count_formal_minus9_state"] == 2590
(BASE / "checks.json").write_text(json.dumps(checks, indent=2) + "\n")
print("PASS: retained-file hashes, two parent CIF Mo counts, formula accounting; geometry flags are retained in checks.json")
