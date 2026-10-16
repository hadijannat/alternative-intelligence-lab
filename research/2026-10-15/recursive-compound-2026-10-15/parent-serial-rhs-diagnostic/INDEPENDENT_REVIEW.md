# Independent serial RHS terminal/result review

Date: 2026-10-16. Publication scope: this completed diagnostic and its bounded observations.

- codeQualityStatus: CLEAR
- recommendation: APPROVE for recording/publishing the scoped result
- publication-blocking defects: []
- Exact execution classification: COMPLETED_SERIAL_RHS_PREFIX_DIAGNOSTIC_ONLY
- Serial RHS repeat criterion: PASS, byte-identical finite float64(19612,1) arrays
- Full-J criterion: UNTESTED in this run; prior full-J failures remain in force

## Independent terminal and integrity checks

PID10645 has no process row (`ps` exit1, empty output). Supervisor returncode0, no termination_reason or monitor_error. Wall893.8663067501038s against1800s cap. Independently recomputed the sampled maximum across4214 samples:3,627,646,976 bytes against10,737,418,240-byte guard. Sampling does not certify peak memory or general runtime safety.

Independently streamed all30 artifact hashes from launch-result.json; all match. No extra run files were found other than launch-result.json itself. Embedded receipt equals supervisor.json. Both output file hashes match their closed-output/per-call/result receipts. Rechecked473/474 grouped preparation pins; only the3,077,044,480-byte saved original metric was left to root's complete rehash. Approval-bound prelaunch review, preparation, inherited qualification mapping and launch token bindings all match. Neither prelaunch review nor any source/scientific artifact was modified.

Preparation SHA256: `0da90217f8074035deb9902173fb9bd3aa53d7679be4e56c0ec4736eded2f92b`.
Approval SHA256: `363d3533814b94a3624657d576b85ef77663c6d5083466ae48b27f9f2d5bf569`.

Terminal SHA256 values:

- launch-result.json: `3fa2f87cccef225fb1eaf227d8ae83c7da914c2a21c6f409dce39fb707cdf510`
- result.json: `6f81389778cc31a7ab7908353cdfce8034541ed554935dcb97bd33bf8d2a0afb`
- supervisor.json: `7162f57e5d6f2de57fd995d05f162e462f0f359c4b1d3c1b4838554cbc0397cf`
- both b_A.npy and b_B.npy: `aa5ed22825b38ee7f5dcd9c5b30b966b530117df5901cc356315a7e71b3e4260`

## Counts, control and storage

Receipts and stages agree: two prefix attempts, two pass1 entries/returns, two sentinel captures, one factorization; zero solves, completed J calls, SCFs and PCM builds. No metric-completion file is present, consistent with interruption before the MemoryRI completion callback rather than missing completed-J evidence. The prelaunch source audit establishes sentinel placement before solver/pass2; this result review checks the resulting counters and artifacts, not independent native tracing.

Pass1 entry/return configured PySCF getters are1 for both attempts. All before/after prefix/setup snapshots report BLAS1/PySCF4, initial/restored getters4/4, with implicit-control-mode restoration explicitly false. All recorded native binary/_flapack hashes were independently recomputed and match. The child-recorded common dpotrf symbol observation is preserved. Configured getters are not measured team sizes.

Immediate pass1 durations from recorded boundary timestamps: A413.118078834028s, B415.104663166916s. Inherited factor timestamps are deferred and must not be read as native factorization duration.

One factor-alias receipt and two equal factor-state records have the same pointer, content digest, readonly and Fortran flags; actual input/factor pointer equality and shared-memory flag are recorded. Original metric content digest `f972103f0d3473f6b899e0a77aa1206a783b68ba97a550707e5fea80edbc7d6f` matches saved replay. Factor digest `261d6cbcbe2d0ee2b42f3dfb064570df01ca831676e968591518f6083c242c0e` matches saved replay and both prefix states. The new original metric/factor arrays were not retained, so this verifies receipt consistency rather than independent elementwise factor reconstruction.

## Independently recomputed RHS observations

Loaded both NPY arrays with allow_pickle=False. Both are finite float64(19612,1); their payload bytes and entire NPY files are identical. B−A maximum and RMS are0, numeric unequal entries0. No production difference helper was imported.

Independently compared each new array with both prior explicit-BLAS1/PySCF4 RHS arrays. Both new arms give the same results:

| Historical RHS | Maximum absolute difference | Unequal entries | RMS using math.fsum |
|---|---:|---:|---:|
| old A |8.958522812463343e-11|19534|3.137543033453138e-12|
| old B |8.913048077374697e-11|19519|3.1443040370662376e-12|

Maxima/counts agree exactly with saved comparisons; RMS agrees within1e-15 relative, with final-digit summation-order differences. These are descriptive differences, not a chemical/J-error threshold. Byte identity of this pair does not establish general determinism across runs or platforms.

## Preserved negatives and publication boundary

The prior explicit-J result remains pinned and reports repeated full-J maximum error6.702407517877873e-10,630 entries above the unchanged1e-10 absolute/rtol0 bound. Historical comparisons also remain failed: A2.560511802585097e-10/80 entries; B8.22808488010196e-10/790 entries. This RHS-prefix run contains no solve or second contraction, so it cannot reverse those failures or qualify the full operator. Do not compare RHS differences numerically to the full-J threshold as though they were the same observable.

The permissible observation is that the two RHS realizations under scoped serial pass1 were bitwise equal in this one retained experiment, while prior four-thread RHS realizations differed. This does not isolate an exclusive causal mechanism, prove native reduction ordering as the cause, establish solve/pass2 repeatability, or demonstrate physical chemistry. No parent SCF, holdout consumption, W/V transfer, exact Mo34WV identity, retention, inheritance or life/intelligence admission follows. No downstream execution is authorized by this report.

## Findings and review perspectives

CRITICAL: none. HIGH: none. MEDIUM: none. LOW: no new result/publication defect. Existing prelaunch script-style limitations remain without changing the result classification.

Programming and remove-ai-slops perspectives were previously loaded and applied to the source review and this artifact audit. No code/test changes or prose-pinning tests were added. No native rerun or web access occurred. Only this report was written. Skipped the large saved-metric rehash assigned to root, actual native team tracing and nonretained factor elementwise verification; publication must preserve these limits and all prior full-J failures.
