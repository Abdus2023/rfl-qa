#!/usr/bin/env python3
"""Pure qualification derivation from validated records and explicitly supplied catalog data."""
import argparse
from copy import deepcopy
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import (EPISTEMIC, Invalid, canonical, catalogs, digest, index, load,
                          validate_schema)
from tools.validate import validate_dossier

from tools.oracle import supporting_refs, evaluate_oracles

RULES_VERSION = '1.1-alpha.3'


def capability(assessment, competency, evidence):
    """Cumulative behavior requirements only. Evidence TIER never enters level selection.

    References must exist (validator). Observations with no executed/proved support
    cannot demonstrate behavior. No reading of evidence_tier or claimed_level here.
    """
    demonstrated, failed, refs = set(), set(), set()
    for observation in assessment['observations']:
        refs.update(observation['evidence_refs'])
        if observation['status'] == 'FAILED':
            failed.add(observation['behavior_id'])
        elif all(evidence[r]['strength'] != 'ABSENCE_OF_EVIDENCE' and
                 evidence[r]['epistemic_status'] not in ('OPEN', 'BLOCKED')
                 for r in observation['evidence_refs']):
            demonstrated.add(observation['behavior_id'])
    level, required = 0, set()
    boundaries = {'L0_satisfied': True}
    for number in range(1, 6):
        required.update(b['id'] for b in competency['behavior_matrix'][f'L{number}'])
        satisfied = required <= demonstrated and not (required & failed)
        boundaries[f'L{number}_satisfied'] = satisfied
        if satisfied:
            level = number
    return {'level': f'L{level}', 'demonstrated_behaviors': sorted(demonstrated),
            'failed_behaviors': sorted(failed), 'level_boundary': boundaries,
            'evidence_refs': sorted(refs)}


def comparison(dossier, capabilities):
    """Exact agreement for auto-issuance; preserve raw inputs; never average or adjudicate."""
    a, b = dossier['assessments']
    differences = []
    def compare(label, left, right):
        if left != right:
            differences.append(label)
    compare('claimed_level', a['claimed_level'], b['claimed_level'])
    compare('behavior_findings', sorted((o['behavior_id'], o['status']) for o in a['observations']),
            sorted((o['behavior_id'], o['status']) for o in b['observations']))
    compare('supported_level', capabilities[0]['capability']['level'], capabilities[1]['capability']['level'])
    for key in ('evidence_tier', 'hard_gates'):
        compare(key, a[key], b[key])
    for assessor in (a, b):
        compare(f"{assessor['assessor_id']}:hard_gates_vs_dossier", assessor['hard_gates'], dossier['hard_gates'])
        evidence = index(dossier['evidence'])
        compare(f"{assessor['assessor_id']}:tier_vs_artifact", assessor['evidence_tier'],
                evidence[dossier['primary_evidence_ref']]['tier'])
        recorded = {i['id']: (i['class'], i['epistemic_status']) for i in dossier['invariants']}
        findings = {i['invariant_ref']: (i['class'], i['epistemic_status']) for i in assessor['invariant_findings']}
        compare(f"{assessor['assessor_id']}:invariant_findings_vs_dossier", recorded, findings)
    return sorted(differences)


