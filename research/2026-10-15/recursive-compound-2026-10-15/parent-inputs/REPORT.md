# Hypothetical parent input construction

Four computational inputs were constructed under the frozen protocol. All use the provisional O57–O64 aqua assignment and model-built H. Physical admission remains false; deposited H positions and solution protonation remain unresolved.

| Input | Verdict | H–H minimum Å | H–other-O minimum Å | H–Mo minimum Å |
|---|---|---:|---:|---:|
| P0_A | PASS_COMPUTATIONAL_INPUT_ONLY | 1.549751565 | 2.137261902 | 2.499740214 |
| P0_B | PASS_COMPUTATIONAL_INPUT_ONLY | 1.549751565 | 1.983553284 | 2.778280566 |
| PT57_A | PASS_COMPUTATIONAL_INPUT_ONLY | 1.549751565 | 1.595820286 | 1.713071746 |
| PT57_B | PASS_COMPUTATIONAL_INPUT_ONLY | 1.549751565 | 1.595820286 | 1.713071746 |

All four have zero clashes under the preregistered gross thresholds. PT57 includes an H–Mo contact at approximately 1.713 Å: passing the 1.50 Å gross gate does not establish favorable coordination or physical feasibility. No geometry was relaxed or selected on energy.

Each doubly protonated site differs between A/B by more than 0.1 Å under an unordered H-set comparison. PT57 acceptor OH is the same in both starts by construction; donor H1 and all fifteen waters differ. H2 alone changes ownership O57@0→O4@0; the full 164-heavy-atom mapping is preserved exactly in metadata and round-trips exactly through the new XYZ files.

Ten rejection controls exercise missing H, changed heavy coordinate, wrong ownership, missing ownership, nonfinite H, wrong element, wrong index, H–H overlap, H–other-O overlap and H–Mo overlap. Each rejects for the intended reason; complete failures and clashes are in checks.json. A complete second build produced identical bytes for all four XYZ files, metadata.json and checks.json.

Invocation: `python3 recursive-compound-2026-10-15/parent-inputs/build.py`. Evidence: `.omo/evidence/receipt.json` and `.omo/evidence/build.stdout.txt` within this directory. No active attempt directory was returned by `omo-agent-toolkit ulw-loop status --json`.

No SCF, energetic optimization, global score tuning, H relaxation, physical admission, target claim, or life claim was performed. Original source and full-hydrated admission files were not edited.
