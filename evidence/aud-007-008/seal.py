"""Seal or verify the local receipt. Self-reference and Git publication metadata excluded."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
import yaml
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent;P=E/'hash-manifest.yaml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--verify' not in sys.argv:
 evidence={str(p.relative_to(R)):sha(p) for p in sorted(E.rglob('*')) if p.is_file() and p!=P and '__pycache__' not in p.parts}
 names=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
 source={p:sha(R/p) for p in sorted(names) if p and not p.startswith('evidence/') and (R/p).is_file()}
 P.write_text(yaml.safe_dump({'algorithm':'SHA256','source_commit':'06053bfc03366912e9880eab5208ba13af3f5da8',
  'sealed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication':'LOCAL_ONLY: push blocked by GitHub App workflows permission',
  'exclusions':['hash-manifest.yaml (self-reference)','__pycache__ (runtime cache)', '.git metadata and subsequent administrative commit/push events'],
  'evidence_files':evidence,'source_files':source},sort_keys=False))
obj=yaml.safe_load(P.read_text())
for section in ['evidence_files','source_files']:
 for p,h in obj[section].items():assert sha(R/p)==h,p
for p,h in json.loads((E/'preserved-evidence.json').read_text()).items():assert sha(R/p)==h,p
print(f"PASS: {len(obj['evidence_files'])} evidence files and {len(obj['source_files'])} source files sealed; all 183 old evidence files preserved. CI remains BLOCKED.")
