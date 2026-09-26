# Rust for Linux (RFL) Engineering Qualification Matrix v2.0 (2026 Edition)

> Measurable, evidence-first qualification framework mapping 100 granular competencies across eight engineering domains, L0–L5 proficiency levels, adversarial proof tasks, failure anti-patterns, and qualification super-gates for Contributors, Subsystem Maintainers, and Migration Architects.

---

## Core Paradigm

> **Knowing a technology is not evidence of being able to use it safely in the kernel.**

The objective is not a ground-up rewrite, but the construction of a **sound, maintainable, mixed-language kernel** where Rust incrementally encodes implicit C invariants into explicit, mechanically enforced interfaces without weakening Linux's performance, concurrency semantics, or subsystem governance.

To operationalize this, we measure capability rather than vocabulary through:
1. Standardized **L0–L5 proficiency levels** (mapped to KNOW, USE, AUDIT, DESIGN, LEAD).
2. The **100-Competency Curriculum Map** grouped across 8 engineering domains.
3. Concrete **Proof Tasks** and **Adversarial Failure Tests**.
4. The **5 Qualification Super-Gates**.
5. The **Role Threshold Matrix** for Contributors, Maintainers, and Architects.

---

## Part 1: Proficiency Level Definitions (L0–L5)

Every competency in the matrix is evaluated against these six standardized levels:

| Level | Title | Definition | Kernel Operational Context |
| :--- | :--- | :--- | :--- |
| **L0** | **Unaware** | Does not know the concept exists or its operational relevance to the kernel. | Cannot participate in kernel engineering discussions. |
| **L1** | **Aware (KNOW)** | Can explain the concept, its purpose, and why it matters in Linux; requires guidance to implement. | Reads kernel code; understands vocabulary; cannot write sound kernel patches without direct supervision. |
| **L2** | **Practitioner (USE)** | Can implement standard tasks using existing abstractions; understands the happy path and basic pitfalls. | Writes safe Rust drivers using existing `kernel::` abstractions; passes standard code review. |
| **L3** | **Auditor (AUDIT)** | Independently implements complex patterns; reads others' code and spots invariant violations, leaks, or race conditions. | Audits PRs; finds subtle defects in `unsafe` blocks; identifies C-side lifetime and locking conflicts. |
| **L4** | **Designer (DESIGN)** | Designs new, sound abstractions from scratch; solves novel FFI/lifetime problems; writes rigorous `SAFETY` proofs. | Designs new `kernel::` subsystem modules; writes `pin-init` abstractions; negotiates API boundaries with C maintainers. |
| **L5** | **Authority / Architect (LEAD)** | Defines subsystem architecture, upstream strategy, and governance; resolves deep semantic and cross-domain conflicts. | Sets RFL toolchain and `unsafe` policy; negotiates cross-subsystem ABI changes with Linus and subsystem maintainers. |

---

## Part 2: The 100-Competency Curriculum Map (8 Domains)

### Domain 1: Systems Foundation & Hardware Architecture (1–10)
*Understanding the physical machine and OS theory; Rust's type system does not eliminate hardware reality.*

1. **CPU Privilege Rings & Exception Entry/Exit:** Ring transitions, privilege modes (user vs kernel), exception vectors, and syscall dispatch.
2. **MMU & Page Table Management:** Multi-level paging (PGD/P4D/PUD/PMD/PTE), page faults, huge pages, and TLB invalidation.
3. **TLB Shootdowns & Hardware Coherency:** Inter-processor interrupts (IPIs) for TLB shootdown, broadcast TLB operations, and hardware coherence boundaries.
4. **Interrupt Controllers:** APIC, GICv3/v4, IRQ domain mapping, MSI/MSI-X allocation, and nested interrupt handling.
5. **DMA Mapping & IOMMU Topologies:** Coherent vs streaming DMA, bounce buffers (SWIOTLB), IOMMU translation domains, and cache flushing/invalidation.
6. **PCIe Enumeration & BAR Management:** Configuration space parsing, Base Address Register mapping, memory-mapped I/O (MMIO), and hotplug events.
7. **USB & Bus Device Topologies:** URB (USB Request Block) lifecycle, USB host controller interfaces (xHCI), and hierarchical device trees.
8. **Cache Hierarchies & Coherency Protocols:** Cache lines, false sharing, MESI/MOESI protocols, and CPU cache-line alignment requirements.
9. **NUMA Topologies & Memory Nodes:** Non-Uniform Memory Access nodes, remote vs local memory latency, zone allocators, and socket affinity.
10. **Boot Sequence & Early Init:** UEFI/BIOS handoff, kernel decompression, early printk, pre-slab initcalls, and architecture boot phases.

