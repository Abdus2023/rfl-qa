# RFL-QA v1.1: Operational Specification & Repository Architecture

> A calibrated, two-axis empirical qualification system separating capability ($L_0$–$L_5$), evidence tiers ($E_0$–$E_5$), invariant taxonomy (Types A–D), and epistemic status (`VERIFIED`, `PARTIALLY_VERIFIED`, `PROVISIONAL`, `OPEN`, `BLOCKED`). Incorporates defect-vs-detection boundaries, structured trust-boundary accounting, dual-assessor calibration, and upstream outcome feedback loops.

---

## 1. Epistemic Principles & The Four Specification Freezes

RFL-QA v1.1 freezes four critical specification-level definitions to eliminate false equivalence, category errors, and uncalibrated risk metrics:

### Freeze 1: Decoupling Evidence Tier from Proficiency Level
$$\mathbf{E_4 \not\implies L_4 \quad \text{and} \quad E_n \not\implies L_n}$$

* **Evidence Tier ($E_n$)** defines the *empirical context and rigor* of the artifact.
* **Capability Level ($L_n$)** defines the *observed engineering scope and depth*.

A merged in-tree patch series ($E_4$) demonstrating driver registration using established boilerplate provides production-grade evidence of practitioner capability ($L_2$ or $L_3$). It does not grant architectural competence ($L_4$ or $L_5$). Capability is recorded strictly as a combined pair:

$$\mathbf{\text{Qualification Result}} = \mathbf{L_m\text{-}E_n} \quad (\text{e.g., } L_3\text{-}E_4)$$

---

### Freeze 2: Orthogonality of Invariant Class and Epistemic Status
$$\mathbf{UNKNOWN \neq \text{Type D}}$$

* **Invariant Class (A / B / C / D)** defines *origin and enforcement mechanism*.
* **Epistemic Status** defines the *current state of empirical knowledge*.

```
INVARIANT
   │
   ├── Enforcement Class:
   │     ├── Type A (Compiler-Enforced)
   │     ├── Type B (API-Enforced)
   │     ├── Type C (Runtime-Enforced)
   │     └── Type D (External / System Contract)
   │
   └── Epistemic Status:
         ├── VERIFIED          (Proven or exhaustively verified under oracle)
         ├── PARTIALLY_VERIFIED(Demonstrated under bounded subsets; gaps remain)
         ├── PROVISIONAL       (Reasonable engineering assumption; unproven)
         ├── OPEN              (Uncharacterized or uninvestigated boundary)
         └── BLOCKED           (Demonstrated violation or hard-gate failure)
```

#### Example of Orthogonality
```yaml
invariant:
  id: "INV-B-042"
  class: "B"  # Type B: API-Enforced
  description: "Callback lifetime strictly dominates wrapper handle lifetime"
epistemic:
  status: "PROVISIONAL"
  reason: "Type signature enforces lifetime, but concurrent teardown under memory pressure has not been exercised"
```
*This is an API-enforced invariant (Type B) with incomplete empirical evidence (`PROVISIONAL`), NOT an external contract (Type D).*

---

### Freeze 3: Defect vs. Detection (Absence of Evidence Boundary)
$$\mathbf{\text{Sanitizer: PASS} \not\implies \text{Absence of Defect}}$$

Dynamic analysis tools provide observation over an executed population, not formal proofs over the complete state space. The qualification record must distinguish four epistemic tiers:

1. **PROOF:** Mathematically established by the type system or formal model under sound assumptions.
2. **OBSERVATION:** Behavior witnessed and recorded during concrete execution traces.
3. **COVERAGE:** The bounded subspace of inputs, interleavings, or states actually exercised.
4. **ABSENCE-OF-EVIDENCE:** A pass result indicating no defect was detected *within the executed coverage*.

*Syzkaller executing $10^7$ iterations without a crash proves that no defect was found within that specific trace population; it does not prove the absence of races or memory corruption across unexercised paths.*

---

