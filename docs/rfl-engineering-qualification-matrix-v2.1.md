# RFL Engineering Qualification Matrix v2.1 (Definitive Assessment Framework)

> Deterministic, evidence-first qualification framework separating language-enforceable invariants, runtime kernel invariants, environmental constraints, and externally established contracts across nine independent engineering domains, empirical evidence-tagged proficiency levels ($L_n\text{-}E$), trust-boundary accounting, teardown-first mechanics, and adversarial qualification gates.

---

## Core Paradigm & Architectural Shift

> **Knowing a technology is not evidence of being able to use it safely in the kernel.**

Rust-for-Linux is not an effort to rewrite the Linux kernel in Rust. It is an engineering discipline centered on **semantic boundaries**:

$$\text{Implicit C Assumptions} \xrightarrow{\quad \text{Invariant Engineering} \quad} \text{Explicit, Reviewable, Verified Contracts}$$

An RFL engineer does not demand that every kernel property be solved at compile time. Instead, the engineer operates under this foundational axiom:

> **Encode every invariant that can reasonably be encoded in the type/API system, and explicitly verify, defend, or bound the remainder.**

---

## 1. Domain Architecture: The 9 Independent Domains

Matrix v2.1 maintains strict separation between **Verification & Observability** and **Toolchain & Build Integration**:

$$\text{Verification Competence} \neq \text{Toolchain/Build Competence}$$

A systems engineer can master dynamic sanitizers, KUnit tests, and syzkaller reproducers while lacking the specialized knowledge needed to maintain Kbuild, LLVM/Clang patching, target triples, and rustc version policies across enterprise distributions.

```
                         RFL ENGINEERING
                               │
         ┌─────────────────────┼──────────────────────┐
         │                     │                      │
      SEMANTICS            IMPLEMENTATION         EVIDENCE
         │                     │                      │
         ├─ C contracts        ├─ Rust core          ├─ KUnit
         ├─ lifetimes          ├─ FFI boundary       ├─ KASAN / KMSAN
         ├─ LKMM               ├─ RFL APIs           ├─ lockdep
         ├─ contexts           ├─ Kbuild             ├─ KCSAN
         └─ hardware           └─ drivers            └─ syzkaller
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                        ABSTRACTION DESIGN
                               │
                     ┌─────────┴─────────┐
                     │                   │
                 SAFE API          UNSAFE CORE
                     │                   │
                     │              invariant proof
                     │                   │
                     └─────────┬─────────┘
                               ▼
                        MIGRATION UNIT
                               │
                 ┌─────────────┼──────────────┐
                 ▼             ▼              ▼
              C remains     Rust moves      FFI boundary
                 │             │              │
                 └─────────────┼──────────────┘
                               ▼
                         VERIFICATION
                               │
                               ▼
                            UPSTREAM
                               │
                               ▼
                          MAINTENANCE
```

### The 9 Independent Competency Domains
1. **Domain 1:** Hardware & Architecture (Systems Foundation)
2. **Domain 2:** Linux Core Internals (C Semantics)
3. **Domain 3:** Concurrency & LKMM (Memory Models & Synchronization)
4. **Domain 4:** C Semantics & FFI (The Semantic Bridge)
5. **Domain 5:** Rust Language & `no_std` (Kernel-Grade Rust)
6. **Domain 6:** RFL `kernel` Crate & Abstraction Design (The Safe Middleware)
7. **Domain 7:** Verification & Observability (Sanitizers, KUnit, Fuzzing)
8. **Domain 8:** Toolchain & Build Integration (Kbuild, LLVM, `rustc`, Pinning)
9. **Domain 9:** Governance, Upstream Process & Migration Architecture

---

## 2. The Invariant Taxonomy: Four Distinct Classes

Kernel engineering fails when an abstraction attempts to force non-static kernel invariants into the compiler, or conversely, assumes the Rust type system proves properties outside its scope.

```
                      KERNEL INVARIANTS
                              │
     ┌────────────────┬───────┴────────┬────────────────┐
     ▼                ▼                ▼                ▼
  Type A           Type B           Type C           Type D
Compiler-        API-             Runtime-         External /
Enforceable      Enforceable      Enforced         System
```

