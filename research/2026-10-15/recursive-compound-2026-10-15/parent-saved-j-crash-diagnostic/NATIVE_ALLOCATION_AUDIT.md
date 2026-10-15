# Native allocation source audit

The installed PySCF C source accompanying the pinned runtime requests approximately 12.8 GB across four workers for two scratch allocations alone. This corrects the earlier assumed 4 GiB scratch allowance. Requested capacity is not measured resident memory, and this audit does not identify the cause of the saved-J parent's SIGTRAP. No operator, SCF, native allocation experiment or runtime change was performed.

## Provenance and call path

Paths below are relative to `../parent-openmp/env-aligned/lib/python3.12/site-packages/pyscf/`. The earlier runtime inventory pins native binaries and selected Python/data files, but excludes `.c` files. The current C-source hashes below identify the inspected files; they do not prove that those exact files produced the pinned binaries.

`df/df_jk.py:459-502` converts the density to C-order float64 and calls the native direct contraction twice: `ijkl,ji->kl` with `hermi=0`, then `ijkl,lk->ij` with `hermi=1`. Both use `s2ij` and one density/component in this parent case. The parent has 36 Mo, 128 O and 32 H atoms, 3,068 AO functions in 1,260 shells, and 19,612 auxiliary functions in 5,156 shells. The auxiliary Mo basis includes I functions (l=6), giving maximum spherical shell dimension d=13. Including the dummy fourth shell, the supplied shell slice is `(0,1260,0,1260,1260,6416,6416,6417)`.

## Allocation arithmetic

In `lib/vhf/nr_direct.c:377-427`, let K be the integral cache size in doubles. For n_dm=ncomp=1 the requested JK capacity is `L = 400000000 - d^4 - K`, provided L is nonnegative. Inside the OpenMP region each worker receives:

- JK data: `8*(L + 136^2)` bytes (`CVHFallocate_JKArray`, lines233-263), without clipping to output size.
- Integral/cache workspace: `8*(d^4 + 2*d^2 + K)` bytes (line427).

Their sum is `8*(400000000 + 136^2 + 2*d^2)` bytes. At d=13 this equals **3,200,150,672 bytes per worker**, or **12,800,602,688 bytes for four workers** (11.921490252 GiB), before keys, output pointers, reordered density, result arrays and other allocations. The K and d^4 terms cancel algebraically; no measured K is claimed.

`lib/vhf/nr_direct_dot.c:180-190` assigns and zeroes output blocks only when first visited. Distinct logical output is 19,612 doubles in pass1 and at most 3,068 squared = 9,412,624 doubles (75,300,992 bytes) in pass2. These logical extents do not bound workspace touches, allocator retention or total residency. Therefore the source arithmetic neither contradicts the recorded sampled RSS of 7,584,022,528 bytes nor proves a 10 GiB RSS breach. The previous 4 GiB scratch allowance cannot certify total requested allocation; earlier arithmetic margins must not be used as launch clearance.

## Index and failure boundaries

In `lib/vhf/optimizer.c:321,344`, both three-center prescreens assert `k < n`, where n is the 1,260 AO-shell count and k ranges over 5,156 auxiliary shells. That assertion is inconsistent with this intended auxiliary range. The actual q_cond allocation is n squared plus naux = 1,592,756 entries, and the referenced `n*n+k` indices fit that allocation. Pass1 dm_cond has n squared = 1,587,600 entries; pass2 has 5,156 entries. The assertion mismatch alone is not an out-of-bounds-write finding or an explanation for the allocator trap. Whether that assertion was active in the binary is not established here.

The density's sign or indefiniteness does not alter these dimensions; pass2 builds its screening array from absolute auxiliary-density values. Static review found no demonstrated invalid write or wrapper misuse. The exact failed incremental density was not saved, so a future synthetic density would not be an exact replay. Source inspection and integer models cannot establish heap integrity or repair the original run.

## Inspected source identities

The separate stdlib-only [integer replay](allocation-audit.json) is PASS_SOURCE_ONLY_INTEGER_MODEL. It parses the actual parent atom order and installed basis text, deriving the shell counts above,49AO blocks and314auxiliary blocks at AO_BLOCK_SIZE64. It checks every unique output key and output shell-pair writeback interval:314keys/5,156intervals for pass1 and2,401keys/1,587,600intervals for pass2. Forward/reverse representative insertion orders with repeated keys fit the modeled bounds for predeclared mock cache sizes0,10,000and1,000,000doubles. These are not measured native cache sizes. Seven portable synthetic tests pass;33guarded source/input/pilot files remained unchanged. Coverage excludes actual libcint writes, other cache sizes, native concurrency, allocation success and heap ownership.

`allocation-audit-pre-portability.json` preserves the earlier successful audit with its earlier test-file digest. It is historical and superseded by `allocation-audit.json` after replacing the source-dependent unit test with a portable synthetic test and rerunning the separate source replay. Both retain the same numerical observations; publication validation must use the final audit. See `../../.omo/evidence/native-index-model.md` for invocation, hashes and preserved initial parser/guard corrections.

| File | SHA256 |
|---|---|
| `lib/vhf/nr_direct.c` | `9c181daa8ce689e312e548694f47a2935105094fab1e685e82b4bf485e0639c4` |
| `lib/vhf/nr_direct_dot.c` | `3db439ca3438b8291ac3510e463d8b8cb7c7ba66d8e95f305161843819745fc8` |
| `lib/vhf/optimizer.c` | `bc2c1890058633ab06efe4f421e740562fe7a668dae6d6e0d42e7da7a7a4200b` |
| `gto/basis/def2-universal-jkfit.dat` | `8970edf068a6010954535eb2b1ee978900dbea989b20e305c730dabb0298de5a` |

The failed pilot, frozen inputs and all negative results remain unchanged. Packed PCM work and any parent retry require a separate reviewed diagnostic protocol; this note supplies neither parent feasibility nor chemical-function evidence.
