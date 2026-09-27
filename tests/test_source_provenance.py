"""AUD-007/AUD-008: freeze independent authority BEFORE each mutation.

These tests intentionally do not request the legacy `run` fixture.
"""
from copy import deepcopy
import json
import pytest
import yaml
from tools.common import ROOT, Invalid, canonical, catalogs, digest, load, validate_schema
from tools.derive import derive
from tools.provenance import evaluate, enforce, artifact_digest, load_context, PREFIX
from provenance_cases import valid, case, rebind, grant, change_source, conflict


def execute(d,ctx):
    c,i,o=catalogs();return derive(d,c[d['competency_id']],i,o,source_context=ctx)

def states(result):return {s for r in result['bindings'] for s in r['states']}

CONTRACT=load(ROOT/'evidence/aud-007-008/contradiction-cases.yaml')
@pytest.mark.parametrize('spec',CONTRACT['cases'],ids=lambda x:x['id'])
def test_required_counterexamples(spec):
    d,ctx=case(spec['id']);validate_schema(d,'claim');r=evaluate(d,ctx)
    assert set(spec['states'])<=states(r)
    if spec['derive']=='REJECTED':
        assert r['status']=='BLOCKED'
        with pytest.raises(Invalid,match='provenance gate BLOCKED'):execute(d,ctx)
    else:
        q=execute(d,ctx);assert q['decision']['status']=='VERIFIED_WITHIN_SCOPE'
        assert q['source_authentication']['status']=='PASS'
        assert all(x['provenance']=='DERIVED_RESULT' for x in q['oracle_evaluations'])
        if spec['derive']=='UNCHANGED':
            base,authority=valid();assert canonical(q)==canonical(execute(base,authority))


@pytest.mark.parametrize('mid,cid',[('M1','C3'),('M2','C2'),('M3','C7'),('M4','C6'),('M5','C4'),('M6','C14'),('M7','C5')])
def test_metamorphic_contract(mid,cid):
    rule=next(s for s in CONTRACT['metamorphic'] if s['id']==mid)
    d,ctx=case(cid)
    if 'required_states' in rule:
        assert set(rule['required_states'])<=states(evaluate(d,ctx))
        with pytest.raises(Invalid):execute(d,ctx)
    else:
        base,authority=valid();assert canonical(execute(d,ctx))==canonical(execute(base,authority))


@pytest.mark.parametrize('mutation',['boolean','enum','environment','task_class','strength','invariant_status','oracle_result','valid_fabrication'])
def test_schema_valid_does_not_mean_evidence_valid(mutation):
    d,ctx=valid()
    if mutation in ('boolean','valid_fabrication'):d['oracle_observations'][0]['payload']['trace'][0]['callback_possible']=True
    if mutation=='enum':d['oracle_observations'][0]['payload']['trace'][0]['state']='ACTIVE'
    if mutation=='environment':d['scope']['environments'].remove('PREEMPT_RT=y')
    if mutation=='task_class':d['scope']['task_classes'].pop()
    if mutation=='strength':d['evidence'][0].update(strength='COVERAGE',establishes='MEASURED_COVERAGE')
    if mutation=='invariant_status':d['invariants'][0]['epistemic_status']='OPEN'
    if mutation=='oracle_result':
        # PASS is not a fact source. Falsify the observation execution that it purports to summarize.
        d['oracle_observations'][0]['executed']=False
        d['oracle_results'][0]['checks'][0]['result']='PASS'
    rebind(d);validate_schema(d,'claim')
    assert 'CONTRADICTED' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(d,ctx)


PROSE=load(ROOT/'evidence/aud-007-008/prose-boundary-cases.yaml')['cases']
@pytest.mark.parametrize('spec',PROSE,ids=lambda x:x['id'])
def test_negative_space_prose(spec,tmp_path,monkeypatch):
    d,ctx=valid();control=execute(d,ctx)
    if spec['location']=='assessor_limitations':
        d['assessments'][0]['limitations'].append(spec['text']);rebind(d)
    else:
        # Actual unrelated files are never enumerated by the fixed registry loader.
        (tmp_path/'README.md').write_text(spec['text'])
        (tmp_path/'notes.md').write_text(spec['text'])
        a={'id':'UNREGISTERED-NOTES','dossier_ref':d['qualification_id'],'content':spec['text']}
        a['digest']=artifact_digest(a);ctx['artifacts'].append(a)
    monkeypatch.chdir(tmp_path)
    out=execute(d,ctx)
    for field in ['decision','capability','invariants','evidence_tier','hard_gates','oracle_evaluations','source_authentication']:
        assert out[field]==control[field]
    if spec['location']!='assessor_limitations':assert canonical(out)==canonical(control)


