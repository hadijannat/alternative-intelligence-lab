# W/V numerical comparison: prepared, unrun

The two previously selected WO4(2-) and VO4(3-) geometries are validated against their pinned CML final geometries and scoped charge/spin records. Thirty preparation pins match. Four source/gate test methods passed, including malformed digest, duplicate/missing file, conflicting charge, wrong spin, geometry mismatch and failed-result controls. Independent prelaunch review is CLEAR. No J/PCM operator or SCF has run; run-v1 is absent at this checkpoint.

Basis metadata: WO4 has88orbital functions,535auxiliary functions,48explicit electrons and60Wcore electrons removed by the ECP; VO4 has87orbital functions,572auxiliary functions and58explicit electrons with all-electronV. These counts are preparation evidence, not chemical predictions.

The frozen protocol permits two sequential180second/2GiB children, each with one direct and one MemoryRI SCF, after the parent pilot terminates. Root enforces this sequencing; the driver has no automatic parent-process lock. Both methods use the same fixed geometry, initial density and solvent. Original Mo numerical thresholds remain unchanged. Failed results must be retained, with no tuning or automatic retry.

These are external fixed-geometry numerical challenges for the W/V method gap, not experimental held-out validation or proof of incorporation into the target. Source method differences, target identity, basis/cavity sensitivity, redox/spin states and integration remain unresolved. Preparation and prelaunch review do not establish a pass.
