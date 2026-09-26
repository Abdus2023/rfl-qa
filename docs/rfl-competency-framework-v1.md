# RFL Competency Framework v1: Measurable Engineering Qualification

> Deterministic, evidence-first qualification framework for measuring Rust-for-Linux engineering capability across five operational depths: **KNOW**, **USE**, **AUDIT**, **DESIGN**, and **LEAD**.

---

## Core Principle

> **Knowing a technology is not evidence of being able to use it safely in the kernel.**

For every competency in this framework, we distinguish five strictly non-interchangeable operational depths:

* **KNOW** — Can explain the mechanism, theory, and operational constraints.
* **USE** — Can implement correctly within established abstractions and patterns.
* **AUDIT** — Can systematically detect defects, unsoundness, and contract violations in someone else's implementation.
* **DESIGN** — Can synthesize a new abstraction that mechanically enforces implicit kernel contracts into safe, zero-cost Rust types.
* **LEAD** — Can establish subsystem architecture, review standards, migration strategy, economic tradeoffs, and upstream LKML consensus.

---

## 1. Systems Foundation Competency Matrix

| Competency | KNOW | USE | AUDIT | DESIGN | LEAD |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CPU architecture** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **MMU / page tables** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Interrupts (IRQ / softirq / NMI)** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **DMA & cache coherency** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **PCI / bus / device model** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Virtual memory & allocators** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **NUMA topology** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Boot & early initialization** | ✓ | ✓ | ✓ | ✓ | ✓ |

### Architecture Depth Requirements
For a contributor, deep mastery across every ISA is not required. A calibrated requirement profile:

```
x86-64          deep
ARM64           working
RISC-V          conceptual / working
other arch      understand portability constraints
```

A lead must clearly distinguish **architecture-dependent versus architecture-independent code** and understand compiler/hardware memory reordering differences across TSO (Total Store Order, e.g., x86) and weak-ordering (e.g., ARM64, RISC-V) architectures.

---

## 2. C Competence: The Semantic Reverse-Engineering Gate

C competence in Rust-for-Linux is not about writing basic C; it is a formal gate on **semantic discovery**.

### Minimum Evaluation Scenario
The engineer is presented with a standard kernel C structure:

```c
struct foo {
    struct list_head node;
    refcount_t refs;
    spinlock_t lock;
    void (*callback)(struct foo *);
};
```

The candidate must immediately formulate the implicit kernel questions before writing a single line of Rust:

* *Who owns `foo`?*
* *Who owns `node`?*
* *Who can invoke `callback`?*
* *Can `callback` race with destruction?*
* *What protects `refs`?*
* *What protects `node`?*
* *Can `callback` sleep?*
* *Can `callback` execute after `foo` is freed?*
* *Can this structure move in physical or virtual memory?*
* *Can this structure be accessed from IRQ or softirq context?*
* *Is RCU read-side protection involved in pointer traversal or reclamation?*

If these questions do not naturally and immediately occur, the engineer is not qualified to design or review the Rust wrapper.

---

## 3. Rust Competence Tiers

The relevant Rust curriculum for the Linux kernel is far narrower and deeper than generic "advanced Rust."

```
┌────────────────────────────────────────────────────────┐
│ Tier A — Mandatory (Kernel Language Core)              │
│ ownership, borrowing, lifetimes, traits, generics,     │
│ associated types, Option, Result, slices, raw pointers,│
│ unsafe, repr(C), FFI, atomics, Send, Sync, MaybeUninit,│
│ Pin, drop semantics                                    │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Tier B — RFL-Critical (Kernel Integration Boundary)   │
│ pin-init, in-place initialization, kernel allocation,  │
│ kernel refcounting, FFI safety proofs, kernel sync,    │
│ context restrictions, error handling, macro interfaces,│
│ C-compatible layouts                                   │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Tier C — Specialist (Subsystem & Architecture Leads)   │
│ codegen / compiler behavior, LLVM IR inspection,       │
│ assembly inspection, ABI details, optimization effects,│
│ compiler / toolchain internals, LKMM mapping           │
└────────────────────────────────────────────────────────┘
```

* **Tier A (Mandatory):** Core type system, borrowing, lifetime analysis, and raw pointer mechanics.
* **Tier B (RFL-Critical):** Subsystem abstractions, in-place initialization (`pin-init`), GFP allocation rules, and lockdep-aware synchronization.
* **Tier C (Specialist):** LLVM IR, codegen auditing, and compiler behavior. Critical for abstraction maintainers and performance-sensitive hot paths, but not required for everyday driver contributors.

---