* **Required Levels:** Contributor (L1–L2), Maintainer (L2–L3), Architect (L4)
* **Concrete Proof Task:** Write a bare-metal or kernel-module Rust driver for a DMA-capable device. Correctly map physical to virtual memory, handle cache flushing/invalidation, and process hardware interrupts without data corruption.
* **Failure Test (The Anti-Pattern):** Assuming virtual addresses are physically contiguous; forgetting to flush/invalidate DMA caches before CPU access; allocating DMA buffers from standard heap memory instead of using the DMA API.

---

### Domain 2: Linux Core Internals & C Semantics (11–25)
*Mastery of the 30-million-line C substrate; identifying implicit contracts invisible to compilers.*

11. **`task_struct` & Scheduling Mechanics:** Task lifecycle, context switching, CPU runqueues, CFS scheduling classes, and preemption flags.
12. **Process/Thread Lifecycle & Teardown:** Fork, clone, exit paths, zombie reaping, thread termination, and asynchronous signal delivery.
13. **Credentials, Namespaces & Capabilities:** UID/GID credentials, user/PID/network namespaces, capability bits (`CAP_SYS_ADMIN`), and security boundaries.
14. **VFS & Inode Lifecycle:** Virtual File System architecture, `inode`, `dentry`, `dcache` lookup, mount points, and pathname resolution.
15. **File Descriptors & `file_operations`:** File table slots, `file_operations` vtable, `open`/`read`/`write`/`release` lifecycle, and `ioctl` dispatch.
16. **User/Kernel Memory Boundary:** `copy_to_user()`, `copy_from_user()`, user pointer validation (`access_ok`), and page fault handling during copy.
17. **Slab/SLUB Allocators & GFP Flags:** `kmalloc`, cache creation (`kmem_cache_create`), and GFP allocation flags (`GFP_KERNEL`, `GFP_ATOMIC`, `GFP_NOWAIT`).
18. **Buddy Allocator & Page Management:** Page frames (`struct page`), page allocation order, compound pages, and physical memory zones (ZONE_NORMAL, ZONE_DMA32).
19. **Virtual Memory Areas (VMAs) & `mmap`:** `vm_area_struct` management, anonymous vs file-backed mapping, page protection flags, and fault handlers.
20. **Device Model & Sysfs:** `struct device`, `kobject`, `kset`, reference counting, attribute groups, and sysfs sys-tree integration.
21. **Module Loading & Init/Exit Sequences:** Module refcounts, module parameters, `module_init`/`module_exit`, and race-free module unload.
22. **Error Pointer Conventions:** Kernel pointer error tagging: `ERR_PTR`, `PTR_ERR`, `IS_ERR`, and `IS_ERR_OR_NULL`.
23. **Workqueues & Asynchronous Contexts:** Normal, bound, unbound, and high-priority workqueues; delayed work; cancel-sync flush semantics.
24. **Timers & Delayed Execution:** Low-resolution timers (`timer_list`), high-resolution timers (`hrtimer`), and softirq execution constraints.
25. **Wait Queues & Completions:** `wait_queue_head_t`, condition sleeping (`wait_event_interruptible`), and completion synchronization (`complete`/`wait_for_completion`).

* **Required Levels:** Contributor (L2), Maintainer (L3), Architect (L5)
* **Concrete Proof Task:** Map the complete ownership and lifetime graph of a complex C subsystem teardown (e.g., netdevice unregistration or block device unplug). Identify every implicit lifetime assumption, callback execution context, and refcount dependency.
* **Failure Test (The Anti-Pattern):** Treating `ERR_PTR` as a standard integer; assuming a deferred workqueue callback cannot fire after a parent structure's release function has initiated teardown; assuming a C function is thread-safe simply because it contains no lock.