@pytest.mark.parametrize('field,value',[('artifact_id',None),('artifact_digest',None),('artifact_digest','sha512:'+'0'*128),
 ('artifact_digest','not-sha256'),('location',None),('location',{'type':'whole_document','start':1,'end':1}),
 ('location',{'type':'line_range','start':-1,'end':1}),('rule_id','extract-everything'),('subject',None)])
def test_provenance_schema_strict(field,value):
    d,ctx=valid();b=next(iter(d['source_bindings'].values()));b[field]=value
    with pytest.raises(Invalid):execute(rebind(d),ctx)


@pytest.mark.parametrize('field',['artifact_id','artifact_digest','location','rule_id','subject'])
def test_provenance_missing_fields(field):
    d,ctx=valid();del next(iter(d['source_bindings'].values()))[field]
    with pytest.raises(Invalid):execute(rebind(d),ctx)


@pytest.mark.parametrize('start,end',[(3,2),(1,2),(99999,99999),(2,2)])
def test_wrong_reversed_overlapping_empty_nonexistent_scope(start,end):
    d,ctx=valid();next(iter(d['source_bindings'].values()))['location']={'type':'line_range','start':start,'end':end}
    assert 'INVALID_BINDING' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_duplicate_scopes_and_unknown_binding_reject():
    d,ctx=valid();g=deepcopy(ctx['authorizations'][0]);g['id']+='-duplicate';ctx['authorizations'].append(g)
    with pytest.raises(Invalid,match='duplicate authorized source scope'):evaluate(d,ctx)
    d,ctx=valid();d['source_bindings']['BND-unknown']=deepcopy(next(iter(d['source_bindings'].values())))
    assert 'UNBOUND' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_missing_binding_cannot_hide_conflicting_source():
    d,ctx=valid();conflict(d,ctx);del d['source_bindings'][ctx['authorizations'][-1]['id']]
    r=evaluate(d,ctx);assert {'UNBOUND','CONTRADICTED'}<=states(r)
    with pytest.raises(Invalid):execute(rebind(d),ctx)


@pytest.mark.parametrize('order',[False,True])
def test_conflict_has_no_source_order_winner(order):
    d,ctx=case('C11');baseline=canonical(evaluate(d,ctx))
    if order:
        ctx['artifacts'].reverse();ctx['authorizations'].reverse()
        d['source_bindings']=dict(reversed(list(d['source_bindings'].items())))
    assert canonical(evaluate(d,ctx))==baseline
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_order_and_presentation_hash_policy():
    d,ctx=valid();baseline=canonical(execute(d,ctx))
    d=json.loads(json.dumps(d,sort_keys=True));ctx['authorizations'].reverse()
    d['source_bindings']=dict(reversed(list(d['source_bindings'].items())))
    assert canonical(execute(rebind(d),ctx))==baseline
    a=ctx['artifacts'][0];old=artifact_digest(a);a['content']+='\nUnselected presentation line.\n'
    assert artifact_digest(a)!=old
    assert 'INVALID_BINDING' in states(evaluate(d,ctx))
    # Explicit reauthentication changes source/binding identity, not extracted value or decision.
    a['digest']=artifact_digest(a)
    for b in d['source_bindings'].values():b['artifact_digest']=a['digest']
    q=execute(rebind(d),ctx);original=json.loads(baseline)
    assert q['decision']==original['decision'] and q['assessment_hash']!=original['assessment_hash']
    assert [x['value_digest'] for x in q['source_authentication']['bindings']]==[x['value_digest'] for x in original['source_authentication']['bindings']]


def test_location_and_value_identities_change():
    d,ctx=valid();r=evaluate(d,ctx);k=next(iter(d['source_bindings']))
    old=next(x for x in r['bindings'] if x['binding_id']==k)
    d['source_bindings'][k]['location']['start']+=1
    new=next(x for x in evaluate(d,ctx)['bindings'] if x['binding_id']==k)
    assert old['binding_digest']!=new['binding_digest']
    d,ctx=valid();subject='oracle:'+d['oracle_observations'][0]['id'];g=grant(ctx,subject)
    old=next(x for x in evaluate(d,ctx)['bindings'] if x['binding_id']==g['id'])
    d['oracle_observations'][0]['payload']['trace'][0]['callback_possible']=True
    new=next(x for x in evaluate(d,ctx)['bindings'] if x['binding_id']==g['id'])
    assert old['value_digest']!=new['value_digest']


