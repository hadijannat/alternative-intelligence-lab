from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent


def overlap(distance_um, radius_um):
    assert radius_um > 0
    pump = math.erfc(math.sqrt(2) * distance_um / radius_um) / 2
    return {"distance_um": distance_um, "radius_um": radius_um,
            "pump_fraction_in_seed": pump,
            "integrated_I_squared_fraction": math.erfc(2 * distance_um / radius_um) / 2,
            "coherent_on_axis_relative_power": pump**2}


def amplitude(q, signs, length=20.0):
    q = np.atleast_1d(np.asarray(q, dtype=float))
    edges = np.linspace(0, length, len(signs) + 1)
    result = np.zeros(q.shape, dtype=complex)
    zero = np.isclose(q, 0, atol=1e-14)
    result[zero] = np.dot(signs, np.diff(edges))
    nz = q[~zero, None]
    pieces = (np.exp(1j*nz*edges[1:]) - np.exp(1j*nz*edges[:-1])) / (1j*nz)
    result[~zero] = pieces @ signs
    return result / length


def self_check():
    at_interface = overlap(0, 35)
    assert at_interface["pump_fraction_in_seed"] == .5
    assert at_interface["integrated_I_squared_fraction"] == .5
    assert at_interface["coherent_on_axis_relative_power"] == .25
    assert overlap(225, 70)["pump_fraction_in_seed"] > overlap(225, 35)["pump_fraction_in_seed"]
    assert overlap(100, 35)["pump_fraction_in_seed"] > overlap(225, 35)["pump_fraction_in_seed"]
    assert overlap(225, 35)["pump_fraction_in_seed"] < 1e-30
    z = np.linspace(-10, 0, 100001)
    integral = np.trapezoid(np.exp(-2*(z-1)**2), z) / math.sqrt(math.pi/2)
    assert abs(integral - overlap(1, 1)["pump_fraction_in_seed"]) < 1e-9
    constant = amplitude(np.array([0, .3, 2.1]), np.ones(40))
    expected = np.array([1, np.exp(1j*.3*10)*np.sinc(.3*10/np.pi),
                         np.exp(1j*2.1*10)*np.sinc(2.1*10/np.pi)])
    assert np.allclose(constant, expected, atol=1e-14)
    signs = np.tile([1., -1.], 20)
    assert abs(amplitude([2*np.pi], signs)[0] - 2j/np.pi) < 1e-13
    scan = np.linspace(0, 4*np.pi, 2001)
    normal, reversed_ = amplitude(scan, signs), amplitude(scan, -signs)
    assert np.array_equal(abs(normal)**2, abs(reversed_)**2)
    assert abs(19.5*.65 - 12.7) < .03
    return {"gaussian_limits_monotonicity_quadrature": "PASS",
            "diameter_to_radius": "70 micrometre diameter => 35 micrometre radius",
            "constant_medium_analytic_integral": "PASS",
            "periodic_first_order_analytic_amplitude": "PASS",
            "global_sign_intensity_invariance": "PASS", "bandwidth_units": "PASS"}


def main():
    checks = self_check()
    source_paths = [ROOT / "PROTOCOL.md", ROOT / "sources/ome2011.pdf", ROOT / "sources/jcg2012.pdf"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    hashes["check_optics.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    scan = np.linspace(0, 4*np.pi, 2001)
    signs = np.tile([1., -1.], 20)
    periodic = abs(amplitude(scan, signs))**2
    reversed_ = abs(amplitude(scan, -signs))**2
    uniform = abs(amplitude(scan, np.ones(40)))**2
    result = {"classification": "Source-informed analytic consistency and synthetic observation-symmetry check; no fit or held-out validation",
              "hashes": hashes, "self_checks": checks,
              "nominal_geometry": overlap(225, 70/2),
              "geometry_sensitivity": [overlap(d, w) for w in (35, 70, 140) for d in (0, 25, 50, 100, 150, 200, 225)],
              "source_peak_ratio_layer_to_seed": .72,
              "conditional_same_geometry_seed_mode_pump_fraction_required": math.sqrt(.72),
              "measured_stray_light_upper_bound": None,
              "independent_experimental_founder_function_upper_bound": None,
              "spectral_consistency": {"seed_nm": 2127.1, "layer_nm": 2126.9, "quoted_half_width_nm": .5,
                  "quoted_error_statistical_definition": None, "center_difference_nm": 2127.1-2126.9,
                  "overlap_of_quoted_intervals_nm": [max(2127.1-.5, 2126.9-.5), min(2127.1+.5, 2126.9+.5)],
                  "reported_bandwidth_product_nm_cm": 12.7, "ideal_bandwidth_product_nm_cm": 9.4,
                  "bandwidth_broadening_factor": 12.7/9.4, "path_length_cm": .65,
                  "FWHM_from_reported_product_nm": 12.7/.65, "FWHM_from_ideal_product_nm": 9.4/.65,
                  "source_FWHM_nm": 19.5},
              "synthetic_phase_matching": {"periods": 20, "scan_q": scan.tolist(),
                  "periodic_intensity": periodic.tolist(), "global_sign_reversed_intensity": reversed_.tolist(),
                  "uniform_intensity": uniform.tolist(), "global_sign_max_intensity_difference": float(abs(periodic-reversed_).max()),
                  "physical_wavelength_prediction": None},
              "verified_integrated_complements_added": 0, "functional_heredity_demonstrated": False}
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "optics.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for w in (35, 70, 140):
        distances = np.linspace(0, 225, 226)
        values = [overlap(d, w)["integrated_I_squared_fraction"] for d in distances]
        axes[0].semilogy(distances, values, label=f"radius {w} um")
    axes[0].axhline(.72, color="black", linestyle=":", label="reported layer/seed peak")
    axes[0].set(xlabel="Beam center distance into new layer (um)", ylabel="Conditional relative SHG",
                title="Ideal Gaussian local-intensity model")
    axes[0].legend(fontsize=8)
    axes[1].plot(scan/(2*np.pi), periodic, label="periodic domains")
    axes[1].plot(scan/(2*np.pi), reversed_, linestyle="--", label="all signs reversed")
    axes[1].plot(scan/(2*np.pi), uniform, alpha=.6, label="uniform medium")
    axes[1].set(xlabel="Dimensionless mismatch / (2 pi)", ylabel="Normalized intensity",
                title="Synthetic grating: absolute sign is lost")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "optics.png", dpi=150)
    plt.close(fig)
    print(json.dumps({"self_checks": checks, "nominal_geometry": result["nominal_geometry"],
                      "spectral_consistency": result["spectral_consistency"],
                      "sign_invariance_max_difference": float(abs(periodic-reversed_).max())}, indent=2))


if __name__ == "__main__":
    main()
