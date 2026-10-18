# Independent spatial Fe function review

2026-10-18. Verdict: **APPROVE for the bounded analytical/synthetic result.**
No blocking mathematical or scientific-interpretation finding remains.
This approval does not establish empirical validation, active repair,
functional inheritance, a novel compound, or an integrated life function.

## Scope and correction

Reviewed `documented-scaffold-2026-10-18/spatial-fe-function/` protocol,
amendment, acquisition/source audit, implementation, tests, report,
extraction boundary, negative ledger and numerical artifacts. Read native
SI methods on S2-S4 and checked its deposited-file identity. No response
points were digitized and no rates were fitted by this reviewer.

An initial wording finding called prior remote-Fe failures "fitted-model
failures". `AMENDMENTS.md` now correctly identifies them as failures of
unfitted synthetic models, while retaining the original protocol bytes.
The final report and analysis carry this correction.

## Mathematical findings

Set `x=N_E`. Nonnegative pools require
`max(0,N-P) <= x <= min(E,N)`. Every point in that closed interval gives
nonnegative `F_E=E-x`, `N_E=x`, `F_P=P-N+x`, `N_P=N-x`, so the interval is
both necessary and sufficient. Incoming current is affine in x; its exact
attainable bounds are the lesser and greater of the two endpoint values.
This also handles reversed and equal regional competence.

For the frozen main case the endpoints are x=0.1 and x=0.4, incoming
current is 1.3 and 4.0, and total current remains 7.5. The positive lower
bound is conditional information; the report correctly does not interpret
it as observed incoming-material activity.

The direction `(1,-1,-1,1)` preserves edge total, plane total, incoming
total and total current. Incoming current changes by `k_P-k_E=-9` per
unit direction in the main example. The measurement matrix has rank 3;
adding an independently observed incoming-edge pool gives rank 4.
Equal positive competence identifies the incoming contribution `k*N`;
zero/all incoming Fe, one empty region and zero inventories are correctly
retained as identifying controls. Zero activity in only one region does
not generally identify that contribution. Full algebraic rank still
does not establish the assumed competence, background, inactive-site
fractions, chemical repair or heredity.

## Captured verification

All invocations used workspace cwd and installed Python
`/USER_HOME/.pyenv/versions/3.12.3/bin/python3`, with
`PYTHONDONTWRITEBYTECODE=1`. No implementation or scientific-result files
were modified by review. Captured review outputs are recorded below in
this artifact.

### Unit-test scenario

Invocation:

```sh
PYTHONDONTWRITEBYTECODE=1 /USER_HOME/.pyenv/versions/3.12.3/bin/python3 -m unittest discover -s documented-scaffold-2026-10-18/spatial-fe-function -p test_model.py -v
```

Observed exit 0, three tests passed:

```text
test_attainable_bounds_and_same_observations ... ok
test_invalid_inputs_and_allocations ... ok
test_reversed_site_competence_and_equal_control ... ok
Ran 3 tests in 0.000s
OK
```

Binary observable: exit 0 and `OK`. Implementation's separately captured
run is `spatial-fe-function/results/test-output.txt`.

### Independent stored-allocation audit

Invocation: the same Python binary with `-c` and the following read-only
program. It independently reconstructs currents and bounds from each CSV
row and its case input, without calling implementation functions.

