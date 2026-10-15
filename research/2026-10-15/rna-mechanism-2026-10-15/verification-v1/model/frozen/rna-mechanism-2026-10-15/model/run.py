"""Frozen dose-curve cross-validation, chemistry/transport diagnosis and exact replay."""
import argparse
import csv
from dataclasses import asdict,replace
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import time
import numpy as np
import scipy
from scipy.optimize import least_squares,minimize_scalar
from model import Parameters,bulk_curve,single_cycle,serial

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
OLD=WORKSPACE/"measured-coupling-2026-10-15/rna_model"
SOURCE=OLD.parent/"rna_sources"
AUDIT=ROOT.parent/"sources/salibi"
CANDIDATES=("original","saturation","saturation_h","saturation_q","saturation_hq")

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save_json(path,value): path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n")
def write_csv(path,rows):
    with path.open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def load():
    with (SOURCE/"observations.csv").open() as stream: rows=list(csv.DictReader(stream))
    for row in rows:
        for key in ["seed_uM","hyper_a_uM","x","value_percent"]: row[key]=float(row[key])
    return rows
def group_key(r): return r["dataset"],r["seed_uM"],r["hyper_a_uM"]
def groups(rows): return sorted(set(group_key(r) for r in rows if r["dataset"].startswith("S13")))

def setup(candidate,fixed_kb=None):
    if candidate=="original":
        return [-5,-9,-2],[0,-1,3],[[-1.5,-5,0],[-1,-4,1],[-2,-6,2]]
    low=[-4,-8,-2]+([-1] if "q" in candidate else [])
    high=[1,0,2]+([0] if "q" in candidate else [])
    starts=[[-1,-5,0,-.155],[-.5,-3,1,-.398],[-1.5,-6,-1,-.0223]]
    starts=[s[:len(low)] for s in starts]
    if fixed_kb is not None:
        low.pop(2);high.pop(2)
        for s in starts:s.pop(2)
    return low,high,starts

def decode(candidate,logp,fixed_kb=None):
    values=list(10**np.asarray(logp))
    if candidate=="original": return Parameters(family="original",kf=values[0],kh=values[1],ki=values[2])
    if fixed_kb is not None: values.insert(2,fixed_kb)
    return Parameters(kf=values[0],kh=values[1],kb=values[2],q=values[3] if "q" in candidate else 1.,hroute=int("h" in candidate))

def kinetic_predictions(p,rows):
    output=[]
    for key in groups(rows):
        selected=sorted([r for r in rows if group_key(r)==key],key=lambda r:r["x"])
        pred=bulk_curve(p,key[1],key[2],[r["x"] for r in selected])
        output.extend({**r,"predicted_percent":float(v),"error_pp":float(v-r["value_percent"])} for r,v in zip(selected,pred))
    return output

def fit(candidate,rows,fixed_kb=None):
    low,high,starts=setup(candidate,fixed_kb)
    def residual(logp):
        return np.array([r["error_pp"] for r in kinetic_predictions(decode(candidate,logp,fixed_kb),rows)])
    results=[];solutions=[]
    for start in starts:
        try:
            result=least_squares(residual,start,bounds=(low,high),xtol=1e-8,ftol=1e-8,gtol=1e-8,max_nfev=120)
            finite=bool(np.all(np.isfinite(result.fun)))
            results.append({"start":start,"success":bool(result.success and finite),"nfev":int(result.nfev),
                            "sse":float(result.fun@result.fun) if finite else None,"message":result.message,
                            "bounds_hit":result.active_mask.tolist()})
            if result.success and finite:solutions.append(result)
        except (RuntimeError,ArithmeticError,ValueError) as error:
            results.append({"start":start,"success":False,"message":str(error),"sse":None})
    if not solutions:return None,{"resolved":False,"starts":results}
    best=min(solutions,key=lambda f:f.fun@f.fun)
    p=decode(candidate,best.x,fixed_kb)
    return p,{"resolved":True,"parameters":asdict(p),"sse":float(best.fun@best.fun),
              "rmse_pp":float(np.sqrt(np.mean(best.fun**2))),"n_observations":len(best.fun),
              "bounds_hit":best.active_mask.tolist(),"jacobian_singular_values":np.linalg.svd(best.jac,compute_uv=False).tolist(),
              "starts":results}

