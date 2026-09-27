import hashlib,json,subprocess
from pathlib import Path
import yaml
R=Path(__file__).resolve().parents[2];A=Path(__file__).parent
old=json.loads((R/'evidence/execution/source-manifest.json').read_text())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in old.items())
remote='origin/arena/01a0dfcc-rfl-qa'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',remote],cwd=R,text=True).splitlines()
assert all((R/p).read_bytes()==subprocess.check_output(['git','show',remote+':'+p],cwd=R) for p in paths)
f=yaml.safe_load((A/'findings.yaml').read_text())['findings']
required=['ID','SEVERITY','STATUS','LOCATION','CLAIM','OBSERVATION','EVIDENCE','IMPACT','RECOMMENDED_ACTION','CLASSIFICATION']
for v in f:
 assert all(k in v for k in required)
 assert v['STATUS'] in ['PROVED','PARTIALLY_VERIFIED','PROVISIONAL','OPEN','BLOCKED']
 assert v['CLASSIFICATION'] in ['IMPLEMENTATION_DEFECT','SCHEMA_DEFECT','ORACLE_DEFECT','FIXTURE_DEFECT','SPECIFICATION_INCONSISTENCY','EVIDENCE_GAP','ENVIRONMENTAL_BLOCKER']
for line in (A/'commands.log').read_text().splitlines():
 record=json.loads(line);assert isinstance(record['exit_code'],int)
assert not any(x in (A/'commands.log').read_text() for x in ['&sig=','?signature=','&signature='])
gates=yaml.safe_load((A/'gate-results.yaml').read_text())
assert gates['release']=='BLOCKED'
assert gates['gates']['human_calibration']['audit_disposition']=='NOT_RUN'
assert gates['gates']['remote_ci']['audit_disposition']=='FAIL'
for name in ['REPORT.md','findings.yaml','environment.yaml','commands.log','gate-results.yaml']:
 assert (A/name).stat().st_size>0
probes=json.loads((A/'engine-results.json').read_text());assert len(probes)==150
assert sum(not r['boundary_held'] for r in probes)==11
print(f'PASS: {len(paths)} original published files byte-identical, including previous evidence; {len(old)} source manifest entries unchanged; {len(f)} classified findings; audit records internally consistent.')
print('No implementation or previous-evidence files modified. No assurance beyond these checks is implied.')
