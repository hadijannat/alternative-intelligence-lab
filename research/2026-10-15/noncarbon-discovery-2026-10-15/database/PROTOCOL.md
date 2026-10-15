# Frozen 1000-record inorganic materials screen

Written 2026-10-15 before inspecting numerical material properties. This is a composition-stratified screen of existing computed crystal structures, not a discovery of 1000 novel compounds or a prediction of life.

## Dataset and selection

Use the official NIST JARVIS registry `dft_3d` archive file 38521619, named `jdft_3d-12-12-2022.json.zip`, expected MD5 `fb3e1eb80339a70ff313af1c644c1777`. The current Figshare article v11 also contains a newer 2025 snapshot; choosing the registry default makes the snapshot explicit, not current to 2026. Record archive SHA256, registry source, version and license. Do not switch datasets after results.

Eligibility uses only structure identity and composition: valid unique `jid`, nonempty elemental list in `atoms.elements`, no carbon, at least two distinct elements (compound), and formula present. Different polymorphs count as distinct structure candidates; report the number of distinct reduced elemental-count compositions separately. Count and retain exclusion reasons. No numerical property determines eligibility or sample selection.

Mutually exclusive chemistry strata in this precedence order and quotas:

1. P and O present: 150 (phosphorus-oxygen composition; not proof of phosphate bonding).
2. Si and O present: 150 (silicon-oxygen composition; not proof of silicate bonding).
3. S present, O absent: 200 (sulfur-containing).
4. N present, O and S absent: 100 (nitrogen-containing).
5. O present after the prior categories: 300 (other oxygen-containing).
6. Remaining carbon-free compounds: 100.

Rank candidates within each stratum by SHA256 of the UTF-8 string `noncarbon-screen-2026-10-15-v1|JID`, then JID as tie-breaker. Take each quota. If a stratum has fewer candidates, fill its deficit from all remaining eligible candidates by the same hash order. Freeze the selected IDs, selection file SHA256 and complete eligible inventory before a separate screen command reads numerical properties. No substitutions for missing or unfavorable properties.

## Descriptive screens, no life score

For all 1000 records retain formula, JID, composition and available source values: `formation_energy_peratom`, `ehull`, `optb88vdw_bandgap`, `mbj_bandgap`, `icsd`. Missing and malformed values are missing, not zero.

Report formation energy <= 0 eV/atom as `nonpositive_formation`; > 0 as `positive_formation`; unavailable as `unknown`. This measures formation relative to the dataset's elemental references and does not establish stability against competing compounds or solution chemistry.

If `ehull` is present, report <= 0.1 eV/atom as `within_screen_threshold`, > 0.1 as `above_screen_threshold`, and unavailable as `unknown`. The 0.1 eV/atom threshold is an explicit broad screening heuristic, not a universal metastability bound or life requirement. Negative hull values are retained and flagged invalid for this physical classification. Do not replace absent hull values with formation energy.

Record two composition-only flags, without claiming a measured mechanism:

- Presence of one or more of V, Cr, Mn, Fe, Co, Ni, Cu, Mo, W: redox-relevant element present. Oxidation states, reversibility and catalytic rate remain unmeasured.
- Presence of one or more of H, Li, Na, K, Rb, Cs, Ag, Cu, Mg, Ca, Zn: candidate ion-bearing composition. Ion mobility, vacancies and switching remain unmeasured.

Bandgaps are descriptive electronic properties only. No bandgap threshold, combined score, intelligence score, or candidate ranking is allowed. Mark autonomous maintenance, replication, functional inheritance, learning and intelligence `UNMEASURED` for every candidate. Database membership does not establish experimental synthesis or novelty; all rows are `existing_database_structure`.

## Verification and negative results

Use a standard-library-only deterministic script with separate `select`, `screen`, `verify` commands. Test carbon vs Ca/Co/Cl distinction, missing/nonfinite numeric values, selection invariance to input ordering, stratum precedence, quota shortage and duplicate IDs. Full replay in a new process must produce byte-identical eligible, selected and screened records. Verify 1000 unique IDs and archive MD5; retain every selected negative/unknown row. Fail loudly if fewer than 1000 eligible candidates exist. Do not train ML or perform new DFT. Do not call this held-out validation: no predictive model is trained and the screen cannot validate a living system.
