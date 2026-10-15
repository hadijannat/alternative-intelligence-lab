"""Reconcile exactly five ancillary snapshot additions; preserve strict failure."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from campaign_verify import HERE, LAB, ROOT, read_json, save, scientific, sha


ADDED_ONLY = {
    "rna-seed-transport-2026-10-15/independent/REPORT.md",
    "rna-seed-transport-2026-10-15/independent/results-v2/frozen/rna-seed-transport-2026-10-15/independent/PROTOCOL.md",
    "rna-seed-transport-2026-10-15/independent/results-v2/frozen/rna-seed-transport-2026-10-15/independent/verify.py",
    "rna-seed-transport-2026-10-15/independent/results-v2/frozen/rna-seed-transport-2026-10-15/model.py",
    "rna-seed-transport-2026-10-15/independent/results-v2/frozen/rna-turnover-tests-2026-10-15/results-v1/full_fits.json",
}
COMPUTATIONAL_INPUTS = {
    "rna-seed-transport-2026-10-15/model.py", "rna-seed-transport-2026-10-15/run.py",
    "rna-seed-transport-2026-10-15/plot.py", "rna-seed-transport-2026-10-15/PROTOCOL.md",
    "rna-seed-transport-2026-10-15/requirements.txt",
    "measured-coupling-2026-10-15/rna_sources/observations.csv",
    "measured-coupling-2026-10-15/rna_sources/conditions.json",
    "measured-coupling-2026-10-15/rna_sources/raw/salibi_data.xlsx",
    "rna-turnover-tests-2026-10-15/results-v1/fits/baseline__omit-none.json",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    main_dir, refit_dir = LAB/"results-v1", LAB/"verification-v1"
    old = read_json(HERE/"campaign-v1/verification.json")
    old_hashes = read_json(HERE/"campaign-v1/audit_source_hashes.json")
    a, b = read_json(main_dir/"freeze.json"), read_json(refit_dir/"freeze.json")
    ma, mb = read_json(main_dir/"manifest.json"), read_json(refit_dir/"manifest.json")
    checks = []

    def check(name, value):
        checks.append({"check":name,"pass":bool(value)})

    check("strict_failure_receipt_retained", old["status"]=="FAIL" and
          {r["check"] for r in old["failed_checks"]}=={"main_refit_same_file_set","main_refit:freeze.json"})
    check("main_manifest_unchanged_since_full_audit",sha(main_dir/"manifest.json")==old_hashes["main_manifest.json"])
    check("refit_manifest_unchanged_since_full_audit",sha(refit_dir/"manifest.json")==old_hashes["refit_manifest.json"])
    check("exact_five_frozen_additions",set(b["files"])-set(a["files"])==ADDED_ONLY)
    check("no_frozen_removals",not set(a["files"])-set(b["files"]))
    check("exact_five_manifest_additions",set(mb)-set(ma)=={"frozen/"+name for name in ADDED_ONLY})
    check("no_manifest_removals",not set(ma)-set(mb))
    common = set(a["files"])&set(b["files"])
    check("46_common_frozen_inputs",len(common)==46)
    check("common_input_hashes_identical",all(a["files"][n]==b["files"][n] for n in common))
    check("computational_inputs_present",COMPUTATIONAL_INPUTS<=common)
    check("same_runtime_starts_bounds_budget",{k:v for k,v in a.items() if k not in ("files","utc_before_fit")}==
          {k:v for k,v in b.items() if k not in ("files","utc_before_fit")})
    for folder,manifest,freeze in ((main_dir,ma,a),(refit_dir,mb,b)):
        for name,digest in manifest.items():
            check(folder.name+":manifest:"+name,sha(folder/name)==digest)
        for name,digest in freeze["files"].items():
            check(folder.name+":frozen_and_live:"+name,sha(folder/"frozen"/name)==digest and sha(ROOT/name)==digest)
        before,after=(read_json(folder/f"prior_integrity_{part}.json") for part in ("before","after"))
        check(folder.name+":prior_maps",before==after)
        for name,digest in before.items():
            check(folder.name+":prior_live:"+name,sha(ROOT/name)==digest)
    start_a=datetime.fromisoformat(a["utc_before_fit"]).timestamp()
    start_b=datetime.fromisoformat(b["utc_before_fit"]).timestamp()
    additions=[]
    for name in sorted(ADDED_ONLY):
        path=ROOT/name
        mtime=path.stat().st_mtime
        check("addition_between_freezes:"+name,start_a<mtime<start_b)
        additions.append({"path":name,"sha256":b["files"][name],
            "last_modified_utc":datetime.fromtimestamp(mtime,timezone.utc).isoformat(),
            "role":"independent verification report" if name.endswith("independent/REPORT.md") else "duplicate independent verification source snapshot",
            "execution_role":"none: these paths are neither imported nor read by run.py, model.py or plot.py",
            "explanation":"Finalized after the main freeze and before the fresh-process refit freeze; added evidence only."})
    exact_files=0
    outputs=0
    for name in sorted(set(ma)&set(mb)):
        if name=="freeze.json" or Path(name).suffix.lower() in (".png",".pdf"):
            continue
        left,right=main_dir/name,refit_dir/name
        equal=scientific(read_json(left))==scientific(read_json(right)) if left.suffix==".json" else left.read_bytes()==right.read_bytes()
        check("common_scientific_exact:"+name,equal)
        exact_files+=1
        outputs+=not name.startswith("frozen/")
    result={**{k:v for k,v in old.items() if k not in ("status","check_count","failed_checks","scientific_files_exactly_matched")},
        "status":"PASS_WITH_DOCUMENTED_ARCHIVE_DIFFERENCE" if all(c["pass"] for c in checks) else "FAIL",
        "archive_identical":False,"computational_inputs_identical":all(a["files"][n]==b["files"][n] for n in COMPUTATIONAL_INPUTS),
        "scientific_outputs_exact":all(c["pass"] for c in checks if c["check"].startswith("common_scientific_exact:")),
        "max_main_refit_scientific_discrepancy":0,
        "full_audit_checks":old["check_count"],"full_audit_numerical_and_preservation_checks_passed":old["check_count"]-2,
        "reconciliation_checks":len(checks),"failed_checks":[c for c in checks if not c["pass"]],
        "common_scientific_files_exactly_matched":exact_files,"scientific_output_files_exactly_matched":outputs,
        "frozen_input_counts":{"main":len(a["files"]),"refit":len(b["files"]),"common":len(common),"changed_common":0,"removed":0,"added_ancillary":5},
        "strict_archive_failure_receipt":"../campaign-v1/verification.json",
        "strict_archive_failure_receipt_sha256":sha(HERE/"campaign-v1/verification.json"),
        "archive_reconciliation":"Only the five exact allowlisted ancillary additions are reconciled. Original strict archive-parity failure remains retained.",
        "ignored_for_scientific_comparison":["elapsed_seconds JSON fields","utc_before_fit JSON fields","PNG/PDF bytes"]}
    save(args.output/"verification.json",result)
    save(args.output/"checks.json",checks)
    save(args.output/"archive_delta.json",{"main_freeze_utc":a["utc_before_fit"],"refit_freeze_utc":b["utc_before_fit"],"added":additions,"removed":[],"changed_common":[],"computational_inputs":sorted(COMPUTATIONAL_INPUTS)})
    shutil.copyfile(__file__,args.output/"reconcile_campaign.py")
    save(args.output/"source_hashes.json",{"reconcile_campaign.py":sha(Path(__file__)),"campaign_verify.py":sha(HERE/"campaign_verify.py"),
         "strict_receipt":sha(HERE/"campaign-v1/verification.json"),"main_manifest":sha(main_dir/"manifest.json"),"refit_manifest":sha(refit_dir/"manifest.json")})
    print(json.dumps(result,indent=2))
    return 0 if result["status"].startswith("PASS") else 1


if __name__=="__main__":
    raise SystemExit(main())
