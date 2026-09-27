from copy import deepcopy
import pytest
from tools.common import ROOT, Invalid, canonical, load
from conftest import poison


def test_separate_assessment_fixtures_agree(dossier,run):
    dossier['assessments']=[load(ROOT/f'tests/fixtures/calibration/lab003_assessor_{x}.yaml') for x in ('a','b')]
    original=deepcopy(dossier['assessments'])
    out=run(dossier)
    assert out['inter_rater']['agreement'] is True
    assert out['assessments']==original
    assert out['capability']['level']=='L3'


def test_disagreement_logged_without_average(run):
    d=poison('inter_rater_disagreement'); before=canonical(d)
    out=run(d)
    assert out['assessments']==d['assessments']
    assert canonical(d)==before
    assert out['inter_rater']['automatic_qualification_halted'] is True
    assert out['capability'] is None
    assert out['derived_signature']=='AWAITING_ADJUDICATION'
    assert out['inter_rater']['events'][0]['adjudication_status']=='OPEN'
    assert out['inter_rater']['events'][0]['classification']!='specification_defect'


@pytest.mark.parametrize('axis', ['evidence','invariant','epistemic','behaviors'])
def test_all_finding_disagreements_halt(dossier,run,axis):
    a=dossier['assessments'][1]
    if axis=='evidence': a['evidence_tier']='E3'
    if axis=='invariant': a['invariant_findings'][0]['class']='B'
    if axis=='epistemic': a['invariant_findings'][0]['epistemic_status']='PROVISIONAL'
    if axis=='behaviors': a['observations'][0]['status']='FAILED'
    out=run(dossier)
    assert out['inter_rater']['automatic_qualification_halted'] is True
    assert out['decision']['status']!='VERIFIED_WITHIN_SCOPE'


def test_assessors_must_bind_same_raw_dossier(dossier,run):
    dossier['assessments'][1]['dossier_digest']='0'*64
    with pytest.raises(Invalid, match='exact raw dossier'): run(dossier)
