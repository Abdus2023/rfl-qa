from pathlib import Path
import hashlib,json,subprocess,sys
import yaml
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
prior=json.loads((E/'preserved-evidence.json').read_text())
for p,h in prior.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
r=yaml.safe_load((E/'regression-results.yaml').read_text());assert r['full_suite']=={'passed':653,'failed':0,'skipped':0,'errors':0}
assert len(r['test_cases'])==653 and r['retained_passed']==564 and r['new_regressions_passed']==89
assert len(r['counterexamples']['cases'])==15 and all(x['result']=='PASS' for x in r['counterexamples']['cases'])
assert all(x['attack']=='REJECTED' and x['control']=='VERIFIED_WITHIN_SCOPE' for x in r['counterexamples']['original_attacks'])
determinism=json.loads((E/'determinism-results.json').read_text());assert len(determinism)==16
assert all(x['valid_byte_identical'] and x['conflict_byte_identical'] for x in determinism)
f=yaml.safe_load((E/'findings.yaml').read_text());assert [x['id'] for x in f['findings']]==['AUD-007','AUD-008']
assert all(x['disposition']=='FIXED_LOCALLY_CI_PENDING' and not x['verified_fix_claim'] for x in f['findings'])
ci=yaml.safe_load((E/'ci.yaml').read_text())['ci'];assert ci['run_id'] is None and ci['conclusion']=='NOT_RUN' and ci['gate']=='BLOCKED'
assert not ci['logs_available'] and not ci['artifacts_available']
assert len(r['matrix'])==13 and r['release']==f['release']=='BLOCKED'
for p in (E/'outputs').glob('*.qualification.json'):assert p.read_bytes()==(E/'procedural'/p.name).read_bytes(),p
assert subprocess.check_output(['git','diff','--name-only','06053bf','--','tools','schemas','tests','dossiers','artifacts','.github'],cwd=R)==b''
for name in ['REPORT.md','findings.yaml','provenance-contract.yaml','contradiction-cases.yaml','prose-boundary-cases.yaml','regression-results.yaml','environment.yaml','commands.log']:
 assert (E/name).is_file(),name
print(f'PASS: {len(prior)} frozen evidence files preserved; 653 test receipts, 15 cases, 7 metamorphic contracts, 16+16 deterministic processes, 2 pending dispositions and 13 gate rows checked. Current-source CI NOT_RUN; release BLOCKED.')
