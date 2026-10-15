"""Closed-membrane warm chemistry and reversible freeze–thaw exchange.

Concentrations are micromolar, warm time is minutes, and transport time is FT
cycles. Exterior inventories use the same unit intracellular-volume reference as
inside inventories. H labels competent founder RNA; it is not an extra species.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

NAMES = ("A", "R", "B", "F", "P", "D", "H")
MOIETIES = np.array([[1, 0, 0, 1, 0, 1, 0],
                    [0, 1, 0, 0, 1, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0]], float)
CHEMISTRY_SOURCE = "rna-turnover-tests-2026-10-15/results-v1/fits/baseline__omit-none.json"
CHEMISTRY_SOURCE_SHA256 = "aa22679582cd8f4233c038b2b2550c6a716f6a32122ad1a795b7eb6d47d47882"
CHEMISTRY = dict(ka=0.01571930404353992, kb=1.3611955373989844,
                 kd=0.012946670134460872, kf=0.14700614279831425,
                 kh=0.0006836756169276764, krh=0.000708265067441493)


def _states(x):
    x = np.asarray(x, float)
    if (x.ndim != 2 or x.shape[1] != len(NAMES) or not len(x)
            or np.any(~np.isfinite(x)) or np.any(x < 0)):
        raise ValueError("Expected finite nonnegative cohort-by-seven states")
    if np.any(x[:, 6] > x[:, 3] + 1e-8):
        raise ValueError("Competent founder tag cannot exceed competent RNA")
    return x


def _weights(x, w):
    w = np.asarray(w, float)
    if (w.shape != (len(x),) or np.any(~np.isfinite(w)) or np.any(w < 0)
            or not np.isclose(w.sum(), 1., rtol=0, atol=1e-12)):
        raise ValueError("Cohort weights must be nonnegative and sum to one")
    return w


def _count(n, name):
    if not np.isfinite(n) or n < 0 or int(n) != n:
        raise ValueError(f"{name} must be a nonnegative integer")
    return int(n)


def _parameters(family, params):
    keys = {"legacy": {"mixing"}, "bath": {"nu"}, "patch": {"nu", "diffusion"}}
    if family not in keys or set(params) != keys[family]:
        raise ValueError("Unknown family or mismatched transport parameter names")
    if not all(np.isfinite(v) for v in params.values()):
        raise ValueError("Transport parameters must be finite")
    if family == "legacy":
        if not 0 <= params["mixing"] <= 1:
            raise ValueError("Mixing must lie in [0,1]")
        return 0.
    if params["nu"] < 1:
        raise ValueError("Exterior/interior volume ratio must be at least one")
    if family == "patch" and params["diffusion"] < 0:
        raise ValueError("Patch diffusion must be nonnegative")
    return float(params["nu"])


def permeability(nu):
    """Conditional 55% retention anchor for an initially internal passive tracer."""
    if not np.isfinite(nu) or nu < 1:
        raise ValueError("Exterior/interior volume ratio must be at least one")
    return float(-np.log(.55 - .45 / nu) / (3 * (1 + 1 / nu)))


def fresh():
    x = np.zeros((2, len(NAMES)))
    x[0, :2], x[1, 2] = (10, 2.5), 15
    return x


def initial(seed):
    if not np.isfinite(seed) or seed < 0:
        raise ValueError("Founder concentration must be finite and nonnegative")
    x = np.vstack((np.zeros((1, len(NAMES))), fresh()))
    x[0, 3] = x[0, 6] = seed
    return x, np.zeros_like(x), np.full(3, 1 / 3)


def react(states, minutes=60, rtol=1e-8):
    """The earlier selected six-species chemistry, with an analytic founder tag."""
    x = _states(states)
    if not np.isfinite(minutes) or minutes < 0:
        raise ValueError("Reaction time must be finite and nonnegative")
    if not np.isfinite(rtol) or not 0 < rtol < 1:
        raise ValueError("Relative tolerance must lie in (0,1)")
    if minutes == 0:
        return x.copy()
    shape = (len(x), 6)
    p = CHEMISTRY

    def rhs(t, flat):
        z = np.maximum(flat.reshape(shape), 0)
        a, r, b, f, _, _ = z.T
        occupancy = b / (p["kb"] + b)
        # shortcut: effective bulk rates; replace when intermediates are measured.
        va = p["ka"] * f * a * occupancy + p["kh"] * a * a * occupancy**2
        vr = p["kf"] * f * r * occupancy + p["krh"] * a * r * occupancy**2
        decay = p["kd"] * f
        return np.stack((-va, -vr, -va-vr, va-decay, vr, decay), axis=1).ravel()

    sol = solve_ivp(rhs, (0, float(minutes)), x[:, :6].ravel(), method="LSODA",
                    rtol=rtol, atol=rtol*1e-2)
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.min(sol.y) < -1e-7:
        raise ArithmeticError("Negative chemical concentration")
    result = np.column_stack((np.maximum(sol.y[:, -1].reshape(shape), 0),
                              x[:, 6] * np.exp(-p["kd"] * minutes)))
    return _states(result)


def exchange(inside, outside, weights, family, params, cycles, *, kappa_override=None):
    """Exact linear exchange map; no reaction occurs during these FT events."""
    x, e = _states(inside).copy(), _states(outside).copy()
    w = _weights(x, weights)
    if e.shape != x.shape:
        raise ValueError("Exterior patches must match intracellular cohorts")
    n = _count(cycles, "FT count")
    nu = _parameters(family, params)
    if kappa_override is not None and (not np.isfinite(kappa_override) or kappa_override < 0):
        raise ValueError("Permeability override must be finite and nonnegative")
    if family == "legacy":
        if kappa_override is not None or np.any(e):
            raise ValueError("Legacy transport has neither permeability nor an exterior pool")
        mean = w @ x
        retention = .55 ** (n/3)
        x = retention * (mean + (1-params["mixing"])**n * (x-mean))
        return _states(x), e, (1-retention)*mean
    if n == 0:
        return x, e, np.zeros(len(NAMES))
    k = permeability(nu) if kappa_override is None else kappa_override
    mean_x, mean_e = w @ x, w @ e
    total = mean_x + nu * mean_e
    difference = (mean_x-mean_e) * np.exp(-k*(1+1/nu)*n)
    next_mean_x = (total + nu*difference) / (1+nu)
    next_mean_e = (total - difference) / (1+nu)
    if family == "bath":
        x = next_mean_x + (x-mean_x)*np.exp(-k*n)
        e = np.broadcast_to(next_mean_e, e.shape).copy()
    else:
        matrix = np.array([[-k, k], [k/nu, -k/nu-params["diffusion"]]])
        evolution = expm(matrix*n)
        dx, de = x-mean_x, e-mean_e
        x = next_mean_x + evolution[0, 0]*dx + evolution[0, 1]*de
        e = next_mean_e + evolution[1, 0]*dx + evolution[1, 1]*de
    if min(np.min(x), np.min(e)) < -1e-9:
        raise ArithmeticError("Negative exchange concentration")
    return _states(np.maximum(x, 0)), _states(np.maximum(e, 0)), np.zeros(len(NAMES))


def reporter(inside, weights):
    """Washed PAGE reads internal RNA without modifying the continuing culture."""
    x = _states(inside)
    inventory = _weights(x, weights) @ x
    denominator = inventory[1] + inventory[4]
    return float(100*inventory[4]/denominator) if denominator > 0 else 0.


def feed(inside, outside, weights, nu):
    """Half suspension transfer, then equal A/R and B fresh-cohort contributions."""
    x, e = _states(inside), _states(outside)
    w = _weights(x, weights)
    if e.shape != x.shape or not np.isfinite(nu) or nu < 0:
        raise ValueError("Invalid exterior state or volume ratio")
    removed = .5 * (w @ x + nu * (w @ e))
    added = .25 * fresh().sum(axis=0)
    new_x = np.vstack((x, fresh()))
    # Resuspension homogenizes the carried half-volume exterior before the next FT.
    new_e = np.broadcast_to(.5*(w @ e), new_x.shape).copy()
    return new_x, new_e, np.r_[w*.5, .25, .25], removed, added


def _snapshot(x, e, w, nu, generation, stage, source, removed, transfer_removed,
              discarded, production=(0., 0.)):
    inside, outside = w @ x, nu * (w @ e)
    balance = MOIETIES @ (source-removed-inside-outside)
    row = dict(generation=generation, stage=stage, cohorts=len(w),
               yield_percent=reporter(x, w),
               reporter_denominator_inside_uM=float(inside[1]+inside[4]),
               competent_inside_uM=float(inside[3]), competent_outside_uM=float(outside[3]),
               founder_inside_uM=float(inside[6]), founder_outside_uM=float(outside[6]),
               newly_generated_competent_inside_uM=float(max(0, inside[3]-inside[6])),
               newly_generated_competent_outside_uM=float(max(0, outside[3]-outside[6])),
               new_reporter_inside_uM=float(production[0]),
               new_reporter_outside_uM=float(production[1]),
               moiety_balance_max_error_uM=float(np.max(np.abs(balance))))
    for label, values in (("inside", inside), ("outside", outside),
                          ("outside_concentration", w @ e), ("source", source),
                          ("removed", removed), ("transfer_removed", transfer_removed),
                          ("discarded", discarded)):
        row.update({f"{label}_{name}_uM": float(v) for name, v in zip(NAMES, values)})
    for label, values in (("source", source), ("removed", removed),
                          ("retained", inside+outside)):
        row.update({f"{label}_moiety_{i+1}_uM": float(v)
                    for i, v in enumerate(MOIETIES @ values)})
    return row


def _simulate(seed, family, params, generations, cycles, exterior_reactive,
              exterior_carried, rtol):
    nu = _parameters(family, params)
    generations, cycles = _count(generations, "Generations"), _count(cycles, "FT count")
    if not all(isinstance(flag, bool) for flag in (exterior_reactive, exterior_carried)):
        raise ValueError("Exterior scenario switches must be booleans")
    if not np.isfinite(rtol) or not 0 < rtol < 1:
        raise ValueError("Relative tolerance must lie in (0,1)")
    x, e, w = initial(seed)
    source = w @ x
    removed, transfer_removed, discarded = (np.zeros(len(NAMES)) for _ in range(3))
    rows, stages = [], []

    def append(g, stage, production=(0., 0.)):
        row = _snapshot(x, e, w, nu, g, stage, source, removed,
                        transfer_removed, discarded, production)
        stages.append(row)
        return row

    rows.append(append(0, "initial"))
    for g in range(1, generations+1):
        if g > 1:
            x, e, w, lost, added = feed(x, e, w, nu)
            source += added
            removed += lost
            transfer_removed += lost
            append(g, "feed")
        x, e, lost = exchange(x, e, w, family, params, cycles)
        removed += lost
        append(g, "exchange")
        # shortcut: warm resuspension homogenizes exterior; resolve when measured.
        e = np.broadcast_to(w @ e, e.shape).copy()
        append(g, "warm_start")
        before_inside, before_outside = (w @ x)[4], nu*(w @ e)[4]
        x = react(x, 60, rtol)
        if exterior_reactive and nu:
            exterior_reacted = react(e[:1], 60, rtol)[0]
            e = np.broadcast_to(exterior_reacted, e.shape).copy()
        production = ((w @ x)[4]-before_inside, nu*(w @ e)[4]-before_outside)
        rows.append(append(g, "measurement", production))
        if not exterior_carried and nu:
            lost = nu*(w @ e)
            discarded += lost
            removed += lost
            e = np.zeros_like(e)
            append(g, "discard")
    return rows, stages


def single_cycle(seed, family, params, cycles, *, exterior_reactive=True,
                 exterior_carried=True, rtol=1e-8):
    """Figure 2 observer after the specified FT count and one warm interval."""
    rows, _ = _simulate(seed, family, params, 1, cycles, exterior_reactive,
                        exterior_carried, rtol)
    return rows[-1]


def serial(seed, family, params, generations=7, *, exterior_reactive=True,
           exterior_carried=True, rtol=1e-8, return_stages=False):
    """G0..Gn observations; exterior discard, if requested, follows each sample."""
    if not isinstance(return_stages, bool):
        raise ValueError("return_stages must be boolean")
    rows, stages = _simulate(seed, family, params, generations, 3,
                             exterior_reactive, exterior_carried, rtol)
    return (rows, stages) if return_stages else rows
