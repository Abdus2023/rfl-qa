#!/usr/bin/env python3
"""Validate syntax, local references and recorded evidence; does not authenticate artifacts."""
import argparse
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import (ROOT, EPISTEMIC, GATES, Invalid, catalogs, dossier_digest,
                          index, load, require, validate_schema, digest)

STRENGTH_MEANING = {'PROOF': 'ASSUMPTION_BOUND_PROOF', 'OBSERVATION': 'BOUNDED_OBSERVATION',
                    'COVERAGE': 'MEASURED_COVERAGE', 'ABSENCE_OF_EVIDENCE': 'NOT_TESTED'}


def check_evidence(record):
    validate_schema(record, 'evidence')
    require(record['establishes'] == STRENGTH_MEANING[record['strength']],
            f"{record['id']}: strength/establishes mismatch")
    if record['strength'] == 'PROOF':
        require(record['method'] in ('rustc', 'formal'), f"{record['id']}: {record['method']} cannot establish PROOF")
        require(bool(record['assumptions']), f"{record['id']}: proof needs explicit assumptions")
    if record['method'] in ('kasan', 'kcsan', 'lockdep', 'kunit', 'scheduler'):
        require(record['strength'] in ('OBSERVATION', 'COVERAGE'),
                f"{record['id']}: dynamic test is only OBSERVATION or COVERAGE")
    if record['strength'] == 'ABSENCE_OF_EVIDENCE':
        require(record['epistemic_status'] in ('OPEN', 'PROVISIONAL', 'BLOCKED'),
                f"{record['id']}: absent evidence cannot be verified")
        require(record['coverage']['executed'] == 0, f"{record['id']}: absent evidence has executions")


def refs_exist(refs, table, context):
    require(all(r in table for r in refs), f'{context}: dangling reference {set(refs) - table.keys()}')


def check_gate(record, context):
    require(not record['findings'] or record['status'] == 'BLOCKED',
            f'{context}: findings contradict PASS')
    require(record['status'] != 'BLOCKED' or bool(record['findings']),
            f'{context}: BLOCKED requires recorded findings')


def check_oracle(oracle, invariants):
    validate_schema(oracle, 'oracle')
    index(oracle['checks'])
    covered = set()
    for check in oracle['checks']:
        refs_exist(check['invariant_refs'], invariants, check['id'])
        covered.update(check['hard_gate_refs'])
    require(covered == set(oracle['hard_gate_coverage']) == set(GATES),
            f"{oracle['id']}: missing explicit hard-gate check coverage")