---

### Domain 3: Concurrency, LKMM & RCU (26–40)
*Navigating the Linux Kernel Memory Model, multi-core synchronization, and lockless scalability.*

26. **Linux Kernel Memory Model (LKMM) Fundamentals:** Ordering semantics, happens-before relations, program-order vs execution-order, and compiler reordering.
27. **Compiler vs CPU Memory Ordering:** Compiler barriers (`barrier()`), hardware memory barriers, store-buffering, and weak vs strong memory architectures.
28. **Memory Barriers & Atomics:** Explicit barriers (`smp_mb`, `smp_rmb`, `smp_wmb`), `READ_ONCE()`, `WRITE_ONCE()`, and relaxed vs acquire-release atomics.
29. **Spinlocks & IRQ Context Safety:** Uniprocessor vs SMP spinlocks, `spin_lock_irqsave()`, `spin_lock_bh()`, and deadlocks caused by IRQ inversion.
30. **Sleeping Locks (Mutexes, Semaphores):** Mutex lifecycle, sleeping in atomic context detection, optimistic spinning, and RT-mutex priority inheritance.
31. **Read-Write Locks & Seqlocks:** `rwlock_t`, read-write semaphores (`down_read`/`down_write`), and sequence counters (`seqlock_t`) for lockless reads.
32. **Refcounting Semantics:** `refcount_t` vs `atomic_t`, overflow saturation protection, and race-free cleanup upon zero.
33. **RCU Read-Side Critical Sections:** `rcu_read_lock()`, `rcu_read_unlock()`, dereferencing RCU pointers (`rcu_dereference`), and reader non-blocking axioms.
34. **RCU Grace Periods & Reclamation:** `synchronize_rcu()`, `call_rcu()`, quiescent states, grace period detection, and pointer publishing (`rcu_assign_pointer`).
35. **SRCU (Sleepable RCU):** Sleepable read-side critical sections (`srcu_read_lock`), dedicated SRCU domains (`srcu_struct`), and cleanup barriers.
36. **Per-CPU Variables & Preemption:** `get_cpu()`, `put_cpu()`, per-CPU allocators, preemption disabling, and CPU hotplug event hooks.
37. **Lock Dependency Validator (lockdep):** Lock classes, static class keys, acquisition order validation, and interpreting lockdep splats.
38. **Bottom-Half / Top-Half Concurrency:** Hardirq vs softirq concurrency, tasklet deprecation, and lock sharing between IRQ and process context.
39. **Atomic Context Restrictions:** Absolute rules against sleeping, memory allocation (`GFP_KERNEL`), and scheduling within atomic/IRQ regions.
40. **RFL `kernel::sync` Integration:** Rust wrappers for kernel locks, RCU guards, and lockdep-annotated lock initialization.

* **Required Levels:** Contributor (L2), Maintainer (L4), Architect (L5)
* **Concrete Proof Task:** Implement an RCU-protected data structure in Rust using `kernel::sync::rcu`. Ensure readers use RCU guards, writers publish updates atomically, old nodes are reclaimed only after a grace period, and lockdep validates lock ordering.
* **Failure Test (The Anti-Pattern):** Using standard Rust `std::sync::Arc` or `std::sync::atomic` across the FFI boundary; sleeping or using a `Mutex` inside an RCU read-side critical section; assuming `"pointer is non-null"` implies `"object remains alive"` under RCU.

---

### Domain 4: C Semantics Reverse Engineering & FFI (41–52)
*Bridging the C and Rust boundary: converting implicit contracts into explicit, sound types.*

