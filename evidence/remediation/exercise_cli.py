"""Retain actual CLI records and 16 environment/concurrency determinism observations."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib,json,sys,tempfile
E=Path(__file__).parent;R=E.parents[1]
sys.path.insert(0,str(E));from record import run
records=[];outputs=E/'outputs';outputs.mkdir(exist_ok=True)
for d in sorted((R/'dossiers/examples').glob('*.json')):
 result=run('derive-'+d.stem,[sys.executable,'tools/derive.py',str(d)])
 assert result['exit_code']==0,result
 out=outputs/(d.stem+'.qualification.json');out.write_text(result['stdout'])
 report=run('report-'+d.stem,[sys.executable,'tools/report.py',str(out)])
 assert report['exit_code']==0,report
 (outputs/(d.stem+'.report.md')).write_text(report['stdout'])
 records.append({'dossier':str(d.relative_to(R)),'assessment_hash':json.loads(result['stdout'])['assessment_hash'],
                 'decision':json.loads(result['stdout'])['decision'],'derive_exit_code':0,'report_exit_code':0})
baseline=(outputs/'003-callback-teardown.qualification.json').read_bytes()
cmd=[sys.executable,str(R/'tools/derive.py'),str(R/'dossiers/examples/003-callback-teardown.json')]
runs=[]
with tempfile.TemporaryDirectory(prefix='rfl-remediation-') as td:
 for seed,loc,tz in [('0','C','UTC'),('1','C.utf8','Africa/Tunis'),('42','C','Pacific/Honolulu'),('random','C.utf8','UTC')]:
  for cwd in [R,Path(td)]:
   r=run(f'determinism-{seed}-{cwd==R}',cmd,cwd=cwd,env={'PYTHONHASHSEED':seed,'LC_ALL':loc,'TZ':tz})
   runs.append(r)
 def concurrent(n):return run(f'parallel-{n}',cmd,cwd=Path(td),env={'PYTHONHASHSEED':str(n)})
 with ThreadPoolExecutor(max_workers=4) as pool:runs+=list(pool.map(concurrent,range(8)))
summary=[{'label':r['label'],'exit_code':r['exit_code'],'environment':r['environment_overrides'],'byte_identical':r['stdout'].encode()==baseline,
          'assessment_hash':json.loads(r['stdout'])['assessment_hash'] if r['exit_code']==0 else None} for r in runs]
(E/'determinism-results.json').write_text(json.dumps(summary,indent=2)+'\n')
(E/'canonical-cli-results.json').write_text(json.dumps(records,indent=2)+'\n')
assert len(summary)==16 and all(r['exit_code']==0 and r['byte_identical'] for r in summary)
print('PASS: 3 canonical dossiers derived/reported; all 16 independent CLI executions byte-identical.')