def cross_validate(rows):
    scores=[];predictions=[]
    for candidate in CANDIDATES:
        folds=[]
        for key in groups(rows):
            train=[r for r in rows if group_key(r)!=key and r["dataset"].startswith("S13")]
            held=[r for r in rows if group_key(r)==key]
            p,details=fit(candidate,train)
            fold={"held_dose":list(key),"fit":details}
            if p is not None:
                pred=kinetic_predictions(p,held)
                fold["sse"]=sum(r["error_pp"]**2 for r in pred)
                predictions.extend({"candidate":candidate,"held_dose":"|".join(map(str,key)),**r} for r in pred)
            folds.append(fold)
            print("CV",candidate,key,"resolved",p is not None,flush=True)
        resolved=all(f["fit"]["resolved"] for f in folds)
        sse=sum(f["sse"] for f in folds) if resolved else None
        scores.append({"candidate":candidate,"resolved":resolved,"folds":folds,"sse":sse,
                       "cv_rmse_pp":float(np.sqrt(sse/40)) if resolved else None,
                       "fitted_parameter_count":len(setup(candidate)[0])})
    valid=[s for s in scores if s["resolved"]]
    if not valid: raise RuntimeError("All candidate CV studies unresolved; preserve partial output and investigate")
    minimum=min(s["cv_rmse_pp"] for s in valid)
    eligible=[s for s in valid if s["cv_rmse_pp"]<=minimum+.25]
    selected=min(eligible,key=lambda s:(s["fitted_parameter_count"],int("h" in s["candidate"]),s["candidate"]))["candidate"]
    return scores,predictions,selected

def fit_mixing(p,rows):
    selected=[r for r in rows if r["dataset"]=="Figure_2" and r["seed_uM"] in [0,1] and r["x"]>0]
    def objective(mixing):
        pc=replace(p,mixing=float(mixing))
        predictions={(s,n):single_cycle(pc,s,n) for s in [0,1] for n in [1,2,3]}
        return sum((predictions[(r["seed_uM"],r["x"])]-r["value_percent"])**2 for r in selected)
    result=minimize_scalar(objective,bounds=(0,1),method="bounded",options={"xatol":1e-7})
    if not result.success:raise RuntimeError("Transport calibration failed")
    return replace(p,mixing=float(result.x)),{"sse":float(result.fun),"rmse_pp":float(np.sqrt(result.fun/len(selected))),"n":len(selected)}

def predictions(p,rows):
    trajectories={str(s):serial(p,s) for s in [0,1,2]}
    cycles={(s,n):single_cycle(p,s,n) for s in [0,1,2] for n in [0,1,2,3]}
    out=[]
    for r in rows:
        if r["dataset"].startswith("S13"):continue
        v=trajectories[str(int(r["seed_uM"]))][int(r["x"])]["yield_percent"] if r["dataset"]=="Figure_3" else cycles[(r["seed_uM"],r["x"])]
        split="development_benchmark" if r["dataset"]=="Figure_3" or r["seed_uM"]==2 else "transport_calibration"
        out.append({**r,"split":split,"predicted_percent":v,"error_pp":v-r["value_percent"]})
    return out,trajectories

def metrics(rows):
    selected=[r for r in rows if r["x"]>0]
    errors=np.array([r["error_pp"] for r in selected])
    means=[np.mean([r["error_pp"] for r in selected if (r["dataset"],r["seed_uM"],r["x"])==key]) for key in sorted(set((r["dataset"],r["seed_uM"],r["x"]) for r in selected))]
    rmse=float(np.sqrt(np.mean(errors**2)));maximum=float(max(abs(np.array(means))))
    return {"n":len(errors),"rmse_pp":rmse,"bias_pp":float(errors.mean()),"maximum_absolute_mean_error_pp":maximum,
            "passes_development_screen":rmse<=2 and maximum<=4}

def freeze(output):
    files=[ROOT/n for n in ("PROTOCOL.md","model.py","run.py","test_model.py")]
    files += [SOURCE/n for n in ("observations.csv","conditions.json","raw/salibi_data.xlsx")]
    files += [AUDIT/n for n in ("observations.csv","conditions.json","verification.json")]
    files += [OLD/"results-v1"/n for n in ("summary.json","predictions.csv")]
    snapshot=output/"frozen";snapshot.mkdir()
    hashes={}
    for source in files:
        relative=source.relative_to(WORKSPACE);destination=snapshot/relative
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,destination)
        hashes[str(relative)]=digest(destination)
    save_json(output/"freeze.json",{"frozen_before_fit_utc":datetime.now(timezone.utc).isoformat(),"files":hashes,
                                    "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
                                    "classification":"development cross-validation and historical benchmark; no fresh validation"})

