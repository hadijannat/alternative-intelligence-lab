# Fixed-density Coulomb-energy sensitivity

Five of six original J comparisons remain nonpassing at absolute 1e-10, rtol=0. Energy sensitivity does not relax that result or establish SCF/chemical accuracy.

| Original comparison | Oriented delta | Original pass | delta E_C (Hartree) | Frobenius norm |
|---|---|---|---|---|
| J2-J1 | J2-J1 | False | -4.0090968424324917e-11 | 4.7632528073848292e-09 |
| J3+J1 | (-J3)-J1 | False | 3.6796504298973436e-11 | 4.4628367741939295e-09 |
| J3+J2 | (-J3)-J2 | False | 7.6887472723298353e-11 | 2.2840689340323172e-09 |
| J1-Jold | J1-Jold | False | -1.7423967359701162e-11 | 4.8330609380415977e-09 |
| J2-Jold | J2-Jold | True | -5.7514935784026085e-11 | 1.3577927182894635e-09 |
| J3+Jold | (-J3)-Jold | False | 1.9372536939272274e-11 | 1.9576723440132433e-09 |

Bounds and full original comparison records are in result.json. J3 is oriented back to positive density. AO/element localization is omitted because a full exact mapping was not saved. No new operators, SCFs or fits were run.
