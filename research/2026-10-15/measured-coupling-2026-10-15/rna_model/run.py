"""Calibrate only registered training sets, then predict untouched transfer observations."""
import argparse
import csv
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import numpy as np
import scipy
from scipy.optimize import least_squares, minimize_scalar
from model import Parameters, bulk_curve, serial, single_cycle

ROOT=Path(__file__).resolve().parent
SOURCES=ROOT.parent/"rna_sources"

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save_json(path,value): path.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
def write_csv(path,rows):
    with path.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def load():
    with (SOURCES/"observations.csv").open() as stream:
        rows=list(csv.DictReader(stream))
    for row in rows:
        for key in ["seed_uM","hyper_a_uM","x","value_percent"]: row[key]=float(row[key])
    return rows

def kinetic_residual(logp,rows,rho=1.,ki_fixed=None):
    k,kb=10**logp[:2]
    ki=ki_fixed if ki_fixed is not None else 10**logp[2]
    p=Parameters(k,kb,ki,rho=rho)
    residual=[]
    for dataset in ["S13_F1","S13_HyperA"]:
        selected=[r for r in rows if r["dataset"]==dataset]
        for seed,hyper in sorted(set((r["seed_uM"],r["hyper_a_uM"]) for r in selected)):
            group=sorted([r for r in selected if r["seed_uM"]==seed and r["hyper_a_uM"]==hyper],key=lambda r:r["x"])
            pred=bulk_curve(p,seed,hyper,[r["x"] for r in group])
            residual.extend(pred-np.array([r["value_percent"] for r in group]))
    return np.array(residual)

def fit_kinetics(rows,rho=1.,ki_fixed=None):
    lower=[-5,-9]+([] if ki_fixed is not None else [-2])
    upper=[0,-1]+([] if ki_fixed is not None else [3])
    starts=[[-1.5,-5,0],[-1,-4,1],[-2,-6,2]]
    fits=[least_squares(kinetic_residual,s[:len(lower)],bounds=(lower,upper),
                        args=(rows,rho,ki_fixed),xtol=1e-8,ftol=1e-8,gtol=1e-8,max_nfev=120)
          for s in starts]
    best=min(fits,key=lambda f:np.sum(f.fun*f.fun))
    p=Parameters(10**best.x[0],10**best.x[1],ki_fixed if ki_fixed is not None else 10**best.x[2],rho=rho)
    return p,{"sse_percent_squared":float(np.sum(best.fun*best.fun)),"rmse_pp":float(np.sqrt(np.mean(best.fun*best.fun))),
              "n_summary_means":len(best.fun),"optimizer_success":bool(best.success),"message":best.message,
              "bounds_hit":best.active_mask.tolist(),"fixed_starts":starts,
              "singular_values_of_residual_jacobian":np.linalg.svd(best.jac,compute_uv=False).tolist()}

def fit_mixing(p,rows):
    selected=[r for r in rows if r["dataset"]=="Figure_2" and r["seed_uM"] in [0,1] and r["x"]>0]
    def objective(m):
        fitted=replace(p,mixing=float(m))
        pred={(s,n):single_cycle(fitted,s,n) for s in [0,1] for n in [1,2,3]}
        return sum((pred[(r["seed_uM"],r["x"])]-r["value_percent"])**2 for r in selected)
    fit=minimize_scalar(objective,bounds=(0,1),method="bounded",options={"xatol":1e-7})
    return replace(p,mixing=float(fit.x)),{"sse_percent_squared":float(fit.fun),"rmse_pp":float(np.sqrt(fit.fun/len(selected))),
                                        "n_replicates":len(selected),"optimizer_success":bool(fit.success)}

def predictions(p,rows):
    output=[]
    serial_data={s:serial(p,s) for s in [0,1,2]}
    curves={(s,n):single_cycle(p,s,n) for s in [0,1,2] for n in [0,1,2,3]}
    for row in rows:
        if row["dataset"].startswith("S13"): continue
        predicted=serial_data[row["seed_uM"]][int(row["x"])]["yield_percent"] if row["dataset"]=="Figure_3" else curves[(row["seed_uM"],row["x"])]
        split="prediction" if row["dataset"]=="Figure_3" or row["seed_uM"]==2 else "calibration"
        output.append({**row,"split":split,"predicted_percent":predicted,"error_pp":predicted-row["value_percent"]})
    return output,serial_data

