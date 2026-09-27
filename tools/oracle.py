"""Fixed bounded alpha evaluators. Supplied result labels are never evaluated as truth.

These routines evaluate structured observations, not arbitrary code or actual kernel
executions. Their hashes bind the supplied facts; they do not authenticate those facts.
"""
from tools.common import digest, index, require

STATES = ('CREATE', 'REGISTER', 'ACTIVE', 'STOP', 'QUIESCE', 'CALLBACK_DRAIN',
          'REFERENCE_DRAIN', 'DESTROY', 'FREE')
CATALOG_STATES = [s.replace('_', ' ') for s in STATES]
PREDICATES = [
    'alive(reference) => object_alive',
    'callback_possible => callback_target_alive',
    'free(object) => no live reference AND no callback possible AND no RCU reader AND no registered owner',
]


def evaluate_teardown(trace):
    """Nine snapshots maximum, no loops controlled by code embedded in a dossier."""
    failures = set()
    if [s['state'] for s in trace] != list(STATES):
        failures.add('teardown_sequence')
    for step in trace:
        state = step['state']
        alive = step['object_alive']
        refs, callback = step['live_references'], step['callback_possible']
        readers, owner = step['rcu_readers'], step['registered_owner']
        if (refs or readers) and not alive:
            failures.add('uaf')
        if callback and not alive:
            failures.add('callback_after_free')
        if owner and not alive:
            failures.add('ffi_lifetime')
        if state == 'CALLBACK_DRAIN' and callback:
            failures.add('callback_after_free')
        if state == 'REFERENCE_DRAIN' and (refs or readers):
            failures.add('uaf')
        if state in ('DESTROY', 'FREE'):
            if refs or readers:
                failures.add('uaf')
            if callback:
                failures.add('callback_after_free')
            if owner:
                failures.add('ffi_lifetime')
        if alive != (state != 'FREE'):
            failures.add('object_lifecycle')
    return {'result': 'BLOCKED' if failures else 'PASS', 'findings': sorted(failures)}


def evaluate_observation(observation, check, oracle, evidence, invariant_catalog):
    payload = observation['payload']
    source_refs = sorted(set(observation['evidence_refs']) | {observation['input_ref']})
    failures = set()
    if not observation['executed']:
        outcome = 'NOT_RUN'
    else:
        for ref in source_refs:
            failures.update(evidence[ref]['detected_defects'])
        if check['predicate'] in ('safety', 'teardown'):
            result = evaluate_teardown(payload['trace'])
            failures.update(result['findings'])
        elif check['predicate'] == 'classification':
            inv = invariant_catalog[payload['invariant_ref']]
            if payload['observed_class'] != inv['class']:
                failures.add('invariant_classification')
        elif check['predicate'] == 'strength':
            actual = evidence[payload['evidence_ref']]['strength']
            if payload['observed_strength'] != actual or actual not in check['strengths']:
                failures.add('strength_classification')
        outcome = 'BLOCKED' if failures else 'PASS'
    return {
        'oracle_ref': oracle['id'], 'check_id': check['id'], 'provenance': 'DERIVED_RESULT',
        'evaluator': 'bounded-alpha-v1', 'observation_ref': observation['id'],
        'input_hash': digest({'input_ref': observation['input_ref'],
                              'artifact_ref': evidence[observation['input_ref']]['artifact_ref'],
                              'payload': payload}),
        'observation_hash': digest(observation),
        'evidence_hash': digest({r: evidence[r] for r in source_refs}),
        'oracle_hash': digest(oracle), 'result': outcome,
        'findings': sorted(failures), 'evidence_refs': source_refs,
    }


def evaluate_oracles(dossier, oracle_catalog, invariant_catalog):
    evidence = index(dossier['evidence'])
    observations = index(dossier['oracle_observations'])
    results = index(dossier['oracle_results'], 'oracle_ref')
    output = []
    for oracle_id in sorted(results):
        oracle = oracle_catalog[oracle_id]
        assertions = index(results[oracle_id]['checks'], 'check_id')
        for check in oracle['checks']:
            observation = observations[assertions[check['id']]['observation_ref']]
            output.append(evaluate_observation(observation, check, oracle, evidence, invariant_catalog))
    return output


def supporting_refs(dossier):
    """Full material closure, independent of a caller's optional-evidence labels."""
    refs = {e['id'] for e in dossier['evidence'] if e['required']}
    refs.add(dossier['primary_evidence_ref'])
    for inv in dossier['invariants']:
        if inv['required']:
            refs.update(inv['evidence_refs'])
            refs.update(e['ref'] for e in inv['external_evidence'])
    observations = index(dossier['oracle_observations'])
    for result in dossier['oracle_results']:
        for check in result['checks']:
            refs.update(check['evidence_refs'])
            o = observations[check['observation_ref']]
            refs.add(o['input_ref'])
            refs.update(o['evidence_refs'])
            if o['payload']['kind'] == 'strength':
                refs.add(o['payload']['evidence_ref'])
    for assessor in dossier['assessments']:
        refs.update(assessor['evidence_refs'])
        for observation in assessor['observations']:
            refs.update(observation['evidence_refs'])
    return refs
