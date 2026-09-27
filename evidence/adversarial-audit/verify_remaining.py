import inspect,json,sys
from pathlib import Path
import yaml
from jsonschema import FormatChecker
import jsonschema._format
ROOT=Path(__file__).resolve().parents[2];A=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from tools.common import load,canonical
from tools.validate import validate_record
items=[]
checker=FormatChecker()
for value in ['2026-09-27T00:00:00Z','yesterday','2026-99-99T99:99:99Z']:
 items.append({'probe':'date-time','input':value,'conforms':checker.conforms(value,'date-time')})
items.append({'probe':'date-time-implementation','source':inspect.getsource(jsonschema._format.is_datetime)})
for name in ['001-pin-init','002-rcu','003-callback-teardown']:
 old=(ROOT/'evidence/execution'/f'{name}.qualification.json').read_bytes()
 new=(A/'reproduced-release'/f'{name}.qualification.json').read_bytes()
 items.append({'probe':'reproduced-old-qualification','lab':name,'byte_identical':old==new,'hash':json.loads(new)['assessment_hash']})
for classification in ['VALIDATED_WITHIN_SCOPE','SCOPE_EXCEEDED','ASSESSMENT_ERROR','ORACLE_FAILURE','SPECIFICATION_FAILURE','EXTERNAL_FAILURE','INCONCLUSIVE']:
 c=load(ROOT/'calibration/cases/CAL-001.yaml');c['classification']=classification
 before=canonical(c);validate_record(c)
 items.append({'probe':'outcome-classification','classification':classification,'preserved':canonical(c)==before,'revision_required':c['revision_required']})
for lab in ['001-pin-init','002-rcu','003-callback-teardown']:
 p=ROOT/'labs'/lab;o=load(p/'oracle.yaml');task=load(p/'task.yaml')
 items.append({'probe':'lab-inventory','lab':lab,'files':sorted(x.name for x in p.iterdir()),'input':task['inputs'],
               'checks':[{'id':c['id'],'predicate':c['predicate'],'strengths':c['strengths'],'invariant_refs':c['invariant_refs']} for c in o['checks']],
               'teardown_model':o['teardown_model'],'safety_predicates':o['safety_predicates']})
(A/'remaining-results.json').write_text(json.dumps(items,indent=2)+'\n')
print(json.dumps(items,indent=2))
