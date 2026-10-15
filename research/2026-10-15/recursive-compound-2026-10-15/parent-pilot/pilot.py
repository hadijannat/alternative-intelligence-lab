import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
INPUT = BASE.parent / "parent-inputs"
GIB = 2**30
WALL_SECONDS = 900
RSS_BYTES = 10 * GIB
THREADS = {k: "1" for k in (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stop_owned_group(process):
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)


def monitored_run(command, directory, wall_seconds, rss_bytes):
    directory.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    reason = None
    monitor_error = None
    samples = []
    with (directory / "stdout.txt").open("w") as stdout, (directory / "stderr.txt").open("w") as stderr:
        child = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                 env={**os.environ, **THREADS}, start_new_session=True)
        try:
            while child.poll() is None:
                elapsed = time.monotonic() - start
                if elapsed >= wall_seconds:
                    reason = "WALL_LIMIT"
                    break
                try:
                    observation = subprocess.run(["ps", "-p", str(child.pid), "-o", "rss="],
                                                 capture_output=True, text=True, timeout=3)
                except (subprocess.TimeoutExpired, OSError) as exc:
                    reason = "RSS_MONITOR_UNAVAILABLE"
                    monitor_error = f"{type(exc).__name__}: {exc}"
                    break
                if child.poll() is not None:
                    break
                if observation.returncode or not observation.stdout.strip().isdigit():
                    reason = "RSS_MONITOR_UNAVAILABLE"
                    break
                rss = int(observation.stdout.strip()) * 1024
                samples.append({"elapsed_seconds": elapsed, "rss_bytes": rss})
                if rss > rss_bytes:
                    reason = "RSS_LIMIT"
                    break
                time.sleep(0.2)
        finally:
            stop_owned_group(child)
        returncode = child.wait()
    result = {"argv": command, "pid": child.pid, "returncode": returncode,
              "termination_reason": reason, "monitor_error": monitor_error,
              "wall_seconds": time.monotonic()-start,
              "wall_cap_seconds": wall_seconds, "rss_guard_bytes": rss_bytes,
              "sampled_max_rss_bytes": max((x["rss_bytes"] for x in samples), default=None),
              "samples": samples, "hard_OS_memory_limit": False}
    (directory / "supervisor.json").write_text(json.dumps(result, indent=2)+"\n")
    return result


