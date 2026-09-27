import ast,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
sys.path.insert(0,str(E));from record import run
# Additional baseline parser reproduction uses the byte-identical recorded pre-fix code,
# not a rollback/modification of current implementation or of previous evidence.
ref='e4f1611c245d5c001d29b5c4477dee088c3d7867'
old=subprocess.check_output(['git','show',ref+':tools/common.py'],cwd=R)
with tempfile.TemporaryDirectory(prefix='rfl-baseline-parser-') as td:
 t=Path(td);(t/'tools').mkdir();(t/'tools/__init__.py').write_text('');(t/'tools/common.py').write_bytes(old)
 for ext in ['json','yaml']:
  p=t/('deep.'+ext);p.write_text('['*1500+'0'+']'*1500)
  r=run('baseline-parser-'+ext,[sys.executable,'-c','from tools.common import load; load("deep.'+ext+'")'],cwd=t,env={'PYTHONPATH':str(t)})
  assert r['exit_code']!=0 and 'RecursionError' in r['stderr']
  r=run('fixed-parser-'+ext,[sys.executable,str(R/'tools/validate.py'),str(p)])
  assert r['exit_code']!=0 and 'Traceback' not in r['stderr']
# Production trust-boundary audit of changes; all subprocess use remains in the old release runner.
rows=[]
for p in sorted((R/'tools').glob('*.py')):
 text=p.read_text();tree=ast.parse(text);calls=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Call):
   name=ast.unparse(n.func)
   if name in ['eval','exec','__import__','pickle.loads','pickle.load']:
    raise AssertionError((p,name))
   if any(x in name for x in ['subprocess','yaml.load','glob','datetime','random','uuid','requests','socket','urlopen','import_module']):
    calls.append({'line':n.lineno,'call':ast.get_source_segment(text,n)})
   assert not any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords)
 rows.append({'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'boundary_sites':calls})
(E/'trust-boundary-review.json').write_text(json.dumps({'baseline_parser_commit':ref,'baseline_common_sha256':hashlib.sha256(old).hexdigest(),'production_tools':rows,'limitations':'Bounded source review and tests, not a security certification; fact authentication and kernel execution remain outside this evaluator.'},indent=2)+'\n')
preserved=json.loads((E/'preserved-evidence.json').read_text())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in preserved.items())
print(f'PASS: {len(preserved)} prior evidence files unchanged; no eval/exec/pickle/shell=True in production tools; deep-input behavior reproduced on baseline and rejected cleanly after patch.')
