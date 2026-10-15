# Source and implementation reuse

The authoritative acquisition ledger is ../identity/next-step/wv-reference-selection/SOURCES.md. It supplies the six SHA256 values, primary download URLs, ICIQ item attribution and CC BY4.0 attribution. Raw files remain in that original location. Prepared pins include that ledger and all six files. Neither raw records nor prior results are rewritten.

WO4: https://iochem-bd.iciq.es/browse/handle/100/28683, Mo/W collection https://doi.org/10.19061/iochem-bd-1-201, Petrus and Bo2021 https://doi.org/10.1021/acs.jpca.1c03292. VO4: https://iochem-bd.iciq.es/browse/handle/100/30238, V/Nb/Ta collection https://iochem-bd.iciq.es/browse/handle/100/30179. Sources use different ADF methods; their energies are not comparison values.

Numerical oracles read: ../rij-jkfit-qualification/run.py and PROTOCOL.md (original error definitions/thresholds), ../cpcm-rij-memory-qualification/run.py (full solvent-aware Fock checks). Reuse its serialization, source-hash and receipt helpers; reuse ../parent-pilot/pilot.py supervisor. Memory implementation and all its native source pins remain unchanged. Imported helper source and native def2-SVP basis data are pinned alongside the new driver/tests/protocol. No existing numerical outcomes are taken as W/V evidence.
