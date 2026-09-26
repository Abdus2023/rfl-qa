# Rust for Linux (RFL) Engineering Qualification Specification v3.0 (Definitive Edition)

> Deterministic, evidence-first qualification framework establishing the four invariant classes (Types A–D), empirical proficiency tiers ($L_n\text{-}E$), nine independent competency domains, teardown-first lifecycle design, trust-boundary accounting, adversarial super-gates, and the 17-step Migration Architect qualification protocol.

---

## Core Definition of the Profession

> **An RFL engineer is not primarily a Rust programmer.**  
> They are an engineer of semantic boundaries between hardware, Linux's C execution model, Rust's safety model, and the kernel's upstream governance system.

An **RFL Migration Architect** adds one final, critical capability:  
*They can decide which boundaries should change, in what order, with what evidence, and at what long-term maintenance cost.*

---

## 1. Core Philosophy: The Four Invariant Types

The foundational premise of RFL engineering is that **the Rust type system is not a complete kernel proof system**. A qualified engineer must classify every invariant into one of four distinct categories and apply the correct enforcement mechanism:

```
                      KERNEL INVARIANTS
                              │
     ┌────────────────┬───────┴────────┬────────────────┐
     ▼                ▼                ▼                ▼
  Type A           Type B           Type C           Type D
Compiler-        API-             Runtime-         External /
Enforceable      Enforceable      Enforced         System
```

| Type | Description | Enforcement Mechanism | Concrete Kernel Example |
| :--- | :--- | :--- | :--- |
| **A. Compiler-Enforceable** | Properties proven by the Rust type system and borrow checker under sound assumptions. | Rust borrow checker, type checker, lifetime variance, Send/Sync markers. | `&T` cannot outlive `T`; `MutexGuard` must be dropped to release the lock; aliasing exclusivity (`&mut`). |
| **B. API-Enforceable** | Properties made unrepresentable or structurally enforced by safe abstraction design. | Typestate patterns, RAII guards, phantom tokens, `pin-init` in-place initialization. | Tying a returned reference's lifetime to an active `LockGuard`; requiring an `RcuGuard` token to dereference protected pointers. |
| **C. Runtime-Enforced** | Properties that must be checked dynamically due to configuration, hardware state, or dynamic execution paths. | `lockdep`, `KASAN`, `KMSAN`, `KCSAN`, `BUG_ON`, `might_sleep()`, `refcount_t` saturation. | Detecting a sleeping allocation (`GFP_KERNEL`) called with local IRQs disabled; verifying lock hierarchy ordering. |
| **D. External / System** | Properties established and maintained outside the Rust abstraction's boundary. | Subsystem contracts, C core callback sequencing, hardware register specs, firmware Device Tree. | The C network core guaranteeing that `ndo_stop` will not execute concurrently with `ndo_start_xmit` without external locks. |

### The Golden Rule of RFL
> **Encode every invariant that can reasonably be encoded in Type A or B. Explicitly verify or defend Type C. Explicitly document, bound, and trust Type D. Never overclaim safety.**

---

## 2. The Capability + Evidence Matrix ($L_n\text{-}E$)

Capability without empirical evidence is merely a claim. Matrix v3.0 indexes every proficiency level against its **Evidence Context**:

### Capability Levels ($L_0$ to $L_5$)
* **L0 (Unaware):** Does not know the concept exists or its operational relevance to the kernel.
* **L1 (KNOW):** Can explain the concept, theory, and kernel relevance; requires guidance to implement.
* **L2 (USE):** Can implement standard patterns using existing abstractions safely.
* **L3 (AUDIT):** Can independently implement complex patterns; audits others' code; spots subtle defects, invariant violations, and concurrency leaks.
* **L4 (DESIGN):** Designs novel, sound abstractions; resolves conflicting constraints; creates safe APIs over unsafe C boundaries; writes formal `SAFETY` proofs.
* **L5 (LEAD):** Defines subsystem architecture, upstream strategy, toolchain roadmap, and governance; makes technically defensible decisions under uncertainty.

