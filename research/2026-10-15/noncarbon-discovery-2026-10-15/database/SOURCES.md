# Source ledger

Accessed 2026-10-15. Dataset attribution: Kamal Choudhary, JARVIS-DFT 3D dataset, NIST, Figshare article 6815699; CC BY 4.0. This directory contains an unchanged downloaded dataset plus derived screening tables. The screen and interpretation are this investigation's work, not NIST conclusions.

| Source | Role | Verified fact / limit |
|---|---|---|
| [NIST JARVIS official portal](https://jarvis.nist.gov/) | Institutional provenance | Links curated Figshare datasets and JARVIS tools. |
| [Registry at commit 3b0c9d0f0c15759135de857dbc93e010db01eb29](https://github.com/usnistgov/jarvis/blob/3b0c9d0f0c15759135de857dbc93e010db01eb29/jarvis/db/figshare.py#L39-L45) | Exact selected download | `dft_3d` resolves to file 38521619. No `dft_3d_no_cfid` key exists in this registry. Saved as `raw/figshare-pinned.py`. |
| [Dataset metadata, article version 11](https://doi.org/10.6084/m9.figshare.6815699.v11) | License and version | Published 2026-05-09; CC BY 4.0. This is the container version; selected file remains the 2022-12-12 snapshot. Metadata API saved as `raw/figshare_metadata.json`. |
| [Exact selected archive](https://ndownloader.figshare.com/files/38521619) | Numerical data | `jdft_3d-12-12-2022.json.zip`; 40,811,489 bytes; official MD5 `fb3e1eb80339a70ff313af1c644c1777`; downloaded SHA256 `d4c64660e9e1fa45c82bd8868a96ec10162195eed69636445972c05550d8d0d6`. |
| [Official release metadata API](https://api.figshare.com/v2/articles/6815699) | Snapshot distinction | Also lists newer file 64391379, `jdft_3d-9-24-2025.json.zip`, 48,447,610 bytes. This newer file was not downloaded or screened. Registry default must not be called the latest snapshot. |
| [Official property schema](https://jarvis-materials-design.github.io/dbdocs/thedownloads/) | Property definitions | Lists formation energy, `ehull`, electronic bandgaps. Availability is verified per selected row. |
| [Formation-energy implementation](https://github.com/usnistgov/jarvis/blob/3b0c9d0f0c15759135de857dbc93e010db01eb29/jarvis/analysis/thermodynamics/energetics.py#L69-L73) | Formation semantics | Subtracts elemental reference energies, divides by number of atoms. Negative formation energy is not a competing-phase stability proof. Saved as `raw/energetics-pinned.py`. |
| [Hull implementation](https://github.com/usnistgov/jarvis/blob/3b0c9d0f0c15759135de857dbc93e010db01eb29/jarvis/analysis/thermodynamics/energetics.py#L422-L428) | Hull semantics | Constructs the phase diagram from included competing compositions. Limited by the reference database, computational treatment and equilibrium assumptions. |
| [NIST primary research, Table 1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=936649) | Units | Reports formation and hull energies in eV/atom; examples show negative formation energies with positive hull distance. |
| [JARVIS overview paper](https://www.nature.com/articles/s41524-020-00440-1) | Dataset methodology | DFT materials-property infrastructure; does not validate autonomy, heredity, intelligence or abiogenesis. |

## Independent read-only source audit

The `jarvis_source_audit` specialist verified the registry and metadata independently, confirmed formation-versus-hull distinctions and reviewed the frozen screen implementation. It found no concrete selection-leakage, parsing or evidence-claim blocker. This is a source/code review, not experimental replication.
