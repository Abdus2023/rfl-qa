from copy import deepcopy
import concurrent.futures, json, os, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; A=Path(__file__).parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(A))
from run_command import run
from tools.common import Invalid,canonical,catalogs,digest,dossier_digest,load
from tools.derive import derive
from tools.validate import validate_record,validate_schema
CAT=catalogs();d=load(ROOT/'dossiers/examples/003-callback-teardown.json');results=[]

def bind(x):
 for a in x['assessments']:a['dossier_digest']=dossier_digest(x)
 return x

def result(x):return derive(x,CAT[0][x['competency_id']],CAT[1],CAT[2])
base=result(d);base_bytes=canonical(base)+b'\n'
def reverse_maps(x):
 if isinstance(x,dict):return {k:reverse_maps(v) for k,v in reversed(list(x.items()))}
 if isinstance(x,list):return [reverse_maps(v) for v in x]
 return x
with tempfile.TemporaryDirectory(prefix='rfl-audit-') as td:
 t=Path(td);json_path=t/'input.json';yaml_path=t/'input.yaml';reversed_path=t/'reversed.yaml'
 json_path.write_text(json.dumps(d));yaml_path.write_text(yaml.safe_dump(d,sort_keys=False));reversed_path.write_text(yaml.safe_dump(reverse_maps(d),sort_keys=False))
 for name,p in [('json',json_path),('yaml',yaml_path),('yaml-reversed-mapping',reversed_path)]:
  q=result(load(p));results.append({'id':name,'hash_equal':q['assessment_hash']==base['assessment_hash'],'byte_equal':canonical(q)==canonical(base)})
 envs=[{'PYTHONHASHSEED':seed,'LC_ALL':loc,'TZ':tz} for seed,loc,tz in [('0','C','UTC'),('1','C.utf8','Africa/Tunis'),('42','C','Pacific/Honolulu'),('random','C.utf8','UTC')]]
 for i,env in enumerate(envs):
  for location in [ROOT,t]:
   r=run(f'determinism-{i}-{location==ROOT}',[sys.executable,str(ROOT/'tools/derive.py'),str(reversed_path)],cwd=location,env=env)
   results.append({'id':r['label'],'exit_code':r['exit_code'],'byte_equal':r['stdout'].encode()==base_bytes,'env':env})
 def cli(n):
  return run(f'concurrent-process-{n}',[sys.executable,str(ROOT/'tools/derive.py'),str(json_path)],cwd=t,env={'PYTHONHASHSEED':str(n)})
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for r in pool.map(cli,range(8)):results.append({'id':r['label'],'exit_code':r['exit_code'],'byte_equal':r['stdout'].encode()==base_bytes})
 # JSON and YAML duplicate/scalar/tag behavior. No arbitrary code is executed.
 samples={
  'duplicate-json':('json','{"id":1,"id":2}'),
  'duplicate-yaml':('yaml','id: 1\nid: 2\n'),
  'yaml-on':('yaml','record_type: invariant\nepistemic_status: ON\n'),
  'yaml-python-tag':('yaml','!!python/object/apply:builtins.str [audit]\n'),
  'yaml-cycle':('yaml','self: &root {back: *root}\n'),
  'yaml-integer':('yaml','count: 01\n'),
  'yaml-null':('yaml','status: null\n'),
  'yaml-timestamp':('yaml','timestamp: 2026-09-27T00:00:00Z\n'),
  'yaml-benign-alias':('yaml','a: &env [x86_64]\nb: *env\n'),
  'json-deep':('json','['*1500+'0'+']'*1500),
  'yaml-deep':('yaml','['*1500+'0'+']'*1500),
 }
 for name,(ext,text) in samples.items():
  p=t/(name+'.'+ext);p.write_text(text)
  try:
   v=load(p);entry={'id':name,'loaded_type':type(v).__name__,'value':v}
   if name in ['yaml-on','yaml-null']:
    try:validate_record(v);entry['semantic']='ACCEPTED'
    except Invalid as exc:entry['semantic']='REJECTED';entry['reason']=str(exc)
   if name=='yaml-benign-alias':entry['alias_same_object']=v['a'] is v['b']
  except Exception as exc:entry={'id':name,'exception':type(exc).__name__,'reason':str(exc)}
  results.append(entry)
 # Equivalent safe YAML anchor use in an actual dossier.
 for e in d['evidence']:e['environments']=d['scope']['environments']
 p=t/'actual-alias.yaml';p.write_text(yaml.safe_dump(d,sort_keys=False))
 alias=result(load(p));results.append({'id':'actual-yaml-anchors','byte_equal':canonical(alias)==canonical(base),'contains_yaml_anchor':'&id' in p.read_text()})
 # Observe structured input errors through the CLI, not only exceptions in-process.
 for name in ['json-deep','yaml-deep','yaml-on','yaml-python-tag']:
  ext=samples[name][0]
  r=run('cli-'+name,[sys.executable,str(ROOT/'tools/validate.py'),str(t/(name+'.'+ext))],timeout=10)
  results.append({'id':'cli-'+name,'exit_code':r['exit_code'],'traceback':'Traceback' in r['stderr']})
# Changed fields must bind the hash. No time comes from the clock.
for label in ['capability','scope','epistemic','timestamp','presentation-limitations','array-order','numeric-representation']:
 x=deepcopy(d)
 if label=='capability':
  for a in x['assessments']:a['observations']=a['observations'][:2];a['claimed_level']='L2'
 elif label=='scope':x['scope']['task_classes']=x['scope']['task_classes'][:1]
 elif label=='epistemic':
  x['invariants'][1]['epistemic_status']='PROVISIONAL'
  for a in x['assessments']:a['invariant_findings'][1]['epistemic_status']='PROVISIONAL'
 elif label=='timestamp':x['timestamp']='2027-09-27T00:00:00Z'
 elif label=='presentation-limitations':x['limitations'].append('Extra explanation.')
 elif label=='array-order':x['assessments'].reverse()
 elif label=='numeric-representation':x['evidence'][0]['coverage']['executed']=1.0
 q=result(bind(x));results.append({'id':'hash-'+label,'hash_changed':q['assessment_hash']!=base['assessment_hash'],'decision_equal':q['decision']==base['decision'],'signature_equal':q['derived_signature']==base['derived_signature']})
# Direct standalone invariant validation lacks dossier-level semantics.
v=deepcopy(d['invariants'][-1]);v['external_evidence']=[];v['evidence_refs']=[]
try:validate_record(v);results.append({'id':'standalone-d-verified-no-evidence','outcome':'ACCEPTED'});(A/'counterexamples/standalone-d-verified-no-evidence.yaml').write_text(yaml.safe_dump(v))
except Invalid as exc:results.append({'id':'standalone-d-verified-no-evidence','outcome':'REJECTED','reason':str(exc)})
(A/'format-determinism-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
