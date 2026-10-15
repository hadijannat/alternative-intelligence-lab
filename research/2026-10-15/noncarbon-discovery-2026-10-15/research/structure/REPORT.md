# An evidence-grounded starting structure exists for the parent, not the target

Reviewed 15 October 2026. Two public crystallographic coordinate files for carbon-free **parent Mo36 salts** were acquired and checked. They permit a future parent-based modeling study. They do **not** establish the existence, stability, site occupancy or function of hypothetical `[Mo(VI)34W(VI)V(V)O112(H2O)16]9−`. No substituted target geometry or quantum-chemical result was generated.

## Acquired coordinates and a preserved data-quality failure

| Deposited structure | Identity and structural scope | Actual check |
|---|---|---|
| [COD 2107026 CIF](https://www.crystallography.net/cod/2107026.cif) | K8[Mo36O112(H2O)16]·nH2O; deposit uses n=37, while the 1982 study reports variable hydration around 36–40. Parent anion, inorganic counterions. | 18 independent Mo sites, 4 symmetry operations and Z=2 give 72 Mo per unit cell, 36 per formula. Sixteen independent Mo sites have six O neighbors within 2.6 Å; Mo8 and Mo10 have seven. No H positions. |
| [COD 4030345 CIF](https://www.crystallography.net/cod/4030345.cif) | Na8[Mo36O112(H2O)16]·58H2O; Krebs, Stiller, Tytko and Mehmke, *European Journal of Solid State and Inorganic Chemistry* 28 (1991), 883–903. | 18 independent Mo sites, 8 symmetry operations and Z=4 give 144 Mo per cell, 36 per formula. No H positions. A suspicious Mo6 environment is retained below. |

The potassium record cites the [1982 primary structure study](https://doi.org/10.1107/S0567740882007018). Its sum formula `H106 K8 Mo36 O165` agrees with sixteen coordinated waters plus 37 lattice waters. Some O and K sites have partial occupancy. In this deposit, all oxygen type symbols are `O-2`, including water O: those labels must not be used to assign a chemically meaningful charge to the full salt. Charge accounting here uses the explicit formula and neutral waters. The earlier [1979 primary report](https://doi.org/10.1039/C39790000780) describes the potassium salt with 36 lattice waters and both MoO6 and MoO7 environments.

The sodium record contains a **Mo6–O13 distance of 1.335(16) Å** in its bond table. Independent calculation from its cell and fractional coordinates gives **1.3352 Å**, with only four O neighbors of Mo6 inside the declared 2.6 Å cutoff. The potassium record does not share this anomaly. This is a source-data quality flag, not a demonstrated exotic bond or an automatic correction. The original sodium refinement/publication must be checked before using that site. Original labels such as `M04`, `OS` and `NaS` are preserved. Neither downloaded CIF was modified.

The neighbor cutoff is an audit aid, not bond-order inference, a proof of coordination chemistry or a general CIF validator. The small checker handles the exact single-line loops and monoclinic cells acquired here. Formula and neighbor checks are recorded in [checks.json](checks.json); full acquisition URLs, file hashes and a failed CCDC lookup are in [acquisition.json](acquisition.json).

## What remains ambiguous when converting a parent to Mo34WV

The parent anion contains 36 metals, 112 framework oxygens and sixteen waters: **164 heavy atoms and 196 atoms with explicit water hydrogens**. Replacing two *different* metal positions by distinguishable W and V gives at most **1,260 ordered site assignments before symmetry reduction**, not 1,260 novel compounds or calculated stable isomers. Different parent salts and proton/water states add further modeling choices. Selecting only peripheral six-coordinate positions would be a hypothesis to compare with alternatives, not measured selectivity.

The target's −9 charge follows from `34×6 + 6 + 5 − 112×2`; the formally V(IV) counterpart is −10 if all other assignments remain fixed. The −9 formula has 2,590 electrons in an all-electron count. Its even electron number alone does not determine its electronic state; the additional electron in a −10 state need not localize on V. No orbital occupation, spin multiplicity, reduction potential, equilibrium constant or lifetime has been calculated.

The published [2006 sensitive-site study](https://doi.org/10.1007/s10876-006-0058-9), available as an [author PDF](https://www.chem.gla.ac.uk/cronin/images/pubs/Long2006JClusterSci.pdf), supplies a useful warning. Its related Mo36 structures contain fourteen waters, organic triethanolammonium ligands and different sodium coordination. These are not interchangeable with the sixteen-water, inorganic parent salts. Its DFT calculations began from crystallographic coordinates, supplied missing water H positions and examined charge distributions with and without continuum solvation. It does not validate W/V substitution or aqueous survival of our target. Those crystallographic deposits are CCDC 292391/292392; this task did not recover their coordinate files.

Also, CCDC **1916468**, referenced by the 2020 autocatalysis paper, belongs to the **Ce-containing large-wheel compound** described in its SI. It must not be cited as the parent Mo36 or proposed Mo34WV structure. This distinction was checked against the already retained [2020 SI](../pom/raw/miras2020_si.txt).

## Minimum requirements before a defensible electronic-structure comparison

1. Use the potassium heavy-atom structure as a traceable parent reference, expand its symmetry and isolate a complete connected anion. Resolve water O, counterions and any protonation; add H positions explicitly and test alternative proton/water configurations. This conversion has not been performed here.
2. Compare the parent, each single substitution and defined W/V positional isomers in the same environment. Break inherited parent symmetry when necessary. Preserve structures that rearrange or dissociate; do not constrain the desired topology until it appears stable.
3. Use a documented treatment of Mo/W relativistic effects, suitable basis/pseudopotentials, solvent/counterion assumptions and multiple electronic states. Validate the parent against known geometry and an independently measured observable before interpreting target differences.
4. Evaluate atom-, charge- and proton-balanced substitution/redox reactions against explicit competing species. Raw total energies for different formulas are not formation free energies. A local geometry minimum would not establish solution persistence, an assembly mechanism, autocatalysis, functional inheritance or intelligence.

This is a modeling prerequisite list, not a wet-laboratory procedure or a completed DFT study. A force-field substitution or relabeled parent CIF would conceal the main uncertainty, so none was produced.

Reproduce the bounded checks with `python3 noncarbon-discovery-2026-10-15/research/structure/check.py` from the workspace root. The acquired Gd-containing COD 1526957 record is retained as a rejected structural substitute: its additional metals and different water assignment are not the parent target.

Skipped quantum calculations, exhaustive coordinate searches and correction of the sodium source anomaly. The target remains an unverified composition; even a stable optimized structure would provide no evidence of life or intelligence.
