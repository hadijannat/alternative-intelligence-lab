# New Mo-ECP/direct-PBE/continuum method qualification

**The bounded runtime and one nuclear-gradient component pass after two diagnostic corrections. The parent P0/PT57 input remains unbuilt and unadmitted.** No parent hydrogen coordinates, parent SCF, optimization, pKa or chemical validation was produced.

## What was missing and what was tested

The prior Mo36 runtime diagnostic used gas-phase H2/RHF and water/PBE0 plus an atomic Mo basis build. The targeted search of prior `discovery-loop/experiments` Python/report files found no `PCM`, `ddCOSMO` or `with_solvent` implementation. The exact command, empty output and exit 1 are saved in `.omo/evidence/prior-audit.json`; this is a scoped search, not proof that no hidden or external calculation exists. Repeating the old water test would not check the missing combination.

New references are **explicitly hypothetical**, fixed 1.75 Å Mo–O geometries: tetrahedral MoO4 with charge −2, and planar trigonal MoO3 with charge 0. No experimental bond length or optimized species is claimed. Both use formal Mo(VI)/O(−II) bookkeeping and singlet trial states. With the 28-electron Mo ECP, the models have 48 and 38 explicit electrons respectively (87 and 73 spherical AOs). Nuclear effective-charge sums minus integrated electrons reproduce their declared charges. The neutral control is a separate electron/charge/runtime test; its total energy is not compared to the anion as a reaction energy.

Actual API: `mf = pyscf.solvent.PCM(dft.RKS(mol))`; `mf.with_solvent.method='C-PCM'`, epsilon 78.4, Lebedev order 17, radius scale 1.2, probe radius 0 Å, unfrozen ground-state solvent. PySCF 2.14.0 uses modified Bondi radii; its Mo entry is 3.779450359404 bohr (2 Å), scaled by 1.2 for the cavity. This default radius is an implementation choice, not a validated Mo-cluster radius. The installed PCM source hash/path is recorded in each solvent result; the package itself warns that PCM remains experimental.

Electronic settings: PBE/def2-SVP, Mo def2 ECP, spherical basis, RKS spin 0, numerical grid level 2, final energy tolerance 1e-11 Eh, orbital tolerance 1e-7, 60-cycle limit. Direct J/K evaluation is made explicit by binding `pyscf.scf.hf.SCF.get_jk` to the method; the inherited RHF path otherwise may cache small-system ERIs despite `direct_scf=True`. Every successful case records no cached four-center ERI and a created direct optimizer. No density fitting was used. Five thread environment variables requested one thread, without independently proving actual worker count.

Four SCFs were run: anion gas, anion C-PCM epsilon 1, anion C-PCM epsilon 78.4, neutral C-PCM epsilon 78.4. Each child was capped at 90 seconds and 60 cycles; the PySCF memory setting was 512 MB, which is a hint, not an OS limit. The later gradient implementation has its own minimum-memory setting visible in retained source; no physical RAM ceiling was enforced.

## Results and two preserved failures

The final four cases converged with explicit solvent-aware orbital-gradient norms below 5.6e-8 and correct integrated electron counts. Their measured worker times were 6.25, 9.34, 7.56 and 3.84 seconds respectively; these are small-reference timings, not parent estimates. Gas and epsilon-one energies agree within 1.2e-12 Eh; the epsilon-one solvent contribution is exactly zero. The water anion's electrostatic PCM term is −0.346134809637 Eh. These are internal runtime controls, not experimental solvation energies or validated aqueous stability.

Failure 1: an initial anion-gas calculation had a convergence flag but a 2.878e-5 orbital-gradient norm, above the declared 1e-5 acceptance bound. Its original source, raw log and output remain in `.omo/evidence/attempt1/`. SCF tolerances were tightened and the complete four-case scenario rerun.

Failure 2: the default `mf.get_grad(coeff, occ)` gave 0.0355 in the solvent case even after tighter SCF convergence. Inspection of the installed source shows that inherited `SCF.get_grad` constructs hcore + veff without the separate PCM potential; `SCFWithSolvent.get_fock` adds it. The corrected orbital diagnostic is:

```python
fock = mf.get_fock(dm=mf.make_rdm1())
orbital_gradient = mf.get_grad(mf.mo_coeff, mf.mo_occ, fock)
```

