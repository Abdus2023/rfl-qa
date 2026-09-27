"""Adversarial audit probes. Writes ONLY under evidence/adversarial-audit/."""
from copy import deepcopy
import json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; A=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from tools.common import Invalid, GATES, EPISTEMIC, canonical, catalogs, digest, dossier_digest, load, validate_schema
from tools.derive import derive
from tools.report import report
from tools.validate import validate_dossier, validate_record
CAT=catalogs(); BASE=load(ROOT/'dossiers/examples/003-callback-teardown.json')
RESULTS=[]; (A/'counterexamples').mkdir(exist_ok=True); (A/'tier-fixtures').mkdir(exist_ok=True)

def bind(d):
 for a in d['assessments']: a['dossier_digest']=dossier_digest(d)
 return d

def sync(d):
 for a in d['assessments']:
  a['invariant_findings']=[{'invariant_ref':i['id'],'class':i['class'],'epistemic_status':i['epistemic_status']} for i in d['invariants']]
 return bind(d)

def verified():
 d=deepcopy(BASE)
 for e in d['evidence']:
  if e['required']: e['epistemic_status']='VERIFIED'
 for i in d['invariants']: i['epistemic_status']='VERIFIED'
 return sync(d)

def behavior(d,n,tier='E4'):
 d['evidence'][0]['tier']=tier
 for a in d['assessments']:
  a['claimed_level']='L'+str(n); a['evidence_tier']=tier
  a['observations']=[{'behavior_id':f'CB-047-{i:02}','status':'DEMONSTRATED','evidence_refs':['ARTIFACT']} for i in range(1,n+1)]
  if not n: a['observations']=[{'behavior_id':'CB-047-01','status':'FAILED','evidence_refs':['ARTIFACT']}]
 return bind(d)

def summarize(q):
 return {'capability':q['capability']['level'] if q['capability'] else None,'decision':q['decision'],'hard_gates':q['hard_gates'],
         'derived_signature':q['derived_signature'],'assessment_hash':q['assessment_hash'],'inter_rater':q['inter_rater']}