def metrics(rows):
    errors=np.array([r["error_pp"] for r in rows if r["x"]>0])
    means=[]
    keys=sorted(set((r["dataset"],r["seed_uM"],r["x"]) for r in rows if r["x"]>0))
    for key in keys:
        means.append(np.mean([r["error_pp"] for r in rows if (r["dataset"],r["seed_uM"],r["x"])==key]))
    return {"n_nonzero_replicates":len(errors),"rmse_pp":float(np.sqrt(np.mean(errors**2))),
            "bias_pp":float(errors.mean()),"maximum_absolute_mean_error_pp":float(max(abs(np.array(means)))),
            "passes_pragmatic_screen":bool(np.sqrt(np.mean(errors**2))<=2 and max(abs(np.array(means)))<=4)}

def run(output):
    if output.exists(): raise FileExistsError("Use a new output directory to preserve prior results")
    output.mkdir(parents=True)
    begun=time.monotonic()
    files=[ROOT/"PROTOCOL.md",ROOT/"model.py",ROOT/"run.py",ROOT/"test_model.py",SOURCES/"observations.csv",SOURCES/"conditions.json",SOURCES/"raw/salibi_data.xlsx"]
    save_json(output/"freeze.json",{"frozen_before_fitting_utc":datetime.now(timezone.utc).isoformat(),
                                    "files":{str(f.relative_to(ROOT.parent)):digest(f) for f in files},
                                    "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
                                    "split":"S13c plus Fig2 zero/1seed calibration; Fig2 2seed and all Fig3 prediction",
                                    "holdout_disclosure":"Published heldout values inspected during source discovery; no fitting or tuning to them"})
    rows=load()
    p,kinetic_fit=fit_kinetics(rows)
    p,mixing_fit=fit_mixing(p,rows)
    print("Calibration complete",asdict(p),flush=True)
    pred,trajectories=predictions(p,rows)
    write_csv(output/"predictions.csv",pred)
    trajectory_rows=[{"seed_uM":s,**r} for s,data in trajectories.items() for r in data]
    write_csv(output/"trajectories.csv",trajectory_rows)
    all_metrics={"all_prediction":metrics([r for r in pred if r["split"]=="prediction"]),
                 "Figure2_2uM_prediction":metrics([r for r in pred if r["dataset"]=="Figure_2" and r["seed_uM"]==2]),
                 "Figure3_prediction":metrics([r for r in pred if r["dataset"]=="Figure_3"])}
    controls={}
    for mode in ["no_regeneration","no_exchange","no_feed","homogeneous"]:
        pc=replace(p,mixing=0 if mode=="no_exchange" else 1 if mode=="homogeneous" else p.mixing)
        cr={s:serial(pc,s,regeneration=mode!="no_regeneration",feed=mode!="no_feed") for s in [0,1,2]}
        comparisons=[{**r,"error_pp":cr[r["seed_uM"]][int(r["x"])]["yield_percent"]-r["value_percent"]} for r in rows if r["dataset"]=="Figure_3"]
        controls[mode]={"metrics":metrics(comparisons),"trajectories":cr}
    save_json(output/"controls.json",controls)
    sensitivity=[]
    for rho in [.5,1.,2.]:
        pk,kfit=(p,kinetic_fit) if rho==1 else fit_kinetics(rows,rho)
        for retention in [.4,.55,.7]:
            ps,mfit=fit_mixing(replace(pk,retention=retention),rows)
            ps_pred,_=predictions(ps,rows)
            sensitivity.append({"rho":rho,"retention":retention,"parameters":asdict(ps),"kinetic_fit":kfit,"mixing_fit":mfit,
                                "prediction_metrics":metrics([r for r in ps_pred if r["split"]=="prediction"])})
        print("Sensitivity rho",rho,"complete",flush=True)
    save_json(output/"sensitivity.json",sensitivity)
    profiles=[]
    for ki in [.03,.1,.3,1,3,10,30,100,300,1000]:
        pp,pfit=fit_kinetics(rows,ki_fixed=ki)
        profiles.append({"ki_uM":ki,"parameters":asdict(pp),**pfit})
    save_json(output/"profile.json",profiles)
    passive=[]
    for seed in [0,1,2]:
        observed=np.mean([r["value_percent"] for r in rows if r["dataset"]=="Figure_3" and r["seed_uM"]==seed and r["x"]==1])/100
        total_label=.55*2.5/3;report=observed*total_label
        for g in range(1,8):
            if g>1:
                report*=.5*.55
                total_label=.55*(.5*total_label+.5*1.25)
            passive.append({"seed_uM":seed,"generation":g,"reporter_uM":report,"total_label_uM":total_label,"yield_percent":100*report/total_label})
    write_csv(output/"passive_carryover.csv",passive)
    refinement=[]
    for seed in [0,1,2]:
        fine=serial(p,seed,rtol=1e-10)
        refinement.append({"seed_uM":seed,"maximum_yield_difference_pp":max(abs(a["yield_percent"]-b["yield_percent"]) for a,b in zip(fine,trajectories[seed]))})
    witness={"status":"functional lineage inheritance unidentifiable",
             "construction":"Attach any parent identity permutation to cohorts after each FT. Parent labels do not enter chemistry or population PAGE observer, so coherent vs scrambled ancestry give exactly identical observed trajectories.",
             "scope":"A constructive observation-level degeneracy; neither alternative lineage mechanism is claimed to have occurred experimentally.",
             "evidence_type":"Analytical invariance of observer to parent identity; no numeric lineage simulation was executed",
             "required_missing_measurement":"Tracked compartment parent/offspring identities and regenerated active function in daughter compartments under a common environment, with carryover and horizontal-exchange controls"}
    save_json(output/"inheritance_witness.json",witness)
    result={"parameters":asdict(p),"kinetic_fit":kinetic_fit,"mixing_fit":mixing_fit,"metrics":all_metrics,
            "maximum_moiety_balance_error_uM":max(r["moiety_balance_max_error_uM"] for r in trajectory_rows),
            "refinement":refinement,"scope":"Same-buffer kinetic extrapolation to vesicle cohorts; not an experimentally calibrated membrane-dependent elementary mechanism",
            "functional_inheritance":"unidentifiable from these assays", "elapsed_seconds":time.monotonic()-begun}
    save_json(output/"summary.json",result)
    plot(output,rows,pred,controls,passive)
    save_json(output/"manifest.json",{f.name:digest(f) for f in sorted(output.iterdir()) if f.is_file() and f.name!="manifest.json"})
    print(json.dumps(result,indent=2))