The original failure is retained in `attempt2/`, along with the source used. Both default and corrected norms are recorded in final results. This is an API/diagnostic distinction, not evidence of a physical change.

## Nuclear derivative gate

The requested follow-up used the same hypothetical anion/water reference and all the same SCF/grid/cavity settings. The coordinate is the first O atom's x coordinate. Central differences use h=1e-3 and 5e-4 bohr; threshold **1e-4 Eh/bohr was fixed before execution**. There were four displaced-energy evaluations plus one reference analytical gradient, each capped at 90 seconds. All five SCFs converged.

The initial default nuclear gradient **failed**: analytical −0.0173090677572 versus finite differences −0.0177549678426 and −0.0177549572982 Eh/bohr, discrepancies 4.45900e-4 and 4.45890e-4. `derivative-result.json` retains `pass_all=false`; the threshold was never relaxed.

Installed RKS gradients default to `grid_response=False`. One additional capped reference calculation changed **only analytical `grid_response=True`**, retaining the original finite differences. `grid_response.py` reuses the exact original driver text with an asserted single replacement and distinct output filenames; it records that source hash. The corrected analytic value is −0.0177629143194, giving discrepancies **7.94648e-6 and 7.95702e-6 Eh/bohr**. Both pass the original threshold. The additional child took 10.45 seconds including process startup (9.78 seconds inside the worker). The original failed result is untouched. This supports one force component at one hypothetical geometry, not all coordinates, Hessians, proton forces or an optimized cluster.

Future code must use:

```python
gradient = mf.nuc_grad_method()
gradient.grid_response = True
forces_as_energy_derivatives = gradient.kernel()
```

The output is the energy gradient, not its negative (physical force). Retain the solvent-aware orbital check separately.

## What can proceed

The local **method machinery** can now be selected explicitly for a proposed input-build/pilot stage, with the two diagnostic fixes above. The parent input itself **cannot yet be admitted**: no 32-H model has been constructed, water assignments remain provisional, H orientations/protonation alternatives are unresolved, and no parent electronic-state, diffuse-basis or solvent/cavity sensitivity has been checked. Any later P0/PT57 input must label H coordinates as hypothetical and preserve both proton-location alternatives. No new structural admission is made here.

The 386-point small-anion cavity does not forecast full-parent cost. At Lebedev order 17, the 196-atom parent has an upper pre-overlap count of 21,560 surface points; one dense float64 square matrix at that count is about 3.46 GiB. PCM creates several matrices/solve workspaces, and overlap screening depends on the unbuilt geometry. No parent cavity allocation or reliable peak-memory/time estimate was made. Grid level 2/order 17 are runtime-check choices, not converged quadratures for the parent. A small-system derivative pass supplies no permission to bypass the existing 900-second/20-cycle initial parent pilot budget or its input checks.

## Exact evidence and reproduction

Use the existing interpreter `discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B` from the workspace root with:

1. `recursive-compound-2026-10-15/identity/next-step/method-qualification/run.py` — four SCFs; final exit 0, `result.json` status `PASS_RUNTIME_ONLY`, raw native logs and command outputs in `.omo/evidence/receipts.json`.
2. `recursive-compound-2026-10-15/identity/next-step/method-qualification/derivative.py` — five SCFs and default analytical gradient; expected final exit 1, `derivative-result.json` false, raw outputs in `.omo/evidence/derivative-receipts.json`.
3. `recursive-compound-2026-10-15/identity/next-step/method-qualification/grid_response.py` — one reference SCF/gradient with grid response enabled; executed as a child with a 90-second timeout and the same one-thread environment. Exit 0 and `grid-response-result.json` true; exact invocation, runtime and output in `.omo/evidence/grid-response-receipt.json`.
4. `python3 recursive-compound-2026-10-15/identity/next-step/method-qualification/check.py` — artifact/threshold/charge consistency check, retains the default-gradient failure rather than erasing it.

The final root `.omo/evidence/identity-method-receipt.txt` combines actual native outputs with the independent check invocation. No broad chemical conclusion follows from a numerical PASS.

Skipped parent H placement/SCF/optimization and experimental calibration. Main risk: small-reference internal consistency does not establish parent accuracy, stability, pKa, life or intelligence.
