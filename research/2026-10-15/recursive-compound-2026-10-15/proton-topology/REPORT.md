# Proton and heavy-contact topology audit

The two supplied structures differ in both H placement and heavy-atom contact graphs over all three frozen cutoffs. They cannot be described as an aqua-to-hydroxo redistribution on identical heavy coordinates or identical 2.5–2.7 Å Mo–O graphs. This does not establish different physical framework identities: cutoff contacts are not bonds, the geometries have different provenance, and no unique cross-source site mapping was inferred.

P0_A's 164 heavy coordinates match the existing crystal-derived site mapping exactly (maximum coordinate distance 0 Å). The old extraction source selects and unwraps a periodic connected component at 2.6 Å; its report treats O57–O64 as provisional water sites. The H builder assigns two H to each of their two symmetry copies. Published geometry is the initialization-coordinate record already audited, without a separately declared final geometry. No input or previous result was changed.

## Frozen contact results

Nearest-O assignment uses <=1.2 Å and rejects distance ties within1e-10 Å. All32 H were assigned uniquely in both structures. Every H assignment and every O's local Mo contact list is in `result.json`.

| Mo–O cutoff, Å | Published edges | P0_A edges | Published Mo-degree histogram | P0_A Mo-degree histogram |
|---|---:|---:|---|---|
| 2.5 | 212 | 220 | 5:8, 6:24, 7:4 | 6:32, 7:4 |
| 2.6 | 212 | 220 | 5:8, 6:24, 7:4 | 6:32, 7:4 |
| 2.7 | 216 | 220 | 5:4, 6:28, 7:4 | 6:32, 7:4 |

Both heavy graphs have one36Mo/128O connected component at each cutoff. Simultaneous element-colored refinement distinguishes their degree/color histograms at its first round in each case; equal edge counts are not required to reach that conclusion. No search beyond the frozen12-round maximum was allowed and no factorial mapping search was performed.

At2.5/2.6 Å, published O-degree counts are72 degree1,32 degree2,20 degree3 and4 degree4. P0_A has64 degree1,40 degree2,20 degree3 and4 degree4. At2.7 Å the published counts become68 degree1 and36 degree2, with higher degrees unchanged. Four extra published contacts are each2.68388744 Å (a31–a20, a70–a99, a126–a167, a143–a181, in the source O–Mo ID order). P0_A has no changes across these cutoffs. This sensitivity limits any chemical interpretation of which contacts are absent.

## H-bearing oxygen environments

At every cutoff the published geometry has24 one-H and4 two-H oxygen sites, all terminal-like (one Mo contact). P0_A has16 two-H oxygen sites:12 terminal-like and4 bridging-like (two Mo contacts). Its bridging-like two-H sites retain the source labels O57@0, O57@2, O64@0 and O64@2. Those labels are within-source provenance, not a mapping to published atom IDs.

At2.6 Å, published one-H O–Mo contacts span1.900370–1.998059 Å; all four two-H O–Mo contacts are2.407220 Å. P0_A two-H contacts span2.320407–2.440658 Å. H-free published contact distances span1.718383–2.499026 Å, versus1.664453–2.378815 Å in P0_A. Full local contact distances and nearest-Mo distances are preserved, including for each H-bearing O.

Calling one-H sites “hydroxo-like” and two-H sites “aqua-like” is a geometric description. Distance assignments alone establish neither chemical bonds, measured protonation nor coordination chemistry. Eight fewer contacts at the two lower cutoffs cannot be assigned to particular changed sites across sources without a defensible map.

## Formal bookkeeping, not mechanism

Under assumed Mo(VI), oxide−2, hydroxide−1 and neutral aqua:

- P0_A:36Mo +16H2O +112O gives Mo36O128H32 and charge216−224=−8.
- Published contact interpretation:36Mo +4H2O +24OH +100O gives Mo36O128H32 and charge216−24−200=−8.

The arithmetic difference is12H2O+12O(2−)↔24OH(−). It conserves atoms and formal charge, but supplies no proton-transfer pathway, equilibrium constant or evidence that the observed geometries are connected by that process. The heavy-contact differences must remain explicit in any subsequent chemistry comparison.

## Evidence and bounded controls

The frozen protocol preceded execution. Commands from workspace root:

```sh
python3 -B recursive-compound-2026-10-15/proton-topology/test_analysis.py
python3 -B recursive-compound-2026-10-15/proton-topology/analysis.py
```

Eight synthetic tests passed, covering exact cutoffs, terminal/bridging assignment, permutation invariance with unresolved symmetric mapping, a distinct-graph negative control, a regular-graph limitation, nonfinite coordinates, tied O assignment and formal charge balance. The regular-graph negative control deliberately gives one12-cycle and two6-cycles identical local-refinement invariants; the algorithm correctly reports unresolved, demonstrating that matching invariants are not isomorphism proof. Raw outputs are retained in `evidence/tests.txt` and `evidence/analysis.stdout.txt`. `result.json` includes source/protocol hashes, full refinement records and local numerical observations; `evidence/verification.txt` captures independent checks.

No SCF, source repair, optimization, network retrieval, cross-source atom correspondence or physical validation was performed. An unambiguous chemical framework comparison remains unresolved; the demonstrated result is different supplied H arrangements and nonisomorphic declared cutoff graphs.

## Addendum: explicit authored GUIBonds, separate result

The original geometry result is retained unchanged in both `result.json` and `result-v1.json`; the original report and protocol are preserved as `REPORT-v1.md` and `PROTOCOL-v1.md`. The current protocol adds a frozen GUIBonds parsing/comparison step. Consequently the original result's protocol hash verifies against `PROTOCOL-v1.md`, not the subsequently extended current protocol. The additive output is `guibonds-result.json`.

The published input contains200 explicit GUI bond declarations:32 H–O,162 Mo–O and6 Mo–Mo. All32 declared H–O assignments exactly agree with the unique nearest-O geometry assignments. The source therefore explicitly encodes four O sites with two H and24 O sites with one H. This is stronger provenance for the authored computational model than distance inference alone, while remaining distinct from measured chemical bonding/protonation.

The declarations do not supply a complete substitute for the Mo–O distance graph. All162 declared Mo–O pairs are within2.5 Å. The geometric graphs contain50 additional undeclared Mo–O contacts at2.5/2.6 Å and54 at2.7 Å. There are no declared Mo–O edges excluded by any of the three cutoffs. Thus this metadata does not reveal stretched declared Mo–O bonds outside the geometric cutoffs or reconcile the missing contacts with P0_A. Its six Mo–Mo declarations and original bond orders are retained without chemical reinterpretation. The Mo–O-only declared subgraph also differs from P0_A's contact graph, but incomplete/different declaration conventions make this a weak basis for chemical framework classification.

The responsible conclusion remains: explicit H topology differs, the fixed-cutoff Mo–O graphs differ, and formal charge can still match. The source GUI declarations confirm the author's4aqua-like/24hydroxo-like arrangement; they cannot by themselves decide physical framework equivalence or produce an unambiguous cross-source site map.

Additional invocations:

```sh
python3 -B recursive-compound-2026-10-15/proton-topology/test_guibonds.py
python3 -B recursive-compound-2026-10-15/proton-topology/guibonds.py
```

Four additional tests passed (including seven malformed-bond subcases): valid order/ID preservation; missing endpoints, self-bonds, nonfinite/nonpositive orders, malformed fields, duplicate pairs/IDs; unterminated blocks; and duplicate atoms. Raw outputs are in `evidence/guibonds-tests.txt` and `evidence/guibonds.stdout.txt`. No earlier source or result was repaired.
