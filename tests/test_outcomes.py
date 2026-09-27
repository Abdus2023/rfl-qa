import pytest
from tools.common import ROOT, Invalid, load
from tools.validate import validate_record


@pytest.mark.parametrize('classification', ['VALIDATED_WITHIN_SCOPE','SCOPE_EXCEEDED','ASSESSMENT_ERROR','ORACLE_FAILURE','SPECIFICATION_FAILURE','EXTERNAL_FAILURE','INCONCLUSIVE'])
def test_explicit_outcome_classification_preserved(classification):
    record=load(ROOT/'calibration/cases/CAL-001.yaml')
    record['classification']=classification
    validate_record(record)
    assert record['classification']==classification
    assert record['revision_required'] is False


def test_external_failure_not_automatic_spec_failure():
    record=load(ROOT/'calibration/cases/CAL-001.yaml')
    record['classification']='EXTERNAL_FAILURE'; record['revision_required']=True
    with pytest.raises(Invalid): validate_record(record)
