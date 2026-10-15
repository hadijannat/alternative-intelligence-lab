"""Synthetic calibrated observer. All quantities refer to original-sample fmol."""
import copy
import math

SPECIES = ('founder', 'new', 'hyper', 'reporter', 'imported')
MODES = ('native', 'refolded')

def calibration():
    return dict(recovery=.5, identity_fraction=.5, capacity_fraction=.25,
                loq=1., relative_margin=.25, cross_upper=.001,
                founder_specific_upper=1.1, new_specific_upper=1.1,
                hyper_upper=.15, reporter_upper=.02, imported_upper=1.1,
                label_qualified=True, mixture_qualified=True,
                recovery_qualified=True, native_qualified=True)

def observe(amounts, capacities, rng, calibration=None, *, volume_pl=1., qualified=True):
    """Generate synthetic measurements; inference sees no hidden state."""
    c = globals()['calibration']() if calibration is None else copy.deepcopy(calibration)
    if volume_pl <= 0 or not math.isfinite(volume_pl):
        raise ValueError('positive finite volume required')
    values = {k: float(amounts.get(k, 0.)) for k in SPECIES}
    values.update({k: float(capacities[k]) for k in MODES})
    if any(not math.isfinite(v) or v < 0 for v in values.values()):
        raise ValueError('nonnegative finite amounts/capacities required')
    numeric=('recovery','loq','identity_fraction','capacity_fraction','relative_margin','cross_upper','founder_specific_upper','new_specific_upper','hyper_upper','reporter_upper','imported_upper')
    if any(not math.isfinite(c[k]) or c[k]<0 for k in numeric):
        raise ValueError('finite nonnegative calibration required')
    if not 0 < c['recovery'] <= 1 or c['loq'] <= 0 or not 0<c['relative_margin']<1:
        raise ValueError('invalid recovery or LOQ')
    if min(c['identity_fraction'],c['capacity_fraction'])<=0 or c['identity_fraction']+2*c['capacity_fraction']>1:
        raise ValueError('aliquots exceed available material or are empty')
    shared = c.pop('_shared_response', float(rng.normal(0,.03)))
    rec_error = c.pop('_shared_recovery', float(rng.normal(0,.05)))
    measured_recovery = c['recovery'] * (1+rec_error)
    if measured_recovery <= 0:
        raise ValueError('invalid simulated standard recovery')
    signals = {}
    for key, value in values.items():
        split = c['identity_fraction'] if key in SPECIES else c['capacity_fraction']
        response = c['recovery']*split
        raw = value*response*(1+shared)*(1+float(rng.normal(0,.03))) + c['cross_upper']*.5
        signals[key] = dict(raw=raw, response=measured_recovery*split,
                            censored=raw<c['loq'])
    return dict(signals=signals, calibration=c, qualified=bool(qualified), volume_pl=volume_pl)

def infer(observation):
    c = observation['calibration']
    reasons = [k for k in ('label_qualified','mixture_qualified','recovery_qualified') if not c[k]]
    if not observation['qualified']:
        reasons.append('external qualification failed')
    intervals = {}
    for key, signal in observation['signals'].items():
        lo, hi = (0., c['loq']) if signal['censored'] else (signal['raw'], signal['raw'])
        intervals[key] = [max(0.,lo-c['cross_upper'])/signal['response']/(1+c['relative_margin']),
                          max(0.,hi)/signal['response']/(1-c['relative_margin'])]
    nuisance = (intervals['founder'][1]*c['founder_specific_upper']+
                intervals['hyper'][1]*c['hyper_upper']+
                intervals['reporter'][1]*c['reporter_upper']+
                intervals['imported'][1]*c['imported_upper'])
    lower, upper, status, mode_reasons = {}, {}, {}, {}
    for mode in MODES:
        admitted = not reasons and (mode!='native' or c['native_qualified'])
        lower[mode] = max(0.,intervals[mode][0]-nuisance) if admitted else 0.
        upper[mode] = min(intervals[mode][1],intervals['new'][1]*c['new_specific_upper']) if admitted else None
        mode_reasons[mode]=list(reasons)
        if mode=='native' and not c['native_qualified']:
            mode_reasons[mode].append('native recovery unqualified')
        if admitted and lower[mode]>upper[mode]:
            admitted=False
            mode_reasons[mode].append('inconsistent capacity and identity intervals')
            lower[mode]=0.;upper[mode]=None
        threshold = c['loq']/observation['signals'][mode]['response']
        status[mode] = 'detected' if admitted and not observation['signals']['new']['censored'] and lower[mode]>threshold else 'unresolved'
    return dict(intervals=intervals,new_capacity_lower=lower,new_capacity_upper=upper,
                status=status,qualified=not reasons,reasons=reasons,
                nuisance_upper=nuisance,mode_reasons=mode_reasons)

def ratio_interval(numerator, denominator):
    return [numerator[0]/denominator[1], numerator[1]/denominator[0]] if denominator[0]>0 else None

def material_budget(diameter_um, concentration_um=1.):
    volume = math.pi*diameter_um**3/6000
    return dict(volume_pl=volume,amount_fmol=concentration_um*volume*.001)

def wilson(successes, n):
    z=1.959963984540054
    p=successes/n
    center=(p+z*z/(2*n))/(1+z*z/n)
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [max(0.,center-half),min(1.,center+half)]