41. **C ABI & Calling Conventions:** `extern "C"`, System V AMD64 / AAPCS64 ABIs, register usage, stack frame layout, and variadic functions (`va_list`).
42. **Struct Layout, Padding & Alignment:** `repr(C)`, field alignment, struct padding, zero-sized types (ZSTs), and explicit packed structs.
43. **Bitfields & Endianness in FFI:** Safe manual encoding/decoding of C bitfields, little/big endian conversions, and byte-order-specific drivers.
44. **C Macro Reverse Engineering:** Decoding macro-heavy C headers, macro constants, inline functions, and compile-time contract assertions.
45. **Implicit Contract Discovery:** Discovering undocumented preconditions: required locks, caller context, pointer provenance, and destruction order.
46. **Callback Registration & Teardown Races:** Asynchronous callbacks, unregister semantics, preventing callback invocation during or after memory deallocation.
47. **Global State & Intrusive Lists:** Traversing intrusive data structures (`struct list_head`, `hlist_node`) and modeling them safely without ownership duplication.
48. **`bindgen` Pipeline & Opaque Types:** Generating raw FFI definitions, configuring type allowlists/blocklists, and mapping opaque kernel types.
49. **Error Code Translation:** Mapping negative C integers, `ERR_PTR`, and `NULL` returns into idiomatic Rust `Result<T, kernel::error::Error>`.
50. **Handling C `NULL` vs Rust `Option<&T>`:** Non-null invariants, pointer validity proof, and mapping nullable C pointers without UB.
51. **FFI Ownership Transfer Semantics:** Borrowed raw pointers vs consumed pointers; encoding explicit transfer of cleanup responsibility.
52. **Zero-Cost FFI Abstraction:** Ensuring wrappers inline cleanly into direct C calls without adding function call or indirection overhead.

* **Required Levels:** Contributor (L2), Maintainer (L4), Architect (L5)
* **Concrete Proof Task:** Take a C API that requires a specific spinlock held and returns a pointer valid only while the lock is held. Design a safe Rust wrapper tying the reference's lifetime to the lock guard's lifetime, making invalid access unrepresentable.
* **Failure Test (The Anti-Pattern):** Exposing raw pointers in safe APIs; writing documentation telling users to "remember to hold a lock" instead of enforcing it via the type system; leaking C cleanup requirements to the Rust caller.

---

### Domain 5: Kernel-Grade Rust & Unsafe Invariant Engineering (53–69)
*Specialized `no_std` systems Rust; constructing bulletproof safety proofs.*

53. **`no_std` Environment & `core` Library:** Building against `core` and `alloc`, eliminating standard library dependencies, and handling missing runtime hooks.
54. **Custom Panic Handlers & OOM Policy:** Kernel panic formatting, `panic = "abort"`, and handling allocation failures gracefully without panicking.
55. **Unsafe-Code Invariant Engineering:** Documenting preconditions, invariants, establishment, maintenance, and invalidation for every `unsafe` block.
56. **Alias Analysis & Raw Pointer Rules:** Aliasing rules (`&` vs `&mut`), stacked borrows, raw pointer provenance, and preventing LLVM `noalias` UB.
57. **Lifetime Elision & Complex Borrow Graphs:** Bounded lifetimes, invariant/covariant/contravariant lifetimes across structs, and higher-rank trait bounds (`for<'a>`).
58. **Variance & Subtyping in Kernel Types:** Controlling variance over raw pointers with `PhantomData<fn() -> T>` vs `PhantomData<*const T>`.
59. **`Send` & `Sync` Kernel Semantics:** Auditing thread and context-safety of types wrapping raw C pointers; defining safe marker trait implementations.
60. **Interior Mutability in the Kernel:** `UnsafeCell`, `Opaque<T>`, and managing shared mutable state exposed to hardware or C code.
61. **`MaybeUninit` & Deferred Initialization:** Safe manipulation of uninitialized memory buffers, out-pointers, and preventing reads of uninitialized data.
62. **Drop Semantics & Destruction Orders:** Deterministic destruction, preventing double-frees, and managing teardown sequences across C boundaries.
63. **`Pin` API & Self-Referential Structs:** Address stability guarantees, structural pinning, `Pin::new_unchecked`, and preventing memory moves.
64. **`pin-init` & In-Place Initialization:** In-place struct initialization macros, safe fallible initialization, and handling kernel registration patterns.
65. **Trait Objects & Dynamic Dispatch:** `dyn Trait` in `no_std`, vtables, dynamic dispatch trade-offs, and memory layouts without runtime overhead.
66. **Procedural Macros for C Vtables:** Macro generation of C-compatible function pointer vtables from idiomatic Rust trait definitions.
67. **Zero-Cost Abstraction Validation:** Auditing `cargo expand`, LLVM IR, and assembly to confirm zero runtime overhead and no hidden allocations.
68. **Custom Allocators (`kmalloc` Wrappers):** `KBox`, `KVBox`, custom allocation flags (`Flags`), and fallible allocation APIs.
69. **Panic-Free Programming Patterns:** Eliminating `unwrap()`, `expect()`, array out-of-bounds panics, and division-by-zero panics from all execution paths.

