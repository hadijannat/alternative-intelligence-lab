# Candidate-role22: cobalt-phosphate isotope source audit

**Disposition: component-supported cobalt recycling / phosphate exchange; insufficient evidence for isotope-resolved newly competent activity.** This is candidate-role22 and supplies no verified complement to nominal Mo34WV. The proposed material is an electrodeposited cobalt-oxygen-phosphate film with orthophosphate electrolyte; its variable composition does not justify assigning a fixed molecular formula or equating it with bulk Co3(PO4)2. The source family is Lutterman, Surendranath and Nocera, JACS 2009, DOI [10.1021/ja900023k](https://doi.org/10.1021/ja900023k). It is distinct from the Fe-feed-21 NiCoFe/borate source. No target experiment or SCF was performed.

## Acquired source and access limit

The complete original 12-page SI was acquired from [ACS Figshare](https://acs.figshare.com/articles/journal_contribution/A_Self_Healing_Oxygen_Evolving_Catalyst/2869057), DOI10.1021/ja900023k.s001. Its title/authors and metadata resource DOI match the requested paper. It contains methods, two tables and four supplementary figures; the repository lists one PDF, no spreadsheet/time-series dataset. Public metadata declares CC BY-NC4.0. Original PDF bytes and metadata are retained in raw/. Extracted text is si-text.txt.

The NSF lead https://par.nsf.gov/servlets/purl/10040540 was returned by search with the requested DOI and isotope text, so it is an indexed matching lead. Direct retrieval repeatedly timed out, and the ACS main-PDF endpoint returned403. Main-article bytes were not acquired or independently identity-checked. No precise main-figure readings are claimed. Search snippets are discovery evidence only; substantive numeric conclusions below come from the downloaded original SI. This limits assessment of the complete article.

## Exact assay conditions (SI page locators)

General (S2): ambient temperature, no numeric temperature; 0.1M potassium phosphate pH7 unless specified. Ag/AgCl potentials converted to NHE by adding0.197V. Platinum-mesh auxiliary unless specified. ITO working electrodes, glass-frit H-cells. Applied electrolysis generally without iR compensation. These conditions do not establish compatibility with the acidic Mo36-derived target hypothesis.

Co-Pi cobalt tracer (S6): film grown from20mL 0.5mM Co(NO3)2 in phosphate enriched with10mCi57Co(NO3)2, at1.30V vs NHE for3.3h,12.5C/cm2. Two electrodes prepared together, typically3.75cm2 immersed each; three5-min washes in fresh80mL phosphate baths. Separate stirred H-cells compare applied1.30V switched on/off and open circuit. Both chamber aliquots were counted; terminal HCl dissolution supplied the denominator. A separate10µCi run used4h deposition,10.0C/cm2. These are distinct preparations, not matched radiation doses.

Phosphate leaching (S4-S5):20mL0.5mM cobalt nitrate in0.1M phosphate plus0.15mL~1.5mCi32P-orthophosphoric acid; deposition1.30V,15min,0.5C/cm2. Three washes, then25mL phosphate in each chamber;1.30V versus open circuit. A1M phosphate operation control used a different4h/10.7C/cm2 deposition and~10mCi label. SI explicitly warns that deposition differences change absolute leaching: around40h, open-circuit values approximately70% versus50%. These are not a controlled phosphate-concentration effect size.

Phosphate uptake (S5-S6): eight initially unlabelled films deposited2h,3.9C/cm2 at1.30V; divided into two four-electrode arrays. Each cell receives~1.5mCi32P in phosphate; one operated1.30V and one open circuit. Removed films were triple washed, acid dissolved, aliquoted and counted. This labels phosphate incorporation into pre-existing films, not newly born cobalt catalyst.

Co-X rescue (S7-S8): film prepared without phosphate in20mL0.1M K2SO4 pH7 containing25mM cobalt nitrate and~2mCi57Co,1.65V, nickel-foil auxiliary. Deposition3.8/4.5h and16.4/29.2C/cm2. Operation in sulfate at1.30/1.51V versus open circuit; phosphate added after30/18h respectively to final0.1M. One open-circuit control removes the electrode before phosphate addition. No decline over5h in that control supports electrode-associated redeposition over bulk precipitation under that control's conditions.

## What the numbers actually measure

S2-S3 calibrate scintillation counting efficiencies:32P1.0,57Co0.68. DPM=CPM/efficiency and0.001nCi=2.2DPM. Solution radioactivity accounts for changing volume, earlier aliquot withdrawals and initial background; terminal acid dissolution normalizes the available total. All aliquots counted together at the experiment end. **Table S1 reports cumulative radioactivity physically removed in aliquots, not percent catalyst leached.** For example0.02/0.04% for Figure1 must not be converted to98–100% catalyst retention or kinetic rates.

S4 reports independent Co-Pi open-circuit30h runs with1.6% and1.3%57Co leached. Arithmetic complements are98.4% and98.7% original label not accounted as leached. They do not establish intact founder structure, isotope-resolved catalytic competence, or a bound on activity of altered founders. Co-X open-circuit6h runs report0.18% and0.16% leaching. Source counting uncertainty is two standard deviations below5%; estimated error across experimental runs is~20%. Neither is a supplied confidence interval on a kinetic parameter; no confidence interval is fabricated.

S7-S8 give approximately0.25% dissolved cobalt label before phosphate and~0.05% after5h with the electrode at open circuit. The derived change is~0.20 percentage points of initial label, or~80% of that small solution pool. These are approximate source prose values, not exact raw observations. No first-order rate is justified by two approximate endpoints; the pool can undergo simultaneous release and uptake. The SI's final reference to FigureS3a appears inconsistent with its FigureS4a rescue discussion and is preserved as a source cross-reference ambiguity.

## Founder bound and functional attribution

The57Co experiment labels founders before operation and follows release/redeposition of their atoms. It does not pulse-label an external new cobalt feed and separate new competent material from old material. Recycled founder atoms may enter new arrangements; isotopic origin alone cannot identify retained organization.32P exchange labels a ligand/electrolyte constituent and cannot quantify replacement of cobalt catalytic centers.

For an additive activity assay, a future conservative bound would be A_new >= max(0,A_total_lower - N_founder_upper*k_founder_max - A_background_upper). None of the required paired functional quantities or a validated founder-specific activity ceiling is supplied in the acquired SI. Nonadditive cooperation would require a different attribution model. Therefore no positive lower bound on newly competent activity can be calculated; the trivial nonnegative bound is0, not evidence of zero actual renewal. Retention/redeposition provides a mechanistic comparator but does not close protocolR orH.

The next discriminating experiment needs independent feed and founder isotope accounting with mass balance, simultaneous calibrated catalytic function, and a founder-only maximum-function control; physical separation or a validated selective intervention must establish competence of new material. Target admission additionally requires target identity and shared operating conditions. No kinetic constants, dose equivalence, target compatibility, inherited state or physical result are inferred here.

Run `python recursive-compound-2026-10-15/renewal/copI-source/analysis.py`. Captured validation and acquisition record: `.omo/evidence/copi-source/`.
