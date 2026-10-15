"""Independent five-state bulk check; no fitting or transport validation."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_ivp

import model

ROOT = Path(__file__).resolve().parent
TIMES = np.array([0., 15., 30., 45., 60.])
DOSES = [(s, 0.) for s in (.1, .25, .5, 1.)] + [(0., a) for a in (1., 1.5, 2., 2.5)]
FAMILIES = ("baseline", "release", "reversible_free", "reversible_equilibrium")
LABELS = ("PAGE_percent", "competent_uM", "free_F_uM", "total_dimers_uM", "full_length_uM")
LIMITS = np.array([1e-4, 1e-7, 1e-7, 1e-7, 1e-7])


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reduced(p, seed, hyper):
    # Common affinities close the total free-strand association flux at U=T-2Q.
    free = seed
    if p["equilibrated"]:
        free = 2*seed/(1+np.sqrt(1+4*p["kbind"]*seed/p["krel"]))
    initial = [0., seed, seed, free, (seed-free)/2]

    def rhs(t, y):
        ligated, total, competent, free_f, pairs = y
        a, r, b = hyper+seed-total+ligated, 5-ligated, 7.5+seed-total
        u, s = total-2*pairs, b/(p["kb"]+b)
        ka = p["kf"] if p["ka"] is None else p["ka"]
        va, vr = ka*free_f*a*s, p["kf"]*free_f*r*s
        vh, vp = p["kh"]*a*a*s*s, p["krh"]*a*r*s*s
        captured = va+vr if p["turnover"] else 0.
        free_gain = -va-vr+vh if p["turnover"] else va+vh
        return [vr+vp, va+vr+vh+vp, va+vh-p["kd"]*competent,
                free_gain-p["kbind"]*free_f*u+p["krel"]*(competent-free_f)-p["kd"]*free_f,
                captured+.5*p["kbind"]*u*u-p["krel"]*pairs]

    sol = solve_ivp(rhs, (0., 60.), initial, method="DOP853", t_eval=TIMES,
                    rtol=1e-10, atol=1e-12)
    assert sol.success, sol.message
    assert np.all(np.isfinite(sol.y)) and np.min(sol.y) >= -1e-8
    ligated, total, competent, free_f, pairs = sol.y
    assert np.min(total-2*pairs) >= -1e-8
    assert np.max(free_f-competent) <= 1e-8
    return np.column_stack((20*ligated, competent, free_f, pairs, total)), sol.nfev


def compare(name, parameters):
    p = model.Parameters(**parameters)
    x = np.zeros((len(DOSES), 12))
    x[:, 0], x[:, 1], x[:, 2], x[:, 3] = [d[1] for d in DOSES], 5., 7.5, [d[0] for d in DOSES]
    ref = model.react(model.initial_complexes(x, p), 60., p, times=TIMES, rtol=1e-10)
    l = ref[:, :, 4]+ref[:, :, 7]+ref[:, :, 10]+2*ref[:, :, 11]
    c = ref[:, :, 3]+2*ref[:, :, 6]+ref[:, :, 7]+ref[:, :, 8]
    q = ref[:, :, 6:].sum(axis=2)
    total = ref[:, :, 3:6].sum(axis=2)+2*q
    reference = np.stack((100*l/(ref[:, :, 1]+l), c, ref[:, :, 3], q, total), axis=2)
    rows = []
    for i, (seed, hyper) in enumerate(DOSES):
        independent, nfev = reduced(parameters, seed, hyper)
        errors = np.max(np.abs(independent-reference[:, i, :]), axis=0)
        rows.append(dict(seed_uM=seed, hyper_uM=hyper, independent=independent.tolist(),
                         reference=reference[:, i, :].tolist(), max_abs_errors=dict(zip(LABELS, errors.tolist())),
                         dop853_nfev=nfev, passed=bool(np.all(errors < LIMITS))))
    return dict(name=name, parameters=parameters, passed=all(r["passed"] for r in rows), doses=rows)


def main():
    source_paths = [Path(__file__).resolve(), ROOT/"model.py", ROOT/"PROTOCOL.md"]
    sources = {str(p): digest(p) for p in source_paths}
    synthetic = dict(kf=.3, ka=.2, kh=.001, krh=.003, kb=2., kd=.02,
                     turnover=True, krel=.1, kbind=0., equilibrated=False)
    cases = [("synthetic_release", synthetic),
             ("synthetic_rebinding_free", dict(synthetic, kbind=.4)),
             ("synthetic_rebinding_equilibrium", dict(synthetic, kbind=.4, equilibrated=True)),
             ("synthetic_baseline", dict(synthetic, turnover=False, krel=0.)),
             ("synthetic_zero_release", dict(synthetic, krel=0.))]
    fits, missing = {}, []
    for family in FAMILIES:
        path = ROOT/"results-v1"/"fits"/(family+"__omit-none.json")
        if not path.exists():
            missing.append(family)
            continue
        fit = json.loads(path.read_text())
        assert fit["complete"] and fit["resolved"], path
        fits[str(path)] = digest(path)
        cases.append(("full_fit_"+family, fit["parameters"]))
    results = [compare(name, parameters) for name, parameters in cases]
    unchanged = all(digest(Path(p)) == h for p, h in (sources | fits).items())
    passed = unchanged and all(r["passed"] for r in results)
    report = dict(status=("PASS" if not missing else "PARTIAL") if passed else "FAIL",
                  classification="Algebraic bulk chemistry verification; not fitting or physical validation",
                  source_sha256=sources, fit_sha256=fits, source_and_fit_hashes_unchanged=unchanged,
                  missing_full_fit_families=missing, times_min=TIMES.tolist(), observable_order=LABELS,
                  comparison_absolute_limits=dict(zip(LABELS, LIMITS.tolist())),
                  solvers={"independent": "DOP853", "reference": "LSODA", "rtol": 1e-10, "atol": 1e-12},
                  invocation="uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 python rna-turnover-tests-2026-10-15/reduction_check.py",
                  equations={"states": "L,T,C,F,Q; U=T-2Q; regeneration enabled",
                             "fragments": "A=a0+f0-T+L; R=5-L; B=7.5+f0-T; s=B/(KB+B)",
                             "rates": "va=ka*F*A*s; vr=kf*F*R*s; vh=kh*A^2*s^2; vp=krh*A*R*s^2",
                             "shared": "L'=vr+vp; T'=va+vr+vh+vp; C'=va+vh-kd*C",
                             "turnover": "Q'=va+vr+0.5*kbind*U^2-krel*Q; F'=-va-vr+vh-kbind*F*U+krel*(C-F)-kd*F",
                             "baseline": "Q'=0.5*kbind*U^2-krel*Q; F'=va+vh-kbind*F*U+krel*(C-F)-kd*F",
                             "initial": "L=0; T=C=f0; F=f0 (free) or 2*f0/(1+sqrt(1+4*kbind*f0/krel)); Q=(f0-F)/2"},
                  cases=results)
    output = ROOT/"reduction-verification.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    assert passed, output
    print(json.dumps({"status": report["status"], "cases": len(results), "missing": missing, "artifact": str(output)}))


if __name__ == "__main__":
    main()
