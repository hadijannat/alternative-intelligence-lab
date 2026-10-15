"""Reduced RNA reaction hypotheses; concentrations µM and time minutes."""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

NAMES = ("HyperA", "Cy5A", "B", "F1", "Cy5F1", "inactive_F1", "complex_AB", "complex_RB")
MOIETIES = np.array([[1, 0, 0, 1, 0, 1, 1, 0],
                     [0, 1, 0, 0, 1, 0, 0, 1],
                     [0, 0, 1, 1, 1, 1, 1, 1]], float)


@dataclass(frozen=True)
class Parameters:
    kf: float = .1
    kh: float = 1e-5
    kb: float = 1.
    ka: float | None = None
    krh: float = 0.
    kd: float = 0.
    kon: float = 0.
    koff: float = 0.
    equilibrated: bool = False
    mixing: float = .1
    transport: str = "fractional"
    retention_f: float = .55
    retention_fragments: float = .55

    def __post_init__(self):
        rates_ = (self.kf, self.kh, self.krh, self.kd, self.kon, self.koff)
        if self.ka is not None:
            rates_ += (self.ka,)
        if not all(np.isfinite(v) and v >= 0 for v in rates_):
            raise ValueError("Rate constants must be finite and nonnegative")
        if not np.isfinite(self.kb) or self.kb <= 0:
            raise ValueError("B saturation constant must be positive and finite")
        if not isinstance(self.equilibrated, bool) or (self.equilibrated and (self.kon <= 0 or self.koff <= 0)):
            raise ValueError("Equilibrated initialization requires positive binding and unbinding rates")
        if self.transport not in ("fractional", "contact"):
            raise ValueError("Unknown transport")
        if not np.isfinite(self.mixing) or not 0 <= self.mixing <= 1:
            raise ValueError("Mixing must lie in [0,1]")
        if not all(np.isfinite(v) and 0 < v <= 1 for v in (self.retention_f, self.retention_fragments)):
            raise ValueError("Retention must lie in (0,1]")


def rates(x, p):
    a, r, b, f, _, _, _, _ = np.maximum(np.asarray(x), 0).T
    occupancy = b / (p.kb + b)
    ka = p.kf if p.ka is None else p.ka
    # shortcut: effective assembly rates; replace when binding intermediates are measured.
    return (ka*f*a*occupancy + p.kh*a*a*occupancy**2,
            p.kf*f*r*occupancy + p.krh*a*r*occupancy**2)


def chemical_states(states):
    states = np.asarray(states, dtype=float)
    if states.ndim != 2 or states.shape[1] != 8 or len(states) == 0 or np.any(~np.isfinite(states)) or np.any(states < 0):
        raise ValueError("Expected finite nonnegative cohort-by-eight chemical states")
    return states


def react(states, minutes, p, regeneration=True, rtol=1e-8, times=None):
    states = chemical_states(states)
    if not np.isfinite(minutes) or minutes < 0:
        raise ValueError("Invalid reaction duration")
    if not np.isfinite(rtol) or not 0 < rtol < 1:
        raise ValueError("Invalid relative tolerance")
    if times is not None:
        times = np.asarray(times, dtype=float)
        if times.ndim != 1 or times.size == 0 or np.any(~np.isfinite(times)) or np.any(np.diff(times) <= 0) or times[0] < 0 or times[-1] > minutes:
            raise ValueError("Observation times must increase within reaction interval")
    if minutes == 0:
        return states[None, :, :].copy() if times is not None else states.copy()
    shape = states.shape

    def rhs(t, flat):
        state = np.maximum(flat.reshape(shape), 0)
        a, r, b, f, _, _, ca, cr = state.T
        va, vr = rates(state, p)
        trap_a, trap_r = p.kon*a*b-p.koff*ca, p.kon*r*b-p.koff*cr
        decay = p.kd*f
        return np.stack((-va-trap_a, -vr-trap_r, -va-vr-trap_a-trap_r,
                         (va if regeneration else 0)-decay, vr,
                         decay+(0 if regeneration else va), trap_a, trap_r), axis=1).ravel()

    sol = solve_ivp(rhs, (0, float(minutes)), states.ravel(), t_eval=times,
                    rtol=rtol, atol=rtol*1e-2, method="LSODA")
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.min(sol.y) < -1e-6:
        raise ArithmeticError("Negative chemical concentration")
    result = sol.y.T.reshape((-1, *shape)) if times is not None else sol.y[:, -1].reshape(shape)
    return np.maximum(result, 0)


def bulk_curves(p, seeds, hypers, times=(0, 15, 30, 45, 60)):
    seeds, hypers, times = np.asarray(seeds, float), np.asarray(hypers, float), np.asarray(times, float)
    if seeds.ndim != 1 or seeds.size == 0 or hypers.shape != seeds.shape:
        raise ValueError("Seeds and Hyper doses must be nonempty paired vectors")
    if times.ndim != 1 or times.size == 0:
        raise ValueError("Observation times must be a nonempty vector")
    x = np.zeros((len(seeds), 8))
    x[:, 0], x[:, 1], x[:, 2], x[:, 3] = hypers, 5, 7.5, seeds
    x = initial_complexes(x, p)
    y = react(x, float(np.max(times)), p, times=times)
    return (100*y[:, :, 4]/(y[:, :, 1]+y[:, :, 4]+y[:, :, 7])).T


