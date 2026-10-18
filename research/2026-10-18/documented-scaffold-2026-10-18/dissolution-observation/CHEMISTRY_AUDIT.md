# Native equations and stoichiometry

This audit is separate from the frozen sampling simulation. No chemical rate or response curve was fitted. It checks the native SI equation structure before using the source's thermodynamic statements.

The plain-text extraction initially made Eq. S5's coefficient look like `0.0593`. Native DOCX OMML instead stores a fraction with numerator `0.059` and denominator `3`; see `sources/si-equation-10.xml` and the source audit. The apparent coefficient error was an extraction artifact, not a source Nernst error.

For the source's balanced reduction half-reaction,

`FeO4^2- + 3H2O + 3e- <=> FeOOH + 5OH-`,

both sides contain Fe1 O7 H6 and charge -5. Three transferred electrons require the logarithmic concentration coefficient to contain the factor 1/3. The native rounded expression

`E_RHE = 2.236 + (0.059/3) log10(a_FeO4) - 0.039 pH`

gives 1.552 V at pH13 and 1.513 V at pH14 when `a_FeO4 = 1e-9`. These agree with the main article's rounded 1.55/1.51 V statements. This is an internal consistency check under the source's activity/standard-state approximation, not an independent ferrate measurement, kinetic validation or temperature-corrected equilibrium calculation for the 20 C experiment.

A different displayed line, Reaction30 (`sources/si-equation-12.xml`), actually contains `FeO4^2- + 8H+ + 3e- <=> Fe3+ + 5OH-`. As printed, left/right Fe/O/H/charge totals are `(1,4,8,+3)` and `(1,5,5,-2)`, respectively. The conventional balanced acid half-reaction would end in `Fe3+ + 4H2O`. Preserve the native typo; it does not invalidate the correctly balanced Eq. S5 or establish that the published Pourbaix result was calculated from the typo.

Executed with the qualified Python3.12.3 binary, exit0, without writing source files:

```python
s5_left = {"Fe": 1, "O": 7, "H": 6, "charge": -5}
s5_right = {"Fe": 1, "O": 7, "H": 6, "charge": -5}
printed30_left = {"Fe": 1, "O": 4, "H": 8, "charge": 3}
printed30_right = {"Fe": 1, "O": 5, "H": 5, "charge": -2}
corrected30_right = {"Fe": 1, "O": 4, "H": 8, "charge": 3}
assert s5_left == s5_right
assert printed30_left != printed30_right
assert printed30_left == corrected30_right
potentials = {pH: 2.236 + (0.059 / 3) * (-9) - 0.039 * pH
              for pH in (13, 14)}
assert all(abs(potentials[p] - e) < 0.005
           for p, e in [(13, 1.55), (14, 1.51)])
```

Independent review separately inspected the native fractions and atom/charge balance. Neither a flattened equation token nor a corrected transcription is admitted as a new measured chemical property.
