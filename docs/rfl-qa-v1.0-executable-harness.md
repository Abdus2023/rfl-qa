# RFL-QA v1.0: Executable Qualification Harness (Proposed Standard)

> A deterministic, schema-driven qualification harness for measuring Rust-for-Linux engineering capability across five governing axioms, machine-readable Evidence Records ($E_0$–$E_5$), non-compensable Hard Safety Gates, explicit adversarial test oracles, canonical Semantic Diffs, Assumption Ledgers, and Migration Unit assessment packets.

---

## Preamble: Epistemic Stance & Definition of the Standard

> **This document defines a proposed evidence-based qualification standard for Rust-for-Linux (RFL) engineering.**

It is not an immutable dogma, but an empirical calibration tool. Its validity is derived solely from its repeated application against real upstream code, reproducible adversarial testing, dual-assessor review, and long-term tracking of downstream kernel defect rates.

### The Five Governing Invariants of Qualification

$$\begin{aligned}
\mathbf{1.} & \quad \text{NO EVIDENCE} & \implies & \quad \text{NO VERIFIED CLAIM} \\
\mathbf{2.} & \quad \text{NO ORACLE} & \implies & \quad \text{NO MEANINGFUL TEST} \\
\mathbf{3.} & \quad \text{NO EXPLICIT ASSUMPTION} & \implies & \quad \text{NO TRUST BOUNDARY} \\
\mathbf{4.} & \quad \text{NO TEARDOWN MODEL} & \implies & \quad \text{NO LIFETIME CLAIM} \\
\mathbf{5.} & \quad \text{NO SEMANTIC DIFF} & \implies & \quad \text{NO MIGRATION-EQUIVALENCE CLAIM}
\end{aligned}$$

* **Rule 1:** A capability claim without an attached artifact, verification oracle, and environmental specification is treated as $E_0$ (Unverified) and holds zero weight.
* **Rule 2:** A test without a formally defined pass/fail oracle across adversarial execution interleavings is merely an uncalibrated demonstration.
* **Rule 3:** Every external Type D invariant must be logged in an Assumption Ledger; unrecorded assumptions represent unmanaged risk.
* **Rule 4:** Steady-state correctness is insufficient; destruction and concurrent unregister semantics must be proven first.
* **Rule 5:** Line-by-line syntax translation is rejected; observable behavior, lifecycles, and concurrency contracts must be explicitly diffed.

---

## 1. The Evidence Record Schema

Proficiency claims are invalid without an attached Evidence Record. Capability levels ($L_1$–$L_5$) are **derived states** computed from the highest validated evidence tier across relevant domains.

```yaml
# Schema: rfl-qa/v1.0/evidence-record
evidence_record:
  competency_id: "C-47"
  title: "C callback registration and teardown races"
  claimed_level: "L4"
  evidence_class: "E4"
  context: "Production upstream patch series for subsystem X"

  artifact:
    type: "kernel_patch_series"
    revision: "git:git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git@a7b9c1d4e2f8"
    lore_link: "https://lore.kernel.org/all/20260927-rfl-rcu-teardown-v4@kernel.org/"

  environment:
    kernel_version: "v6.12-rc4"
    rustc_version: "1.85.0"
    target_arch: ["x86_64", "arm64"]
    kconfig: "CONFIG_RUST=y + CONFIG_PREEMPT_RT=y + CONFIG_KASAN=y + CONFIG_KCSAN=y + CONFIG_PROVE_LOCKING=y"

  verification_oracle:
    kunit: "PASS (14 test cases, 0 failures)"
    lockdep: "PASS (0 lockdep warnings / splats)"
    kasan: "PASS (0 invalid memory accesses)"
    kcsan: "PASS (0 data races detected)"
    syzkaller: "PASS (120 CPU-hours, 10^7 iterations, 0 crashes)"

  adversarial_cases_executed:
    - name: "callback_after_unregister"
      result: "PASS"
    - name: "concurrent_remove_during_ioctl"
      result: "PASS"
    - name: "double_unregister_attempt"
      result: "PASS"
    - name: "final_reference_release_under_memory_pressure"
      result: "PASS"

  review:
    primary_reviewer: "Subsystem Maintainer <maintainer@kernel.org>"
    secondary_reviewer: "RFL Reviewer <rfl-reviewer@kernel.org>"
    outcome: "ACKED (Merged into subsystem tree)"

  limitations_and_assumptions:
    - id: "A-01"
      statement: "Hardware interrupt controller callback ordering remains external Type D invariant"
      ledger_ref: "Assumption Ledger #A-01"

  timestamp: "2026-09-27T14:30:00Z"
  derived_status: "VERIFIED"
```