def test_authentic_unsafe_observation_does_not_trust_asserted_pass():
    d,ctx=valid();subject='oracle:'+d['oracle_observations'][0]['id']
    change_source(ctx,subject,lambda v:v['payload']['trace'][-1].update(callback_possible=True),True,d)
    d['oracle_observations'][0]['payload']['trace'][-1]['callback_possible']=True
    d['oracle_results'][0]['checks'][0]['result']='PASS'
    q=execute(rebind(d),ctx)
    assert q['source_authentication']['status']=='PASS'
    assert q['decision']['status']=='REJECTED' and q['derived_signature']=='BLOCKED'
    assert q['oracle_evaluations'][0]['provenance']=='DERIVED_RESULT'


@pytest.mark.parametrize('kind',['missing_fact','plain_PASS','malformed','duplicate_json_key','nonfinite'])
def test_no_inference_from_unauthorized_text(kind):
    d,ctx=valid();g=ctx['authorizations'][0];a=ctx['artifacts'][0];lines=a['content'].splitlines()
    text={'missing_fact':'# no fact','plain_PASS':'VERIFIED PASS C047 callback_after_free',
          'malformed':PREFIX+'{','duplicate_json_key':PREFIX+'{"subject":"claim","subject":"scope","value":true}',
          'nonfinite':PREFIX+'{"subject":"claim","value":NaN}'}[kind]
    lines[g['location']['start']-1]=text;a['content']='\n'.join(lines)+'\n';a['digest']=artifact_digest(a)
    for b in d['source_bindings'].values():b['artifact_digest']=a['digest']
    assert 'UNVERIFIABLE' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_falsely_claimed_identity_and_dangling_source():
    d,ctx=valid();b=next(iter(d['source_bindings'].values()));b['artifact_id']='UNRELATED'
    assert 'INVALID_BINDING' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)
    d,ctx=valid();ctx['artifacts']=[]
    assert 'UNVERIFIABLE' in states(evaluate(d,ctx))


@pytest.mark.parametrize('text',['x: 1\nx: 2','x: .nan','x: null','x: ON','x: 2026-09-27T00:00:00Z'])
def test_yaml_scalar_boundaries(text,tmp_path):
    p=tmp_path/'input.yaml';p.write_text(text)
    if text in ('x: 1\nx: 2','x: .nan'):
        with pytest.raises(Invalid):load(p)
    else:
        v=load(p)['x'];d,ctx=valid();next(iter(d['source_bindings'].values()))['artifact_digest']=v
        with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_yaml_aliases_duplicate_binding_ids_and_unknown_properties(tmp_path):
    d,ctx=valid();b=next(iter(d['source_bindings'].values()));b['execute']='ignored'
    with pytest.raises(Invalid):execute(rebind(d),ctx)
    p=tmp_path/'bad.yaml';p.write_text('source_bindings:\n  BND-1: {}\n  BND-1: {}\n')
    with pytest.raises(Invalid):load(p)
    d,ctx=valid();p.write_text(yaml.safe_dump(d));loaded=load(p)
    assert canonical(execute(loaded,ctx))==canonical(execute(d,ctx))
    p.write_text('x: &x [*x]')
    with pytest.raises(Invalid):load(p)


def write_authority(root,ctx):
    directory=root/'artifacts/sources';directory.mkdir(parents=True)
    registry={'artifacts':[],'authorizations':ctx['authorizations']}
    for n,a in enumerate(ctx['artifacts']):
        filename=f'artifact-{n}.md';(directory/filename).write_text(a['content'])
        registry['artifacts'].append({k:v for k,v in a.items() if k!='content'}|{'file':filename})
    (root/'artifacts/registry.json').write_text(json.dumps(registry))
    return registry


