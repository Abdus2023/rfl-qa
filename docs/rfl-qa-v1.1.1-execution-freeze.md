# RFL-QA v1.1.1 — Execution Freeze

Agreed. The specification is sufficiently frozen to move from **design** to **execution**.

One important correction before implementation: the current text still contains a few places where the measurement model could accidentally become circular or overclaim validity. I would freeze those as **v1.1.1 clarifications**, without reopening the architecture.

## 1. Separate the three things currently called “qualification”

The repository should distinguish:

```text
DEMONSTRATION
    │
    ├── capability_level
    ├── evidence_tier
    ├── invariant findings
    └── epistemic findings
            │
            ▼
       ASSESSMENT
            │
            ▼
      QUALIFICATION
            │
            ▼
      CALIBRATION
```

A qualification is **not** simply:

```yaml
qualification: VERIFIED
```

It should identify exactly what was qualified:

```yaml
qualification:
  scope:
    competency_ids: [C047]
    domains: ["C Semantics & FFI"]

  capability:
    level: L3

  evidence:
    tier: E4

  epistemic_ceiling: PARTIALLY_VERIFIED

  hard_gates:
    status: PASS

  decision:
    status: PROVISIONAL
```

This prevents the dangerous interpretation:

> “VERIFIED qualification” = “the engineer's code is universally correct.”

It means only that **the specified capability claim satisfied the specified evidence and assessment rules within the declared scope and assumptions**.

---

## 2. `VERIFIED` must be scoped

This is the most important remaining epistemic constraint.

Suppose an engineer demonstrates:

```yaml
competency: C047
capability: L3
evidence: E4
```

That does **not** establish:

```text
L3 Rust engineer
```

It establishes something closer to:

```text
L3
for C047
under the assessed task distribution
with E4 evidence
under the recorded environments and assumptions
```

Therefore every qualification gets a **scope vector**:

```yaml
scope:
  competencies:
    - C047

  domains:
    - c_ffi

  task_classes:
    - callback_registration
    - concurrent_teardown

  environments:
    - x86_64
    - CONFIG_RUST
    - PREEMPT_RT

  exclusions:
    - dma
    - nmi_context
    - arm64
```

This makes extrapolation an explicit operation rather than an implicit one.

---

## 3. Replace “predictive validity” with measurable outcome variables

The current calibration section says the system should determine whether qualification “predicts upstream success.”

That is directionally correct but statistically underspecified.

Do **not** define:

```text
qualified → successful
unqualified → unsuccessful
```

as the oracle.

Upstream work is affected by many confounders:

* task difficulty
* subsystem maturity
* reviewer availability
* maintainer preferences
* hardware availability
* patch scope
* kernel version
* organizational constraints
* time spent on the work
* whether the engineer was working independently

Instead, record observable outcome variables.

### Outcome record

```yaml
outcome:
  qualification_ref: Q-2026-0047

  observation_window:
    start: 2026-10-01
    end: 2027-10-01

  artifacts:
    patches_submitted: 14
    patches_merged: 9
    patches_revised: 5
    patches_reverted: 0

  defect_events:
    uaf: 0
    data_race: 0
    deadlock: 0
    lifetime_regression: 0
    abi_regression: 0

  maintainer_feedback:
    safety_rewrite_required: 1
    semantic_rewrite_required: 2

  confounders:
    hardware_access: LIMITED
    reviewer_continuity: HIGH
    subsystem_churn: MEDIUM
```

Then calibration can ask precise questions instead of making a vague prediction claim.

---

## 4. “False positive” needs a stricter definition

A later bug does not automatically mean the qualification was a false positive.

For example:

```text
Qualification
     │
     ├── claim scope: C047 callback teardown
     │
     └── evidence scope: x86_64 + PREEMPT_RT
                │
                ▼
          later ARM64 DMA bug
```

That is **not necessarily** evidence that the C047 qualification failed.

The calibration engine needs:

```yaml
calibration_classification:
  - VALIDATED_WITHIN_SCOPE
  - SCOPE_EXCEEDED
  - ASSESSMENT_ERROR
  - ORACLE_FAILURE
  - SPECIFICATION_FAILURE
  - EXTERNAL_FAILURE
  - INCONCLUSIVE
```

This is critical.

Otherwise every downstream defect gets incorrectly fed back into the assessment specification.

---

## 5. The actual repository should now become executable

I would make the first implementation milestone deliberately small.

```text
RFL-QA v1.1
        │
        ▼
┌───────────────────────┐
│ Machine schemas       │
├───────────────────────┤
│ claim                 │
│ evidence              │
│ invariant             │
│ dossier               │
│ qualification         │
│ oracle                │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Deterministic engine  │
├───────────────────────┤
│ validate              │
│ derive                │
│ gate                  │
│ emit                  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ First 3 laboratories  │
├───────────────────────┤
│ Pin-init              │
│ RCU                   │
│ callback teardown     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Dual assessment       │
└───────────┬───────────┘
            │
            ▼
      CALIBRATION-001
```

Do **not** implement all 100 competencies first.

That would create a large specification before testing whether the underlying measurement machinery works.

---

## 6. First executable slice

The initial repository should therefore be:

