import pytest
from tools.common import Invalid
from conftest import poison, rebind


def test_verified_d_without_external_evidence_rejected(run):
    with pytest.raises(Invalid, match='external_evidence'):
        run(poison('type_d_verified_without_external_evidence'))


@pytest.mark.parametrize('change', ['missing_ref', 'wrong_method', 'empty_description', 'unknown_assessor'])
def test_external_evidence_is_not_arbitrary_field(dossier, run, change):
    ext = dossier['invariants'][-1]['external_evidence'][0]
    if change == 'missing_ref': ext['ref'] = 'NOPE'
    if change == 'wrong_method': ext['ref'] = 'TEST'
    if change == 'empty_description': ext['description'] = ''
    if change == 'unknown_assessor': ext['assessor'] = 'NOPE'
    with pytest.raises(Invalid): run(rebind(dossier))


def test_supported_d_verified_is_valid(dossier, run):
    out = run(dossier)
    assert out['invariants'][-1]['class'] == 'D'
    assert out['invariants'][-1]['epistemic_status'] == 'VERIFIED'
