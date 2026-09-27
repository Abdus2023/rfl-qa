# Rust-for-Linux Engineering Capability & Verification Analysis (2026)

> Deep analysis, verification, and capability model for contributing to and leading Rust integration and migration in the Linux kernel.

---

## Part I — Initial Assessment: The Engineering Challenge & Skill Framework

To deeply analyze and verify the skills required to contribute to or lead the effort of integrating and migrating the Linux Kernel to Rust (primarily through the **Rust for Linux (RFL)** project), we must discard the notion of a "ground-up rewrite." The Linux kernel is a 30-year-old, 30+ million line C codebase. The actual effort is an **incremental migration**, requiring the creation of safe Rust abstractions over existing C code, and eventually rewriting core subsystems.

Therefore, the required skill set is a highly specialized intersection of **OS theory, advanced C, bleeding-edge Rust, and kernel-specific tooling**.

Below is a deeply analyzed, categorized, and verified list of skills required for this monumental engineering task.

---

### Phase 1: Foundational Systems & OS Architecture
*You cannot write kernel code in any language if you do not understand the hardware and OS theory. Rust's safety guarantees do not replace the need for systems knowledge.*

* **Hardware/Software Interface:** Deep understanding of CPU architectures (x86_64, ARM64, RISC-V), Memory Management Units (MMU), Page Tables, Interrupt Controllers (APIC/GIC), DMA (Direct Memory Access), and bus architectures (PCIe, USB).
* **Concurrency & Memory Models:** Mastery of lockless programming, atomic operations, memory barriers, and cache coherency.
  * *Kernel Specific:* Deep understanding of **RCU (Read-Copy-Update)**, per-CPU data, and bottom-half/top-half interrupt handling.
* **Memory Management:** Physical vs. Virtual memory, slab/slub allocators, NUMA architectures, and the kernel's buddy allocator.
* **Boot & Initialization:** Understanding the boot sequence (BIOS/UEFI -> Bootloader -> Kernel Entry -> Early Init -> Subsystem Init).

### Phase 2: Advanced "Kernel-Grade" Rust
*Standard Rust development (web, CLI, async apps) uses almost none of the skills required for the kernel. Kernel Rust is essentially `no_std` systems programming.*

