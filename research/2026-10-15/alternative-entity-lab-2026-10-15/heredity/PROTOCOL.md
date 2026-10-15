# Prospective compositional-transmission failure envelope, v1

Frozen before the first official run, 2026-10-15. Read `config.json` for all fixed
parameters and seeds. Tests use smaller synthetic configurations and different
seeds. No development screen of this grid precedes the official run. Negative
results remain in the record. Source/config/protocol hashes are recorded before
and after execution; existing output directories are refused.

## Question and relation to earlier work

Does an explicitly supplied two-type copying network preserve a functional
composition through paid synthesis, stochastic loss and daughter partition, and
where does transmission fail as copying error and finite resources change?
The earlier `serial-renewal-lineage-identifiability-v1` experiment established
conditional observability requirements, not physical synthesis. This experiment
adds a stochastic trajectory and failure envelope; it neither calibrates that
earlier model nor supplies a real chemical mechanism.

All species are dimensionless bookkeeping molecules. Both catalyst types have
the same total production kinetics; each favors copying its own type. A newly
made molecule switches type with probability mu. This template rule is supplied
by the investigator. All births cost one precursor and one fuel unit. The finite
feed and fuel budget is reset once per passage, explicitly recorded, and unused
feed/fuel is discarded. At most three production attempts per surviving catalyst
are available, with success probability 0.8, bounded by the feed/fuel budget.
No catalyst means no synthesis. Loss is independently binomial per molecule.
Molecules are partitioned between two actual daughters; one is continued and
the other is discarded. Neither copying of arrays nor a compartment reset adds
material to the continued trajectory. Initial counts are 45:5 in half of the
24 compartments, and 5:45 in the other half. There is no population selection.

Each molecule carries a true birth-origin tag: founder F or newly synthesized N.
At the end of passage six, after partition and exchange, an ideal observer
selectively removes all surviving F material. This oracle purge is an experimental
model intervention, not a claim that a physical tag permits selective removal.
Thereafter any attributed catalyst activity must arise from paid N material.
This strict purge complements natural dilution and rules out founder carryover
inside the model. It does not establish replication, reproduction of compartments,
evolution, autonomous maintenance, or intelligence.

## Four controls and matching

`faithful`: supplied parent-type copying, with error mu.
`exchanged`: identical copying rule, followed by global pooling of actual F and
N molecules separately and random redistribution among the 24 compartments.
Every recipient retains its exact F and N counts; aggregate type counts and
tags are conserved. This breaks genealogical association while retaining
material and resources. It is not an independently evolved random parent.
`neutral`: births choose types equiprobably, irrespective of parent composition.
`no_synthesis`: synthesis disabled; finite feed/fuel remains available but unused.

The three active arms use common demographic random draws for degradation,
birth totals and retained daughter totals. Thus their per-compartment F/N total
counts, birth costs, losses and daughter totals match exactly at every passage.
Conditional hypergeometric draws select type allocation; this has the same
partition distribution as independent molecule-wise fair partition, while making
count matching exact. No-synthesis has the same starting counts and resource
access; post-intervention counts cannot be matched because depletion is the
treatment. Type draws and assay noise use independent seeded streams. Pairing
supports comparisons inside a seed; compartments and passages are not treated
as independent experimental replicates.

## Independently attributed functional events

After each passage, each compartment receives 64 X reporter substrate units,
64 Y units, and 128 reporter fuel units. A favors X and B favors Y. Direct and
cross activity coefficients are 1 and 0.1. Each substrate unit has conversion
probability 1-exp(-0.6 * weighted catalyst count / 64). Converted-event counts
are binomial and assigned to F/N catalyst origin proportional to their hazard.
Each event consumes one reporter substrate and fuel unit. Catalysts are not
consumed. These explicit finite assay supplies are additional to synthesis
supplies. No uncounted assay molecule enters the reproducing inventory.
Functional preference is (X events - Y events)/(X events + Y events), with zero
when no events occur. This is a model event count, not a measured biochemical
rate. The investigator selected catalytic specificity; this test only measures
whether that supplied specificity is transmitted.

## Frozen analyses and decision

For each of nine mu/budget conditions and each of the 12 fresh seeds, retain
every compartment/passage record. Across the last four passages, compute:
(1) Pearson correlation of each compartment's previous assay preference with
its next assay preference (the exchange arm follows recipient identity);
(2) functional contrast: mean preference in A-rich founder group minus that in
B-rich founder group, divided by two; (3) median newly attributed event count.
Correlation is zero when either series has zero variance. The no-synthesis
control must have zero catalyst and zero activity at and after the purge.

A seed passes only if faithful correlation >0.3, faithful functional contrast
>0.2, faithful contrast exceeds BOTH exchange and neutral contrasts by >0.15,
and faithful median new-material events >=8. A condition passes the strict
every-replicate criterion only if all 12 seeds pass. Report seed count, exact
pass fraction and Wilson 95% interval as descriptive finite-seed uncertainty;
the interval does not turn 12 selected pseudorandom seeds into physical
replicates. Also report per-seed differences and their range. This grid is a
failure envelope, not an optimization: no tuning to failures is allowed in v1.

The strongest possible conclusion is conditional functional compositional
transmission in this supplied network. Physical feasibility, chemistry-derived
copying, evolvability and life/intelligence remain unassessed. Runtime target is
under two minutes on the available local Python runtime.
