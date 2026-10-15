# Moussawi Mo36 occupancy follow-up

Date: 2026-10-15. Outcome: **no exact W-substituted Mo36 formula, site occupancy table, uncertainty, or CIF was recovered in this bounded follow-up.** The prior direct author-summary claim remains relevant, but its missing structural detail remains missing. No candidate, geometry, chemistry simulation, or novelty claim was added.

Four evidence branches were checked: the national thesis catalogue, author/publication metadata, publisher abstracts for adjacent papers, and a collaborator's thesis citation. The earlier blocked Moussawi full-PDF routes were not repeatedly retried.

## New catalogue evidence

The public [theses.fr record](https://theses.fr/2017SACLV078) was acquired as HTML. Its embedded `__NUXT_DATA__` metadata identifies **Mhamad Aly Moussawi**, the thesis *Assemblages à base de polyoxométallates : des interactions fondamentales aux matériaux hybrides supramoléculaires*, defense date **25 October 2017**, Université Paris-Saclay (ComUE), supervisors Sébastien Floquet and Mohamed Haouas, NNT **2017SACLV078**, and DOI **10.70675/0c7d0a8azeb8bz4b8fzb5c0zc6a013ac8438**. It contains the same abstract-level W/Mo36 claim as the existing institutional summary. It supplies no alternate full-text URL or crystallographic data in the inspected record. The catalogue's accessibility flag does not demonstrate successful access to the thesis PDF.

The legacy `.json` catalogue route returned HTTP 404. The acquired HTML is a catalogue record, not the thesis. Exact SHA256 values and response outcomes are in `acquisition.json`.

The previously recovered full-text locator remains [HAL tel-01719282v1](https://theses.hal.science/tel-01719282v1), filename `74668_MOUSSAWI_2017_archivage.pdf`. The prior audit retains the anti-bot HTML responses. The [UVSQ summary](https://www.uvsq.fr/%C2%AB-assemblages-a-base-de-polyoxometallates-des-interactions-fondamentales-aux-materiaux-hybrides-supramoleculaires-%C2%BB-par-mhamad-aly-moussawi), English abstract first paragraph / summary PDF page 2, directly names ordinary Krebs `[Mo36O112(H2O)16]8−` and preferential central seven-coordinate W occupation. That statement does not specify a substituted formula or occupancy uncertainty.

## Adjacent papers checked against the target topology

The broader public HAL author query and publisher-deposited Crossref metadata produced identifiable nearby publications. Four primary ACS abstracts were inspected through indexed publisher text after direct publisher opens returned HTTP 403. Their reported systems are distinct:

| DOI / primary publisher record | Reported system | Consequence for Mo36 identity |
|---|---|---|
| [10.1021/jacs.7b08058](https://pubs.acs.org/doi/10.1021/jacs.7b08058) | `[P2W18O62]@2γ-CD@{Mo154}` | W belongs to an encapsulated Dawson anion; this is no Mo36 substitution table. |
| [10.1021/jacs.7b07317](https://pubs.acs.org/doi/10.1021/jacs.7b07317) | Dawson `[P2W18O62]6−`, Ta6 cluster, γ-cyclodextrin assemblies | Different building blocks; its advertised CIFs cannot be treated as Mo36 data. |
| [10.1021/jacs.8b07525](https://pubs.acs.org/doi/10.1021/jacs.8b07525) | Lindqvist `M6O19` with M=Mo or W, stabilized by γ-cyclodextrin | Different nuclearity/topology. |
| [10.1021/acs.inorgchem.7b01644](https://pubs.acs.org/doi/10.1021/acs.inorgchem.7b01644) | Large selenotungstate architectures assembled with Mo2O2S2 fragments | Different heteroatom, sulfur inventory and topology. |

These exclusions follow each abstract's main characterized system. They do not assert an exhaustive search of inaccessible full papers or every supplementary reference. No underlying journal article specifically documenting the summary's W-substituted Mo36 was identified.

## Collaborator-thesis lead

The indexed [URV primary deposit](https://repositori.urv.cat/repositori/getDocument/TDX%3A2031?ds=Memoria&mime=application%2Fpdf) identifies María Dolores Melgar Freire, *Keplerates: From Electronic Structure to Dynamic Properties*, legal-deposit identifier **T 258-2016**. Printed page **97**, Table **3.8** and the following paragraph, attributes preliminary W12Mo120 sulfide-Keplerate crystal results to Moussawi and cites reference **201**. It supports a lead to related work, with a different cluster. It provides no inspected Mo36 occupancy evidence.

The direct URV PDF fetch timed out; the [Tesisenred mirror](https://www.tesisenred.net/bitstream/handle/10803/349212/Tesi%20Maria.pdf?isAllowed=y&sequence=1) returned 502 through the web tool. Reference 201 and a whole-thesis Mo36/Krebs search therefore remain unverified. The deposit year is not a verified defense date. No PDF was acquired in this follow-up.

## Exact evidence still required

To advance W–Mo36 identity, an accessible copy of the Moussawi thesis's relevant chapter and supporting crystallography, or the corresponding primary publication/deposit, must provide:

1. The isolated substituted anion and salt formula, actual W loading and independent elemental analysis where available.
2. Atom-labelled coordinates, Mo/W occupancies and their uncertainties, refinement constraints, and the relationship between fractional occupancy and molecular composition.
3. A topology mapping connecting the substituted crystal's pentagonal center to the ordinary Mo36 parent. The existing Mo8 label cannot be transferred across structures without this mapping.
4. Counterion and protonation assignments, coordinated/lattice water inventory, and any disorder or unlocated H atoms.
5. Species-resolved solution evidence and its conditions, sufficient to distinguish the solid-state identity from persistence in solution.

An exact V-containing structure or species-resolved assignment is a separate requirement. A W-only result cannot establish nominal `[MoVI34WVI VV O112(H2O)16]9−`, its simultaneous site occupancies, or its stability. Bibliographic absence and technical access failure establish neither novelty nor impossibility.

`evidence.json` records the finite search, source tiers, exclusions, missing fields and tool failures. Three acquired raw responses are hash-verified in `checks.json`; these comprise one catalogue HTML and two metadata JSON files. The existing source ledgers and numerical handoff were left unchanged. No author or institution was contacted.