```python
import csv, json
from pathlib import Path
import numpy as np
p = Path('documented-scaffold-2026-10-18/spatial-fe-function')
a = json.loads((p/'results/analysis.json').read_text())
rows = list(csv.DictReader((p/'results/grid_allocations.csv').open()))
worst = 0.0
counts = {}
for r in rows:
    c = a['grid_cases'][int(r['case_id'])]
    z = c['inputs']
    fE,nE,fP,nP = [float(r[k]) for k in
                    ('founder_edge','new_edge','founder_plane','new_plane')]
    E,P,N,ke,kp,b = [z[k] for k in
                    ('edge','plane','incoming','k_edge','k_plane','background')]
    jn = ke*nE + kp*nP
    current = b + ke*(fE+nE) + kp*(fP+nP)
    lo,hi = max(0,N-P),min(E,N)
    bounds = sorted((kp*N+(ke-kp)*lo,kp*N+(ke-kp)*hi))
    err = max(abs(fE+nE-E), abs(fP+nP-P), abs(nE+nP-N),
              abs(current-float(r['total_current'])),
              abs(jn-float(r['new_current'])),max(0,-min(fE,nE,fP,nP)),
              abs(bounds[0]-c['new_current_bounds'][0]),
              abs(bounds[1]-c['new_current_bounds'][1]))
    worst = max(worst,err)
    counts[int(r['case_id'])] = counts.get(int(r['case_id']),0)+1
assert len(rows)==15120 and len(counts)==720
assert set(counts.values())=={21} and worst<1e-12
A = np.array(a['linear_algebra']['matrix'])
assert np.all(A@np.array([1,-1,-1,1])==0)
assert np.linalg.matrix_rank(A)==3
assert np.linalg.matrix_rank(np.vstack((A,[0,1,0,0])))==4
assert a['empirical_held_out_validation']['status']=='INSUFFICIENT_DATA'
assert a['empirical_held_out_validation']['training_points']==0
assert a['empirical_held_out_validation']['held_out_points']==0
print(len(rows),len(counts),worst,'PASS_ALGEBRA_ONLY')
```

Captured output: 15,120 rows, 720 cases, independent maximum residual
`3.552713678800501e-15`, rank 3, augmented rank 4,
`PASS_ALGEBRA_ONLY`; exit 0. Binary observable: all assertions pass.
The implementation's own recorded maximum is
`4.440892098500626e-16`; the slightly different expression ordering in
the independent reconstruction accounts for a different rounding residual.
Both remain below the frozen absolute tolerance 1e-12.

### Source identity and claims

Read-only invocation: Python `-c` loading the native PDF through PyMuPDF,
hashing its bytes through hashlib, and comparing `supplied_md5` with
`sources/figshare-28718969.json`. Binary assertions: exact resource DOI
`10.1021/jacs.5c00438`, 35 PDF pages, zero embedded files, one deposited
file, and matching MD5. Captured output: all assertions passed; exit 0;
1,342,459 bytes, CC BY-NC 4.0, SHA-256
`658e8a17f67d282b219ea77cefb59aa59dccfe1deb06555b7a7a3f93e1f6dca1`.

Native S2-S4 confirms total-Fe TOF normalization, changing Fe loading with
preparation potential, and the different bulk/SECCM/Raman supports and
conditions. Oxygen labelling follows oxygen; it supplies no Fe origin
label. The source audit keeps unavailable-main-text claims bounded. The
current model is correctly described as a static favorable limiting
observation model with arbitrary dimensionless coefficients, rather than
a fitted transport law or a measured new compound.

### Negative-result preservation

Read-only invocation: Python `-c` loading
`documented-scaffold-2026-10-18/remote-fe-transport/results/analysis.json`
and printing `checks` and
`synthetic.lower_sink_minus_higher_sink_A_5h`. Captured observables:
`step_convergence_below_1e_minus_5: false`; all five `reversal` flags false
for ka in `{0,0.1,1,10,100}`. These source results remain present.
The new report and SF10 explicitly preserve both failures.
The new ledger retains 11 negative results and labels the empirical screen
INSUFFICIENT_DATA with zero training/held-out points. No historical failure
is reclassified as a successful empirical validation.

## Reviewed artifact hashes

All declared input hashes in final `analysis.json` matched current source
bytes at review.

| Artifact | SHA-256 |
|---|---|
| analyze.py | 2affe76c99fc55a7574783db2a60e844e9e217cef5713d46ddc24bdf86455acb |
| test_model.py | e63f298dff4bc073e82d1ba526a998bca29630eb9517705c825b07a2398905a4 |
| REPORT.md | 9b2e5c72f42d43381c71e8514f38aad4d4f68bb46d14ae7ca1a7e39317d92a65 |
| NEGATIVE_RESULTS.json | fa7300ac11bf735e7142f097d4478f88245c22d1cc849d8b303c040573682d6e |
| results/analysis.json | c15ef4d801f523ad0b34095832f640d74b76dcd703857cac68964746de4884d6 |
| results/grid_allocations.csv | ef2d8dcf1ab308e9d4f4d336df837d206cc067540d9f8f771ad075af70844e03 |

No unavailable main article, raw experimental response dataset, physical
experiment or empirical held-out model performance was independently
verified. Those limits remain explicit; no life-function requirement closes.