### Type A: Compiler-Enforceable Invariants
*Properties proven by the language rules and borrow checker under sound Rust assumptions.*
* **Scope:** Lexical lifetimes, pointer aliasing exclusivity (`&mut` vs `&`), basic Send/Sync marker constraints, size/alignment layout guarantees (`repr(C)`), drop execution upon scope exit.
* **Example:** Guaranteeing that a borrowed slice `&[u8]` cannot outlive the underlying driver buffer `T`.

### Type B: API-Enforceable Invariants
*Properties made unrepresentable or structurally enforced through type design, typestate tokens, and RAII guards.*
* **Scope:** Enforcing lock-holding via guard tokens, preventing move-after-init via `Pin`, ensuring fallible allocation handling via mandatory `Result`, scoping RCU pointer dereferencing to an explicit guard closure.
* **Example:** A structure `Locked<'a, T>` that exposes its inner value `&'a T` only while the corresponding spinlock guard is in scope.

### Type C: Runtime-Enforced Invariants
*Properties that depend on dynamic kernel execution state, configuration options, or complex scheduling conditions.*
* **Scope:** Memory safety via KASAN, uninitialized memory checks via KMSAN, lock hierarchy verification via `lockdep`, atomic context violation detection via `might_sleep()`, reference counter saturation via `refcount_t`.
* **Example:** Detecting at runtime that a sleeping allocation (`GFP_KERNEL`) was invoked with local IRQs disabled.

### Type D: External / System Invariants
*Assumptions established and maintained outside the Rust abstraction's boundary.*
* **Scope:** C subsystem callback sequencing, hardware device register semantics, ACPI/Device Tree binding validity, bus host controller firmware integrity, cooperative kernel threads not corrupting shared memory.
* **Example:** The C networking core promising that `ndo_stop` will not execute concurrently with `ndo_start_xmit` on the same queue without an external lock.

$$\mathbf{Rust\ Type\ System \neq Complete\ Kernel\ Proof\ System}$$

---

## 3. Empirical Proficiency Scale ($L_n\text{-}E$)

Capability without empirical upstream evidence produces paper certifications. Matrix v2.1 indexes every capability level against its **Evidence Tier**:

### Capability Levels ($L_0$ to $L_5$)
* **L0 (Unaware):** Does not know the concept exists.
* **L1 (KNOW):** Can explain the concept, theory, and kernel relevance.
* **L2 (USE):** Can implement standard patterns within existing abstractions.
* **L3 (AUDIT):** Can systematically discover defects, leaks, and unsoundness in others' code.
* **L4 (DESIGN):** Can synthesize new sound abstractions and resolve complex semantic conflicts.
* **L5 (LEAD):** Can define subsystem architecture, upstream policy, toolchain roadmap, and governance.

### Empirical Evidence Suffixes ($-E$)
* **-T (Theoretical / Examined):** Evaluated through verbal defense, whiteboard analysis, or written examination.
* **-C (Controlled Exercise):** Demonstrated in a simulated kernel sandbox, synthetic lab exercise, or private test suite.
* **-P (Production / Upstream):** Demonstrated in public upstream LKML patch series, merged in-tree drivers, or audited kernel security releases.

$$\text{Example: } \mathbf{L3\text{-}P} \equiv \text{Auditor-level competence verified through accepted upstream patch reviews on LKML.}$$

---

## 4. Trust-Boundary Accounting & Surface Minimization

Counting lines of `unsafe` is a vanity metric. What matters is the **topology and auditability of the trust boundary**.

```
                   Rust Safe Code
                         │
                         ▼
             [ Trust Boundary: Audited ]
                         │
                    Unsafe Core
                         │
                    C / FFI ABI
                         │
                  Linux C Kernel
                         │
                     Hardware
```

### Mandatory Trust-Boundary Inventory
Every migration unit must deliver an explicit inventory table:

| Boundary Seam | Unsafe? | Justification | Invariant Maintained | Verification Evidence |
| :--- | :---: | :--- | :--- | :--- |
| `raw_ptr_deref` | Yes | C ABI returns raw pointer | Pointer non-null, aligned, mapped | Type B guard + KASAN test |
| `c_callback_trampoline` | Yes | C core invokes Rust fn | Object alive, context valid | `refcount_t` inc + lockdep |
| `dma_map_single` | Yes | Hardware physical addressing | Device owns memory during IO | Bounce-buffer test + IOMMU |
| `rcu_dereference` | Yes | Lockless pointer fetch | Valid inside grace period | RCU guard token + KCSAN |