* **`unsafe` Rust Mastery:** The kernel is inherently unsafe (talking to hardware, raw pointers). You must know how to write bulletproof `unsafe` blocks, ensuring all safety invariants are documented and enforced.
* **`no_std` Environment:** Writing Rust without the standard library. This requires implementing custom panic handlers, allocators (using the kernel's `kmalloc`), and understanding compiler intrinsics.
* **Pinning & Self-Referential Structs:** **This is the hardest Rust concept for kernel devs.** Kernel data structures (like file operations or device drivers) are often registered with the C kernel, which holds a raw pointer to them. Rust's `Pin` API must be used to guarantee these structures are never moved in memory, preventing use-after-free or memory corruption.
* **Advanced Trait System & Macros:** Heavy use of declarative (`macro_rules!`) and procedural macros to generate boilerplate (e.g., generating C-compatible vtables, module initialization code).
* **Zero-Cost Abstractions:** Understanding how Rust compiles down to assembly. You must be able to read `cargo expand` and LLVM IR to ensure abstractions do not introduce hidden allocations or performance regressions.

### Phase 3: C Interoperability (FFI) & Translation
*The bridge between the 95% C kernel and the 5% Rust kernel is the most critical battleground.*

* **C ABI & Calling Conventions:** Deep knowledge of `extern "C"`, struct layout, padding, alignment, bitfields, and variadic functions.
* **Reading & Auditing C Code:** You must be able to read complex, macro-heavy C code, identify implicit contracts (e.g., "this function must be called with `spin_lock` held"), and translate those contracts into Rust's type system.
* **Error Code Translation:** Mapping the kernel's C-style error handling (negative integers, `ERR_PTR`, `IS_ERR`) to Rust's `Result<T, kernel::error::Error>`.
* **Bindgen & Tooling:** Using `bindgen` to auto-generate Rust FFI bindings from C headers, and knowing how to manually wrap those raw bindings into safe, idiomatic Rust APIs.

### Phase 4: Rust for Linux (RFL) Specific Abstractions
*You must understand the specific architecture of the RFL project, which lives in the `rust/` directory of the kernel tree.*

* **The `kernel` Crate:** Mastery of the internal `kernel` crate, which provides the safe abstractions. You must know how to extend it (e.g., adding a safe wrapper for a new C subsystem like the Block Layer or Networking).
* **Kernel Synchronization Primitives:** Implementing Rust wrappers for kernel primitives: `Mutex`, `SpinLock`, `RwLock`, and `Refcount`. You must ensure these wrappers correctly integrate with the kernel's lockdep (lock dependency validator) for deadlock detection.
* **Device Driver Model:** Writing character devices, platform drivers, and PCI drivers using the Rust abstractions (`kernel::driver`, `kernel::file_operations`).
* **Thread & Task Management:** Wrapping the kernel's `task_struct` and workqueues into safe Rust threads/tasks, ensuring correct lifetime management when a kernel thread is killed.

### Phase 5: Verification, Testing, and Debugging
*In the kernel, a bug means a system panic, data corruption, or a security vulnerability. "It compiles" is not enough.*

* **Kernel Debugging:** Proficiency with QEMU, GDB, KGDB, ftrace, and eBPF to trace execution and inspect memory.
* **KUnit & kselftest:** Writing unit tests using the kernel's KUnit framework (which has Rust bindings) and integration tests via kselftest.
* **Panic-Free Programming:** In user-space Rust, a panic is a caught exception. In the kernel, a panic kills the machine. You must master patterns that guarantee code is **panic-free** (e.g., avoiding `unwrap()`, using `expect` with rigorous proof, or returning `Result`).
* **Formal Methods & Fuzzing:** Using tools like `cargo-fuzz` adapted for the kernel, and understanding how Rust's borrow checker acts as a compile-time formal proof against Use-After-Free (UAF) and Double-Free bugs.

### Phase 6: Community, Process, and Governance
*The Linux Kernel community is notoriously strict. The tool you use matters less than how you interact with the maintainers.*

* **LKML Etiquette:** Mastery of `git send-email`, plain-text email formatting, patch threading, and responding to code reviews.
* **Subsystem Maintainer Hierarchy:** Understanding that you don't submit to "Linus"; you submit to the subsystem maintainer (e.g., Networking, Block, Drivers).
* **Rust for Linux RFC Process:** The RFL project has a strict process for accepting new abstractions. You must be able to write detailed RFCs proving why a C API should be wrapped in Rust, and how the safety invariants are maintained.

---

### Verification & Reality Check: The "Rewrite" Myth

If you are planning a team or personal journey into this space, it is vital to verify the current reality of the project (as of 2026):

1. **It is NOT a rewrite from scratch:** No one is rewriting the Linux kernel in Rust from day one. The effort is **incremental**. You write a Rust driver, then a Rust filesystem, then you rewrite the C implementation of a subsystem in Rust while maintaining C compatibility.
2. **The "Impedance Mismatch":** The biggest technical hurdle is not Rust; it is mapping C's implicit, global-state-heavy paradigms (like global linked lists of devices) into Rust's strict, localized ownership model.
3. **The RCU Problem:** Read-Copy-Update (RCU) is the backbone of Linux kernel scalability. Expressing RCU safely in Rust's borrow checker is currently one of the most active and difficult areas of research in the RFL project.
4. **Assembly is still required:** Rust does not eliminate the need for architecture-specific assembly. Boot code, context switching, and low-level interrupt handling will remain in C/Assembly for the foreseeable future.

### Recommended Learning Path for Verification
If you want to verify your readiness for this task, attempt the following progression:
1. **Write a `no_std` Rust program** that runs on bare metal (e.g., using the `cortex-m-rt` or `x86_64` crate) and prints to a UART serial port.
2. **Read the Rust for Linux source tree.** Specifically, study `rust/kernel/sync.rs` to see how they solved the Mutex/SpinLock wrapping problem.
3. **Write a simple Kernel Module in Rust.** Use the RFL toolchain to write a basic character device driver that allocates memory, handles a user-space `ioctl`, and safely frees the memory without panicking.
4. **Submit a patch to LKML.** Find a missing abstraction in the `rust/kernel/` tree, write it, prove its safety, and submit it via `git send-email` to the Rust for Linux mailing list.

---

## Part II — Critical Verification & 2026 Reality Assessment

The framework above is directionally correct, but several statements are now outdated or too strong for the **September 2026** state of Rust for Linux. The biggest correction is conceptual:

> **The engineering problem is not "rewrite Linux in Rust." It is building a maintainable mixed-language kernel in which Rust can safely own increasingly important pieces without weakening Linux's existing C interfaces, memory model, performance model, or subsystem governance.**

Current Linux/Rust-for-Linux documentation and kernel Rust API documentation substantiate this assessment:

* Reference: [Kernel Documentation](https://docs.kernel.org/rust/)
* Reference: [General Information](https://cdn.kernel.org/doc/html/latest/rust/general-information.html)
* Reference: [Rust Kernel API Docs](https://rust.docs.kernel.org/)
* Reference: [RCU Module Docs](https://rust.docs.kernel.org/kernel/sync/rcu/index.html)
* Reference: [Sync Module Docs](https://rust.docs.kernel.org/kernel/sync/index.html)
* Reference: [Rust Reference Drivers](https://rust-for-linux.com/rust-reference-drivers)
* Reference: [Contributing Guide](https://rust-for-linux.com/contributing)
* Reference: [Arc in the Linux Kernel](https://rust-for-linux.com/arc-in-the-linux-kernel)
* Reference: [Unstable Features](https://rust-for-linux.com/unstable-features)
* Reference: [Rust Version Policy](https://rust-for-linux.com/rust-version-policy)
* Reference: [Rust Kernel Policy](https://rust-for-linux.com/rust-kernel-policy)
* Reference: [Quick Start Guide](https://cdn.kernel.org/doc/html/latest/rust/quick-start.html)

---

### 1. Verification of the Major Claims

| Claim | Assessment | Correction / Context |
| :--- | :--- | :--- |
| **Linux is not being rewritten from scratch** | **VERIFIED** | Correct. Rust is integrated incrementally into the existing kernel. |
| **C/Rust FFI is central** | **VERIFIED** | This is one of the fundamental engineering boundaries. |
| **`no_std` is required** | **VERIFIED** | Kernel Rust links against `core`, not `std`. |
| **Advanced `unsafe` Rust is required** | **VERIFIED** | Especially for kernel abstractions and FFI boundaries. |
| **Rust abstractions should precede bypassing them** | **VERIFIED** | Current kernel documentation explicitly says to wrap/port an unavailable C API rather than bypass the `kernel` crate. |
| **Pinning is central** | **PARTIALLY VERIFIED** | Pinning/in-place initialization is important, but calling it *the* hardest Rust concept is subjective and misleading. |
| **RCU is an unsolved Rust problem** | **OUTDATED** | RFL now has an `rcu` API including guards, `read_lock`, `synchronize_rcu`, and `rcu_barrier`. |
| **Rust must understand Linux's memory model** | **STRONGLY VERIFIED** | This is actually more important than generic Rust knowledge. |
| **Lockdep integration matters** | **VERIFIED** | Kernel synchronization abstractions have to preserve Linux synchronization semantics, not merely provide Rust-looking locks. |
| **Rust drivers are an important entry point** | **VERIFIED** | Reference drivers explicitly exist to bootstrap abstractions and provide living examples. |
| **`cargo-fuzz` is a normal kernel verification mechanism** | **MISLEADING** | Kernel fuzzing is important, but the kernel ecosystem's relevant tools include KUnit, kselftest, KASAN, KMSAN, UBSAN, KFENCE, syzkaller, lockdep, etc. |
| **Rust borrow checking is a formal proof of absence of UAF/double-free** | **TOO STRONG** | Rust proves properties of the Rust abstraction under its assumptions. It does not prove the C side, FFI contracts, hardware behavior, unsafe blocks, or entire kernel subsystem correct. |
| **Assembly remains necessary** | **VERIFIED** | Rust does not eliminate architecture-specific kernel implementation. |
| **Rust can eventually replace major C subsystems** | **POSSIBLE, NOT THE CORE PREMISE** | It should not be presented as an established migration roadmap. The current project is about enabling Rust where it makes sense, subsystem by subsystem. |
| **Every Rust patch needs subsystem + Rust review** | **VERIFIED** | RFL explicitly states that Rust patches should go to both the relevant subsystem and Rust maintainers/reviewers. |

The most important correction is therefore **RCU**. Current Rust kernel documentation exposes an actual RCU abstraction rather than treating RCU as something Rust cannot express.

---

### 2. The Real Skill Model: Nine Capability Domains

Restructuring the six phases into **nine capability domains**:

```
                    RUST-FOR-LINUX ENGINEER
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
    Hardware               Linux internals       Rust semantics
        │                      │                      │
        ├─ MMU                 ├─ VFS               ├─ ownership
        ├─ DMA                 ├─ scheduler         ├─ lifetimes
        ├─ interrupts          ├─ networking        ├─ unsafe
        ├─ PCI/USB             ├─ memory mgmt       ├─ pin-init
        └─ architecture        ├─ locking           ├─ traits/macros
                               └─ RCU               └─ FFI
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                        Mixed-language design
                               │
                  ┌────────────┴────────────┐
                  │                         │
              Verification              Integration
                  │                         │
         KUnit / kselftest             Kbuild
         KASAN / UBSAN                 clang/LLVM
         syzkaller                     bindgen
         lockdep                       rustc
         QEMU/GDB                      CI
                  │                         │
                  └────────────┬────────────┘
                               │
                          Kernel process
                               │
                     patch / review / merge
```

This is a better model than simply saying "advanced Rust + C + OS."

---

### 3. Domain I — Linux Kernel Internals

This is probably the **largest missing emphasis** in typical developer models. A person can be an excellent Rust programmer and still be completely unqualified to design a Rust kernel abstraction.

#### Core Kernel Concepts
* `task_struct`
* credentials
* namespaces
* capabilities
* scheduling
* interrupts
* softirqs
* workqueues
* wait queues
* completions
* timers
* reference counting
* locking
* RCU
* per-CPU state
* memory allocation
* GFP flags
* page allocation
* slab/slub
* virtual memory
* DMA
* device model
* sysfs
* kobjects
* VFS
* file descriptors
* poll/epoll
* kernel/user boundary
* `copy_to_user()` / `copy_from_user()`
* error-pointer conventions
* lifetime rules

The critical skill isn't memorizing APIs. It's being able to answer:

> **What invariant does this C API assume that the compiler cannot see?**

That is the actual bridge to Rust.

---

### 4. Domain II — Linux Kernel Memory Model (LKMM)

Elevated to its own category: generic Rust concurrency knowledge is insufficient. A serious RFL contributor needs to understand the **Linux Kernel Memory Model (LKMM)** and how Linux's atomics, barriers, and synchronization interact with compiler and CPU ordering.

This becomes particularly important because RFL explicitly does **not simply substitute standard Rust synchronization primitives for kernel primitives**.

For example, RFL's custom `Arc` exists partly because Linux uses `refcount_t` and the LKMM rather than simply adopting Rust's standard `Arc`/atomic semantics.

The mental model must be:

```
Rust memory model
  + LLVM memory model
  + CPU memory ordering
  + Linux Kernel Memory Model
  + specific Linux synchronization primitive
```

That is substantially harder than "know atomics."

---

### 5. Domain III — Rust at the Abstraction Boundary

Unsafe Rust must be split into two distinct concerns:

#### A. Local Unsafe
Understanding `unsafe { ... }` is not enough. You need to construct an argument of the form:

```
unsafe operation
  ↓ required preconditions
  ↓ who establishes them?
  ↓ how are they preserved?
  ↓ what happens if the C side violates them?
  ↓ why is the public safe API still sound?
```

This is **unsafe-code invariant engineering**.

#### B. Kernel-Specific Rust
Important topics include:
* `no_std`
* lifetimes
* ownership
* variance
* `Send` / `Sync`
* interior mutability
* atomics
* trait objects
* dynamically sized types
* associated types
* generic bounds
* macro systems
* procedural macros
* `repr(C)`
* raw pointers
* FFI
* `MaybeUninit`
* initialization invariants
* pinning
* in-place initialization
* drop semantics
* custom allocators
* kernel-specific reference counting

The project also has a dedicated **pin-init** subproject, which is a stronger indication of the actual architectural importance of initialization/lifetime invariants than simply saying "learn `Pin`."

---

### 6. Pinning: A More Precise Explanation

The statement *"Pin API must be used to guarantee these structures are never moved"* captures an important problem but oversimplifies the solution. The actual problem is broader:

```
C kernel
  │
  │ stores pointer
  ▼
Rust object
  │
  ├── must be initialized correctly
  ├── must remain at required address
  ├── must outlive every external reference
  ├── must be destroyed at correct time
  └── must not expose invalid intermediate state
```

Therefore:

```
Pinning
  + in-place initialization
  + ownership
  + lifetime tracking
  + drop/destruction protocol
  + FFI invariant
```

is the real skill. This is why **pin-init** is architecturally significant.

---

### 7. Domain IV — C Is Not Merely an FFI Language

An RFL engineer needs to be able to **reason in C**, not merely call C.

For example:

```c
struct foo {
    struct list_head node;
    spinlock_t lock;
    struct refcount_t refs;
    /* ... */
};
```

The Rust engineer must discover:
* Who owns `foo`?
* Who owns `node`?
* Can `node` be detached concurrently?
* Who holds `lock`?
* Can `refs` reach zero under the lock?
* Can a callback execute after destruction?
* Does list membership imply a lifetime?
* Which CPU can access it?
* Can IRQ context access it?
* Can process context sleep?

None of those properties necessarily appear in the C type. That is precisely what Rust must eventually encode.

So: **C semantic reverse engineering** is a first-class skill.

---

### 8. Domain V — `bindgen` Is Not the Abstraction

This distinction is crucial. A naive migration looks like:

```
C header ──► bindgen ──► Rust
```

A production-quality migration is closer to:

```
C API
  │
  ├── ABI
  ├── lifetime contract
  ├── locking contract
  ├── context restrictions
  ├── ownership contract
  ├── error contract
  ├── concurrency contract
  └── initialization contract
          ↓
      FFI layer
          ↓
  safe Rust abstraction
          ↓
     Rust users
```

`bindgen` can generate the **syntax-level interface**. It cannot discover the entire semantic contract. That is one of the central skills for RFL.

---

### 9. Domain VI — RFL `kernel` Crate Architecture

Core competence, not merely project-specific knowledge. Current documentation describes the `kernel` crate as the shared layer containing APIs ported or wrapped for Rust code in the kernel. The documentation explicitly instructs developers to add a wrapper when an API isn't available rather than bypassing the crate.

Conceptually:

```
             Rust driver/module
                     │
                     ▼
              kernel:: abstraction
                     │
           ┌─────────┴─────────┐
           ▼                   ▼
        safe API            invariants
           │                   │
           ▼                   ▼
        FFI layer           safety proof
           │
           ▼
        Linux C API
           │
           ▼
       kernel internals
```

The ability to design this middle layer is probably the single most important **RFL-specific engineering skill**.

---

### 10. Domain VII — Verification Needs to Be Broader

Replace: *"Rust prevents UAF/double free"* with:

> **Rust eliminates classes of memory-safety bugs inside sound Rust abstractions, while kernel correctness still depends on unsafe Rust, C code, FFI contracts, concurrency semantics, hardware behavior and subsystem invariants.**

This distinction is essential. The assurance stack:

```
                 Kernel correctness
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    Rust type        unsafe-code       C/assembly
     system          invariants        correctness
        │                │                │
        └────────────────┼────────────────┘
                         │
                   FFI contracts
                         │
                    concurrency
                         │
                     hardware
```

No single layer proves the whole stack.

---

### 11. Verification Toolchain

A serious engineer should know approximately this landscape:

| Area | Tools / Mechanisms |
| :--- | :--- |
| **Build** | Kbuild, LLVM/Clang, GCC, rustc |
| **Rust analysis** | rustc, rustdoc, rustfmt, Clippy where applicable |
| **FFI** | bindgen |
| **Unit testing** | KUnit |
| **Integration** | kselftest |
| **Kernel fuzzing** | syzkaller |
| **Memory bugs** | KASAN, KFENCE, KMSAN |
| **Undefined behavior** | UBSAN |
| **Locking** | lockdep |
| **Dynamic tracing** | ftrace |
| **BPF tracing** | eBPF |
| **Debugging** | GDB, KGDB |
| **Virtual hardware** | QEMU |
| **Static analysis** | sparse, Smatch, Coccinelle and related tooling |
| **Rust-specific transformation** | Coccinelle for Rust |
| **CI** | kernel/Rust/build/test infrastructure |

The official kernel Rust documentation has dedicated sections for quick start, architecture support, coding guidelines, and testing.

---

### 12. Domain VIII — Toolchain Engineering Is Unusually Important

RFL is not ordinary Cargo development. The kernel currently uses Rust 2021 plus some unstable features. The project explicitly tracks those unstable features and is working toward reducing/removing their use.

As of current project policy, Linux v7.1 uses Rust **1.85.0 as its minimum**, following Debian 13's toolchain policy.

The engineer therefore needs to understand:

```
Kbuild
  ↓
rustc
  ↓
LLVM
  ↓
bindgen / libclang
  ↓
generated bindings
  ↓
kernel crate
  ↓
Rust modules
```

A compiler/toolchain change can itself become a kernel integration problem. The official Quick Start documents kernel-specific LLVM/Rust toolchains and `rust-analyzer` integration rather than treating this as an ordinary Cargo project.

---

### 13. Domain IX — Kernel Governance

There isn't one monolithic "RFL development process." Current Rust-for-Linux policy explicitly says that **each subsystem decides how it wants to integrate Rust**. Some want to develop Rust themselves; some want Rust co-maintainers/sub-maintainers; some currently don't want Rust.

Therefore:

```
Linux kernel governance
  │
  ├── subsystem maintainer
  ├── Rust subsystem
  ├── relevant reviewers
  ├── architecture maintainers
  └── mailing lists / CI
```

is more accurate than `RFL → Linus`. Contribution guidance specifically says Rust patches should go to both the relevant subsystem and Rust reviewers/maintainers.

---

### 14. Subsystem Engineering: Architecture for Leads

For someone intending to **lead** rather than merely contribute:

> **Bad question:** *"Which Linux subsystem should we rewrite in Rust?"*  
> **Better question:** *"Which subsystem has a sufficiently bounded semantic boundary, sufficient Rust abstractions, maintainers willing to review it, measurable safety benefit, and a credible incremental migration path?"*

This changes the entire engineering strategy.

The project explicitly uses **Rust reference drivers** to solve the problem where an abstraction needs a real in-tree user before it can be merged, while a duplicate driver is undesirable. That's a governance/architecture constraint that a purely technical migration plan can easily miss.

---

### 15. What "Lead Engineer" Actually Requires: Three Levels

#### Contributor
```
understand subsystem ──► modify existing Rust ──► write safe abstraction ──► test ──► debug ──► submit patch
```

#### Subsystem Rust Maintainer
* Design abstraction API
* Review unsafe invariants
* Understand C/Rust interaction
* Negotiate API with subsystem maintainers
* Maintain long-term compatibility
* Review other contributors

#### Migration Architect / Technical Lead
```
                    migration architecture
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
       technical          governance         economics
           │                  │                  │
        safety            maintainer         manpower
        ABI               bandwidth          schedule
        performance       review load        testing
        memory model      ownership          maintenance
        tooling           upstreamability    support
```

At that level, **Rust expertise alone becomes a relatively small fraction of the job**.

---

### 16. The Calibrated Readiness Ladder

```
L0   Rust fundamentals
  ↓
L1   unsafe Rust + no_std
  ↓
L2   bare-metal / architecture
  ↓
L3   Linux kernel C development
  ↓
L4   kernel concurrency + LKMM + RCU
  ↓
L5   C/Rust FFI
  ↓
L6   RFL kernel abstractions
  ↓
L7   Rust kernel driver
  ↓
L8   abstraction contribution
  ↓
L9   subsystem-level contribution
  ↓
L10  subsystem Rust maintainer
  ↓
L11  cross-subsystem migration architect
```

**L3–L5 cannot be skipped.**

* `Rust → Rust kernel module` (skipping L3–L5): developer only learns to call existing APIs.
* `Rust → unsafe/no_std → Linux C → LKMM/RCU/locking → FFI → RFL`: developer can actually design sound abstractions.

---

### 17. Practical Verification Projects (Adversarial Progression)

* **Project A — Bare metal:**  
  `Rust no_std` → interrupt handling → UART driver → minimal allocator → explicit panic behavior.
* **Project B — C kernel module:**  
  Implement the same conceptual device in C. Learn: `file_operations`, `ioctl`, `copy_from_user`, `copy_to_user`, locking, lifetime, `refcount`, module unload.
* **Project C — Rust equivalent:**  
  Implement it using existing RFL APIs. Verify: module load, concurrent access, module unload, error paths, allocation failure, invalid user-space input, race testing under KASAN and lockdep.
* **Project D — Abstraction engineering:**  
  Find a missing abstraction required by the driver. Implement: C contract → FFI bindings → safe wrapper → Rust user → KUnit tests.
* **Project E — Adversarial review gate:**  
  For every `unsafe` block, produce an explicit proof artifact:
  * `SAFETY INVARIANT`
  * `PRECONDITIONS`
  * `ESTABLISHMENT`
  * `MAINTENANCE`
  * `INVALIDATION`
  * `DESTRUCTION`
  * `CONCURRENT ACCESS`
  * `FFI ASSUMPTIONS`
  * `TEST EVIDENCE`

---

### 18. The Deepest Conceptual Shift

The most important skill isn't "knowing Rust." It is **transforming an implicit C invariant into an explicit, mechanically enforced interface**.

```
C world
  struct object *
    + "must hold lock"
    + "must remain alive"
    + "callback may run asynchronously"
    + "cannot sleep here"
    + "RCU read-side protection required"
```

becomes:

```
Rust world
  Object
    ├── lifetime
    ├── ownership
    ├── lock guard
    ├── RCU guard
    ├── context restriction
    └── callback registration
```

The abstraction isn't merely wrapping a C function. It is **encoding the C semantic contract into a Rust interface**. That is the heart of Rust-for-Linux.

---

### Final Summary: The 2026 Competency Model

The original list is roughly **85% structurally right**, but it mixes three different things:

1. **General kernel engineering**
2. **Advanced Rust**
3. **Current RFL project status**

The third category changes quickly and needs continuous verification.

> **Rust for Linux is an incremental mixed-language kernel engineering project whose central technical challenge is constructing sound Rust abstractions over Linux's existing C, concurrency, memory-management, device, and ABI contracts.**

The strongest skills aren't simply `Rust + C + OS`, but:

```
Linux internals
  + LKMM / concurrency / RCU
  + unsafe Rust
  + FFI semantics
  + initialization / lifetime design (pin-init)
  + kernel abstraction design
  + verification (KUnit, lockdep, KASAN, syzkaller)
  + Kbuild / toolchain engineering
  + subsystem architecture
  + upstream governance
```

**RCU should no longer be described simply as "the RCU problem" or as something RFL currently cannot express.** The Rust kernel API now has an explicit RCU module and primitives; the engineering challenge has shifted toward making those abstractions sufficiently expressive, sound, performant, and usable across real kernel subsystems.

The official Rust kernel API exposes synchronization facilities including mutexes, spinlocks, atomics, barriers, completions, and SRCU, while the `kernel` crate serves as the common abstraction layer.

This is the calibrated **2026 competency model** for someone aiming not merely to write a Rust driver, but eventually to **lead serious Rust adoption inside Linux**.
