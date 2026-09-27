# RFL-QA v1.1-alpha: Implementation Contract & Executable Release-Gate Plan

Execution freeze accepted.

The correct next step is to **instantiate the repository and make the release gates executable**, without adding new conceptual machinery.

I would implement the alpha in this order:

```text
schemas
  ↓
fixture dossiers
  ↓
validate.py
  ↓
competency/rubric data
  ↓
derive.py
  ↓
oracle fixtures
  ↓
dual-assessment/calibration fixtures
  ↓
report.py
  ↓
CI release-gate tests
  ↓
v1.1-alpha candidate
```

One implementation correction is necessary before writing code: the frozen specification uses both `VERIFIED/PARTIALLY_VERIFIED/...` and `PROOF/OBSERVATION/COVERAGE`. These are **different axes**, so the executable schema should preserve both rather than overload `epistemic_status`.

Likewise, the hard-gate vocabulary should have one canonical machine value (`BLOCKED`/`PASS`) rather than mixing `FAIL` and `BLOCKED`.

I would therefore treat the supplied specification as normative and make only these **schema-level consistency normalizations**, not conceptual changes.

### Alpha implementation contract

```text
Capability
    L0..L5
    ← demonstrated behaviors only

Evidence
    E0..E5
    ← artifact/evidence quality only

Invariant
    A | B | C | D
    ← where the invariant lives

Epistemic status
    VERIFIED
    PARTIALLY_VERIFIED
    PROVISIONAL
    OPEN
    BLOCKED

Evidence strength
    PROOF
    OBSERVATION
    COVERAGE
    ABSENCE_OF_EVIDENCE

Hard gate
    PASS | BLOCKED

Qualification
    PROVISIONAL
    VERIFIED_WITHIN_SCOPE
    REJECTED
```

And the critical derivation invariant becomes executable:

```text
                 evidence tier
                      │
                      │ NEVER
                      ▼
                capability level
                      ▲
                      │ ONLY
                      │
             demonstrated behaviors
                      │
                      ▼
                   rubric
```

The engine therefore has **no code path** of the form:

```python
level = int(evidence_tier[1])
```

or any equivalent indirect mapping.

### First implementation target

The repository should initially contain deterministic fixtures for at least:

```text
tests/
├── test_schema_gate.py
├── test_no_e_to_l_inference.py
├── test_type_d_requires_evidence.py
├── test_hard_gate_veto.py
├── test_epistemic_ceiling.py
├── test_strength_separation.py
├── test_inter_rater.py
├── test_determinism.py
└── fixtures/
    ├── valid/
    ├── poisoned/
    │   ├── e4_does_not_imply_l4.json
    │   ├── type_d_verified_without_external_evidence.json
    │   ├── injected_uaf.json
    │   ├── injected_race.json
    │   └── critical_assumption_open.json
    └── calibration/
        ├── lab003_assessor_a.yaml
        └── lab003_assessor_b.yaml
```

The most important test is not the happy path. It is:

```text
E4 + weak behavioral evidence
        │
        ├── must NOT → L4
        │
        └── must preserve the independently established capability level
```

followed by:

```text
HARD_GATE = BLOCKED
        │
        ▼
decision = REJECTED
signature = BLOCKED
        │
        ▼
no compensation from L/E/epistemic evidence
```

And for calibration:

```text
Assessor A ──┐
             ├── same raw dossier
Assessor B ──┘
       │
       ▼
 divergence detector
       │
 ┌─────┴─────┐
 │           │
none       disagreement
 │           │
 ▼           ▼
derive     record event
             │
             ▼
          adjudication
```

I would **not** populate the remaining ~97 competencies yet. The alpha's purpose is to discover whether this machinery actually behaves deterministically and whether independent assessors can operate it consistently.

**Execution target:** a repository that can run:

```bash
python tools/validate.py --all
python tools/derive.py dossiers/examples/...
python tools/report.py ...
pytest
```

with the seven frozen release gates represented as executable tests, producing a machine-verifiable `v1.1-alpha` release candidate rather than another specification document.