* **Required Levels:** Contributor (L2–L3), Maintainer (L4), Architect (L5)
* **Concrete Proof Task:** Implement a self-referential kernel structure using `pin-init` that registers with a C subsystem. Ensure in-place initialization, correct lifetime attachment, and safe destruction upon unregister.
* **Failure Test (The Anti-Pattern):** Using `unwrap()` or `expect()` in kernel code; moving a pinned struct; implementing `Drop` manually without accounting for C refcounts reaching zero asynchronously; using standard library collections (`Vec`, `HashMap`).

---

### Domain 6: RFL `kernel` Crate & Abstraction Design (70–80)
*Designing the shared layer that makes the Linux kernel safely accessible to Rust.*

70. **`kernel` Crate Architecture:** Module layout, internal layering, visibility rules, and maintaining separation between raw bindings and safe APIs.
71. **Designing Safe Wrappers for Subsystems:** Porting and wrapping C subsystem interfaces into ergonomic, idiomatic, and sound Rust modules.
72. **The "Reference Driver" Pattern:** Developing clean in-tree reference drivers to bootstrap, validate, and prove new abstractions upstream.
73. **Encoding Execution Contexts in Types:** Using typestate or token patterns to prevent calling sleepable or blocking APIs from non-sleepable contexts.
74. **Guard Patterns for Locks & RCU:** Implementing RAII guard types that tie resource release, lock unlocking, and RCU exit to lexical scopes.
75. **Abstraction Leakage Prevention:** Ensuring callers of a safe Rust API never need to read C code or understand underlying C implementation details.
76. **Minimizing Unsafe Surface Area:** Isolating all `unsafe` operations inside minimal, heavily audited helper functions and abstraction modules.
77. **Translating Subsystem Idioms:** Mapping C idioms (e.g., container_of, private data pointers, vtable callbacks) to Rust traits and handles.
78. **Handling C Callbacks in Rust:** Implementing safe C-callable trampolines that convert raw parameters into safe Rust references and trap panics.
79. **KUnit Integration for Rust Abstractions:** Writing unit tests inside the `kernel` crate using kernel KUnit bindings to test wrappers directly.
80. **Maintaining C-Compatibility Guarantees:** Ensuring Rust abstractions do not alter, break, or compromise existing C ABI or kernel stability.

* **Required Levels:** Contributor (L2), Maintainer (L4), Architect (L5)
* **Concrete Proof Task:** Design a new `kernel::` abstraction for a hardware interrupt controller or platform driver. Prevent users from registering handlers in an invalid context, and provide automated KUnit test coverage.
* **Failure Test (The Anti-Pattern):** Bypassing the `kernel` crate to write ad-hoc FFI in driver code; allowing "unsafe creep" where driver code becomes C written in Rust syntax; failing to provide an in-tree reference user when proposing a new core abstraction.

---

### Domain 7: Verification, Toolchain & Build Integration (81–90)
*Kbuild integration, toolchain stability policies, dynamic sanitizers, and kernel fuzzing.*

