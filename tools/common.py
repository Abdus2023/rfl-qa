"""Strict local IO and canonical encoding shared by the three CLI entry points."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://rfl-qa.dev/schemas/'
EPISTEMIC = ('VERIFIED', 'PARTIALLY_VERIFIED', 'PROVISIONAL', 'OPEN', 'BLOCKED')
GATES = ('callback_after_free', 'double_free', 'uaf', 'data_race', 'deadlock',
         'prohibited_sleep', 'ffi_lifetime', 'critical_external_assumption',
         'required_abi_break', 'dma_ownership')
COMPETENCIES = ('C047-callback-teardown', 'C053-pin-init', 'C034-rcu-grace-periods')


class Invalid(ValueError):
    """Invalid input; never repaired or silently defaulted."""


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid(f'duplicate key: {key}')
        result[key] = value
    return result


class StrictLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    return unique_pairs([(loader.construct_object(k), loader.construct_object(v))
                         for k, v in node.value])


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)
# Dates must stay strings for JSON Schema, not implicitly become Python date objects.
StrictLoader.yaml_implicit_resolvers = {
    k: [(tag, rex) for tag, rex in v if tag != 'tag:yaml.org,2002:timestamp']
    for k, v in StrictLoader.yaml_implicit_resolvers.items()
}


def load(path):
    path = Path(path)
    try:
        require(path.stat().st_size <= 2_000_000, 'input exceeds 2 MB limit')
        text = path.read_text(encoding='utf-8')
        if path.suffix == '.json':
            def reject_constant(value):
                raise Invalid(f'non-JSON number: {value}')
            result = json.loads(text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
        else:
            result = yaml.load(text, Loader=StrictLoader)
        check_document(result)
        return result
    except (OSError, ValueError, yaml.YAMLError, RecursionError, TypeError) as exc:
        raise Invalid(f'{path}: {exc}') from exc



def check_document(value):
    """Bound parser/validator work and prohibit non-JSON keys and ambiguous numeric input."""
    stack = [(value, 0)]
    visited = 0
    while stack:
        item, depth = stack.pop()
        visited += 1
        require(depth <= 64 and visited <= 100_000, 'document depth/node limit exceeded')
        if isinstance(item, dict):
            require(all(isinstance(k, str) for k in item), 'JSON object keys must be strings')
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
        else:
            require(item is None or type(item) in (str, int, bool),
                    'unsupported scalar: integer counts required; floats/non-finite values forbidden')


def canonical(value):
    """UTF-8, sorted object keys, compact JSON, no NaN; array order is significant."""
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def dossier_digest(dossier):
    """Assessors bind to exactly the same raw dossier, excluding assessments only."""
    return digest({k: v for k, v in dossier.items() if k != 'assessments'})


@lru_cache(maxsize=1)
def schema_set():
    schemas = {p.stem.split('.')[0]: load(p) for p in sorted((ROOT / 'schemas').glob('*.json'))}
    registry = Registry()
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
    return schemas, registry


def validate_schema(value, name, definition=None):
    check_document(value)
    schemas, registry = schema_set()
    schema = schemas[name] if definition is None else {
        '$ref': BASE + name + '.schema.json#/$defs/' + definition}
    errors = sorted(Draft202012Validator(schema, registry=registry,
                                        format_checker=FormatChecker()).iter_errors(value),
                    key=lambda e: str(list(e.absolute_path)))
    if errors:
        raise Invalid('; '.join(f'{"/".join(map(str, e.absolute_path)) or "$"}: {e.message}'
                                for e in errors))


def index(items, key='id'):
    result = {}
    for item in items:
        if item[key] in result:
            raise Invalid(f'duplicate {key}: {item[key]}')
        result[item[key]] = item
    return result


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def catalogs():
    rubric_schema = load(ROOT / 'competency/_schema.yaml')
    Draft202012Validator.check_schema(rubric_schema)
    competencies = {}
    for name in COMPETENCIES:
        record = load(ROOT / 'competency' / (name + '.yaml'))
        errors = list(Draft202012Validator(rubric_schema).iter_errors(record))
        require(not errors, f'competency {name}: {[e.message for e in errors]}')
        require(record['id'] == name.split('-')[0], f'{name}: mismatched competency ID')
        behaviors = [b for group in record['behavior_matrix'].values() for b in group]
        index(behaviors)
        require(all(b['id'].startswith('CB-' + record['id'][1:] + '-') for b in behaviors),
                f'{name}: behavior belongs to another competency')
        competencies[record['id']] = record
    invariants = index([load(p) for p in sorted((ROOT / 'invariants').glob('*/*.yaml'))])
    oracles = index([load(p) for p in sorted((ROOT / 'oracles').glob('*/*.yaml'))])
    for r in invariants.values():
        validate_schema(r, 'invariant')
    for r in oracles.values():
        validate_schema(r, 'oracle')
    return competencies, invariants, oracles
