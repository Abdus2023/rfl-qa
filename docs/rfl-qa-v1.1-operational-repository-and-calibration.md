# RFL-QA v1.1: Operational Qualification Repository & Calibration Protocol

> A formally coherent, two-axis empirical measurement system for Rust-for-Linux engineering capability, incorporating the four specification freezes, the four-dimensional claim model, canonical repository architecture, machine-readable schemas, inter-rater reliability calibration, and downstream predictive outcome tracking.

---

## Preamble: The Four Specification Freezes

Before any schema, oracle, or adversarial lab is executed, four structural corrections are frozen into the specification. These are not minor refinements; they are **epistemic load-bearing walls**. Removing any one collapses the qualification system's empirical validity:

| Freeze | Axiom | What It Prevents |
| :--- | :--- | :--- |
| **F1** | **Evidence Tier $\neq$ Capability Level** ($E_n \not\implies L_n$) | A narrow, trivial merged upstream patch ($E_4$) from artificially inflating an engineer's capability claim to architectural competence ($L_4$). |
| **F2** | **Invariant Class $\perp$ Epistemic Status** (`UNKNOWN` $\neq$ Type D) | Misclassifying a poorly evidenced Type-B (API) invariant as a Type-D external assumption. Invariant class defines origin; epistemic status defines evidence state. |
| **F3** | **Defect $\neq$ Detection** (Observation $\neq$ Proof) | Treating absence-of-evidence as evidence-of-absence (`KASAN: PASS` is an observation over an executed trace population, not a universal proof of memory safety). |
| **F4** | **Unsafe Surface $\neq$ Line Ratio** | Optimizing for a cosmetic line-count ratio that rewards hiding unsafe code rather than auditing and encapsulating trust-boundary topology. |

---

## 1. The Two-Axis Qualification Model & 4-Dimensional Claim Record

Qualification within RFL-QA v1.1 is strictly evaluated across two independent axes:

```
                       RFL-QA QUALIFICATION
                               │
                  ┌────────────┴────────────┐
                  │                         │
             CAPABILITY                 EVIDENCE
                  │                         │
           L0  Unaware               E0  Self-assertion
           L1  Aware                 E1  Explanation / Interview
           L2  Practitioner          E2  Controlled impl
           L3  Independent           E3  Kernel lab artifact
           L4  Expert                E4  Upstream patch / review
           L5  Authority             E5  Sustained ownership
                  │                         │
                  └────────────┬────────────┘
                               │
                     ┌─────────┴─────────┐
                     │   INVARIANT CLASS │
                     │                   │
                     │  A  Compiler      │
                     │  B  API-design    │
                     │  C  Runtime       │
                     │  D  External      │
                     └─────────┬─────────┘
                               │
                     ┌─────────┴─────────┐
                     │ EPISTEMIC STATUS  │
                     │                   │
                     │  VERIFIED         │
                     │  PARTIAL          │
                     │  PROVISIONAL      │
                     │  OPEN             │
                     │  BLOCKED          │
                     └─────────┬─────────┘
                               │
                               ▼
                        QUALIFICATION
                     ┌─────────┴─────────┐
                     │                   │
                  VERIFIED         PROVISIONAL
                                     │
                                  BLOCKED
```

### The 4-Dimensional Claim Record Schema

Every qualified claim in the system is recorded as an immutable 4-tuple:

$$\mathbf{Q} = \Big\langle \mathbf{Capability}\ (L_0\text{--}L_5),\; \mathbf{Evidence}\ (E_0\text{--}E_5),\; \mathbf{Invariant\ Class}\ (\text{A/B/C/D}),\; \mathbf{Epistemic\ Status}\ (\text{VERIFIED}\dots\text{BLOCKED}) \Big\rangle$$