81. **Kbuild & Makefile Integration:** Integration with the kernel's top-level `Makefile`, `rustc` rules, crate dependencies, and object generation.
82. **Toolchain Version Policy:** Tracking the kernel's Rust toolchain policy (e.g., Rust 1.85.0+ baseline), LTS distro toolchain support, and Debian 13 alignment.
83. **Unstable Feature Tracking:** Monitoring, reducing, and eliminating nightly/unstable feature usage to progress toward stable rustc compilation.
84. **LLVM/Clang & `bindgen` Pipeline:** Compiler flags, Clang integration, target triple specifications, and debugging libclang binding generation.
85. **KUnit & kselftest Frameworks:** Writing and running in-tree unit and integration tests under QEMU and bare metal.
86. **Memory Sanitizers (KASAN, KMSAN, KFENCE):** Configuring and triaging Kernel Address Sanitizer, Memory Sanitizer, and low-overhead KFENCE memory bug detectors.
87. **Undefined Behavior & Concurrency Sanitizers (UBSAN, KCSAN):** Triaging UB reports and detecting data races under Kernel Concurrency Sanitizer.
88. **Kernel Debugging (QEMU, GDB, KGDB):** Debugging kernel images, inspecting memory, tracing symbols, and analyzing crash dumps (`crash`/`kdump`).
89. **Dynamic Tracing (ftrace, eBPF):** Profiling Rust kernel code paths using ftrace tracepoints and eBPF tracing probes without disrupting timing.
90. **Kernel Fuzzing with Syzkaller:** Writing Syzkaller syscall descriptions for Rust-backed drivers and triaging coverage-guided fuzzing crashes.

* **Required Levels:** Contributor (L1–L2), Maintainer (L3), Architect (L5)
* **Concrete Proof Task:** Add a new Rust module to the kernel tree. Integrate it cleanly with `Kconfig` for conditional compilation, ensure it compiles under the pinned compiler toolchain, and write a KUnit test reproducing a known race condition under KCSAN.
* **Failure Test (The Anti-Pattern):** Modifying the compiler toolchain or introducing new unstable language features without community consensus; relying on user-space `cargo test` instead of KUnit; ignoring KASAN or lockdep splats in CI.

---

### Domain 8: Governance, Upstream Process & Migration Strategy (91–100)
*The human and architectural mechanics of the Linux kernel community.*

91. **LKML Etiquette & Patch Formatting:** `git send-email`, `b4` patch management, plain-text email formatting, commit message conventions, and patch versioning.
92. **Subsystem Maintainer Dynamics:** Navigating the Linux maintainer hierarchy, subsystem tree branching, and differences in subsystem review culture.
93. **RFL Dual-Maintainership Model:** Routing patches through both the subsystem maintainer tree and the Rust-for-Linux maintainer tree.
94. **Scoping Migration Units:** Decomposing large migration goals into bounded, incrementally mergeable, non-binary migration units.
95. **Dependency Graph Modeling:** Modeling multi-step abstraction dependencies and sequencing in-tree reference drivers before abstraction merges.
96. **Safety vs Performance Trade-offs:** Benchmarking throughput, latency, and memory footprint against C baselines to prove zero overhead.
97. **Reviewability & Maintainability:** Designing code that traditional C maintainers can read, audit, and understand without requiring a Rust PhD.
98. **Toolchain Sustainability & Distro Policy:** Evaluating long-term maintenance costs, compiler update cadences, and enterprise distribution support.
99. **Upstream Review Handling:** Constructively handling NACKs, review pushback, API redesign requests, and upstream revisions.
100. **Talent & Subsystem Sustainability:** Building documentation, mentoring contributors, and establishing sustainable review bandwidth.

* **Required Levels:** Contributor (L1–L2), Maintainer (L4), Architect (L5)
* **Concrete Proof Task:** Author an RFC for migrating a specific subsystem component to Rust. Include a complete dependency graph of required abstractions, a rollback plan, performance benchmarks proving no regression, and a reference driver implementation.
* **Failure Test (The Anti-Pattern):** Proposing a "big-bang" rewrite of a subsystem; ignoring a subsystem maintainer's concerns about ABI stability or review bandwidth; submitting patches without CCing both the subsystem and Rust maintainers.

---

## Part 3: The 5 Qualification Super-Gates

To verify L3, L4, and L5 capabilities, candidates must pass adversarial engineering gates. Passing requires surviving deliberate failure injections.

```
┌────────────────────────────────────────────────────────┐
│ Gate 1: Execution-Context Matrix Gate                  │
│ Enforce IRQ vs process vs atomic contexts in types     │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Gate 2: Unsafe Invariant Engineering Gate              │
│ Complete formal proofs: preconditions to destruction   │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Gate 3: C Semantic Reverse Engineering Gate            │
│ Reverse-engineer intrusive lists, refcounts, callbacks │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Gate 4: In-Place Initialization & Pinning Gate         │
│ Safe self-referential structures registered with C VFS │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│ Gate 5: Migration Architecture & Governance Gate       │
│ Dependency graphs, zero-regression proofs, RFC consensus│
└────────────────────────────────────────────────────────┘
```

