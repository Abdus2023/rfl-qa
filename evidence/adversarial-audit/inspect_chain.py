import hashlib, importlib.metadata, json, os, platform, subprocess, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; A=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from tools.common import canonical,digest

def git(*args):
 p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True)
 return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
manifest=json.loads((ROOT/'evidence/execution/source-manifest.json').read_text())
ledger=yaml.safe_load((ROOT/'evidence/execution/ledger.yaml').read_text())['execution']
source_mismatch=[p for p,h in manifest.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
log_mismatch=[c['log'] for c in ledger['commands'] if hashlib.sha256((ROOT/'evidence/execution'/c['log']).read_bytes()).hexdigest()!=c['log_sha256']]
remote='origin/arena/01a0dfcc-rfl-qa'
paths=git('ls-tree','-r','--name-only',remote)['stdout'].splitlines()
remote_mismatch=[]
for p in paths:
 r=subprocess.run(['git','show',remote+':'+p],cwd=ROOT,capture_output=True)
 if not (ROOT/p).exists() or r.stdout!=(ROOT/p).read_bytes(): remote_mismatch.append(p)
chain={'local_branch':git('branch','--show-current'),'local_revision':git('rev-parse','HEAD'),'working_tree_status':git('status','--short'),
       'remote_revision':git('rev-parse',remote),'local_is_ancestor_of_remote':git('merge-base','--is-ancestor','HEAD',remote),
       'remote_is_ancestor_of_local':git('merge-base','--is-ancestor',remote,'HEAD'),
       'claimed_source_commit':git('show','--stat','993cf96'),'claimed_evidence_commit':git('show','--stat','50512a3'),
       'actual_evidence_history':git('log','--format=%H %s',remote,'--','evidence/execution/ledger.yaml'),
       'source_files_compared':len(manifest),'source_manifest_mismatches':source_mismatch,
       'source_manifest_hash_matches_ledger':digest(manifest)==ledger['source_manifest_sha256'],
       'command_log_files_compared':len(ledger['commands']),'log_digest_mismatches':log_mismatch,
       'remote_files_compared':len(paths),'remote_content_mismatches':remote_mismatch,
       'previous_test_claim':ledger['tests'],'previous_commit_claim':ledger['commit'],
       'evidence_qualification':'Historical self-authored and internally consistent; not authenticated command execution. Independent rerun recorded separately.'}
(A/'evidence-chain.json').write_text(json.dumps(chain,indent=2)+'\n')
pins={l.split('==')[0]:l.split('==')[1] for l in (ROOT/'requirements.txt').read_text().splitlines() if '==' in l}
allow=['PYTHONHASHSEED','PYTHONPATH','PYTHONHOME','PYTEST_ADDOPTS','PYTEST_DISABLE_PLUGIN_AUTOLOAD','LANG','LC_ALL','TZ','VIRTUAL_ENV']
env={'python':sys.version,'executable':sys.executable,'os':platform.platform(),'architecture':platform.machine(),
     'revision':git('rev-parse','HEAD')['stdout'].strip(),'content_matches_remote':git('rev-parse',remote)['stdout'].strip() if not remote_mismatch else False,
     'pinned_dependencies':pins,'installed_dependencies':{p:importlib.metadata.version(p) for p in pins},
     'relevant_environment':{k:os.environ.get(k,'<unset>') for k in allow},'locales':subprocess.run(['locale','-a'],capture_output=True,text=True).stdout.splitlines(),
     'secret_environment_policy':'Only named test-related variables recorded; credentials excluded.',
     'venv_bootstrap_tools':{p:importlib.metadata.version(p) for p in ['pip','setuptools']}}
(A/'environment.yaml').write_text(yaml.safe_dump(env,sort_keys=False))
print(json.dumps(chain,indent=2))
