# RFL Qualification System v3.1: Evidence Execution Layer (Executable Standard)

> A deterministic, evidence-based qualification standard for measuring Rust-for-Linux engineering capability across multi-dimensional competency vectors, five-tier empirical evidence hierarchies ($E_0$–$E_5$), machine-readable evidence records, non-compensable safety gates, explicit adversarial test oracles, canonical semantic diffs, assumption ledgers, and migration unit assessments.

---

## Epistemic Grounding & Definition of the Standard

> **The framework itself is a normative engineering specification. Its empirical grounding must come from evidence produced by applying it to real RFL/Linux code and real qualification exercises.**

This framework defines a **proposed evidence-based qualification standard for RFL engineering**. A qualification standard cannot declare itself "definitive" by assertion; it becomes authoritative exclusively through upstream adoption, dual-assessor calibration, reproducible adversarial verification, and long-term tracking of downstream kernel defect rates.

---

## The Five Governing Qualification Axioms

$$\begin{aligned}
\mathbf{1.} & \quad \text{NO EVIDENCE} & \implies & \quad \text{NO VERIFIED CLAIM} \\
\mathbf{2.} & \quad \text{NO ORACLE} & \implies & \quad \text{NO MEANINGFUL TEST} \\
\mathbf{3.} & \quad \text{NO EXPLICIT ASSUMPTION} & \implies & \quad \text{NO TRUST BOUNDARY} \\
\mathbf{4.} & \quad \text{NO TEARDOWN MODEL} & \implies & \quad \text{NO LIFETIME CLAIM} \\
\mathbf{5.} & \quad \text{NO SEMANTIC DIFF} & \implies & \quad \text{NO MIGRATION-EQUIVALENCE CLAIM}
\end{aligned}$$

### Core Invariant Principle
> **A capability is qualified only to the extent that its claimed invariant has been demonstrated under an explicitly defined environment, adversarial test model, and evidence boundary.**

---

## 1. The Evidence Record: Eliminating Unverified Labels

A proficiency claim (such as "L4" or "Senior RFL Engineer") **must never exist by itself**. Every capability determination is a **derived state** resulting from a machine-verifiable Evidence Record:

```
Capability Claim
       │
       ▼
Evidence Record
       │
       ├── competency_id
       ├── claimed_level
       ├── evidence_context
       ├── artifact
       ├── environment
       ├── test_oracle
       ├── adversarial_cases
       ├── reviewer
       ├── result
       ├── limitations
       └── timestamp
               │
               ▼
       Qualification Decision
```

### Canonical Evidence Record Format
```yaml
competency: C-47
title: "C callback registration and teardown races"

claim:
  level: L4
  context: E4

artifact:
  type: kernel_patch_series
  revision: "git:git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git@a7b9c1d4e2f8"

environment:
  kernel_commit: "v6.12-rc4"
  rustc_version: "1.85.0"
  arch: "x86_64"
  config: "defconfig + CONFIG_RUST=y + CONFIG_PROVE_LOCKING=y + CONFIG_KASAN=y + CONFIG_KCSAN=y"

verification:
  kunit: PASS
  lockdep: PASS
  kasan: PASS
  kcsan: PASS
  syzkaller: PASS (120 CPU-hours, 0 crashes)

adversarial_tests:
  callback_after_unregister: PASS
  concurrent_remove: PASS
  double_unregister: PASS
  final_reference_release: PASS

review:
  assessor_primary: "kernel-subsystem-maintainer-id"
  assessor_secondary: "rfl-maintainer-id"
  disposition: PASS

limitations:
  - "Hardware interrupt controller callback ordering remains external Type D invariant."

status: VERIFIED
```

---

## 2. Five-Tier Evidence Hierarchy ($E_0$ to $E_5$)

The simplistic `C/P/U` classification is expanded into five strictly delineated empirical evidence tiers:

| Tier | Designation | Concrete Meaning | Qualification Strength |
| :---: | :--- | :--- | :--- |
| **$E_0$** | **Self-Assertion** | Unverified resume claims, portfolio links, conversational assertions. | **Zero qualification.** Cannot support any claim. |
| **$E_1$** | **Explanation / Interview** | Can verbally articulate concepts, trace code flow, answer oral defense questions. | **KNOW evidence.** Supports $L_1$. |
| **$E_2$** | **Controlled Implementation** | Implements standard drivers or patterns in isolated lab exercises or synthetic testbeds. | **USE evidence.** Supports $L_2$. |
| **$E_3$** | **Kernel Laboratory Artifact** | Solves complex, adversarial kernel exercises under KASAN, KCSAN, lockdep, and fault-injection. | **AUDIT / DESIGN lab evidence.** Supports $L_3$ or lab $L_4$. |
| **$E_4$** | **Upstream-Quality Patch / Review** | Author of public in-tree patch series surviving adversarial LKML review, or reviewer discovering defects in others' upstream code. | **Production evidence.** Required for operational $L_3/L_4$. |
| **$E_5$** | **Maintained Subsystem Responsibility** | Sustained long-term architectural stewardship, toolchain maintenance, and ABI stability management. | **Sustained authority evidence.** Required for $L_5$. |

