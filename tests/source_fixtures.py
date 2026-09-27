"""Controlled synthetic authority issuer FOR TESTS/MIGRATION ONLY.

Provenance adversaries must call this BEFORE mutating data, and preserve the returned
independent context. Production does not import this module or issue trust grants.
"""
from copy import deepcopy
from tools.common import canonical, digest, dossier_digest
from tools.provenance import subjects, artifact_digest, RULE, PREFIX


def issue(dossier):
    d = deepcopy(dossier)
    previously_bound = [a['dossier_digest'] == dossier_digest(d) for a in d['assessments']]
    values = subjects(d)
    identity = digest(values)
    artifact = {'id': 'ART-' + identity, 'dossier_ref': d['qualification_id'],
                'content': '# Explicit synthetic source. Not human/kernel evidence.\n\n' +
                           '\n'.join(PREFIX + canonical({'subject': k, 'value': values[k]}).decode()
                                     for k in sorted(values)) + '\n'}
    artifact['digest'] = artifact_digest(artifact)
    authorizations, bindings = [], {}
    for n, subject in enumerate(sorted(values)):
        auth = {'id': f'BND-{identity}-{n:03}', 'artifact_id': artifact['id'],
                'dossier_ref': d['qualification_id'], 'subject': subject,
                'location': {'type': 'line_range', 'start': n+3, 'end': n+3}, 'rule_id': RULE}
        authorizations.append(auth)
        bindings[auth['id']] = deepcopy({k:v for k,v in auth.items() if k not in ('id', 'dossier_ref')})
        bindings[auth['id']]['artifact_digest'] = artifact['digest']
    d['source_bindings'] = bindings
    for valid, a in zip(previously_bound, d['assessments']):
        if valid:
            a['dossier_digest'] = dossier_digest(d)
    return d, {'artifacts': [artifact], 'authorizations': authorizations}
