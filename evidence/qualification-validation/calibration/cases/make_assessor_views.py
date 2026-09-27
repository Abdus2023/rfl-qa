#!/usr/bin/env python3
"""Derive assessor-blind views of the frozen calibration case set.

Reads calibration/cases.yaml (FROZEN — never modified) and writes one assessor-facing
file per case with `expected_boundary` and `boundary_derivation` removed. Writes a
generation receipt with the frozen case-set digest and per-view digests.

Exit 0 on success; nonzero if any view is missing a required non-boundary field.
"""
import hashlib, sys
from pathlib import Path
import yaml

PKG = Path(__file__).resolve().parents[2]
CASES = PKG / 'calibration' / 'cases.yaml'
OUTDIR = PKG / 'calibration' / 'cases' / 'assessor-view'
BLIND_FIELDS = ('expected_boundary', 'boundary_derivation')
REQUIRED = ('id', 'class', 'competency_id', 'task', 'evidence_package',
            'applicable_invariants', 'applicable_oracles', 'hard_gate_conditions')

def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main():
    raw = CASES.read_bytes()
    frozen_digest = sha_bytes(raw)
    doc = yaml.safe_load(raw)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    views, problems = {}, []
    for case in doc['cases']:
        cid = case['id']
        for f in REQUIRED:
            if f not in case:
                problems.append(f'{cid}: missing required field {f}')
        if 'scoring_contract' not in case:
            problems.append(f'{cid}: missing scoring_contract')
        view = {k: v for k, v in case.items() if k not in BLIND_FIELDS}
        for f in BLIND_FIELDS:
            if f in view:
                problems.append(f'{cid}: blind field {f} leaked into assessor view')
        vb = yaml.safe_dump(view, sort_keys=False, width=100)
        (OUTDIR / f'{cid}.assessor.yaml').write_text(vb)
        views[cid] = sha_bytes(vb.encode())
    receipt = {
        'record_type': 'assessor_view_generation',
        'generated_by': 'calibration/cases/make_assessor_views.py',
        'frozen_case_set': 'evidence/qualification-validation/calibration/cases.yaml',
        'frozen_case_set_sha256': frozen_digest,
        'case_set_id': doc['case_set']['id'],
        'case_set_instrument_commit': doc['case_set']['instrument_commit'],
        'blind_fields_removed': list(BLIND_FIELDS),
        'view_count': len(views),
        'view_sha256': views,
        'frozen_source_unmodified': sha_bytes(CASES.read_bytes()) == frozen_digest,
        'status': 'PREPARED_FOR_DISTRIBUTION_DISTRIBUTION_NOT_RUN',
        'distribution_blocker': 'No independent human assessors exist in this execution environment.',
    }
    (PKG / 'calibration' / 'cases' / 'view-generation.yaml').write_text(
        yaml.safe_dump(receipt, sort_keys=False, width=100))
    print(f"views={len(views)} frozen_digest={frozen_digest[:16]} problems={problems}")
    sys.exit(1 if problems or not receipt['frozen_source_unmodified'] else 0)

if __name__ == '__main__':
    main()