def validate_dossier(dossier, catalog=None):
    validate_schema(dossier, 'claim')
    competencies, invariant_catalog, oracle_catalog = catalog or catalogs()
    competency = competencies[dossier['competency_id']]
    scope = dossier['scope']
    require(scope['competencies'] == [competency['id']], 'scope competencies do not match assessed competency')
    require(scope['domains'] == [competency['domain']], 'scope domain mismatch')
    constraints = competency['scope_constraints']
    for key in ('task_classes', 'environments'):
        require(set(scope[key]) <= set(constraints[key]), f'scope {key}: extrapolation outside rubric')
    require(set(constraints['exclusions']) <= set(scope['exclusions']), 'scope: required exclusions removed')
    require(not (set(scope['environments'] + scope['task_classes']) & set(scope['exclusions'])),
            'scope includes an excluded environment/task')
    evidence = index(dossier['evidence'])
    invariants = index(dossier['invariants'])
    assessors = index(dossier['assessments'], 'assessor_id')
    refs_exist([dossier['primary_evidence_ref']], evidence, 'primary evidence')
    require(evidence[dossier['primary_evidence_ref']]['required'], 'primary evidence must be required')
    for item in evidence.values():
        check_evidence(item)
        if item['required']:
            require(set(scope['environments']) <= set(item['environments']),
                    f"{item['id']}: evidence does not cover claimed environments")
    required = competency['required_evidence']
    refs_exist(required['invariant_refs'], invariants, 'required invariants')
    for inv in invariants.values():
        refs_exist([inv['id']], invariant_catalog, 'invariant catalog')
        require(inv['class'] == invariant_catalog[inv['id']]['class'], f"{inv['id']}: class contradicts taxonomy")
        if inv['id'] in required['invariant_refs']:
            require(inv['required'], f"{inv['id']}: required invariant disabled")
        refs_exist(inv['evidence_refs'], evidence, inv['id'])
        if inv['epistemic_status'] in ('VERIFIED', 'PARTIALLY_VERIFIED'):
            require(bool(inv['evidence_refs']), f"{inv['id']}: missing invariant evidence")
        if inv['class'] == 'D' and inv['epistemic_status'] == 'VERIFIED':
            require(bool(inv['external_evidence']), f"{inv['id']}: VERIFIED Type-D requires external_evidence")
        for external in inv['external_evidence']:
            refs_exist([external['ref']], evidence, inv['id'] + ' external_evidence')
            require(external['ref'] in inv['evidence_refs'], 'external evidence not linked to invariant')
            item = evidence[external['ref']]
            require(item['method'] == external['type'], f"{inv['id']}: external evidence method mismatch")
            require(item['strength'] != 'ABSENCE_OF_EVIDENCE' and item['tier'] != 'E0', 'empty external support')
            require(external['assessor'] in assessors, 'external evidence assessor not present')
    results = index(dossier['oracle_results'], 'oracle_ref')
    require(set(results) == set(required['oracle_refs']), 'oracle references differ from required oracles')
    for oracle_id, result in results.items():
        refs_exist([oracle_id], oracle_catalog, 'oracle')
        oracle = oracle_catalog[oracle_id]
        check_oracle(oracle, invariant_catalog)
        require(oracle['competency_id'] == competency['id'], 'oracle competency mismatch')
        checks = index(result['checks'], 'check_id')
        require(set(checks) == {c['id'] for c in oracle['checks']}, f'{oracle_id}: missing/extra oracle checks')
        for check in checks.values():
            refs_exist(check['evidence_refs'], evidence, check['check_id'])
            if check['result'] != 'NOT_RUN':
                require(bool(check['evidence_refs']), f"{check['check_id']}: result without evidence")
            if check['result'] == 'PASS':
                definition = next(c for c in oracle['checks'] if c['id'] == check['check_id'])
                strengths = {evidence[r]['strength'] for r in check['evidence_refs']}
                require(set(definition['strengths']) <= strengths,
                        f"{check['check_id']}: missing required evidence strength")
    check_gate(dossier['hard_gates'], 'dossier hard gates')
    behaviors = {b['id'] for group in competency['behavior_matrix'].values() for b in group}
    for a in assessors.values():
        require(a['dossier_ref'] == dossier['qualification_id'], 'assessor dossier reference mismatch')
        require(a['dossier_digest'] == dossier_digest(dossier), 'assessors did not assess this exact raw dossier')
        obs = index(a['observations'], 'behavior_id')
        require(set(obs) <= behaviors, 'unknown behavior ID')
        for observation in obs.values():
            refs_exist(observation['evidence_refs'], evidence, observation['behavior_id'])
        refs_exist(a['evidence_refs'], evidence, 'assessor evidence')
        findings = index(a['invariant_findings'], 'invariant_ref')
        require(set(findings) == set(invariants), 'assessor must classify every invariant')
        check_gate(a['hard_gates'], 'assessor hard gates')
    # A used reference is required even if its standalone required flag is false.
    used = {r for inv in invariants.values() if inv['required'] for r in inv['evidence_refs']}
    used.update(r for a in assessors.values() for o in a['observations'] for r in o['evidence_refs'])
    for ref in used:
        require(set(scope['environments']) <= set(evidence[ref]['environments']),
                f'{ref}: referenced evidence does not cover claimed environments')
    # Different assessors may record different findings; comparison, not repair, follows.
    return competency


