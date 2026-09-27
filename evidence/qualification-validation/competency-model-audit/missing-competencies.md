# Missing-Competency Attack (§12)

Question: what important Rust-for-Linux engineering capability could a candidate **lack while still passing C034, C047, and C053**? Each candidate omission is classified per the frozen rule: OUT_OF_SCOPE / COVERED_ELSEWHERE / REQUIRED_BUT_MISSING / OPTIONAL-SPECIALIZED / OPEN. No competency is added in this audit.

| Dimension | Could pass all three while lacking it? | Classification | Rationale |
|---|---|---|---|
| Publication semantics (memory ordering/visibility of a newly initialized/published object) | YES — no behavior requires reasoning about release/acquire at publication | **REQUIRED_BUT_MISSING** (CM-014, C053) | Publication is constitutive of "correct construction and publication of immovable kernel objects"; Pin provides no visibility guarantees (S1) |
| Release/last-put callback execution context (kref/kobject release runs in arbitrary context; must not sleep/block on self) | YES | **REQUIRED_BUT_MISSING** (CM-011, C047) | Standard teardown pattern; failure class is frequent and subtle |
| Execution-context discipline beyond negative sleep gate (atomic vs sleepable contexts; PREEMPT_RT threadirqs effects) | PARTIALLY — gates punish violations negatively | PARTIALLY COVERED; residual classified **OPEN** (CM-001 interplay) | Positive context-selection skill is untested; PREEMPT_RT regime changes legality (S2/S3) |
| Memory ordering / LKMM as first-class skill (acquire/release/barrier selection) | PARTIALLY — C034 L4 audits ordering adversarially | PARTIALLY COVERED (within-scope); standalone depth **OPTIONAL/SPECIALIZED** | LKMM depth beyond these competencies is real but out of the frozen 3-competency scope |
| Lock design / lock ordering (positive design skill) | YES — deadlock gate is negative-only | **OPTIONAL/SPECIALIZED** | Negative gate catches cycles in assessed artifacts; positive lock-architecture design is a distinct skill |
| IRQ/NMI constraints | NMI excluded by scope; IRQ partial via C047 mechanisms | **OUT_OF_SCOPE** (consistent with frozen exclusions) | Scope statement forbids claiming this; correctly excluded rather than missing |
| Allocation constraints (GFP contexts, atomic allocations) | YES (only allocator-lifetime audit at C053 L4) | **OPTIONAL/SPECIALIZED** (within these competencies) | Real RfL skill; would be its own competency |
| DMA/coherency | excluded | **OUT_OF_SCOPE** | Frozen exclusions (arm64/dma) — consistent |
| Error-path design beyond init unwind (downstream call error handling) | PARTIALLY — C053 L4 covers init unwind only | PARTIALLY COVERED | Broader error-path engineering is a distinct competency |
| Cancellation/shutdown races | NO — C047 L4 is precisely this | COVERED_ELSEWHERE (C047) | — |
| Reference counting as explicit design skill | PARTIALLY — C047 L2 wrapper | PARTIALLY COVERED | Deep refcount design (kref conventions, debug validation) is broader |
| ABI compatibility design | PARTIALLY — required_abi_break gate (negative); C053 L5 mentions ABI boundaries | PARTIALLY COVERED | Positive ABI design mostly at the (currently OPEN) L5 boundary |
| Kernel-configuration sensitivity (CONFIG_ variants changing semantics) | YES — CM-001 is an instance | **REQUIRED_BUT_MISSING as an explicit skill**; currently an implicit hazard | The model's own scope (PREEMPT_RT) proves configurations change semantics; no behavior tests noticing this |
| Architecture sensitivity | excluded | **OUT_OF_SCOPE** | Frozen x86_64 scope |
| Debugging/diagnostic reasoning (locating real defects from logs/crashes) | YES | **OPTIONAL/SPECIALIZED** | Valuable; distinct assessment format needed |
| Transfer/generalization across subsystems | YES (Profile H) | **OPEN** (CM-017) | Alpha scope limitation; must be stated in scope, not silently assumed |

## Summary

Two within-scope **REQUIRED_BUT_MISSING** omissions materially affect construct completeness (publication semantics; release-callback context), one systemic gap is now demonstrated by the model's own scope choice (configuration sensitivity), and the remainder are either correctly excluded by the frozen scope or optional specializations. Per §12/§19 these are recorded as recommendations for the next instrument freeze: `ADD_MISSING_BEHAVIOR` (publication, release-context) is recommended but **not executed** — the audit does not modify frozen competency files.