### The Separation of Evidence and Capability
$$\mathbf{Higher\ Evidence\ Tier \neq Higher\ Capability\ Level}$$

An engineer with an $E_5$ artifact (e.g., maintaining a small driver for five years) may demonstrate only $L_3$ competence in that narrow domain. Conversely, a candidate may demonstrate $L_4$ design capability within an $E_3$ laboratory scenario. 

*A merged patch is not proof of architectural mastery; it is merely an $E_4$ artifact within a bounded scope.*

---

## 3. Multidimensional Capability Vectors

Qualification must **never collapse into a single aggregate score** (e.g., "Score: 4.2/5"). Aggregations create false precision and permit dangerous compensation between unrelated domains (e.g., compensating for bad concurrency skills with excellent macro programming).

Capability is recorded strictly as a **9-Domain Vector**:

$$\mathbf{C}_{\text{RFL}} = \begin{bmatrix}
\text{Hardware \& Architecture} \\
\text{Linux Core Internals} \\
\text{Concurrency \& LKMM} \\
\text{C Semantics \& FFI} \\
\text{Rust Language \& no\_std} \\
\text{RFL \texttt{kernel} Crate Design} \\
\text{Verification \& Observability} \\
\text{Toolchain \& Build Engineering} \\
\text{Governance \& Migration Architecture}
\end{bmatrix}$$

### Example Operational Profile
```
Hardware & Architecture:      L3 [E3]
Linux Core Internals:         L4 [E4]
Concurrency & LKMM:           L4 [E4]
C Semantics & FFI:            L5 [E5]
Rust Language & no_std:       L5 [E5]
RFL kernel Crate Design:      L4 [E4]
Verification & Observability: L3 [E3]
Toolchain & Build:            L2 [E2]
Governance & Migration:       L3 [E4]
```

This vector immediately informs an upstream maintainer that the candidate can independently design core FFI and language abstractions, but must not be assigned to maintain Kbuild toolchain infrastructure or lead cross-subsystem political negotiations.

---

## 4. Non-Compensable Safety Blockers (Hard Gates)

No amount of expertise in Rust, type systems, or architecture can compensate for a safety violation in kernel space.

```
                 ┌──────────────────────┐
                 │ Candidate Evaluation │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Capability     Evidence       Safety
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     HARD GATE CHECK
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
        PASS              BLOCKED          INCONCLUSIVE
```

### Automatic Blocker Conditions
The presence of any of the following defects in a candidate's artifact triggers an **immediate, unconditional BLOCKED status**:

1. **Use-After-Free (UAF):** Any reachable execution path permitting access to deallocated memory.
2. **Double-Free:** Any path triggering duplicate reclamation of memory or resources.
3. **Unsound `unsafe` Block:** An `unsafe` block whose safety comment is false, incomplete, or invalid under adversarial inputs.
4. **Data Race:** Unsynchronized concurrent access to shared mutable memory under LKMM or Rust rules.
5. **Introduced Deadlock:** Lock ordering inversion, AB-BA deadlock, or sleep-inside-spinlock detected by lockdep.
6. **Incorrect Lifetime Invariant:** A Rust reference escaping the lifetime of its underlying C or hardware object.
7. **ABI Incompatibility:** Corrupting structure padding, alignment, bitfield layout, or calling convention where compatibility is required.
8. **Prohibited Execution Context Violation:** Calling a sleeping function or allocating memory (`GFP_KERNEL`) from an atomic, IRQ, or RCU read-side critical section.
9. **Incorrect DMA Ownership:** CPU accessing DMA buffer memory while ownership resides with the hardware device.
10. **Callback-After-Free:** An asynchronous callback invoking code on an object that has initiated deallocation.
11. **Missing Teardown Synchronization:** Failure to flush workqueues, cancel timers, or wait for RCU grace periods prior to resource destruction.
12. **Unexplained Semantic Regression:** Unjustified alteration of C-side error codes, side effects, or ordering.

---

## 5. Explicit Adversarial Test Oracles

A qualification test without an explicit oracle is merely an impressionistic code review. Every Super-Gate must specify its **Formal Test Oracle**.

### Example: Concurrent Teardown Oracle

