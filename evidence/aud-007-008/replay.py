"""Independent post-fix replay; authority is frozen before observation mutations."""
from pathlib import Path
from copy import deepcopy
import json,sys
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent;sys.path[:0]=[str(R),str(R/'tests')]
from tools.common import load,canonical,Invalid,catalogs
from tools.derive import derive
from tools.provenance import evaluate
from test_remediation import current_provenance
from provenance_cases import case,rebind
from source_fixtures import issue
c,i,o=catalogs()
def execute(d,ctx):return derive(d,c[d['competency_id']],i,o,source_context=ctx)
rows=[];directory=E/'cases';directory.mkdir(exist_ok=True)
for spec in load(E/'contradiction-cases.yaml')['cases']:
 d,ctx=case(spec['id']);p=directory/(spec['id']+'.json');p.write_text(json.dumps({'dossier':d,'authority':ctx},sort_keys=True,indent=2)+'\n')
 r=evaluate(d,ctx);actual={s for x in r['bindings'] for s in x['states']}
 assert set(spec['states'])<=actual
 try:q=execute(d,ctx);outcome=q['decision']['status']
 except Invalid:outcome='REJECTED'
 assert (outcome=='REJECTED')==(spec['derive']=='REJECTED')
 rows.append({'id':spec['id'],'expected':spec,'states':sorted(actual),'outcome':outcome,'result':'PASS'})
oldrows=[];template=load(R/'dossiers/examples/003-callback-teardown.json')
for name in ['contradictory-teardown-trace-with-pass-labels','type-d-unrelated_audit']:
 bad=current_provenance(load(R/f'evidence/adversarial-audit/counterexamples/{name}.json'),template)
 # Only repair the attacked textual source identity/statement for the positive source control.
 # Keep all VERIFIED statuses, labels and original check payloads, isolating the old attack.
 control=deepcopy(bad)
 for e in control['evidence']:
  t=next(x for x in template['evidence'] if x['id']==e['id'])
  for field in ['statement','artifact_ref']:e[field]=t[field]
 control,ctx=issue(rebind(control));positive=execute(control,ctx)
 assert positive['decision']['status']=='VERIFIED_WITHIN_SCOPE'
 bad['source_bindings']=deepcopy(control['source_bindings']);rebind(bad)
 result=evaluate(bad,ctx)
 assert 'CONTRADICTED' in {s for row in result['bindings'] for s in row['states']}
 try:execute(bad,ctx)
 except Invalid:outcome='REJECTED'
 else:raise AssertionError('original attack still accepted')
 (directory/(name+'.json')).write_text(json.dumps({'dossier':bad,'authority':ctx},sort_keys=True,indent=2)+'\n')
 oldrows.append({'input':name,'control':positive['decision']['status'],'attack':outcome,
                 'conflicts':[row for row in result['bindings'] if row['states']!=['SUPPORTED']]})
(E/'replay-results.json').write_text(json.dumps({'cases':rows,'original_attacks':oldrows},indent=2)+'\n')
print('PASS: 15/15 contracted cases; both original attacks reject against independent pre-mutation authority; both paired controls qualify synthetically.')
