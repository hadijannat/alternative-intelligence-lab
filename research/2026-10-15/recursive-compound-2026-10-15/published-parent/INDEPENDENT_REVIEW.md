# Independent reference comparison review

cpcm_memory_design independently parsed the raw XML and reproduced the sole196-atom initialization molecule, identical geometryCML coordinates, SINGLE POINT run label, method fields and all checked source/provenance hashes. No final optimized geometry is established by this record.

Both582-entry frequency arrays contain49negative values. Thirteen uniquely matched ScanFreq replacements leave36conditionally negative entries (34below-20cm-1). This is accounting of explicit records, not a definitive corrected spectrum or minimum verdict. The report preserves that distinction and avoids subtracting ADF bonding energies from PySCF absolute energies.

At the fixed1.2A contact threshold the reviewer independently obtained4two-H and24one-H oxygen sites in the published geometry, versus16two-H and0one-H in P0_A. Every H lies within the threshold; nearest versus next-nearest O differs by at least0.636A in the published geometry. The classification is not a near-tie artifact. All three heavy-element pair-distance RMS differences were reproduced and correctly labelled distribution differences rather than mapped displacements.

Verdict: CLEAR for bounded parent-reference comparison. No new SCF, optimization, physical admission, target identity or held-out validation. Geometry history and final-spectrum completeness remain unresolved.
