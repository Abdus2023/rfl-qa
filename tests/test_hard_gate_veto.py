import pytest
from tools.common import GATES
from conftest import poison, rebind


@pytest.mark.parametrize('fixture', ['injected_uaf','injected_race','critical_assumption_open'])
def test_required_injections_veto(run, fixture):
    out = run(poison(fixture))
    assert out['hard_gates']['status'] == 'BLOCKED'
    assert out['decision']['status'] == 'REJECTED'
    assert out['derived_signature'] == 'BLOCKED'


@pytest.mark.parametrize('gate', GATES)
def test_every_hard_gate_is_noncompensable(dossier, run, gate):
    dossier['hard_gates'] = {'status':'BLOCKED','findings':[gate]}
    for a in dossier['assessments']:
        a['hard_gates'] = {'status':'BLOCKED','findings':[gate]}
        a['observations'] = [{'behavior_id':f'CB-047-{i:02}','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']} for i in range(1,6)]
        a['claimed_level']='L5'; a['evidence_tier']='E5'
    for e in dossier['evidence']: e['tier']='E5'
    out=run(rebind(dossier))
    assert out['capability']['level']=='L5'
    assert out['decision']['status']=='REJECTED'
    assert out['derived_signature']=='BLOCKED'


def test_one_assessor_veto_survives_disagreement(dossier, run):
    dossier['assessments'][1]['hard_gates']={'status':'BLOCKED','findings':['uaf']}
    out=run(dossier)
    assert out['inter_rater']['agreement'] is False
    assert out['decision']['status']=='REJECTED'


def test_oracle_violation_veto(dossier, run):
    dossier['oracle_results'][0]['checks'][0]['result']='BLOCKED'
    assert run(rebind(dossier))['derived_signature']=='BLOCKED'
