# Prospective numerical holdout: HMo2O7 anion

The previously documented availability fallback HMo2O7(-1) is now acquired before any successor PCM comparison. The existing H2Mo2O7 selection record states that this fallback had not been inspected. This is a candidate unused geometry for numerical validation, not a new chemical complement or an independent evidence family.

The [institutional item](https://iochem-bd.iciq.es/browse/handle/100/28778) declares CC BY4.0 and belongs to the Petrus-Bo2021 collection, dataset DOI10.19061/iochem-bd-1-201. Only metadata, XYZ and input were requested. All three returned HTTP200. The XYZ and input exactly match the independent specialist's SHA256/byte counts recorded in selection.json. No deposited output, energy, frequency or convergence result was inspected, and the downloaded input script was not executed.

Composition is ten atoms, Mo2O7H; the input explicitly sets charge -1. Spin is not explicit and remains null. The exported XYZ differs from starting input coordinates. The collection identifies an ADF geometry optimization and the input specifies PBE/TZP, large frozen core, scalar ZORA and COSMO water/Delley surface. This does not verify a converged minimum or establish equivalence to the proposed PySCF method.

The specialist found no exact selected identifier in25 campaign preparation/pin/manifest/selection records and no matching hash among11 existing campaign XYZ files. A separate root scan of188 JSON files and three XYZ files in nine named numerical campaigns also found no exact identifier or matching hash. The two audits cover different sets of files. Unknown aliases, transformed coordinates and undocumented outside use remain possible; universal unseen status is not claimed.

No numerical operator or SCF was run. A future method protocol must freeze its restricted-spin convention, input transformation, test matrices, thresholds, cases and resource bounds before looking at results. Shared publication provenance with earlier geometries must remain explicit. Numerical agreement would test an implementation, not the existence or function of Mo34WV.
