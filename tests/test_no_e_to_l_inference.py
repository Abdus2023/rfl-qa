from copy import deepcopy
import pytest
from conftest import poison, rebind


def test_poisoned_e4_claim_is_capped(run):
    result = run(poison('e4_does_not_imply_l4'))
    assert result['capability']['level'] == 'L2'
    assert result['evidence_tier'] == 'E4'
    assert result['capability']['level_boundary']['L4_satisfied'] is False


@pytest.mark.parametrize('tier', ['E0','E1','E2','E3','E4','E5'])
def test_changing_only_evidence_tier_cannot_change_capability(run, tier):
    d = poison('e4_does_not_imply_l4')
    for e in d['evidence']: e['tier'] = tier
    for a in d['assessments']: a['evidence_tier'] = tier
    # Remove VERIFIED external assertion for E0; external evidence quality is a separate rule.
    if tier == 'E0':
        d['invariants'][-1]['epistemic_status'] = 'OPEN'
        d['invariants'][-1]['external_evidence'] = []
        for a in d['assessments']: a['invariant_findings'][-1]['epistemic_status'] = 'OPEN'
    result = run(rebind(d))
    assert result['capability']['level'] == 'L2'
    if tier == 'E0': assert result['decision']['status'] == 'REJECTED'


def test_failed_required_behavior_caps_level(dossier, run):
    for a in dossier['assessments']:
        a['observations'][1]['status'] = 'FAILED'
    out = run(dossier)
    assert out['capability']['level'] == 'L1'
    assert out['capability']['failed_behaviors'] == ['CB-047-02']


def test_higher_behavior_without_prerequisites_never_promotes(dossier, run):
    for a in dossier['assessments']:
        a['observations'] = [{'behavior_id':'CB-047-05','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']}]
    assert run(dossier)['capability']['level'] == 'L0'
