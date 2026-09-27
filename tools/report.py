#!/usr/bin/env python3
"""Present an already-derived, hash-checked record without changing any finding."""
import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Invalid, load
from tools.validate import validate_record


def report(record):
    validate_record(record)
    if record['record_type'] != 'qualification':
        raise Invalid('report requires a derived qualification, not a dossier')
    fields = [('Scope', record['scope']), ('Capability', record['capability']),
              ('Evidence tier', record['evidence_tier']), ('Evidence records', record['evidence']),
              ('Invariants', record['invariants']), ('Epistemic ceiling', record['decision']['epistemic_ceiling']),
              ('Oracle evaluations (derived)', record['oracle_evaluations']),
              ('Hard gates', record['hard_gates']), ('Assessors (raw records)', record['assessments']),
              ('Capabilities by assessor', record['capabilities_by_assessor']),
              ('Inter-rater result', record['inter_rater']), ('Decision', record['decision']),
              ('Signature', record['derived_signature']), ('Limitations', record['limitations']),
              ('Provenance', record['provenance']), ('Hash', record['assessment_hash'])]
    text = f"# Scoped qualification {record['qualification_id']}\n\n"
    text += '> This report is not universal certification or evidence of system validity.\n\n'
    for title, value in fields:
        text += f'## {title}\n\n```json\n{json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)}\n```\n\n'
    return text.rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('qualification')
    args = parser.parse_args()
    try:
        print(report(load(args.qualification)), end='')
        return 0
    except (Invalid, KeyError, TypeError) as exc:
        print(f'FAIL {args.qualification} report {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