---

### Gate 1: The Execution-Context Matrix Gate (Skills 26–40, 73)
*The core of kernel programming is knowing **where** code runs. Rust must enforce this.*

* **The Proof Task:** Given a C subsystem with 10 APIs, construct an **Execution-Context Matrix** (Process, IRQ, Softirq, May Sleep, Lock Required, RCU Required). Then, design a safe Rust API that makes it **compile-time impossible** to call a sleeping function from an IRQ context, or to access an RCU-protected pointer without an RCU guard.
* **Adversarial Failure Test:** The candidate exposes all C functions as standard methods on a struct, relying on doc comments to warn about execution context. The examiner calls a `mutex_lock` wrapper from inside a timer callback or spinlock critical section. If the code compiles and deadlocks the kernel at runtime, the candidate **FAILS**.

---

### Gate 2: Unsafe Invariant Engineering Gate (Skills 53–56, 76)
*The compiler checks the Rust code; the engineer must prove the `unsafe` assumptions.*

* **The Proof Task:** Write a safe Rust wrapper around a C function that returns a raw pointer to an object protected by a spinlock. Document the `SAFETY` comment not by repeating what the code does, but by proving:
  1. Why the pointer is valid.
  2. How the type system guarantees the spinlock remains held while the pointer is accessed.
  3. What happens if the C side invalidates or frees the object.
  4. Why the public safe API cannot trigger undefined behavior under any input.
* **Adversarial Failure Test:** The candidate writes `// SAFETY: Pointer returned by C API, assumed valid.` The examiner introduces an asynchronous C callback that frees the object under memory pressure. If a Use-After-Free is possible, the candidate **FAILS**.

---

### Gate 3: C Semantic Reverse Engineering Gate (Skills 41–49)
*`bindgen` generates syntax; the engineer must discover semantics.*

* **The Proof Task:** Analyze a complex C struct containing a `list_head`, a `refcount_t`, and a function pointer callback. Produce an ownership graph and lifetime graph. Design a Rust type that prevents the callback from executing after the object is freed, and prevents the list node from being detached while the lock is not held.
* **Adversarial Failure Test:** The candidate treats the C struct as a 1:1 memory layout and uses `bindgen` output directly, or uses standard Rust `Drop` without coordinating with the C-side `refcount_t` reaching zero asynchronously. If this results in double-free, callback-after-free, or list corruption, the candidate **FAILS**.

---

### Gate 4: In-Place Initialization & Pinning Gate (Skills 61–64)
*Kernel objects are registered with the C core, which retains raw pointers to their memory addresses.*

* **The Proof Task:** Implement a character device driver using `pin-init`. The device struct contains a `Mutex` and state registered with the C VFS. Prove that the struct is initialized in-place, never moves in memory, and is safely destroyed only after the C VFS releases all references.
* **Adversarial Failure Test:** The candidate attempts to use `Box::new()` or standard Rust move initialization, or implements `Drop` manually without synchronizing with the C-side `kref`/`refcount`. If the struct moves in memory or memory is reclaimed while `ioctl` is executing, the candidate **FAILS**.

---

### Gate 5: Migration Architecture & Governance Gate (Skills 94–100)
*Leadership requires knowing what **not** to rewrite, and how to sequence work upstream.*

* **The Proof Task:** Propose a comprehensive migration strategy for a major kernel component (e.g., Block Layer or Network device). Identify Migration Units, map the dependency graph (what Rust abstractions must merge first), provide an in-tree reference driver, and document a zero-downtime rollback strategy if benchmarks show regressions.
* **Adversarial Failure Test:** The candidate proposes a "ground-up rewrite" of the component in Rust, suggests bypassing the `kernel` crate to write raw FFI for performance, or ignores the C maintainer's concerns about review bandwidth. The patch is NACKed upstream; the candidate **FAILS**.

---

## Part 4: Role Qualification Threshold Matrix

