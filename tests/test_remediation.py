"""Frozen audit counterexamples plus current-schema semantic regressions (HG-01..07)."""
from copy import deepcopy
import json
import pytest
from conftest import rebind
from tools.common import ROOT, Invalid, EPISTEMIC, GATES, canonical, digest, load, catalogs
from tools.derive import derive
from tools.oracle import evaluate_teardown, STATES, supporting_refs
from tools.validate import check_evidence, validate_record
from tools.report import report

AUDIT = ROOT/'evidence/adversarial-audit/counterexamples'


def verified(d):
    d=deepcopy(d)
    for e in d['evidence']:
        if e['required']: e['epistemic_status']='VERIFIED'
    for i in d['invariants']: i['epistemic_status']='VERIFIED'
    for a in d['assessments']:
        for i in a['invariant_findings']: i['epistemic_status']='VERIFIED'
    return rebind(d)


def current_provenance(old, template):
    """Add template observations/bindings to a COPY, retaining old fields.

    This does not authenticate or transcribe narrative facts; safe template facts
    may contradict the old prose. That limitation is explicitly replayed/reported."""
    d=deepcopy(old)
    d['oracle_observations']=deepcopy(template['oracle_observations'])
    for e, t in zip(d['evidence'], template['evidence']):
        e['oracle_check_refs']=deepcopy(t['oracle_check_refs']);e['invariant_refs']=deepcopy(t['invariant_refs'])
    for r,tr in zip(d['oracle_results'],template['oracle_results']):
        for c,tc in zip(r['checks'],tr['checks']):
            c['provenance']=tc['provenance'];c['observation_ref']=tc['observation_ref']
    return rebind(d)


@pytest.mark.parametrize('name', [
 'critical-open-declared-noncritical','critical-verified-with-open-support',
 'not-tested-as-observation','scope-erased-x86_64','scope-erased-PREEMPT_RT-y','scope-erased-CONFIG_RUST-y'])
def test_original_bypass_with_current_provenance_rejects(name,dossier,run):
    old=load(AUDIT/(name+'.json'))
    with pytest.raises(Invalid):run(current_provenance(old,dossier))


@pytest.mark.parametrize('name', [p.name for p in AUDIT.glob('*.json') if not p.name.endswith('.result.json') and not p.name.endswith('.catalog.json')])
def test_frozen_legacy_counterexamples_never_silently_upgraded(name,run):
    old=load(AUDIT/name)
    with pytest.raises(Invalid):
        if old['record_type']=='qualification':report(old)
        else:run(old)


def test_hg01_catalog_criticality_control(dossier,run,catalog):
    assert run(dossier)['invariants'][-1]['critical'] is True
    d=deepcopy(dossier);d['invariants'][-1]['critical']=False
    with pytest.raises(Invalid,match='criticality'):run(rebind(d))
    d=deepcopy(dossier);d['invariants'][0]['critical']=True
    with pytest.raises(Invalid,match='criticality'):run(rebind(d))
    c,i,o=deepcopy(catalog);del i['D01']
    with pytest.raises(Invalid):derive(dossier,c['C047'],i,o)


def test_hg01_assessor_cannot_downgrade(dossier,run):
    dossier['invariants'][-1]['epistemic_status']='OPEN'
    for a in dossier['assessments']:
        a['invariant_findings'][-1].update({'class':'B','epistemic_status':'VERIFIED'})
    result=run(rebind(dossier))
    assert result['hard_gates']['status']=='BLOCKED'
    assert result['decision']['status']=='REJECTED'


