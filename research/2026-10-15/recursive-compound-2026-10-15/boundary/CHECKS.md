# Validation record

No current ulw-loop attempt was available: `omo-agent-toolkit ulw-loop status --json` returned `ULW_LOOP_PLAN_MISSING`. Evidence is therefore under this owned directory's `.omo/evidence/`.

Run from the workspace root:

```sh
python3 recursive-compound-2026-10-15/boundary/checks.py
```

| Success criterion | Exact scenario / invocation | Binary observable | Captured artifact |
|---|---|---|---|
| Five concrete alternatives with findings, limits, disposition and next alternative | Above invocation validates `candidates.json` | Exactly five ordered unique candidates; required fields nonempty; zero verified complements | `.omo/evidence/checks.json` and `candidates.json` |
| Retain primary source evidence with limits | Above invocation checks `sources.json` and `raw/acquisition.json` | Every referenced artifact exists and is nonempty; every successfully downloaded file matches size and SHA256 | `sources.json`, `raw/acquisition.json`, `.omo/evidence/checks.json` |
| Bounded quantitative work with no invented permeability | Above invocation evaluates source-reported inventories and formal reactions | Inventory bounds hold; all atom/charge residuals zero; zero/one-cluster counterexample both obey same elemental inventory | `.omo/evidence/checks.json` |
| Read prior relevant support work without treating reports as empirical measurements | Direct inspection of prior report, encounter code, FeIII model and protocol; above invocation records hashes | Named source files exist with recorded SHA256; report limits match code's assigned fields and omitted target kinetics | `.omo/evidence/checks.json` `prior_artifacts_read_sha256`; `REPORT.md` |
| Specific next measurement and strict joint-function gate | Review `REPORT.md` and candidate records | Contact/exchange comparison, fraction-resolved identity/activity, independent flux and subsequent renewal specified; no joint verification claimed | `REPORT.md`; `candidates.json` |

The last row is a document-content check, not an executed physical assay. Source acquisition and interpretation do not count as experimental replication. No physical success criterion is claimed complete.
