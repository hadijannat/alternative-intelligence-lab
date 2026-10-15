"""Finite molecule-accounted planning worlds; no calibrated kinetic constants."""
from pathlib import Path
import importlib.util
import numpy as np

_spec = importlib.util.spec_from_file_location('joint_f1_assay', Path(__file__).resolve().parents[1]/'assay/model.py')
assay = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(assay)
M = 6.02214076e8
SPECIES = ('founder_active','founder_inactive','older_new_active','older_new_inactive',
           'pulse_new_active','pulse_new_inactive','import_active','import_inactive',
           'A','B','R','reporter')
ACTIVE = (0,2,4,6)
WORLDS = ('strong','weak','founder_only','inactive_new','reporter_only',
          'common_feed','horizontal','shared_history_environment','no_founder')
PLATFORMS = ((.524,1.),(1000.,1.),(1000.,.01))
FIELDS = ('replicate','group','root','batch','generation','volume_pl','qualified',
          'new_lower','new_upper','state_lower','state_upper','detected',
          'true_current_active','true_founder_active','true_older_active','true_import_active',
          'founder_raw','new_raw','hyper_raw','reporter_raw','imported_raw','native_raw','refolded_raw',
          'identity_response','capacity_response','native_lower','native_upper',
          'true_native','true_total_f1','true_current_total','pedigree_valid','sample_recovered')

def moieties(x):
    f = x[...,:8].sum(axis=-1)
    return np.stack((x[...,8]+f,x[...,9]+f+x[...,11],x[...,10]+x[...,11]),axis=-1)

def partition(x, rng):
    fractions = rng.beta(20,20,x.shape[:-1])
    first = rng.binomial(x,fractions[...,None])
    daughters = np.stack((first,x-first),axis=-2).reshape(x.shape[0],-1,x.shape[-1])
    return daughters, np.stack((fractions,1-fractions),axis=-1).reshape(x.shape[0],-1)

def react(x, world, history, unit, rng):
    before = moieties(x)
    active = x[...,ACTIVE].sum(axis=-1)
    factor = {'strong':4.,'weak':.5,'inactive_new':4.,'horizontal':4.}.get(world,0.)
    expected = active*factor
    if world == 'common_feed':
        expected = np.full_like(active,unit,dtype=float)
    if world == 'shared_history_environment':
        expected = np.broadcast_to(np.where(history[:,None],2.,.1)*unit,active.shape)
    formed = np.minimum(np.minimum(x[...,8],x[...,9]),rng.poisson(expected))
    q = 0. if world in ('inactive_new','horizontal') else .9
    competent = rng.binomial(formed,q)
    x[...,4] += competent
    x[...,5] += formed-competent
    x[...,8] -= formed
    x[...,9] -= formed
    report = np.minimum(np.minimum(x[...,10],x[...,9]),rng.poisson(.1*active+.03*x[...,8]))
    x[...,10] -= report
    x[...,9] -= report
    x[...,11] += report
    assert np.array_equal(before,moieties(x)), 'ligation stoichiometry'

