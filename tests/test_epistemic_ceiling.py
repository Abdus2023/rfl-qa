from copy import deepcopy
import pytest
from tools.common import EPISTEMIC, canonical
from tools.report import report
from conftest import rebind


@pytest.mark.parametrize('status', EPISTEMIC)
def test_weakest_required_invariant_wins(dossier, run, status):
    for e in dossier['evidence']:
        if e['required']: e['epistemic_status']='VERIFIED'
    for inv in dossier['invariants']: inv['epistemic_status']='VERIFIED'
    dossier['invariants'][1]['epistemic_status']=status
    for a in dossier['assessments']:
        for f in a['invariant_findings']: f['epistemic_status']='VERIFIED'
        a['invariant_findings'][1]['epistemic_status']=status
    out=run(rebind(dossier))
    assert out['decision']['epistemic_ceiling']==status
    assert (out['decision']['status']=='VERIFIED_WITHIN_SCOPE') == (status=='VERIFIED')


def test_counts_tiers_time_and_report_never_upgrade(dossier, run):
    baseline=run(dossier)
    dossier['timestamp']='2027-09-27T00:00:00Z'
    for e in dossier['evidence']:
        if e['required']: e['coverage']['executed']=10**9
        e['tier']='E5'
    for a in dossier['assessments']: a['evidence_tier']='E5'
    out=run(rebind(dossier))
    assert out['decision']['epistemic_ceiling']==baseline['decision']['epistemic_ceiling']=='PARTIALLY_VERIFIED'
    before=canonical(out)
    text=report(out)
    assert canonical(out)==before
    assert 'PARTIALLY_VERIFIED' in text
    assert out['decision']['status']=='PROVISIONAL'


def test_excluded_nmi_absence_not_required(dossier, run):
    out=run(dossier)
    assert out['decision']['epistemic_ceiling']=='PARTIALLY_VERIFIED' # not OPEN from excluded NMI
    assert out['scope']==out['decision']['scope']==dossier['scope']


def test_not_run_oracle_prevents_verified(dossier, run):
    for e in dossier['evidence']:
        if e['required']: e['epistemic_status']='VERIFIED'
    for inv in dossier['invariants']: inv['epistemic_status']='VERIFIED'
    for a in dossier['assessments']:
        for f in a['invariant_findings']: f['epistemic_status']='VERIFIED'
    dossier['oracle_results'][0]['checks'][0]['result']='NOT_RUN'
    assert run(rebind(dossier))['decision']['status']=='PROVISIONAL'