### Boundary Minimization Rule
The goal of the RFL engineer is **not zero `unsafe`**—which is impossible in kernel space—but:

> **A minimal, auditable unsafe surface area with mathematically explicit invariant proofs and complete runtime defensive bounds.**

---

## 5. Negative-Space Analysis

An engineer must explicitly define what an abstraction **cannot** guarantee. Overclaiming safety is an active kernel security hazard.

Every `SAFETY` documentation block for a public abstraction must state:

```rust
// SAFETY:
// 1. GUARANTEES PROVIDED:
//    - Exclusivity: Only one mutable Rust reference exists to the underlying device state.
//    - Lifetime: The returned reference is bound to the lifetime of the registered driver.
//
// 2. NEGATIVE SPACE (WHAT THIS DOES NOT GUARANTEE):
//    - Hardware correctness: Does not guarantee that hardware registers will not return
//      corrupted data or trigger bus aborts.
//    - Subsystem callback concurrency: Does not prevent the C core from invoking
//      unregistered callbacks if the C subsystem driver core contains race conditions.
//    - Scheduler fairness: Does not prevent CPU starvation if the caller loops indefinitely.
```

---

## 6. Execution Contexts: Static Encoding vs. Dynamic Defense

Real Linux contexts are not cleanly partitioned into "Process" and "IRQ". They form a multidimensional execution spectrum:

```
                         KERNEL EXECUTION SPECTRUM
                                     │
      ┌──────────────────┬───────────┴───────────┬──────────────────┐
      ▼                  ▼                       ▼                  ▼
Process Context     Softirq / BH            Hardirq            NMI / MCE
(Sleepable)         (Non-sleepable)         (Non-sleepable)    (Re-entrant)
GFP_KERNEL ok       GFP_ATOMIC only         GFP_ATOMIC only    No alloc / locks
```

### Calibrated Assessment Requirement
The candidate is not evaluated on whether they can force every dynamic context into static Rust types. The candidate must answer:

> **Which context constraints can be encoded statically via type tokens, and which must be defended via runtime assertions and kernel conventions?**

* **Statically Expressible:** Parameterizing operations by capability tokens (e.g., `Context<CanSleep>` vs `Context<Atomic>`), preventing `Mutex::lock` from being called on non-sleepable contexts at compile time.
* **Dynamically Dependent:** Checking preemption state, spinlock depth, or interrupt disable flags at runtime via `might_sleep()`, `in_atomic()`, or `lockdep_assert_held()`.

---

## 7. RCU Qualification: Invariant-Centric Evaluation

The RCU evaluation does not demand memorization of specific uniprocessor or RT kernel preemption configurations. The candidate must demonstrate mastery of the **fundamental RCU invariant**:

```
Reader:  [ rcu_read_lock ] ──► [ dereference P ] ──► [ use *P ] ──► [ rcu_read_unlock ]
                                                            │
Writer:  [ allocate P' ] ──► [ publish P' ] ──► [ synchronize_rcu ] ──► [ free old P ]
                                                         ▲
                                           GRACE PERIOD BARRIER
```

### The Decisive RCU Questions
1. *Why does `pointer != NULL` fail to guarantee object validity under RCU?*
2. *Why is freeing an RCU-protected structure before the grace period completes a catastrophic Use-After-Free even if the writer has detached the pointer from all global lists?*
3. *How does RFL's `kernel::sync::rcu::Guard` prevent the dereferenced reference from escaping the lexical scope of the read-side critical section?*

---

## 8. Failure Path Exhaustion (Beyond "No `unwrap`")

Prohibiting `unwrap()` and `expect()` is merely syntax-level linting. The true qualification test is **Failure Path Exhaustion**:

$$\forall \text{ reachable failure path } \implies \text{Deliberate, bounded kernel-level behavior}$$

The candidate must audit and demonstrate predictable behavior across all eight kernel failure modes:

1. **Allocation Failure:** System running under heavy memory pressure (`ENOMEM`), never panicking.
2. **Invalid Userspace Input:** Memory pointer faults, truncated buffers (`EFAULT`), bad `ioctl` arguments.
3. **C Subsystem Return Codes:** Unexpected negative errors or `ERR_PTR` returned by core C APIs.
4. **Hardware Failure:** Unresponsive MMIO reads, bus timeouts, parity/ECC errors.
5. **Resource Exhaustion:** Out of minor numbers, IRQ vectors, or DMA bounce buffer slots.
6. **Concurrent Teardown:** User unbinds driver via sysfs while active `ioctl` operations are in-flight.
7. **Partial Initialization:** Early failure during `probe()` triggering clean unwind of partially initialized state.
8. **Asynchronous Cancellation:** Workqueues or timers cancelled while mid-execution.

