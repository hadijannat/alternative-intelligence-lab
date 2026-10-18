# Metadata-driven clarification before numerical outcomes

The executor identified `WNi78Tfinal.DTA`, an additional86400s CHRONOP record in the looping WNi78T folder. No potential/current trace values were reported when this issue was raised.

The original instruction to summarize each native loop OER block is ambiguous for an appended continuous24h record. Clarification: divide a long continuous CHRONOP extension into complete6000s intervals using the same last300s median rule. Do not compress86400s into a single point or treat it as a normal6000s loop. Preserve the residual partial interval as incomplete coverage.

Concatenation as a pulse-off extension requires chronological native header evidence and inspection for intervening acquisition types; otherwise treat it separately and leave physical specimen/protocol continuity unresolved. Never add an inferred chemical phase across unrecorded time. This amendment is triggered by file structure, before numerical response inspection, and does not alter the fit/forecast cutoff, parameter grid, tolerances or origin criterion.

The metadata check rejects direct concatenation: loop43 starts19March2022 at10:27:24 and its6000s OER ends12:07:24. Regen43 starts12:07:39 with only6s recorded. RuFinal EIS starts15:13:51, lasts19s, then the final CHRONOP starts15:14:11. The unrecorded interval exceeds3h and EIS intervenes. Keep the43loopblocks as the main specimen case. Retain14complete interval summaries from the separate24h tail, with its own anchor and incomplete remainder, as an exploratory followup without a reserved forecast. It cannot validate a pulse-withdrawal causal comparison.
