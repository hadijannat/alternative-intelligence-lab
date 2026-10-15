# First parent pilot: resource preflight rejected

The fixed hypothetical P0_A input passed atom, heavy-coordinate, charge and basis checks, then exited before SCF. Its 9,284 SWIG surface points imply 689,541,248 bytes for one dense surface matrix. The frozen screening formula gives 15,938,308,608 bytes (14.843706608 GiB), exceeding the unchanged 10 GiB limit. This is an estimated allocation budget, not observed peak memory and not chemical evidence against the parent.

The worker returned 2 and the supervisor returned 1. No monitoring error or forced termination occurred. Wall time was 0.836 s; sampled maximum child RSS was 102,957,056 bytes. These observations cover input construction and preflight only. No SCF iteration, electronic energy, convergence outcome, orbital stability, geometry optimization or proton-arrangement comparison exists.

Artifacts: [preflight.json](run-v1/preflight.json), [supervisor.json](run-v1/supervisor.json), [stdout.txt](run-v1/stdout.txt), [stderr.txt](run-v1/stderr.txt), [native.log](run-v1/native.log). The original [protocol](PROTOCOL.md), script and run-v1 remain unchanged. Source/input/method hashes are recorded in preflight.json.

Follow-up inspection found a second resource obstacle: the installed PCM AO-surface contractions impose at least 400 surface points per block. At 3,068 AOs, a single such float64 tensor occupies 30,120,396,800 bytes (28.051805496 GiB), before other arrays. Omitting the unused C-PCM D matrix alone would therefore be insufficient.

The separate [blocked implementation qualification](../cpcm-blocked/PROTOCOL.md) keeps the C-PCM/SWIG equations, mesh and chemistry fixed while testing bounded matrix construction and smaller AO-surface blocks. It must match the installed operator and small-reference results before any new parent run. The parent RSS and wall limits are not raised. Physical admission and every unverified integrated function remain unresolved.