def probe(name,d,expect,group,check=None,save=False):
 d=bind(deepcopy(d)); phase='SCHEMA'
 try:
  validate_schema(d,'claim'); phase='SEMANTIC'
  validate_dossier(d,CAT); phase='DERIVATION'
  q=derive(d,CAT[0][d['competency_id']],CAT[1],CAT[2])
  result={'outcome':'ACCEPTED','value':summarize(q)}
  ok=(expect!='REJECT_INVALID') and (check(q) if check else True)
 except Invalid as exc:
  result={'outcome':'REJECTED_INVALID','phase':phase,'reason':str(exc)}; ok=expect=='REJECT_INVALID'
 except Exception as exc:
  result={'outcome':'CRASH','phase':phase,'exception':type(exc).__name__,'reason':str(exc)}; ok=False
 entry={'id':name,'group':group,'expected':expect,'boundary_held':ok,**result}; RESULTS.append(entry)
 if not ok or save:
  (A/'counterexamples'/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n')
  if result['outcome']=='ACCEPTED': (A/'counterexamples'/f'{name}.result.json').write_text(json.dumps(q,indent=2)+'\n')
 return result

# Every requested E/L combination; E0 affects eligibility, never behavioral level.
for tier,n in [('E5',0),('E4',1),('E4',2),('E3',2),('E2',3),('E1',4),('E0',5)]:
 d=behavior(deepcopy(BASE),n,tier)
 (A/'tier-fixtures'/f'{tier}-L{n}.json').write_text(json.dumps(d,indent=2)+'\n')
 probe(f'tier-{tier}-L{n}',d,f'capability L{n}', 'E_TO_L',lambda q,n=n:q['capability']['level']==f'L{n}')
for n in range(6):
 for tier in ['E0','E1','E2','E3','E4','E5']:
  probe(f'fixed-behavior-L{n}-{tier}',behavior(deepcopy(BASE),n,tier),f'L{n}','E_TO_L',lambda q,n=n:q['capability']['level']==f'L{n}')
for n in [2,3,4,5]:
 d=behavior(deepcopy(BASE),n)
 probe(f'all-L{n}',d,f'L{n}','BEHAVIOR',lambda q,n=n:q['capability']['level']==f'L{n}')
 for a in d['assessments']: a['observations'][-1]['status']='FAILED'
 probe(f'failed-required-L{n}',d,f'L{n-1}','BEHAVIOR',lambda q,n=n:q['capability']['level']==f'L{n-1}')
d=behavior(deepcopy(BASE),2)
for a in d['assessments']: a['claimed_level']='L3'
probe('partial-L3-only-L2',d,'L2','BEHAVIOR',lambda q:q['capability']['level']=='L2')
for level in [4,5]:
 d=behavior(deepcopy(BASE),level-1,f'E{level}')
 for a in d['assessments']: a['claimed_level']=f'L{level}'
 probe(f'incomplete-L{level}-high-tier',d,f'L{level-1}','BEHAVIOR',lambda q,level=level:q['capability']['level']==f'L{level-1}')
for unknown in ['CB-047-999','CB-047-99','CB-053-01']:
 d=deepcopy(BASE);d['assessments'][0]['observations'][0]['behavior_id']=unknown
 probe('invented-'+unknown,d,'REJECT_INVALID','SCHEMA')
d=deepcopy(BASE);d['assessments'][0]['observations'].append(deepcopy(d['assessments'][0]['observations'][0]))
probe('duplicate-identical-behavior',d,'REJECT_INVALID','SCHEMA')
d['assessments'][0]['observations'][-1]['status']='FAILED'
probe('duplicate-conflicting-behavior',d,'REJECT_INVALID','SCHEMA')

# Scope additions reject, task subsets narrow, environment conjunction erasure is attacked separately.
for key,value in [('environments','arm64'),('task_classes','dma'),('task_classes','nmi_context'),('environments','PREEMPT_RT=n'),('competencies','C053'),('task_classes','all_ffi')]:
 d=deepcopy(BASE);d['scope'][key].append(value)
 probe('scope-outside-'+value,d,'REJECT_INVALID','SCOPE')
for key in ['competencies','domains','task_classes','environments','exclusions']:
 d=deepcopy(BASE);del d['scope'][key]
 probe('scope-missing-'+key,d,'REJECT_INVALID','SCOPE')
d=verified();d['scope']['task_classes']=['callback_registration']
probe('scope-task-subset',d,'preserved narrower task scope','SCOPE',lambda q:q['scope']==d['scope'])
for envs in [['x86_64'],['PREEMPT_RT=y'],['CONFIG_RUST=y']]:
 d=verified();d['scope']['environments']=envs
 probe('scope-erased-'+envs[0].replace('=','-'),d,'REJECT_INVALID','SCOPE',save=True)

# Type-D structure and semantic support.
for kind in ['missing','boolean','empty','bad_ref','unrelated_method','unknown_assessor','valid','provisional','open','unrelated_audit']:
 d=verified();inv=d['invariants'][-1]
 if kind=='missing': del inv['external_evidence']
 elif kind=='boolean': inv['external_evidence']=True
 elif kind=='empty': inv['external_evidence']=[]
 elif kind=='bad_ref': inv['external_evidence'][0]['ref']='MISSING'
 elif kind=='unrelated_method': inv['external_evidence'][0]['ref']='TYPE';inv['evidence_refs'].append('TYPE')
 elif kind=='unknown_assessor': inv['external_evidence'][0]['assessor']='not-a-participant'
 elif kind in ['provisional','open']: inv['epistemic_status']=kind.upper();inv['external_evidence']=[];sync(d)
 elif kind=='unrelated_audit':
  inv['external_evidence'][0]['description']='Audit concerns an unrelated SATA register, not unregister/drain or target lifetime.'
  d['evidence'][-1]['statement']='Reviewed unrelated SATA register documentation; no callback lifetime information.'
 expected='REJECT_INVALID' if kind in ['missing','boolean','empty','bad_ref','unrelated_method','unknown_assessor','unrelated_audit'] else ('BLOCKED' if kind in ['provisional','open'] else 'supported D accepted')
 probe('type-d-'+kind,d,expected,'TYPE_D',lambda q,kind=kind:q['hard_gates']['status']=='BLOCKED' if kind in ['provisional','open'] else q['decision']['status']=='VERIFIED_WITHIN_SCOPE')

# Trust-boundary metadata downgrade. D01 is critical in the normative catalog.
d=verified();d['invariants'][-1]['epistemic_status']='OPEN';d['invariants'][-1]['external_evidence']=[];sync(d)
probe('critical-open-control',d,'BLOCKED','HARD_GATE',lambda q:q['hard_gates']['status']=='BLOCKED')
d['invariants'][-1]['critical']=False
probe('critical-open-declared-noncritical',d,'BLOCKED or validation rejection','HARD_GATE',lambda q:q['hard_gates']['status']=='BLOCKED',save=True)
# OPEN external evidence cannot substantiate a VERIFIED critical external contract.
d=verified();d['evidence'][-1]['epistemic_status']='OPEN'
probe('critical-verified-with-open-support',d,'BLOCKED or validation rejection','TYPE_D',lambda q:q['hard_gates']['status']=='BLOCKED',save=True)

# Independent axes and weakest-required ceiling.
for inv_id,status in [('A01','PROVISIONAL'),('B01','VERIFIED'),('C01','PARTIALLY_VERIFIED'),('D01','OPEN'),('C01','PROVISIONAL'),('B01','OPEN')]:
 d=verified();i=next(i for i in d['invariants'] if i['id']==inv_id);i['epistemic_status']=status;sync(d)
 probe(f'epistemic-{inv_id}-{status}',d,status,'EPISTEMIC',lambda q,status=status:q['decision']['epistemic_ceiling']==status)
for status in EPISTEMIC:
 d=verified();d['invariants'][1]['epistemic_status']=status;sync(d)
 for tier in ['E0','E4','E5']:
  d=behavior(d,3,tier)
  probe(f'ceiling-{status}-{tier}',d,status,'EPISTEMIC',lambda q,status=status:q['decision']['epistemic_ceiling']==status)
# Required oracle evidence is omitted from the ceiling closure.
d=verified();test=next(e for e in d['evidence'] if e['id']=='TEST');test['required']=False;test['epistemic_status']='OPEN'
d['invariants'][2]['evidence_refs']=['ARTIFACT'];sync(d)
probe('oracle-open-evidence-not-in-ceiling',d,'ceiling OPEN or rejection','EPISTEMIC',lambda q:q['decision']['epistemic_ceiling']=='OPEN',save=True)
# Explicit not_tested/zero-count evidence is not rejected when mislabeled OBSERVATION.
d=verified();artifact=d['evidence'][0];artifact['method']='not_tested';artifact['coverage']['executed']=0;artifact['statement']='No assessment or observation was performed.'
probe('not-tested-as-observation',d,'REJECT_INVALID','STRENGTH',save=True)
for strength in ['PROOF','COVERAGE','OBSERVATION']:
 d=verified();e=next(e for e in d['evidence'] if e['id']=='TEST');e['coverage']['executed']=10**12;e['strength']=strength
 e['establishes']={'PROOF':'ASSUMPTION_BOUND_PROOF','COVERAGE':'MEASURED_COVERAGE','OBSERVATION':'BOUNDED_OBSERVATION'}[strength];e['assumptions']=['Audited model']
 # callback checks require OBSERVATION: use ARTIFACT when testing legal COVERAGE evidence.
 if strength=='COVERAGE':
  for check in d['oracle_results'][0]['checks']:
   if check['evidence_refs']==['TEST']:check['evidence_refs']=['ARTIFACT']
 probe('kcsan-'+strength,d,'REJECT_INVALID' if strength=='PROOF' else 'strength preserved','STRENGTH',lambda q,strength=strength:next(e for e in q['evidence'] if e['id']=='TEST')['strength']==strength)

# Every frozen hard gate dominates maximal L/E/epistemic inputs.
for gate in GATES:
 d=behavior(verified(),5,'E5');d['evidence'][0]['detected_defects']=[gate]
 probe('hard-gate-'+gate,d,'REJECTED/BLOCKED','HARD_GATE',lambda q:q['decision']['status']=='REJECTED' and q['derived_signature']=='BLOCKED' and q['hard_gates']['status']=='BLOCKED')

# Schema invalidity, no silent repair.
for field,value in [('qualification_id','bad'),('timestamp','not-a-date'),('scope',None),('competency_id','C999')]:
 d=deepcopy(BASE);d[field]=value;probe('malformed-'+field,d,'REJECT_INVALID','SCHEMA')
for label,fn in [
 ('unknown-property',lambda d:d.update(extra=True)),
 ('empty-evidence',lambda d:d.update(evidence=[])),
 ('empty-assessments',lambda d:d.update(assessments=[])),
 ('unknown-invariant',lambda d:d['invariants'][0].update(id='NOTFOUND')),
 ('unknown-assessor-ref',lambda d:d['invariants'][-1]['external_evidence'][0].update(assessor='alien')),
 ('bad-level-type',lambda d:d['assessments'][0].update(claimed_level=4)),
 ('unknown-epistemic',lambda d:d['invariants'][0].update(epistemic_status='PROVED')),
 ('unknown-class',lambda d:d['invariants'][0].update(**{'class':'UNKNOWN'})),
 ('missing-behavior-evidence',lambda d:d['assessments'][0]['observations'][0].update(evidence_refs=[])),
 ('duplicate-assessor',lambda d:d['assessments'][1].update(assessor_id=d['assessments'][0]['assessor_id']))]:
 d=deepcopy(BASE);fn(d);probe(label,d,'REJECT_INVALID','SCHEMA')

# Disagreement remains explicit across all five axes.
for axis in ['capability','evidence','invariant','epistemic','hard-gate']:
 d=deepcopy(BASE);a=d['assessments'][1]
 if axis=='capability': a['claimed_level']='L4'
 if axis=='evidence': a['evidence_tier']='E5'
 if axis=='invariant': a['invariant_findings'][0]['class']='B'
 if axis=='epistemic': a['invariant_findings'][0]['epistemic_status']='PROVISIONAL'
 if axis=='hard-gate': a['hard_gates']={'status':'BLOCKED','findings':['uaf']}
 probe('assessor-disagreement-'+axis,d,'halt and preserve divergence','CALIBRATION',lambda q:not q['inter_rater']['agreement'] and q['capability'] is None and bool(q['inter_rater']['events']))

# Oracle predicates are strings. A contradictory trace statement does not get evaluated.
d=verified();d['evidence'][0]['statement']='Counterexample: FREE(target) while callback_possible=true and live_reference=true. Delayed callback then dereferences freed target.'
probe('contradictory-teardown-trace-with-pass-labels',d,'BLOCKED or rejection','ORACLE',lambda q:q['hard_gates']['status']=='BLOCKED',save=True)
# Semantic field-free oracle tampering is studied in a copy of catalogs, not production files.
modified=deepcopy(CAT);modified[2]['OR-CALLBACK']['teardown_model']=['FREE','ACTIVE'];modified[2]['OR-CALLBACK']['safety_predicates']=['looks correct']
try:
 q=derive(verified(),modified[0]['C047'],modified[1],modified[2])
 RESULTS.append({'id':'oracle-invalid-state-model','group':'ORACLE','expected':'reject missing frozen states/predicate','boundary_held':False,'outcome':'ACCEPTED','value':summarize(q)})
 (A/'counterexamples/oracle-invalid-state-model.catalog.json').write_text(json.dumps(modified[2]['OR-CALLBACK'],indent=2)+'\n')
except Invalid as e: RESULTS.append({'id':'oracle-invalid-state-model','group':'ORACLE','boundary_held':True,'outcome':'REJECTED_INVALID','reason':str(e)})

# Report purity of genuine results, then rehashed forged result (not an authentication claim).
for status in EPISTEMIC:
 d=verified();d['invariants'][1]['epistemic_status']=status;sync(d)
 q=derive(d,CAT[0]['C047'],CAT[1],CAT[2]);before=canonical(q);text=report(q)
 RESULTS.append({'id':'report-purity-'+status,'group':'REPORT','boundary_held':before==canonical(q) and status in text,'outcome':'PRESENTED','decision':q['decision']})
q=derive(bind(deepcopy(BASE)),CAT[0]['C047'],CAT[1],CAT[2]);q['decision']['status']='VERIFIED_WITHIN_SCOPE';q['decision']['epistemic_ceiling']='VERIFIED';q['assessment_hash']=digest({k:v for k,v in q.items() if k!='assessment_hash'})
try:
 text=report(q);RESULTS.append({'id':'report-rehashed-contradictory-decision','group':'REPORT','boundary_held':False,'expected':'reject self-contradictory qualification','outcome':'PRESENTED','decision':q['decision']})
 (A/'counterexamples/report-rehashed-contradictory-decision.json').write_text(json.dumps(q,indent=2)+'\n')
except Invalid as e: RESULTS.append({'id':'report-rehashed-contradictory-decision','group':'REPORT','boundary_held':True,'outcome':'REJECTED_INVALID','reason':str(e)})
(A/'engine-results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
failed=[r['id'] for r in RESULTS if not r['boundary_held']]
print(json.dumps({'probes':len(RESULTS),'boundaries_held':len(RESULTS)-len(failed),'counterexamples':failed},indent=2))
sys.exit(bool(failed))
