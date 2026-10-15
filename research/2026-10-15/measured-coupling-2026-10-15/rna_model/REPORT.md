# R3C/POPC coupling test: measured inputs, unsuccessful predictive model

The supplied measurements support RNA catalysis, partial content retention and horizontal propagation in the same POPC vesicle preparation. Our coupled model **does not adequately reproduce their joint quantitative behavior**. Its chemistry fit already has substantial error, and the held-out transfer predictions fail the frozen numerical screen. This is evidence against the adequacy of this effective model, not against the reported experimental observations. Functional parent-offspring compartment inheritance remains unidentifiable from these assays.

The primary source is [Salibi et al., Nature Communications14,1222(2023)](https://doi.org/10.1038/s41467-023-36940-z). Its public Source Data workbook was acquired and hashed;148 numerical records were extracted with exact cell coordinates. Of these,40 are S13c summary means,36 are Figure2 individual replicate observations, and72 are Figure3 replicate observations including generation0. The held-out evaluation contains72 nonzero-condition replicate observations:9 from Figure2 and63 from Figure3. Published outcomes were inspected before analysis design, so this is a disclosed analysis-design holdout rather than blinded validation. No fitted parameter was selected using held-out error.

## Conditions and what is actually measured

All modeled vesicle operations use POPC,50mM EPPS pH8.5,20mM MgCl2,900mM sucrose internally,900mM glucose externally, three5min/−80C plus5min/room-temperature FT cycles, and60min at42C. Every later serial generation replaces half the vesicle preparation with fresh substrate-containing vesicles. S13c kinetic data use the same buffer and42C without membranes. Applying those kinetics inside GUVs is an extrapolation across membrane, local concentration and crowding effects; it is not a fully matched measurement of intracellular elementary reaction constants.

The species are52nt Hyper-A,52nt inactive Cy5-A,14nt triphosphorylated B,66nt active F1, and66nt inactive Cy5-F1 reporter. The model consumes one A and one B for each F1 and one Cy5-A and one B for each reporter. Only active F1 catalyses subsequent ligation. The observation is the fraction of all retained fluorescent A-derived strands in full-length reporter product, including carryover. It is not active catalyst concentration. Fresh fragments, initial catalysts, prepared membranes, thermal cycling and sample handling are supplied inputs. RNA nucleotide-equivalent conservation is checked, but this model does not claim a complete thermodynamic or pyrophosphate balance.

The45% content-loss estimate over three FT cycles comes from the paper's source-gel interpretation. A common55% concentration retention for every RNA species, equal internal volume fractions for GUV populations, partial linear exchange between cohorts, and zero chemistry during FT are model assumptions. SI18 reports a different bulk FT protocol and is not used as a quantitative correction. A uniform population model and mechanisms for spontaneous division were not silently substituted for these assumptions.

## Calibration and prediction results

| Evaluation | Error, RMSE in percentage points | Interpretation |
|---|---:|---|
| S13c kinetics,40 summary means |7.866|Effective chemistry is insufficient already in calibration|
| Figure2 zero/1uM seed,18 replicates |1.072|Fitted exchange can partly match low-seed endpoints|
| Figure2 held-out2uM seed,9 replicates |4.946|Seed-dose generalization fails|
| All Figure3 transfer predictions,63 replicates |3.020|Transfer prediction fails|
| Combined held-out evaluation,72 replicates |3.322|Fails frozen analysis-protocol RMSE≤2pp and worst mean error≤4pp screen|

The largest absolute held-out condition-mean error is6.890pp. For the2uM-seed series at generation7, the model predicts5.074% reporter compared with11.961% mean measured reporter. For no seed it predicts0.015% at generation7 while the observed mean is2.133%. It underpredicts spontaneous/background product generation and loses much of the experimental separation between initial seed concentrations. A matching low-seed endpoint is therefore not sufficient evidence of the full mechanism.

| Parameter | Primary value | Status and units |
|---|---:|---|
|`k`|0.0144053|Fitted effective catalytic coefficient, uM^-2 min^-1; conditional on the chosen rate law and reporter ratio|
|`kb`|2.90684e-8|Fitted effective2A2B background coefficient, uM^-3 min^-1; active product is not directly observed|
|`ki`|1000|uM; reaches upper bound, so a finite inhibition scale is not identified|
|`mixing`|0.0673964|Fitted exchange fraction per FT under the cohort model; not a direct transport measurement|
|`retention`|0.55|Fixed approximate content retention per three FT cycles, inferred from paper|
|`rho`|1|Assumed reporter/active catalytic-efficiency ratio|

The inhibition profile is nearly flat at high Ki: calibration RMSE changes from7.871pp at Ki100uM to7.866pp at1000uM. The data therefore do not identify that parameter within this model. The best fit approaches the simpler uninhibited-rate limit. All nine prespecified retention/rho scenarios fail the held-out screen; combined held-out RMSE spans3.322–7.572pp. These scenarios are structural sensitivity ranges, not confidence intervals. Selecting the lowest-error scenario after evaluating the holdout would not provide new validation, and none was selected as a replacement.

## Causal controls, substrate accounting and inheritance

With the same fitted parameters, routing new Hyper-A ligation product into an inactive species while retaining original catalyst activity increases serial RMSE to6.496pp. No exchange gives7.650pp. A fully homogeneous pool gives64.905pp, exposing why matching bulk buffer does not justify treating the preparation as instantly homogeneous. These are model ablations, not newly performed chemical experiments.

A pure carryover baseline, initialized from the observed generation1 reporter, predicts only0.00423% reporter at generation7 for the2uM-seed treatment. The much larger observed signal requires new reporter formation under the assumed loss/feed accounting. It does **not alone** prove that the new reporter is active or that daughter compartments inherit function. In the coupled simulation, original seed F1 surviving into generation7 is at most0.0001586uM, whereas modeled total active F1 is0.09639uM; that excess is model-generated catalyst, not directly measured active F1. Every trajectory records the analytical founder bound separately from newly generated model F1.

Lineage inheritance has an analytical identifiability problem: the population PAGE observer and model equations contain no parent labels. Assigning coherent or scrambled parent labels to the same chemical cohort states leaves every observed quantity unchanged. `inheritance_witness.json` describes this mathematical degeneracy; it is explicitly not a simulated lineage experiment or measured inheritance result. The paper describes horizontal transfer and states that its prepared-fragment ligase does not evolve or provide compartment fitness under the tested conditions.

## Verification and next discriminating measurements

Seven tests passed: source-cell equality, stoichiometric conservation, reporter inactivity, separated/no-exchange behavior, inherited-catalyst depletion, exchange inventory, and serial mass balance with solver refinement. Maximum moiety imbalance across the primary trajectories is5.40e-15uM; tightening integration tolerances changes reporter predictions by at most1.77e-7pp. A separate process replayed108 predictions at frozen parameters with exactly zero difference and verified source/output hashes. This replay scope does not independently refit parameters; the unified suite performs that stronger comparison separately when run.

The original system Python's SciPy installation could not import because a Mach-O PROPACK binary had an invalid zero-fill offset. Computation used an isolated uv environment with Python3.12.3,NumPy2.4.1,SciPy1.16.1,openpyxl3.1.3 andMatplotlib3.10.8; the global environment was not repaired or changed. The full calibration, sensitivity, profile and prediction run took34.7s on this host.

The next useful evidence is a matched GUV assay measuring active F1 separately from inactive reporter, per-species retained amounts and encapsulated volume before/after each FT, plus tracked compartment identity across actual division. Multiple parent compositions should be challenged in the same environment, with initial-catalyst carryover, inactive-catalyst and allowed/blocked-horizontal-exchange controls. Those measurements distinguish regeneration, passive persistence and functional lineage inheritance. Fitting more flexible kinetics to the existing held-out curves would not resolve the missing identity measurements.

No wet experiment was performed. The present result is a reproducible, falsifiable model failure and an identified inheritance-data gap; it does not establish an integrated living or intelligent entity.
