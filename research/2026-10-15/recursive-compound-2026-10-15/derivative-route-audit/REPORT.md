# Can the current model execute the registered chemical comparison?

Date: 2026-10-16. Decision: **the four-start P0/PT57 H-only relaxation and orbital-stability campaign is not ready**. The serial RHS pair passed its limited repeat criterion, while full-J acceptance and parent SCF remain unresolved. Independent source inspection identifies additional derivative/response dependencies. This audit executes arithmetic and reads code; it does not reproduce a native gradient failure or perform chemical validation.

## Nuclear derivatives

The frozen `cpcm-blocked/blocked_pcm.py` rejects gradients, Hessians, response and stability. `MemoryPCM` inherits that boundary and retains a solvent factor instead of the upstream dense cache. Removing those guards would not implement the missing capabilities:

- Installed `grad/rks.py` calls the gradient object's `get_j`; `grad/rhf.py:381` dispatches its own direct `int2e_ip1` contraction. The project RI implementation installs an instance `get_jk` and `_rij_df`, without the standard DF gradient machinery. Bypassing the guard would mix RI electronic energies with a direct Coulomb derivative contribution. This is a source-level incompatibility, not an observed numerical discrepancy.
- Installed `solvent/grad/pcm.py:262` requests `A,D,S,K`, absent from the custom factor-only cache.
- Its derivative-integral loop uses a minimum block size of400 surface points. At3068 AOs, a full400-point three-component tensor alone requires90,361,190,400bytes (84.15541649GiB). The actual last block may be smaller; this is allocation arithmetic, not measured RSS. It exceeds the previously observed36GiB host memory without counting other allocations.
- One dense auxiliary-metric derivative at19612 auxiliary AOs requires9,231,133,056bytes (8.59716260GiB), before the factor and other work arrays. Bounded derivative contractions would require a separate implementation and qualification.

A consistent low-code nuclear route is central differences of fully reconverged, same-method total energies. Each displaced geometry needs a fresh molecule, RI object and solvent surface. For32 movable H atoms, the fixed heavy framework leaves96 coordinates:192 displaced SCFs for one gradient at one start,768 across four starts, or1536 for both h and h/2. Center energies, line searches, subsequent optimization steps and failed SCFs are additional. No rigid-body coordinates are subtracted because the heavy framework is fixed.

The observed two serial RHS contractions averaged414.111371000472seconds. Assigning that time to just one RHS in each of768 displaced calculations gives3.68098996444864days. This is conditional work accounting, **not a runtime forecast or a guaranteed lower bound**: displaced calculations may differ, and full SCFs require other work and potentially many iterations. Neither parent convergence nor complete optimization cost has been measured.

An analytical successor must include moving-auxiliary RI derivatives, Pulay and one-electron/ECP terms, nuclear forces, XC-grid response, and moving SWIG cavity/surface derivatives. The prior direct-method `grid_response=True` repair qualified one O-force component; it does not qualify the current RI/memory implementation or H forces.

## Orbital stability

Internal real-RKS stability uses the full `get_fock` entry point and a real symmetric response density. The same ordinary RI J operator could in principle serve that response density, but no such integrated response implementation is qualified today.

At fixed geometry let G map AO density to its positive electronic surface potential, f=(epsilon-1)/epsilon and S be the C-PCM surface matrix. The factor-based candidate is delta_q=f*S^-1*G*delta_P and delta_V=-G^T*delta_q. It must omit the nuclear offset and leave ground-state caches unchanged. This is a derived candidate to test against installed stock response and finite differences, not a validated operator. Epsilon1 requires an exact zero response.

The installed response implementation requests K/R, absent from the memory cache. The current `_B_dot_x` is explicitly unsupported. Stock stability also temporarily sets `equilibrium_solvation=True`, which the current guard rejects; supplying `_B_dot_x` alone would not make stability operational.

There is a separate external-channel hazard. Installed `scf/stability.py:340` constructs its orbital Fock as `hcore + get_veff`. The solvent wrapper keeps its potential as `v_solvent` metadata until `get_fock` adds it numerically. That inspected path therefore omits the tagged solvent contribution to its Fock. Internal stability uses `get_fock` correctly. External real-to-complex and RKS-to-UKS channels need independent full-Fock and response handling; an internal-only pass would not establish full orbital stability.

## Decision and next test

Keep every frozen guard and previous failure. Do not launch another parent campaign solely because RHS repetition passed. First test a standalone fixed-geometry solvent-response candidate on an existing retrospective small reference, preserving the unused holdout. This tests one missing component; it does not implement nuclear derivatives, full orbital stability or the registered chemical comparison. The new `cpcm-response-probe` must freeze its tests and resource bounds and pass independent review before native execution.

Before any later relaxation, declare a force criterion, electronic-state-following policy, stability-channel scope and resource plan, and qualify a complete consistent derivative/response route. Exact Mo34WV identity, solution persistence and useful joint function still require characterization. A parent proton-energy ranking cannot establish W/V coexistence in the requested molecule.

The independent `integrated_goal_dependency_audit` reviewer confirmed the dispatch, cache, allocation and external-Fock findings, with the conditional/scope qualifications above. Root separately inspected the installed paths and reproduced the192/768/1536 counts and both memory allocations. The source hash inventory is in evidence.json. No native physics, fit, holdout test, new role or complement admission occurred. Aggregate24/0; all twelve functions remain unfulfilled.
