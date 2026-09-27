from copy import deepcopy
import pytest
from tools.common import ROOT, catalogs, dossier_digest, load
from tools.derive import derive


@pytest.fixture
def dossier():
    return load(ROOT / 'dossiers/examples/003-callback-teardown.json')


@pytest.fixture(scope='session')
def catalog():
    return catalogs()


@pytest.fixture
def run(catalog, monkeypatch):
    def execute(d):
        competencies, invariants, oracles = deepcopy(catalog)
        # Existing 564 tests isolate downstream rules using independently issued
        # synthetic fixture authority. Provenance tests NEVER use this run fixture.
        # Preserve intentionally stale assessor bindings; issuance does not repair them.
        from source_fixtures import issue
        from tools import provenance
        if 'oracle_observations' in d:
            d, context = issue(d)
            monkeypatch.setattr(provenance, 'load_context', lambda: context)
        return derive(d, competencies[d['competency_id']], invariants, oracles)
    return execute


def rebind(d):
    for a in d['assessments']:
        a['dossier_digest'] = dossier_digest(d)
    return d


def poison(name):
    return load(ROOT / 'tests/fixtures/poisoned' / (name + '.json'))
