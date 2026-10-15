# Exact-version isolated OpenMP alignment

PASS for required installed-source equality and native runtime support only. Initial env and its prior receipts preserved; initial-env-qualification-prerequisite.json records its SciPy source mismatch.

All-conda binary solve succeeded for Python3.12.3,NumPy2.4.1,SciPy1.18.1,h5py3.16.0,PySCF2.14.0. PySCF package has py311 in build label but noarch Python metadata and unversioned Python dependency. Current arm64 solver accepted it with Python3.12.3 and imports passed. Exact62-package URLs/MD5s in aligned-explicit-spec.txt and package SHA256s in aligned-solve.stdout.

Invocation: `python3 recursive-compound-2026-10-15/parent-openmp/guard-aligned.py solve`, then same script with `install`. Exit0,16.123s install, max sampled cumulative logical bytes1,756,830,681; additional allocation below1.5GB and cumulative below3GB guard. Cache is shared locally with initial installation. No compilation/global changes. Sampling does not certify instantaneous peaks.

Validation invocation: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 recursive-compound-2026-10-15/parent-openmp/env-aligned/bin/python recursive-compound-2026-10-15/parent-openmp/probe-aligned.py`

Exit0. Asserts verify all five exact versions, and every installed-site-packages pin in cpcm-rij-memory/source_pins.json. Four matches: PySCF df/df_jk.py, solvent/pcm.py, def2-universal-jkfit.dat and SciPy linalg/_decomp_cholesky.py (8049dead6bf409e4e0d45cefb9c3d0e05974fc6df8c3f735d74cf97c48a83f91). aligned-source-checks.json records expected and actual SHA256s. Native thread assertions require PySCF1→4→1 and actual OpenMP teams1→4→1; aligned-probe-result.json captures distinct four-worker identifiers. Python callbacks hold the GIL; this demonstrates worker creation, not speedup.

aligned-source-binary-pins.json freezes824+ sources/native/package metadata. All records copied to .omo/evidence/parent-openmp. No molecular operators or SCFs performed. No numerical equivalence or performance claim; root owns frozen numerical qualification before any parent attempt.
