# Independent transport and serial accounting check

**PASS.** A separately written, fully coupled DOP853 transport integration agrees with the production mean/deviation and matrix-exponential solution. A separately written reaction RHS and serial event map also agree with the production simulator. No measured data were fitted or used to choose verification inputs.

| Comparison | Coverage | Largest difference |
|---|---|---:|
| Transport concentrations | 48 cases; 2,688 scalar comparisons | 8.38e-13 µM |
| Three-generation serial inventories and ledgers | 24 paths; 19,440 quantities including PAGE | 1.51e-9 µM |
| Washed intracellular PAGE | Every short-serial stage | 9.62e-8 percentage points |

Transport cases cover four unequal cohort weights, all seven channels, exterior/interior volume ratios 1/3/30, empty and preloaded exterior pools, one/three FT units and patch exchange 0.001/0.1/10. Serial paths cover seeds 0/1/2 µM, both finite transport families and the four exterior reaction/carryover sensitivities. The independent chemistry uses the earlier selected baseline constants read from its retained result, rather than production RHS code.

All declared transport, conservation, feed, observer, reaction and founder-tag checks pass. Three consecutive one-unit FT steps equal a three-unit step without exterior reset. The model permits reuptake; isolated patches preserve their own total cargo; increasing patch exchange approaches the common-bath solution. The patch-to-bath maximum concentration differences at exchange rates 100/1,000/10,000 are 0.0028094/0.00028042/0.000028037 µM. Half-transfer preserves the specified dilution and substrate feed, including the carried exterior. PAGE observation leaves the continuing culture unchanged. The founder tag remains a subset of competent F and follows the specified decay law.

`results-v2/verification.json` is the final receipt; complete transport and stage comparisons, synthetic inputs and source hashes are alongside it. `results-v2/frozen/` preserves the four hashed inputs. `results-v1/` remains intact: it passed before the model worker added input validation for the zero-generation relative-tolerance edge case. Equations were unchanged, and both runs have identical scientific comparison values.

Reproduce without overwriting either result directory:

```sh
uv run --offline --no-project --python /USER_HOME/.pyenv/versions/3.12.3/bin/python3 --with numpy==2.4.1 --with scipy==1.16.1 python rna-seed-transport-2026-10-15/independent/verify.py --output NEW_DIRECTORY
```

Skipped measured fitting and physical experiments. This check establishes numerical implementation agreement and accounting consistency; it does not identify transport rates, validate the 55% tracer approximation, or establish functional inheritance.