```yaml
# Schema: claim.schema.json
claim:
  competency_id: "C-047"
  title: "C callback registration and teardown races"
  domain: "C Semantics & FFI"

  capability:
    level: "L4"
    descriptor: "Can design cross-FFI callback lifetime protocols preventing teardown races"

  evidence:
    tier: "E4"
    artifact_type: "kernel_patch_series"
    artifact_ref: "lore.kernel.org/r/20260815-rust-callback-v3"
    environment:
      kernel: "v6.14-rc2"
      rust: "1.85.0"
      arch: "x86_64"
      config: "defconfig + RUST=y + PREEMPT_RT=y + CONFIG_KASAN=y + CONFIG_KCSAN=y"

  invariant:
    class: "B"  # API-enforceable (NOT Type-D)
    description: "Callback target lifetime dominates callback execution window via Pin + refcount"
    mechanism: "Pin + refcount guard tied to registration scope"

  epistemic_status: "PARTIAL"
  status_justification: "Type-level proof + KASAN/KCSAN pass under lab tests, but teardown stress-test under heavy RT load incomplete"

  qualification: "PROVISIONAL"  # Derived: L4 capability, E4 evidence, but PARTIAL epistemic status

  hard_gate:
    result: "PASS"
    checks:
      uaf: "NO_DEFECT_OBSERVED"
      double_free: "NO_DEFECT_OBSERVED"
      callback_after_free: "NO_DEFECT_OBSERVED"
      data_race: "NO_DEFECT_OBSERVED"

  limitations:
    - "Hardware callback ordering remains an external Type-D invariant (see Ledger A-012)"
    - "KCSAN coverage limited to 4-CPU x86_64; ARM64 weak ordering not yet exercised"

  derived_qualification: "L4-E4"
```

### Derivation Rules

The `qualification` determination is mathematically **derived**, never claimed directly:

| Capability | Evidence | Epistemic Status | Hard Gate Check | Derived Qualification |
| :---: | :---: | :---: | :---: | :---: |
| Any | $E_0$ | Any | Any | **BLOCKED** (No evidence) |
| Any | $E_1$--$E_2$ | `OPEN` | Any | **BLOCKED** (No verification) |
| $\ge L_2$ | $\ge E_2$ | `VERIFIED` | `PASS` | **VERIFIED** |
| $\ge L_2$ | $\ge E_3$ | `PARTIAL` | `PASS` | **PROVISIONAL** |
| $\ge L_3$ | $\ge E_4$ | `PROVISIONAL` | `PASS` | **PROVISIONAL** |
| Any | Any | `BLOCKED` | Any | **BLOCKED** |
| Any | Any | Any | `FAIL` | **BLOCKED** |

### Evidence Strength Qualifiers (Freeze F3)

Every verification entry must specify its empirical strength qualifier:

* **PROOF:** Formally or mechanically demonstrated within stated assumptions (e.g., Rust borrow checker proving `&T` cannot outlive `T`).
* **OBSERVATION:** Empirically observed under a defined test population without defect detection (e.g., KASAN reporting no UAF across $10^6$ syzkaller iterations).
* **COVERAGE:** Quantified fraction of relevant state space, interleavings, or inputs exercised.
* **ABSENCE_OF_EVIDENCE:** No test or proof has been executed; explicitly distinguished from "no defect."

---

## 2. Canonical Repository Architecture

