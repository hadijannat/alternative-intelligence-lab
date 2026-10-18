# Physical-learning source acquisition and schema audit

Primary experiment: Dillavou et al., PNAS121,e2319718121(2024),
[DOI10.1073/pnas.2319718121](https://doi.org/10.1073/pnas.2319718121),
PMCIDPMC11252732. Existing verified native XML is reused by reference in
`sources/browser-receipt.json`; its CC BY-NC-ND4.0 article license is distinct
from the repository licenses. No source code from the deposits was executed.

## Native bytes and provenance

| Asset | Current result | Independent repository evidence |
|---|---|---|
| [Dryad data](https://datadryad.org/dataset/doi:10.5061/dryad.8w9ghx3vx) | Native data.zip acquired,15,756,671bytes | Current file3283458 size/SHA256 match exactly; CC0 metadata |
| Dryad README | Native3135bytes acquired | Current file3283475 size/SHA256 match exactly |
| [Zenodo software](https://zenodo.org/records/12009234) | Native PNASscriptFig3.m acquired,9277bytes | MD5b1d791f1f80fabeb8699500e0592a261 matches the normal-browser file table; MIT metadata |
| Other software assets | Native helperZIP and Fig2/4/5/6 scripts remain unacquired | Public page lists them; direct403 bodies and browser timeouts retained |

Native files are in `sources/browser-native/`. Current metadata/receipts are
in `sources/attempt1/`, `sources/attempt2/` and `sources/browser-receipt.json`.
Exact dataset SHA256 is
`f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c`.
The data registry identifies version4 and curationStatusPublished while its
versionStatus field reads submitted; this source metadata is retained as-is.
Software concept DOI12009232 resolves to12009234; it is not another data mirror.

Normal public Chrome access supplied the actual data/README/Fig3 files.
Download-event timeouts did not prove absent transfers: subsequent narrow
source-file integrity checks found exact expected native bytes. The duplicate
full-dataset wrapper archives have different bytes and are not substituted for
the native data.zip hash. `sources/browser-observations.json` distinguishes
observed UI, returned handles, local bytes and unconfirmed transfers.

## Complete archive and MATLAB storage inventory

`inventory.py` safely checks the entire retained ZIP before reading MAT files.
There are404central-directory entries including directories/AppleDouble
metadata,201MAT files and16,237,245expanded bytes. All ZIP CRCs pass; no absolute,
parent-traversal or symlink entry was found. No archive-contained code runs.

All201MAT files parse at the storage level using the existing isolated project
interpreter, Python3.12.3/NumPy2.4.1/SciPy1.18.1. The default interpreter's
PROPACK import failure remains recorded; no global repair or install occurred.

-200MAT files store an `experiment` object as opaqueMCOS classExperiment2.
  This class is also used by calibration files;200objects are not asserted to
  be200independent learning tasks. Ordinary loadmat exposes class/reference
  metadata and a byte workspace, without named property/value associations.
- For the named XOR file, the opaque object shape is(1,), its uint32 object
  metadata shape is(6,1), and the function-workspace uint8 shape is(1,1559048).
  whosmat fails on this object; successful loadmat is not resolved property access.
- `data/OscilloscopeData.mat` is transparent: numeric T2,float64,shape(100,3).
  The native README maps its columns to time,input voltage,output voltage.
  No values or response outcomes were inspected or calculated.

All filenames/top-level shapes/types are preserved in
`sources/native-inventory.json`. No MCOS property association is guessed.

## What remains unverified

The native README describes TRAIN/TEST source-target arrays, capacitor
histories, learning intervals and free/clamped node states. The verified Fig3
script references those properties and stored measurement/error fields.
Those descriptions cannot establish the actual property arrays, TRAIN/TEST
overlap, initial-validity rules, units or causal controls until an independently
qualified MCOS reader or author-compatible MATLAB export resolves them.

A later protocol must freeze source mapping, run inclusion, available causal
controls and baselines before response calculations. It must retain all runs,
and avoid copying a plotting script's display filtering or validity conventions
as scientific exclusions. No discarded row, digitized proxy, reconstructed
time series or unmeasured learning state is invented here.

The source describes supervised physical learning through local analog updates.
It does not supply chemical maintenance/resource control, learned-state
renewal or same-system PMo12/Mo34WV integration. Thus this acquisition can
support a future scoped A/C comparator audit; it closes no integrated requirement.
