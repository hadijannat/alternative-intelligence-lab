# Finite-inventory maintenance laboratory

Decision: **SUPPORTED_WITHIN_PHENOMENOLOGICAL_MODEL**. 12/12 paired seeds met every frozen endpoint. This is a conditional mechanism result in an analyst-designed model.

| Arm | Final structure tokens | Surviving new structure | Fraction of requested work paid |
| --- | ---: | ---: | ---: |
| normal | 4.080937 to 4.118856 | 3.990219 to 4.028138 | 1.000000 to 1.000000 |
| no_feed | 0.113717 to 0.113717 | 0.022999 to 0.022999 | 0.162493 to 0.162493 |
| no_renewal | 0.090718 to 0.090718 | 0.000000 to 0.000000 | 1.000000 to 1.000000 |
| extra_leak | 1.445286 to 1.480129 | 1.444539 to 1.479382 | 1.000000 to 1.000000 |

All 48 runs retain their initial state and 600 subsequent steps in trajectories.csv. The maximum absolute material, energy, reservoir or fuel-energy residual is 1.56e-13. Every accepted input is drawn from the finite 30-token external reservoir. Every work payment is capped by available work units. There is no recycling of waste or unrecorded replenishment.

The maximum final-structure relative change on deterministic constant-feed dt/2 refinement is 0.00299864. dt_refinement.json contains both endpoint values, including stored energy. This first-order sensitivity is separate from the frozen replicate decision and provides no physical calibration.

The API is `initialise(fuel, structure, energy) -> State`, `step(state, influx, work, dt, Params()) -> StepResult`, and `debit_work(state, work) -> (State, actual_work)`. Callers must debit accepted_influx from their own finite reservoir and gate task effects on actual_work. Dataclasses are immutable. `validate` rejects negative/nonfinite values and broken ledgers. Dividing an entity requires partitioning all inventories and accounting baselines; subtracting material without a recipient ledger is invalid.

The supplied renewal/catalytic rule and assumed material/work yields explain the effect by construction. This assay checks their consequences, accounting, dependence on supplied feed, and separation of founder material from new product. It establishes no chemical recipe, spontaneously originating catalyst, autonomous living entity, replication, intelligence, evolutionary novelty, or advantage over an optimized engineered maintenance controller. The finite source also rules out interpreting the endpoint as indefinite persistence. Initial structure and work are externally prepared. Preparation energy, molecular kinetics, transport and thermodynamic efficiency remain unmeasured.

Reproduce from the package root with `/USER_HOME/.pyenv/versions/3.12.3/bin/python3 maintenance/run_lab.py --output maintenance/replay-results` using a new output path. Frozen source hashes are checked before every run. The included unit-test record predates the official run. A rerun is computational repeatability, not independent experimental replication.
