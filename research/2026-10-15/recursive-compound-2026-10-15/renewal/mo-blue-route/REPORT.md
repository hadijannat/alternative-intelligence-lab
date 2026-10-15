# Mo-blue route: conversion evidence does not establish target renewal

The [primary supplement](https://doi.org/10.1021/jacs.3c09344.s001) supplies constraints on an electrochemically driven Mo36-to-larger-cluster pathway. It supplies no Mo34WV renewal or functional-inheritance observation. This extends the existing Mo36 source assessment; it adds no new candidate role.

Three method details prevent treating its plots as a calibrated replacement model:

- Page9 scales each species' fitted Raman area to its own maximum of100%. Without species-specific response factors, those curves cannot supply absolute concentrations or a cross-species material balance. A fit R-squared above0.99 does not identify those missing factors.
- Page8 prints15mL of1g/mL sodium molybdate, with acid volumes and nominal H/Mo ratios. Using two nominal acid equivalents per H2SO4, these imply a formula-unit mass of2400–2408g/mol per Mo. Ordinary anhydrous sodium molybdate or its dihydrate cannot reconcile that accounting. The recipe discrepancy remains unresolved; no concentration typo or hydration state is silently substituted.
- Page9's ESI measurements use1:39sample/acetonitrile dilution after collection. The30-minute bound concerns standing before dilution; total time to scan completion is unspecified. These measurements do not directly establish unperturbed operando solution identity. Page8 also describes an anolyte Raman connection while specifying cathode electrolytes, leaving a sampling-side ambiguity.

The apparatus uses externally driven flow, carbon-paper electrodes, Nafion and IrO2. These dependencies must be retained when discussing system integration. Precursor fragmentation and assembly into another cluster do not demonstrate repair of the original proposed compound.

[analysis.json](analysis.json) and `audit.py` preserve the arithmetic and missing quantities. Two synthetic unit-accounting tests pass. No rates, holdout performance, physical experiment or verified complement are added.