def plot(output,rows,pred,controls,passive):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(13,4),sharey=True)
    for ax,seed in zip(axes,[0,1,2]):
        measured=[r for r in rows if r["dataset"]=="Figure_3" and r["seed_uM"]==seed]
        ax.scatter([r["x"] for r in measured],[r["value_percent"] for r in measured],s=18,color="black",label="Measured replicates",zorder=5)
        pr=[r for r in pred if r["dataset"]=="Figure_3" and r["seed_uM"]==seed and r["replicate"]=="1"]
        ax.plot([r["x"] for r in pr],[r["predicted_percent"] for r in pr],color="#2166ac",label="Coupled prediction")
        nr=controls["no_regeneration"]["trajectories"][seed]
        ax.plot([r["generation"] for r in nr],[r["yield_percent"] for r in nr],"--",color="#b2182b",label="No regeneration")
        pc=[r for r in passive if r["seed_uM"]==seed]
        ax.plot([r["generation"] for r in pc],[r["yield_percent"] for r in pc],":",color="#666666",label="Passive from measured G1")
        ax.set(title=f"Initial seed {seed} µM",xlabel="Serial generation",xticks=range(8));ax.grid(alpha=.2)
    axes[0].set_ylabel("Inactive Cy5-F1 reporter yield (%)")
    axes[-1].legend(fontsize=8)
    fig.suptitle("Held-out serial transfer prediction: same buffer, inferred exchange and retention")
    fig.tight_layout();fig.savefig(output/"prediction.png",dpi=180);plt.close(fig)

def replay(directory):
    summary=json.loads((directory/"summary.json").read_text())
    p=Parameters(**summary["parameters"])
    frozen=json.loads((directory/"freeze.json").read_text())
    mismatches=[name for name,h in frozen["files"].items() if digest(ROOT.parent/name)!=h]
    if mismatches: raise AssertionError(f"Frozen source mismatch: {mismatches}")
    pred,_=predictions(p,load())
    with (directory/"predictions.csv").open() as stream:
        saved=list(csv.DictReader(stream))
    delta=max(abs(a["predicted_percent"]-float(b["predicted_percent"])) for a,b in zip(pred,saved))
    assert len(pred)==len(saved) and delta<1e-8
    expected=json.loads((directory/"manifest.json").read_text())
    assert all(digest(directory/n)==h for n,h in expected.items())
    print(json.dumps({"frozen_sources_match":True,"manifest_matches":True,"replayed_predictions":len(pred),"maximum_difference_pp":delta}))

if __name__=="__main__":
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output",type=Path);group.add_argument("--replay",type=Path)
    args=parser.parse_args()
    if args.replay: replay(args.replay)
    else: run(args.output)