```text
rfl-qa/
├── SPEC.md                          # The normative operational specification (v1.1)
├── GOVERNANCE.md                    # Assessor certification, appeal, and spec revision process
├── CHANGELOG.md                     # Revision history driven by calibration divergence events
│
├── competency/                      # ~100 atomic competency definitions
│   ├── registry.yaml                # Master index of competencies
│   ├── C001-cpu-privilege.yaml
│   ├── C002-mmu-pagetables.yaml
│   ├── ...
│   ├── C047-callback-teardown.yaml
│   ├── ...
│   └── C100-upstream-rfc.yaml
│
├── invariants/                      # Invariant classification reference library
│   ├── _taxonomy.md                 # Formal A/B/C/D taxonomy definitions
│   ├── A-compiler/
│   │   ├── A01-lifetime.yaml
│   │   ├── A02-aliasing.yaml
│   │   └── A03-send-sync.yaml
│   ├── B-api/
│   │   ├── B01-lock-guard-lifetime.yaml
│   │   ├── B02-context-restriction.yaml
│   │   └── B03-callback-pin.yaml
│   ├── C-runtime/
│   │   ├── C01-lockdep-ordering.yaml
│   │   ├── C02-kasan-bound.yaml
│   │   └── C03-refcount-overflow.yaml
│   └── D-external/
│       ├── D01-c-subsystem-contract.yaml
│       ├── D02-hardware-ordering.yaml
│       └── D03-firmware-data.yaml
│
├── evidence/                        # Evidence schemas and calibrated records
│   ├── schema.yaml                  # Evidence record schema
│   ├── strength-qualifiers.md       # PROOF / OBSERVATION / COVERAGE / ABSENCE
│   └── examples/
│       ├── e4-rcu-abstraction.yaml
│       ├── e3-pin-init-lab.yaml
│       └── e2-ffi-wrapper.yaml
│
├── oracles/                         # Formal adversarial test oracles
│   ├── _oracle-schema.yaml
│   ├── teardown/
│   │   ├── oracle.md                # Formal concurrent teardown oracle
│   │   ├── state-machine.yaml       # CREATE -> ... -> FREE lifecycle
│   │   └── interleavings.yaml       # Adversarial scheduler injection patterns
│   ├── semantic-diff/
│   │   ├── oracle.md
│   │   ├── dimensions.yaml          # 13 required diff dimensions
│   │   └── template.yaml
│   ├── context/
│   │   ├── oracle.md
│   │   └── context-matrix.yaml      # Process / IRQ / Softirq / Preempt matrix
│   └── ffi/
│       ├── oracle.md
│       └── contract-checklist.yaml  # 11-point FFI contract audit
│
├── labs/                            # 15 Standardized adversarial qualification labs
│   ├── _lab-schema.yaml
│   ├── 001-pin-init/                # In-place self-referential initialization
│   ├── 002-rcu-guard/               # RCU read-side critical sections & grace periods
│   ├── 003-callback-lifetime/       # Asynchronous callback teardown races
│   ├── 004-ffi-wrapper/             # Raw C binding to safe abstraction wrapping
│   ├── 005-lockdep-integration/     # Lock class keys and inversion prevention
│   ├── 006-dma-ownership/           # Cache flushing, IOMMU, and device ownership
│   ├── 007-workqueue-teardown/      # cancel_work_sync vs module unload races
│   ├── 008-semantic-diff/           # 13-dimension C-to-Rust contract mapping
│   ├── 009-unsafe-audit/            # Trust-boundary accounting & invariant proofs
│   ├── 010-assumption-ledger/       # Type-D risk quantification & tracking
│   ├── 011-kunit-kasan/             # In-tree unit testing and sanitizer triage
│   ├── 012-context-restriction/     # Sleepable vs atomic context type enforcement
│   ├── 013-abstraction-quality/     # Evaluating leakage, composability, and overhead
│   ├── 014-migration-unit/          # Full Migration Unit design and packet assembly
│   └── 015-governance-rfc/          # LKML RFC defense and maintainer negotiation
│
├── dossiers/                        # Candidate qualification dossiers
│   ├── _dossier-schema.yaml
│   ├── template/
│   │   ├── capability-vector.yaml
│   │   ├── evidence-log.yaml
│   │   ├── assumption-ledger.yaml
│   │   ├── unsafe-inventory.yaml
│   │   └── semantic-diff.yaml
│   └── examples/
│       └── candidate-anon-001/
│
├── assessors/                       # Evaluation protocols and rubrics
│   ├── rubric.md                    # Objective scoring rubrics per competency
│   ├── review-protocol.md           # Blind dual-assessor review procedures
│   ├── certification.md             # Assessor qualification requirements
│   └── conflict-resolution.md       # Assessor disagreement protocol
│
├── calibration/                     # THE EMPIRICAL FEEDBACK LOOP
│   ├── inter-rater.md               # Inter-rater reliability measurement protocol
│   ├── divergence-thresholds.yaml   # Quantitative triggers for spec revisions
│   ├── historical-cases/            # Calibrated "gold standard" historical case studies
│   │   ├── case-001-false-positive.yaml
│   │   └── case-002-false-negative.yaml
│   └── drift-detection.yaml         # Downstream defect rate and drift metrics
│
├── schemas/                         # Machine-readable JSON Schemas
│   ├── claim.schema.json
│   ├── evidence.schema.json
│   ├── dossier.schema.json
│   ├── invariant.schema.json
│   ├── qualification.schema.json
│   ├── unsafe-inventory.schema.json
│   ├── assumption-ledger.schema.json
│   └── semantic-diff.schema.json
│
└── tools/                           # Automated validation and analysis tooling
    ├── validate-dossier.py          # Schema validation for dossiers
    ├── compute-qualification.py     # Derivation rule evaluation engine
    └── calibration-report.py        # Assessor divergence and drift report generator
```

---

## 3. Core Schema Definitions