---

## 2. Evidence Hierarchy & Multidimensional Capability Vectors

### Evidence Classes ($E_0$ to $E_5$)
* **$E_0$ (Self-Assertion):** Resume claims, informal portfolio links. **Qualification Weight: Zero.**
* **$E_1$ (Explanation / Interview):** Oral defense or whiteboard discussion. Validates **$L_1$ (KNOW)**.
* **$E_2$ (Controlled Implementation):** Isolated lab exercise or synthetic module. Validates **$L_2$ (USE)**.
* **$E_3$ (Kernel Laboratory Artifact):** Out-of-tree module or in-tree test passing KUnit, KASAN, and lockdep. Validates **$L_3$ (AUDIT)**.
* **$E_4$ (Upstream-Quality Patch / Review):** Patch series or detailed code review surviving subsystem and LKML audit. Validates **$L_4$ (DESIGN)**.
* **$E_5$ (Maintained Subsystem Stewardship):** Long-term ownership of an in-tree `kernel::` abstraction or subsystem Rust integration. Validates **$L_5$ (LEAD)**.

$$\mathbf{Higher\ Evidence\ Tier \neq Higher\ Global\ Capability}$$

An engineer with an $E_5$ artifact in platform driver bindings does not possess $L_5$ in LKMM or memory-management internals.

### Multidimensional Capability Vector
Candidates are evaluated strictly as a 9-dimensional capability vector. **Scalar score averaging (e.g., "4.2 / 5") is strictly prohibited**, as it permits dangerous compensation between unrelated domains.

$$\mathbf{C}_{\text{RFL}} = \begin{bmatrix}
\text{Hardware \& Architecture} & L_3 \; [E_3] \\
\text{Linux Core Internals} & L_4 \; [E_4] \\
\text{Concurrency \& LKMM} & L_4 \; [E_4] \\
\text{C Semantics \& FFI} & L_5 \; [E_5] \\
\text{Rust Language \& no\_std} & L_5 \; [E_5] \\
\text{RFL \texttt{kernel} Crate Design} & L_4 \; [E_4] \\
\text{Verification \& Observability} & L_3 \; [E_3] \\
\text{Toolchain \& Build Engineering} & L_2 \; [E_2] \\
\text{Governance \& Migration Architecture} & L_3 \; [E_4]
\end{bmatrix}$$

---

## 3. Non-Compensable Hard Safety Gates (Automatic BLOCKED)

The following defects constitute an **immediate, unconditional failure** of the qualification for that migration unit, regardless of the candidate's proficiency in other domains. No amount of high-level macro expertise can compensate for a kernel safety violation:

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

