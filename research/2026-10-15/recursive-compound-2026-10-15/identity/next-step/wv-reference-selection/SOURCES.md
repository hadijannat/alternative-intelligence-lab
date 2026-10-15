# W/V reference selection checkpoint

These computational source files were retrieved before any new W/V calculation. Selection followed availability order: WO4(2-) before HWO4(-), and VO4(3-) before HVO4(2-). Both first choices were available. No W/V SCF, comparison result, target incorporation or chemical validation is claimed.

The sources are the [WO4 ICIQ deposit](https://iochem-bd.iciq.es/browse/handle/100/28683) in the [Mo/W collection](https://doi.org/10.19061/iochem-bd-1-201), associated with [Petrus and Bo (2021)](https://doi.org/10.1021/acs.jpca.1c03292), and the [VO4 ICIQ deposit](https://iochem-bd.iciq.es/browse/handle/100/30238) in the [V/Nb/Ta collection](https://iochem-bd.iciq.es/browse/handle/100/30179). Item pages declare CC BY 4.0. The publication retains this attribution and reacquisition ledger; acquired files remain excluded under the existing archive policy.

| Local acquired file | Primary URL | SHA256 |
|---|---|---|
| raw/WO4.xyz | https://iochem-bd.iciq.es/browse/cml2xyz?id=28896&mode=single_xyz | d00419b85f8feba8e52f9b79bd1ec68d02f48094a48bd00fbdf44d599bbbe980 |
| raw/WO4.in | https://iochem-bd.iciq.es/browse/bitstream/100/28683/3/W1O4-0H.in | 9fa339898d050447b2e2bd17a8ec62b25681ecb1ae38ffb33c4283460df4ccd4 |
| raw/WO4-output.cml | https://iochem-bd.iciq.es/browse/bitstream/100/28683/4/output.cml | 2df753b648c1037e022ca529eb7f688544019bfefb291f72c062136b56be4eb0 |
| raw/VO4.xyz | https://iochem-bd.iciq.es/browse/cml2xyz?id=30433&mode=single_xyz | 2dfc20e7c1725576e9c6944aca7f93611ad544e2330c9e74a00ebe1e698afbbc |
| raw/VO4.in | https://iochem-bd.iciq.es/browse/bitstream/100/30238/3/V01O4-0H.in | d0f275dca3dbec1a445dbe0486dcf5d3c503c85fcdc7979640ea193b96bd2b9c |
| raw/VO4-output.cml | https://iochem-bd.iciq.es/browse/bitstream/100/30238/4/output.cml | a9eb7e614adeb1b851cb5bc5639388dafa7c489c0e5f4f4b5d46a78026d05a73 |

The inputs explicitly declare charges -2 and -3. Their outputs declare restricted spin. W uses ADF PBE/TZP, small frozen core, scalar ZORA and COSMO water; V additionally declares Grimme3 dispersion. These source methods differ from the proposed PySCF method. Their absolute energies are not an interchangeable benchmark, and monomer numerical agreement would not verify W/V incorporation in Mo36 or target stability.

Both CML files contain additional `a:charge` scalars in logfile modules, including zeros. The physical run charge is under the run-type symmetry module. A future parser must scope that field and test conflicting/logfile values; the earlier neutral H2Mo2O7 guard requiring a sole global charge value cannot be reused unchanged. No such parser or W/V calculation has yet been qualified.