def validate_record(record, catalog=None):
    require(isinstance(record, dict), 'record must be an object')
    kind = record.get('record_type')
    if kind == 'dossier':
        return validate_dossier(record, catalog)
    if kind in ('evidence', 'invariant', 'oracle', 'qualification'):
        validate_schema(record, kind)
        if kind == 'evidence':
            check_evidence(record)
        if kind == 'oracle':
            check_oracle(record, (catalog or catalogs())[1])
        if kind == 'qualification':
            require(digest({k: v for k, v in record.items() if k != 'assessment_hash'}) == record['assessment_hash'],
                    'qualification hash mismatch')
            require(record['decision']['scope'] == record['scope'], 'decision scope mismatch')
        return
    definitions = {'assessment': 'claim', 'calibration_case': 'claim', 'outcome': 'claim',
                   'task': 'oracle', 'expected_observations': 'oracle', 'taxonomy': 'invariant'}
    require(kind in definitions, f'unknown record_type: {kind}')
    validate_schema(record, definitions[kind], kind)
    if kind == 'assessment':
        matches = [load(p) for p in sorted((ROOT / 'dossiers/examples').glob('*.json'))]
        matches = [d for d in matches if d['qualification_id'] == record['dossier_ref']]
        require(len(matches) == 1, 'standalone assessor: unknown or ambiguous dossier reference')
        dossier = matches[0]
        slots = [i for i, a in enumerate(dossier['assessments']) if a['assessor_id'] == record['assessor_id']]
        require(len(slots) == 1, 'standalone assessor: unknown assessor slot')
        dossier['assessments'][slots[0]] = record
        validate_dossier(dossier, catalog)
    if kind in ('task', 'expected_observations'):
        oracle_catalog = (catalog or catalogs())[2]
        refs_exist([record['oracle_ref']], oracle_catalog, kind)
        oracle = oracle_catalog[record['oracle_ref']]
        if kind == 'task':
            require(record['competency_id'] == oracle['competency_id'], 'task oracle mismatch')
        else:
            require({e['check_id'] for e in record['expectations']} == {c['id'] for c in oracle['checks']},
                    'expected observations missing checks')
    if kind == 'calibration_case':
        # No automatic causal classifier: preserve explicit attribution and rationale.
        if record['revision_required']:
            require(record['classification'] in ('ASSESSMENT_ERROR', 'ORACLE_FAILURE', 'SPECIFICATION_FAILURE'),
                    'classification does not justify automatic spec revision')


def all_records():
    """Positive fixtures only. Poisoned fixtures are validated against expected outcomes by pytest."""
    patterns = ['invariants/taxonomy.yaml', 'dossiers/**/*.json', 'dossiers/**/*.yaml', 'invariants/*/*.yaml',
                'oracles/*/*.yaml', 'labs/*/*.yaml', 'tests/fixtures/valid/*',
                'tests/fixtures/calibration/*.yaml', 'calibration/cases/*.yaml']
    return sorted({p for pattern in patterns for p in ROOT.glob(pattern) if p.is_file()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    if not args.all and not args.path:
        parser.error('provide path or --all')
    failed = False
    try:
        catalog = catalogs()
        for c in catalog[0].values():
            refs_exist(c['required_evidence']['invariant_refs'], catalog[1], c['id'])
            refs_exist(c['required_evidence']['oracle_refs'], catalog[2], c['id'])
        print('PASS competency/_schema.yaml catalog schemas and references')
    except (Invalid, KeyError, TypeError) as exc:
        print(f'FAIL catalog $ {exc}', file=sys.stderr)
        return 1
    for path in all_records() if args.all else [Path(args.path)]:
        try:
            record = load(path)
            validate_record(record, catalog)
            print(f'PASS {path} {record.get("record_type")}')
        except (Invalid, KeyError, TypeError) as exc:
            failed = True
            print(f'FAIL {path} $ {exc}', file=sys.stderr)
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
