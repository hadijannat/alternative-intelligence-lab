# Parent runtime gate after the wall-limit result

The completed run-v1 remains immutable. Its short sample places the first J call in the second direct three-center integral pass, as recorded in REPORT.md. Source-level OpenMP pragmas do not establish that the installed binary supports parallel execution.

A separate, non-chemical runtime probe imported the existing PySCF environment and called its actual thread-control interface. Observed results:

```json
{"before": 1, "request_4_return": 0, "after": 1, "scientific_operators": 0, "SCFs": 0}
```

PySCF emitted: `OpenMP is not available. Setting omp_threads to 4 has no effects.` The process used the same five original single-thread environment settings; no J, PCM, molecular calculation or SCF was performed. Host inspection reports14physical/logical CPUs and36GiB RAM, but this build cannot use OpenMP integral threading. Static binary inspection via Xcode tools was unavailable because its license gate was not accepted; the runtime probe supplies the decisive observation.

Decision: do not repeat the parent attempt with only changed thread environment variables. A separately installed OpenMP-enabled environment must pass the existing small-case numerical checks before any new parent execution. The original pinned environment must remain intact. A bounded first-J-only timing/memory diagnostic would then determine whether native parallelism makes the expensive step tractable. No new environment or parent diagnostic was launched in this continuation.

Independent source inspection also found that the parent currently discards the preparatory J before SCF requests the same initial-density J again. A carefully validated single-use reuse could avoid that duplicate calculation, at a retained J cost of75,300,992bytes. It must match density/request settings and return independent storage because consumers modify J. Native RKS already supports incremental J from a density difference and previous tagged J; inventing a second incremental algorithm is unnecessary. Neither improvement can retroactively produce the first J that failed to finish.

Full parent convergence, solution identity and target integration remain unverified. The completed W/V small-case comparison does not remove this resource limitation.