---

## 9. Compatibility Boundaries: Five Distinct ABIs

Kernel engineering does not demand "100% backward compatibility" across all internal C functions. Internal kernel interfaces change constantly. An architect must distinguish five distinct ABI layers:

| Layer | Stability Guarantee | Can Rust Alter It? |
| :--- | :--- | :--- |
| **Userspace ABI** | Strictly immutable ("never break userspace"). | **NO.** Syscalls, sysfs layout, and `ioctl` numbers must remain byte-identical. |
| **Kernel Internal API** | Fluid; evolves with in-tree callers. | **YES.** Upstream developers refactor internal C APIs as needed. |
| **Rust-for-Linux API** | Version-pinned; evolves under RFCs. | **YES.** Changes coordinated through RFL maintainers. |
| **C/Rust FFI ABI** | Governed by C calling conventions. | **NO.** Must strictly adhere to `repr(C)` and ISA ABI standards. |
| **Hardware ABI** | Fixed by silicon specification. | **NO.** MMIO registers, DMA descriptors, and endianness are immutable. |

---

## 10. Teardown-First Lifecycle Design

Inexperienced engineers design creation and use, leaving teardown as an afterthought. Matrix v2.1 mandates **Teardown-First Architecture**:

```
CREATE
  ↓
REGISTER
  ↓
ACTIVE (Steady-state I/O)
  ↓
STOP NEW WORK (Reject incoming requests)
  ↓
QUIESCE (Wait for active requests to finish)
  ↓
CANCEL / FLUSH CALLBACKS (Flush workqueues, cancel timers)
  ↓
RELEASE REFERENCES (Drop external refcounts)
  ↓
WAIT FOR READERS (Synchronize RCU grace periods)
  ↓
DESTROY (Run inner destructors)
  ↓
FREE (Return physical memory to allocator)
```

The decisive evaluation question:

> **What happens if an asynchronous interrupt, workqueue, or concurrent `ioctl` executes during each individual transition in this teardown sequence?**

---

## 11. The 100-Competency Matrix Across 9 Domains

### Domain 1: Hardware & Architecture (Skills 1–10)
1. CPU Privilege Rings & Exception Entry/Exit
2. MMU & Page Table Management (PGD to PTE)
3. TLB Shootdowns & Hardware Coherency
4. Interrupt Controllers (APIC/GIC) & IRQ Domains
5. DMA Mapping, Cache Coherency & IOMMU
6. PCIe Configuration Space, BARs & MSI-X
7. USB Topologies & URB Lifecycle
8. Cache Hierarchies, False Sharing & Alignment
9. NUMA Nodes & Memory Locality
10. Boot Sequence & Early Pre-Slab Init

### Domain 2: Linux Core Internals (Skills 11–25)
11. `task_struct` & Scheduler Runqueues
12. Process/Thread Teardown & Zombie Reaping
13. Credentials, Namespaces & Capabilities
14. VFS Architecture, Inodes & Dentry Lookup
15. File Descriptors & `file_operations` Table
16. `copy_to_user` / `copy_from_user` Page Faulting
17. SLUB Allocator & GFP Allocation Flags
18. Buddy Allocator & Page Frame Management
19. Virtual Memory Areas (VMAs) & Fault Handlers
20. Device Model, `kobject` & Sysfs Attributes
21. Module Lifecycle & Race-Free Unload
22. Error Pointer Conventions (`ERR_PTR`, `IS_ERR`)
23. Workqueues (Bound, Unbound, Flush Semantics)
24. Timers (`timer_list`, `hrtimer`) & Softirqs
25. Wait Queues & Completion Barriers