To qualify for a specific role in the Rust-for-Linux project, an engineer must achieve the following minimum proficiency levels across all 8 domains:

| Competency Domain | Contributor (L2/L3 Focus) | Subsystem Rust Maintainer (L3/L4 Focus) | Migration Architect (L4/L5 Focus) |
| :--- | :---: | :---: | :---: |
| **Domain 1: Hardware & Architecture** | **L1** (Conceptual) | **L2** (Working knowledge of target ISA) | **L4** (Cross-ISA portability & weak ordering) |
| **Domain 2: Linux Core Internals** | **L2** (Uses VFS, Device, Memory APIs) | **L3** (Audits lifecycle, teardown, GFP flags) | **L5** (Defines core subsystem boundaries) |
| **Domain 3: Concurrency & LKMM** | **L2** (Uses `kernel::sync` correctly) | **L4** (Designs lockless / RCU abstractions) | **L5** (Resolves LKMM vs Rust model conflicts) |
| **Domain 4: C Semantics & FFI** | **L2** (Writes standard wrappers) | **L4** (Reverse-engineers implicit C contracts) | **L5** (Negotiates C API evolution for Rust) |
| **Domain 5: Kernel-Grade Rust** | **L3** (Audits `unsafe` blocks, no panics) | **L4** (Designs sound `pin-init` abstractions) | **L5** (Sets tree-wide `unsafe` and soundness policy) |
| **Domain 6: RFL `kernel` Crate** | **L2** (Extends existing module wrappers) | **L4** (Designs new core crate modules) | **L5** (Architects long-term crate evolution) |
| **Domain 7: Verification & Toolchain** | **L2** (Writes KUnit tests, checks CI) | **L3** (Integrates KASAN, lockdep, syzkaller) | **L5** (Designs toolchain policy & CI architecture) |
| **Domain 8: Governance & Strategy** | **L2** (Follows LKML etiquette & `b4`) | **L4** (Mentors contributors, reviews patches) | **L5** (Manages upstream politics, RFCs, & Linus) |

---

## Role Profile Summaries

### 1. The Contributor
* **Target Levels:** L2 across core engineering; L3 in at least one area (FFI, Rust, or Verification).
* **Scope of Authority:** Can safely extend drivers and subsystems using existing `kernel` crate abstractions.
* **Limitation:** Cannot introduce new `unsafe` abstractions to the core `kernel` crate without maintainer sponsorship.

### 2. The Subsystem Rust Maintainer
* **Target Levels:** L3/L4 across FFI, Rust, Concurrency, and Internals.
* **Scope of Authority:** Designs new safe abstractions in `kernel::`; audits `unsafe` blocks; reviews and merges patches for their subsystem; co-maintains with C maintainers.
* **Limitation:** Operates within subsystem boundaries; does not set tree-wide toolchain or governance policy.

### 3. The Migration Architect / Technical Lead
* **Target Levels:** L4/L5 across Governance, Concurrency, Toolchain, and System Internals.
* **Scope of Authority:** Selects migration candidates; structures migration units; designs cross-subsystem abstractions; defends the project against both ungrounded rewrites and anti-Rust obstructionism.
* **Ultimate Metric:** Successfully merges complex Rust abstractions into mainline Linux while maintaining 100% C ABI backward compatibility and zero performance regressions.

---

## The Ultimate Mindset Shift

To pass through these qualification gates, an engineer must internalize the deepest conceptual shift of Rust for Linux:

$$\mathbf{Implicit\ Human\ Knowledge\ (C)} \xrightarrow{\quad \text{Invariant Engineering} \quad} \mathbf{Compiler-Verified\ Truth\ (Rust)}$$

* **You are not writing Rust code that calls C.**
* **You are building a type-system bridge that translates implicit, human-enforced C conventions into explicit, mechanically enforced Rust invariants.**

If your Rust API requires the caller to read a documentation comment to avoid undefined behavior, the abstraction has failed. If your `unsafe` block relies on the C side "promising" to behave, the abstraction is unsound. 

The goal of the RFL engineer is to shrink the space of implicit human assumption and expand the space of verifiable truth—without breaking the 30-year-old, 30-million-line foundation of the Linux kernel.
