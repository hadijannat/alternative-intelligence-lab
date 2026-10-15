"""Effective C3 chemistry and explicitly hypothetical compartment transfer."""
import numpy as np
from scipy.integrate import solve_ivp

VOLUME = 50.0  # uL; mM * uL = nmol
Q = 0.84
AZIDE = 3.2


def total_product(time, k0, kcat, capacity=Q, seed=0.0):
    time = np.asarray(time, dtype=float)
    if min(k0, kcat, capacity, seed) < 0 or np.any(time < 0):
        raise ValueError("Nonnegative parameters and times required")
    a = k0 + kcat * seed
    decay = np.exp(-(a + kcat * capacity) * time)
    denominator = a + kcat * capacity * decay
    formed = np.divide(capacity * a * (1 - decay), denominator,
                       out=np.zeros_like(time), where=denominator > 0)
    return seed + formed


def initial(seed=0.0, localization=1.0):
    if seed < 0 or not 0 <= localization <= 1:
        raise ValueError("Invalid seed/localization")
    return np.array([Q * VOLUME, AZIDE * VOLUME,
                     seed * VOLUME * localization,
                     seed * VOLUME * (1 - localization), 0.0, 0.0])


def integrate(state, duration, k0, kcat, localization=1.0, escape=0.0,
              entry=0.0, active=1.0, regeneration=True, rtol=1e-9):
    state = np.asarray(state, dtype=float)
    if state.shape != (6,) or not np.all(np.isfinite(state)) or np.any(state < -1e-9):
        raise ValueError("Six finite nonnegative amounts required")
    if not (0 <= localization <= 1 and 0 <= active <= 1):
        raise ValueError("Fractions must lie in [0,1]")
    if not all(np.isfinite(x) and x >= 0 for x in (duration, k0, kcat, escape, entry)):
        raise ValueError("Finite nonnegative time/rates required")

    def rhs(_, y):
        # shortcut: pooled accessible substrate and phase-independent activity;
        # replace when active C3 transport and phase-specific rates are measured.
        available = max(0.0, min(y[0], y[1] / 3))
        rate = (k0 + kcat * active * sum(y[2:]) / VOLUME) * available if regeneration else 0.0
        old_exchange = entry * y[3] - escape * y[2]
        new_exchange = entry * y[5] - escape * y[4]
        return [-rate, -3 * rate, old_exchange, -old_exchange,
                localization * rate + new_exchange,
                (1 - localization) * rate - new_exchange]

    sol = solve_ivp(rhs, [0, duration], state, rtol=rtol, atol=rtol * 1e-2)
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.min(sol.y) < -1e-7:
        raise ArithmeticError("Negative chemical amount")
    return sol.y[:, -1]


def transfer(state, q, mode="selected"):
    """25 uL discarded/refilled; selective C3 recovery is a declared hypothesis."""
    state = np.asarray(state, dtype=float)
    if state.shape != (6,) or np.any(state < -1e-7) or not np.all(np.isfinite(state)):
        raise ValueError("Invalid chemical state")
    if not 0 <= q <= 1 or mode not in ("selected", "bulk", "pooled"):
        raise ValueError("Invalid transfer mode/fraction")
    kept = state * 0.5
    if mode == "selected":
        kept[2:] = state[2:] * [q, 0, q, 0]
    elif mode == "pooled":
        # Pooling destroys spatial labels, while old/new chemical labels survive.
        kept[2:4] = [0, (state[2] + state[3]) * 0.5]
        kept[4:6] = [0, (state[4] + state[5]) * 0.5]
    # For pooled mode, discarded inside/outside labels are undefined after mixing.
    discarded_totals = np.array([state[0]-kept[0], state[1]-kept[1],
                                 sum(state[2:4])-sum(kept[2:4]),
                                 sum(state[4:])-sum(kept[4:])])
    additions = np.array([Q * VOLUME - kept[0], AZIDE * VOLUME - kept[1]])
    if np.min(additions) < -1e-7:
        raise ValueError("Refill target requires negative feed")
    kept[:2] += additions
    return kept, discarded_totals, additions


def passages(k0, kcat, localization, q, escape, active, control="regeneration",
             mode="selected", seed=0.02, count=8, rtol=1e-9):
    if control not in ("regeneration", "baseline_only", "no_regeneration"):
        raise ValueError("Unknown control")
    state = initial(seed, localization)
    initial_state = state.copy()
    discarded = np.zeros(4)
    feed = np.zeros(2)
    rows = []
    for passage in range(1, count + 1):
        before = state.copy()
        end = integrate(state, 2.0, k0, 0 if control == "baseline_only" else kcat,
                        localization, escape, active=active,
                        regeneration=control != "no_regeneration", rtol=rtol)
        formed = sum(end[4:]) - sum(before[4:])
        state, removed, added = transfer(end, q, mode)
        discarded += removed
        feed += added
        new = active * sum(state[4:]) / VOLUME
        old = active * sum(state[2:4]) / VOLUME
        fraction = old / (old + new) if old + new > 0 else 1.0
        marginal = (kcat if control == "regeneration" else 0.0) * new * Q
        rows.append({"passage": passage, "newly_formed_nmol": formed,
                     "retained_founder_nmol": float(sum(state[2:4])),
                     "retained_new_nmol": float(sum(state[4:])),
                     "retained_active_new_mM": new, "founder_active_fraction": fraction,
                     "hypothetical_new_marginal_rate_mM_min": marginal,
                     "conditional_function_pass": bool(new >= 0.01 and marginal >= 0.01 and fraction <= .01),
                     "state_nmol": state.tolist(), "discarded_cumulative_nmol": discarded.tolist(),
                     "feed_cumulative_nmol": feed.tolist()})
    formed_total = sum(r["newly_formed_nmol"] for r in rows)
    balance = {
        "TPA_nmol": initial_state[0] + feed[0] - state[0] - discarded[0] - formed_total,
        "azide_nmol": initial_state[1] + feed[1] - state[1] - discarded[1] - 3 * formed_total,
        "founder_nmol": sum(initial_state[2:4]) - sum(state[2:4]) - discarded[2],
        "new_C3_nmol": formed_total - sum(state[4:]) - discarded[3],
        "prescribed_net_volume_change_uL": count * (25 - 25),
    }
    return rows, {k: float(v) for k, v in balance.items()}
