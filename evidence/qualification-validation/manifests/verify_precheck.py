#!/usr/bin/env python3
"""Phase execution precheck: verify instrument freeze, phase-1 receipts, and package integrity.

Exit code 0 = all verifications PASS. Any mismatch exits 1 (STOP condition per phase protocol).
Writes manifests/freeze-verification.yaml when --write is given.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parents[3]
PKG = R / 'evidence' / 'qualification-validation'
EXPECTED_BASELINE = 'bb3970d5dfda6175e01058505ca3bbbebb9d8d10'

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=R).decode().strip()

def main():
    results, failures = [], []

    # --- Git facts (section 2) ---
    head = git('rev-parse', 'HEAD')
    remote_ref = git('ls-remote', 'origin', 'refs/heads/arena/01a0dfcc-rfl-qa').split()[0]
    status = git('status', '--porcelain') or 'CLEAN'
    tags = git('tag', '-l')
    git_facts = {
        'head': head, 'branch': git('branch', '--show-current'),
        'remote_url': git('remote', 'get-url', 'origin'),
        'remote_tip': remote_ref, 'parent_of_head': git('rev-parse', 'HEAD~1'),
        'working_tree_status': status if status == 'CLEAN' else status,
        'tag_count': len(tags.splitlines()),
        'baseline_expected': EXPECTED_BASELINE,
        'baseline_matches_remote': remote_ref == EXPECTED_BASELINE,
        'head_matches_remote': head == remote_ref,
    }
    results.append(('git_facts', git_facts))
    if not git_facts['baseline_matches_remote']:
        failures.append('remote tip != frozen baseline bb3970d')
    if git_facts['tag_count'] != 0:
        failures.append('unexpected tags exist')

    # --- Instrument freeze recomputation (section 2) ---
    import yaml
    inst = yaml.safe_load((PKG / 'instrument.yaml').read_text())
    recomputed = {}
    drift = []
    for rel, recorded in sorted(inst['instrument_files'].items()):
        p = R / rel
        if not p.is_file():
            drift.append(f'{rel}: MISSING'); continue
        actual = sha(p)
        recomputed[rel] = actual
        if actual != recorded:
            drift.append(f'{rel}: DRIFT recorded={recorded[:12]} actual={actual[:12]}')
    # directory manifest digest
    lines = '\n'.join(f'{p} {h}' for p, h in sorted(recomputed.items()))
    dir_digest = hashlib.sha256(lines.encode()).hexdigest()
    inst_check = {
        'instrument_commit_recorded': inst['instrument_commit'],
        'instrument_commit_current_head': head,
        'instrument_commit_unchanged': inst['instrument_commit'] == EXPECTED_BASELINE,
        'file_count_recorded': inst['file_count'],
        'file_count_recomputed': len(recomputed),
        'recorded_directory_manifest_digest': inst['directory_manifest_digest'],
        'recomputed_directory_manifest_digest': dir_digest,
        'directory_manifest_digest_unchanged': dir_digest == inst['directory_manifest_digest'],
        'drift': drift,
    }
    results.append(('instrument_freeze', inst_check))
    if drift:
        failures.append(f'{len(drift)} instrument file(s) drifted or missing')
    if dir_digest != inst['directory_manifest_digest']:
        failures.append('instrument directory manifest digest changed')

    # --- Phase-1 receipt hashes (section 20: previous manifests unchanged) ---
    man = yaml.safe_load((PKG / 'hash-manifest.yaml').read_text())
    receipt_drift = []
    for rel, recorded in sorted(man['receipt_files'].items()):
        p = PKG / rel
        if not p.is_file():
            receipt_drift.append(f'{rel}: MISSING'); continue
        if sha(p) != recorded:
            receipt_drift.append(f'{rel}: HASH CHANGED')
    receipt_check = {
        'phase1_receipt_files': len(man['receipt_files']),
        'phase1_receipt_drift': receipt_drift,
        'phase1_receipts_unchanged': not receipt_drift,
    }
    results.append(('phase1_receipts', receipt_check))
    if receipt_drift:
        failures.append(f'{len(receipt_drift)} phase-1 receipt file(s) changed')

    # --- Sealed prior evidence (section 20) ---
    seal = subprocess.run([sys.executable, str(R / 'evidence' / 'aud-007-008' / 'seal.py'), '--verify'],
                          cwd=R, capture_output=True, text=True)
    seal_check = {'exit_code': seal.returncode, 'stdout_tail': seal.stdout.strip().splitlines()[-1] if seal.stdout.strip() else ''}
    results.append(('sealed_prior_evidence', seal_check))
    if seal.returncode != 0:
        failures.append('sealed aud-007-008 package verification FAILED')

    verdict = 'PASS' if not failures else 'FAIL'
    doc = {'record_type': 'phase_execution_precheck', 'phase': 'empirical-validation-execution',
           'verdict': verdict, 'failures': failures, 'checks': dict(results)}
    print(json.dumps({'verdict': verdict, 'failures': failures,
                      'instrument_digest_unchanged': inst_check['directory_manifest_digest_unchanged'],
                      'phase1_receipts_unchanged': receipt_check['phase1_receipts_unchanged'],
                      'seal_exit': seal.returncode}, indent=2))
    if '--write' in sys.argv:
        out = PKG / 'manifests' / 'freeze-verification.yaml'
        out.parent.mkdir(parents=True, exist_ok=True)
        import yaml as _y
        out.write_text(_y.safe_dump(doc, sort_keys=False, width=100))
        print(f'wrote {out.relative_to(R)}')
    sys.exit(0 if not failures else 1)

if __name__ == '__main__':
    main()
