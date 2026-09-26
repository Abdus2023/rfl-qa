from copy import deepcopy
import pytest
from tools.common import ROOT, Invalid, load, validate_schema
from tools.validate import check_oracle, validate_record


def test_three_labs_have_matching_executable_oracles(catalog):
    _, invariants, oracles=catalog
    labs=list((ROOT/'labs').iterdir())
    assert len(labs)==3
    for lab in labs:
        oracle=load(lab/'oracle.yaml')
        assert oracle==oracles[oracle['id']]
        check_oracle(oracle,invariants)
        validate_record(load(lab/'task.yaml'),catalog)
        validate_record(load(lab/'expected-observations.yaml'),catalog)
        for c in oracle['checks']:
            assert c['input'] and c['expected_condition'] and c['failure_condition']


def test_missing_oracle_failure_condition_rejected(catalog):
    oracle=deepcopy(catalog[2]['OR-CALLBACK'])
    del oracle['checks'][0]['failure_condition']
    with pytest.raises(Invalid): validate_schema(oracle,'oracle')


def test_callback_teardown_all_interleavings_and_states(catalog):
    o=catalog[2]['OR-CALLBACK']
    assert o['teardown_model']==['CREATE','REGISTER','ACTIVE','STOP','QUIESCE','CALLBACK DRAIN','REFERENCE DRAIN','DESTROY','FREE']
    inputs=' '.join(c['input'] for c in o['checks'])
    for race in ['callback vs unregister','callback vs free','ioctl vs remove','reference release vs free','RCU reader vs destroy']:
        assert race in inputs


def test_oracle_missing_gate_coverage_rejected(catalog):
    o=deepcopy(catalog[2]['OR-CALLBACK']); o['checks'].pop(0)
    with pytest.raises(Invalid, match='coverage'): check_oracle(o,catalog[1])
