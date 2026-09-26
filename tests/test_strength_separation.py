import pytest
from tools.common import EPISTEMIC, Invalid, validate_schema
from tools.validate import check_evidence
from conftest import poison, rebind


def test_sanitizer_is_not_proof(run):
    with pytest.raises(Invalid, match='cannot establish PROOF'):
        run(poison('kcsan_as_proof'))


@pytest.mark.parametrize('cls',list('ABCD'))
@pytest.mark.parametrize('status',EPISTEMIC)
def test_schema_axes_independent(dossier, cls, status):
    inv=dossier['invariants'][0]
    inv['class']=cls; inv['epistemic_status']=status
    validate_schema(inv,'invariant') # evidence consistency is a separate semantic check


@pytest.mark.parametrize('strength,meaning,method', [
    ('PROOF','ASSUMPTION_BOUND_PROOF','rustc'),
    ('OBSERVATION','BOUNDED_OBSERVATION','kcsan'),
    ('COVERAGE','MEASURED_COVERAGE','scheduler'),
    ('ABSENCE_OF_EVIDENCE','NOT_TESTED','not_tested')])
def test_strength_is_distinct_from_status(dossier,strength,meaning,method):
    e=dossier['evidence'][0]
    e.update(strength=strength, establishes=meaning, method=method,
             epistemic_status='PROVISIONAL', assumptions=['Sound API'])
    if strength=='ABSENCE_OF_EVIDENCE': e['coverage']['executed']=0
    check_evidence(e)


def test_establishes_contradiction_rejected(dossier):
    e=dossier['evidence'][2]; e['establishes']='ASSUMPTION_BOUND_PROOF'
    with pytest.raises(Invalid, match='mismatch'): check_evidence(e)


def test_type_b_provisional_not_external(dossier,run):
    dossier['invariants'][1]['epistemic_status']='PROVISIONAL'
    for a in dossier['assessments']: a['invariant_findings'][1]['epistemic_status']='PROVISIONAL'
    out=run(rebind(dossier))
    assert out['invariants'][1]['class']=='B'
    assert out['decision']['epistemic_ceiling']=='PROVISIONAL'