## 4. The Unsafe-Code Qualification Gate

This is one of the strictest qualification gates in the entire curriculum. Every `unsafe` operation must undergo explicit, structured invariant analysis:

```
                    UNSAFE OPERATION
                           │
                           ▼
                  What can go wrong?
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          lifetime      aliasing       layout
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                   required invariant
                           │
                           ▼
                  who establishes it?
                           │
                           ▼
                  who maintains it?
                           │
                           ▼
                  who invalidates it?
                           │
                           ▼
                     destruction
```

### The Invariant Independence Rule
> **A candidate must be able to perform this invariant proof without relying on the borrow checker or compiler error messages to discover the answer.**

The compiler only checks what the Rust type system is told. The engineer must prove that the **underlying unsafe assumptions and FFI contracts themselves are sound**.

---

## 5. FFI Qualification: The Three-Layer Rule

A robust qualification exercise requires taking an arbitrary kernel C interface and decomposing it into three strictly separated layers:

```
┌────────────────────────────────────────────────────────┐
│ Layer 1 — Raw Binding                                  │
│ extern "C" { fn foo_get(...) -> *mut Foo; }            │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Layer 2 — Unsafe Wrapper                               │
│ unsafe fn foo_get_raw(...) -> *mut Foo                 │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Layer 3 — Safe Rust Abstraction                        │
│ struct FooHandle { ... }                               │
└────────────────────────────────────────────────────────┘
```

For every interface crossing this boundary, the candidate must produce explicit evidence covering:

* `OWNERSHIP` — Single, shared, or borrowed ownership?
* `LIFETIME` — Tied to parent object, hardware state, or subsystem unregister?
* `NULLABILITY` — Valid pointer, null, or `ERR_PTR` error code?
* `ERROR REPRESENTATION` — Converted to `Result<T, kernel::error::Error>`.
* `THREAD SAFETY` — Soundness of `Send` and `Sync` trait implementations.
* `INTERRUPT CONTEXT` — Safe for hardirq, softirq, or process context only?
* `LOCKING` — External locking preconditions required by C API.
* `REFERENCE COUNTING` — Increment/decrement contract and saturation semantics.
* `CALLBACKS` — Reentrancy, sleeping allowed, or teardown races.
* `DESTRUCTION` — Destructor sequence and synchronization before free.
* `ABI` — Alignment, struct packing, and calling conventions.

### Cardinal Principle
$$\mathbf{UNKNOWN \neq SAFE}$$

If any dimension in this contract cannot be definitively verified from C source and subsystem documentation, the abstraction must treat it as unsafe or restricted.

---

## 6. Concurrency & Synchronization Qualification

A kernel Rust engineer must distinguish: `Mutex`, `SpinLock`, `RwLock`, `atomic`, `refcount`, `RCU`, `completion`, `wait queue`, `workqueue`, and `per-CPU state`.

More importantly, the engineer must prove **why** a specific synchronization primitive is mandated:

```
                    Shared state
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
        process         IRQ           CPU
        context        context       parallel
           │             │             │
           └─────────────┼─────────────┘
                         ▼
                   synchronization
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      lock             atomic            RCU
```

Choosing the wrong primitive (e.g., using a sleeping `Mutex` inside an IRQ context or spinlock critical section) produces code that compiles cleanly in Rust, but causes immediate kernel deadlocks or panics at runtime.

---

## 7. RCU Qualification

The candidate must demonstrate rigorous operational reasoning regarding read-side critical sections vs. reclamation:

```
Writer Path:
  writer ──► replace pointer ──► synchronize_rcu() / call_rcu() ──► destroy / free

Reader Path:
  reader ──► enter rcu_read_lock() ──► dereference pointer ──► use object ──► exit rcu_read_unlock()
```

### Critical Axiom
> **`"pointer is non-null"` does NOT imply `"object remains alive."`**

The pointer remains valid *only* within the bounded RCU read-side critical section.

### 2026 Framing
Current RFL exposes active RCU abstractions in `kernel::sync::rcu`. The qualification question is no longer *"Can you solve RCU in Rust?"* but:

> **Can you correctly use and extend RFL's RCU abstractions while strictly preserving Linux's RCU semantics and memory barriers?**

---

## 8. Execution Context Awareness

Kernel code executes across strictly constrained execution contexts:

```
                    Kernel execution
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
        process           IRQ           softirq
        context         context         context
           │               │               │
      may sleep?     cannot sleep!    cannot sleep!
     user access?    no user copy!    no user copy!
     GFP_KERNEL?       GFP_ATOMIC?     GFP_ATOMIC?
```