1. **Use-After-Free (UAF) or Double-Free:** Any reachable execution path permitting access to deallocated memory or duplicate resource release.
2. **Unsound `unsafe` Block:** An `unsafe` block whose `SAFETY` comment relies on false premises, incomplete invariants, or unverified C-side promises.
3. **Data Race:** Unsynchronized concurrent access to shared mutable state under LKMM or Rust aliasing rules (caught by KCSAN or logical proof).
4. **Introduced Deadlock:** Lock ordering inversion, AB-BA deadlock, or sleep-inside-spinlock detected by lockdep or stress testing.
5. **Incorrect Lifetime Invariant:** A Rust reference escaping the lifetime of its underlying C object or hardware mapping.
6. **ABI Incompatibility:** Corrupting structure padding, alignment, bitfields, or calling conventions where compatibility is required.
7. **Prohibited Execution Context Violation:** Calling a sleeping function or allocating memory (`GFP_KERNEL`) from an atomic, IRQ, or RCU read-side critical section.
8. **Incorrect DMA Ownership:** Accessing DMA memory from the CPU while ownership resides with the hardware device.
9. **Callback-After-Free:** An asynchronous callback invoking code on an object that has initiated or completed deallocation.
10. **Missing Teardown Synchronization:** Failing to flush workqueues, cancel timers, or wait for RCU grace periods prior to resource destruction.
11. **Unexplained Semantic Regression:** Unintended alteration of C-side error codes, side effects, or ordering detected via the Semantic Diff.

---

## 4. The 5 Super-Gates & Adversarial Test Oracles

### Super-Gate 1: Concurrent Teardown Oracle
* **Candidate Lifecycle Model:**
  $$\text{CREATE} \longrightarrow \text{REGISTER} \longrightarrow \text{ACTIVE} \longrightarrow \text{STOP} \longrightarrow \text{QUIESCE} \longrightarrow \text{CALLBACK DRAIN} \longrightarrow \text{REFERENCE DRAIN} \longrightarrow \text{DESTROY} \longrightarrow \text{FREE}$$
* **Adversarial Scheduler Injections:** The test harness randomly interleaves:
  * $T_1: \text{ioctl()}$ $\longleftrightarrow$ $T_2: \text{remove()}$
  * $T_1: \text{c\_callback()}$ $\longleftrightarrow$ $T_2: \text{unregister()}$
  * $T_1: \text{final\_ref\_release()}$ $\longleftrightarrow$ $T_2: \text{free()}$
  * $T_1: \text{rcu\_read\_lock()}$ $\longleftrightarrow$ $T_2: \text{destroy()}$
  * $T_1: \text{workqueue\_handler()}$ $\longleftrightarrow$ $T_2: \text{cancel\_work\_sync()}$
* **Formal Oracle Pass Condition:**
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

### Super-Gate 2: Invariant Classification & Negative-Space Analysis
* **Task:** Classify every invariant of a complex C interface into Type A (Compiler), Type B (API), Type C (Runtime), or Type D (External).
* **Negative-Space Oracle:** The candidate must author a formal Negative-Space statement defining what the abstraction *does not* guarantee.
* **Pass Condition:** The candidate must explicitly identify at least two external Type D assumptions that the Rust layer cannot prove (e.g., hardware FIFO flushing or external C subsystem callback serialization).

### Super-Gate 3: The Canonical Semantic Diff
* **Task:** Structure an exhaustive 12-dimension comparison between legacy C code and proposed Rust abstractions. Line-by-line syntax diffing is rejected.
* **The 12 Dimensions:** Inputs, Outputs, Errors, Ownership, Lifetime, Locking, Atomicity, Execution Context, Callbacks, Side Effects, Ordering, Teardown.
* **Classification Taxonomy:**
  * `UNCHANGED` — Exact semantic parity preserved.
  * `INTENTIONALLY_CHANGED` — Deliberate deviation (must be justified, e.g., turning a runtime error into a compile-time guard).
  * `ACCIDENTALLY_CHANGED` — Unintended drift (Constitutes a defect).
  * `UNKNOWN` — Semantic contract unestablished (Flags Assumption Debt; **legitimate and encouraged**).
  * `NOT_APPLICABLE` — Dimension not applicable to boundary.
* **Pass Condition:** Zero `ACCIDENTALLY_CHANGED` dimensions. All `UNKNOWN` dimensions must be logged in the Assumption Ledger.

### Super-Gate 4: Execution Context Enforcement
* **Task:** Enforce IRQ vs Process vs Atomic execution constraints.
* **Pass Condition:** The candidate must prove which constraints can be encoded statically via Type B typestate tokens, and which *must* be defended via Type C runtime assertions (`might_sleep()`, `in_atomic()`). Candidates who attempt to force all dynamic contexts into rigid static types fail.