### Freeze 4: Trust-Boundary Topology vs. Raw Line Counts
$$\mathbf{\text{Unsafe Risk} \neq \frac{\text{Lines of Unsafe}}{\text{Total Lines}}}$$

Raw lines of `unsafe` is a dangerous vanity metric: ten rigorously audited and encapsulated lines of unsafe code can be substantially safer than one poorly abstracted unsafe pointer cast. Risk is evaluated across **trust-boundary topology**:

$$\text{Trust Boundary Vector} = \begin{bmatrix}
\text{Unsafe Concentration (Density per encapsulation seam)} \\
\text{Boundary Seam Count (Distinct FFI / raw-pointer crossing points)} \\
\text{Invariant Coverage (Ratio of explicit proofs to unsafe operations)} \\
\text{Independent Review Coverage (Assessor consensus on safety comments)} \\
\text{Unresolved Assumptions (Count of PROVISIONAL/OPEN Type D entries)} \\
\text{Verification Coverage (Sanitizer, KUnit, and dynamic testing depth)}
\end{bmatrix}$$

---

## 2. The Formal Two-Axis Qualification Model

Qualification is determined by evaluating the interaction of capability and empirical evidence across four explicit dimensions:

```
                       RFL-QA QUALIFICATION
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
             CAPABILITY                     EVIDENCE
                  │                             │
              L0 ─ L5                       E0 ─ E5
                  │                             │
                  └──────────────┬──────────────┘
                                 │
                          QUALIFICATION
                                 │
                 ┌───────────────┼────────────────┐
                 ▼               ▼                ▼
              VERIFIED       PROVISIONAL        BLOCKED
```

### The 4-Tuple Claim Record
Every qualified claim within the system is recorded as an immutable 4-tuple:

$$\mathbf{Q} = \Big\langle \mathbf{Capability}\ (L_0\text{--}L_5),\; \mathbf{Evidence}\ (E_0\text{--}E_5),\; \mathbf{Invariant}\ (\text{A/B/C/D}),\; \mathbf{Status}\ (\text{VERIFIED}\dots\text{BLOCKED}) \Big\rangle$$

---

## 3. The Dual-Assessor Calibration Loop

A qualification system that lacks inter-rater calibration is merely an arbitrary subjective grading rubric.

### Inter-Rater Reliability Requirement
Two independent assessors evaluating the identical Migration Unit Dossier must independently produce concordant ratings across:
* **Capability Level** ($\Delta L \le 0$)
* **Evidence Tier** ($\Delta E \le 0$)
* **Invariant Classification** (Agreement on Types A, B, C, D)
* **Epistemic Status** (Concordance on `VERIFIED`, `PROVISIONAL`, `OPEN`, `BLOCKED`)
* **Hard Safety Gates** (Zero divergence on `PASS` vs `BLOCKED`)

$$\text{Disagreement between Assessors} \implies \text{Defect in Qualification Specification Precision}$$

When assessors diverge, the discrepancy is treated as an ambiguity bug in the qualification specification, triggering revision.

### The Upstream Feedback Calibration Loop
```
SPECIFICATION
     │
     ▼
LAB & DOSSIER
     │
     ▼
ORACLE EVALUATION
     │
     ▼
INDEPENDENT ASSESSORS (Primary & Secondary)
     │
     ▼
QUALIFICATION DECISION
     │
     ▼
UPSTREAM OUTCOME (Merged code, LKML reviews, syzkaller reports)
     │
     ▼
CALIBRATION REPOSITORY (Tracking false-positives & regressions)
     │
     ▼
SPECIFICATION REVISION
```

$$\mathbf{NO\ CALIBRATION \implies NO\ CLAIM\ THAT\ THE\ SYSTEM\ IS\ VALIDATED.}$$

---

## 4. Canonical Repository Architecture (`rfl-qa`)

The RFL-QA system is organized as a machine-readable, schema-validated engineering repository:

