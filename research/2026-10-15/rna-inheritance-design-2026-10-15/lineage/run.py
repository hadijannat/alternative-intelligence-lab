"""Run frozen worlds or replay their complete numerical outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import zipfile
import numpy as np
from scipy.stats import t
import model

HERE=Path(__file__).resolve().parent

def write(path,value):
    path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def coverage(rows):
    c={v:i for i,v in enumerate(model.FIELDS)}
    admitted=rows[:,c['qualified']]>0
    lower=rows[:,c['new_lower']]
    truth=rows[:,c['true_current_active']]
    upper=rows[:,c['new_upper']]
    usable=admitted & np.isfinite(upper)
    a=int(np.sum(lower[usable]<=truth[usable]+1e-12))
    b=int(np.sum(upper[usable]>=truth[usable]-1e-12))
    n=int(usable.sum())
    cluster_fractions=[];all_covered=[]
    for rep in np.unique(rows[:,c['replicate']]):
        mask=usable&(rows[:,c['replicate']]==rep)
        hits=(lower[mask]<=truth[mask]+1e-12)&(upper[mask]>=truth[mask]-1e-12)
        cluster_fractions.append(float(np.mean(hits)))
        all_covered.append(bool(hits.all()))
    k=len(cluster_fractions)
    mean=float(np.mean(cluster_fractions))
    half=float(t.ppf(.975,k-1)*np.std(cluster_fractions,ddof=1)/np.sqrt(k)) if k>1 else 1.
    return dict(n=n,lower_covers=a,upper_covers=b,
                independent_experiments=k,cluster_coverage_mean=mean,
                cluster_t_interval=[max(0.,mean-half),min(1.,mean+half)],
                all_covered_experiments=sum(all_covered),
                all_covered_wilson=model.assay.wilson(sum(all_covered),k),
                missing=int((~usable).sum()))

def retention(volume,loq,seed,n=128):
    rng=np.random.default_rng(seed)
    c=model.assay.calibration();c['loq']=loq
    outcomes=[]
    for rep in range(n):
        before=volume*.001*16
        count=round(before*model.M)
        after_count=rng.binomial(count,.9)
        active_after=rng.binomial(after_count,.95)
        after=after_count/model.M
        capacity=active_after/model.M
        observations=[]
        for amount,native,refolded in ((before,before,before),(after,capacity,capacity+.2*(after-capacity))):
            obs=model.assay.observe(dict(founder=amount),dict(native=native,refolded=refolded),rng,c,
                                    volume_pl=volume*16)
            observations.append(obs)
        intervals=[model.assay.infer(o)['intervals'] for o in observations]
        ratios={key:model.assay.ratio_interval(intervals[1][key],intervals[0][key])
                for key in ('founder','native','refolded')}
        truth=dict(founder=after/before,native=capacity/before,
                   refolded=(capacity+.2*(after-capacity))/before)
        outcomes.append(dict(replicate=rep,before_fmol=before,after_fmol=after,
            external_loss_fmol=(count-after_count)/model.M,inactivated_fmol=(after_count-active_after)/model.M,
            observations=observations,ratios=ratios,truth=truth))
    summary={}
    for key in ('founder','native','refolded'):
        qualified=[o for o in outcomes if o['ratios'][key] is not None]
        hit=sum(o['ratios'][key][0]<=o['truth'][key]<=o['ratios'][key][1] for o in qualified)
        summary[key]=dict(qualified=len(qualified),coverage=hit,
            wilson=model.assay.wilson(hit,len(qualified)) if qualified else None,
            mean_interval=np.mean([o['ratios'][key] for o in qualified],axis=0).tolist() if qualified else None)
    return dict(summary=summary,raw=outcomes)

def source_hashes():
    paths=[HERE/'model.py',HERE/'run.py',HERE/'test_model.py',HERE/'PROTOCOL.md',HERE.parent/'assay/model.py',
           HERE.parent/'research/lineage/REPORT.md',HERE.parent/'research/lineage/sources.json',
           HERE.parent/'research/assays/REPORT.md',HERE.parent/'research/assays/ledger.json']
    return {str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def run(out,reps,development):
    start=time.time()
    out.mkdir(parents=True,exist_ok=False)
    hashes=source_hashes()
    write(out/'freeze.json',dict(protocol='v2',replicates=reps,development=development,
        namespace=[20261015,5199 if development else 5201],n=[24,48,96],thresholds_um=[.5,1.,2.],
        fields=model.FIELDS,sources=hashes,numpy=np.__version__))
    with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as snapshot:
        for name in hashes: snapshot.write(HERE.parent/name,name)
    all_decisions=[]; summaries=[]; digests={}
    for wi,world in enumerate(model.WORLDS):
        for pi,(volume,loq) in enumerate(model.PLATFORMS):
            arrays=[]
            for rep in range(reps):
                seed=[20261015,5199 if development else 5201,wi,pi,rep]
                rng=np.random.default_rng(seed)
                pools,groups,batches,ledger,records=model.simulate(world,volume,rng,pedigree=rep==0)
                if rep==0:
                    verified=model.validate_pedigree(records)
                    write(out/f'pedigree-{world}-{pi}.json',dict(nodes=records,validation=verified,ledger=ledger))
                rows=model.observe_pools(pools,groups,batches,loq,rng,rep)
                arrays.append(rows)
                for n in (24,48,96):
                    shuffled=model.shuffle_history(rows,n,np.random.default_rng([*seed,900+n]))
                    for threshold in (.5,1.,2.):
                        result=model.decisions(rows,n,threshold=threshold)
                        result.update(world=world,platform=pi,replicate=rep,
                            shuffled=model.decisions(shuffled,n,threshold=threshold))
                        all_decisions.append(result)
            raw=np.stack(arrays)
            name=f'raw-{world}-{pi}.npz'
            np.savez_compressed(out/name,observations=raw)
            digests[name]=hashlib.sha256(raw.tobytes()).hexdigest()
            cov=coverage(raw.reshape(-1,len(model.FIELDS)))
            for n in (24,48,96):
                for threshold in (.5,1.,2.):
                    chosen=[d for d in all_decisions if d['world']==world and d['platform']==pi and d['n']==n and d['threshold_um']==threshold]
                    k=sum(d['passed'] for d in chosen)
                    shuffled_k=sum(d['shuffled']['passed'] for d in chosen)
                    ci=model.assay.wilson(k,len(chosen))
                    positive=world in ('strong','weak')
                    summaries.append(dict(world=world,platform=pi,volume_pl=volume,loq_fmol=loq,n=n,
                        threshold_um=threshold,experiments=len(chosen),accepted=k,rate=k/len(chosen),wilson=ci,
                        shuffled_accepted=shuffled_k,shuffled_wilson=model.assay.wilson(shuffled_k,len(chosen)),
                        target_established=ci[0]>=.8 if positive else ci[1]<=.05,
                        target='power>=0.8' if positive else 'false_positive<=0.05',coverage=cov))
            print(f'{world} platform={pi} reps={reps} seconds={time.time()-start:.1f}',flush=True)
    write(out/'decisions.json',all_decisions)
    write(out/'summary.json',summaries)
    for pi,(v,q) in enumerate(model.PLATFORMS):
        write(out/f'retention-{pi}.json',retention(v,q,[20261015,5199 if development else 5201,900,pi],reps))
    assert hashes==source_hashes(),'source changed during run'
    write(out/'numerical-digests.json',digests)
    write(out/'execution.json',dict(seconds=time.time()-start,source_hashes_unchanged=True))

def replay(original,new):
    frozen=json.loads((original/'freeze.json').read_text())
    assert frozen['sources']==source_hashes(),'frozen code/source mismatch'
    run(new,frozen['replicates'],frozen['development'])
    names=['summary.json','decisions.json','numerical-digests.json',*(f'retention-{p}.json' for p in range(3))]
    names += [f'pedigree-{w}-{p}.json' for w in model.WORLDS for p in range(3)]
    checks={name:(original/name).read_bytes()==(new/name).read_bytes() for name in names}
    write(new/'replay.json',dict(checks=checks,passed=all(checks.values())))
    assert all(checks.values())

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--development',action='store_true')
    p.add_argument('--replay',type=Path)
    args=p.parse_args()
    if args.replay: replay(args.replay,args.output)
    else: run(args.output,2 if args.development else 128,args.development)
