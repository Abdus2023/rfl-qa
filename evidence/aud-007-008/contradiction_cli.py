"""Controlled conflict replay process, NOT a production source-authority endpoint."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
from tools.common import load,canonical
from tools.provenance import evaluate
case=load(Path(__file__).parent/'cases/C11.json');d,ctx=case['dossier'],case['authority']
if len(sys.argv)>1 and sys.argv[1]=='reverse':
 ctx['artifacts'].reverse();ctx['authorizations'].reverse()
 d['source_bindings']=dict(reversed(list(d['source_bindings'].items())))
print(canonical(evaluate(d,ctx)).decode())