### Super-Gate 5: Trust-Boundary Accounting & Minimization
* **Task:** Map and audit the FFI seam of the migration unit.
* **Pass Condition:** Produce a complete Unsafe Surface Inventory where every `unsafe` block, raw pointer, and C callback is mapped to an explicit invariant. Candidate must demonstrate shrinking the unsafe surface area compared to a naive 1:1 translation.

---

## 5. The Migration Unit Assessment Packet

Qualification is assessed strictly per **Migration Unit**. To qualify at $L_4$ or $L_5$, a candidate must submit a complete dossier comprising:

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

### A. Unsafe Surface Inventory
| Boundary Seam | Unsafe? | Architectural Rationale | Invariant Required | Verification Evidence |
| :--- | :---: | :--- | :--- | :--- |
| `ffi::c_api_call` | Yes | Crosses C ABI boundary | Pointer is non-null & properly aligned | KUnit null-check test |
| `c_callback_trampoline` | Yes | C core invokes Rust callback | Target object outlives callback execution | `refcount_t` + pinned state |
| `dma_map_single` | Yes | Interacts with physical MMIO | Buffer owned exclusively by device | DMA API contract + IOMMU |

### B. Assumption Ledger (Tracking Type D Invariants)
| ID | Assumption Stated | Type | Owner | Verification Evidence | Epistemic Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **A-01** | C core cannot invoke callbacks after `unregister()` returns | **D** | Subsystem C Core | C source audit + KUnit test | `VERIFIED` |
| **A-02** | DMA mapping remains coherent until `dma_unmap` completion | **D** | Hardware Device | DMA API contract | `VERIFIED` |
| **A-03** | Rust wrapper lifetime strictly dominates callback trampoline | **B** | Rust Abstraction | Type system proof (`Pin` + lifetime) | `VERIFIED` |
| **A-04** | Hardware guarantees MMIO write ordering after register write | **D** | Hardware Silicon | Datasheet Section 4.2 | `PROVISIONAL` |

$$\mathbf{\text{Assumption Debt}} = \sum \text{Unverified Assumptions} + \sum \text{Weak External Contracts} + \sum \text{Semantic Unknowns}$$

### C. Migration Risk Accounting
The candidate must evaluate risk across nine operational vectors, assigning a rating of `LOW`, `MEDIUM`, `HIGH`, or `BLOCKED` with supporting evidence:
1. **Unsafe Surface Area** (Ratio of unsafe seams to safe public API)
2. **External Assumption Debt** (Count of unverified Type D invariants)
3. **Semantic Unknowns** (Count of `UNKNOWN` entries in Semantic Diff)
4. **Concurrency Complexity** (Distinct locking and RCU domains crossed)
5. **ABI Exposure** (Userspace ABI immutable vs Kernel Internal API)
6. **Toolchain Dependencies** (Unstable compiler feature reliance)
7. **Verification Gaps** (Missing sanitizer or hardware coverage)
8. **Review Complexity** (Can traditional maintainers audit the safety argument?)
9. **Performance Uncertainty** (Benchmarks proving zero-cost abstractions)

---

## 6. The 15 Adversarial Labs (Evidence Generators)

To generate reproducible $E_3$ (Kernel Lab) and $E_4$ (Upstream) evidence, candidates execute standardized adversarial labs designed to probe failure boundaries:

1. **The Pin-Init Gauntlet:** Safely initialize a self-referential C struct from Rust without exposing intermediate uninitialized states.
2. **The RCU Grace Period Trap:** Implement an RCU-protected reader/writer with artificial delays, proving readers never access freed memory.
3. **The Context Violation Fuzzer:** Call sleeping abstractions from an atomic/IRQ context; verify compile-time errors or clean `might_sleep()` runtime warnings without panicking.
4. **The Callback After Free:** Register an asynchronous C callback to a Rust object and trigger object teardown; verify callbacks are rejected or synchronized.
5. **The Error-Path Teardown:** Inject allocation failures (`kmalloc` returns `NULL`) across multi-stage initialization; prove zero resource leaks.
6. **The Bindgen Layout Shock:** Add struct padding and bitfields in C headers; prove Rust FFI either adapts safely or refuses to compile.
7. **The DMA Coherency Audit:** Map a streaming DMA buffer, write from device, read from Rust; prove correct cache invalidation verified by KMSAN.
8. **The Lockdep Deadlock Maze:** Implement nested locking reflecting C deadlocks; prove lockdep catches it or the Rust type system prevents the nesting.
9. **The `unwrap()` Elimination:** Refactor a driver filled with `.unwrap()`, replacing every panic path with controlled error propagation or teardown.
10. **The Trait Object Escape:** Pass a Rust trait object across FFI; prove the abstraction prevents lifetime escape or manages vtable lifetimes safely.
11. **The Workqueue Cancellation Race:** Schedule workqueue items, trigger module unbind; prove `cancel_work_sync()` waits without deadlocks.
12. **The Per-CPU Data Migration:** Translate C per-CPU access into Rust; prove preemption is disabled during the access window.
13. **The Macro Expansion Audit:** Expand a complex macro-heavy C API; implement a sound Rust wrapper without string-matching hacks.
14. **The Toolchain Breakage Test:** Introduce a feature requiring unstable compiler flags; demonstrate proper Kbuild/Kconfig gating.
15. **The Maintainer Negotiation Simulation:** Author an RFC for a `kernel::` abstraction, anticipate three maintainer objections, and formulate technical rebuttals.

---

## 7. Operational Execution Protocol for Assessors

When evaluating a candidate or proposed patch series using RFL-QA v1.0:

1. **Demand the Migration Unit Packet:** Never evaluate isolated, decontextualized code snippets.
2. **Validate Evidence Records:** Ensure every capability claim maps to an $E_3$, $E_4$, or $E_5$ record with complete environmental metadata.
3. **Execute Test Oracles:** Run the concurrent teardown and semantic diff checks against the formal pass conditions.
4. **Audit the Assumption Ledger:** Challenge all Type D invariants. If an assumption lacks a source audit, datasheet, or test, flag it as unmanaged debt.
5. **Enforce Hard Safety Gates:** Scan for non-compensable defects. If a memory corruption or data race is found, **immediately halt and mark BLOCKED**.
6. **Render the Capability Vector:** Output the verified 9-dimensional capability vector.

---

## 8. Role Progression Thresholds

| Role Tier | Required Vector Threshold | Evidence Requirement | Safety Gate Status |
| :--- | :--- | :--- | :--- |
| **Contributor** | $L_2$ across Linux, Rust, RFL APIs. $L_3$ in at least one of (FFI, Concurrency, Verification). | $E_3$ (Kernel Lab) or $E_4$ (Upstream) | Zero Hard Gate failures. |
| **Subsystem Rust Maintainer** | $L_3$ in Subsystem Internals, Concurrency, Verification. $L_4$ in FFI, Abstraction Design, Unsafe Invariant Engineering. | $E_4$ (Upstream) with dual-assessor review. | Zero Hard Gate failures; demonstrated concurrent teardown safety. |
| **Migration Architect** | $L_4$ in Semantic Translation, Abstraction Design. $L_5$ in Migration Architecture, Governance, Toolchain Strategy. | $E_5$ (Sustained Maintenance) + upstream consensus. | Zero Hard Gate failures; demonstrated assumption debt and risk management. |

---

## Final Standard Metric

The ultimate measure of an RFL Migration Architect under RFL-QA v1.0 is:

$$\mathbf{M} = \frac{\Delta \text{ Implicit Risk Converted to Explicit, Reviewable, Verifiable Invariants}}{\text{Long-Term Upstream Maintenance \& Review Burden}}$$

An RFL engineer does not eliminate the physical hardware, the C substrate, or the upstream community. They build the **verifiable type-system bridge** that allows the Linux kernel to safely and maintainably evolve across them all.