### Domain 3: Concurrency, LKMM & RCU (Skills 26–40)
26. Linux Kernel Memory Model (LKMM) Ordering
27. Compiler Barriers vs Hardware Memory Barriers
28. Atomics, `READ_ONCE()`, `WRITE_ONCE()`
29. Spinlocks & IRQ-Disabled Critical Sections
30. Mutexes & Sleeping-in-Atomic Diagnostics
31. Read-Write Locks & Seqlock Counters
32. `refcount_t` vs `atomic_t` Saturation Semantics
33. RCU Read-Side Critical Sections & Dereferencing
34. RCU Grace Periods, `synchronize_rcu` & Quiescence
35. Sleepable RCU (SRCU) Domain Management
36. Per-CPU Variables & Preemption Disabling
37. Lockdep Class Keys & Dependency Splats
38. Hardirq vs Softirq vs Process Concurrency
39. Atomic Context Execution Restrictions
40. RFL `kernel::sync` & Lockdep Integration

### Domain 4: C Semantics & FFI (Skills 41–52)
41. C ABI, Calling Conventions & Calling Registers
42. `repr(C)`, Field Alignment & Padding Rules
43. Bitfield Encoding & Endianness Conversions
44. Variadic Functions (`va_list`) Across FFI
45. C Macro Reverse Engineering
46. Implicit Precondition & Contract Discovery
47. Asynchronous Callback Teardown Races
48. Intrusive Data Structures (`struct list_head`)
49. `bindgen` Pipeline, Allowlist & Opaque Types
50. Error Code Mapping to `Result<T, Error>`
51. Null Pointer vs `Option<&T>` Semantic Mapping
52. FFI Ownership Transfer (Borrowed vs Consumed)

### Domain 5: Kernel-Grade Rust & `no_std` (Skills 53–69)
53. `no_std` Environment & `core` / `alloc` Subsets
54. Custom Kernel Panic & OOM Handlers
55. Unsafe Invariant Formal Proof Engineering
56. Raw Pointer Provenance & Aliasing Rules
57. Lifetime Elision & Bounded Invariant Lifetimes
58. Variance Control via `PhantomData`
59. `Send` and `Sync` Auditing for FFI Wrappers
60. Interior Mutability (`UnsafeCell`, `Opaque<T>`)
61. `MaybeUninit` & Out-Pointer Initialization
62. Deterministic Drop & Double-Free Defenses
63. Address Stability via `Pin`
64. In-Place Initialization (`pin-init` Macros)
65. Dynamic Dispatch (`dyn Trait`) in `no_std`
66. Procedural Macros for C Vtable Generation
67. LLVM IR & Assembly Zero-Cost Verification
68. Custom Kernel Allocators (`KBox`, `KVBox`)
69. Panic-Free Pattern Engineering

### Domain 6: RFL `kernel` Crate & Abstraction Design (Skills 70–80)
70. `kernel` Crate Architecture & Boundary Rules
71. Safe Subsystem Wrapper Design
72. In-Tree Reference Driver Pattern
73. Context-Encoding Typestate Patterns
74. RAII Guards for Locks and RCU Critical Sections
75. Abstraction Leakage Detection & Elimination
76. Trust-Boundary Accounting & Minimization
77. Subsystem Idiom Translation (`container_of`)
78. Safe C Callback Trampoline Architecture
79. KUnit Unit Testing Inside `kernel::`
80. Subsystem Backward Compatibility Boundaries

### Domain 7: Verification & Observability (Skills 81–90)
81. KUnit Test Design & Mocking Constraints
82. kselftest User-Space Test Harnesses
83. KASAN & KFENCE Memory Bug Detection
84. KMSAN Uninitialized Memory Triage
85. UBSAN & KCSAN Concurrency Sanitization
86. Lockdep Assertions & Class Key Debugging
87. Dynamic Tracing with ftrace & Tracepoints
88. eBPF Probing of Rust Kernel Code Paths
89. QEMU, GDB & Kernel Crash Dump (`kdump`) Triage
90. Syzkaller Coverage-Guided Kernel Fuzzing

### Domain 8: Toolchain & Build Integration (Skills 91–95)
91. Kbuild Integration & Kernel `Makefile` Rules
92. Kernel `Kconfig` Dependency & Feature Gating
93. Toolchain Pinning Policy (Debian 13 / 1.85.0+ Baseline)
94. Unstable Feature Tracking & Deprecation Roadmap
95. Clang/LLVM, `libclang` & `bindgen` CI Automation

### Domain 9: Governance, Upstream Process & Migration Strategy (96–100)
96. LKML Etiquette, `b4`, and `git-send-email`
97. Subsystem Maintainer Review Dynamics
98. Dual-Maintainership Workflow (Subsystem + RFL)
99. Scoping Migration Units & Dependency Trees
100. Economic Trade-off Analysis (Safety vs Review Cost)

