import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
F = 96485.33212
PROTOCOL_SHA = "97d9721694d1af68a3d9218b5980c607f5e459293ab224a6252366ca2d18aa5c"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polarization(u, parameters):
    limit, slope, half = parameters
    return limit / (1 + np.exp(-slope * (np.asarray(u) - half)))


def exponential(u, parameters):
    log_scale, slope = parameters
    return np.exp(log_scale + slope * (np.asarray(u) - 1.4))


def refine_grid(objective, bounds):
    original = np.asarray(bounds, dtype=float)
    interval = original.copy()
    for _ in range(7):
        axes = [np.linspace(lo, hi, 81) for lo, hi in interval]
        grids = np.meshgrid(*axes, indexing="ij")
        loss = objective(*grids)
        index = np.unravel_index(np.argmin(loss), loss.shape)
        best = np.array([axes[d][i] for d, i in enumerate(index)])
        widths = (interval[:, 1]-interval[:, 0])/80
        interval = np.stack((np.maximum(original[:, 0], best-widths),
                             np.minimum(original[:, 1], best+widths)), axis=1)
    return best, bool(np.any(np.isclose(best, original[:, 0]) | np.isclose(best, original[:, 1])))


def fit_polarization(u, j):
    def loss(slope, half):
        shape = 1/(1+np.exp(-slope[..., None]*(u-half[..., None])))
        limit = np.clip(np.sum(shape*j, axis=-1)/np.sum(shape**2, axis=-1), 1, 10000)
        return np.sum((limit[..., None]*shape-j)**2, axis=-1)
    (slope, half), hit = refine_grid(loss, [(0.01, 30), (-2, 5)])
    shape = 1/(1+np.exp(-slope*(u-half)))
    limit = float(np.clip(np.dot(shape,j)/np.dot(shape,shape),1,10000))
    return np.array([limit,slope,half]), bool(hit or limit in (1,10000))


def fit_exponential(u, j):
    def loss(slope):
        shape=np.exp(slope[...,None]*(u-1.4))
        scale=np.sum(shape*j,axis=-1)/np.sum(shape**2,axis=-1)
        return np.sum((scale[...,None]*shape-j)**2,axis=-1)
    (slope,), _ = refine_grid(loss, [(0,30)])
    shape=np.exp(slope*(u-1.4))
    return np.array([np.log(np.dot(shape,j)/np.dot(shape,shape)),slope])


def detector(times, input_times, input_signal, tau):
    """Exact first-order response to a piecewise-linear, externally measured input."""
    times = np.asarray(times)
    if tau <= 0:
        return np.interp(times, input_times, input_signal)
    knots = np.unique(np.concatenate(([0.0], times, input_times)))
    y, previous = 0.0, 0.0
    values = {0.0: y}
    for t in knots[knots > 0]:
        x0, x1 = np.interp([previous, t], input_times, input_signal)
        dt = t - previous
        slope = (x1 - x0) / dt
        decay = np.exp(-dt / tau)
        y = y * decay + x0 * (1 - decay) + slope * (dt - tau * (1 - decay))
        values[float(t)] = float(y)
        previous = t
    return np.array([values[float(t)] for t in times])


def metrics(observed, predicted):
    residual = np.asarray(predicted) - observed
    return dict(rmse=float(np.sqrt(np.mean(residual**2))),
                max_absolute_error=float(np.max(np.abs(residual))),
                predicted=np.asarray(predicted).tolist(), observed=np.asarray(observed).tolist(),
                residual_predicted_minus_observed=residual.tolist())


def discharge_current(red_mol, total_mol, parameters, u=1.7, area_cm2=0.031):
    if red_mol <= 0 or total_mol <= 0:
        return 0.0
    limit, slope, half = parameters
    kinetic = limit * np.exp(slope * (u - half))
    transport = limit * red_mol / (0.5 * total_mol)
    return float(kinetic * transport / (kinetic + transport) * area_cm2 / 1000)


