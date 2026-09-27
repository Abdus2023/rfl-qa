"""Static audit inventory with source hashes/locations; not a security certification."""
import ast, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];A=Path(__file__).parent
inventory={}
for p in sorted((ROOT/'tools').glob('*.py')):
 text=p.read_text();tree=ast.parse(text);hits=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Call):
   call=ast.unparse(n.func)
   if any(x in call for x in ['eval','exec','subprocess','pickle','import_module','__import__','yaml.load','glob','rglob','datetime','environ','uuid','random','socket','requests','urlopen']):
    hits.append({'line':n.lineno,'call':ast.get_source_segment(text,n)})
  if isinstance(n,(ast.Import,ast.ImportFrom)):
   hits.append({'line':n.lineno,'import':ast.get_source_segment(text,n)})
 inventory[str(p.relative_to(ROOT))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sites':sorted(hits,key=lambda h:h['line'])}
# Mark exact tier-related code for full-path manual analysis.
tier_sites=[]
for name in ['tools/derive.py','tools/validate.py','tools/common.py']:
 for n,line in enumerate((ROOT/name).read_text().splitlines(),1):
  if any(t in line for t in ['evidence_tier',"['tier']",'capability(',"['claimed_level']"]):tier_sites.append({'file':name,'line':n,'source':line})
inventory['tier_to_capability_review']={'sites':tier_sites,'conclusion':'No tier read in capability(). Tier influences artifact consistency, divergence and E0 eligibility, not computed supported levels. Valid-case audit varies tier through all 6 levels.'}
(A/'static-review.json').write_text(json.dumps(inventory,indent=2)+'\n')
print(json.dumps(inventory,indent=2))
