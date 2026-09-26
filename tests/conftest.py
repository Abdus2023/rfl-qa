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
def run(catalog):
    def execute(d):
        competencies, invariants, oracles = deepcopy(catalog)
        return derive(d, competencies[d['competency_id']], invariants, oracles)
    return execute


def rebind(d):
    for a in d['assessments']:
        a['dossier_digest'] = dossier_digest(d)
    return d


def poison(name):
    return load(ROOT / 'tests/fixtures/poisoned' / (name + '.json'))
