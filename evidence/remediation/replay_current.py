from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
sys.path[:0]=[str(R),str(R/'tests')]
from test_remediation import current_provenance,verified
from tools.common import load,catalogs,Invalid
from tools.derive import derive
c,i,o=catalogs();template=load(R/'dossiers/examples/003-callback-teardown.json')
rows=[]
for p in sorted((R/'evidence/adversarial-audit/counterexamples').glob('*.json')):
 d=load(p)
 if d.get('record_type')!='dossier' or p.name.endswith('.result.json'):continue
 adapted=current_provenance(d,template)
 try:
  q=derive(adapted,c['C047'],i,o)
  rows.append({'counterexample':p.name,'migration':'synthetic template observations/bindings added; old fields retained; NOT a transcription or authentication of narrative facts','result':'ACCEPTED','decision':q['decision'],'hard_gates':q['hard_gates']})
 except Invalid as e:rows.append({'counterexample':p.name,'result':'REJECTED','reason':str(e)})
(E/'current-provenance-results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