@pytest.mark.parametrize('kind', ['missing-env','missing-task','unsupported-env','removed-exclusion','conflicting-exclusion','duplicate'])
def test_hg02_scope_rejects(dossier,run,kind):
    scope=dossier['scope']
    if kind=='missing-env':scope['environments'].remove('PREEMPT_RT=y')
    if kind=='missing-task':scope['task_classes'].pop()
    if kind=='unsupported-env':scope['environments'].append('arm64')
    if kind=='removed-exclusion':scope['exclusions'].remove('arm64')
    if kind=='conflicting-exclusion':scope['exclusions'].append('x86_64')
    if kind=='duplicate':scope['environments'].append(scope['environments'][0])
    with pytest.raises(Invalid):run(rebind(dossier))


def test_hg02_exact_and_permuted_scope_accepted(dossier,run):
    baseline=run(dossier)
    for v in dossier['scope'].values():v.reverse()
    result=run(rebind(dossier))
    assert result['decision']['status']==baseline['decision']['status']
    assert result['scope']==dossier['scope']


@pytest.mark.parametrize('status',EPISTEMIC)
def test_hg03_hg05_required_oracle_closure(status,dossier,run):
    d=verified(dossier);d['invariants'][2]['evidence_refs']=['ARTIFACT']
    e=next(e for e in d['evidence'] if e['id']=='TEST');e['required']=False;e['epistemic_status']=status
    out=run(rebind(d))
    assert 'TEST' in supporting_refs(d)
    assert out['decision']['epistemic_ceiling']==status
    assert (out['decision']['status']=='VERIFIED_WITHIN_SCOPE')==(status=='VERIFIED')


def test_hg03_original_counterexample_now_nonverified(dossier,run):
    old=load(AUDIT/'oracle-open-evidence-not-in-ceiling.json')
    out=run(current_provenance(old,dossier))
    assert out['decision']['epistemic_ceiling']=='OPEN'
    assert out['decision']['status']!='VERIFIED_WITHIN_SCOPE'


METHODS=['not_tested','kasan','kcsan','lockdep','kunit','scheduler','rustc','formal','source_audit','manual_review']
STRENGTHS=['PROOF','OBSERVATION','COVERAGE','ABSENCE_OF_EVIDENCE']
@pytest.mark.parametrize('method',METHODS)
@pytest.mark.parametrize('strength',STRENGTHS)
def test_hg04_method_strength_crossproduct(dossier,method,strength):
    e=dossier['evidence'][0];e['method']=method;e['strength']=strength
    e['establishes']=dict(zip(STRENGTHS,['ASSUMPTION_BOUND_PROOF','BOUNDED_OBSERVATION','MEASURED_COVERAGE','NOT_TESTED']))[strength]
    e['epistemic_status']='PROVISIONAL';e['assumptions']=['Sound compiler/API model'];e['coverage']['executed']=0 if strength=='ABSENCE_OF_EVIDENCE' else 1
    allowed=(strength=='ABSENCE_OF_EVIDENCE' if method=='not_tested' else
             strength in (['PROOF','OBSERVATION','COVERAGE'] if method in ('rustc','formal') else ['OBSERVATION','COVERAGE']))
    if allowed:check_evidence(e)
    else:
        with pytest.raises(Invalid):check_evidence(e)


def test_hg04_absence_never_behavioral_credit(dossier,run):
    for a in dossier['assessments']:
        for o in a['observations']:o['evidence_refs']=['NMI']
    out=run(dossier)
    assert out['capability']['level']=='L0'
    assert out['decision']['status']!='VERIFIED_WITHIN_SCOPE'


# Every canonical oracle check is attacked, including classification and exclusion-awareness checks.
CHECKS=[(p.name,c['check_id']) for p in sorted((ROOT/'dossiers/examples').glob('*.json'))
        for r in load(p)['oracle_results'] for c in r['checks']]
