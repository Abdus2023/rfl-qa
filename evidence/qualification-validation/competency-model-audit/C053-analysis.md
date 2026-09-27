# C053 — Pin Initialization: Validity Audit

Construct under audit: "Scoped in-place initialization behavior" (domain `initialization`), behaviors CB-053-01…05, oracle OR-PIN, scope x86_64/CONFIG_RUST=y/PREEMPT_RT=y.

## 1. Definition

What "pin initialization" means in the RfL context (S1/S5): constructing an object **in place** at its final address so that address-stability guarantees (Pin, `Opaque` FFI representations, self-referential/kernel-registered structures) hold from first publication; `kernel::init` provides `PinInit`/`Init` in-place constructors with `pin_init!`/`try_pin_init!`/`stack_pin_init!` — merged kernel-crate API (S5), with the machinery now a separate crate under active upstream sync (S7).

- Scope: the construct mixes three layers: (a) Rust-generic pin/borrow semantics (L1–L2), (b) RfL in-place-initialization machinery (L3), (c) kernel object lifecycle engineering (L4–L5). Layering is intentional prerequisite structure, but the title ("Pin Initialization") over-signals layer (b/c) relative to layer (a) — the competency measures an **accidental mixture** unless assessors treat L1/L2 as prerequisite evidence (CM-013). Verdict: CORRECT-but-layered; boundary clarification required.
- Distinct constructs not conflated: initialization is kept separate from teardown (C047) and concurrency (C034), except where lifecycle composition is intended (cross-competency-analysis.md).

## 2. Existence audit

| Behavior | Claim | Reality check (S1/S5) | Class | verdict |
|---|---|---|---|---|
| CB-053-01 | Identify address-change failure in self-referential C structure | Real and foundational: address instability invalidates embedded self-pointers — the entire reason for pinning | REAL AND CENTRAL | SUPPORTED technically; construct = Rust/C-generic prerequisite (CM-013) |
| CB-053-02 | In-place field init + compile-fail use-after-borrow demonstration | Real: move-after-borrow is rejected by rustc (E0505-class); a supplied compile-fail artifact is directly checkable | REAL AND CENTRAL | SUPPORTED both; best observability in the model |
| CB-053-03 | Single init + pinned lifetime in a safe API with teardown model | Real: in-place constructors + pinned lifetime encoding is exactly what kernel::init exists for; "safe API" here means Rust-level safety CONTRACT, which must not be read as kernel-invariant proof | REAL AND CENTRAL | SUPPORTED; ASSESSOR_AMBIGUITY on "safe" (CM-013b) |
| CB-053-04 | Audit partial-initialization unwind paths + allocator lifetime assumptions under adversarial teardown | Real and deep: fallible in-place init with already-initialized fields on error paths, allocator contracts as external dependencies (D01) — a genuine expert discriminator | REAL BUT SPECIALIZED | SUPPORTED both |
| CB-053-05 | Reviewed reusable subsystem initialization policy with explicit ABI boundaries | Real activity; review infrastructure dependency | REAL BUT SPECIALIZED | TECHNICAL SUPPORTED; CONSTRUCT PROVISIONAL (CM-015) |

Required attacks:
- `Pin<T> = fully initialized kernel object`: **false** — pinning constrains movement; it says nothing about initialization state, memory visibility, or kernel invariants. The matrix does not assert the equivalence (CB-053-03 requires a teardown model — i.e., more than Pin). Verdict: model avoids the naive equivalence; assessor guidance should say so explicitly.
- `!Unpin = safe publication`: **false** — `!Unpin` constrains moves only; cross-CPU publication requires synchronization/memory ordering, which Pin does not provide (S1). Finding: the matrix contains **no publication-semantics behavior** (CM-014) — for a construct about "correct construction and publication of immovable kernel objects," publication is missing; the construct as written is mostly construction.

## 3. Construction audit

- CB-053-01/02: DIRECTLY_OBSERVABLE (trace + compile-fail artifact; independently re-checkable by re-running rustc — the only behavior in the catalog whose evidence is machine-recheckable).
- CB-053-03: OBSERVABLE_WITH_INSTRUMENTATION; "safe API" ambiguity must be resolved by rubric guidance (contract-level safety vs kernel invariant).
- CB-053-04: INFERENTIAL (audit quality); confounder: Rust init-machinery familiarity (S7 — API churn) vs genuine lifecycle reasoning; assessors must score the reasoning (unwind ordering, allocator dependency statement), not macro fluency (CM-020).
- CB-053-05: DIFFICULT_TO_OBSERVE under current protocol (CM-015).

## 4. Version stability (CM-020)

Durable principles (stable): address stability before publication; in-place fallible initialization; allocator contracts as external assumptions; init-before-use ordering. Implementation surfaces (moving): macro spellings, crate split (`pin-init` separate crate, upstream-sync patch series mid-2026, S5/S7). The behaviors are phrased at the durable-principle level (good), but example artifacts and assessor training must be re-anchored per instrument freeze when the API moves.

**C053 disposition: PARTIALLY_SUPPORTED → RETAIN_WITH_BOUNDARY_CLARIFICATION** with one **ADD_MISSING_BEHAVIOR recommendation (publication semantics) deferred to the next instrument freeze** (not executed now, per audit-first mandate). 
