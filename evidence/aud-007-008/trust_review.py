from pathlib import Path
import ast,hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
rows=[]
for p in sorted((R/'tools').glob('*.py')):
 text=p.read_text();tree=ast.parse(text);sites=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Call):
   name=ast.unparse(n.func)
   assert name not in ('eval','exec','__import__','pickle.load','pickle.loads','importlib.import_module'),(p,name)
   assert not any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords)
   if any(w in name for w in ['subprocess','yaml.load','read_','write_','resolve','glob','environ','importlib']):
    sites.append({'line':n.lineno,'call':ast.get_source_segment(text,n)})
 rows.append({'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'boundary_calls':sites})
(E/'trust-review.json').write_text(json.dumps(rows,indent=2)+'\n')
prior=json.loads((E/'preserved-evidence.json').read_text())
for path,h in prior.items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
files=subprocess.check_output(['git','ls-tree','-r','--name-only','92d3bba','tests'],cwd=R,text=True).splitlines()
original=[p for p in files if Path(p).name.startswith('test_') and p.endswith('.py')]
for p in original:assert subprocess.check_output(['git','show','92d3bba:'+p],cwd=R)==(R/p).read_bytes(),p
(E/'preservation-results.json').write_text(json.dumps({'prior_evidence_files_unchanged':len(prior),'prior_test_modules_unchanged':len(original),'result':'PASS'},indent=2)+'\n')
print(f'PASS: no forbidden execution calls in production AST; {len(prior)} previous evidence files and {len(original)} previous test modules byte-preserved. Existing release-runner subprocess calls reviewed separately; this is not security certification.')