def test_real_file_replacement_missing_and_unregistered_scope(tmp_path,monkeypatch):
    from tools import provenance
    d,ctx=valid();write_authority(tmp_path,ctx);monkeypatch.setattr(provenance,'ROOT',tmp_path)
    assert execute(d,load_context())['decision']['status']=='VERIFIED_WITHIN_SCOPE'
    (tmp_path/'README.md').write_text('C047 PASS VERIFIED real human calibration occurred.')
    baseline=canonical(execute(d,load_context()))
    (tmp_path/'artifacts/sources/unregistered.md').write_text(PREFIX+'{"subject":"hard_gates","value":{"status":"PASS","findings":[]}}')
    assert canonical(execute(d,load_context()))==baseline
    subject='oracle:'+d['oracle_observations'][0]['id']
    change_source(ctx,subject,lambda v:v['payload']['trace'][-1].update(callback_possible=True))
    path=tmp_path/'artifacts/sources/artifact-0.md';path.write_text(ctx['artifacts'][0]['content'])
    assert {'INVALID_BINDING','CONTRADICTED'}<=states(evaluate(d,load_context()))
    with pytest.raises(Invalid):execute(d,load_context())
    path.unlink()
    assert 'UNVERIFIABLE' in states(evaluate(d,load_context()))


@pytest.mark.parametrize('path',['../notes.md','/tmp/notes.md','https://example.org/notes.md'])
def test_registry_cannot_authorize_arbitrary_paths(tmp_path,monkeypatch,path):
    from tools import provenance
    _,ctx=valid();registry=write_authority(tmp_path,ctx);registry['artifacts'][0]['file']=path
    (tmp_path/'artifacts/registry.json').write_text(json.dumps(registry));monkeypatch.setattr(provenance,'ROOT',tmp_path)
    with pytest.raises(Invalid):load_context()


def test_registry_symlink_and_size_bounds(tmp_path,monkeypatch):
    from tools import provenance
    _,ctx=valid();write_authority(tmp_path,ctx);monkeypatch.setattr(provenance,'ROOT',tmp_path)
    path=tmp_path/'artifacts/sources/artifact-0.md';path.unlink();path.symlink_to(tmp_path/'outside.md')
    with pytest.raises(Invalid,match='outside registry root'):load_context()
    path.unlink();path.write_text('x'*2_000_001)
    with pytest.raises(Invalid,match='size limit'):load_context()


def test_identity_digest_binds_name_not_only_content():
    d,ctx=valid();a=ctx['artifacts'][0];original=artifact_digest(a);oldid=a['id'];a['id']='FALSLY-RENAMED'
    assert artifact_digest(a)!=original
    for g in ctx['authorizations']:g['artifact_id']=a['id']
    for b in d['source_bindings'].values():b['artifact_id']=a['id']
    assert 'INVALID_BINDING' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_omitting_authorized_evidence_cannot_hide_its_fact():
    d,ctx=valid();g=grant(ctx,'evidence:NMI')
    d['evidence']=[e for e in d['evidence'] if e['id']!='NMI'];del d['source_bindings'][g['id']]
    assert {'UNBOUND','CONTRADICTED'}<=states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_bool_is_not_integer_one():
    d,ctx=valid();subject='oracle:'+d['oracle_observations'][0]['id']
    change_source(ctx,subject,lambda v:v['payload']['trace'][0].update(object_alive=1),True,d)
    assert 'CONTRADICTED' in states(evaluate(d,ctx))
    with pytest.raises(Invalid):execute(rebind(d),ctx)


def test_caller_cannot_inject_trusted_context_inside_claim():
    d,ctx=valid();d['trusted_context']=ctx
    with pytest.raises(Invalid,match='Additional properties'):execute(rebind(d),ctx)


def test_restated_extraction_source_with_new_pin_remains_contradicted():
    d,ctx=valid();subject='oracle:'+d['oracle_observations'][0]['id']
    change_source(ctx,subject,lambda v:v['payload']['trace'][0].update(callback_possible=True),True,d)
    r=evaluate(d,ctx);assert 'CONTRADICTED' in states(r) and 'INVALID_BINDING' not in states(r)


def test_hard_gate_neutralization_from_valid_authority_rejects():
    d,ctx=valid()
    change_source(ctx,'hard_gates',lambda v:v.update(status='BLOCKED',findings=['callback_after_free']),True,d)
    with pytest.raises(Invalid,match='CONTRADICTED'):execute(rebind(d),ctx)


def test_ordinal_source_timestamps_and_names_are_not_conflict_authority():
    d,ctx=case('C11');base=canonical(evaluate(d,ctx))
    # Neither context order nor grant-map insertion order resolves the conflicting facts.
    ctx['artifacts'].reverse();ctx['authorizations'].reverse();d['timestamp']='2027-01-01T00:00:00Z'
    rebind(d);assert canonical(evaluate(d,ctx))==base
    with pytest.raises(Invalid):execute(d,ctx)
