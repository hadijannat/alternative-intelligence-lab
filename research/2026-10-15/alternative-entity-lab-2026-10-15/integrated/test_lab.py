from dataclasses import asdict
import json
from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from lab import decide, history, initialise, load_config, observed_feedback, renew_labels, retrieve, run_case, split_state, update_labels


def config():
    return load_config(Path(__file__).with_name("config.json"))


def test_split_conserves_every_extensive_ledger():
    state = initialise(7,19,11)
    left,right = split_state(state,0.37)
    for key,value in asdict(state).items():
        assert asdict(left)[key]+asdict(right)[key] == pytest.approx(value)


def test_memory_has_no_delay_loss_and_eventual_random_fallback():
    assert retrieve(1,0,0.08,0.999,0) == 1
    assert retrieve(1,1e6,0.08,0.01,0) == 0
    assert decide(np.array([20,0]),1,0) == 1
    assert decide(np.array([0,20]),1,0) == 0


def test_switching_requires_actual_paid_energy():
    counts,state,n = update_labels(np.array([20,0]),1,0.25,initialise(0,20,0.03),0.02)
    assert n == 1 and counts.tolist() == [19,1]
    assert state.energy == pytest.approx(0.01)
    counts,state,n = update_labels(counts,1,1,state,0.02)
    assert n == 0 and counts.tolist() == [19,1]


def test_renewal_never_exceeds_actual_carrier_material():
    rng = np.random.default_rng(13)
    for structure in (0,0.9,1,2.2,40,80):
        out = renew_labels(np.array([20,20]),min(20,structure),structure,0.01,rng)
        assert int(out.sum()) == int(structure) and np.all(out >= 0)


def test_no_renewal_cannot_create_new_carrier_types():
    rng = np.random.default_rng(8)
    out = renew_labels(np.array([40,0]),39.60199335,39.60199335,0.5,rng)
    assert out.tolist() == [39,0]


def test_empty_or_capped_resource_cannot_reveal_hidden_correctness():
    c = config()
    assert observed_feedback(0,0,1,c) is None
    assert observed_feedback(0.2,0.2,1,c) is None
    assert observed_feedback(7.5,100,1,c) is True
    assert observed_feedback(0.45,100,1,c) is False
    c["episodes"] = 40
    c["feed_stock"] = 0
    result,rows = run_case(c,2026101560,"primary","adaptive")
    assert result["consumed_feed"] == 0
    assert all(r["switches"] == 0 for r in rows)


def test_histories_replay_and_no_feed_is_finite():
    c = config()
    c["episodes"] = 40
    env = history(c,11)
    assert all(np.array_equal(v,history(c,11)[k]) for k,v in env.items())
    result,rows = run_case(c,11,"primary","no_feed",env)
    assert result["consumed_feed"] == 0
    assert result["max_balance_error"] < 1e-8
    assert all(r["feed"] == 0 for r in rows)


def test_invalid_config_rejected(tmp_path):
    c = config()
    c["switch_cost"] = 0
    path = tmp_path/"bad.json"
    path.write_text(json.dumps(c))
    with pytest.raises(ValueError,match="switch cost"):
        load_config(path)
    c = config()
    c["episodes"] = c["adaptation_allowance"]
    path.write_text(json.dumps(c))
    with pytest.raises(ValueError,match="evaluation episode"):
        load_config(path)