### Evidence Tiers ($-E$)
* **`-T` (Theoretical / Examined):** Evaluated through whiteboard defense, verbal examination, or written specification.
* **`-C` (Controlled / Lab):** Demonstrated in an isolated sandbox, synthetic kernel module exercise, or CTF environment.
* **`-P` (Production / Upstream):** Demonstrated in merged upstream LKML patches, public review history, real hardware execution, or audited production code.
* **`-U` (Unverified):** Claims capability without verifiable evidence. *(Note: An L4-U candidate is treated as L2 for qualification purposes).*

$$\mathbf{L4\text{-}P} \equiv \text{Has designed and merged a core abstraction actively used by in-tree drivers upstream.}$$

---

## 3. The 9-Domain Competency Model

Matrix v3.0 maintains strict separation between **Verification & Observability** and **Toolchain & Build Engineering**:

$$\text{Verification Competence} \neq \text{Toolchain/Build Competence}$$

A systems engineer can master dynamic sanitizers and syzkaller reproducers while lacking the specialized knowledge needed to maintain Kbuild, LLVM/Clang patching, target triples, and Debian/LTS toolchain policies.

```
                         RFL ENGINEERING
                               │
         ┌─────────────────────┼──────────────────────┐
         │                     │                      │
      SEMANTICS            IMPLEMENTATION         EVIDENCE
         │                     │                      │
         ├─ C contracts        ├─ Rust               ├─ KUnit
         ├─ lifetimes          ├─ FFI                ├─ KASAN / KCSAN
         ├─ LKMM               ├─ RFL APIs           ├─ lockdep
         ├─ context            ├─ Kbuild             ├─ syzkaller
         └─ hardware           └─ drivers            └─ ftrace / eBPF
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                        ABSTRACTION DESIGN
                               │
                     ┌─────────┴─────────┐
                     │                   │
                 SAFE API          UNSAFE CORE
                     │                   │
              invariant proof            └─ (Trust-Boundary Inventory)
                     │
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

### The 9 Independent Domains
1. **Domain 1: Hardware & Architecture:** CPU privilege rings, MMU/page tables, TLB shootdowns, APIC/GIC, DMA/IOMMU, PCIe BARs, USB URBs, cache hierarchies, NUMA nodes, early boot/pre-slab.
2. **Domain 2: Linux Core Internals:** `task_struct`, scheduling, namespaces/credentials, VFS/inodes, `copy_to/from_user`, slab/SLUB & GFP flags, buddy pages, VMAs, device model (`kobject`), module init/exit, `ERR_PTR`, workqueues, timers, wait queues/completions.
3. **Domain 3: Concurrency, LKMM & RCU:** LKMM fundamentals, compiler vs CPU ordering, memory barriers, atomics, spinlocks/mutexes/rwlocks, `refcount_t`, RCU read-side/grace periods/SRCU, per-CPU data, lockdep class keys, bottom/top halves, atomic context bans, `kernel::sync`.
4. **Domain 4: C Semantics & FFI:** C calling conventions, `repr(C)` & padding, bitfields, variadics, C macro reverse engineering, implicit contract discovery, callback teardown races, intrusive lists (`list_head`), `bindgen` pipelines, error translation, FFI ownership transfers.
5. **Domain 5: Kernel-Grade Rust & `unsafe`:** `no_std`/`core`, custom panic/OOM handlers, unsafe invariant engineering, alias analysis, lifetime variance, `Send`/`Sync` markers, `UnsafeCell`, `MaybeUninit`, drop semantics, `Pin`/`pin-init`, trait objects, proc macros, zero-cost LLVM verification, custom allocators.
6. **Domain 6: RFL `kernel` Crate & Abstractions:** Crate architecture, safe subsystem wrappers, reference driver pattern, context-encoding types, lock/RCU guards, abstraction leakage prevention, minimal unsafe surface area, C callback trampolines, KUnit integration, C compatibility guarantees.
7. **Domain 7: Verification & Observability:** KUnit for Rust, kselftest harnesses, KASAN/KMSAN/KFENCE, UBSAN, KCSAN data race detection, lockdep assertions, QEMU/GDB/KGDB, ftrace & eBPF tracing, Syzkaller coverage-guided fuzzing.
8. **Domain 8: Toolchain & Build Engineering:** Kbuild/Makefile integration, `rustc` toolchain pinning policy (Rust 1.85.0+ baseline), unstable feature tracking, Clang/LLVM/`bindgen` pipeline, `rust-analyzer` kernel configuration, CI automation.
9. **Domain 9: Governance & Migration Strategy:** LKML etiquette (`b4`/`git send-email`), subsystem maintainer dynamics, RFL dual-maintainership, migration unit scoping, dependency graph modeling, safety vs performance benchmarks, reviewability metrics, toolchain sustainability, upstream RFC defense.

---

## 4. Trust-Boundary Accounting & Abstraction Quality

Counting lines of `unsafe` is a vanity metric. What matters is the **topology, auditability, and defense of the trust boundary**.

### The Unsafe Surface Inventory
For every migration unit, the engineer must produce an explicit inventory:

| Boundary Seam | Unsafe? | Why? | Invariant Required | Verification Evidence |
| :--- | :---: | :--- | :--- | :--- |
| **FFI Call to C** | Yes | C ABI | Valid pointer, initialized memory | KUnit test + KASAN |
| **C Callback into Rust** | Yes | C invokes Rust | Object lifetime > callback execution | Refcount + `rcu_barrier` |
| **DMA Mapping** | Yes | Hardware physical memory | DMA contract honored by device | DMA API + IOMMU tests |
| **Intrusive List Traversal** | Yes | C structure | Lock or RCU read guard held | lockdep assertion + KCSAN |

### The Minimization Principle
The goal is not *zero unsafe*. The goal is:

> **A minimal, auditable unsafe surface with explicit invariants, transforming scattered C conventions into tightly bounded Rust FFI layers wrapped by safe public APIs.**

### Abstraction Quality Gate (Mandatory L4 Requirement)
A wrapper can be memory-safe and still be a terrible abstraction. It must be evaluated across seven dimensions:

1. **Safety:** Does it prevent invalid states and undefined behavior?
2. **Completeness:** Does it expose everything legitimate users need without forcing them to bypass the crate?
3. **Leakage:** Does the caller need C implementation knowledge? *(If the caller must know C locking rules, it fails).*
4. **Composability:** Can other kernel Rust code consume it naturally?
5. **Performance:** Does the abstraction impose measurable, unjustified runtime overhead?
6. **Evolution:** Can the underlying C implementation change without breaking Rust callers?
7. **Reviewability:** Can an upstream maintainer understand and verify the safety argument in 5 minutes?

---

## 5. The Adversarial Qualification Super-Gates

Candidates for L3, L4, and L5 must survive adversarial engineering gates designed to test the reality of kernel complexity.

```
┌────────────────────────────────────────────────────────┐
│ Super-Gate 1: Teardown-First & Concurrent Teardown     │
│ Destruction designed first; survives concurrent ioctl  │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Super-Gate 2: Invariant Classification & Negative Space│
│ Types A–D mapped; explicit negative-space bounds       │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Super-Gate 3: Semantic-Diff & Trust-Boundary Audit     │
│ 12-dimension semantic diff; full unsafe inventory      │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Super-Gate 4: Context Enforcement (Static vs Dynamic)  │
│ Type B typestate tokens vs Type C runtime assertions   │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Super-Gate 5: Failure Path Exhaustion (No Panic)       │
│ Deliberate bounded behavior across all 8 failure modes │
└────────────────────────────────────────────────────────┘
```

---

### Super-Gate 1: Teardown-First & Concurrent Teardown
*Amateurs design `create -> use`. Kernel engineers design `unregister -> quiesce -> destroy`.*

* **The Proof Task:** Given a C subsystem with asynchronous callbacks, workqueues, and reference counts, design the **destruction path** before the steady-state path:
  $$\text{STOP NEW WORK} \longrightarrow \text{QUIESCE} \longrightarrow \text{CANCEL/FLUSH CALLBACKS} \longrightarrow \text{RELEASE REFS} \longrightarrow \text{WAIT FOR READERS} \longrightarrow \text{DESTROY} \longrightarrow \text{FREE}$$
* **Adversarial Concurrent Teardown Test:** Map a scenario where CPU0 is executing an active `ioctl()` (holding an in-flight reference) while CPU1 executes `remove()` (unregistering and freeing the device).
* **Failure Condition:** The candidate relies on Rust's `Drop` trait to handle teardown without coordinating with the C-side `kref`, workqueue flush, or RCU grace periods. If this allows a Use-After-Free, double-free, callback-after-destruction, or deadlock, the candidate **FAILS**.

---

### Super-Gate 2: Invariant Classification & Negative-Space Analysis
*Rust cannot prove hardware or external C subsystem correctness.*

* **The Proof Task:** Take a complex C API. Classify every invariant into Type A (Compiler), Type B (API), Type C (Runtime), or Type D (External). Author a mandatory **Negative-Space Document** explicitly stating what the Rust abstraction does *not* guarantee:
  * *Guaranteed (Type A/B):* "This abstraction guarantees the buffer cannot be freed while a reference exists."
  * *Not Guaranteed (Type D):* "This abstraction does NOT guarantee the hardware DMA engine has flushed its FIFO or that registers return valid data."
* **Failure Condition:** Overclaiming safety. If the candidate claims the Rust API makes the subsystem "100% memory safe" while ignoring underlying C-side global state mutations or hardware races, the candidate **FAILS**.

---

### Super-Gate 3: Semantic-Diff & Trust-Boundary Audit
*Line-by-line translation is a catastrophic failure mode.*

* **The Proof Task:** Given an existing C implementation and a proposed Rust rewrite, produce a **Semantic Diff** across 12 dimensions:
  1. Inputs / Outputs  
  2. Error Representation  
  3. Lifetimes  
  4. Locking Contracts  
  5. Atomicity  
  6. Execution Context  
  7. Callbacks & Asynchrony  
  8. Resource Ownership  
  9. Side Effects  
  10. Memory Ordering  
  11. Teardown Sequence  
  12. Negative Space (Unenforced Contracts)  
  Deliver the accompanying **Unsafe Surface Inventory** mapping every FFI boundary.
* **Failure Condition:** Performing a line-by-line syntax conversion; missing an implicit memory barrier or lock acquisition assumption present in the C code.

---

### Super-Gate 4: Context Enforcement (Static vs. Dynamic)
*Not all context restrictions can or should be static.*

* **The Proof Task:** Design an API that prevents calling a sleeping function from an atomic/IRQ context. Determine which constraints can be enforced via Rust types (Type B typestate/tokens) and which *must* be enforced via runtime kernel assertions (Type C, e.g., `might_sleep()`, `in_atomic()`).
* **Failure Condition:** Attempting to encode every dynamic execution context (Process, IRQ, Softirq, NMI, BH-disabled, `PREEMPT_RT`) into an unergonomic, bloated static typestate system that breaks under dynamic kernel configuration.

---

### Super-Gate 5: Failure Path Exhaustion (Beyond "No `unwrap`")
*A kernel panic kills the machine; all failure paths must be bounded.*

* **The Proof Task:** Prove that every reachable failure path has a deliberate, bounded kernel outcome across all eight failure modes:
  1. Allocation failure (`ENOMEM`)
  2. Invalid user-space input (`EFAULT`)
  3. Unexpected C-side error return or `ERR_PTR`
  4. Hardware timeouts or MMIO faults
  5. Resource exhaustion (IDs, IRQ lines, bounce buffers)
  6. Concurrent unregister/teardown in-flight
  7. Partial initialization during `probe()` unwind
  8. Asynchronous workqueue/timer cancellation
* **Failure Condition:** Using `unwrap()` or `expect()` in kernel paths; failing to cleanly unwind partially allocated resources on error; failing to return an appropriate negative `errno`.

---

## 6. Role Progression & Threshold Matrix

To qualify for an operational role, an engineer must meet both the **Proficiency Level** and the **Empirical Evidence Tier** across all 9 domains:

| Domain | Contributor (L2/L3 Focus) | Subsystem Rust Maintainer (L3/L4 Focus) | Migration Architect (L4/L5 Focus) |
| :--- | :---: | :---: | :---: |
| **1. Hardware & Architecture** | **L1-C** (Conceptual) | **L2-C** (Target ISA mastery) | **L4-P** (Cross-ISA portability & weak ordering) |
| **2. Linux Core Internals** | **L2-C** (VFS, Device, Memory APIs) | **L3-P** (Audits lifecycle, teardowns, GFP) | **L5-P** (Defines core subsystem boundaries) |
| **3. Concurrency & LKMM** | **L2-C** (Uses `kernel::sync` correctly) | **L4-P** (Designs lockless/RCU abstractions) | **L5-P** (Resolves LKMM vs Rust model conflicts) |
| **4. C Semantics & FFI** | **L2-C** (Writes standard wrappers) | **L4-P** (Reverse-engineers implicit C contracts) | **L5-P** (Negotiates C API evolution for Rust) |
| **5. Kernel-Grade Rust** | **L3-C** (Audits `unsafe`, no panics) | **L4-P** (Designs sound `pin-init` abstractions) | **L5-P** (Sets tree-wide `unsafe` and soundness policy) |
| **6. RFL `kernel` Crate** | **L2-C** (Extends existing module wrappers) | **L4-P** (Designs new core crate modules) | **L5-P** (Architects long-term crate evolution) |
| **7. Verification & Observability** | **L2-C** (Writes KUnit tests, checks CI) | **L3-P** (Integrates KASAN, lockdep, syzkaller) | **L4-P** (Designs complete verification pipelines) |
| **8. Toolchain & Build** | **L1-C** (Builds via Kbuild) | **L3-C** (Debugs `bindgen`/LLVM issues) | **L5-P** (Sets toolchain pinning & distro policy) |
| **9. Governance & Migration** | **L2-P** (LKML etiquette, `b4`, reviews) | **L4-P** (Mentors contributors, reviews PRs) | **L5-P** (Manages upstream politics, RFCs, Linus) |

---

## 7. The Ultimate Migration Architect Qualification (17-Step Protocol)

To qualify as an **L5 Migration Architect**, the candidate must take an existing Linux C subsystem and execute the following 17-step engineering protocol, defending every decision under adversarial review:

1. **Extract Semantic Contracts:** Reverse-engineer the subsystem's implicit assumptions, locking discipline, and execution constraints.
2. **Map Ownership & Lifetimes:** Construct explicit graphs of resource ownership, parent-child lifecycles, and asynchronous destruction paths.
3. **Map Execution Contexts:** Identify process, IRQ, softirq, and atomic regions for all subsystem entry points.
4. **Identify Synchronization Mechanisms:** Audit locks, sequence counters, completions, and per-CPU data structures.
5. **Identify LKMM Dependencies:** Map explicit memory barriers, atomics, and ordering requirements.
6. **Identify FFI Boundaries:** Determine the exact seam where C transitions into Rust.
7. **Classify Invariants:** Categorize every contract into Type A (Compiler), Type B (API), Type C (Runtime), or Type D (External).
8. **Design Migration Units:** Partition the migration into discrete, incrementally mergeable, non-binary units.
9. **Design Rust Abstractions:** Construct sound Type A/B Rust wrappers making misuse unrepresentable.
10. **Define Runtime Verification (Type C):** Implement KUnit tests, lockdep annotations, and dynamic sanitizer checks.
11. **Document & Bound External Contracts (Type D):** Formulate the Negative-Space Document detailing external assumptions.
12. **Minimize the Unsafe Surface:** Produce the Unsafe Surface Inventory, eliminating unnecessary `unsafe` operations.
13. **Define the Verification Strategy:** Set up KUnit suites, kselftest harnesses, and Syzkaller fuzzing profiles.
14. **Measure Performance:** Benchmark latency, throughput, and CPU overhead against the C baseline to prove zero-cost abstractions.
15. **Define Rollback & Compatibility Boundaries:** Establish clear rollback criteria; differentiate Userspace ABI (immutable) from Internal Kernel API (fluid) and FFI ABI.
16. **Author Upstream Patch / RFC Series:** Format patch series for `git send-email`/`b4`, CCing subsystem maintainers and RFL maintainers.
17. **Defend & Iterate:** Defend the architecture under adversarial review on LKML, revising the design when empirical evidence disproves an assumption.

---

## The Definitive Metric of Success

The qualification of an RFL Migration Architect is not measured by:

$$\text{"How many lines of C did you replace?"}$$

The definitive metric of success is:

$$\mathbf{M} = \frac{\Delta \text{ Implicit Risk Converted to Explicit, Reviewable, Verifiable Invariants}}{\text{Long-Term Upstream Maintenance \& Review Burden}}$$

An RFL engineer does not eliminate the physical hardware, the C substrate, or the upstream community. They build the **verifiable type-system bridge** that allows the Linux kernel to safely and maintainably evolve across them all.