### Core Design Requirement
> **A safe Rust API should make invalid kernel-context usage difficult or impossible at compile time.**

Abstractions must encode context requirements using phantom types, token-passing patterns, or context-specific guards rather than deferring failures to runtime assertions or kernel panics.

---

## 9. Verification Architecture: Layered Defense

Correctness in mixed-language kernel code is established through a defense-in-depth pipeline:

```
                CHANGE
                   │
                   ▼
              rustc / Kbuild
                   │
                   ▼
               unit tests
                 KUnit
                   │
                   ▼
              integration
               kselftest
                   │
                   ▼
              dynamic tools
         ┌─────────┼──────────┐
         ▼         ▼          ▼
       KASAN     lockdep    UBSAN
         │         │          │
         └─────────┼──────────┘
                   ▼
                 QEMU
                   │
                   ▼
               syzkaller
                   │
                   ▼
              real hardware
```

### Ground Reality
$$\text{compile success} \neq \text{memory safety} \neq \text{concurrency correctness} \neq \text{ABI correctness} \neq \text{kernel correctness}$$

No single stage establishes complete correctness.

---

## 10. Evidence Levels for Qualification & Invariants

To eliminate unsupported capability claims, all invariant proofs and qualification statements must use five standardized epistemic status levels:

| Level | Definition | Concrete Kernel Example |
| :--- | :--- | :--- |
| **PROVED** | Established by the language type system or a bounded formal proof. | Rust ownership and `&mut` exclusivity prevent data races within the abstraction. |
| **VERIFIED** | Demonstratively validated by reproducible tests and dynamic tooling. | KUnit tests pass; KASAN, KMSAN, and lockdep report zero warnings under heavy load. |
| **PARTIALLY VERIFIED** | Evidence exists but does not exhaust the complete semantic contract. | Passes single-CPU tests; multi-core SMP stress or hotplug unbind not yet executed. |
| **PROVISIONAL** | Reasonable engineering assumption based on C comments; unproven. | Assuming C subsystem callback never executes concurrently with module unload. |
| **OPEN** | Invariant has not yet been established or characterized. | Behavior during DMA mapping failure under memory pressure is unverified. |

This epistemic discipline prevents *"Rust makes it safe"* from becoming an unverified marketing assertion.

---

## 11. The Migration Unit

Kernel migration must not be planned as "Rewrite Subsystem X in Rust." Work is organized into discrete, verifiable **Migration Units**:

```
Migration Unit
  ├── 1. Existing C API specification
  ├── 2. Semantic contract & invariant audit
  ├── 3. Safe Rust abstraction
  ├── 4. Bounded FFI boundary
  ├── 5. Idiomatic Rust implementation
  ├── 6. Bidirectional C compatibility layer
  ├── 7. KUnit & kselftest test suite
  ├── 8. Benchmarked performance measurements
  ├── 9. Clear subsystem review ownership
  └── 10. Documented rollback strategy
```

Migration is **non-binary**: it proceeds incrementally across well-defined semantic seams.

```
C subsystem
     │
     ├── API A ──► Rust wrapper A
     ├── API B ──► Rust wrapper B
     ├── API C ──► Unchanged C
     └── API D ──► Rust implementation
```

---

## 12. Migration Dependency Graph

Subsystem migrations must explicitly map dependencies back to kernel core abstractions:

```
                 Rust module
                      │
                      ▼
               Rust abstraction
                      │
           ┌──────────┼──────────┐
           ▼          ▼          ▼
        locking     memory      device
           │          │          │
           ▼          ▼          ▼
         C API      C API       C API
           │          │          │
           └──────────┼──────────┘
                      ▼
                  subsystem
```

When a required abstraction is missing:

```
driver migration
  │
  ▼
missing abstraction identified
  │
  ▼
abstraction patch written
  │
  ▼
reference driver user attached
  │
  ▼
upstream subsystem + RFL dual review
```

This explains why the **Rust reference driver** strategy is an upstream prerequisite.

---

## 13. What a Migration Architect Must Optimize

A technical lead does not optimize for *"lines of C replaced."* True migration optimization evaluates twelve dimensions:

| Dimension | Critical Architectural Question |
| :--- | :--- |
| **Safety** | What specific bug classes (UAF, double-free, data race) are eliminated? |
| **Soundness** | Are the Rust abstractions sound under all adversarial inputs? |
| **Coverage** | How much meaningful subsystem functionality is implemented in Rust? |
| **FFI Surface** | How much unsafe boundary remains exposed? |
| **Maintainability** | Is the resulting code cleaner and easier to maintain than the C original? |
| **Performance** | Did latency, throughput, CPU overhead, or memory footprint degrade? |
| **Reviewability** | Can traditional C maintainers realistically inspect and review patches? |
| **Testing** | Is test coverage strictly equal to or better than the original C baseline? |
| **Toolchain** | Is the minimum compiler toolchain sustainable for long-term LTS distros? |
| **Governance** | Does the subsystem maintainer community actively support this integration? |
| **Talent** | Can future contributors and maintainers understand and debug the code? |
| **Portability** | Does the code build and run on all target architectures supported by the driver? |

$$\text{Optimization Target}: \frac{\text{Unsafe / Implicit Invariants}}{\text{Implicit Conventions}} \Longrightarrow \frac{\text{Explicit / Sound Invariants}}{\text{Mechanically Enforced Types}}$$

---

## 14. Leadership-Level Failure Modes

A migration lead must actively defend against five fatal anti-patterns:

### Failure Mode A — "Rust Automatically Makes It Safe"
**Fallacy:** Assuming that writing Rust code guarantees kernel safety.  
**Reality:** The trust chain `Rust → unsafe FFI → C → hardware` is only as strong as its weakest link.

### Failure Mode B — Mechanical Translation
**Fallacy:** Translating C functions line-by-line into Rust.  
**Reality:** Replicates C's implicit assumptions and raw pointers into an unidiomatic, unmaintainable Rust codebase. The target is semantic re-architecture.

### Failure Mode C — Abstraction Leakage
**Fallacy:** Writing a "safe" wrapper that still requires the caller to know C rules.  
**Reality:** If callers must read C docs to know *"call function X only while holding spinlock Y,"* the abstraction has failed.

### Failure Mode D — Unsafe Creep
**Fallacy:** Allowing convenient `unsafe` escape hatches in driver code.  
**Reality:** One escape hatch leads to another. The Rust layer rapidly degenerates into C syntax with a Rust compiler. Unsafe code must be contained strictly inside audited abstraction crates.

### Failure Mode E — Benchmark Blindness
**Fallacy:** Delivering safety at the expense of unacceptable throughput or latency regressions.  
**Reality:** The Linux kernel will reject abstractions that introduce avoidable performance penalties. Safety and zero-cost performance must be achieved together.

---

## 15. The Practical Qualification Assessment: The Context Matrix

To qualify an RFL engineer, avoid trivia questions. Provide an existing C subsystem driver and require the candidate to deliver a **15-Artifact Engineering Qualification Dossier**:

1. Semantic inventory
2. Ownership graph
3. Lifetime graph
4. Concurrency & locking graph
5. **Execution-context matrix**
6. Bounded FFI boundary definition
7. Safe Rust abstraction specification
8. Unsafe invariant proof document
9. Implementation code
10. KUnit test suite
11. Concurrency stress tests
12. Sanitizer & lockdep verification evidence
13. Comparative performance benchmarks
14. Upstream-ready patch series (`git send-email` formatted)
15. Maintainer review response simulation

### The Execution-Context Matrix Gate
The candidate must fill out and defend an execution matrix for every API in the subsystem:

| Subsystem API | Process Context | Hardirq Context | Softirq Context | May Sleep? | Lock Required | RCU Required |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `api_action_a()` | ✓ | ✗ | ✗ | **YES** | `mutex` | No |
| `api_action_b()` | ✓ | ✓ | ✓ | **NO** | `spinlock` | No |
| `api_action_c()` | ✓ | ✓ | ✓ | **NO** | None | **YES** |
| `api_action_d()` | ✓ | ✗ | ✓ | **NO** | `spin_lock_bh` | Optional |

The decisive qualification question:

> **How does your Rust API mechanically prevent callers from violating these context and locking constraints at compile time?**

---

## 16. The Ultimate Skill Hierarchy

```
                      Rust syntax
                           ↓
                     Rust semantics
                           ↓
                    unsafe reasoning
                           ↓
                      C semantics
                           ↓
                    Linux semantics
                           ↓
                 concurrency semantics
                           ↓
                   hardware semantics
                           ↓
                  subsystem architecture
                           ↓
                  migration architecture
                           ↓
                    upstream design
```

An engineer who masters the entire chain is not merely a "Rust programmer writing kernel modules"—they are a **Systems Migration Architect**.

### The Fundamental Question of Rust-for-Linux
> **Which invariants currently exist only in human knowledge, comments, conventions, locking discipline, lifetime rules, and subsystem culture—and which of those can be converted into mechanically enforceable interfaces without breaking Linux?**