```text
rfl-qa/
├── SPEC.md                           # Normative operational specification
├── GOVERNANCE.md                     # Maintenance, dispute resolution, and calibration policy
├── competency/                       # Registry of 100 granular competencies
│   ├── C001.yaml                     # CPU privilege rings & exception handling
│   ├── C047.yaml                     # C callback registration & teardown races
│   ├── ...
│   └── C100.yaml                     # Subsystem sustainability & knowledge transfer
├── invariants/                       # Invariant taxonomy & formal proofs
│   ├── A-compiler/                   # Type A: Borrow checker, lifetimes, Send/Sync
│   ├── B-api/                        # Type B: Typestate, pin-init, RAII guards
│   ├── C-runtime/                    # Type C: lockdep, KASAN, KCSAN, might_sleep
│   └── D-external/                   # Type D: Hardware registers, C core contracts
├── evidence/                         # Evidence records and evaluation artifacts
│   ├── schema.yaml                   # Machine-readable evidence record schema
│   └── examples/                     # Calibrated canonical evidence examples
├── oracles/                          # Formal adversarial test oracles
│   ├── teardown/                     # Concurrent teardown interleaving oracles
│   ├── semantic-diff/                # 12-dimension semantic diff oracle
│   ├── context/                      # Static vs dynamic execution context oracle
│   └── ffi/                          # Trust-boundary minimization oracle
├── labs/                             # 15 Standardized adversarial labs
│   ├── 001-pin-init/                 # Self-referential struct initialization
│   ├── 002-rcu/                      # Read-side protection vs grace-period traps
│   ├── 003-callback/                 # Asynchronous callback teardown races
│   ├── 004-context-violation/        # Sleep-in-atomic injection tests
│   ├── 005-error-unwind/             # Multi-stage allocation failure unwinding
│   ├── 006-bindgen-shock/            # Struct padding and layout drift defenses
│   ├── 007-dma-coherency/            # Cache invalidation & device ownership
│   ├── 008-lockdep-maze/             # Nested lock inversion detection
│   ├── 009-unwrap-elimination/       # Systematic panic-free refactoring
│   ├── 010-trait-escape/             # Trait object vtable lifetime containment
│   ├── 011-workqueue-race/           # cancel_work_sync vs module unload
│   ├── 012-percpu-migration/         # Preemption-disabled per-CPU access
│   ├── 013-macro-expansion/          # Macro reverse-engineering & typing
│   ├── 014-toolchain-gating/         # Rustc pinning & Kbuild conditional gating
│   └── 015-governance-rfc/           # LKML RFC defense & maintainer negotiation
├── dossiers/                         # Assessment submission dossiers
│   └── template/                     # Standard Migration Unit Dossier template
├── assessors/                        # Evaluation rubrics and protocol
│   ├── rubric.md                     # Objective capability grading rubric
│   └── review-protocol.md            # Dual-assessor blind review procedures
├── calibration/                      # Systemic validity and reliability tracking
│   ├── inter-rater.md                # Inter-rater concordance measurement protocol
│   └── historical-cases/             # Regression archives and calibrated case studies
└── schemas/                          # JSON Schemas for validation
    ├── evidence.schema.json          # Schema for Evidence Records
    ├── dossier.schema.json           # Schema for Migration Unit Dossiers
    ├── invariant.schema.json         # Schema for Invariant & Assumption Ledger entries
    └── qualification.schema.json     # Schema for Qualification Decision Records
```

---

## 5. Machine-Readable Schema Specifications