def run(output):
    if output.exists():raise FileExistsError("Output must be a new directory")
    output.mkdir(parents=True);freeze(output);begun=time.monotonic();rows=load()
    scores,cv_predictions,selected=cross_validate(rows)
    save_json(output/"cross_validation.json",{"selected":selected,"scores":scores})
    write_csv(output/"cross_validation_predictions.csv",cv_predictions)
    fullfits={};kinetic=[];selected_p=None
    for candidate in CANDIDATES:
        p,details=fit(candidate,rows);fullfits[candidate]=details
        if p is not None:kinetic.extend({"candidate":candidate,**r} for r in kinetic_predictions(p,rows))
        if candidate==selected:selected_p=p
    if selected_p is None:raise RuntimeError("Selected full-data fit unresolved")
    save_json(output/"full_fits.json",fullfits);write_csv(output/"kinetic_predictions.csv",kinetic)
    profiles=[]
    if selected!="original":
        for kb in [.01,.1,1,10,100]:
            _,detail=fit(selected,rows,fixed_kb=kb);profiles.append({"fixed_KB_uM":kb,"fit":detail})
    save_json(output/"profiles.json",profiles)
    transport={};allpred=[];trajectories={};controls={};sensitivity=[];refinement=[]
    for mode in ["fractional","contact"]:
        p,mfit=fit_mixing(replace(selected_p,transport=mode),rows)
        pred,tr=predictions(p,rows);trajectories[mode]=tr
        allpred.extend({"transport":mode,**r} for r in pred)
        transport[mode]={"parameters":asdict(p),"mixing_fit":mfit,
                         "all_benchmark":metrics([r for r in pred if r["split"]=="development_benchmark"]),
                         "Figure2_2uM":metrics([r for r in pred if r["dataset"]=="Figure_2" and r["seed_uM"]==2]),
                         "Figure3":metrics([r for r in pred if r["dataset"]=="Figure_3"])}
        for control in ["no_regeneration","no_exchange"]:
            pc=replace(p,mixing=0) if control=="no_exchange" else p
            ctr={str(s):serial(pc,s,regeneration=control!="no_regeneration") for s in [0,1,2]}
            comp=[{**r,"error_pp":ctr[str(int(r["seed_uM"]))][int(r["x"])]["yield_percent"]-r["value_percent"]} for r in rows if r["dataset"]=="Figure_3"]
            controls[mode+"_"+control]={"metrics":metrics(comp),"trajectories":ctr}
        for retention in [.3,.55,.8,.95]:
            ps,ms=fit_mixing(replace(p,retention_f=retention),rows)
            pr,ts=predictions(ps,rows)
            sensitivity.append({"transport":mode,"active_retention":retention,"fragment_retention":.55,
                                "parameters":asdict(ps),"mixing_fit":ms,
                                "benchmark":metrics([r for r in pr if r["split"]=="development_benchmark"]),"trajectories":ts})
        for seed in [0,1,2]:
            fine=serial(p,seed,rtol=1e-10)
            delta=max(abs(a["yield_percent"]-b["yield_percent"]) for a,b in zip(fine,tr[str(seed)]))
            refinement.append({"transport":mode,"seed_uM":seed,"maximum_difference_pp":delta,"pass":delta<1e-4})
        print("Transport",mode,"complete",flush=True)
    write_csv(output/"predictions.csv",allpred)
    save_json(output/"trajectories.json",trajectories);save_json(output/"controls.json",controls)
    save_json(output/"sensitivity.json",sensitivity);save_json(output/"refinement.json",refinement)
    old=json.loads((OLD/"results-v1/summary.json").read_text())
    structural={"S13_negative_control_predicted_percent":bulk_curve(selected_p,seed=0,hyper=0,times=[0,60]).tolist(),
                "S13_negative_control_observed_percent":[0,0],"source_cells":["S13!C6","S13!C10"],
                "other_new_assays":"S12/S15/S18 differ in sucrose, concentration or protocol; no calibrated numerical extrapolation attempted"}
    save_json(output/"new_assay_checks.json",structural)
    summary={"selected_chemistry":selected,"selection":"whole-dose cross-validation only; 0.25pp simplicity tolerance",
             "classification":"development study, no prospective unseen validation","transport":transport,
             "original_historical_benchmark":old["metrics"],"original_kinetic_fit":old["kinetic_fit"],
             "maximum_balance_error_uM":max(r["moiety_balance_max_error_uM"] for tr in trajectories.values() for rs in tr.values() for r in rs),
             "all_refinement_pass":all(r["pass"] for r in refinement),
             "functional_inheritance":"unidentifiable: no lineage-linked active-F1 observations",
             "elapsed_seconds":time.monotonic()-begun}
    save_json(output/"summary.json",summary);plot(output,rows,kinetic,allpred,selected)
    save_json(output/"manifest.json",{str(p.relative_to(output)):digest(p) for p in sorted(output.rglob("*")) if p.is_file() and p.name!="manifest.json"})
    print(json.dumps(summary,indent=2))