def derive(dossier, competency, invariant_catalog, oracle_catalog, source_context=None):
    """No clock, network, random values or writes. Optional authority snapshot is a trusted caller input; otherwise load the fixed repository registry."""
    from tools import provenance
    source_context = provenance.load_context() if source_context is None else source_context
    validate_dossier(dossier, ({competency['id']: competency}, invariant_catalog, oracle_catalog), source_context)
    authentication = provenance.enforce(dossier, source_context)
    d = deepcopy(dossier)
    evidence = index(d['evidence'])
    capabilities = [{'assessor_id': a['assessor_id'], 'capability': capability(a, competency, evidence)}
                    for a in d['assessments']]
    differences = comparison(d, capabilities)
    # Required closure: explicit required evidence, required invariants and behavior trail.
    required_refs = supporting_refs(d)
    statuses = []
    findings = set(d['hard_gates']['findings'])
    for item in evidence.values():
        findings.update(item['detected_defects'])
    for inv in d['invariants']:
        if inv['required']:
            statuses.append(inv['epistemic_status'])
            required_refs.update(inv['evidence_refs'])
        if invariant_catalog[inv['id']]['critical'] and invariant_catalog[inv['id']]['class'] == 'D' and inv['epistemic_status'] != 'VERIFIED':
            findings.add('critical_external_assumption')
    for assessor in d['assessments']:
        findings.update(assessor['hard_gates']['findings'])
        for inv in assessor['invariant_findings']:
            original = next(i for i in d['invariants'] if i['id'] == inv['invariant_ref'])
            if original['required']:
                statuses.append(inv['epistemic_status'])
            if invariant_catalog[original['id']]['critical'] and invariant_catalog[original['id']]['class'] == 'D' and inv['epistemic_status'] != 'VERIFIED':
                findings.add('critical_external_assumption')
        for observation in assessor['observations']:
            required_refs.update(observation['evidence_refs'])
    statuses.extend(evidence[r]['epistemic_status'] for r in sorted(required_refs))
    # Weakest declared required finding wins. Counts and E tiers never alter this order.
    ceiling = max(statuses, key=EPISTEMIC.index)
    checks_complete = True
    evaluations = evaluate_oracles(d, oracle_catalog, invariant_catalog)
    for evaluation in evaluations:
        if evaluation['result'] == 'BLOCKED':
            findings.update(evaluation['findings'])
            findings.add('oracle:' + evaluation['check_id'])
        if evaluation['result'] == 'NOT_RUN':
            checks_complete = False
    for result in d['oracle_results']:
        oracle_checks = index(oracle_catalog[result['oracle_ref']]['checks'])
        for check in result['checks']:
            if check['result'] == 'BLOCKED':
                findings.update(oracle_checks[check['check_id']]['hard_gate_refs'])
                findings.add('oracle:' + check['check_id'])
            if check['result'] == 'NOT_RUN':
                checks_complete = False
    tier = evidence[d['primary_evidence_ref']]['tier']
    supported = None if differences else capabilities[0]['capability']
    if findings:
        status, signature = 'REJECTED', 'BLOCKED'
    elif ceiling == 'BLOCKED' or tier == 'E0':
        status, signature = 'REJECTED', 'BLOCKED'
    elif differences:
        status, signature = 'PROVISIONAL', 'AWAITING_ADJUDICATION'
    else:
        status = ('VERIFIED_WITHIN_SCOPE' if ceiling == 'VERIFIED' and checks_complete
                  and supported['level'] != 'L0' else 'PROVISIONAL')
        signature = f"{supported['level']}-{tier}-{competency['id']}-{ceiling}"
    limitations = list(d['limitations'])
    if d['fixture_kind'] == 'synthetic':
        limitations.append('Synthetic fixture: not a real candidate qualification or human calibration.')
    if differences:
        limitations.append('Automatic qualification halted pending explicit adjudication; no capability average.')
    if not checks_complete:
        limitations.append('Required oracle checks NOT_RUN; no verified decision permitted.')
    events = []
    if differences:
        events.append({'id': 'CAL-' + digest({'dossier': d, 'differences': differences})[:16],
                       'classification': 'artifact_ambiguity', 'differences': differences,
                       'adjudication_status': 'OPEN',
                       'rationale': 'Conflicting assessment records. Cause unresolved; not an automatic specification failure.'})
    output = {'record_type': 'qualification', 'schema_version': d['schema_version'],
              'qualification_id': d['qualification_id'], 'timestamp': d['timestamp'],
              'derivation_input': deepcopy(d), 'oracle_evaluations': evaluations,
              'source_authentication': authentication,
              'scope': d['scope'], 'capability': supported, 'evidence': d['evidence'],
              'evidence_tier': tier, 'invariants': d['invariants'],
              'hard_gates': {'status': 'BLOCKED' if findings else 'PASS', 'findings': sorted(findings)},
              'assessments': d['assessments'], 'capabilities_by_assessor': capabilities,
              'inter_rater': {'agreement': not differences, 'automatic_qualification_halted': bool(differences),
                              'events': events},
              'decision': {'status': status, 'epistemic_ceiling': ceiling, 'scope': deepcopy(d['scope'])},
              'derived_signature': signature, 'limitations': limitations,
              'provenance': {'rules_version': RULES_VERSION, 'input_sha256': digest(d),
                             'rubric_sha256': digest(competency),
                             'invariant_catalog_sha256': digest(invariant_catalog),
                             'oracles_sha256': digest({key: oracle_catalog[key] for key in
                                                      competency['required_evidence']['oracle_refs']})}}
    # Hash ALL output fields except assessment_hash. Explicit input timestamp is included.
    output['assessment_hash'] = digest(output)
    validate_schema(output, 'qualification')
    return output


def derive_from_path(path):
    dossier = load(path)
    competencies, invariants, oracles = catalogs()
    # Validate before indexing so malformed dossiers return a useful validation error.
    validate_dossier(dossier, (competencies, invariants, oracles))
    return derive(dossier, competencies[dossier['competency_id']], invariants, oracles)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dossier')
    args = parser.parse_args()
    try:
        output = derive_from_path(args.dossier)
        print(canonical(output).decode())
        # Valid rejected decisions are legitimate results, not validator errors.
        return 0
    except (Invalid, KeyError, TypeError) as exc:
        print(f'FAIL {args.dossier} derivation {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
