# Independent October 18 publication review

Checkout reviewed: `PROJECT_ROOT/publication/alternative-intelligence-lab`. Reviewer owns only this outer-workspace evidence file. No checkout edits, source/model reruns, git staging, commit or push were performed. Commands use `python3 -B` to avoid creating bytecode in the checkout; export/tamper tests use temporary directories. This review concerns publication integrity, not chemical validation.

## Initial concrete snapshot

Reviewed `tools/export_october18.py`, `tools/verify_october18.py`, `tests/test_export_october18.py`, the added CI step, generated README/manifest, relevant source sanitization helpers and root license boundaries. Initial snapshot has 216 included authored/provenance files, 9,703,464 published payload bytes, plus generated README and manifest (218 actual files), with no missing requested reviews. The ongoing `spatial-fe-function` subtree is explicitly excluded in this version.

Executed from the checkout:

```sh
python3 -B tools/verify_october18.py
python3 -B -m unittest discover -s tests -p test_export_october18.py -v
```

Both exit 0: verifier reports `PASS_OCTOBER18_PUBLICATION_ONLY`, zero scientific reruns; all four initial tests pass. Test scenarios cover source/publication hash distinction under sanitization, symlink and tool-envelope exclusion, fresh destination enforcement, failure-log allowlisting, native/source exclusion, candidate-ledger semantic tampering, removal of a mandatory failure log, and insertion of an unlisted payload. The CI invokes the verifier and this test suite using standard-library dependencies.

## Independent source-to-publication verification

A separate read-only Python invocation loaded the manifest, recomputed SHA256 from every included `source_path` under the original research workspace, scanned all published text including generated README and manifest, and invoked `export(source, temporary_destination)` in a fresh temporary directory. Binary observables:

- All **216 original source hashes match** live files; no source mismatch.
- **46 transformed files** retain explicit transformation records and distinct source/publication hashes.
- Independently regenerated **all 218 files byte for byte**, including manifest and generated README; no differences.
- Whole-snapshot host-home and recognized credential-pattern scan reports **zero matching files**, including text not examined by the per-record verifier.
- All six explicit failure artifacts are retained: founder-repair and regeneration execution failures, regeneration execution summary, state-template failures, Fe-site extraction failures, and remote-Fe execution log.
- Exclusions report 12 private/runtime subtrees, 676 third-party payload/registry entries, 3 native/annotated image entries, 2 one-to-one native-cell dumps, and 1 ongoing iteration subtree.

The seven included PNGs correspond to authored plotting `savefig` outputs, not source figure crops. PNG text metadata was parsed directly and checked for the same host/credential patterns; no hits. The included NPZ passes ZIP CRC and contains only `dt.npy`, `coarse.npy`, `fine_dt.npy`, and `fine.npy`. Native movies/PDFs/workbooks, source crops, raw regeneration files and consultation captures are excluded. No broad claim of detecting every possible secret or rights issue is made from pattern scans.

The snapshot README correctly distinguishes original frozen scientific hashes from sanitized publication hashes, maps the original contract/review paths, preserves source URLs/hash receipts, and states that excluded native inputs must be reacquired. It expressly declines checkout-only scientific reproducibility, scientific validation, and completed life/intelligence claims. Licenses preserve third-party rights; the MIT code license is scoped to original code, and LICENSE-DATA limits its grant to original material rather than relicensing acquired sources. Original generated figures and derived analyses are not presented as newly measured chemistry.

## Actionable initial finding: saved-result semantic guard gap

The current projection itself retains the remote-Fe convergence failure correctly. However, the initial verifier checks the corresponding negative ledger without checking the actual `results/analysis.json` failure flag. This was independently demonstrated in a temporary snapshot:

1. Copy the dated snapshot to a temporary directory.
2. Set remote-Fe `results/analysis.json` → `checks.step_convergence_below_1e_minus_5 = true`.
3. Update that record's manifest published SHA256/size and total bytes, leaving the negative ledger unchanged.
4. Invoke `verify(temp_snapshot)`.

Observed result: **`PASS_OCTOBER18_PUBLICATION_ONLY`**, despite the saved numerical failure becoming a pass. Existing coordinated-manifest tamper tests protect the candidate negative-ledger flag but do not cover this result-level contradiction.

Requested correction: directly protect the actual false convergence result, insufficient candidate statuses with empty fits, null AEM/CEM strict endpoint results and absence of five-hour synthetic reversals, with a coordinated result-plus-manifest tamper regression. This is a publication consistency issue; no scientific model rerun is required. Root was notified before approval.

## Semantic correction verified

Root's publisher added direct assertions on the remote numerical result: convergence remains false; the exact three candidate entries have `insufficient_data`, empty fits and 2/6 training/reserved counts; AEM/CEM strict endpoint results remain null; the five expected ka entries retain false five-hour reversal flags. The new regression exercises eight separate result promotions/removals while coordinating published hashes and sizes in the manifest.

Re-executed the same verifier and the full changed test module: **both exit 0; five tests pass**, including all eight coordinated-result tamper subcases. The original demonstrated convergence promotion is now rejected. No scientific model ran. The actionable initial finding is **resolved** for the current 216-file snapshot.

Current publication code/projection review has no remaining blocker. Terminal snapshot approval remains pending the parent-requested narrow delta review if the independently reviewed spatial iteration is added before publication. No such delta is approved by this section.
