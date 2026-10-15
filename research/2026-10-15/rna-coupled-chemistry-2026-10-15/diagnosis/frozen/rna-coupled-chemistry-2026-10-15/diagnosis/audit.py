"""Fixed-parameter channel audit of the preceding failed transport model."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

import numpy as np
from scipy.integrate import simpson, solve_ivp

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
PRIOR = WORKSPACE / 'rna-seed-transport-2026-10-15'
CHANNELS = ('va', 'vr', 'vh', 'vp', 'decay')
CASES = ('reference', 'inert_exterior', 'discard_exterior', 'no_active_background',
         'no_direct_background', 'no_background')


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def csv_save(path, rows):
    with path.open('w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def rates(z, p):
    a, r, b, f, _, _ = z.T
    s = b / (p['kb'] + b)
    return np.stack((p['ka']*f*a*s, p['kf']*f*r*s,
                     p['kh']*a*a*s*s, p['krh']*a*r*s*s,
                     p['kd']*f), axis=-1)


def reaction(x, p, w, rtol, spacing):
    n = len(x)
    y0 = np.column_stack((x[:, :6], np.zeros((n, 5))))

    def rhs(t, flat):
        z = np.maximum(flat.reshape(n, 11)[:, :6], 0)
        q = rates(z, p)
        va, vr, vh, vp, d = q.T
        chemistry = np.stack((-va-vh, -vr-vp, -va-vh-vr-vp,
                              va+vh-d, vr+vp, d), axis=-1)
        return np.column_stack((chemistry, q)).ravel()

    sol = solve_ivp(rhs, (0, 60), y0.ravel(), method='DOP853',
                    rtol=rtol, atol=rtol*.01, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    end = sol.y[:, -1].reshape(n, 11)
    times = np.linspace(0, 60, int(60/spacing)+1)
    grid = sol.sol(times).reshape(n, 11, -1)[:, :6].transpose(2, 0, 1)
    if min(np.min(end[:, :6]), np.min(grid)) < -1e-8:
        raise ArithmeticError('Negative state')
    qgrid = np.array([rates(z, p) for z in grid])
    quadrature = simpson(qgrid, x=times, axis=0)
    extents = w @ end[:, 6:]
    mean_grid = np.einsum('i,tij->tj', w, grid)
    mean_rate_integral = simpson(rates(mean_grid, p), x=times, axis=0)
    s = grid[:, :, 2] / (p['kb'] + grid[:, :, 2])
    exposures = np.stack((grid[:, :, 0]*s,
                          grid[:, :, 0]**2*s**2,
                          grid[:, :, 0]*grid[:, :, 1]*s**2), axis=-1)
    exposures = simpson(np.einsum('i,tij->tj', w, exposures), x=times, axis=0)
    details = {'quadrature_max_error_uM': float(np.max(np.abs(quadrature-end[:, 6:]))),
               'mean_rate_vh_extent_uM': float(mean_rate_integral[2]),
               'A_s_exposure_uM_min': float(exposures[0]),
               'A2_s2_exposure_uM2_min': float(exposures[1]),
               'AR_s2_exposure_uM2_min': float(exposures[2])}
    for i, key in ((0, 'A'), (1, 'R'), (2, 'B'), (3, 'F')):
        details[f'{key}_min_uM'] = float(grid[:, :, i].min())
        details[f'{key}_max_uM'] = float(grid[:, :, i].max())
        details[f'{key}_warm_start_max_uM'] = float(grid[0, :, i].max())
    details['A_above_2p5_weighted_minutes'] = float(simpson(
        np.einsum('i,ti->t', w, grid[:, :, 0] > 2.5), x=times))
    result = np.column_stack((np.maximum(end[:, :6], 0),
                              x[:, 6]*np.exp(-p['kd']*60)))
    return result, extents, details


def simulate(model, family, params, case, seed, rtol, spacing):
    p = model.CHEMISTRY.copy()
    if case in ('no_active_background', 'no_background'):
        p['kh'] = 0.
    if case in ('no_direct_background', 'no_background'):
        p['krh'] = 0.
    nu = params.get('nu', 0.)
    x, e, w = model.initial(seed)
    source, removed = w @ x, np.zeros(7)
    rows = []
    for g in range(1, 8):
        if g > 1:
            x, e, w, lost, added = model.feed(x, e, w, nu)
            source += added
            removed += lost
        before = w @ x
        pre_total = before + nu*(w @ e)
        x, e, lost = model.exchange(x, e, w, family, params, 3)
        removed += lost
        after = w @ x
        e = np.broadcast_to(w @ e, e.shape).copy()
        start_inside, start_outside = w @ x, nu*(w @ e)
        x, qi, di = reaction(x, p, w, rtol, spacing)
        qo, de = np.zeros(5), None
        if nu and case != 'inert_exterior':
            eo, q, de = reaction(e[:1], p, np.ones(1), rtol, spacing)
            e = np.broadcast_to(eo[0], e.shape).copy()
            qo = nu*q
        elif nu:
            # Frozen chemistry still has a nonzero extracellular substrate pool.
            de = dict.fromkeys(di, 0.)
            a, r, b, f = e[0, :4]
            s = b/(p['kb']+b)
            de.update(A_s_exposure_uM_min=60*a*s,
                      A2_s2_exposure_uM2_min=60*a*a*s*s,
                      AR_s2_exposure_uM2_min=60*a*r*s*s,
                      A_above_2p5_weighted_minutes=60.*(a>2.5))
            for name, value in zip(('A', 'R', 'B', 'F'), (a, r, b, f)):
                for suffix in ('min_uM', 'max_uM', 'warm_start_max_uM'):
                    de[f'{name}_{suffix}'] = float(value)
        inside, outside = w @ x, nu*(w @ e)
        residual = float(np.max(np.abs(model.MOIETIES @ (source-removed-inside-outside))))
        row = dict(family=family, case=case, seed_uM=seed, generation=g,
                   yield_percent=model.reporter(x, w),
                   mass_error_uM=residual,
                   chemical_balance_error_uM=float(max(
                       abs(inside[3]-start_inside[3]-(qi[0]+qi[2]-qi[4])),
                       abs(inside[4]-start_inside[4]-(qi[1]+qi[3])),
                       abs(outside[3]-start_outside[3]-(qo[0]+qo[2]-qo[4])),
                       abs(outside[4]-start_outside[4]-(qo[1]+qo[3])))))
        for j, name in enumerate(model.NAMES):
            row[f'inside_{name}_uM'] = float(inside[j])
            row[f'outside_{name}_inventory_uM'] = float(outside[j])
            row[f'pre_exchange_total_{name}_uM'] = float(pre_total[j])
            row[f'exchange_net_inside_{name}_uM'] = float(after[j]-before[j])
        for label, q in (('inside', qi), ('outside', qo)):
            row.update({f'{label}_{channel}_extent_uM': float(value)
                        for channel, value in zip(CHANNELS, q)})
        for label, detail in (('inside', di), ('outside', de)):
            row.update({f'{label}_{key}': value if detail else 0.
                        for key, value in (detail or dict.fromkeys(di, 0.)).items()})
        row['reporter_denominator_uM'] = float(inside[1]+inside[4])
        rows.append(row)
        if case == 'discard_exterior' and nu:
            removed += nu*(w @ e)
            e = np.zeros_like(e)
    return rows


def main():
    if (HERE / 'verification.json').exists():
        raise FileExistsError('Preserve the existing completed diagnostic')
    inputs = [PRIOR/'model.py', PRIOR/'results-v1/fits.json',
              WORKSPACE/'measured-coupling-2026-10-15/rna_sources/observations.csv',
              WORKSPACE/'measured-coupling-2026-10-15/rna_sources/raw/salibi.txt',
              WORKSPACE/'measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt',
              HERE/'PROTOCOL.md', Path(__file__).resolve()]
    hashes = {str(p.relative_to(WORKSPACE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in inputs}
    save(HERE/'input_hashes.json', hashes)
    frozen = HERE/'frozen'
    frozen.mkdir(exist_ok=True)
    for path in inputs:
        target = frozen/path.relative_to(WORKSPACE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    spec = importlib.util.spec_from_file_location('prior_transport', PRIOR/'model.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    fits = json.loads((PRIOR/'results-v1/fits.json').read_text())
    standard, refined = [], []
    for tolerance, spacing, output in ((1e-9, .25, standard), (1e-11, .125, refined)):
        for family in ('legacy', 'bath', 'patch'):
            for case in CASES:
                for seed in (0, 2):
                    output.extend(simulate(model, family, fits[family]['parameters'],
                                           case, seed, tolerance, spacing))
    csv_save(HERE/'diagnostics.csv', standard)
    csv_save(HERE/'refined_diagnostics.csv', refined)
    max_reference = 0.
    for family in ('legacy', 'bath', 'patch'):
        for seed in (0, 2):
            expected = model.serial(seed, family, fits[family]['parameters'])
            actual = [r for r in standard if r['family']==family and
                      r['case']=='reference' and r['seed_uM']==seed]
            max_reference = max(max_reference, max(abs(r['yield_percent']-
                                expected[r['generation']]['yield_percent']) for r in actual))
    checks = {'rows': len(standard), 'paths': len(standard)//7,
              'max_mass_error_uM': max(r['mass_error_uM'] for r in standard+refined),
              'max_chemical_balance_error_uM': max(r['chemical_balance_error_uM'] for r in standard+refined),
              'max_quadrature_error_uM': max(r[f'{side}_quadrature_max_error_uM']
                    for r in standard+refined for side in ('inside', 'outside')),
              'max_refined_yield_difference_pp': max(abs(a['yield_percent']-b['yield_percent'])
                                             for a, b in zip(standard, refined)),
              'max_reference_yield_difference_pp': max_reference,
              'source_hashes_unchanged': all(hashlib.sha256((WORKSPACE/name).read_bytes()).hexdigest()==digest
                                           for name, digest in hashes.items())}
    checks['passed'] = (checks['rows']==252 and checks['max_mass_error_uM']<1e-7 and
        checks['max_chemical_balance_error_uM']<1e-7 and checks['max_quadrature_error_uM']<1e-7 and
        checks['max_refined_yield_difference_pp']<1e-5 and max_reference<1e-5 and checks['source_hashes_unchanged'])
    save(HERE/'verification.json', checks)
    print(json.dumps(checks, indent=2))
    if not checks['passed']:
        raise AssertionError('Diagnostic numerical qualification failed')


if __name__ == '__main__':
    main()
