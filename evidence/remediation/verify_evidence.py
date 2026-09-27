"""Final local checks of bounds, preservation and receipt consistency."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
import yaml
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
sys.path.insert(0,str(R))
from tools.common import load,Invalid
# Additional exact-bound controls: explicitly executed locally, not claimed as CI tests.
bounds=[]
with tempfile.TemporaryDirectory(prefix='rfl-bound-controls-') as td:
 p=Path(td)/'bound.json'
 for name,text,accepted in [('bytes-exact',' '*(2_000_000-2)+'{}',True),('bytes-over',' '*(2_000_001-2)+'{}',False),
                           ('depth-exact','['*64+'0'+']'*64,True),('depth-over','['*65+'0'+']'*65,False),
                           ('nodes-exact',json.dumps([0]*99_999),True),('nodes-over',json.dumps([0]*100_000),False)]:
  p.write_text(text)
  try:load(p);actual=True
  except Invalid:actual=False
  assert actual==accepted,name
  bounds.append({'case':name,'expected_accept':accepted,'actual_accept':actual,'result':'PASS'})
(E/'parser-boundary-results.json').write_text(json.dumps(bounds,indent=2)+'\n')
preserved=json.loads((E/'preserved-evidence.json').read_text())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in preserved.items())
base='e4f1611c245d5c001d29b5c4477dee088c3d7867'
old_tests=[p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'tests'],cwd=R,text=True).splitlines() if p.endswith('.py')]
assert all(subprocess.check_output(['git','show',base+':'+p],cwd=R)==(R/p).read_bytes() for p in old_tests)
(E/'preservation-results.json').write_text(json.dumps({'unchanged_prior_evidence_files':len(preserved),'unchanged_original_python_test_files':len(old_tests),'original_test_files':old_tests,'result':'PASS'},indent=2)+'\n')
f=yaml.safe_load((E/'findings.yaml').read_text())['findings']
assert [x['id'] for x in f]==[f'AUD-{n:03}' for n in range(1,16)]
allowed={'FIXED_AND_RETESTED','FIXED_LOCALLY_CI_PENDING','NOT_REPRODUCED','OPEN','SPECIFICATION_FAILURE','EXTERNAL_FAILURE','INCONCLUSIVE'}
assert all(x['disposition'] in allowed and x['verified_fix_claim'] is False for x in f)
r=yaml.safe_load((E/'regression-results.yaml').read_text())
assert len(r['test_cases'])==564 and r['full_suite']['original']==119 and r['full_suite']['additional']==445
assert r['release']=='BLOCKED' and len(r['final_matrix'])==19
assert len(json.loads((E/'pre-fix-counterexamples.json').read_text()))==12
assert len(json.loads((E/'post-fix-counterexamples.json').read_text()))==12
assert all(x['outcome']=='REJECTED' for x in json.loads((E/'post-fix-counterexamples.json').read_text()))
assert all(x['byte_identical'] for x in json.loads((E/'determinism-results.json').read_text()))
for p in (E/'outputs').glob('*.qualification.json'):
 assert p.read_bytes()==(E/'procedural-final'/p.name).read_bytes()
print(f'PASS: six exact parser bounds/overruns; {len(preserved)} prior evidence files and {len(old_tests)} original test files byte-unchanged; 564-case receipts, 15 dispositions, 19 gate rows, canonical output identity and counterexample counts checked. Release BLOCKED.')
