from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json,sys,tempfile
E=Path(__file__).resolve().parent;R=E.parents[1];sys.path.insert(0,str(E));from record import run
out=E/'outputs';out.mkdir(exist_ok=True);canonical_results=[]
for d in sorted((R/'dossiers/examples').glob('*.json')):
 r=run('derive-'+d.stem,[sys.executable,str(R/'tools/derive.py'),str(d)]);assert r['exit_code']==0
 p=out/(d.stem+'.qualification.json');p.write_text(r['stdout'])
 report=run('report-'+d.stem,[sys.executable,str(R/'tools/report.py'),str(p)]);assert report['exit_code']==0
 (out/(d.stem+'.report.md')).write_text(report['stdout'])
 canonical_results.append({'dossier':d.name,'assessment_hash':json.loads(r['stdout'])['assessment_hash'],'decision':json.loads(r['stdout'])['decision'],'derive_exit':0,'report_exit':0})
expected=(out/'003-callback-teardown.qualification.json').read_text();rows=[]
with tempfile.TemporaryDirectory(prefix='aud-provenance-') as td:
 def one(n):
  env={'PYTHONHASHSEED':['0','1','42','random'][n%4],'LC_ALL':['C','C.utf8'][n%2],'TZ':['UTC','Africa/Tunis','Pacific/Honolulu'][n%3]}
  cwd=R if n%2 else Path(td)
  command=[sys.executable,str(R/'tools/derive.py'),str(R/'dossiers/examples/003-callback-teardown.json')]
  p=run('determinism-'+str(n),command,cwd=cwd,env=env)
  q=run('conflict-'+str(n),[sys.executable,str(E/'contradiction_cli.py')]+(['reverse'] if n%2 else []),cwd=cwd,env=env)
  assert p['exit_code']==q['exit_code']==0 and p['stdout']==expected
  return {'process':n,'environment':env,'cwd':str(cwd),'valid_byte_identical':True,'conflict_output':q['stdout']}
 # Independent processes, eight sequential and eight concurrently scheduled.
 rows=[one(n) for n in range(8)]
 with ThreadPoolExecutor(max_workers=4) as pool:rows+=list(pool.map(one,range(8,16)))
assert len({x['conflict_output'] for x in rows})==1
for row in rows:row['conflict_byte_identical']=True;del row['conflict_output']
(E/'determinism-results.json').write_text(json.dumps(rows,indent=2)+'\n')
(E/'canonical-results.json').write_text(json.dumps(canonical_results,indent=2)+'\n')
print('PASS: all 3 canonical derive/report pipelines; 16 independent derivation processes plus 16 independent contradiction processes, byte-identical per population.')