def worker():
    from collections import Counter
    import inspect
    import types
    import numpy as np
    import pyscf
    from pyscf import dft, gto, solvent
    from pyscf.dft import gen_grid
    from pyscf.scf import hf
    from pyscf.solvent import pcm

    evidence = BASE / "run-v1"
    metadata = json.loads((INPUT / "metadata.json").read_text())
    candidate = next(c for c in metadata["candidates"] if c["id"] == "P0_A")
    xyz = INPUT / "P0_A.xyz"
    assert candidate["checks"]["computational_input_admitted"]
    assert candidate["physical_admission"] is False and candidate["charge"] == -8
    assert sha(xyz) == candidate["xyz_sha256"]
    lines = xyz.read_text().splitlines()
    atoms = [(line.split()[0], tuple(map(float, line.split()[1:]))) for line in lines[2:]]
    assert int(lines[0]) == len(atoms) == 196
    assert Counter(e for e, _ in atoms) == {"Mo": 36, "O": 128, "H": 32}
    mapping_path = BASE.parent / "identity/site_mapping.json"
    mapping = json.loads(mapping_path.read_text())
    assert atoms[:164] == [(s["element"], tuple(s["cartesian_A"])) for s in mapping]
    start = time.monotonic()
    mol = gto.M(atom=atoms, unit="Angstrom", basis="def2-svp", ecp={"Mo": "def2-svp"},
                charge=-8, spin=0, verbose=4, max_memory=8000,
                output=str(evidence / "native.log"))
    assert mol.nao_nr() == 3068 and mol.nelectron == 1568
    assert sum(mol.atom_charges())-mol.nelectron == -8
    surface = pcm.gen_surface(mol, ng=gen_grid.LEBEDEV_ORDER[17],
                              rad=1.2*pcm.modified_Bondi, surface_discretization_method="SWIG")
    n = len(surface["grid_coords"])
    estimate = 20*8*n*n + 2*GIB
    preflight = {"input_id": "P0_A", "input_sha256": sha(xyz),
                 "metadata_sha256": sha(INPUT / "metadata.json"), "mapping_sha256": sha(mapping_path),
                 "pilot_sha256": sha(Path(__file__)), "protocol_sha256": sha(BASE / "PROTOCOL.md"),
                 "pyscf": pyscf.__version__, "PCM_source_sha256": sha(Path(inspect.getsourcefile(pcm))),
                 "atoms": mol.natm, "AOs": mol.nao_nr(), "explicit_electrons": mol.nelectron,
                 "charge": -8, "spin_2S_trial": 0, "surface_points": n,
                 "one_surface_matrix_bytes": 8*n*n, "screening_estimate_bytes": estimate,
                 "screening_limit_bytes": RSS_BYTES, "screening_is_measured_peak": False,
                 "preflight_elapsed_seconds": time.monotonic()-start,
                 "physical_admission": False, "parent_input_hypothetical": True}
    (evidence / "preflight.json").write_text(json.dumps(preflight, indent=2)+"\n")
    print(json.dumps(preflight), flush=True)
    if estimate > RSS_BYTES:
        print("RESOURCE_PREFLIGHT_REJECTED; no SCF launched", flush=True)
        return 2
    del surface
    mf = dft.RKS(mol)
    mf.xc = "PBE"
    mf.grids.level = 2
    mf.conv_tol, mf.conv_tol_grad, mf.max_cycle = 1e-11, 1e-7, 20
    mf.direct_scf, mf.chkfile = True, None
    mf = solvent.PCM(mf)
    mf.with_solvent.method, mf.with_solvent.eps = "C-PCM", 78.4
    mf.with_solvent.lebedev_order, mf.with_solvent.vdw_scale = 17, 1.2
    mf.with_solvent.r_probe, mf.with_solvent.frozen = 0.0, False
    mf.get_jk = types.MethodType(hf.SCF.get_jk, mf)

    def record_cycle(env):
        row = {"cycle": int(env["cycle"])+1, "elapsed_seconds": time.monotonic()-start,
               "energy_Eh_unqualified": float(env["e_tot"]),
               "orbital_gradient_norm": float(env["norm_gorb"])}
        with (evidence / "iterations.jsonl").open("a") as stream:
            stream.write(json.dumps(row)+"\n")
        print(json.dumps(row), flush=True)

    mf.callback = record_cycle
    energy = float(mf.kernel())
    dm = mf.make_rdm1()
    gradient = float(np.linalg.norm(mf.get_grad(mf.mo_coeff, mf.mo_occ, mf.get_fock(dm=dm))))
    electrons = float(np.einsum("ij,ji", dm, mf.get_ovlp()))
    passes = bool(mf.converged and math.isfinite(energy) and gradient < 1e-5
                  and abs(electrons-1568) < 1e-6 and mf._eri is None)
    result = {"numerical_SCF_pass": passes, "converged": bool(mf.converged), "cycles": mf.cycles,
              "energy_Eh": energy, "orbital_gradient_norm": gradient, "electron_trace": electrons,
              "cached_four_center_ERI": mf._eri is not None, "elapsed_seconds": time.monotonic()-start,
              "orbital_stability_checked": False, "geometry_optimized": False,
              "relative_chemistry_comparison_performed": False, "physical_admission": False,
              "goal_verified": False}
    (evidence / "SCF-result.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result), flush=True)
    mol.stdout.close()
    return 0 if passes else 3


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        sys.exit(worker())
    destination = BASE / "run-v1"
    if destination.exists():
        raise SystemExit("run-v1 already exists; preserve it and do not restart automatically")
    interpreter = ROOT / "discovery-loop/experiments/borazine-water-endpoint-electronic-v1/.venv/bin/python"
    result = monitored_run([str(interpreter), "-B", str(Path(__file__).resolve()), "--worker"],
                           destination, WALL_SECONDS, RSS_BYTES)
    print(json.dumps({k: v for k, v in result.items() if k != "samples"}, indent=2))
    sys.exit(0 if result["returncode"] == 0 and result["termination_reason"] is None else 1)
