import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

BASE=Path(__file__).resolve().parent
PROTOCOL_SHA="2e8fc310cbe13cdd163f7cb9a54f703cdd85ed44bff66501e7a7cfac7494749c"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalytic_rows():
    tables=json.loads((BASE/"sources/gtm3/tables.json").read_text())
    assert len(tables)==1 and tables[0]["id"]=="tbl1"
    rows=[]
    current=None
    for raw in tables[0]["rows"][2:]:
        if len(raw)==4:
            current=raw[0]
            values=raw[1:]
        elif len(raw)==3 and current:
            values=raw
        else:
            raise ValueError("Unexpected Table1 rowspan")
        conversion,u,l=[float(x.replace("–","-").replace("−","-")) for x in values]
        if current not in ("SS-GTM-3","RR-GTM-3") or not 0<=conversion<=100 or not all(abs(x)<=100 for x in (u,l)):
            raise ValueError("Invalid catalyst/table units")
        rows.append(dict(catalyst=current,conversion_percent=conversion,
                         inversion_ee_percent=u,retention_ee_percent=l,
                         link_to_crossed_seeded_offspring_lot=None))
    assert len(rows)==4 and sum(x["catalyst"]=="SS-GTM-3" for x in rows)==2
    return rows


def weighted_ee(founder_flux_fraction,founder_ee,new_ee):
    if not 0<=founder_flux_fraction<=1 or max(abs(founder_ee),abs(new_ee))>1:
        raise ValueError("Flux fraction and normalized ee outside bounds")
    return founder_flux_fraction*founder_ee+(1-founder_flux_fraction)*new_ee


def parent_priority(seed,cue):
    return cue if seed is None else seed


def cue_priority(seed,cue):
    return cue


def csv_inventory(path):
    with path.open(encoding="utf-8-sig",newline="") as handle:
        reader=csv.reader(handle)
        header=next(reader)
        labels=[x.strip() for x in header]
        if labels not in (["time","Flux N2","time","Flux CO2"],["time","N2 flux","time","CO2 flux"]):
            raise ValueError("Unexpected independent time/flux columns")
        channels={"N2":[],"CO2":[]}
        orphan={"N2":0,"CO2":0}
        count=0
        for row in reader:
            if len(row)!=4:
                raise ValueError("Unexpected CSV width")
            count+=1
            for name,start in (("N2",0),("CO2",2)):
                pair=[None if x.strip() in ("","--") else float(x) for x in row[start:start+2]]
                if any(v is not None and not math.isfinite(v) for v in pair):
                    raise ValueError("Nonfinite time/flux value")
                if all(v is not None for v in pair):
                    channels[name].append(pair)
                elif any(v is not None for v in pair):
                    orphan[name]+=1
    return dict(rows=count,channels={name:dict(valid_pairs=len(values),unpaired_fields=orphan[name],
                negative_flux_pairs=sum(y<0 for _,y in values),
                minimum_time=min(t for t,_ in values),maximum_time=max(t for t,_ in values),
                after_83h_pairs=sum(t>83 for t,_ in values)) for name,values in channels.items()})


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    assert digest(BASE/"PROTOCOL.md")==PROTOCOL_SHA
    receipt=json.loads((BASE/"sources/gtm3/receipt.json").read_text())
    for name,metadata in receipt["files"].items():
        assert digest(BASE/"sources/gtm3"/name)==metadata["sha256"]
    function=catalytic_rows()
    assert all((row["inversion_ee_percent"]<0)==row["catalyst"].startswith("SS") for row in function)
    factorial=[]
    for loading,seed,cue in itertools.product((5,10),(-1,1),(-1,1)):
        factorial.append(dict(seed_loading_percent_of_feed_oxide=loading,seed="SS" if seed<0 else "RR",
                              directing_agent="SS" if cue<0 else "RR",
                              source_ordinal_progress="greater_if_matched" if seed==cue else "lower_if_mismatched",
                              measured_new_material_function_sign=None,
                              parent_priority_counterfactual_sign=parent_priority(seed,cue),
                              cue_priority_counterfactual_sign=cue_priority(seed,cue),
                              counterfactuals_disagree=seed!=cue))
    assert len(factorial)==8 and sum(r["counterfactuals_disagree"] for r in factorial)==4
    assert weighted_ee(0,0.3,-0.3)==-0.3 and weighted_ee(1,0.3,-0.3)==0.3
    try:
        weighted_ee(2,0.3,-0.3)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid flux fraction accepted")
    for observation in function:
        cue=-1 if observation["catalyst"].startswith("SS") else 1
        measured_sign=-1 if observation["inversion_ee_percent"]<0 else 1
        assert parent_priority(None,cue)==cue_priority(None,cue)==measured_sign
    boundary=BASE/"sources/boundary"
    checksums=json.loads((boundary/"checksums.json").read_text())
    for entry in checksums:
        assert digest(boundary/entry["name"])==entry["sha256"]
        if "expected_md5" in entry:
            assert hashlib.md5((boundary/entry["name"]).read_bytes()).hexdigest()==entry["expected_md5"]
    inventory={name:csv_inventory(boundary/name) for name in ("Figure4.csv","Figure5.csv")}
    result=dict(protocol_sha256=PROTOCOL_SHA,analysis_sha256=digest(Path(__file__)),
                status="EVIDENCE_AND_IDENTIFIABILITY_ASSESSMENT_COMPLETE_NOT_GOAL_COMPLETE",
                evidence_class="Previously inspected primary observations; no empirical kinetic fit or fresh chemical holdout",
                gtm3=dict(doi="10.1021/jacs.2c01874",catalytic_observations=function,
                          functional_observable="Sign of inversion-product ee under the source assay; preparation labels are not absolute framework configurations",
                          crossed_growth_conditions=factorial,
                          incompatible_counterfactual_predictions=4,
                          resolved_by_measured_offspring_function=0,
                          functional_inheritance_identified=False,
                          founder_catalytic_flux_fraction=None,
                          copying_fidelity=None,
                          conclusion="Two candidate explanations share observed qualitative growth matching and separately measured catalyst signs; off-diagonal offspring function remains unmeasured. These are identifiability witnesses, not fitted chemical mechanisms."),
                boundary_dataset=dict(doi="10.25405/data.ncl.9610601.v1",checksum_verification="PASS",
                                      inventory=inventory,fit_allowed=False,
                                      reasons=["README names a different paper and unreconciled drilled-channel geometry",
                                               "Figure labels differ from accepted paper",
                                               "Independent time columns include orphaned CO2 flux values",
                                               "Late data extend beyond documented plotted conditions; no spontaneous-failure or durability claim"]),
                source_to_target_properties_transferred=False,
                verified_integrated_complements_added=0,
                full_goal_complete=False)
    out=BASE/"results"
    out.mkdir(exist_ok=True)
    (out/"assessment.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(gtm3_growth_conditions=8,disagreeing_counterfactuals=4,
                          measured_offspring_function_resolving_them=0,
                          boundary_dataset=inventory,integrated_additions=0),indent=2))


if __name__=="__main__":
    main()
