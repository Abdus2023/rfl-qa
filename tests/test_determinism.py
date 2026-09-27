from copy import deepcopy
import subprocess
import sys
import pytest
from tools.common import ROOT, Invalid, canonical, digest
from tools.report import report
from conftest import rebind


def test_one_hundred_identical_derivations(dossier,run):
    original=deepcopy(dossier)
    results=[canonical(run(dossier)) for _ in range(100)]
    assert len(set(results))==1
    assert dossier==original


def test_hash_covers_entire_record_except_hash(dossier,run):
    out=run(dossier)
    assert digest({k:v for k,v in out.items() if k!='assessment_hash'})==out['assessment_hash']
    changed=deepcopy(out); changed['decision']['epistemic_ceiling']='VERIFIED'
    with pytest.raises(Invalid, match='hash mismatch'): report(changed)


def test_change_in_input_changes_hash(dossier,run):
    original=run(dossier)
    dossier['limitations'].append('Additional explicit exclusion notice.')
    assert run(rebind(dossier))['assessment_hash']!=original['assessment_hash']


def test_scope_not_extrapolated(dossier,run):
    out=run(dossier)
    assert out['scope']==out['decision']['scope']==dossier['scope']
    assert 'arm64' in out['scope']['exclusions']
    assert 'arm64' not in out['scope']['environments']


def test_complete_cli_pipeline_repeatable(tmp_path):
    command=[sys.executable,str(ROOT/'tools/derive.py'),str(ROOT/'dossiers/examples/003-callback-teardown.json')]
    outputs=[subprocess.run(command,cwd=tmp_path,capture_output=True,check=True).stdout for _ in range(2)]
    assert outputs[0]==outputs[1]
    p=tmp_path/'qualification.json'; p.write_bytes(outputs[0])
    result=subprocess.run([sys.executable,str(ROOT/'tools/report.py'),str(p)],cwd=tmp_path,capture_output=True)
    assert result.returncode==0
    assert b'PARTIALLY_VERIFIED' in result.stdout
