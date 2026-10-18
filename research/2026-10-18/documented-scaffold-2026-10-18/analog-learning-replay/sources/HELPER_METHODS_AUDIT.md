# Native helper methods: schedule and measurement semantics

New source acquisition on2026-10-18, after the first replay stopped at its
frozen binary-DOTEST rule. No response score, learning error or other outcome
was calculated in this source audit. Root owns all replay protocol/code/results.

## Acquired native source

The narrow initial check found no `Downloads/helper_scripts.zip`. One normal
Chrome downloadMedia action on the actually displayed public Zenodo link then
returned that native path. No purchase, login change, author contact or bypass
was performed. The public record is
[Zenodo12009234](https://zenodo.org/records/12009234), versionv1,MIT license.

The native ZIP has50,569bytes, repository-matching
MD5`b9b06b71f3b709445f97d4386366fe76`, and
SHA256`7c65cecb1b2cf19b7bb5f665c9b44695bb805d47214f38a9945ddffd5202cd46`.
Its14entries pass ZIP CRC/safety checks. Six logical MATLAB source files were
extracted as bytes into `helper-native/`; AppleDouble metadata remains inside
the intact ZIP. Receipt: `attachment-receipt.json`. Original failed attempts
and the earlier successful three-file receipt were not overwritten.

`helper-native/Experiment2.m` has189,506bytes and
SHA256`d95070097420a6e2f382e087089dd152f8edb1cab1bb39b98720e43ee6eb0cf3`.
Line references below refer to those exact retained bytes; CRLF is preserved.
No deposited MATLAB source was executed.

## Primary source semantics

| Question | Native source lines | Finding and limit |
|---|---|---|
| What is DOTEST? | Experiment2.m:69;425-427 | Measurement/test schedule indices, one row. It is not declared or validated as a binary performed-test flag. |
| Is that description used operationally? | Experiment2.m:718-728;1280-1290 | DOTEST(m)-1 enters cyclic training-index arithmetic; a requested training step is located by equality against DOTEST. These operations contradict the binary-flag interpretation. |
| Is the schedule supplied to apparatus? | Experiment2.m:86;613-650 | DOTEST belongs to DATANAMES; sendData sends array values to the Arduino. The actual acquisition/controller firmware is not among these six deposited helper files. |
| What are stored output tensor axes? | Experiment2.m:138-140;264-267 | TestMeasurements uses(TAR,TST,MES),TrainMeasurements uses(TAR,TRA,MES),LearnTimes uses(1,MES). |
| What are node-state axes? | Experiment2.m:168-175 | Train state records the last training point at each snapshot; TestFreeState/TestClampedState use(row,col,MES,TST), with the whole test set measured at each snapshot. Comments place the clamped state before the scheduled update. |
| How are outputs linked to nodes? | Experiment2.m:4140-4162;4198-4218 | Methods compare TestMeasurements(target,:,snapshot) with TestFreeState(TLOC(target)+1,snapshot,:) at the same snapshot. No row shift is applied. These are intended consistency mappings, not evidence that every deposited row numerically agrees. |
| Which labels/measurements are compared? | Experiment2.m:752-758;770-811 | CalcError uses TEST target rows after SOR and the corresponding TestMeasurements tensor; TST>0 enables test-error calculation. It does not treat DOTEST==1 as a validity predicate. |
| What is the differential sign? | Experiment2.m:781-787;2950-2953 | CalcError uses first-minus-second for both labels and outputs; classification uses second-minus-first, as does the verified Fig3 script. Squared errors are unchanged if both use the same convention; signed outputs require a declared consistent convention. |
| How is elapsed learning time handled? | Experiment2.m:1047;4268;4365;verified Fig3:45 | Cumulative LearnTimes is converted from microseconds to milliseconds or seconds. Acquisition/handling overhead is not thereby included. |

The `getDimensions` convenience method at274-275 groups TestFreeState with
three-dimensional properties and omits its TST axis, while the dedicated
property declaration and measurement-consistency methods include that axis.
Use the explicit tensor declarations and direct mapping, retaining this source
inconsistency instead of treating the convenience method as a complete schema.

## Initial row, ordering and valid-snapshot limit

The source helper does not supply a universal first-row deletion or signed-sum
test. Its plotting and error methods operate across stored snapshots. Some
plots choose later display snapshots; that does not establish that all first
rows are placeholders. All-zero signed sums can also occur in valid physical
data, so such a sum cannot become an exclusion rule.

DOTEST is a scheduled training-step coordinate, not an observation-validity
flag. The exact event ordering of controller acquisition, training and save
operations cannot be reconstructed solely from this class's sender/analysis
methods. The full serial acquisition/firmware code is absent from this helper
package. A future replay may use source-grounded shape/finite-value and
same-snapshot mapping checks, retaining any malformed/inconsistent snapshot
with an explicit reason; it cannot silently make schedule1 uniquely valid.

This is new primary source evidence that justifies considering a documented
amendment to the binary-DOTEST assumption. It does not itself amend the frozen
root protocol, reinterpret failed replay output as a pass, verify actual
snapshot consistency, or establish generalization/chemical adaptation.

## Verification

`python3 -B documented-scaffold-2026-10-18/analog-learning-replay/sources/verify_helper_attachment.py`
checks native hashes/size, all archive CRCs, six extracted source hashes,MIT
metadata and the no-execution/no-response-replay record. The original source
verifier and original acquisition/inventory files remain unchanged.

## Subsequent precision/readout follow-up

This bounded follow-up was requested after root's amended replay stopped at
the frozen same-snapshot mapping tolerance. No task error was calculated here,
and no tolerance or canonical mapping was changed.

Native `Experiment2.m:422-423` rounds SENDTRAIN/SENDTEST times255. These are
the commanded stimulus arrays, not an assignment to the stored measurement
arrays, so those lines cannot independently calibrate readout precision.
`Experiment2.m:192-198` specifies NODEMULT=4.985/11 and GATEMULT=4.985*2
for converting normalized measurements/parameters to volts. These constants
give physical scale, not an error bound. REP is described as measurement
repetitions at26; RES is edge-reset duration at36, not ADC resolution.
ExperimentGroup.m:35 gives a differing RES description in cycles, reinforcing
that it is a reset parameter rather than readout bit depth.

The class supplies no native assignment/receiver method showing how the two
readout tensors are populated or normalized from raw ADC codes. Its
`measurementConsistency` method at4198-4218 returns their maximum discrepancy;
it does not assert bitwise or1e-12 equality. `logic_truth_table3.m:15-21`
initially selects TestMeasurements, then overwrites the plotted outputs with
the corresponding TestFreeState nodes. That plotting choice is not a precision
specification and does not authorize changing a frozen canonical observation.

An exact primary preprint methods check adds independent hardware evidence:
[arXiv2311.00537v2](https://arxiv.org/html/2311.00537v2), AppendixE.3
Supervisor Circuitry and E.4 Measurement Circuitry. The source describes8-bit
applied/measured voltages, individual multiplexed reads,11x node amplification,
TLC0820ACN ADC conversion, nominal node spacing Vmax/256 (about1.8mV), and
repeated/averaged measurements. This was inspected in the web reader; no new
native preprint/SI payload is claimed by this follow-up.

This hardware description supports finite resolution independently of the
observed discrepancy. It does not specify the exact conversion/averaging path
for each stored property, distinguish /255 from /256 normalization in those
properties, or prove whether they are copied values versus separate captures.
Nominal ADC bin spacing is not a calibrated deterministic uncertainty bound
for the difference between two recorded tensors. Analog noise, settling,
rounding, channel offsets and acquisition order remain unquantified here.

**Decision:** no independently justified per-record discrepancy bound was
established. Preserve the frozen mapping failure and leave full-performance
replay failed/uncomputed. A new bound cannot be chosen from its observed
maximum. The missing discriminator is the actual acquisition/receiver mapping
and readout normalization/precision metadata, or a separately calibrated
same-node capture comparison with known timing and uncertainty.