#### Candidate Artifact Lifecycle
$$\text{CREATE} \longrightarrow \text{REGISTER} \longrightarrow \text{ACTIVE} \longrightarrow \text{STOP} \longrightarrow \text{QUIESCE} \longrightarrow \text{CALLBACK DRAIN} \longrightarrow \text{REFERENCE DRAIN} \longrightarrow \text{DESTROY} \longrightarrow \text{FREE}$$

#### Adversarial Execution Interleavings (Test Harness)
* **Thread 1 (Worker/User):** `ioctl()` $\parallel$ **Thread 2 (Sysfs):** `remove()`
* **Thread 1 (Core):** `c_callback()` $\parallel$ **Thread 2 (Driver):** `unregister()`
* **Thread 1 (Caller):** `final_ref_release()` $\parallel$ **Thread 2 (Allocator):** `free()`
* **Thread 1 (Reader):** `rcu_read_lock()` $\parallel$ **Thread 2 (Writer):** `destroy()`
* **Thread 1 (Timer/Work):** `work_handler()` $\parallel$ **Thread 2 (Unload):** `cancel_work_sync()`

#### The Formal Oracle
The candidate passes if and only if they mathematically and empirically demonstrate:

$$\begin{aligned}
\forall \text{ execution interleavings}: & \\
\text{alive}(\text{ref}) & \implies \text{object\_alive}(\text{target}) \\
\text{callback\_possible}(\text{target}) & \implies \text{callback\_target\_alive}(\text{target}) \\
\text{free}(\text{object}) & \implies \left(
\begin{aligned}
& \neg \text{live\_reference}(\text{object}) \;\wedge \\
& \neg \text{callback\_possible}(\text{object}) \;\wedge \\
& \neg \text{RCU\_reader}(\text{object}) \;\wedge \\
& \neg \text{registered\_owner}(\text{object})
\end{aligned}
\right)
\end{aligned}$$

---

## 6. The Canonical Semantic Diff

Line-by-line syntax comparison is banned. The candidate must produce a structured **Semantic Diff** evaluating the delta between C semantics and the proposed Rust abstraction:

```
SEMANTIC-DIFF
                  C implementation
                         │
                         ▼
                ┌─────────────────┐
                │ Contract model  │
                └────────┬────────┘
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
     Observable      Lifecycle        Concurrency
      behavior        behavior          behavior
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                 Rust implementation
                         │
                         ▼
                  Semantic Delta
```

### The 12 Canonical Dimensions
1. **Inputs & Validation:** Range, nullability, alignment, out-of-band sentinel values.
2. **Outputs & Returns:** Reference borrowing vs owned handles, error encapsulation.
3. **Error Representation:** Mapping negative C integers, `ERR_PTR`, and `NULL` to `Result<T, Error>`.
4. **Ownership:** Shared, exclusive, or borrowed; transfer of destruction duty.
5. **Lifetime:** Lexical vs dynamic; reference counting; parent-child binding.
6. **Locking Contracts:** Locks required on entry; locks acquired internally; lockdep annotations.
7. **Atomicity:** Critical section boundaries; wait-free vs lock-free paths.
8. **Execution Context:** Sleepable vs atomic; IRQ, softirq, process constraints.
9. **Callbacks & Asynchrony:** Re-entrancy guarantees; execution context of trampolines.
10. **Side Effects & Memory Ordering:** Hardware MMIO writes; explicit memory barriers (`smp_mb`).
11. **Teardown Sequence:** Drain ordering, quiescence barriers, cleanup guarantees.
12. **Negative Space:** Explicitly unenforced invariants; external dependency boundaries.

### Dimension Classification Status
Every dimension in the Semantic Diff must be assigned one of five explicit classifications:
* `UNCHANGED` — Exact semantic parity preserved.
* `INTENTIONALLY_CHANGED` — Deliberately altered (e.g., converting runtime check to compile-time guard; must be justified).
* `ACCIDENTALLY_CHANGED` — Unintended drift from C behavior (Defect).
* `UNKNOWN` — Semantic contract cannot be established from source/docs (Requires investigation).
* `NOT_APPLICABLE` — Dimension does not apply to this boundary.

> **`UNKNOWN` is a legitimate and valued engineering result.** Forcing every question into PASS/FAIL breeds invented certainty and dangerous assumptions.

---

## 7. Assumption Debt & The Assumption Ledger

Every migration accumulates unverified assumptions about external C subsystem behavior, hardware quirks, and firmware contracts (Type D invariants).

An RFL project must maintain an **Assumption Ledger**:

