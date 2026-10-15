"""Frozen synthetic planning; exclusive outputs preserve all prior runs."""
import argparse
import csv
import hashlib
import json
import pathlib
import zipfile
import numpy as np
from model import calibration, observe, infer, material_budget, ratio_interval, wilson

HERE=pathlib.Path(__file__).resolve().parent

def write(path,value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')

def scenarios():
    rows=[]
    for founder in (0,10,100):
        for new in (0,10,100,1000):
            for fraction in (0,.25,1):
                if new==0 and fraction!=0: continue
                rows.append(dict(id=f'f{founder}_n{new}_a{fraction}',founder=founder,new=new,active=fraction,gate=None))
    for gate in ('label_qualified','mixture_qualified','recovery_qualified','native_qualified','refolding_only'):
        rows.append(dict(id=gate,founder=10,new=1000,active=1,gate=gate))
    return rows

def run(output,development=False):
    output.mkdir(parents=True,exist_ok=False)
    n=16 if development else 256
    seed=[17,19] if development else [20261015,5101]
    sources=sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.md','.json'))
    frozen={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    write(output/'freeze.json',dict(hashes=frozen,seed=seed,replicates=n,calibration=calibration(),scenarios=scenarios()))
    with zipfile.ZipFile(output/'source.zip','w') as z:
        for p in sources:z.write(p,p.name)
    summaries=[]
    with (output/'observations.jsonl').open('w') as raw:
        for index,case in enumerate(scenarios()):
            hits={m:0 for m in ('native','refolded')}; covers=dict(hits)
            for rep in range(n):
                rng=np.random.default_rng(np.random.SeedSequence(seed+[index,rep]))
                amounts=dict(founder=case['founder'],new=case['new'],hyper=20.,reporter=40.,imported=0.)
                newcap=case['new']*case['active']
                capacity=case['founder']+newcap+20*.08+40*.005
                caps=dict(native=capacity,refolded=capacity)
                truth=dict(native=newcap,refolded=newcap)
                c=calibration()
                if case['gate']=='refolding_only':
                    caps['native']-=newcap;truth['native']=0.
                elif case['gate']:
                    c[case['gate']]=False
                obs=observe(amounts,caps,rng,c,volume_pl=1000000.)
                result=infer(obs)
                for m in hits:
                    hits[m]+=result['status'][m]=='detected'
                    upper=result['new_capacity_upper'][m]
                    covers[m]+=upper is not None and result['new_capacity_lower'][m]<=truth[m]<=upper
                raw.write(json.dumps(dict(scenario=case['id'],replicate=rep,truth_new_capacity=truth,observation=obs,inference=result),sort_keys=True)+'\n')
            entry=dict(case=case,n=n)
            for m in hits:
                ci=wilson(hits[m],n)
                null=(case['active']==0 or case['new']==0 or (case['gate']=='refolding_only' and m=='native'))
                entry[m]=dict(detections=hits[m],rate=hits[m]/n,wilson95=ci,coverage=covers[m]/n,coverage_wilson95=wilson(covers[m],n),
                              target='false_positive<=.05' if null else 'power>=.8',
                              target_certified=ci[1]<=.05 if null else ci[0]>=.8,
                              coverage_applicable=case['gate'] not in ('label_qualified','mixture_qualified','recovery_qualified') and not (m=='native' and case['gate']=='native_qualified'))
                if not entry[m]['coverage_applicable']:
                    entry[m]['coverage']=None;entry[m]['coverage_wilson95']=None
            summaries.append(entry)
    write(output/'summary.json',summaries)
    retention=[]
    with (output/'retention_observations.jsonl').open('w') as raw:
        for idx,(retained,active,recovery_known) in enumerate([(r,a,k) for r in (.3,.8) for a in (.4,1.) for k in (True,False)]):
            covered=0; detected_inactivation=0; mass_balanced=0; paired_detected=0;paired_covered=0
            for rep in range(n):
                rng=np.random.default_rng(np.random.SeedSequence(seed+[100+idx,rep]))
                shared=float(rng.normal(0,.03)); rec=float(rng.normal(0,.05))
                pairs={}
                for name,fraction,cap_fraction,recovery in [('before',1.,1.,.5),('inside',retained,retained*active,.3),('outside',.9-retained,.9-retained,.8),('surface',.1,.1,.5)]:
                    c=calibration();c.update(recovery=recovery,recovery_qualified=recovery_known,_shared_response=shared,_shared_recovery=rec)
                    obs=observe(dict(founder=100*fraction,new=900*fraction),dict(native=800*cap_fraction,refolded=800*fraction),rng,c,volume_pl=1e6)
                    pairs[name]=dict(observation=obs,inference=infer(obs))
                ints={k:v['inference']['intervals'] for k,v in pairs.items()}
                total={k:[ints[k]['founder'][j]+ints[k]['new'][j] for j in (0,1)] for k in ints}
                amount_ratio=ratio_interval(total['inside'],total['before']) if recovery_known else None
                capacity_ratio=ratio_interval(ints['inside']['native'],ints['before']['native']) if recovery_known else None
                before_specific=ratio_interval(ints['before']['native'],total['before'])
                inside_specific=ratio_interval(ints['inside']['native'],total['inside'])
                loss_specific=ratio_interval(inside_specific,before_specific) if recovery_known else None
                # Shared multiplicative calibration cancels in this matched contrast.
                short={}
                for name in ('inside','before'):
                    o=pairs[name]['observation']
                    short[name]={}
                    for key in ('native','founder','new'):
                        s=o['signals'][key]
                        short[name][key]=[max(0,s['raw']-o['calibration']['cross_upper'])/s['response']/1.1,
                                          s['raw']/s['response']/.9]
                paired_specific={k:ratio_interval(v['native'],[sum(v[a][j] for a in ('founder','new')) for j in (0,1)]) for k,v in short.items()}
                paired_admitted=recovery_known and all(not pairs[k]['observation']['signals'][a]['censored'] for k in ('inside','before') for a in ('native','founder','new'))
                paired_ratio=ratio_interval(paired_specific['inside'],paired_specific['before']) if paired_admitted else None
                paired_detected+=paired_admitted and paired_ratio[1]<1
                paired_covered+=paired_admitted and paired_ratio[0]<=active<=paired_ratio[1]
                balance=[sum(total[k][j] for k in ('inside','outside','surface')) for j in (0,1)]
                bounds={k:[v['inference']['new_capacity_lower']['native'],v['inference']['new_capacity_upper']['native']] for k,v in pairs.items()}
                new_retention=ratio_interval(bounds['inside'],bounds['before']) if recovery_known else None
                mass_balanced+=balance[0]<=1000<=balance[1]
                covered+=recovery_known and capacity_ratio[0]<=retained*active<=capacity_ratio[1]
                detected_inactivation+=recovery_known and loss_specific[1]<1
                raw.write(json.dumps(dict(scenario=idx,replicate=rep,paired=pairs,amount_retention_interval=amount_ratio,capacity_retention_interval=capacity_ratio,specific_capacity_ratio_interval=loss_specific,paired_specific_capacity_ratio_interval=paired_ratio,mass_balance_interval=balance if recovery_known else None,new_age_active_retention_interval=new_retention),sort_keys=True)+'\n')
            retention.append(dict(retained=retained,active_survival=active,recovery_qualified=recovery_known,n=n,coverage=covered/n if recovery_known else None,coverage_wilson95=wilson(covered,n) if recovery_known else None,inactivation_detection=detected_inactivation/n,paired_inactivation_detection=paired_detected/n,paired_detection_wilson95=wilson(paired_detected,n),paired_specific_coverage=paired_covered/n if recovery_known else None,paired_coverage_wilson95=wilson(paired_covered,n) if recovery_known else None,mass_balance_coverage=mass_balanced/n if recovery_known else None,mass_balance_wilson95=wilson(mass_balanced,n) if recovery_known else None))
    write(output/'retention.json',retention)
    budgets=[]
    for diameter in (10,20,50):
        for count in (1,100,10000,100000):
            for fraction in (.1,.5,1.):
                b=material_budget(diameter);new=b['amount_fmol']*count*fraction
                budgets.append(dict(diameter_um=diameter,pool=count,new_fraction=fraction,new_fmol=new,identity_recovered=new*.5*.5,capacity_recovered=new*.25*.5,all_channels_above_loq=new*.25*.5>=1,**b))
    with (output/'material_budget.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(budgets[0]));w.writeheader();w.writerows(budgets)
    write(output/'nonidentifiability.json',dict(worlds=[dict(founder_amount=10,new_amount=10,founder_capacity=10,new_capacity=0),dict(founder_amount=10,new_amount=10,founder_capacity=0,new_capacity=10)],common_marginals=dict(founder_amount=10,new_amount=10,total_capacity=10),new_capacity_interval=[0,10],interpretation='Origin and total activity marginals do not uniquely identify new activity.'))
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,4))
    for founder in (0,10,100):
        selected=[x for x in summaries if x['case']['founder']==founder and x['case']['active']==1 and not x['case']['gate']]
        ax.plot([x['case']['new'] for x in selected],[x['native']['rate'] for x in selected],'-o',label=f'Founder {founder} fmol')
    ax.axhline(.8,color='gray',linestyle='--');ax.set(xscale='log',ylim=(-.02,1.02),xlabel='New active F1 capacity (fmol equivalent)',ylabel='Detection fraction',title='Synthetic planning: native new-capacity lower bound')
    ax.legend();fig.tight_layout();fig.savefig(output/'power.png');plt.close(fig)
    assert frozen=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    write(output/'verification.json',dict(status='PASS',source_unchanged=True,scenarios=len(summaries),replicates=n,assay_observations=len(summaries)*n,retention_observations=len(retention)*n*4))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--development',action='store_true');a=p.parse_args();run(a.output,a.development)