### 3.1 Competency Definition
```yaml
# competency/C047-callback-teardown.yaml
id: "C047"
domain: "C Semantics & FFI"
title: "C callback registration and teardown races"
description: >
  Design and implement safe Rust wrappers for C APIs that register
  callbacks, ensuring the callback target outlives all possible
  invocations including concurrent teardown.

levels:
  L1: "Can explain callback-after-free and registration races conceptually."
  L2: "Can use existing kernel:: callback abstractions correctly without panicking."
  L3: "Can design a new callback wrapper utilizing Pin + refcount guards."
  L4: "Can resolve callback teardown races across FFI with concurrent module removal."
  L5: "Can establish subsystem-wide callback lifecycle and unregister policy."

required_invariants:
  - class: "B"
    description: "Callback target lifetime dominates all possible invocations"
  - class: "C"
    description: "Teardown synchronization prevents callback invocation post-unregister"
  - class: "D"
    description: "C subsystem core honors unregister completion semantics"

hard_gate_conditions:
  - "Demonstrated callback-after-free in any test"
  - "Missing teardown synchronization prior to object free"
  - "Unsynchronized concurrent access to callback target state"

super_gates:
  - "teardown"
  - "semantic-diff"
```

---

### 3.2 Invariant Record (Freeze F2: Orthogonal Axes)
```yaml
# invariants/B-api/B03-callback-pin.yaml
id: "B03"
class: "B"  # API-enforceable
title: "Callback lifetime dominated by wrapper via Pin + refcount"
description: >
  The safe Rust API ensures that a registered callback's target
  object cannot be moved in memory (Pin) or deallocated (refcount)
  while the C subsystem may still invoke the callback.

epistemic_requirements:
  VERIFIED:
    - "Type system proof: Pin guarantees address stability"
    - "Refcount proof: Reference count held during active registration"
    - "Teardown test: Callback drain completes before refcount release"
  PARTIAL:
    - "Type system proof exists, but teardown stress-test under RT load is incomplete"
  PROVISIONAL:
    - "Design appears sound by inspection, but no adversarial test executed"
  OPEN:
    - "No empirical evidence beyond design intent"
  BLOCKED:
    - "Adversarial test demonstrated callback-after-free"

# NOTE: This is a Type-B invariant. If its epistemic status is PROVISIONAL,
# that means the API-design invariant is incompletely evidenced. It does NOT
# become a Type-D external assumption.
```

---

### 3.3 Unsafe Surface Inventory (Freeze F4: Topology, Not Lines)
```yaml
# dossiers/template/unsafe-inventory.yaml
migration_unit: "block-layer-rust-wrapper"
assessed_by: "assessor-007"
date: "2026-09-27"

boundaries:
  - id: "UB-01"
    type: "ffi_call"
    location: "rust/kernel/block/ffi.rs:42"
    description: "Call to blk_mq_alloc_request"
    invariants_required: ["A01-lifetime", "B01-lock-guard"]
    evidence: ["kunit-block-01", "kasan-run-03"]
    reviewed_by: ["maintainer-primary"]
    status: "VERIFIED"

  - id: "UB-02"
    type: "callback_boundary"
    location: "rust/kernel/block/queue.rs:118"
    description: "C block layer invokes Rust completion callback trampoline"
    invariants_required: ["B03-callback-pin", "D01-c-subsystem-contract"]
    evidence: ["kunit-block-02"]
    reviewed_by: []
    status: "PARTIAL"

metrics:
  unsafe_block_count: 14
  ffi_call_count: 8
  callback_boundary_count: 3
  dma_boundary_count: 2
  synchronization_boundary_count: 5
  external_assumption_count: 4

  # Inventory statistics (informative only):
  unsafe_lines: 87
  total_lines: 2340

  # Active safety metrics (evaluative):
  invariant_coverage: "11 of 15 identified invariants have verified evidence"
  review_coverage: "9 of 14 unsafe blocks independently reviewed by L4+ assessor"
  unresolved_assumptions: 2
  verification_coverage: "4 of 7 teardown interleavings empirically tested"
```

---

