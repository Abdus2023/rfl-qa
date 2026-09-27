from copy import deepcopy
import subprocess
import sys
import pytest
from tools.common import ROOT, Invalid, load, validate_schema
from tools.validate import all_records, validate_record, validate_dossier
from conftest import rebind


def test_all_positive_records(catalog):
    for path in all_records():
        validate_record(load(path), catalog)


@pytest.mark.parametrize('path,value', [
    (['qualification_id'], 'Q-nope'), (['timestamp'], 'yesterday'),
    (['assessments',0,'claimed_level'], 'L6'), (['evidence',0,'tier'], 'E6'),
    (['invariants',0,'class'], 'UNKNOWN'), (['invariants',0,'epistemic_status'], 'PROVED'),
    (['invariants',0,'epistemic_status'], 'PROOF'), (['hard_gates','status'], 'FAIL'),
    (['scope'], {}), (['scope','competencies'], []), (['scope','domains'], []),
    (['assessments',0,'observations'], []), (['assessments',0,'evidence_refs'], []),
    (['assessments',0,'observations',0,'evidence_refs'], []),
    (['assessments'], []), (['evidence',0,'strength'], 'PASS'),
    (['oracle_results',0,'checks',0,'result'], 'FAIL'),
])
def test_schema_rejects_bad_fields(dossier, path, value):
    target = dossier
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(Invalid):
        validate_schema(dossier, 'claim')


def test_additional_properties_rejected(dossier):
    dossier['automatic_promotion'] = True
    with pytest.raises(Invalid, match='Additional properties'):
        validate_schema(dossier, 'claim')


@pytest.mark.parametrize('target', ['behavior', 'invariant', 'oracle', 'evidence', 'scope', 'hard_coverage'])
def test_dangling_or_incomplete_references(dossier, catalog, target):
    if target == 'behavior': dossier['assessments'][0]['observations'][0]['behavior_id'] = 'CB-999-01'
    if target == 'invariant': dossier['invariants'][0]['id'] = 'MISSING'
    if target == 'oracle': dossier['oracle_results'][0]['oracle_ref'] = 'MISSING'
    if target == 'evidence': dossier['assessments'][0]['observations'][0]['evidence_refs'] = ['MISSING']
    if target == 'scope': dossier['scope']['environments'].append('arm64')
    if target == 'hard_coverage': dossier['oracle_results'][0]['checks'].pop()
    with pytest.raises(Invalid):
        validate_dossier(rebind(dossier), catalog)


def test_distinct_assessors_required(dossier, run):
    dossier['assessments'][1] = deepcopy(dossier['assessments'][0])
    with pytest.raises(Invalid): run(dossier)


def test_duplicate_keys_rejected_json_and_yaml(tmp_path):
    for suffix, text in [('.json','{"id":1,"id":2}'),('.yaml','id: 1\nid: 2\n')]:
        path = tmp_path / ('duplicate' + suffix); path.write_text(text)
        with pytest.raises(Invalid, match='duplicate key'): load(path)


def test_cli_all():
    result = subprocess.run([sys.executable, 'tools/validate.py', '--all'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'PASS' in result.stdout


def test_cli_negative_error_is_specific(tmp_path):
    p = tmp_path / 'bad.json'; p.write_text('{"record_type":"dossier"}')
    result = subprocess.run([sys.executable, str(ROOT/'tools/validate.py'), str(p)], cwd=tmp_path,
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert 'FAIL' in result.stderr and 'required property' in result.stderr


def test_used_evidence_cannot_hide_scope_gap(dossier,run):
    dossier['evidence'][0]['required']=False
    # Leave the primary reference required, but use another purported behavioral artifact.
    dossier['primary_evidence_ref']='TYPE'
    dossier['evidence'][0]['environments']=['arm64']
    with pytest.raises(Invalid, match='claimed environments'):
        run(rebind(dossier))