def bulk_curve(p, seed=0., hyper=0., times=(0, 15, 30, 45, 60)):
    return bulk_curves(p, [seed], [hyper], times)[0]


def initial_complexes(states, p):
    x = chemical_states(states).copy()
    if p.equilibrated:
        a, r, b = x[:, 0]+x[:, 6], x[:, 1]+x[:, 7], x[:, 2]+x[:, 6]+x[:, 7]
        kd = p.koff/p.kon
        c = kd+a+r-b
        root = np.sqrt(c*c+4*b*kd)
        free_b = np.empty_like(b)
        positive = c >= 0
        free_b[positive] = 2*b[positive]*kd/(root[positive]+c[positive])
        free_b[~positive] = (root[~positive]-c[~positive])/2
        bound = free_b/(kd+free_b)
        x[:, 6], x[:, 7] = a*bound, r*bound
        x[:, 0], x[:, 1], x[:, 2] = a-x[:, 6], r-x[:, 7], free_b
    return x


def fresh(p):
    return initial_complexes([[10, 2.5, 0, 0, 0, 0, 0, 0], [0, 0, 15, 0, 0, 0, 0, 0]], p)


def initial(seed, p):
    if not np.isfinite(seed) or seed < 0:
        raise ValueError("Invalid founder concentration")
    return np.vstack((np.array([[0, 0, 0, seed, 0, 0, 0, 0]], float), fresh(p))), np.ones(3)/3


def cohort_weights(x, w):
    w = np.asarray(w, float)
    if w.shape != (len(x),) or np.any(~np.isfinite(w)) or np.any(w < 0) or not np.isclose(w.sum(), 1):
        raise ValueError("Cohort weights must be finite, nonnegative and sum to one")
    return w


def exchange(x, w, p, n):
    if not np.isfinite(n) or n < 0 or int(n) != n:
        raise ValueError("FT count must be a nonnegative integer")
    x = chemical_states(x).copy()
    w = cohort_weights(x, w).copy()
    before = w@x
    # shortcut: complex retention is set to fragment retention until measured directly.
    retention = np.full(8, p.retention_fragments**(1/3))
    retention[[3, 5]] = p.retention_f**(1/3)
    for _ in range(int(n)):
        mean = w@x
        if p.transport == "fractional":
            x = (1-p.mixing)*x+p.mixing*mean[None, :]
        elif p.mixing > 0:
            x = np.vstack((x, mean))
            w = np.append(w*(1-p.mixing), p.mixing)
            keep = w > 0
            x, w = x[keep], w[keep]
        x *= retention
    return x, w, before-w@x


def reporter(x, w):
    x = chemical_states(x)
    inventory = cohort_weights(x, w)@x
    total = inventory[1]+inventory[4]+inventory[7]
    return float(100*inventory[4]/total) if total > 0 else 0.


def single_cycle(p, seed, n, regeneration=True, rtol=1e-8):
    x, w = initial(seed, p)
    x, w, _ = exchange(x, w, p, n)
    return reporter(react(x, 60, p, regeneration, rtol), w)


def serial(p, seed, generations=7, regeneration=True, rtol=1e-8):
    if not np.isfinite(generations) or generations < 0 or int(generations) != generations:
        raise ValueError("Generations must be a nonnegative integer")
    x, w = initial(seed, p)
    source, removed, rows = w@x, np.zeros(8), []

    def append(g):
        inventory = w@x
        founder = seed/3 if g == 0 else seed/3*p.retention_f**g*.5**(g-1)*np.exp(-60*p.kd*g)
        rows.append(dict(generation=g, yield_percent=reporter(x, w),
                         **{name+"_uM": float(value) for name, value in zip(NAMES, inventory)},
                         founder_F1_model_uM=founder,
                         newly_generated_F1_model_uM=float(max(0, inventory[3]-founder)),
                         moiety_balance_max_error_uM=float(np.max(np.abs(MOIETIES@(source-removed-inventory)))),
                         source_moiety_uM=(MOIETIES@source).tolist(),
                         removed_moiety_uM=(MOIETIES@removed).tolist(),
                         retained_moiety_uM=(MOIETIES@inventory).tolist(), cohorts=len(w)))

    append(0)
    for g in range(1, int(generations)+1):
        if g > 1:
            removed += .5*(w@x)
            w *= .5
            added = fresh(p)
            source += .25*added.sum(axis=0)
            x, w = np.vstack((x, added)), np.concatenate((w, [.25, .25]))
        x, w, lost = exchange(x, w, p, 3)
        removed += lost
        x = react(x, 60, p, regeneration, rtol)
        append(g)
    return rows
