"""RNA turnover hypotheses; concentrations µM and time minutes.

Shared binding/release rates for competent, inactive and reporter strands are an
unmeasured affinity closure. Complexes occupy both strands until release.
"""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

NAMES = ("A", "R", "B", "F", "P", "D", "QFF", "QFP", "QFD", "QDD", "QDP", "QPP")
MOIETIES = np.array([[1, 0, 0, 1, 0, 1, 2, 1, 2, 2, 1, 0],
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2],
                    [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]], float)


@dataclass(frozen=True)
class Parameters:
    kf: float = .1
    kh: float = 1e-5
    kb: float = 1.
    ka: float | None = None
    krh: float = 0.
    kd: float = 0.
    turnover: bool = False
    krel: float = 0.
    kbind: float = 0.
    equilibrated: bool = False
    mixing: float = .1
    transport: str = "fractional"
    loss: str = "uniform"
    complex_reset: bool = False
    retention_f: float = .55
    retention_fragments: float = .55

    def __post_init__(self):
        values = (self.kf, self.kh, self.krh, self.kd, self.krel, self.kbind)
        if self.ka is not None:
            values += (self.ka,)
        if not all(np.isfinite(v) and v >= 0 for v in values):
            raise ValueError("Rate constants must be finite and nonnegative")
        if not np.isfinite(self.kb) or self.kb <= 0:
            raise ValueError("B saturation constant must be positive and finite")
        if not all(isinstance(v, bool) for v in (self.turnover, self.equilibrated, self.complex_reset)):
            raise ValueError("Model switches must be booleans")
        if self.equilibrated and (self.kbind <= 0 or self.krel <= 0):
            raise ValueError("Equilibrated initialization requires positive binding and release rates")
        if self.transport not in ("fractional", "contact") or self.loss not in ("uniform", "all_or_none"):
            raise ValueError("Unknown transport or loss closure")
        if not np.isfinite(self.mixing) or not 0 <= self.mixing <= 1:
            raise ValueError("Mixing must lie in [0,1]")
        if not all(np.isfinite(v) and 0 < v <= 1 for v in (self.retention_f, self.retention_fragments)):
            raise ValueError("Retention must lie in (0,1]")
        if self.retention_f != self.retention_fragments:
            raise ValueError("Differential retention is unsupported for mixed-strand complexes")


def _ligation_rates(x, p):
    a, r, b, f = np.maximum(np.asarray(x), 0).T[:4]
    occupancy = b / (p.kb + b)
    ka = p.kf if p.ka is None else p.ka
    # shortcut: effective ligation rates; replace when intermediates are measured.
    return (ka*f*a*occupancy, p.kf*f*r*occupancy,
            p.kh*a*a*occupancy**2, p.krh*a*r*occupancy**2)


def rates(x, p):
    va, vr, vi, vp = _ligation_rates(x, p)
    return va+vi, vr+vp


def chemical_states(states):
    states = np.asarray(states, dtype=float)
    if states.ndim != 2 or states.shape[1] != len(NAMES) or len(states) == 0 or np.any(~np.isfinite(states)) or np.any(states < 0):
        raise ValueError("Expected finite nonnegative cohort-by-twelve chemical states")
    return states


def competent_inventory(states):
    x = np.asarray(states)
    return x[..., 3]+2*x[..., 6]+x[..., 7]+x[..., 8]


def reporter_product(states):
    x = np.asarray(states)
    return x[..., 4]+x[..., 7]+x[..., 10]+2*x[..., 11]


def dissociate_complexes(states):
    x = chemical_states(states).copy()
    x[:, 3] = competent_inventory(x)
    x[:, 4] = reporter_product(x)
    x[:, 5] += x[:, 8]+2*x[:, 9]+x[:, 10]
    x[:, 6:] = 0
    return x


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
        x = np.maximum(flat.reshape(shape), 0)
        f, product, inactive = x[:, 3:6].T
        va, vr, vi, vp = _ligation_rates(x, p)
        d = np.zeros_like(x)
        d[:, 0], d[:, 1], d[:, 2] = -va-vi, -vr-vp, -va-vi-vr-vp
        if p.turnover:
            d[:, 3] = -va-vr+(vi if regeneration else 0)
            d[:, 4], d[:, 5] = vp, 0 if regeneration else vi
            d[:, 6 if regeneration else 8] = va
            d[:, 7] = vr
        else:
            d[:, 3] = va+vi if regeneration else 0
            d[:, 4], d[:, 5] = vr+vp, 0 if regeneration else va+vi
        net = p.kbind*np.stack((.5*f*f, f*product, f*inactive,
                               .5*inactive*inactive, inactive*product, .5*product*product), axis=1)-p.krel*x[:, 6:]
        ff, fp, fd, dd, dp, pp = net.T
        d[:, 3] -= 2*ff+fp+fd
        d[:, 4] -= fp+dp+2*pp
        d[:, 5] -= fd+2*dd+dp
        d[:, 6:] += net
        decay_f, decay_ff, decay_fp, decay_fd = p.kd*x[:, [3, 6, 7, 8]].T
        d[:, 3] -= decay_f
        d[:, 5] += decay_f
        d[:, 6] -= 2*decay_ff
        d[:, 7] -= decay_fp
        d[:, 8] += 2*decay_ff-decay_fd
        d[:, 9] += decay_fd
        d[:, 10] += decay_fp
        return d.ravel()

    sol = solve_ivp(rhs, (0, float(minutes)), states.ravel(), t_eval=times,
                    rtol=rtol, atol=rtol*1e-2, method="LSODA")
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.min(sol.y) < -1e-6:
        raise ArithmeticError("Negative chemical concentration")
    result = sol.y.T.reshape((-1, *shape)) if times is not None else sol.y[:, -1].reshape(shape)
    return np.maximum(result, 0)