def plot(output,rows,kinetic,pred,selected):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(13,7))
    for ax,key in zip(axes[0,:2],["S13_F1","S13_HyperA"]):
        for group in groups([r for r in rows if r["dataset"]==key]):
            obs=[r for r in rows if group_key(r)==group]
            line=[r for r in kinetic if r["candidate"]==selected and group_key(r)==group]
            color=ax.plot([r["x"] for r in line],[r["predicted_percent"] for r in line],label=f"{max(group[1:]):g} µM")[0].get_color()
            ax.scatter([r["x"] for r in obs],[r["value_percent"] for r in obs],color=color,s=18)
        ax.set(title=key+" full-data fit",xlabel="Minutes",ylabel="Cy5-F1 yield (%)");ax.legend(fontsize=8)
    cv=json.loads((output/"cross_validation.json").read_text())["scores"]
    axes[0,2].barh([s["candidate"] for s in cv],[s["cv_rmse_pp"] or 0 for s in cv],color="#3182bd")
    axes[0,2].set(xlabel="Whole-dose CV RMSE (pp)",title="Development model comparison")
    for ax,seed in zip(axes[1],[0,1,2]):
        observed=[r for r in rows if r["dataset"]=="Figure_3" and r["seed_uM"]==seed]
        ax.scatter([r["x"] for r in observed],[r["value_percent"] for r in observed],color="black",s=15,label="Measured")
        for mode in ["fractional","contact"]:
            line=[r for r in pred if r["transport"]==mode and r["dataset"]=="Figure_3" and r["seed_uM"]==seed and r["replicate"]=="1"]
            ax.plot([r["x"] for r in line],[r["predicted_percent"] for r in line],label=mode)
        ax.set(title=f"Historical serial benchmark, seed {seed} µM",xlabel="Generation",ylabel="Cy5-F1 yield (%)");ax.legend(fontsize=8)
    for ax in axes.flat:ax.grid(alpha=.2)
    fig.suptitle("RNA chemistry revision: mechanism hypotheses, no fresh validation",fontsize=13)
    fig.tight_layout();fig.savefig(output/"comparison.png",dpi=180);plt.close(fig)

def replay(directory):
    manifest=json.loads((directory/"manifest.json").read_text())
    assert all(digest(directory/n)==h for n,h in manifest.items()),"Output manifest mismatch"
    frozen=json.loads((directory/"freeze.json").read_text())["files"]
    assert all(digest(directory/"frozen"/n)==h for n,h in frozen.items()),"Snapshot mismatch"
    assert all(digest(WORKSPACE/n)==h for n,h in frozen.items()),"Current source mismatch"
    summary=json.loads((directory/"summary.json").read_text())
    with (directory/"predictions.csv").open() as stream:saved=list(csv.DictReader(stream))
    regenerated=[]
    for mode in ["fractional","contact"]:
        pr,_=predictions(Parameters(**summary["transport"][mode]["parameters"]),load())
        regenerated.extend(pr)
    assert len(saved)==len(regenerated)
    delta=max(abs(float(a["predicted_percent"])-b["predicted_percent"]) for a,b in zip(saved,regenerated))
    assert delta<1e-8
    print(json.dumps({"manifest_and_frozen_sources_match":True,"replayed_predictions":len(saved),"maximum_difference_pp":delta}))

if __name__=="__main__":
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output",type=Path);group.add_argument("--replay",type=Path)
    args=parser.parse_args()
    if args.replay:replay(args.replay)
    else:run(args.output)