### 3.4 Assumption Ledger (Tracking Type-D Debt)
```yaml
# dossiers/template/assumption-ledger.yaml
migration_unit: "block-layer-rust-wrapper"

assumptions:
  - id: "A-001"
    description: "blk_mq_free_request will not be called on an already-freed request"
    invariant_class: "D"  # External: C block layer contract
    owner: "block subsystem maintainers"
    evidence:
      type: "source audit + KUnit"
      status: "VERIFIED"
    risk_if_wrong: "Double-free, kernel panic"

  - id: "A-002"
    description: "DMA completion interrupt fires after DMA engine writes are coherent"
    invariant_class: "D"  # External: hardware contract
    owner: "architecture maintainer"
    evidence:
      type: "datasheet section 7.3"
      status: "PROVISIONAL"  # Ambiguous ordering in vendor documentation
    risk_if_wrong: "Stale data read, silent memory corruption"

  - id: "A-003"
    description: "Rust wrapper outlives all registered callbacks"
    invariant_class: "B"  # API-enforceable
    owner: "RFL engineer"
    evidence:
      type: "Pin + refcount type proof + teardown test"
      status: "VERIFIED"
    risk_if_wrong: "Use-after-free, privilege escalation"

assumption_debt_summary:
  total_count: 12
  verified_count: 8
  partial_count: 2
  provisional_count: 2
  open_count: 0
  blocked_count: 0
  debt_rating: "MEDIUM"  # Driven by provisional count and severity of failure
```

---

### 3.5 The Canonical 13-Dimension Semantic Diff
```yaml
# dossiers/template/semantic-diff/diff-block-wrapper.yaml
migration_unit: "block-layer-rust-wrapper"
c_baseline: "block/blk-mq.c @ v6.12"
rust_implementation: "rust/kernel/block/ @ patch-v3"

dimensions:
  inputs:
    status: "UNCHANGED"
    notes: "Same request parameters passed through FFI"
  outputs:
    status: "UNCHANGED"
    notes: "Same completion status codes, translated to Result<T, Error>"
  errors:
    status: "INTENTIONALLY_CHANGED"
    notes: "C ERR_PTR convention replaced with Rust Result; semantically equivalent"
    justification: "Type-B invariant: error state is unrepresentable as valid pointer"
  ownership:
    status: "INTENTIONALLY_CHANGED"
    notes: "Implicit C ownership conventions -> explicit Rust ownership via types"
    justification: "Core migration objective"
  lifetime:
    status: "INTENTIONALLY_CHANGED"
    notes: "Manual refcount discipline -> Rust refcount + Pin"
    justification: "Core migration objective"
  locking:
    status: "UNCHANGED"
    notes: "Same spinlock protects same data; Rust wrapper uses kernel::sync::SpinLock"
  atomicity:
    status: "UNCHANGED"
    notes: "Same atomic operations for request state transitions"
  execution_context:
    status: "UNKNOWN"  # LEGITIMATE: triggers an action item, NOT failure
    notes: "Unclear whether Rust completion callback can be invoked from NMI context"
    action_required: "Audit C block layer NMI paths; may require Type-C runtime check"
  callbacks:
    status: "INTENTIONALLY_CHANGED"
    notes: "C function pointer -> Rust trait object with Pin guarantee"
    justification: "Type-B invariant enforcement"
  side_effects:
    status: "UNCHANGED"
    notes: "Same hardware register writes via same MMIO paths"
  ordering:
    status: "UNCHANGED"
    notes: "Same memory barriers; Rust uses kernel atomic primitives"
  teardown:
    status: "INTENTIONALLY_CHANGED"
    notes: "Added explicit callback drain phase before memory free"
    justification: "Addresses C code's implicit assumption about quiescence"
  negative_space:
    status: "NOT_APPLICABLE"
    notes: >
      Rust wrapper does NOT guarantee: hardware correctness, C block layer
      internal consistency, scheduling fairness, or I/O ordering beyond
      what the C baseline provided.

unknown_count: 1
unknown_dimensions: ["execution_context"]
```

---

## 4. The Calibration Engine & Inter-Rater Feedback Loop

A qualification system is only as valid as its inter-rater reliability. If Assessor A and Assessor B evaluate the same dossier and diverge, **the qualification specification has failed**, not the candidate.

### 4.1 Inter-Rater Reliability (IRR) Protocol

