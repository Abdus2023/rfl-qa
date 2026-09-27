from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2];sys.path[:0]=[str(R),str(R/'tests')]
from tools.common import load,catalogs
from tools.derive import derive
from test_remediation import current_provenance
c,i,o=catalogs();template=load(R/'dossiers/examples/003-callback-teardown.json');rows=[]
for name in ['contradictory-teardown-trace-with-pass-labels','type-d-unrelated_audit']:
 d=current_provenance(load(R/f'evidence/adversarial-audit/counterexamples/{name}.json'),template)
 q=derive(d,c['C047'],i,o)
 rows.append({'input':name,'decision':q['decision'],'hard_gates':q['hard_gates'],'attack_statement':d['evidence'][0]['statement']})
 assert q['decision']['status']=='VERIFIED_WITHIN_SCOPE'
out=Path(__file__).parent/'before.json';out.write_text(json.dumps(rows,indent=2)+'\n');print(out.read_text())
