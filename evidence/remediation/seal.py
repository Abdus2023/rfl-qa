"""Seal or verify the evidence snapshot. Do not record this in the already sealed log."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
import yaml
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
manifest=E/'hash-manifest.yaml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--verify' not in sys.argv:
 files={str(p.relative_to(R)):sha(p) for p in sorted(E.rglob('*')) if p.is_file() and p!=manifest and '__pycache__' not in p.parts}
 tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
 source={p:sha(R/p) for p in sorted(tracked) if p and not p.startswith('evidence/') and (R/p).is_file()}
 obj={'algorithm':'SHA256','sealed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'source_commit':'b0582f61ae4fad99c02a262c9b27475330bd018e',
      'exclusions':['evidence/remediation/hash-manifest.yaml (self-reference)','__pycache__ (runtime cache)', '.git administrative publication metadata'],
      'scope':'Immutable receipt snapshot before evidence-only publication; source/test CI receipts identify the executed SHA explicitly.',
      'remediation_files':files,'source_files':source}
 manifest.write_text(yaml.safe_dump(obj,sort_keys=False))
obj=yaml.safe_load(manifest.read_text())
for section in ['remediation_files','source_files']:
 for p,h in obj[section].items():assert sha(R/p)==h,p
prior=json.loads((E/'preserved-evidence.json').read_text())
for p,h in prior.items():assert sha(R/p)==h,p
print(f"PASS: {len(obj['remediation_files'])} remediation files, {len(obj['source_files'])} source files sealed; {len(prior)} immutable prior evidence files preserved. Manifest self-excluded.")