| ID | Stated Assumption | Type | Owner | Evidence Base | Epistemic Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **A-01** | C core cannot invoke device callbacks after `device_del()` completes. | **D** | Subsystem C Core | C source audit + KUnit test | `VERIFIED` |
| **A-02** | DMA address remains mapped until completion interrupt fires. | **D** | Hardware Driver | DMA API documentation | `VERIFIED` |
| **A-03** | Rust wrapper lifetime strictly bounds callback trampoline existence. | **B** | Rust Abstraction | Rust type system proof | `VERIFIED` |
| **A-04** | Hardware registers preserve written configuration across soft resets. | **D** | Hardware Silicon | Vendor Datasheet Rev 1.2 | `PROVISIONAL` |
| **A-05** | Memory barrier in C helper establishes acquire semantics across archs. | **C** | LKMM / Arch | LKMM `litmus` test missing | `OPEN` |

### Architectural Formula: Assumption Debt
$$\mathbf{\text{Assumption Debt}} = \sum \text{Unverified Assumptions} + \sum \text{Weak External Contracts} + \sum \text{Semantic Unknowns}$$

A migration that replaces 10,000 lines of C with Rust but increases Assumption Debt has **increased total system risk**, not decreased it.

---

## 8. Migration Risk Accounting

A Migration Architect must maintain an explicit risk evaluation across nine operational vectors:

$$\mathbf{Risk\ Vector} = \begin{bmatrix}
\text{Unsafe Surface Area} \\
\text{External Assumptions (Type D Debt)} \\
\text{Semantic Unknowns} \\
\text{Concurrency Complexity} \\
\text{ABI Exposure (Userspace vs FFI)} \\
\text{Toolchain Dependencies (Unstable Features)} \\
\text{Verification Gaps (Sanitizer Coverage)} \\
\text{Review Bandwidth \& Complexity} \\
\text{Performance \& Overhead Uncertainty}
\end{bmatrix} \longrightarrow \begin{pmatrix}
\mathbf{LOW} \\
\mathbf{MEDIUM} \\
\mathbf{HIGH} \\
\mathbf{BLOCKED}
\end{pmatrix}$$

Every risk rating must be justified by specific entries in the Trust-Boundary Inventory and Assumption Ledger.

---

## 9. The Migration Unit as the Fundamental Assessment Object

Assessments must **never be conducted on isolated, synthetic Rust exercises**. The fundamental unit of qualification is the **Migration Unit**:

```
                    MIGRATION UNIT
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
      Semantics       Implementation     Evidence
         │                │                │
     C contracts       Rust/FFI          Tests
     Ownership         kernel API        Sanitizers
     Context           Unsafe core       Benchmarks
     LKMM              Kbuild            Review
     Teardown          Integration       Hardware
         │                │                │
         └────────────────┼────────────────┘
                          ▼
                    Compatibility
                          │
                          ▼
                       Upstream
```

### Complete Migration Unit Deliverable Checklist
1. **Existing C Interface & Invariant Specification**
2. **Canonical Semantic Diff (12 Dimensions)**
3. **Teardown-First Lifecycle State Machine**
4. **Trust-Boundary Inventory & Minimization Proof**
5. **Assumption Ledger & Debt Accounting**
6. **Safe Rust Abstraction (`kernel::`) & In-Tree Reference Driver**
7. **KUnit Test Suite & Adversarial Concurrency Tests**
8. **Sanitizer Execution Evidence (KASAN, KCSAN, lockdep, Syzkaller)**
9. **Zero-Overhead Performance Benchmark Results**
10. **Upstream Review History (`git send-email` / LKML review responses)**

---

## 10. The Complete RFL-QA v1.0 Executable Architecture

To execute reproducible assessments, the framework couples the curriculum directly to executable harnesses:

$$\begin{aligned}
& 9 \text{ Domains} \\
\times & \text{ 100-Competency Registry} \\
\times & \text{ 5 Evidence Tiers } (E_0\text{--}E_5) \\
\times & \text{ 5 Non-Compensable Safety Gates} \\
\times & \text{ 15 Adversarial Laboratory Scenarios} \\
\times & \text{ Formal Test Oracles} \\
\times & \text{ Assumption Ledgers} \\
\times & \text{ Canonical Semantic Diffs} \\
\times & \text{ Trust-Boundary Inventories} \\
\times & \text{ Dual-Assessor Review Protocol} \\
= & \quad \mathbf{REPRODUCIBLE\ RFL\ QUALIFICATION}
\end{aligned}$$

---

## Final Standard Statement

This specification does not measure how enthusiastically an engineer advocates for Rust. It measures their ability to **engineer verifiable semantic boundaries under kernel reality**.

The definitive metric of the discipline remains:

$$\mathbf{M} = \frac{\Delta \text{ Implicit Risk Converted to Explicit, Reviewable, Verifiable Invariants}}{\text{Long-Term Upstream Maintenance \& Review Burden}}$$