---

## 12. The Practical Qualification Super-Gates

### Gate 1: The Context Matrix & Invariant Classification Gate
*The candidate is given a 10-function C subsystem interface.*

1. Construct the **Execution-Context Matrix** (Process, IRQ, Softirq, May Sleep, Required Locks, RCU Protection).
2. Classify every invariant into **Type A, Type B, Type C, or Type D**.
3. Design a Rust API that statically enforces Type A/B invariants and integrates runtime defenses for Type C/D.
* **Failure Condition:** Exposing a sleeping function in an atomic context without runtime assertions or static barriers; claiming a Type D external invariant is "proven safe by Rust."

### Gate 2: The Unsafe Trust-Boundary Audit Gate
*The candidate is presented with an existing Rust abstraction containing 5 `unsafe` blocks.*

1. Produce an **Unsafe Surface Inventory** mapping preconditions, establishment, maintenance, and destruction.
2. Formulate the **Negative-Space Statement** defining what the abstraction does not guarantee.
3. Minimize the boundary by eliminating unnecessary `unsafe` operations.
* **Failure Condition:** Documenting `SAFETY` by merely describing what the code does; failing to catch an aliasing violation or missing destruction lock.

### Gate 3: The Semantic Diff & Teardown Gate
*The candidate is given an existing C driver and its proposed Rust rewrite.*

1. Produce a **Semantic Diff** covering lifetimes, locking, atomicity, error codes, and side effects.
2. Map the **Teardown-First State Machine** from `STOP NEW WORK` to `FREE`.
3. Defend the design against concurrent invocation during each phase of teardown.
* **Failure Condition:** Performing a line-by-line syntax comparison; introducing a race where an unregister callback fires after memory has been freed.

### Gate 4: The In-Place Initialization & Concurrency Gate
*The candidate implements a character device registered with the C VFS.*

1. Implement in-place initialization using `pin-init`.
2. Protect dynamic reader lookups using `kernel::sync::rcu`.
3. Verify the implementation under KASAN, KCSAN, and lockdep.
* **Failure Condition:** Moving a pinned object in memory; sleeping inside an RCU read-side critical section; leaking references upon initialization failure.

### Gate 5: The Migration Unit & Upstream RFC Defense Gate
*The candidate authors an RFC proposing migration of a subsystem component.*

1. Define the **Migration Unit**, dependency graph, and in-tree reference driver.
2. Detail the **Rollback Plan** and benchmark performance against the C baseline.
3. Defend the proposal against adversarial maintainer review on LKML.
* **Failure Condition:** Proposing a "big-bang" rewrite; demanding breaking changes to the Userspace ABI; ignoring maintainer review bandwidth concerns.

---

## 13. Role Qualification Profile

To qualify for an operational role, an engineer must meet both the **Proficiency Level** and the **Empirical Evidence Tier**:

| Domain | Contributor | Subsystem Rust Maintainer | Migration Architect |
| :--- | :---: | :---: | :---: |
| **1. Hardware & Arch** | L1-C | L2-C | L4-P |
| **2. Linux Internals** | L2-C | L3-P | L5-P |
| **3. Concurrency & LKMM** | L2-C | L4-P | L5-P |
| **4. C Semantics & FFI** | L2-C | L4-P | L5-P |
| **5. Kernel-Grade Rust** | L3-C | L4-P | L5-P |
| **6. `kernel` Crate Design** | L2-C | L4-P | L5-P |
| **7. Verification & Observability** | L2-C | L3-P | L4-P |
| **8. Toolchain & Build** | L1-C | L3-C | L5-P |
| **9. Governance & Migration** | L2-P | L4-P | L5-P |

---

## The Definitive Metric of Success

The final measure of an RFL Migration Architect is not:

$$\text{"How many lines of C did you replace?"}$$

The definitive metric is:

$$\mathbf{M} = \frac{\Delta \text{ Implicit Risk Converted to Explicit, Verifiable Invariants}}{\text{Long-Term Upstream Maintenance \& Review Burden}}$$

An RFL engineer does not eliminate the physical machine, the C kernel, or the upstream community. They build the **verifiable bridge** that allows Linux to safely evolve across them all.
