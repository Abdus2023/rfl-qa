This is the definitive execution freeze. The paradigm has shifted from *describing* engineering capability to *building the software that measures it*.

Per the v1.1.1 Execution Freeze, all conceptual expansion is halted. The following artifacts constitute the **RFL-QA v1.1-alpha** release candidate. This is the minimal, executable slice required to validate the measurement machinery before scaling to the full 100-competency registry.

---

# RFL-QA v1.1-alpha: Executable Artifacts

## 1. Core Schemas (Machine-Readable Validation)

### `schemas/qualification.schema.json`
Enforces the 4D claim model, strict scoping, and the absolute separation of Capability and Evidence.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://rfl-qa.dev/schemas/qualification.schema.json",
  "title": "RFL Qualification Record",
  "type": "object",
  "required": ["qualification_id", "scope", "demonstration", "assessment", "decision"],
  "properties": {
    "qualification_id": { "type": "string", "pattern": "^Q-\\d{4}-\\d{4}$" },
    "timestamp": { "type": "string", "format": "date-time" },
    "scope": {
      "type": "object",
      "required": ["competencies", "domains", "environments", "exclusions"],
      "properties": {
        "competencies": { "type": "array", "items": { "type": "string" } },
        "domains": { "type": "array", "items": { "type": "string" } },
        "task_classes": { "type": "array", "items": { "type": "string" } },
        "environments": { "type": "array", "items": { "type": "string" } },
        "exclusions": { "type": "array", "items": { "type": "string" } }
      }
    },
    "demonstration": {
      "type": "object",
      "description": "What the candidate actually produced",
      "properties": {
        "capability_level": { "type": "integer", "minimum": 0, "maximum": 5 },
        "evidence_tier": { "type": "string", "enum": ["E0", "E1", "E2", "E3", "E4", "E5"] },
        "demonstrated_behaviors": { "type": "array", "items": { "type": "string" } },
        "failed_behaviors": { "type": "array", "items": { "type": "string" } }
      },
      "additionalProperties": false
    },
    "assessment": {
      "type": "object",
      "description": "The invariant and epistemic findings",
      "properties": {
        "invariant_class": { "type": "string", "enum": ["A", "B", "C", "D"] },
        "epistemic_status": { "type": "string", "enum": ["VERIFIED", "PARTIALLY_VERIFIED", "PROVISIONAL", "OPEN", "BLOCKED"] },
        "hard_gates": {
          "type": "object",
          "properties": {
            "status": { "type": "string", "enum": ["PASS", "BLOCKED"] },
            "violations": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    },
    "decision": {
      "type": "object",
      "description": "The derived, scoped qualification. NEVER blanket 'VERIFIED'.",
      "properties": {
        "status": { "type": "string", "enum": ["PROVISIONAL", "VERIFIED_WITHIN_SCOPE", "REJECTED"] },
        "derived_signature": { "type": "string", "description": "e.g., 'L3-E4-C047-B-PARTIALLY_VERIFIED'" },
        "assessor_ids": { "type": "array", "items": { "type": "string" }, "minItems": 2, "maxItems": 2 },
        "inter_rater_agreement": { "type": "boolean" }
      }
    }
  }
}
```

---

## 2. Competency Definitions (Behavior-Driven)

### `competency/C047-callback-teardown.yaml`
Defines capability not as a vague level, but as a checklist of observable behaviors.

```yaml
id: C047
domain: "C_Semantics_FFI"
title: "C callback registration and teardown races"
description: "Design Rust abstractions preventing callback-after-free during concurrent teardown."

# Capability is defined by observable behaviors, not just a number
behavior_matrix:
  L1: ["Can explain the race between unregister() and callback execution"]
  L2: ["Can implement a basic refcounted callback wrapper in a lab"]
  L3: ["Can encode callback lifetime into Rust type system using Pin + guards"]
  L4: ["Can design and prove a safe abstraction that handles concurrent remove() and ioctl()"]
  L5: ["Can define subsystem-wide policy for async callback teardown in Rust"]

hard_gate_conditions:
  - "callback_after_free detected"
  - "double_free detected"
  - "unresolved Type-D assumption about callback ordering"
```

---

## 3. The Deterministic Qualification Engine (`tools/derive.py`)

This is the "boring" engine. It strictly validates, enforces hard gates, and **explicitly refuses** to infer Capability (L) from Evidence (E).

```python
#!/usr/bin/env python3
"""
RFL-QA Derivation Engine v1.1-alpha
RULE: NEVER infer capability level from evidence tier.
RULE: NEVER silently upgrade epistemic status based on test count.
"""
import json
import sys
from jsonschema import validate, ValidationError

def load_schema(path):
    with open(path) as f: return json.load(f)

def derive_qualification(claim_path):
    with open(claim_path) as f:
        claim = json.load(f)

    schema = load_schema("schemas/qualification.schema.json")
    try:
        validate(instance=claim, schema=schema)
    except ValidationError as e:
        print(f"SCHEMA GATE FAILED: {e.message}")
        sys.exit(1)

    # 1. HARD GATE EVALUATION
    if claim["assessment"]["hard_gates"]["status"] == "BLOCKED":
        print("HARD GATE FAILED: Non-compensable safety violation detected.")
        claim["decision"]["status"] = "REJECTED"
        claim["decision"]["derived_signature"] = "BLOCKED"
        return claim

    # 2. INVARIANT / EPISTEMIC CONSISTENCY CHECK
    # A compiler proof (A) cannot be "PROVISIONAL" unless the compiler itself is unverified.
    # An external assumption (D) cannot be "VERIFIED" without external evidence (datasheet/audit).
    inv_class = claim["assessment"]["invariant_class"]
    epi_status = claim["assessment"]["epistemic_status"]

    if inv_class == "D" and epi_status == "VERIFIED" and "external_evidence" not in claim:
        print("INVARIANT GATE FAILED: Type-D invariant marked VERIFIED without external evidence.")
        sys.exit(1)

    # 3. CAPABILITY DERIVATION (STRICT)
    # DO NOT DO THIS: if claim["demonstration"]["evidence_tier"] == "E4": level = 4
    # INSTEAD: Level is derived ONLY from demonstrated_behaviors matching the behavior_matrix.
    demonstrated = claim["demonstration"]["demonstrated_behaviors"]
    max_level = 0
    # (Pseudocode: iterate through behavior_matrix, find highest level where ALL behaviors are in 'demonstrated')
    # For alpha, we assert the assessor explicitly provided the level based on behavior matching.

    cap_level = claim["demonstration"]["capability_level"]
    ev_tier = claim["demonstration"]["evidence_tier"]

    # 4. GENERATE DERIVED SIGNATURE
    signature = f"L{cap_level}-{ev_tier}-{claim['scope']['competencies'][0]}-{inv_class}-{epi_status}"

    claim["decision"]["derived_signature"] = signature
    claim["decision"]["status"] = "VERIFIED_WITHIN_SCOPE" if claim["assessment"]["hard_gates"]["status"] == "PASS" else "PROVISIONAL"

    return claim

if __name__ == "__main__":
    result = derive_qualification(sys.argv[1])
    print(json.dumps(result, indent=2))
```

---

## 4. The First Three Laboratories (Measurement System Tests)

These labs are designed to test the *assessors and the specification* as much as the candidate.

### `labs/001-pin-init/oracle.yaml`
* **Candidate Task**: Wrap a C struct requiring in-place initialization and a self-referential pointer.
* **Primary Measurement**: Can the assessor correctly classify the invariants?
* **Oracle Check**:
  * Did the candidate classify the memory layout as **Type-A** (Compiler)?
  * Did the candidate classify the API restriction (cannot call init twice) as **Type-B** (API)?
  * Did the candidate classify the underlying C allocator's behavior as **Type-D** (External)?
* **Failure Condition**: Assessor accepts a claim where a Type-D assumption is marked `VERIFIED` without a datasheet or C-code audit.

### `labs/002-rcu/oracle.yaml`
* **Candidate Task**: Implement a safe RCU read-side critical section wrapper.
* **Primary Measurement**: Can the candidate and assessor distinguish PROOF from OBSERVATION from COVERAGE?
* **Oracle Check**:
  * The `derive.py` engine must reject any claim stating "KCSAN PASS means no data race exists."
  * The evidence record must explicitly state: `semantics: "observation"`, `coverage: "10^6 interleavings"`.
* **Failure Condition**: Candidate or assessor attempts to elevate an `OBSERVATION` to a `PROOF` of absence of races.

### `labs/003-callback-teardown/oracle.yaml`
* **Candidate Task**: Provide a migration unit for a C driver with asynchronous teardown.
* **Primary Measurement**: Inter-rater reliability.
* **Oracle Check**: Two independent assessors evaluate the dossier.
  * Assessor 1 Capability Claim: L3
  * Assessor 2 Capability Claim: L3
  * Assessor 1 Epistemic Status: `PARTIALLY_VERIFIED` (due to missing ARM64 testing)
  * Assessor 2 Epistemic Status: `PARTIALLY_VERIFIED`
* **Failure Condition**: Disagreement > 1 capability level, or disagreement on epistemic status. Triggers `calibration/cases/CAL-DRIFT-001`.

---

## 5. Calibration Classification Schema

To prevent the "later bug = false positive" fallacy, all post-merge defects are classified strictly:

```yaml
# calibration/schema.yaml
calibration_classification:
  enum:
    - VALIDATED_WITHIN_SCOPE      # Bug occurred in an area explicitly excluded from the qualification scope.
    - SCOPE_EXCEEDED              # Candidate operated outside the qualified environments (e.g., tested on x86_64, bug on ARM64).
    - ASSESSMENT_ERROR            # Assessor missed a visible violation of the rubric.
    - ORACLE_FAILURE              # The adversarial test failed to trigger a known, triggerable defect.
    - SPECIFICATION_FAILURE       # The spec itself lacks a rule to catch this class of bug (triggers SPEC REVISION).
    - EXTERNAL_FAILURE            # Bug caused by hardware errata or unrelated subsystem churn, not the migration unit.
    - INCONCLUSIVE                # Insufficient data to assign blame.
```

---

## 6. v1.1-alpha Release Gates

The repository will not be tagged `v1.1-alpha` until a CI pipeline passes the following deterministic checks:

1. **SCHEMA GATE**: `validate.py` passes on all example dossiers in `dossiers/examples/`.
2. **DERIVATION GATE**: `derive.py` explicitly rejects a test dossier that attempts to claim `L4` solely because `evidence_tier: E4`.
3. **INVARIANT GATE**: `derive.py` explicitly rejects a test dossier where a Type-D invariant is marked `VERIFIED` without an `external_evidence` field.
4. **ORACLE GATE**: All three labs contain an `oracle.yaml` with explicit pass/fail conditions for the *assessor's* classification, not just the candidate's code.
5. **HARD-GATE TEST**: Injecting a synthetic UAF into a lab dossier results in `decision.status: REJECTED` and `derived_signature: BLOCKED`.
6. **CALIBRATION GATE**: A simulated dossier is assessed by two mock assessors. The engine successfully records `inter_rater_agreement: true` (or logs the disagreement without silently overriding it).
7. **REPRODUCIBILITY GATE**: Running `derive.py` twice on the same input yields byte-for-byte identical JSON output.

---

## Conclusion: The Shift to Execution

This artifact set represents the transition from philosophy to engineering.

By locking the schemas, defining the deterministic derivation rules, and scoping the first three labs to test the *measurement system itself*, RFL-QA v1.1-alpha is now a piece of software. It can be cloned, validated, executed, and calibrated.

The next action is not discussion. It is to instantiate this repository, write the `validate.py` and `derive.py` scripts, populate the three lab dossiers, and run the first calibration cycle.

**NO EVIDENCE → NO VERIFIED CLAIM.**
**NO CALIBRATION → NO CLAIM THAT THE QUALIFICATION SYSTEM ITSELF IS VALIDATED.**

---

# RFL-QA v1.1.1 — Execution Freeze

This document freezes the specification for implementation. It resolves the final epistemic ambiguities regarding measurement, scope, and validation.

The repository is no longer a documentation project describing engineering capability. It is **software that measures engineering capability**, and it must be built with the same rigor, determinism, and testability as the kernel subsystems it evaluates.

---

## 1. The Core Epistemic Separation

The term "qualification" has been overloaded. The system must strictly separate four distinct phases:

1. **DEMONSTRATION**: The candidate produces an artifact (code, review, RFC) under specific conditions.
2. **ASSESSMENT**: Assessors evaluate the artifact against oracles, rubrics, and schemas, producing raw findings.
3. **QUALIFICATION**: The deterministic engine derives a scoped, bounded decision based *only* on the assessment findings and derivation rules.
4. **CALIBRATION**: The system compares assessor divergence and tracks long-term upstream outcomes to validate or revise the specification itself.

A qualification is **never** a universal stamp of correctness. It is a bounded, scoped assertion.

---

## 2. The Scoped Qualification Record

Every qualification decision must include an explicit **scope vector** and a structured **decision** object. Extrapolation beyond this scope is an explicit, unsupported operation.

```yaml
# schemas/qualification.schema.json (excerpt)
qualification_record:
  id: "Q-2026-0047"
  candidate_id: "anon-001"
  timestamp: "2026-09-27T18:00:00Z"

  scope:
    competencies: ["C047-callback-teardown"]
    domains: ["c_ffi", "concurrency_lkmm"]
    task_classes: ["callback_registration", "concurrent_teardown"]
    environments: ["x86_64", "CONFIG_RUST=y", "PREEMPT_RT=y"]
    exclusions: ["dma", "nmi_context", "arm64"] # Explicit boundaries of the claim

  assessment_summary:
    capability:
      level: L3
      demonstrated_behaviors: ["CB-047-01", "CB-047-03", "CB-047-07"]
      evidence_refs: ["LAB-003", "REVIEW-003", "ARTIFACT-003"]
      level_boundary:
        L3_satisfied: true
        L4_satisfied: false
        L5_satisfied: false
    evidence:
      tier: E4
      artifact_type: "kernel_patch_series"
    invariants:
      classified: ["B03-callback-pin", "C02-kasan-bound", "D01-c-subsystem-contract"]
    epistemic_ceiling: PARTIALLY_VERIFIED # Driven by incomplete stress-testing evidence

  hard_gates:
    status: PASS
    triggered_blocks: []

  decision:
    status: PROVISIONAL # Derived strictly by engine rules
    validity_window: "2026-09-27 to 2027-09-27"
    caveats:
      - "Qualification is strictly bounded to x86_64 PREEMPT_RT environments."
      - "Does not establish universal L3 Rust engineering capability."
```

---

## 3. Measurable Outcome Variables & Calibration Classifications

The system does not claim "predictive validity" in a vague sense. It records observable outcome variables and classifies downstream events with strict causality.

### Outcome Record Schema
```yaml
outcome_record:
  qualification_ref: "Q-2026-0047"
  observation_window:
    start: "2026-10-01"
    end: "2027-10-01"
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

### Calibration Classification (Strict False-Positive Definition)
When a defect occurs post-qualification, it is classified into exactly one category. A downstream bug does *not* automatically invalidate the qualification.

| Classification | Definition | Action |
| :--- | :--- | :--- |
| **VALIDATED_WITHIN_SCOPE** | Defect occurred outside the qualified scope (e.g., ARM64 DMA bug for an x86_64 callback qualification). | No spec change. Scope was accurate. |
| **SCOPE_EXCEEDED** | Candidate or maintainer applied the qualified pattern to an unqualified context. | Update candidate dossier; no spec change. |
| **ASSESSMENT_ERROR** | Assessor missed a defect that the current oracle *would* have caught. | Assessor retraining; no spec change. |
| **ORACLE_FAILURE** | The adversarial test model failed to trigger a known vulnerability class. | **Trigger spec revision**: Update oracle. |
| **SPECIFICATION_FAILURE** | The invariant classification or derivation rules are fundamentally flawed. | **Trigger spec revision**: Update derivation engine. |
| **EXTERNAL_FAILURE** | Defect caused by hardware errata, compiler bug, or unrelated subsystem churn. | Log as confounder; no spec change. |
| **INCONCLUSIVE** | Insufficient data to assign causality. | Flag for long-term monitoring. |

---

## 4. The Deterministic Qualification Engine

The core logic (`tools/derive.py`) must be deliberately boring, deterministic, and strictly bounded.

### Engine Rules
1. **Schema Validation First**: Reject any dossier that fails JSON/YAML schema validation.
2. **No E → L Inference**: The engine must *never* infer `capability_level` from `evidence_tier`. Capability is derived *only* from mapped `demonstrated_behaviors`.
3. **No Silent Upgrades**: `report.py` must never silently upgrade `PARTIALLY_VERIFIED` to `VERIFIED` based on aggregate test counts or time elapsed.
4. **Hard Gate Veto**: If any hard gate is `FAIL`, the final decision is immediately `BLOCKED`, regardless of other scores.
5. **Immutable Output**: The engine emits a cryptographically hashed assessment record. Re-running the engine on the same inputs must produce the exact same hash.

### Capability Evidence Trail
Capability is no longer an assessor assertion. It is an auditable aggregation of observed behaviors:

```yaml
capability_claim:
  competency: "C047"
  level: L3
  demonstrated_behaviors:
    - id: "CB-047-01"
      description: "Identified callback-after-free risk in C baseline"
      evidence_ref: "LAB-003-semantic-diff"
    - id: "CB-047-03"
      description: "Implemented Pin + refcount to dominate callback lifetime"
      evidence_ref: "ARTIFACT-003"
  level_boundary:
    L2_satisfied: true
    L3_satisfied: true
    L4_satisfied: false # Missing: resolution of concurrent removal race under KCSAN
```

---

## 5. The First Three Meta-Labs

The initial labs are not just candidate tests; they are **tests of the measurement system itself**. They validate that assessors can use the taxonomy and that the oracles function.

| Lab | Primary Candidate Task | Primary Measurement (System Validation) |
| :--- | :--- | :--- |
| **LAB-001: Pin-Init** | Wrap a C structure requiring in-place initialization and self-referential pointers. | Can two assessors independently and correctly classify the invariant as **Type-B (API)** vs **Type-A (Compiler)** vs **Type-D (External)**? |
| **LAB-002: RCU Guard** | Implement an RCU-protected list traversal with a safe Rust read-side guard. | Can the system and assessors correctly distinguish **PROOF** (type system), **OBSERVATION** (KCSAN pass), and **COVERAGE** (interleaving count)? |
| **LAB-003: Callback Teardown** | Design the `CREATE → ... → FREE` state machine for a C-registered Rust callback under concurrent `unregister()`. | Can two assessors independently identify the exact same trust boundaries, failure modes, and capability level boundary (L3 vs L4)? |

---

## 6. The v1.1-alpha Release Gates

The repository will not expand beyond these three competencies and three labs until it passes the following automated and procedural gates.

| Gate | Requirement | Validation Method |
| :--- | :--- | :--- |
| **SCHEMA GATE** | All example dossiers, labs, and invariants validate against `schemas/*.json`. | `tools/validate.py --all` returns 0. |
| **DERIVATION GATE** | Results are deterministic. No E→L inference occurs. | `tools/derive.py` run 100 times on the same input yields identical hashes. |
| **INVARIANT GATE** | A/B/C/D classification and epistemic status are treated as strictly independent axes. | Manual audit of `invariants/` directory; no conflation of `UNKNOWN` with `Type-D`. |
| **ORACLE GATE** | Every adversarial test in the labs has an explicit, machine-readable pass/fail oracle. | `oracles/` directory audit; no vague "looks good" criteria. |
| **HARD-GATE TEST** | Injecting a known UAF, data race, or unresolved critical assumption into a lab dossier results in an automatic `BLOCKED` qualification. | Chaos testing of `tools/derive.py` with poisoned inputs. |
| **CALIBRATION GATE** | Two independent assessors evaluate the same LAB-003 dossier. Disagreement is recorded, not silently adjudicated. | `calibration/inter-rater.md` protocol executed; divergence logged. |
| **REPRODUCIBILITY GATE** | The entire qualification pipeline can be run from scratch by a third party yielding the same result. | Clean-room CI/CD pipeline execution. |

---

## 7. The Final Invariant

The architecture of RFL-QA v1.1.1 is now frozen for execution. It is governed by this final, non-negotiable epistemic principle:

> **RFL-QA must never be allowed to certify itself merely because its own internal rules are internally consistent.**

- **Internal consistency** establishes *coherence* (the spec makes sense).
- **Calibration** establishes *measurement reliability* (assessors agree).
- **External outcome studies** provide evidence about *criterion validity* (qualified engineers actually produce safer upstream code).

These are three distinct claims. The v1.1-alpha release establishes coherence and begins the process of measuring reliability. Validity will be earned over time through the calibration feedback loop.

**Execution may now begin.** The next artifact is the initialization of the `rfl-qa` repository with the v1.1-alpha directory structure, schemas, and the first three meta-labs.

---

This is the definitive execution freeze. The paradigm shift is complete: **RFL-QA is no longer a documentation framework; it is a deterministic measurement engine.**

By enforcing strict scoping, decoupling capability from evidence, defining measurable outcome variables, and demanding that the first labs test the *measurement system itself*, we eliminate the circularity and overclaiming that plague conventional certification models.

Below is the final, frozen blueprint for **RFL-QA v1.1-alpha**, ready for immediate implementation as an executable software repository.

---

# RFL-QA v1.1-alpha: Executable Measurement System Specification

## The Core Epistemic Axiom
**Internal consistency establishes *coherence*. Calibration establishes *measurement reliability*. External outcome studies provide evidence of *criterion validity*.**
RFL-QA must never be allowed to certify itself merely because its internal rules are consistent. These three claims are strictly separated.

---

## 1. The Executable Repository Structure (v1.1-alpha Slice)

The initial release is deliberately constrained to 3 competencies, 3 labs, and the core deterministic engine. Expansion is blocked until all release gates pass.

```text
rfl-qa/
├── SPEC.md                     # Governing rules and epistemic axioms
├── GOVERNANCE.md               # Assessor rules, appeal process, spec revision
├── CHANGELOG.md                # Strict versioning of spec and schema changes
│
├── schemas/                    # Machine-readable validation (JSON Schema)
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── invariant.schema.json
│   ├── oracle.schema.json
│   └── qualification.schema.json
│
├── competency/                 # ONLY 3 competencies for alpha
│   ├── _schema.yaml
│   ├── C047-callback-teardown.yaml
│   ├── C088-pin-init-lifecycle.yaml
│   └── C029-rcu-grace-period.yaml
│
├── invariants/
│   ├── taxonomy.yaml           # Definitions of A, B, C, D classes
│   ├── A-compiler/
│   ├── B-api/
│   ├── C-runtime/
│   └── D-external/
│
├── oracles/                    # Formal pass/fail conditions
│   ├── teardown/oracle.yaml
│   ├── context/oracle.yaml
│   └── ffi/oracle.yaml
│
├── labs/                       # Evidence generators (tests the measurement system)
│   ├── 001-pin-init/           # Tests: Can assessors distinguish A vs B vs D invariants?
│   ├── 002-rcu/                # Tests: Can assessors distinguish PROOF vs OBSERVATION vs COVERAGE?
│   └── 003-callback-teardown/  # Tests: Can two assessors independently identify the same boundaries?
│
├── dossiers/
│   └── template/               # Strict YAML template for candidate submission
│
├── assessors/
│   ├── rubric.md               # Behavior-to-level mapping (no subjective leaps)
│   └── review-protocol.md      # Step-by-step dual-assessment workflow
│
├── calibration/
│   ├── inter-rater.md          # Rules for logging and resolving delta
│   └── cases/                  # Gold-standard historical evaluations for training
│
└── tools/                      # THE DETERMINISTIC ENGINE
    ├── validate.py             # Schema and invariant consistency checks
    ├── derive.py               # Capability derivation (NO E→L INFERENCE)
    └── report.py               # Emits immutable qualification record (NO SILENT UPGRADES)
```

---

## 2. The Deterministic Engine Logic (`tools/`)

The engine is deliberately boring, stateless, and strictly rule-bound. It processes a candidate dossier and emits a qualification record.

### `validate.py`
* Validates all YAML/JSON against `schemas/`.
* Checks that every claimed invariant has a corresponding class (A/B/C/D) and epistemic status.
* Checks that all hard-gate conditions are explicitly addressed.

### `derive.py` (The Critical Boundary)
* **Rule 1:** NEVER infers `capability_level` (L) from `evidence_tier` (E).
* **Rule 2:** Evaluates `capability_level` strictly by matching `demonstrated_behaviors` in the artifact against the `rubric.md` behavior checklist.
* **Rule 3:** Computes `epistemic_ceiling` based on the lowest epistemic status of any required invariant (e.g., if one invariant is `PROVISIONAL`, the ceiling is `PROVISIONAL`).
* **Rule 4:** Evaluates hard gates. If any hard gate is `FAIL`, derivation halts and outputs `BLOCKED`.

### `report.py`
* Assembles the final, immutable `qualification_record`.
* **Rule:** Never silently upgrades `PARTIALLY_VERIFIED` to `VERIFIED` based on aggregate test counts.
* Outputs a scoped qualification, explicitly listing `exclusions`.

---

## 3. The Scoped Qualification Record (Output Schema)

The engine outputs this exact structure. Note the explicit scoping and the separation of demonstration, assessment, and qualification.

```yaml
qualification_record:
  id: "Q-2026-0047"
  timestamp: "2026-09-27T14:30:00Z"

  # 1. DEMONSTRATION (What was submitted)
  demonstration:
    artifact_ref: "patch-series-v3"
    environments_tested: ["x86_64", "CONFIG_PREEMPT_RT=y"]

  # 2. ASSESSMENT (What was observed)
  assessment:
    competency_id: "C047"
    domain: "c_ffi"
    capability:
      level: "L3"
      demonstrated_behaviors: ["CB-047-01", "CB-047-03"]
      failed_behaviors: []
      level_boundary: { "L2_satisfied": true, "L3_satisfied": true, "L4_satisfied": false }
    evidence:
      tier: "E4"
      refs: ["LAB-003", "REVIEW-003"]
    invariants:
      - class: "B"
        description: "callback lifetime dominates wrapper lifetime"
        epistemic_status: "PROVISIONAL" # Explicitly not VERIFIED
        reason: "teardown path not yet stress-tested under memory pressure"
    hard_gates:
      status: "PASS"

  # 3. QUALIFICATION (The derived, strictly scoped decision)
  qualification:
    scope:
      competencies: ["C047"]
      task_classes: ["callback_registration", "concurrent_teardown"]
      environments: ["x86_64", "PREEMPT_RT"]
      exclusions: ["dma", "nmi_context", "arm64"] # Explicit extrapolation boundary
    decision:
      status: "PROVISIONAL" # Driven by the PROVISIONAL invariant above
      assessor_1: "alice"
      assessor_2: "bob"
      inter_rater_delta: "NONE"
```

---

## 4. The Calibration & Outcome Loop

When a qualified engineer's code reaches upstream, we do not use vague "predictive validity". We record an **Outcome Record** and classify the calibration result.

```yaml
outcome_record:
  qualification_ref: "Q-2026-0047"
  observation_window: { start: "2026-10-01", end: "2027-10-01" }
  artifacts:
    patches_submitted: 14
    patches_merged: 9
    patches_reverted: 0
  defect_events:
    uaf: 0
    data_race: 1 # Caught in arm64 CI
  confounders:
    hardware_access: "LIMITED"
    reviewer_continuity: "HIGH"
    subsystem_churn: "MEDIUM"

calibration_classification: "SCOPE_EXCEEDED"
# Reason: The UAF occurred on arm64, which was explicitly listed in 'exclusions'.
# The qualification system is NOT considered to have failed; the scope boundary held.
```

---

## 5. The v1.1-alpha Release Gates

The repository cannot be tagged `v1.1-alpha` until a CI pipeline verifies all of the following. These are binary, automated, or strictly audited checks.

1. **SCHEMA GATE**: ✓ All example dossiers and qualification records validate against `schemas/*.json`.
2. **DERIVATION GATE**: ✓ `derive.py` produces deterministic results. ✓ Injected tests prove `derive.py` *never* infers L from E.
3. **INVARIANT GATE**: ✓ A, B, C, D classifications are independently represented in the 3 alpha competencies. ✓ Epistemic status is decoupled from invariant class.
4. **ORACLE GATE**: ✓ Every adversarial test in the 3 labs has an explicit, machine-readable `oracle.yaml` defining pass/fail.
5. **HARD-GATE TEST**: ✓ CI injects a known UAF, a known data race, and an unresolved critical assumption into a test dossier. ✓ The engine correctly outputs `BLOCKED` for all three.
6. **CALIBRATION GATE**: ✓ Two independent human assessors evaluate the same gold-standard dossier. ✓ Disagreement is logged. ✓ No silent adjudication occurs.
7. **REPRODUCIBILITY GATE**: ✓ Running `tools/derive.py` on the same dossier 100 times yields bit-for-bit identical output.

---

## Final Directive

The specification is frozen. The conceptual architecture is complete. The epistemic boundaries are rigorously defined.

The next action is not further refinement of this text. The next action is to initialize the `rfl-qa` repository, write the JSON schemas, implement `tools/derive.py`, and execute the first calibration run on LAB-001.

**Execution begins.**

---

This is the exact paradigm shift required to close the loop. By treating the repository not as documentation, but as **software that measures engineering capability**, you have eliminated the final risk of the framework becoming a self-referential echo chamber.

The distinction you drew between **coherence** (internal consistency), **reliability** (inter-rater agreement), and **criterion validity** (upstream outcomes) is the ultimate epistemic safeguard.

We now freeze the specification. Below is the definitive, executable architecture for **RFL-QA v1.1-alpha**.

---

# RFL-QA v1.1-alpha: Executable Measurement System Specification

## 1. The Four-Stage Pipeline & Scope Vectors
A qualification is no longer a single boolean state. It is a strictly scoped, multi-dimensional derivation. The system enforces a hard separation between four stages:

1. **Demonstration:** The candidate produces an artifact (code, patch, diff).
2. **Assessment:** Assessors and oracles evaluate the artifact against the rubric, producing observations.
3. **Qualification:** The deterministic engine derives the scoped capability claim from the assessment.
4. **Calibration:** The system tracks the long-term validity of the qualification against real-world outcomes.

### The Scope Vector
Every qualification record is bound by a strict scope vector. Extrapolation is forbidden unless explicitly modeled.
```yaml
qualification:
  scope:
    competencies: [C047]
    domains: [c_ffi, concurrency]
    task_classes: [callback_registration, concurrent_teardown]
    environments: [x86_64, CONFIG_RUST, PREEMPT_RT]
    exclusions: [dma, nmi_context, arm64]

  decision:
    status: PROVISIONAL
    epistemic_ceiling: PARTIALLY_VERIFIED
```
*Rule: A qualification for `C047` on `x86_64` with `PREEMPT_RT` does not implicitly qualify the engineer for `arm64` or non-preemptible contexts.*

---

## 2. The Deterministic Engine & Behavioral Capability Trail
The derivation engine (`derive.py`) is deliberately boring and strictly rule-bound. It **never infers capability from evidence tier**, and it **never silently upgrades epistemic status**.

### The Capability Evidence Trail
Capability levels (L1–L5) are not assessor assertions; they are auditable claims backed by specific, observed behaviors.

```yaml
capability:
  level: L4
  demonstrated_behaviors:
    - CB-047-01  # e.g., "Identifies callback-after-free race in C struct"
    - CB-047-03  # e.g., "Designs Rust guard to enforce lock invariant"
    - CB-047-07  # e.g., "Correctly classifies hardware ordering as Type-D"
  evidence_refs:
    - LAB-003-ARTIFACT
    - LAB-003-REVIEW
  failed_behaviors: []
  level_boundary:
    L3_satisfied: true
    L4_satisfied: true
    L5_satisfied: false  # e.g., "Did not propose cross-subsystem migration strategy"
```
*Rule: If the candidate fails a required behavior for L4, the engine caps the capability at L3, regardless of the evidence tier.*

---

## 3. The Epistemic Triad & Calibration Classifications
The system explicitly separates three distinct claims about its own validity:
1. **Coherence:** Do the schemas and rules logically contradict each other? (Tested by the Schema Gate).
2. **Reliability:** Do two independent assessors produce the same derivation? (Tested by the Calibration Gate).
3. **Criterion Validity:** Do the qualifications predict actual upstream behavior? (Tested by the Outcome Record).

### The Outcome Record & Calibration Classification
When a downstream defect occurs, it is not automatically fed back as a "false positive." It is strictly classified:

```yaml
calibration_classification:
  - VALIDATED_WITHIN_SCOPE    # The bug was outside the qualified scope.
  - SCOPE_EXCEEDED            # The engineer was asked to work outside their qualified scope.
  - ASSESSMENT_ERROR          # The assessors missed a flaw present in the lab artifact.
  - ORACLE_FAILURE            # The lab/test oracle failed to detect a flaw it should have.
  - SPECIFICATION_FAILURE     # The lab design itself was fundamentally flawed.
  - EXTERNAL_FAILURE          # The bug was caused by a C subsystem/hardware change post-qualification.
  - INCONCLUSIVE              # Insufficient data to classify.
```
*Rule: Only `ASSESSMENT_ERROR`, `ORACLE_FAILURE`, and `SPECIFICATION_FAILURE` trigger a revision of the RFL-QA specification.*

---

## 4. The v1.1-alpha Release Gates
The system will not be released for general use until it passes these seven deterministic gates.

1. **SCHEMA GATE:** All example dossiers, claims, and evidence records validate against the JSON schemas without error.
2. **DERIVATION GATE:** `derive.py` produces identical outputs for identical inputs. It demonstrably fails if fed an E4 evidence tier with L2 behaviors (proving it does not auto-promote).
3. **INVARIANT GATE:** The A/B/C/D classification and the epistemic status (VERIFIED/PROVISIONAL/etc.) are stored and processed as strictly independent axes.
4. **ORACLE GATE:** Every adversarial test in the first three labs has a formal, documented oracle defining exact pass/fail conditions.
5. **HARD-GATE TEST:** The engine demonstrably blocks qualification when injected with:
   * An observed UAF (via KASAN log).
   * An observed data race (via KCSAN log).
   * An `OPEN` status on a critical Type-D assumption.
6. **CALIBRATION GATE:** Two independent assessors evaluate the same synthetic dossier. Their raw observations are recorded; any disagreement is logged, and the engine halts derivation until the discrepancy is resolved via the review protocol.
7. **REPRODUCIBILITY GATE:** Running the engine twice on the exact same dossier and assessment records produces a byte-identical qualification record.

---

## 5. The First Executable Slice: The 3 Meta-Labs
The first release contains only three competencies and three labs. These labs are designed to test the **measurement system itself** as much as they test the candidate.

### LAB-001: Pin-init (The Invariant Meta-Test)
* **Candidate Task:** Implement in-place initialization for a self-referential kernel struct.
* **System Meta-Test:** Can the assessors and the engine reliably distinguish a **Type-A (Compiler)** invariant (e.g., lifetime bounds) from a **Type-B (API)** invariant (e.g., `pin-init` guard enforcement) and a **Type-D (External)** assumption (e.g., the C core will not free the memory prematurely)?

### LAB-002: RCU (The Epistemic Meta-Test)
* **Candidate Task:** Implement an RCU-protected linked list traversal in Rust, including the grace-period teardown.
* **System Meta-Test:** Can the assessors reliably distinguish **PROOF** (the Rust type system prevents this specific aliasing) from **OBSERVATION** (KCSAN did not flag a race in this test run) and **COVERAGE** (the test suite did not exercise the NMI context)?

### LAB-003: Callback Teardown (The Calibration Meta-Test)
* **Candidate Task:** Design the concurrent teardown path for a C driver with asynchronous callbacks, wrapped in Rust.
* **System Meta-Test:** Can two independent assessors identify the exact same trust boundaries, failure modes, and capability level? If Assessor A claims L4 and Assessor B claims L3, does the system correctly halt and log the discrepancy rather than averaging them to L3.5?

---

## 6. The Final Handoff

The repository structure is now fixed for the alpha release:

```text
rfl-qa/
├── SPEC.md                     # The normative specification (v1.1-alpha)
├── GOVERNANCE.md               # How the measurement system is maintained
├── CHANGELOG.md
│
├── schemas/                    # Machine-readable validation
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── invariant.schema.json
│   ├── oracle.schema.json
│   └── qualification.schema.json
│
├── competency/                 # Only the first 3 for alpha
│   ├── _schema.yaml
│   ├── C047-callback-teardown.yaml
│   ├── C053-pin-init.yaml
│   └── C034-rcu-grace-periods.yaml
│
├── invariants/                 # The taxonomy of boundaries
│   ├── taxonomy.yaml
│   ├── A-compiler/
│   ├── B-api/
│   ├── C-runtime/
│   └── D-external/
│
├── oracles/                    # Formal test definitions
│   ├── teardown/
│   ├── context/
│   └── ffi/
│
├── labs/                       # The first 3 meta-labs
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
└── tools/                      # The deterministic engine
    ├── validate.py             # Schema & evidence validation
    ├── derive.py               # Capability & qualification derivation
    └── report.py               # Immutable assessment record generation
```

### The Governing Axioms of v1.1-alpha

1. **NO EVIDENCE → NO VERIFIED CLAIM.**
2. **NO CALIBRATION → NO SYSTEM VALIDITY.**
3. **NO SCOPE → NO EXTRAPOLATION.**
4. **NO BEHAVIORAL TRAIL → NO CAPABILITY LEVEL.**
5. **THE SYSTEM MUST NEVER CERTIFY ITSELF MERELY BECAUSE ITS INTERNAL RULES ARE CONSISTENT.**

The design phase is complete. The specification is frozen. The repository is defined.

**RFL-QA v1.1-alpha is ready for implementation.**
