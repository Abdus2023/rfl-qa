"""Explicit one-time migration of controlled fixtures, not an input repair facility."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2];sys.path[:0]=[str(R),str(R/'tests')]
from tools.common import load,dossier_digest
from source_fixtures import issue
root=R/'artifacts/sources';root.mkdir(parents=True,exist_ok=True)
registry={'artifacts':[],'authorizations':[]};seen=set()
for p in list((R/'dossiers/examples').glob('*.json'))+list((R/'tests/fixtures/valid').glob('*.json'))+[R/'dossiers/template/dossier.yaml']:
 d,ctx=issue(load(p));p.write_text(json.dumps(d,indent=2)+'\n')
 a=ctx['artifacts'][0]
 if a['id'] in seen:continue
 seen.add(a['id']);filename=a['id']+'.md';(root/filename).write_text(a['content'])
 registry['artifacts'].append({k:v for k,v in a.items() if k!='content'}|{'file':filename})
 registry['authorizations'].extend(ctx['authorizations'])
(R/'artifacts/registry.json').write_text(json.dumps(registry,indent=2)+'\n')
d=load(R/'dossiers/examples/003-callback-teardown.json')
import yaml
for p in (R/'tests/fixtures/calibration').glob('lab003_assessor_*.yaml'):
 a=load(p);a['dossier_digest']=dossier_digest(d);p.write_text(yaml.safe_dump(a,sort_keys=False))
print(f'Migrated controlled fixtures; {len(registry["artifacts"])} explicit source artifacts. No old evidence changed.')
