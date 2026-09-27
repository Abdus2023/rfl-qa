"""Replay frozen audit artifacts; no writes to the audit directory."""
from copy import deepcopy
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
sys.path.insert(0,str(R))
from tools.common import catalogs,load,canonical
from tools.derive import derive
from tools.validate import validate_record
from tools.report import report
cat=catalogs();out=[]
for p in sorted((R/'evidence/adversarial-audit/counterexamples').glob('*')):
 if p.name.endswith('.result.json'):continue
 try:
  d=load(p)
  if p.name.endswith('.catalog.json'):
   c=deepcopy(cat);c[2][d['id']]=d
   d=load(R/'evidence/adversarial-audit/counterexamples/oracle-open-evidence-not-in-ceiling.json')
   q=derive(d,c[0][d['competency_id']],c[1],c[2]);kind='DERIVED'
  elif d.get('record_type')=='dossier':
   q=derive(d,cat[0][d['competency_id']],cat[1],cat[2]);kind='DERIVED'
  elif d.get('record_type')=='qualification': report(d);q=d;kind='PRESENTED'
  else:validate_record(d);q={};kind='VALIDATED'
  out.append({'counterexample':p.name,'outcome':kind,'decision':q.get('decision'),'hard_gates':q.get('hard_gates')})
 except Exception as e:out.append({'counterexample':p.name,'outcome':'REJECTED','exception':type(e).__name__,'reason':str(e)})
(E/(sys.argv[1]+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