```text
rfl-qa/
├── SPEC.md
├── GOVERNANCE.md
├── CHANGELOG.md
│
├── schemas/
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── invariant.schema.json
│   ├── oracle.schema.json
│   └── qualification.schema.json
│
├── competency/
│   ├── _schema.yaml
│   ├── C047-callback-teardown.yaml
│   ├── C0xx-pin-init.yaml
│   └── C0xx-rcu.yaml
│
├── invariants/
│   ├── taxonomy.yaml
│   ├── A-compiler/
│   ├── B-api/
│   ├── C-runtime/
│   └── D-external/
│
├── oracles/
│   ├── teardown/
│   ├── context/
│   └── ffi/
│
├── labs/
│   ├── 001-pin-init/
│   ├── 002-rcu/
│   └── 003-callback-teardown/
│
├── dossiers/
│   └── template/
│
├── assessors/
│   ├── rubric.md
│   └── review-protocol.md
│
├── calibration/
│   ├── inter-rater.md
│   └── cases/
│
└── tools/
    ├── validate.py
    ├── derive.py
    └── report.py
```

Only after this slice survives actual assessment should the competency registry expand.

---

## 7. Deterministic qualification engine

The engine should be deliberately boring.

```text
Input
 │
 ├── claim
 ├── evidence
 ├── invariant records
 ├── oracle results
 ├── hard-gate findings
 └── scope
       │
       ▼
  Schema validation
       │
       ▼
  Evidence validation
       │
       ▼
  Invariant consistency
       │
       ▼
  Hard-gate evaluation
       │
       ▼
  Capability assessment
       │
       ▼
  Epistemic ceiling
       │
       ▼
  Qualification derivation
       │
       ▼
  Immutable assessment record
```

Crucially:

```text
derive.py
```

must **never infer capability from evidence tier**.

And:

```text
report.py
```

must never silently upgrade:

```text
PARTIALLY_VERIFIED → VERIFIED
```

because of aggregate test counts.

---

## 8. Capability should itself have an evidence trail

The biggest remaining weakness in the four-dimensional record is that:

```yaml
capability:
  level: L4
```

could still become an assessor assertion.

Instead:

```yaml
capability:
  level: L4

  demonstrated_behaviors:
    - CB-047-01
    - CB-047-03
    - CB-047-07

  evidence_refs:
    - LAB-003
    - REVIEW-003
    - ARTIFACT-003

  failed_behaviors: []

  level_boundary:
    L3_satisfied: true
    L4_satisfied: true
    L5_satisfied: false
```

Now L4 is itself an auditable claim.

This produces a useful structure:

```text
Competency
   │
   ├── required behaviors
   │
   ├── L1 behaviors
   ├── L2 behaviors
   ├── L3 behaviors
   ├── L4 behaviors
   └── L5 behaviors
            │
            ▼
       Observations
            │
            ▼
        Evidence
            │
            ▼
       Capability claim
```

That is much stronger than a conventional rubric.

---

## 9. The first three labs should test the measurement system itself

They should not merely test Rust knowledge.

### LAB-001 — Pin-init

Tests:

```text
C semantics
      +
Rust initialization
      +
unsafe boundary
      +
API invariant classification
```

Primary measurement:

```text
Can the assessor distinguish
A compiler invariant
from
B API invariant
from
D external assumption?
```

### LAB-002 — RCU

Tests:

```text
RCU semantics
      +
lifetime
      +
memory ordering
      +
teardown
      +
adversarial interleavings
```

Primary measurement:

```text
Can the assessor distinguish
PROOF
from
OBSERVATION
from
COVERAGE?
```

### LAB-003 — Callback teardown

Tests:

```text
FFI
 +
callback
 +
refcount
 +
concurrent unregister
 +
final free
```

Primary measurement:

```text
Can two assessors independently
identify the same trust boundaries,
failure modes and capability level?
```

This is important because these three labs are simultaneously:

```text
candidate assessment
        +
assessor calibration
        +
specification testing
```

---

## 10. The first release gate

I would therefore define:

```text
RFL-QA v1.1-alpha
```

with only three competencies and three labs.

Release requires:

```text
SCHEMA GATE
  ✓ all examples validate

DERIVATION GATE
  ✓ deterministic results
  ✓ no E→L inference

INVARIANT GATE
  ✓ A/B/C/D classification independently represented
  ✓ epistemic status independent

ORACLE GATE
  ✓ every adversarial test has an explicit oracle

HARD-GATE TEST
  ✓ injected UAF blocks qualification
  ✓ injected race blocks qualification
  ✓ unresolved critical assumption blocks qualification

CALIBRATION GATE
  ✓ two assessors
  ✓ independent assessment
  ✓ disagreement recorded
  ✓ no silent adjudication

REPRODUCIBILITY GATE
  ✓ same dossier → same machine-derived result
```

Only then:

```text
v1.1-alpha
      ↓
calibration
      ↓
v1.1-beta
      ↓
expand competencies/labs
      ↓
v1.2
```

## The key architectural shift

The repository should now be treated as **software that measures engineering capability**, not as documentation describing engineering capability.

Therefore it gets the same discipline as the systems it evaluates:

```text
SPEC
  ↓
SCHEMA
  ↓
VALIDATOR
  ↓
ORACLE
  ↓
EXECUTION
  ↓
EVIDENCE
  ↓
DETERMINISTIC DERIVATION
  ↓
INDEPENDENT REVIEW
  ↓
CALIBRATION
  ↓
RELEASE GATE
```

And the most important new invariant is:

> **RFL-QA must never be allowed to certify itself merely because its own internal rules are internally consistent.**

Internal consistency establishes **coherence**.

Calibration establishes **measurement reliability**.

External outcome studies provide evidence about **criterion validity**.

Those are three different claims, and RFL-QA should keep them separate.