@pytest.mark.parametrize('filename,check_id',CHECKS)
@pytest.mark.parametrize('attack',['remove','unrelated','open','absence','strength','blocked'])
def test_hg05_each_check_material_evidence(filename,check_id,attack,run):
    d=load(ROOT/'dossiers/examples'/filename)
    check=next(c for r in d['oracle_results'] for c in r['checks'] if c['check_id']==check_id)
    obs=next(o for o in d['oracle_observations'] if o['id']==check['observation_ref'])
    e=next(e for e in d['evidence'] if e['id']==check['evidence_refs'][0])
    if attack=='remove':check['evidence_refs']=[]
    if attack=='unrelated':
        new=deepcopy(e);new['id']='UNRELATED';new['oracle_check_refs']=[];d['evidence'].append(new)
        check['evidence_refs']=['UNRELATED'];obs['evidence_refs']=['UNRELATED']
    if attack=='open':e['epistemic_status']='OPEN'
    if attack=='blocked':e['epistemic_status']='BLOCKED'
    if attack=='absence':
        e.update(method='not_tested',strength='ABSENCE_OF_EVIDENCE',establishes='NOT_TESTED',epistemic_status='OPEN')
        e['coverage']['executed']=0
    if attack=='strength':
        if e['strength']=='PROOF':e['strength']='OBSERVATION';e['establishes']='BOUNDED_OBSERVATION'
        else:e['strength']='PROOF';e['establishes']='ASSUMPTION_BOUND_PROOF'
        e['assumptions']=['test']
    try:out=run(rebind(d))
    except Invalid:return
    assert out['decision']['status']!='VERIFIED_WITHIN_SCOPE'
    if attack in ('remove','unrelated','strength'):pytest.fail('malformed or unrelated observation accepted')


def test_hg06_positive_derived_pass(dossier,run):
    out=run(verified(dossier))
    assert out['decision']['status']=='VERIFIED_WITHIN_SCOPE'
    for r in out['oracle_evaluations']:
        assert r['provenance']=='DERIVED_RESULT' and r['result']=='PASS'
        assert all(len(r[k])==64 for k in ['input_hash','observation_hash','oracle_hash','evidence_hash'])


@pytest.mark.parametrize('attack',['no_observation','unrelated','failure','not_run','forged_provenance'])
def test_hg06_asserted_pass_is_not_execution(dossier,run,attack):
    d=verified(dossier);c=d['oracle_results'][0]['checks'][0];o=d['oracle_observations'][0]
    if attack=='no_observation':d['oracle_observations'].pop(0)
    if attack=='unrelated':o['input_ref']='NMI'
    if attack=='failure':o['payload']['trace'][-1]['callback_possible']=True
    if attack=='not_run':o['executed']=False
    if attack=='forged_provenance':c['provenance']='DERIVED_RESULT'
    try:out=run(rebind(d))
    except Invalid:return
    assert attack in ('failure','not_run')
    assert out['decision']['status']!='VERIFIED_WITHIN_SCOPE'


TRACE_ATTACKS=['callback_after_free','reference_after_free','free_before_callback_drain','free_before_reference_drain',
               'registered_owner','incomplete','impossible_transition','duplicate','reordered','empty']
def poison_trace(t,attack):
    t=deepcopy(t)
    if attack=='callback_after_free':t[-1]['callback_possible']=True
    if attack=='reference_after_free':t[-1]['live_references']=1
    if attack=='registered_owner':t[-1]['registered_owner']=True
    if attack=='free_before_callback_drain':t[5]['state']='FREE';t[5]['callback_possible']=True;t[5]['object_alive']=False
    if attack=='free_before_reference_drain':t[6]['state']='FREE';t[6]['live_references']=1;t[6]['object_alive']=False
    if attack=='incomplete':t.pop()
    if attack=='impossible_transition':t[1]['state']='DESTROY'
    if attack=='duplicate':t[2]=deepcopy(t[1])
    if attack=='reordered':t[3],t[4]=t[4],t[3]
    if attack=='empty':t=[]
    return t


