import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
PROTOCOL_SHA = "118d1e96066224ccbc6f1e7cd448ae8a34b0685755332463b0f695640bc72bdd"


def number(value):
    if value == "—":
        return None
    if value == "∞":
        return math.inf
    return float(value)


def al_fraction(oxide_ratio):
    if oxide_ratio <= 0 or math.isnan(oxide_ratio):
        raise ValueError("Positive oxide ratio required")
    return 2/(oxide_ratio+2)


def fit_mixture(x, y):
    mean_x, mean_y = float(np.mean(x)), float(np.mean(y))
    unconstrained_a = float(np.dot(x-mean_x,y-mean_y)/np.dot(x-mean_x,x-mean_x))
    unconstrained_c = mean_y-unconstrained_a*mean_x
    candidates = [(0,float(np.clip(mean_y,0,1))),
                  (float(np.clip(np.dot(x,y)/np.dot(x,x),0,1)),0)]
    edge_a = float(np.clip(np.dot(x-1,y-1)/np.dot(x-1,x-1),0,1))
    candidates.append((edge_a,1-edge_a))
    if unconstrained_a >= 0 and unconstrained_c >= 0 and unconstrained_a+unconstrained_c <= 1:
        candidates.append((unconstrained_a,unconstrained_c))
    a,c = min(candidates,key=lambda ac:float(np.sum((ac[1]+ac[0]*x-y)**2)))
    return dict(alpha=a,intercept=c,g=c/(1-a) if a<1 else None,
                unconstrained_alpha=unconstrained_a,
                boundary_hit=bool(a==0 or a==1 or c==0 or a+c==1))


def errors(observed, predicted):
    residual=np.asarray(predicted)-observed
    return dict(observed=np.asarray(observed).tolist(),predicted=np.asarray(predicted).tolist(),
                residual_predicted_minus_observed=residual.tolist(),
                rmse=float(np.sqrt(np.mean(residual**2))))


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    assert hashlib.sha256((BASE/"PROTOCOL.md").read_bytes()).hexdigest()==PROTOCOL_SHA
    source=BASE/"sources/tables-exact.json"
    raw=json.loads(source.read_text())
    seeds={r[0]:r for r in raw["table1"] if len(r)==11 and r[0].startswith("S") and r[0][1:].isdigit()}
    products=[r for r in raw["table2"] if len(r)==8 and r[0].startswith("BEA")]
    assert len(seeds)==len(products)==10 and len({r[1] for r in products})==10
    rows=[]
    for product in products:
        seed=seeds[product[1]]
        sr,pr=number(seed[5]),number(product[3])
        rows.append(dict(product=product[0],seed=seed[0],
                         seed_oxide_ratio=None if math.isinf(sr) else sr,
                         seed_is_pure_silica=math.isinf(sr),product_oxide_ratio=pr,
                         seed_Al_cation_fraction=al_fraction(sr),product_Al_cation_fraction=al_fraction(pr),
                         seed_Vmicro_cm3_g=number(seed[6]),product_Vmicro_cm3_g=number(product[4]),
                         product_yield_percent=number(product[7]),
                         nominal_gel_to_product_oxide_ratio=40/pr))
    train=np.array([not r["seed_is_pure_silica"] for r in rows])
    x=np.array([r["seed_Al_cation_fraction"] for r in rows])
    y=np.array([r["product_Al_cation_fraction"] for r in rows])
    assert train.sum()==8 and (~train).sum()==2
    parameters=fit_mixture(x[train],y[train])
    prediction=parameters["intercept"]+parameters["alpha"]*x
    composition=errors(y[~train],prediction[~train])
    parent_copy=errors(y[~train],x[~train])
    pore_rows=[r for r in rows if r["product_Vmicro_cm3_g"] is not None]
    pore_train=[r for r in pore_rows if not r["seed_is_pure_silica"]]
    pore_test=[r for r in pore_rows if r["seed_is_pure_silica"]]
    assert len(pore_train)==4 and len(pore_test)==2
    mean_pore=float(np.mean([r["product_Vmicro_cm3_g"] for r in pore_train]))
    pore_observed=np.array([r["product_Vmicro_cm3_g"] for r in pore_test])
    pore_common=errors(pore_observed,np.full(2,mean_pore))
    pore_copy=errors(pore_observed,np.array([r["seed_Vmicro_cm3_g"] for r in pore_test]))
    assert al_fraction(40)==1/21 and al_fraction(math.inf)==0
    synthetic=np.array([0.0,0.1,0.2])
    check=fit_mixture(synthetic,0.02+0.5*synthetic)
    assert abs(check["alpha"]-0.5)<1e-12 and abs(check["g"]-0.04)<1e-12
    check_copy=fit_mixture(synthetic,synthetic)
    assert check_copy["alpha"]==1 and check_copy["g"] is None
    assert all(0<=v<=1 for v in prediction)
    result=dict(status="RETROSPECTIVE_BULK_STATE_TRANSFER_COMPARISONS_COMPLETE",
                protocol_sha256=PROTOCOL_SHA,
                source_table_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                classification="Primary tables inspected before fitting; two pure-silica parents withheld from parameter estimation, not blind validation",
                composition=dict(calibration_seeds=[r["seed"] for r in rows if not r["seed_is_pure_silica"]],
                                 heldout_seeds=[r["seed"] for r in rows if r["seed_is_pure_silica"]],
                                 parameters=parameters,
                                 effective_mixture_heldout=composition,direct_parent_copy_heldout=parent_copy,
                                 limitation="Bulk XRF state descriptor; alpha is not copying fidelity, founder fraction or an uncertainty bound"),
                microporosity=dict(calibration_seeds=[r["seed"] for r in pore_train],
                                   heldout_seeds=[r["seed"] for r in pore_test],
                                   common_product_mean_cm3_g=mean_pore,
                                   common_product_heldout=pore_common,parent_copy_heldout=pore_copy,
                                   limitation="One-growth nitrogen accessibility; no lineage-linked catalytic function or quantitative active founder bound"),
                exact_target_integration=False, PMo12_same_medium_integration=False,
                newly_active_product_mol=None, empirical_founder_function_bound=None,
                functional_transmission_matrix=None,
                preserved_negatives=[
                    "Direct parent bulk-composition copying contradicts pure-silica-parent/Al-containing-product contrast",
                    "Effective positive composition-memory coefficient reaches zero boundary under constrained descriptor",
                    "Unknown yield denominator prevents converting10wt%seed/feed into final founder fraction",
                    "Unchanged and chemically altered founder function not independently bounded",
                    "No serial newly competent descendants, catalytic inheritance or selectable inherited variants measured",
                    "Seeds were originally made with organic templates and later calcined",
                    "Alkaline140C synthesis not a demonstrated common medium with acidicPMo12 electrolysis"
                ])
    out=BASE/"results"
    out.mkdir(exist_ok=True)
    (out/"analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    with (out/"joined_tables.csv").open("w",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({"parameters":parameters,"composition_rmse":composition["rmse"],
                      "parent_copy_rmse":parent_copy["rmse"],"pore_common_rmse":pore_common["rmse"],
                      "pore_copy_rmse":pore_copy["rmse"]},indent=2))


if __name__ == "__main__":
    main()
