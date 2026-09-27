"""Authorized exact-slice extraction. Content integrity is NOT real-world truth.

The trusted registry is deployment configuration, never supplied inside a dossier.
Only rfl-json-fact-v1 capsules at explicitly granted selectors have authority.
"""
from copy import deepcopy
import json
from tools.common import ROOT, Invalid, canonical, check_document, digest, index, load, require, unique_pairs, validate_schema

RULE = 'rfl-json-fact-v1'
PREFIX = 'RFL-QA-FACT '


def artifact_digest(artifact):
    return digest({'artifact_id': artifact['id'], 'dossier_ref': artifact['dossier_ref'],
                   'content': artifact['content']})


def load_context():
    """Read ONLY registry-authorized local files. No glob, URL, cwd or env authority."""
    registry = load(ROOT / 'artifacts/registry.json')
    validate_schema(registry, 'source')
    root = ROOT / 'artifacts/sources'
    require(not root.is_symlink(), 'source root cannot be a symlink')
    artifacts, size = [], 0
    for entry in registry['artifacts']:
        path = root / entry['file']
        require(not path.is_symlink() and path.resolve().parent == root.resolve(), 'source path outside registry root')
        content = None
        try:
            require(path.stat().st_size <= 2_000_000, 'source artifact size limit exceeded')
            with path.open('rb') as stream:
                raw = stream.read(2_000_001)
            require(len(raw) <= 2_000_000, 'source artifact size limit exceeded')
            size += len(raw)
            require(size <= 2_000_000, 'source collection size limit exceeded')
            content = raw.decode('utf-8')
        except (OSError, UnicodeError):
            pass  # Explicitly unavailable below; never fall back to submitted values.
        artifacts.append({'id': entry['id'], 'dossier_ref': entry['dossier_ref'],
                          'digest': entry['digest'], 'content': content})
    return {'artifacts': artifacts, 'authorizations': registry['authorizations']}


def subjects(d):
    """Closed qualification-input projection; no arbitrary pointer/expression engine."""
    result = {'claim': {k: d[k] for k in ('qualification_id', 'competency_id', 'fixture_kind', 'primary_evidence_ref')},
              'scope': d['scope'], 'hard_gates': d['hard_gates']}
    for field, prefix in [('evidence', 'evidence'), ('invariants', 'invariant'), ('oracle_observations', 'oracle')]:
        for item in d[field]:
            result[prefix + ':' + item['id']] = deepcopy(item)
    for a in d['assessments']:
        # Digest is a circular record binding, not source truth. Limitations are non-authoritative prose.
        result['assessment:' + a['assessor_id']] = {k: v for k, v in a.items()
                                                  if k not in ('dossier_digest', 'limitations')}
    return result


def extract(artifact, authorization):
    """One declared line, exact capsule grammar. Unknown/malformed text provides nothing."""
    location = authorization['location']
    if location['start'] != location['end']:
        return None
    lines = artifact['content'].splitlines()
    n = location['start']
    if n > len(lines) or not lines[n - 1].startswith(PREFIX):
        return None
    try:
        def reject_constant(value):
            raise Invalid('nonfinite extraction value')
        value = json.loads(lines[n - 1][len(PREFIX):], object_pairs_hook=unique_pairs,
                           parse_constant=reject_constant)
        check_document(value)
        if not isinstance(value, dict) or set(value) != {'subject', 'value'}:
            return None
        if value['subject'] != authorization['subject']:
            return None
        return value  # Wrapper distinguishes an extracted JSON null from no extraction.
    except (ValueError, TypeError, RecursionError):
        return None


def evaluate(dossier, context):
    """Pure, deterministic fail-closed evaluation of independently supplied authority."""
    validate_schema(context, 'source', 'context')
    require(sum(len((a['content'] or '').encode('utf-8')) for a in context['artifacts']) <= 2_000_000,
            'source collection size limit exceeded')
    artifacts = index(context['artifacts'])
    authorizations = index(context['authorizations'])
    expected = subjects(dossier)
    bindings = dossier['source_bindings']
    rows, extracted = {}, {}
    required = {key: auth for key, auth in authorizations.items()
                if auth['dossier_ref'] == dossier['qualification_id']}
    # Detect duplicate/overlapping grants instead of giving repeated sources extra weight.
    scopes = set()
    for key, auth in sorted(required.items()):
        scope = (auth['artifact_id'], auth['location']['start'], auth['location']['end'])
        require(scope not in scopes, 'duplicate authorized source scope')
        scopes.add(scope)
    for key in sorted(set(bindings) | set(required)):
        binding, auth = bindings.get(key), authorizations.get(key)
        subject = auth['subject'] if auth else binding['subject']
        row = {'binding_id': key, 'subject': subject, 'states': [],
               'binding_digest': digest(binding), 'value_digest': digest(expected.get(subject)),
               'source_digest': None}
        failures = set()
        if binding is None:
            failures.add('UNBOUND')
        if auth is None:
            failures.add('UNBOUND')
        elif key not in required:
            failures.add('INVALID_BINDING')
        if auth:
            if binding and any(binding[k] != auth[k] for k in ('artifact_id', 'subject', 'location', 'rule_id')):
                failures.add('INVALID_BINDING')
            location = auth['location']
            if location['start'] != location['end']:
                failures.add('INVALID_BINDING')
            artifact = artifacts.get(auth['artifact_id'])
            if artifact is None or artifact['content'] is None:
                failures.add('UNVERIFIABLE')
            else:
                actual = artifact_digest(artifact)
                row['source_digest'] = actual
                if (artifact['dossier_ref'] != dossier['qualification_id'] or actual != artifact['digest'] or
                        (binding and binding['artifact_digest'] != actual)):
                    failures.add('INVALID_BINDING')
                value = extract(artifact, auth)
                if value is None:
                    failures.add('UNVERIFIABLE')
                else:
                    # A difference is diagnostic even for stale pins; NEVER positive support in that case.
                    raw = canonical(value['value'])
                    extracted.setdefault(subject, []).append((key, raw))
                    if subject not in expected or raw != canonical(expected[subject]):
                        failures.add('CONTRADICTED')
        row['states'] = sorted(failures) or ['SUPPORTED']
        rows[key] = row
    for subject in sorted(set(expected) - {a['subject'] for a in required.values()}):
        key = 'UNBOUND:' + subject
        rows[key] = {'binding_id': key, 'subject': subject, 'states': ['UNBOUND'],
                     'binding_digest': digest(None), 'value_digest': digest(expected[subject]), 'source_digest': None}
    for group in extracted.values():
        if len({raw for _, raw in group}) > 1:
            for key, _ in group:
                rows[key]['states'] = sorted((set(rows[key]['states']) - {'SUPPORTED'}) | {'CONTRADICTED'})
    result = {'status': 'PASS' if all(r['states'] == ['SUPPORTED'] for r in rows.values()) else 'BLOCKED',
              'bindings': [rows[k] for k in sorted(rows)]}
    validate_schema(result, 'source', 'result')
    return result


def enforce(dossier, context):
    result = evaluate(dossier, context)
    require(result['status'] == 'PASS', 'provenance gate BLOCKED: ' + canonical(result).decode())
    return result