@pytest.mark.parametrize('attack',TRACE_ATTACKS)
def test_hg07_adversarial_trace_has_explicit_blocked_oracle(dossier,run,attack):
    d=verified(dossier);t=d['oracle_observations'][0]['payload']['trace']
    assert evaluate_teardown(t)=={'result':'PASS','findings':[]}
    bad=poison_trace(t,attack)
    assert evaluate_teardown(bad)['result']=='BLOCKED'
    d['oracle_observations'][0]['payload']['trace']=bad
    out=run(rebind(d))
    assert out['decision']['status']=='REJECTED' and out['derived_signature']=='BLOCKED'


def test_hg07_submitted_label_does_not_control_evaluator(dossier,run):
    d=verified(dossier)
    d['oracle_observations'][0]['payload']['trace'][-1]['rcu_readers']=1
    outputs=[]
    for label in ['PASS','BLOCKED']:
        d['oracle_results'][0]['checks'][0]['result']=label
        out=run(rebind(d));outputs.append(out['oracle_evaluations'])
        assert out['hard_gates']['status']=='BLOCKED'
    assert outputs[0]==outputs[1]


@pytest.mark.parametrize('tier,n',[('E5',0),('E4',1),('E4',2),('E3',2),('E2',3),('E1',4),('E0',5)]+[(f'E{e}',n) for e in range(6) for n in range(6)])
def test_preserved_tier_level_boundary(dossier,run,tier,n):
    dossier['evidence'][0]['tier']=tier
    for a in dossier['assessments']:
        a['evidence_tier']=tier;a['claimed_level']=f'L{n}'
        a['observations']=[{'behavior_id':f'CB-047-{i:02}','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']} for i in range(1,n+1)] or [{'behavior_id':'CB-047-01','status':'FAILED','evidence_refs':['ARTIFACT']}]
    out=run(rebind(dossier));assert out['capability']['level']==f'L{n}'


@pytest.mark.parametrize('idx',range(4))
@pytest.mark.parametrize('status',['VERIFIED','OPEN'])
def test_preserved_class_status_independence(dossier,run,idx,status):
    d=verified(dossier);d['invariants'][idx]['epistemic_status']=status
    for a in d['assessments']:a['invariant_findings'][idx]['epistemic_status']=status
    out=run(rebind(d))
    assert out['invariants'][idx]['class']=='ABCD'[idx]
    assert out['decision']['epistemic_ceiling']==status


def test_aud009_contradictory_rehashed_report_rejected(dossier,run):
    out=run(dossier);before=canonical(out);report(out);assert canonical(out)==before
    out['decision']['status']='VERIFIED_WITHIN_SCOPE';out['decision']['epistemic_ceiling']='VERIFIED'
    out['assessment_hash']=digest({k:v for k,v in out.items() if k!='assessment_hash'})
    with pytest.raises(Invalid,match='derivation'):report(out)


def test_aud010_standalone_invariant_rules():
    with pytest.raises(Invalid):validate_record(load(AUDIT/'standalone-d-verified-no-evidence.yaml'))


@pytest.mark.parametrize('ext,text',[('json','['*1500+'0'+']'*1500),('yaml','['*1500+'0'+']'*1500),
                                  ('json','{"x":NaN}'),('yaml','x: .nan'),('json','{"x":1.0}'),('yaml','x: 1.0'),
                                  ('json','{"x":1,"x":2}'),('yaml','x: 1\nx: 2'),('yaml','!!python/object/apply:builtins.str [x]')])
def test_aud011_bounded_strict_parser(tmp_path,ext,text):
    p=tmp_path/f'bad.{ext}';p.write_text(text)
    with pytest.raises(Invalid):load(p)


def test_original_bad_model_rejected(dossier,run,catalog):
    c,i,o=deepcopy(catalog);o['OR-CALLBACK']=load(AUDIT/'oracle-invalid-state-model.catalog.json')
    with pytest.raises(Invalid,match='teardown'):derive(dossier,c['C047'],i,o)