```
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    ▼                                                     │
  SPEC (v1.1)                                             │
    │                                                     │
    ▼                                                     │
  LAB / ORACLE                                            │
    │                                                     │
    ▼                                                     │
  CANDIDATE ARTIFACT                                      │
    │                                                     │
    ▼                                                     │
  ASSESSOR A ──┐                                          │
               ├──► DIVERGENCE CHECK                      │
  ASSESSOR B ──┘       │                                  │
                       ▼                                  │
               ┌─── ACCEPTABLE? ───┐                      │
               │                   │                      │
              YES                  NO                     │
               │                   │                      │
               ▼                   ▼                      │
         QUALIFICATION      SPEC REVISION                 │
         ISSUED             TRIGGERED                     │
               │                   │                      │
               ▼                   │                      │
         REAL UPSTREAM             │                      │
         OUTCOME                   │                      │
               │                   │                      │
               ▼                   │                      │
         CALIBRATION ◄─────────────┘                      │
         DATA                                             │
               │                                          │
               └──────────────────────────────────────────┘
```

1. **Blind Dual Assessment:** Every artifact submitted for $L_3$ or above must be evaluated independently by two certified assessors.
2. **Evaluated Tuple Comparison:** Assessors independently record:
   - Capability Level ($\Delta L$)
   - Evidence Tier ($\Delta E$)
   - Invariant Class (A / B / C / D)
   - Epistemic Status (`VERIFIED` $\dots$ `BLOCKED`)
   - Hard Safety Gate Result (`PASS` / `BLOCKED`)
3. **Acceptance Thresholds:**
   - $\Delta L \le 1$ level
   - $\Delta E \le 1$ tier
   - Invariant Class must agree **exactly**
   - Hard Gate determination must agree **exactly**
4. **Discrepancy Logging:** Any divergence beyond acceptable thresholds halts qualification and logs a **Calibration Event**.

---

### 4.2 Historical Calibration Cases (Gold Standards)
```yaml
# calibration/historical-cases/case-001-false-positive.yaml
case_id: "CAL-001"
type: "false_positive"
description: >
  Candidate qualified L4-E4 in C/FFI based on merged driver patch series.
  Six months later, a UAF was discovered in the abstraction under a
  PREEMPT_RT kernel configuration not exercised in the original testbed.
root_cause: >
  Original verification environment omitted PREEMPT_RT. Invariant B03
  was classified as VERIFIED when it should have been PROVISIONAL for
  real-time configurations where spinlocks become sleeping rt_mutexes.
spec_revision: "v1.1 Freeze F3: Mandated PREEMPT_RT in core verification matrix"
```

---

### 4.3 Specification Revision Triggers

The normative specification (`SPEC.md`) is flagged for mandatory revision when:
1. Inter-rater agreement drops below **80%** in any domain across 10 consecutive assessments.
2. A single `hard_gate` disagreement occurs between two certified assessors.
3. A `VERIFIED` qualification is contradicted by an upstream kernel regression (false positive).
4. A new class of kernel bug emerges that cannot be categorized under the A/B/C/D invariant taxonomy.

---

## 5. The Seven Governing Axioms (Constitution of RFL-QA)

These seven axioms govern all operational decisions within RFL-QA v1.1. No assessor, rubric, or review protocol may override them:

$$\begin{aligned}
\mathbf{G1.} & \quad \text{No evidence, no claim.} & \implies & \quad \text{evidence\_tier} = E_0 \implies \text{qualification} = \mathbf{BLOCKED} \\
\mathbf{G2.} & \quad \text{No oracle, no test.} & \implies & \quad \text{Super-Gates require formal adversarial interleaving models} \\
\mathbf{G3.} & \quad \text{No assumption, no boundary.} & \implies & \quad \text{Every Type-D invariant must appear in the Assumption Ledger} \\
\mathbf{G4.} & \quad \text{No teardown, no lifetime.} & \implies & \quad \text{Lifetime claims require a teardown model verified under race conditions} \\
\mathbf{G5.} & \quad \text{No semantic diff, no equivalence.} & \implies & \quad \text{Migration requires a 13-dimension diff with explicit \texttt{UNKNOWN} tracking} \\
\mathbf{G6.} & \quad \text{Evidence} \neq \text{Capability.} & \implies & \quad \text{Evidence tier and capability level are strictly independent dimensions} \\
\mathbf{G7.} & \quad \text{No calibration, no validity.} & \implies & \quad \text{The qualification system is unvalidated without proven inter-rater reliability}
\end{aligned}$$

---

## Summary Statement

RFL-QA v1.1 is not an academic essay or a curriculum wishlist. It is a **deterministic, calibratable, and falsifiable measurement system**. 

It provides the Linux kernel community with an empirical harness to ensure that Rust integration is guided by **mathematical and operational rigor**, shrinking implicit assumptions, bounding external risk, and protecting the stability of the operating system.
