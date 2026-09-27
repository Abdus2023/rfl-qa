#!/usr/bin/env python3
"""Execute local alpha gates and retain evidence. Never self-authorizes human calibration."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT, canonical, digest
import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/execution')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    status = subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True)
    sources = []
    for name in ['tools','schemas','competency','invariants','oracles','labs','dossiers',
                 'assessors','calibration','tests','artifacts','.github']:
        sources.extend(p for p in (ROOT/name).rglob('*') if p.is_file() and
                       '__pycache__' not in p.parts and '.pytest_cache' not in p.parts)
    sources.extend(ROOT/name for name in ['SPEC.md','GOVERNANCE.md','CHANGELOG.md','requirements.txt','pytest.ini','.gitignore'])
    manifest = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(set(sources)) if p.exists()}
    (output/'source-manifest.json').write_bytes(canonical(manifest)+b'\n')
    commands = []
    python = sys.executable
    def run(label, command, stdout_file=None):
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, cwd=ROOT, capture_output=True)
        log = output/(label+'.log')
        log.write_bytes(b'$ '+shlex.join(command).encode()+b'\nSTDOUT:\n'+result.stdout+b'\nSTDERR:\n'+result.stderr+
                        f'\nEXIT_CODE: {result.returncode}\n'.encode())
        if stdout_file:
            (output/stdout_file).write_bytes(result.stdout)
        record = {'command':shlex.join(command),'timestamp':started,'exit_code':result.returncode,
                  'result':'PASS' if result.returncode==0 else 'FAIL','log':log.name,
                  'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
        commands.append(record)
        return record['result']
    gates = {}
    run('dependencies',[python,'-m','pip','check'])
    gates['schema']=run('schema',[python,'tools/validate.py','--all'])
    groups = {
        'derivation':['tests/test_no_e_to_l_inference.py','tests/test_epistemic_ceiling.py'],
        'invariant':['tests/test_type_d_requires_evidence.py','tests/test_strength_separation.py'],
        'oracle':['tests/test_oracle_gate.py'],
        'aud_007_provenance':['tests/test_source_provenance.py'],
        'aud_008_prose_authority':['tests/test_source_provenance.py','-k','negative_space_prose or no_inference'],
        'hard_gate':['tests/test_hard_gate_veto.py'],
        'calibration_automated':['tests/test_inter_rater.py','tests/test_outcomes.py'],
        'reproducibility':['tests/test_determinism.py'],
    }
    for name, files in groups.items():
        gates[name]=run(name,[python,'-m','pytest','-q',*files])
    run('tests',[python,'-m','pytest','-q','--junitxml='+str(output/'pytest.xml')])
    for lab in ['001-pin-init','002-rcu','003-callback-teardown']:
        run('derive-'+lab,[python,'tools/derive.py',f'dossiers/examples/{lab}.json'],lab+'.qualification.json')
        run('report-'+lab,[python,'tools/report.py',str(output/(lab+'.qualification.json'))],lab+'.report.md')
    # Real assessor independence is a procedural fact, not something a fixture can assert.
    gates['calibration']='BLOCKED'
    counts={'passed':0,'failed':0,'skipped':0,'errors':0}
    if (output/'pytest.xml').exists():
        suite = ET.parse(output/'pytest.xml').getroot()
        for case in suite.iter('testcase'):
            if case.find('failure') is not None: counts['failed']+=1
            elif case.find('error') is not None: counts['errors']+=1
            elif case.find('skipped') is not None: counts['skipped']+=1
            else: counts['passed']+=1
    dependencies = {line.split('==')[0]:importlib.metadata.version(line.split('==')[0])
                    for line in (ROOT/'requirements.txt').read_text().splitlines() if '==' in line}
    ci_run = (f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
              if os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('GITHUB_RUN_ID') else None)
    ledger={'execution':{'commit':commit,'timestamp':datetime.now(timezone.utc).isoformat(),
                         'source_manifest_sha256':digest(manifest),'worktree_status_at_start':status.splitlines(),
                         'environment':platform.platform(),'python':sys.version,'executable':python,
                         'dependencies':dependencies,'commands':commands,'gates':gates,'tests':counts,
                         'ci':'BLOCKED' if ci_run else 'NOT_RUN','ci_run_url':ci_run,'human_calibration':'BLOCKED','release_status':'BLOCKED',
                         'limitations':['Local execution only; CI authority requires actual remote run evidence.',
                                        'Synthetic assessor records do not establish independent human calibration.',
                                        'No kernel tests or upstream outcome studies executed.']}}
    (output/'ledger.yaml').write_text(yaml.safe_dump(ledger,sort_keys=False))
    e=ledger['execution']
    lines=['# RFL-QA v1.1-alpha EXECUTION REPORT','',f'Repository: `Abdus2023/rfl-qa`',
           f'Commit at execution: `{commit}`', f'Source snapshot: `source-manifest.json` (SHA-256 `{digest(manifest)}`)',
           '',f'Environment: `{e["environment"]}`',f'Python: `{platform.python_version()}`',
           'Dependencies: pinned in `requirements.txt`; installed versions recorded in `ledger.yaml`.','',
           '| Gate | Status | Executed evidence |','|---|---|---|']
    for name in ['schema','derivation','invariant','oracle','hard_gate','aud_007_provenance','aud_008_prose_authority','calibration','reproducibility']:
        evidence = ('`calibration_automated.log`: synthetic comparison tests only; independent human run unavailable'
                    if name=='calibration' else f'`{name}.log`')
        lines.append(f'| {name.upper()} | **{gates[name]}** | {evidence} |')
    lines.extend(['',f'Tests: **{counts["passed"]} passed**, {counts["failed"]} failed, {counts["errors"]} errors, {counts["skipped"]} skipped. See `tests.log` and `pytest.xml`.',
                  '', '## Reproduction and records','',
                  'The determinism test executed 100 full in-process derivations and two CLI derivations. Each of the three lab examples was derived and reported; canonical qualification records and readable reports are retained here. Input scopes and epistemic states remain unchanged.',
                  '', 'The source manifest binds the actual executed files, independently of pre-existing unrelated worktree changes. Raw stdout/stderr and exit codes are retained, including valid rejected-decision tests. Logs demonstrate only their declared populations.',
                  '', '## Known limitations and OPEN findings','',
                  '- **Human calibration BLOCKED:** only synthetic fixture assessors were available; no independent human measurements or adjudication were performed.',
                  (f'- **CI release gate BLOCKED:** current run {ci_run}; consult GitHub for the final job result.' if ci_run else '- **Remote CI NOT_RUN:** local commands have executed; workflow existence is not CI execution evidence.'),
                  '- **No real kernel runs:** no Rust/compiler/sanitizer/hardware execution or actual candidate artifact review. Structured fixture results are not kernel safety proof.',
                  '- **External authenticity OPEN:** scoped content integrity and authorization are checked against the explicit registry; producer honesty, source-audit adequacy and actual human independence remain unestablished.',
                  '- **Outcome attribution OPEN:** causal classifications require reviewed scope/confounder evidence; no downstream bug is automatically a false positive or validation.',
                  '- **Criterion validity OPEN:** no longitudinal upstream data. Hash consistency is not authenticity or empirical validity.',
                  '- See `GOVERNANCE.md` for recorded vocabulary/sample-code contradictions and their limited treatment.',
                  '', '## Release status: BLOCKED','',
                  'No tag or release created. Mandatory independent calibration and remote CI evidence are missing. Machine checks do not certify the system itself.'])
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'gates':gates,'tests':counts,'release_status':'BLOCKED','report':str(output/'REPORT.md')},indent=2))
    return 1  # mandatory procedural gate not completed; never an implicit release approval


if __name__=='__main__':
    sys.exit(main())