def test_hg03_assessor_support_in_closure(dossier,run):
    d=verified(dossier)
    for a in d['assessments']:a['evidence_refs']=['NMI']
    out=run(d)
    assert out['decision']['epistemic_ceiling']=='OPEN'


def test_hg07_unsafe_trace_overrides_false_pass(dossier,run):
    d=verified(dossier)
    for c in d['oracle_results'][0]['checks']:c['result']='PASS'
    for o in d['oracle_observations']:
        if o['payload']['kind']=='trace':
            o['payload']['trace'][-1].update(object_alive=False,callback_possible=True,live_references=1,rcu_readers=1,registered_owner=True)
    out=run(rebind(d))
    assert all(e['result']=='BLOCKED' for e in out['oracle_evaluations'])
    assert {'callback_after_free','uaf','ffi_lifetime'} <= set(out['hard_gates']['findings'])


def test_hg06_same_safe_trace_opposite_labels_same_evaluations(dossier,run):
    d=verified(dossier);a=run(d)
    d['oracle_results'][0]['checks'][0]['result']='BLOCKED';b=run(rebind(d))
    assert a['oracle_evaluations']==b['oracle_evaluations']
    # The separate conservative reported-failure veto must not be weakened.
    assert b['hard_gates']['status']=='BLOCKED'


def test_hg07_no_arbitrary_trace_fields_or_expressions(dossier,run):
    dossier['oracle_observations'][0]['payload']['trace'][0]['expression']='eval(candidate)'
    with pytest.raises(Invalid):run(rebind(dossier))


def test_hash_and_yaml_json_equivalence(dossier,run,tmp_path):
    import yaml
    out=run(dossier)
    for name,text in [('input.json',json.dumps(dossier,sort_keys=True)),('input.yaml',yaml.safe_dump(dossier,sort_keys=True))]:
        p=tmp_path/name;p.write_text(text)
        assert canonical(run(load(p)))==canonical(out)
    before=canonical(out)
    report(out)
    assert canonical(out)==before
    # Presentation indentation is not part of the input record.
    assert digest(json.loads(json.dumps(out,indent=8)))==digest(out)
    for field in ['timestamp','limitations']:
        d=deepcopy(dossier)
        if field=='timestamp':d[field]='2027-09-27T00:00:00Z'
        else:d[field].append('Additional recorded limitation (a fact, not formatting).')
        changed=run(rebind(d))
        assert changed['assessment_hash']!=out['assessment_hash']
        assert changed['decision']==out['decision']
    swapped=deepcopy(dossier);swapped['assessments'].reverse()
    assert run(swapped)['assessment_hash']!=out['assessment_hash']


def test_yaml_scalar_and_alias_boundaries(tmp_path,dossier,run):
    import yaml
    p=tmp_path/'data.yaml'
    p.write_text('timestamp: 2026-09-27T00:00:00Z\nstatus: ON\nvalue: null\n')
    value=load(p)
    assert isinstance(value['timestamp'],str)
    assert value['status'] is True and value['value'] is None
    d=deepcopy(dossier);d['invariants'][0]['epistemic_status']=value['status']
    with pytest.raises(Invalid):run(rebind(d))
    for e in dossier['evidence']:e['environments']=dossier['scope']['environments']
    p.write_text(yaml.safe_dump(dossier,sort_keys=False))
    assert '&id' in p.read_text()
    assert canonical(run(load(p)))==canonical(run(dossier))
    p.write_text('x: &x {recursive: *x}')
    with pytest.raises(Invalid):load(p)


def test_catalog_missing_criticality_rejected(dossier,catalog):
    c,i,o=deepcopy(catalog);del i['D01']['critical']
    with pytest.raises(Invalid):derive(dossier,c['C047'],i,o)


def test_hg06_execution_failure_not_hidden_by_positive_trace(dossier,run):
    d=verified(dossier)
    # Trace itself is safe, but observation evidence records a real (synthetic) defect.
    d['evidence'][0]['detected_defects']=['deadlock']
    result=run(rebind(d))
    assert all(e['result']=='BLOCKED' for e in result['oracle_evaluations'])
    assert result['decision']['status']=='REJECTED'