### 5.1. Qualification Decision Schema (`qualification.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://rfl-qa.org/schemas/qualification.schema.json",
  "title": "QualificationDecision",
  "type": "object",
  "required": [
    "candidate_id",
    "migration_unit_id",
    "evaluators",
    "capability_vector",
    "hard_gate_status",
    "decision",
    "timestamp"
  ],
  "properties": {
    "candidate_id": { "type": "string" },
    "migration_unit_id": { "type": "string" },
    "evaluators": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 2
    },
    "capability_vector": {
      "type": "object",
      "required": [
        "hardware",
        "linux_core",
        "concurrency_lkmm",
        "c_ffi",
        "rust_unsafe",
        "rfl_abstractions",
        "verification",
        "toolchain",
        "governance"
      ],
      "additionalProperties": {
        "type": "object",
        "required": ["capability_level", "evidence_tier", "status"],
        "properties": {
          "capability_level": { "type": "string", "enum": ["L0", "L1", "L2", "L3", "L4", "L5"] },
          "evidence_tier": { "type": "string", "enum": ["E0", "E1", "E2", "E3", "E4", "E5"] },
          "status": { "type": "string", "enum": ["VERIFIED", "PARTIALLY_VERIFIED", "PROVISIONAL", "OPEN", "BLOCKED"] }
        }
      }
    },
    "hard_gate_status": {
      "type": "string",
      "enum": ["PASS", "BLOCKED", "INCONCLUSIVE"]
    },
    "decision": {
      "type": "string",
      "enum": ["QUALIFIED", "PROVISIONAL", "REJECTED"]
    },
    "timestamp": { "type": "string", "format": "date-time" }
  }
}
```

---

### 5.2. Invariant & Assumption Ledger Schema (`invariant.schema.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://rfl-qa.org/schemas/invariant.schema.json",
  "title": "InvariantLedgerEntry",
  "type": "object",
  "required": [
    "invariant_id",
    "enforcement_class",
    "description",
    "owner",
    "epistemic_status",
    "evidence_basis"
  ],
  "properties": {
    "invariant_id": { "type": "string", "pattern": "^INV-[ABCD]-[0-9]{3,}$" },
    "enforcement_class": {
      "type": "string",
      "enum": ["A_COMPILER", "B_API", "C_RUNTIME", "D_EXTERNAL"]
    },
    "description": { "type": "string" },
    "owner": { "type": "string" },
    "epistemic_status": {
      "type": "string",
      "enum": ["VERIFIED", "PARTIALLY_VERIFIED", "PROVISIONAL", "OPEN", "BLOCKED"]
    },
    "evidence_basis": {
      "type": "object",
      "required": ["nature", "details"],
      "properties": {
        "nature": {
          "type": "string",
          "enum": ["PROOF", "OBSERVATION", "COVERAGE_BOUNDED", "ABSENCE_OF_EVIDENCE", "SPECIFICATION"]
        },
        "details": { "type": "string" }
      }
    }
  }
}
```

---

## 6. The Execution Protocol for Assessor Teams

1. **Intake Migration Unit Dossier:** Verify completeness against `dossier.schema.json`. Reject ad-hoc code snippets or resumes lacking attached artifacts.
2. **Execute Primary Blind Evaluation:** Assessor A evaluates evidence records, test oracles, and the semantic diff independently.
3. **Execute Secondary Blind Evaluation:** Assessor B conducts an independent review without access to Assessor A's evaluation.
4. **Compare Concordance:** Run the inter-rater calibration check. If ratings diverge ($\Delta L > 0$ or status mismatch), halt and conduct reconciliation.
5. **Enforce Hard Safety Gates:** Verify zero blocker defects. If any memory corruption, data race, or context violation is detected, assign `BLOCKED`.
6. **Audit Assumption Debt:** Calculate the sum of unresolved Type D invariants:
   $$\text{Assumption Debt} = \sum (\text{PROVISIONAL}) + \sum (\text{OPEN}) + \sum (\text{UNKNOWN Semantic Dimensions})$$
7. **Issue Qualification Decision:** Record the derived 9-dimensional vector into `qualification.schema.json` and archive in the calibration repository.

---

## The Ultimate Standard

$$\mathbf{NO\ EVIDENCE \implies NO\ VERIFIED\ CLAIM}$$

$$\mathbf{NO\ CALIBRATION \implies NO\ VALIDATED\ SYSTEM}$$

An RFL engineer is not an evangelist for a programming language. They are a rigorous engineer of semantic interfaces operating across the physical machine, Linux C substrate, Rust type system, and the kernel upstream governance process.
