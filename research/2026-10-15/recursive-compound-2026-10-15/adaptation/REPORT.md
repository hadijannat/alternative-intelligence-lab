# Recursive adaptation complement screen — 15 October 2026

**Four sequential proposals checked; zero verified complements added.** WO3·H2O, VO2 and Ag2S remain unresolved integration candidates. Direct adoption of the published 200 °C NiO gas protocol is rejected for the ambient aqueous architecture. The nominal `[MoVI34WVI VVO112(H2O)16]9−` identity and operating window are unverified, so none can be called target-compatible. No intelligent-life endpoint has been demonstrated.

The scope is sensing, persistent state, local update and state-dependent action that improves measured resource use or maintenance under withheld conditions. External energy and training signals are permissible. The audit instead identifies where updates occur, what the apparatus computes, and whether learned state survives replacement or copying of its material carrier.

## Sequential decisions

1. **WO3·H2O → HxWO3·H2O:** start with the closest aqueous proton/electron-state candidate. The validated Spencer XML supports acidic electrochemistry; it also identifies hydrogen evolution as a competing outlet. Replaying the existing finite-capacity calculation confirms conservation constraints, not coupling. Next alternative: structural memory that need not retain reactive reducing equivalents. [Primary paper](https://doi.org/10.1039/D4SC00102H)
2. **VO2:** the reopened manuscript describes 2.1 V, 10 μs pulses on a 3 μm device, about 1.4 μs initial incubation, tenfold shortening after 10 ms and history still detectable after 10,000 s. This is credible retained material history. A chemical sensor, actuator and aqueous-compatible interface remain absent. Next alternative: a material that responds directly to chemical stimuli. [Primary paper](https://doi.org/10.1038/s41928-022-00812-z)
3. **NiO:** fresh primary text distinguishes 900 s H2 OFF forgetting from 45 s OFF habituation at 200 °C, with 900 s ON exposure and a 15 s O3 intervention. That protocol cannot simply be placed in the parent-like 24.3 °C aqueous assembly. Room-temperature light response is a distinct lead, not validation of the gas protocol at low temperature. The associated clustering task is simulated. Next alternative: an ionic update device with room-temperature measurements. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8488684/)
4. **Ag2S/Ag:** newly acquired full primary text specifies 200 × 200 nm cells, Ti/Pt contacts, 50 μs pulses at ±400 mV, and a 100 s rest probe. The material performs local ionic updates; motion learning is a system-level simulation. A joint aqueous function and renewal of learned material remain unmeasured. [Primary paper](https://doi.org/10.1038/srep39216)

The exact formulas, functions, checks, conditions, contrary evidence, update location and next alternative are machine-readable in [candidates.json](candidates.json). No unknown rate, occupancy, survival probability or learning score was assigned. Reported device voltages were not converted to solution potentials.

## New quantitative constraint

The Ag2S primary Eq. 1 was downloaded as an image and visually inspected: `τfac = a Gfinal^b`, with reported `a = 3.40 × 10^12 s/S^4`, `b = 4`. Evaluation at the reported 1 and 3.5 mS endpoints gives **3.40 and 510.2125 s**, a **150.0625-fold** ratio. A deliberately wrong mS-as-S input changes the result by 10^12, detected by the check. These are evaluations of an empirical fit, not newly measured lifetimes. The authors identify failure of their first model for paired pulses and variability in the refined model. Do not use either endpoint as a freely suspended Ag2S retention constant or a prediction for Mo34WV.

This matters for an adaptive resource interface: matching only stimulus energy would leave materially different initial states and relaxation behavior uncontrolled. A fixed “memory lifetime” cannot represent all programmed states. Memory-ablation controls must match the actual measured state and probe disturbance.

## Architecture and target compatibility

The physically local contrastive-learning network provides a useful architecture comparator: local analog circuits update capacitor voltages, while the computer supplies inputs/labels, measures outputs and enables or freezes learning. That is physical learning with external supervision. It does not establish a carbon-free entire apparatus or an aqueous renewing chemical system. [Primary paper](https://doi.org/10.1073/pnas.2319718121)

I attempted the next genuinely new check suggested by the prior information dossier: download the [experimental dataset](https://doi.org/10.5061/dryad.8w9ghx3vx) and inspect TRAIN/TEST overlap and held-out behavior. Metadata and publisher digests were obtained. Both API downloads returned 401; public file-stream downloads returned 403. **No measurements were downloaded or replayed.** The presence of TEST in a README is therefore not promoted to verified held-out evaluation.

The smallest candidate architecture remains an immobilized hydrated-WO3 state element with separately defined proton/electron paths, an environmental input, and an output that changes measured resource allocation. This is a proposal. The parent Mo36 comparison uses approximately pH 1.7 and 24.3 °C; the nominal substituted target has no established pH/redox/temperature window. The reviewed oxide experiment uses 0.5 M H2SO4 and H2 purge. Separate acidic operation is insufficient to establish a common working medium. No candidate earns compatibility from an inferred pH or a guessed electrode-potential conversion.

The old counterion model independently reinforces this architectural requirement: charged transport needs a countercharge path; the electrical terms cancel for the specified electroneutral routes. Its formal gradients and hypothetical cluster proton count are not a measured pump or target synthesis. The WO3/Mn/Ce model confirms finite empty-site capacity and exact formal reversal. It supplies neither a favorable reaction direction nor a kinetic learning rule.

## Checks and artifacts

No active `ulw-loop` attempt existed (status returned `ULW_LOOP_PLAN_MISSING`). Evidence is kept under this assignment's `.omo/evidence/` without editing existing labs.

| Scenario | Invocation | Binary observable | Captured artifact |
|---|---|---|---|
| Counterion balance replay | `python checks/run.py` | Existing runner exit 0; 24 route cases, 72 decompositions and all assertions true | `.omo/evidence/counterion.stdout.json` |
| Finite WO3 capacity replay | Same invocation | Existing runner exit 0; 63 initial states; all corruption controls rejected | `.omo/evidence/wo3_capacity.stdout.json` |
| Ag2S fit/unit check | Same invocation | Exact Decimal values and 10^12 unit-negative-control factor match assertions | `.omo/evidence/checks.json` |
| Candidate/source accounting | `python build_records.py` | Four ordered candidates; zero admissions; source hash assertion passes | `.omo/evidence/records.stdout.txt` |
| Experimental learning-data replay | Public API and file-stream requests in `raw/acquisition.json` | **FAIL: download blocked; replay not executed** | `raw/acquisition.json` |

Run invocations are relative to this directory. The model runner paths, SHA256 hashes, detailed outputs and interpreter invocation are captured in `.omo/evidence/checks.json`. Source hashes and access limits are in [sources.json](sources.json). Passing accounting or arithmetic is not a physical success criterion.

## Specific next test

**First acquire a joint, species-resolved compatibility time series for identified Mo36 and WO3·H2O in one stated medium, before extending to structurally identified Mo34WV.** Compare two measured initial oxide proton states and an unwritten control; track cluster identity/activity, oxide state, dissolved metals and charge/H2 balance before and after the intended resource cycle. Use a read-only or calibrated low-perturbation state probe. Failure to retain both identified active components rejects that interface.

If this succeeds, freeze a resource-allocation task and withhold entire input schedules and one input–resource relation. Compare the proposed local update with update-disabled, memory-reset and matched-energy open-loop controls. The causal endpoint is an increase in measured active-cluster maintenance or resource yield that disappears when only the state-to-action route is broken. Log what computes each update. Finally replace a measured fraction of state-bearing material and test whether its new fraction preserves the learned function; the present evidence supplies no such renewal or copying result.

Skipped: physical experiments, target synthesis, speculative kinetic simulation, paid computation, publication and blocked dataset replay. Main risk: interfacing useful memory components may erase the state or destroy the active cluster; full intelligent life remains unverified.
