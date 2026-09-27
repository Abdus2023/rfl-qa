"""Frozen-before-mutation, explicit attack fixtures. No legacy run-fixture issuance."""
from copy import deepcopy
import json
from tools.common import ROOT, load, canonical, dossier_digest
from tools.provenance import PREFIX, artifact_digest
from source_fixtures import issue


def rebind(d):
    for a in d['assessments']:a['dossier_digest']=dossier_digest(d)
    return d


def valid():
    d=load(ROOT/'dossiers/examples/003-callback-teardown.json')
    for e in d['evidence']:
        if e['required']:e['epistemic_status']='VERIFIED'
    for inv in d['invariants']:inv['epistemic_status']='VERIFIED'
    for a in d['assessments']:
        for inv in a['invariant_findings']:inv['epistemic_status']='VERIFIED'
    return issue(rebind(d))


def grant(ctx,subject):return next(g for g in ctx['authorizations'] if g['subject']==subject)
def artifact(ctx,g):return next(a for a in ctx['artifacts'] if a['id']==g['artifact_id'])

def change_source(ctx,subject,change,reseal=False,d=None):
    g=grant(ctx,subject);a=artifact(ctx,g);lines=a['content'].splitlines()
    n=g['location']['start']-1;fact=json.loads(lines[n][len(PREFIX):]);change(fact['value'])
    lines[n]=PREFIX+canonical(fact).decode();a['content']='\n'.join(lines)+'\n'
    if reseal:
        a['digest']=artifact_digest(a)
        if d is not None:
            for b in d['source_bindings'].values():
                if b['artifact_id']==a['id']:b['artifact_digest']=a['digest']


def conflict(d,ctx,subject='scope'):
    g=deepcopy(grant(ctx,subject));a=deepcopy(artifact(ctx,g))
    a['id']+='-conflict';g['id']+='-conflict';g['artifact_id']=a['id']
    temp={'artifacts':[a],'authorizations':[g]}
    change_source(temp,subject,lambda v:v['environments'].remove('PREEMPT_RT=y'),reseal=True)
    ctx['artifacts'].append(a);ctx['authorizations'].append(g)
    d['source_bindings'][g['id']]=deepcopy({k:v for k,v in g.items() if k not in ('id','dossier_ref')})|{'artifact_digest':a['digest']}


def case(identifier):
    d,ctx=valid();subject='oracle:'+d['oracle_observations'][0]['id'];g=grant(ctx,subject)
    if identifier in ('C2','C15'):d['oracle_observations'][0]['payload']['trace'][0]['callback_possible']=True
    if identifier=='C3':change_source(ctx,subject,lambda v:v['payload']['trace'][0].update(callback_possible=True))
    if identifier=='C4':d['source_bindings'][g['id']]['artifact_digest']='0'*64
    if identifier=='C5':d['source_bindings'][g['id']]['location']={'type':'line_range','start':1,'end':1}
    if identifier=='C6':ctx['artifacts'][0]['content']=None
    if identifier=='C11':conflict(d,ctx)
    if identifier=='C12':change_source(ctx,subject,lambda v:v['payload']['trace'][-1].update(callback_possible=True),True,d)
    if identifier=='C13':change_source(ctx,'hard_gates',lambda v:v.update(status='BLOCKED',findings=['critical_external_assumption']),True,d)
    if identifier=='C14':
        d['qualification_id']='Q-2026-9999'
        for a in d['assessments']:a['dossier_ref']=d['qualification_id']
    # C7..C10: unrelated bytes exist as an unregistered artifact, no grant.
    if identifier in ('C7','C8','C9','C10'):
        text={'C7':'PASS','C8':'VERIFIED','C9':'Human calibration occurred','C10':'C047 CB-047-01 OR-CALLBACK'}[identifier]
        a={'id':'UNRELATED','dossier_ref':d['qualification_id'],'content':text};a['digest']=artifact_digest(a);ctx['artifacts'].append(a)
    return rebind(d),ctx
