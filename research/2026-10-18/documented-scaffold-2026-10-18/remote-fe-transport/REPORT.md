# A boundary must preserve competent states, not just retain metal

The new primary intervention supplies stronger evidence than current-only regeneration curves: an electrode exposed behind an anion-exchange membrane remains substantially less active when remeasured in refreshed single-cell conditions. A transport model that changes only the counter-electrode sink cannot explain this ordering under common active-state/readout assumptions. Adding a simple aggregation interaction permits a transient reversal, but fails the five-hour contrast throughout the frozen synthetic grid. No chemical rate or verified repair function is identified.

## Source and controls

[Zhao et al., *Remote Iron dynamics of NiFe (oxy)hydroxides toward robust active sites in water oxidation*](https://doi.org/10.1038/s41467-025-60728-y), Nature Communications16,5601 (2025). [Acquisition](<ACQUISITION.md>) verifies the native article, SI, peer-review file,19-sheet numerical workbook and supplementary17CIF structures. [The source audit](<SOURCE_AUDIT.md>) maps actual headers and preserves numbering/preparation inconsistencies. These are newly analyzed source data, not another experiment.

The low-loading comparison uses NiFe-LDH-derived material in single-cell(SC), AEM H-cell and CEM/PEM H-cell configurations in1M KOH. Membrane, geometry and solution-volume differences remain; the exact CA interfacial-potential correction is not fully specified. The paper does address immediate membrane/electrolyte/bubble effects: the **same working electrode** is tested in refreshed SC conditions before and after its assigned exposure. This positive control is retained, not dismissed.

Counter-electrode metal measurements use another substrate/loading. They cannot be joined to these low-loading current traces as a measured Fe balance or calibrated sink rate. Surface/bulk Fe/Ni ratios are depth-dependent relative measurements, not absolute active-Fe inventories. Our numerical extraction tests function and condition ordering; it does not independently re-estimate the source's Fe enrichment or phase fractions. Oxygen18 labeling in a separate assay is not an incoming-Fe label. DFT structures/energies do not provide macroscopic exchange constants.

## Frozen experimental screen

[Protocol](<PROTOCOL.md>), [metadata amendment](<AMENDMENTS.md>) and [extraction notes](<EXTRACTION.md>) separate reserved numerical observations from already known qualitative claims. This is retrospective and source-informed. No clean blind or independent-specimen validation is claimed.

At1.53V, including both CV branch crossings, the refreshed-SC after/before current ratios are:

| Exposure | Nominal ratio | All-crossing ratio envelope |
|---|---:|---:|
|SC|0.8496|0.8182–0.8820|
|CEM H-cell|1.2663|1.2625–1.2702|
|AEM H-cell|0.4007|0.3820–0.4202|

The fixed1.55V sensitivity gives the same ordering. These envelopes reflect branch choices, not confidence intervals or replicate uncertainty. The persistent difference under matched measurement conditions supports an exposure-induced material-state change. It does not identify its unique chemical cause or prove that altered function belongs to newly formed material. CEM's post-assay gain also shows that a fully competent initial state is not a measured fact.

The native CA observed-window retention medians are0.8456(SC),0.1625(AEM),0.7322(CEM). However, AEM/CEM end at299.83333/299.91667min. The conservative strict300min screen is **null**, with no endpoint filling or window shift. The observed-window descriptions remain separate. SC's appended out-of-order300min row is preserved. CA decay and post-CV change are different readouts; their percentages are not one calibrated active-site trajectory.

## Coupled chemistry test and negative result

The simple finite-pool model exchanges active Fe(A) and dissolved Fe(D), with inactive(X) and counter-associated(C) sinks. With nonnegative common rates and identical initial pools, reducing only the counter sink cannot lower A. Its cooperative dynamics preserve the ordering. Using that invariant to interpret current additionally requires common catalytic competence and the assumed membrane transport ordering; the source does not independently measure low-loading permeability. The experiment challenges this **combined mechanism/readout/boundary hypothesis**, not every exchange mechanism.

The proposed improvement adds coarse-grained `A+D -> 2X`: retained dissolved material can consume a competent state into an inactive aggregate. A and D count normalized Fe units; D is not an experimentally identified free-Fe3+ species, and X is not a measured FeOOH quantity. No rate is fitted to the experimental curves.

Ten frozen synthetic cases use the specified common rates, ka=0,0.1,1,10,100 and counter-sink rates0/2 per hour. All conserve finite Fe to1.27e-14. For ka10 and100, lower sink produces transiently lower A around0.835/1.015h, with differences−0.02513/−0.006819. Those reversals survive the step-halving comparison. At **five hours every pair has the opposite ordering**, so the proposed interaction does not reproduce the late contrast in this grid. This rejects that parameterized test, not the entire aggregation mechanism or all possible rates. No early time was selected as a replacement success criterion.

The step-halving diagnostic also fails its implementation tolerance1e-5 for the two ka100 cases, reaching1.15e-5. The other eight are below9e-7. The protocol required the comparison but supplied no tolerance; the implementation's failure flag is retained. Eleven other checks pass. Process exit0 means artifacts were saved, not that every numerical or scientific check passed. No result was retuned or replaced to obtain a pass.

![Native observations and frozen tests](<results/observations.png>)

[Results](<results/analysis.json>) retain native-cell provenance, all crossings/windows, null screens, synthetic trajectories, failures and frozen hashes. The improvement still lacks a measured inactive-state population, persistent blocking kinetics and independently constrained boundary flux. Adding more free loss terms to the consumed curves would not identify those quantities.

## Zn-derived precursor decision

The candidate is nominal `[Ni0.75Fe0.25]0.6Zn0.4Clx`, electrochemically converted to Zn-depleted Ni(Fe) oxyhydroxide. It is a precursor label, not an exact final molecular identity. The source proposes vacancies that accommodate Fe.

All three retention series have cycles20,30,50,70,80,100,150,200. Only two points fall in the fixed training interval<=40, below the required three. **All forecasts are insufficient-data; no model is fitted and no split is moved.** At cycle200 the reported retention is35.69% for LDH,103.03% for NiFeCl and101.23% for NiFeZnCl. These descriptive observations support chloride-derived retention under the source conditions but do not show an incremental Zn-specific advantage at that endpoint. They are not statistical equivalence, general catalyst superiority, repaired new-material function or held-out model validation.

Carbon black/Nafion, glassy carbon and the external electrochemical apparatus remain dependencies. No carbon-free maintained organization or same-medium coupling to Mo34WV/PMo12 is demonstrated. Preserve the nominal3:1 versus methods4:1 Ni/Fe inconsistency rather than choosing a composition to fit.

## Recursive disposition

Retain state-dependent competence and inactive-material removal as necessary design questions. Reject a boundary proposal justified solely by total-metal retention. The tested aggregation model remains an unvalidated partial explanation; chloride-derived NiFe is a source-condition comparator, and the Zn modifier earns no verified incremental retention role here. Zero integrated complements are added; all12full-system requirements remain unclosed.

The parallel [contact-state assessment](<../contact-chirality/REPORT.md>) provides a different H-route proposal but no isolated, serially inherited recipient function. The exact Mo34WV identity, coupled renewal, functional heredity and intelligence remain unverified.

A concrete next primary lead is spatial edge/plane Fe function, DOI10.1021/jacs.5c00438, previously abstract-screened only. Its native SI/data must first be acquired and matched to independent site-state/function measurements before adding a persistent-state term or testing another candidate. No property from that unacquired dataset is used here. This step is progress through new intervention evidence, executed tests and preserved negative decisions; the full original goal remains active and unachieved.
