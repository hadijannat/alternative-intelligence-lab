# Blocked parent pilot: retained wall-limit result

The single reviewed launch terminated at the900-second wall limit, with supervisor wall time900.208349750seconds and child returncode-15. The child process is confirmed absent. No SCF cycle was reported and no converged energy or SCF-result.json exists. This is a resource-limited numerical outcome, not chemical rejection or evidence of nonconvergence after completed iterations.

Sampled maximum RSS was7,103,660,032bytes (6.615798950GiB), below the10GiB sampled guard. The matrix and Cholesky build completed1.849427875seconds after worker setup; the last stage was SCF_start. A one-second macOS sample during initialization placed826samples in the direct integral driver CVHFnr_direct_drv. This local observation identifies work in progress, not the full-run fraction of time. Its separately reported physical-footprint peak9.2G is not the supervisor RSS metric. No certified peak-memory bound is claimed.

All11 frozen pins remain unchanged. run-v1 retains stages, raw native log, stdout/stderr, sample trace and supervisor/launch receipts. The original parent-pilot rejection remains intact. No retry or increased budget occurred. Next numerical work must qualify a tractable direct-Coulomb alternative separately; the new published-parent comparison also requires explicit proton-topology alternatives before target substitution. No target, gradient, stability, geometry-optimization or physical function result follows.

## Historical preparation record

Before launch, the surface-only preflight and nine non-SCF self-checks passed. The full run directory was absent then. No surface S matrix, Cholesky factor or parent SCF was calculated during preparation. Those prelaunch checks deliberately require an absent run directory; they are not a command to overwrite or repeat this completed attempt.

The actual P0_A preflight confirmed 196 atoms, 3068 AOs, 1568 explicit electrons, charge -8, spin 0 trial and 9284 SWIG surface points. Frozen allocation screening totals 9,538,078,608 bytes (8.883027926 GiB), below 10 GiB. It includes three surface matrices, eight 128-row temporaries, a surface-size Boolean array, one AO8 tensor, 32 AO buffers, one nuclear block and 4 GiB scratch allowance. This is an allowance-based screen, not a certified memory upper bound.

`preflight-v1/preflight.json` records all input, qualified implementation, qualification result, installed PCM, original supervisor, new driver and protocol hashes plus allocation terms. The original supervisor was reused unchanged by import. Its observed surface-only child exited 0 in 0.8345 seconds with sampled maximum RSS 104,300,544 bytes. That measurement concerns only surface preflight, not the future solver/SCF. The 900-second wall cap, 10 GiB sampled RSS guard and five single-thread environment requests remain unchanged.

The driver logs stages before/after basis creation, surface screening, solvent matrix/factor build and SCF; per-cycle energies/residuals remain diagnostics. All terminal exceptions and supervisor outcomes remain recorded. It refuses existing run directories. Full solvent-aware residual, electron trace, convergence, finite energy and absent four-center ERIs determine the eventual numerical verdict. Unsupported physical, gradient, stability and chemistry claims remain false.

## Actual preparation invocations

From workspace root, using the existing interpreter:

```sh
./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/parent-pilot-blocked/selfcheck.py
./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/parent-pilot-blocked/pilot.py --preflight
```

`selfcheck.json` and `selfcheck.stdout.txt` contain the scenarios, exact binary observables and passing verdicts: frozen arithmetic; AO tensor arithmetic; original supervisor identity; caps/thread requests; all pins; overwrite rejection; fresh destination behavior; fail-closed hash mismatch; and absent parent-run artifacts. `preflight-v1/` retains raw stdout/stderr, native log, stages, preflight and supervisor/result receipts. Empty stderr is the actual no-error output.

## Executed launch invocation — do not repeat

Executed once after root and independent review, from workspace root:

```sh
./discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python -B recursive-compound-2026-10-15/parent-pilot-blocked/pilot.py --launch
```

This created one fresh run-v1 under the frozen limits. The retained wall-limit outcome is described above. Converged parent throughput, complete solvent contraction at parent scale, numerical stability and physical admission remain unresolved.