def simulate(world, volume, rng, n=96, pedigree=False):
    if world not in WORLDS or n%4 or n<8 or volume<=0:
        raise ValueError('registered world, positive volume and balanced n required')
    roots = 4*n
    group = np.repeat(np.arange(4),n)  # high intact, low intact, high reset, low reset
    history = np.isin(group,(0,2))
    batch = np.tile(np.repeat(np.arange(4),n//4),4)
    unit = volume*.001*M
    x = np.zeros((roots,1,12),dtype=np.int64)
    x[:,0,0] = np.rint(np.where(history,.4,.01)*unit).astype(np.int64)
    x[:,0,1] = round(unit)-x[:,0,0]
    initial = moieties(x).sum(axis=1)
    emitted = np.zeros_like(initial)
    supplied = np.zeros_like(initial)
    sampled = np.zeros_like(initial)
    reset = group>=2
    emitted[reset] += moieties(x[reset]).sum(axis=1)
    x[reset,0,0] = round(.01*unit)
    x[reset,0,1] = round(unit)-round(.01*unit)
    supplied[reset] += moieties(x[reset]).sum(axis=1)
    if world=='reporter_only':
        x[...,1] += x[...,0]
        x[...,0] = 0
    if world=='no_founder':
        emitted += moieties(x).sum(axis=1)
        x[...] = 0
    ids = np.ones((roots,1),dtype=np.int64)
    records = []
    chosen_roots = [0,n,2*n,3*n]
    if pedigree:
        for root in chosen_roots:
            records.append(dict(root=root,id=f'{root}:0:1',parent=None,generation=0,
                                volume_pl=volume,stock=x[root,0].tolist(),sampled=False,pulse=False))
    pools = {}
    for g in range(1,7):
        x[...,2:4] += x[...,4:6]
        x[...,4:6] = 0
        parent_ids = np.repeat(ids,2,axis=1)
        x, fractions = partition(x,rng)
        ids = parent_ids*2+np.tile([0,1],(roots,parent_ids.shape[1]//2))
        terminal = np.ones(x.shape[:2],dtype=bool) if g==6 else np.zeros(x.shape[:2],dtype=bool)
        if g==5:
            choice = rng.integers(0,2,(roots,x.shape[1]//2))
            terminal = np.stack((choice==0,choice==1),axis=-1).reshape(x.shape[:2])
        feed = np.zeros_like(x)
        feed[...,8:11] = np.rint(np.array([8.,12.,4.])*unit).astype(np.int64)
        if world=='horizontal':
            feed[...,6] = round(.5*unit)
        x += feed
        supplied += moieties(feed).sum(axis=1)
        retained = rng.binomial(x,.9)
        emitted += moieties(x-retained).sum(axis=1)
        x = retained
        for a in ACTIVE:
            inactive = rng.binomial(x[...,a],.05)
            x[...,a] -= inactive
            x[...,a+1] += inactive
        react(x,world,history,unit,rng)
        if pedigree:
            for root in chosen_roots:
                for j in range(x.shape[1]):
                    records.append(dict(root=root,id=f'{root}:{g}:{ids[root,j]}',
                        parent=f'{root}:{g-1}:{parent_ids[root,j]}',generation=g,
                        birth_volume_pl=float(volume*fractions[root,j]),volume_pl=volume,
                        carrier_added_pl=float(volume*(1-fractions[root,j])),
                        stock=x[root,j].tolist(),sampled=bool(terminal[root,j]),
                        pulse=bool(terminal[root,j]), donor_source='external_donor' if world=='horizontal' else None))
        if g>=5:
            pool = np.where(terminal[...,None],x,0).sum(axis=1)
            pools[g] = (pool,terminal.sum(axis=1)*volume)
            sampled += moieties(pool)
            x = x[~terminal].reshape(roots,-1,12)
            ids = ids[~terminal].reshape(roots,-1)
        assert np.array_equal(initial+supplied,emitted+sampled+moieties(x).sum(axis=1)), 'open-system conservation'
    ledger = dict(initial=initial.tolist(),supplied=supplied.tolist(),external_loss=emitted.tolist(),
                  terminal_samples=sampled.tolist(),final=moieties(x).sum(axis=1).tolist())
    return pools, group, batch, ledger, records

def observe_pools(pools,group,batch,loq,rng,replicate):
    rows = []
    shared_response = rng.normal(0,.03,4)
    shared_recovery = rng.normal(0,.05,4)
    for g,(stocks,volumes) in pools.items():
        for i,(stock,v) in enumerate(zip(stocks,volumes)):
            s = stock/M
            active = s[list(ACTIVE)].sum()
            native = active+.05*s[8]+.005*s[11]
            refolded = native+.2*s[[1,3,5,7]].sum()
            ancestry_ok = rng.random()>.02
            recovered = rng.random()>(.02+.08*np.exp(-active/(v*.001)))
            c = assay.calibration()
            c.update(loq=loq,_shared_response=shared_response[batch[i]],_shared_recovery=shared_recovery[batch[i]])
            amounts = dict(founder=s[:4].sum(),new=s[4:6].sum(),hyper=s[8],reporter=s[11],imported=s[6:8].sum())
            observation = assay.observe(amounts,dict(native=native,refolded=refolded),rng,c,
                                        volume_pl=v,qualified=ancestry_ok and recovered)
            result = assay.infer(observation)
            lower = result['new_capacity_lower']['native']
            upper = result['new_capacity_upper']['native']
            l,u = 0.,1.
            if upper is not None:
                if lower/(v*.001)>.5: l=u=1.
                elif upper/(v*.001)<.5: l=u=0.
            raw = [observation['signals'][key]['raw'] for key in (*assay.SPECIES,*assay.MODES)]
            rows.append([replicate,group[i],i,batch[i],g,v,result['qualified'],lower,
                np.nan if upper is None else upper,l,u,result['status']['native']=='detected',
                s[4],s[0],s[2],s[6],*raw,
                observation['signals']['new']['response'],observation['signals']['native']['response'],
                *result['intervals']['native'],native,s[:8].sum(),s[4:6].sum(),ancestry_ok,recovered])
    return np.asarray(rows,dtype=np.float64)

def decisions(rows,n,max_n=96,threshold=.5):
    col = {v:i for i,v in enumerate(FIELDS)}
    per_batch = max_n//4
    within = rows[:,col['root']].astype(int)%max_n%per_batch
    data = rows[within<n//4]
    results = []
    for g in (5,6):
        d = data[data[:,col['generation']]==g]
        batch_lowers, batch_mids, variances = [],[],[]
        for b in range(4):
            lower,mid,var = 0.,0.,0.
            for group,sign in enumerate((1,-1,-1,1)):
                q = d[(d[:,col['batch']]==b)&(d[:,col['group']]==group)]
                assert len(q)==n//4
                capacity_lower=q[:,col['new_lower']]/(q[:,col['volume_pl']]*.001)
                capacity_upper=q[:,col['new_upper']]/(q[:,col['volume_pl']]*.001)
                l=(capacity_lower>threshold).astype(float)
                u=np.where(np.isfinite(capacity_upper)&(capacity_upper<threshold),0.,1.)
                lower += sign*np.mean(l if sign>0 else u)
                midpoint = (l+u)/2
                mid += sign*np.mean(midpoint)
                var += np.var(midpoint,ddof=1)/len(q)
            batch_lowers.append(lower);batch_mids.append(mid);variances.append(var)
        se = max(np.sqrt(sum(variances)/16),np.std(batch_mids,ddof=1)/2)
        contrast_lower = np.mean(batch_lowers)-3.3*se
        hi = d[d[:,col['group']]==0]
        fraction = np.mean(hi[:,col['detected']])
        results.append(dict(generation=g,contrast_lower=float(contrast_lower),
            contrast_midpoint=float(np.mean(batch_mids)),standard_error=float(se),
            high_intact_detected=float(fraction),
            high_intact_qualified=float(np.mean(hi[:,col['qualified']])),
            passed=bool(contrast_lower>0 and fraction>=.8)))
    return dict(n=n,threshold_um=threshold,passed=all(r['passed'] for r in results),generations=results)

def shuffle_history(rows,n,rng,max_n=96):
    c={v:i for i,v in enumerate(FIELDS)}
    selected=rows[rows[:,c['root']].astype(int)%max_n%(max_n//4)<n//4].copy()
    for b in range(4):
        for arm in (0,1):
            mask=(selected[:,c['batch']]==b)&(selected[:,c['group']]//2==arm)
            roots=np.unique(selected[mask,c['root']]).astype(int)
            labels=rng.permutation(np.repeat([2*arm,2*arm+1],n//4))
            for root,label in zip(roots,labels):
                selected[selected[:,c['root']]==root,c['group']]=label
    return selected

def validate_pedigree(records):
    indexed = {r['id']:r for r in records}
    assert len(indexed)==len(records)
    child_counts = {}
    for r in records:
        if r['parent'] is None: continue
        p = indexed[r['parent']]
        assert not p['sampled'] and p['generation']==r['generation']-1
        assert p['root']==r['root'] and r['volume_pl']>0
        assert not p['pulse'], 'terminal pulse never continues'
        child_counts[p['id']] = child_counts.get(p['id'],0)+1
    for r in records:
        assert child_counts.get(r['id'],0)==(0 if r['sampled'] else 2)
    for parent in child_counts:
        children = [r for r in records if r['parent']==parent]
        assert abs(sum(c['birth_volume_pl'] for c in children)-indexed[parent]['volume_pl'])<1e-8
    return dict(nodes=len(records),roots=sum(r['parent'] is None for r in records),
                sampled=sum(r['sampled'] for r in records),checks='passed')