def inventory(parameters, *, total_mol=0.0005, initial_fraction=0.0, driven=True, charge_enabled=True):
    """Ideal active inventory; current outside mediator pathway is excluded."""
    if total_mol < 0 or not 0 <= initial_fraction <= 1:
        raise ValueError("nonnegative stock and red fraction in [0,1] required")
    red = total_mol * initial_fraction
    initial_red = red
    q_in = q_out = q_refused = h2 = o2 = t0 = 0.0
    traces = []
    # Schedule and 1 mL volume are illustrative interventions, not source reconstructions.
    for name, hours in [("charge", 12), ("rest", 3), ("discharge", 24), ("recharge", 12)]:
        duration = hours * 3600
        grid = np.linspace(0, duration, int(hours * 60) + 1)
        start_red = red
        if name in ("charge", "recharge"):
            request_a = 0.100 * 0.031 if driven and charge_enabled else 0.0
            requested = request_a * grid
            accepted = np.minimum(requested, 2 * F * (total_mol - red))
            series = red + accepted / (2 * F)
            current = np.where(accepted < 2 * F * (total_mol - red), request_a, 0.0)
            phase_h2 = np.full_like(grid, h2)
            phase_o2 = o2 + (series - start_red) / 2
            phase_q_in = q_in + accepted
            phase_q_out = np.full_like(grid, q_out)
            q_refused += float(requested[-1] - accepted[-1])
        elif name == "discharge" and driven and red > 0:
            limit, slope, half = parameters
            kinetic_a = limit*np.exp(slope*(1.7-half))*0.031/1000
            alpha = limit*0.031/1000/(0.5*total_mol)
            lo, hi = -alpha*grid/(2*F), np.zeros_like(grid)
            for _ in range(80):
                z=(lo+hi)/2
                residual=z+alpha*red/kinetic_a*np.expm1(z)+alpha*grid/(2*F)
                lo=np.where(residual<0,z,lo)
                hi=np.where(residual>=0,z,hi)
            series=red*np.exp((lo+hi)/2)
            current = np.array([discharge_current(r, total_mol, parameters) for r in series])
            phase_h2 = h2 + start_red - series
            phase_o2 = np.full_like(grid, o2)
            phase_q_in = np.full_like(grid, q_in)
            phase_q_out = q_out + 2 * F * (start_red - series)
        else:
            series = np.full_like(grid, red)
            current = np.zeros_like(grid)
            phase_h2, phase_o2 = np.full_like(grid, h2), np.full_like(grid, o2)
            phase_q_in, phase_q_out = np.full_like(grid, q_in), np.full_like(grid, q_out)
        for i, t in enumerate(grid):
            traces.append(dict(time_h=(t0+t)/3600, phase=name, red_mol=float(series[i]),
                               ox_mol=float(total_mol-series[i]), mediator_current_A=float(current[i]),
                               H2_mol=float(phase_h2[i]), O2_mol=float(phase_o2[i]),
                               charge_in_C=float(phase_q_in[i]), charge_out_C=float(phase_q_out[i])))
        red, h2, o2 = float(series[-1]), float(phase_h2[-1]), float(phase_o2[-1])
        q_in, q_out = float(phase_q_in[-1]), float(phase_q_out[-1])
        t0 += duration
    # Atom/charge balances expressed as reaction extents, including initially stored Red.
    errors = {
        "mediator_mol": max(abs(r["red_mol"] + r["ox_mol"] - total_mol) for r in traces),
        "stored_charge_C": max(abs(2*F*(r["red_mol"]-initial_red) - r["charge_in_C"] + r["charge_out_C"]) for r in traces),
        "H2_electron_C": max(abs(2*F*r["H2_mol"] - r["charge_out_C"]) for r in traces),
        "O2_electron_C": max(abs(4*F*r["O2_mol"] - r["charge_in_C"]) for r in traces),
        "bound_H2_equivalent_mol": max(abs(r["red_mol"]-initial_red+r["H2_mol"]-2*r["O2_mol"]) for r in traces),
    }
    assert min(r["red_mol"] for r in traces) >= 0
    assert min(r["ox_mol"] for r in traces) >= -1e-16
    assert errors["mediator_mol"] < 1e-14 and max(errors[k] for k in errors if k.endswith("_C")) < 1e-9
    assert errors["bound_H2_equivalent_mol"] < 1e-14
    return traces, dict(total_mol=total_mol, capacity_C=2*F*total_mol,
                       final_red_fraction=red/total_mol if total_mol else 0.0,
                       charge_in_C=q_in, charge_out_C=q_out, refused_charging_C=q_refused,
                       H2_mol=h2, O2_mol=o2, required_abs_proton_transfer_mol=(q_in+q_out)/F,
                       balance_errors=errors)


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled")
    assert digest(BASE/"PROTOCOL.md") == PROTOCOL_SHA, "Frozen protocol changed"
    raw = list(csv.DictReader((BASE/"data/plot_points.csv").open()))
    assert len(raw) == 29
    def data(figure, series):
        rows = [r for r in raw if r["figure"] == figure and r["series"] == series]
        return np.array([float(r["x"]) for r in rows]), np.array([float(r["y"]) for r in rows])
    u4, j4 = data("fig4a", "Pt_ECPB")
    u4, j4 = -u4, -j4
    train = u4 <= 1.8
    assert train.sum() == 6 and (~train).sum() == 2
    p, boundary_hit = fit_polarization(u4[train],j4[train])
    rival = fit_exponential(u4[train],j4[train])
    bounded = metrics(j4[~train], polarization(u4[~train], p))
    unbounded = metrics(j4[~train], exponential(u4[~train], rival))
    u5, j5 = data("fig5a", "Pt_ECPB")
    u5, j5 = -u5, -j5*1000
    geometry = metrics(j5, polarization(u5, p))
    input_t, input_y = data("fig5b", "H2_charge_calculated")
    gas_t, gas_y = data("fig5b", "H2_GC_measured")
    gas_train = gas_t <= 240
    assert gas_train.sum() == 3 and (~gas_train).sum() == 3
    (delay,), delay_hit = refine_grid(lambda taus: np.array([
        np.sum((detector(gas_t[gas_train],input_t,input_y,tau)-gas_y[gas_train])**2) for tau in taus]), [(0.01,600)])
    lagged = metrics(gas_y[~gas_train], detector(gas_t[~gas_train], input_t, input_y, delay))
    instant = metrics(gas_y[~gas_train], detector(gas_t[~gas_train], input_t, input_y, 0))
    assert np.allclose(detector([0, 10], [0, 10], [1, 1], 10), [0, 1-np.exp(-1)])
    optimum,_=refine_grid(lambda x,y:(x-1.25)**2+(y+0.75)**2,[(-3,3),(-3,3)])
    assert np.allclose(optimum,[1.25,-0.75],atol=1e-7)
    assert polarization(100, p) <= p[0] and discharge_current(0, 0.0005, p) == 0
    traces, stock = inventory(p)
    _, no_drive = inventory(p, driven=False)
    _, no_buffer = inventory(p, total_mol=0)
    _, oxidized_no_charge = inventory(p, charge_enabled=False, initial_fraction=0)
    _, reduced_no_charge = inventory(p, charge_enabled=False, initial_fraction=1)
    assert no_drive["H2_mol"] == no_buffer["H2_mol"] == oxidized_no_charge["H2_mol"] == 0
    assert 0 < reduced_no_charge["H2_mol"] <= reduced_no_charge["total_mol"]
    assert reduced_no_charge["O2_mol"] == 0 and reduced_no_charge["charge_in_C"] == 0
    discharge = [r for r in traces if r["phase"] == "discharge"]
    frozen_current_H2 = discharge[0]["mediator_current_A"] * 24*3600 / (2*F)
    assert frozen_current_H2 > stock["total_mol"]
    assert stock["H2_mol"] <= stock["total_mol"]
    # Source SI held condition; no parameter is estimated from these charge endpoints.
    capacity_si = 0.0035*0.5*2*96485
    result = dict(status="BOUNDED_SIMULATIONS_COMPLETE", protocol_sha256=PROTOCOL_SHA,
                  inputs={"plot_points_sha256":digest(BASE/"data/plot_points.csv"),
                          "model_sha256":digest(Path(__file__)),
                          "source_PDF_sha256":digest(BASE.parent/"recursive-compound-2026-10-15/energy/raw/symes2013.pdf"),
                          "supplement_sha256":digest(BASE/"sources/symes2013-si.pdf")},
                  runtime=dict(python=sys.version.split()[0], numpy=np.__version__, matplotlib=matplotlib.__version__),
                  validation_class="retrospective plotted-source holdouts; not independent experimental validation",
                  transport=dict(parameters=dict(j_lim_mA_cm2=float(p[0]), b_per_V=float(p[1]), u_half_V=float(p[2])),
                                 fit_boundary_hit=boundary_hit, calibration_voltage_V=u4[train].tolist(),
                                 heldout_voltage_V=u4[~train].tolist(), calibration=metrics(j4[train],polarization(u4[train],p)),
                                 heldout=bounded, screening_pass=bounded["rmse"]<=10,
                                 effective_k_m_cm_s=float(p[0]/1000/(2*F*0.00025)),
                                 exponential_baseline_parameters=rival.tolist(), exponential_heldout=unbounded),
                  geometry_transfer=dict(heldout=geometry, screening_pass=geometry["rmse"]<=10,
                                         max_observed_over_old_limit=float(max(j5)/p[0]),
                                         limitation="Actual immersed mesh area unknown; no fitted multiplier or quantitative enlarged-geometry prediction"),
                  gas_observation=dict(tau_min=float(delay), fit_boundary_hit=delay_hit,
                                       calibration=metrics(gas_y[gas_train],detector(gas_t[gas_train],input_t,input_y,delay)),
                                       heldout=lagged, instantaneous_heldout=instant, screening_pass=lagged["rmse"]<=0.3,
                                       limitation="Conditioned on measured charge input; headspace percent response, not chemical rate or absolute gas yield"),
                  conditional_inventory=stock,
                  controls=dict(no_drive=no_drive, no_buffer_mediator_pathway=no_buffer,
                                oxidized_no_charge_discharge_enabled=oxidized_no_charge,
                                initially_reduced_no_charge=reduced_no_charge,
                                frozen_current_rival_H2_mol=frozen_current_H2,
                                frozen_current_rival_exceeds_available_stock=frozen_current_H2>stock["total_mol"]),
                  separate_SI_capacity_check=dict(nominal_capacity_C=capacity_si, first_reduction_C=317,
                                                 fourth_reduction_C=308, first_fraction_of_capacity=317/capacity_si,
                                                 fourth_fraction_of_capacity=308/capacity_si,
                                                 fourth_over_first=308/317,
                                                 limitation="No ideal complete-conversion model explains reduced throughput or loss; charge ratio is not molecule survival"),
                  source_energy_penalties=dict(three_electrode_equivalent_V=2.94, direct_V=2.55,
                                               relative_efficiency=2.55/2.94, source_two_electrode_relative_efficiency=0.79),
                  limits=["No mediator decomposition, O2 side reaction or molecular repair kinetics identified",
                          "Direct water splitting outside the mediator pathway is excluded, not experimentally absent",
                          "Effective transport law extrapolation to changing redox fraction is conditional",
                          "No inherited variants, active material replacement, maintained boundary or intelligence established"])
    out = BASE/"results"
    out.mkdir(exist_ok=True)
    (out/"results.json").write_text(json.dumps(result, indent=2)+"\n")
    with (out/"inventory_timeseries.csv").open("w", newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(traces[0])); writer.writeheader(); writer.writerows(traces)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    ax=axes[0,0]; grid=np.linspace(0.5,2.35,200)
    ax.plot(grid,polarization(grid,p),label="finite transport")
    ax.plot(grid,exponential(grid,rival),"--",label="kinetic baseline")
    ax.scatter(u4[train],j4[train],label="calibration")
    ax.scatter(u4[~train],j4[~train],marker="x",label="held out")
    ax.set(xlabel="|iR-corrected cell voltage| (V)",ylabel="Pt current (mA/cm²)",ylim=(0,200),title="Fig 4a: voltage holdout"); ax.legend(fontsize=8)
    ax=axes[0,1]; ax.plot(u5,polarization(u5,p),label="unchanged Fig 4 fit")
    ax.scatter(u5,j5,label="Fig 5 larger counterelectrode")
    ax.set(xlabel="|iR-corrected cell voltage| (V)",ylabel="Pt current (mA/cm²)",title="Geometry transfer: retained failure"); ax.legend(fontsize=8)
    ax=axes[1,0]; grid=np.linspace(0,600,300)
    ax.plot(input_t,input_y,label="measured charge input")
    ax.plot(grid,detector(grid,input_t,input_y,delay),label="one-time-constant detector")
    ax.scatter(gas_t[gas_train],gas_y[gas_train],label="GC calibration")
    ax.scatter(gas_t[~gas_train],gas_y[~gas_train],marker="x",label="GC held out")
    ax.set(xlabel="Time (min)",ylabel="Headspace H₂ (%)",title="Fig 5b: observation delay"); ax.legend(fontsize=8)
    ax=axes[1,1]; ax.plot([r["time_h"] for r in traces],[r["red_mol"]*1000 for r in traces],label="Red stock")
    ax.plot([r["time_h"] for r in traces],[r["H2_mol"]*1000 for r in traces],label="H₂ delivered")
    ax.set(xlabel="Illustrative time (h)",ylabel="Amount (mmol)",title="1 mL finite stock; imposed drive"); ax.legend(fontsize=8)
    fig.suptitle("PMo12: source comparisons and conditional inventory; no life claim")
    fig.tight_layout(); fig.savefig(out/"comparisons.png",dpi=160); plt.close(fig)
    print(json.dumps({"transport_holdout_rmse_mA_cm2":bounded["rmse"],
                      "kinetic_baseline_rmse_mA_cm2":unbounded["rmse"],
                      "geometry_transfer_rmse_mA_cm2":geometry["rmse"],
                      "gas_holdout_rmse_percentage_points":lagged["rmse"],
                      "instantaneous_gas_rmse_percentage_points":instant["rmse"],
                      "inventory":stock},indent=2))


if __name__ == "__main__":
    main()