def test_aud011_non_string_yaml_key_rejected(tmp_path):
    p=tmp_path/'keys.yaml';p.write_text('? [a,b]\n: value\n')
    with pytest.raises(Invalid):load(p)


def test_catalog_inconsistent_identity_rejects(dossier,catalog):
    c,i,o=deepcopy(catalog);i['D01']['id']='D99'
    with pytest.raises(Invalid,match='identity'):derive(dossier,c['C047'],i,o)


def test_empty_dynamic_population_not_observation(dossier):
    e=next(e for e in dossier['evidence'] if e['method']=='kcsan');e['coverage']['executed']=0
    with pytest.raises(Invalid,match='no executions'):check_evidence(e)


@pytest.mark.parametrize('gate',GATES)
def test_all_ten_veto_at_l5_e5_verified_agreement(dossier,run,gate):
    d=verified(dossier)
    for e in d['evidence']:e['tier']='E5'
    for a in d['assessments']:
        a['claimed_level']='L5';a['evidence_tier']='E5'
        a['observations']=[{'behavior_id':f'CB-047-{n:02}','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']} for n in range(1,6)]
    control=run(rebind(d))
    assert control['decision']['epistemic_ceiling']=='VERIFIED'
    assert control['inter_rater']['agreement'] is True
    d['hard_gates']={'status':'BLOCKED','findings':[gate]}
    for a in d['assessments']:a['hard_gates']=deepcopy(d['hard_gates'])
    out=run(rebind(d))
    assert out['capability']['level']=='L5' and out['evidence_tier']=='E5'
    assert out['decision']['epistemic_ceiling']=='VERIFIED' and out['inter_rater']['agreement'] is True
    assert out['hard_gates']['status']=='BLOCKED' and out['decision']['status']=='REJECTED'
    assert out['derived_signature']=='BLOCKED'


@pytest.mark.parametrize('field',['scope','invariants','oracle_results','oracle_observations','evidence','assessments','timestamp','primary_evidence_ref'])
@pytest.mark.parametrize('mutation',['missing','null'])
def test_mandatory_fields_not_repaired(dossier,field,mutation):
    if mutation=='missing':del dossier[field]
    else:dossier[field]=None
    with pytest.raises(Invalid):validate_record(dossier)


@pytest.mark.parametrize('mutation',['scope','capability','evidence'])
def test_semantic_changes_are_hash_bound(dossier,run,mutation):
    before=run(dossier)
    if mutation=='scope':dossier['scope']['exclusions'].append('additional_unqualified_task')
    if mutation=='evidence':dossier['evidence'][0]['statement']+=' Additional explicit fact.'
    if mutation=='capability':
        for a in dossier['assessments']:
            a['claimed_level']='L5'
            a['observations']=[{'behavior_id':f'CB-047-{n:02}','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']} for n in range(1,6)]
    assert run(rebind(dossier))['assessment_hash']!=before['assessment_hash']


def test_original_unsafe_narrative_explicitly_transcribed_to_trace(dossier,run):
    old=load(AUDIT/'contradictory-teardown-trace-with-pass-labels.json')
    assert 'FREE(target) while callback_possible=true and live_reference=true' in old['evidence'][0]['statement']
    d=current_provenance(old,dossier)
    # Explicit fixture transcription, NOT a general prose parser or engine inference.
    for o in d['oracle_observations']:
        if o['payload']['kind']=='trace':
            o['payload']['trace'][-1].update(object_alive=False,callback_possible=True,live_references=1)
    out=run(rebind(d))
    assert out['decision']['status']=='REJECTED' and out['derived_signature']=='BLOCKED'
    assert {'uaf','callback_after_free'}<=set(out['hard_gates']['findings'])