def bulk_curves(p, seeds, hypers, times=(0, 15, 30, 45, 60), rtol=1e-8):
    seeds, hypers, times = np.asarray(seeds, float), np.asarray(hypers, float), np.asarray(times, float)
    if seeds.ndim != 1 or seeds.size == 0 or hypers.shape != seeds.shape:
        raise ValueError("Seeds and Hyper doses must be nonempty paired vectors")
    if times.ndim != 1 or times.size == 0:
        raise ValueError("Observation times must be a nonempty vector")
    x = np.zeros((len(seeds), len(NAMES)))
    x[:, 0], x[:, 1], x[:, 2], x[:, 3] = hypers, 5, 7.5, seeds
    y = react(initial_complexes(x, p), float(np.max(times)), p, times=times, rtol=rtol)
    product = reporter_product(y)
    return (100*product/(y[:, :, 1]+product)).T


def bulk_curve(p, seed=0., hyper=0., times=(0, 15, 30, 45, 60), rtol=1e-8):
    return bulk_curves(p, [seed], [hyper], times, rtol)[0]


def initial_complexes(states, p):
    x = chemical_states(states).copy()
    if p.equilibrated:
        x = dissociate_complexes(x)
        total = x[:, 3:6].sum(axis=1)
        ratio = p.kbind/p.krel
        free_fraction = 2/(1+np.sqrt(1+4*ratio*total))
        x[:, 3:6] *= free_fraction[:, None]
        f, product, inactive = x[:, 3:6].T
        x[:, 6:] = ratio*np.stack((.5*f*f, f*product, f*inactive,
                                  .5*inactive*inactive, inactive*product, .5*product*product), axis=1)
    return x


def fresh(p):
    x = np.zeros((2, len(NAMES)))
    x[0, :2], x[1, 2] = [10, 2.5], 15
    return initial_complexes(x, p)


def initial(seed, p):
    if not np.isfinite(seed) or seed < 0:
        raise ValueError("Invalid founder concentration")
    founder = np.zeros((1, len(NAMES)))
    founder[0, 3] = seed
    return np.vstack((initial_complexes(founder, p), fresh(p))), np.ones(3)/3


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
    removed = np.zeros(len(NAMES))
    retention = p.retention_f**(1/3)
    for _ in range(int(n)):
        mean = w@x
        if p.transport == "fractional":
            x = (1-p.mixing)*x+p.mixing*mean[None, :]
        elif p.mixing > 0:
            x = np.vstack((x, mean))
            w = np.append(w*(1-p.mixing), p.mixing)
            keep = w > 0
            x, w = x[keep], w[keep]
        removed += (1-retention)*(w@x)
        if p.loss == "uniform":
            x *= retention
        else:
            w *= retention
            empty = np.all(x == 0, axis=1)
            empty_weight = w[empty].sum()+1-retention
            x = np.vstack((x[~empty], np.zeros(len(NAMES))))
            w = np.append(w[~empty], empty_weight)
        if p.complex_reset:
            x = dissociate_complexes(x)
    return x, w, removed


def reporter(x, w):
    x = chemical_states(x)
    inventory = cohort_weights(x, w)@x
    product = reporter_product(inventory)
    total = inventory[1]+product
    return float(100*product/total) if total > 0 else 0.


def single_cycle(p, seed, n, regeneration=True, rtol=1e-8):
    x, w = initial(seed, p)
    x, w, _ = exchange(x, w, p, n)
    return reporter(react(x, 60, p, regeneration, rtol), w)


def serial(p, seed, generations=7, regeneration=True, rtol=1e-8):
    if not np.isfinite(generations) or generations < 0 or int(generations) != generations:
        raise ValueError("Generations must be a nonnegative integer")
    x, w = initial(seed, p)
    source, removed, rows = w@x, np.zeros(len(NAMES)), []

    def append(g):
        inventory = w@x
        founder = seed/3 if g == 0 else seed/3*p.retention_f**g*.5**(g-1)*np.exp(-60*p.kd*g)
        competent = float(competent_inventory(inventory))
        rows.append(dict(generation=g, yield_percent=reporter(x, w),
                         **{name+"_uM": float(value) for name, value in zip(NAMES, inventory)},
                         competent_total_model_uM=competent,
                         founder_competent_model_uM=founder,
                         newly_generated_competent_model_uM=float(max(0, competent-founder)),
                         founder_tag_assumption="uniform_per_strand_hazard_and_uniform_material_retention",
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
