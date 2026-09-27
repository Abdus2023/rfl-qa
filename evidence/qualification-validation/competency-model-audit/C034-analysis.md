# C034 — RCU Grace Periods: Validity Audit

Construct under audit: "Scoped RCU grace-period behavior" (domain string: `concurrency_lkmm`), behaviors CB-034-01…05, oracle OR-RCU, scope x86_64/CONFIG_RUST=y/PREEMPT_RT=y, exclusions arm64/dma/nmi.

## 1. Definition

What is measured: the ability to reason about read-side protection, grace periods, and deferred reclamation ordering in a kernel concurrency setting — plus (L3–L4) designing guards/order models and auditing memory-ordering claims without over-trusting dynamic tools.

- Scope verdict: **CORRECT with one boundary clarification (CM-001)**. The construct is Linux-generic concurrency reasoning instantiated in Rust-for-Linux context (the `concurrency_lkmm` domain string says so honestly). Title accurately describes the construct.
- Prerequisites: LKMM familiarity (happens-before, acquire/release) is implicit at L4 — MISSING_PREREQUISITE (mild; recorded in findings).
- Conflation: L2 is partly API knowledge (flavor vocabulary), L3–L4 are reclamation reasoning; the matrix does not pin which RCU flavor (classic/SRCU/bh/kfree_rcu) each behavior refers to — ASSESSOR_AMBIGUITY (CM-003).

## 2. Existence audit (behavior-by-behavior)

| Behavior | Claim | Reality check (primary sources S2/S3/S8) | Class | necessary | common | verdict |
|---|---|---|---|---|---|---|
| CB-034-01 | Identify reader racing with removal in a schedule | Real and central: RCU protects readers in flight; removal followed by premature free is the canonical UAF class | REAL AND CENTRAL | yes | yes | SUPPORTED technically; SUPPORTED constructually |
| CB-034-02 | Traverse read-side protected list; explain matching grace period | Real: list traversal under rcu_read_lock with grace-period accounting on removal is core RCU usage | REAL AND CENTRAL | yes | yes | SUPPORTED technically; PARTIALLY_SUPPORTED constructually (CM-003) |
| CB-034-03 | Guard preventing reference escape; model remove→grace→free ordering | Real: Rust `sync::rcu::Guard` is deliberately `!Send`/per-thread (S6); ownership-vs-grace-period distinction (a refcounted reference does NOT end at grace period and vice versa) is a real, frequently-failed reasoning step | REAL AND CENTRAL | yes | yes | SUPPORTED both |
| CB-034-04 | Audit memory ordering and adversarial interleavings WITHOUT treating KCSAN as proof | Real: KCSAN is a sampling detector (S8) — "clean run" is OBSERVATION+COVERAGE; ordering claims need LKMM reasoning | REAL AND CENTRAL | yes | specialized | SUPPORTED both — this behavior is the strongest epistemics test in the catalog |
| CB-034-05 | Reviewed subsystem RCU policy covering flavor-specific lifetime contracts | Real activity (maintainer-level); but requires review infrastructure to verify | REAL BUT SPECIALIZED | no (role-dependent) | rare | TECHNICAL: SUPPORTED; CONSTRUCT: PROVISIONAL (CM-015 — observability) |

Implicit-proposition attack (required): `Rust lifetime ⇒ RCU lifetime safety` and `safe Rust ⇒ runtime reclamation correctness` are **false** as stated, and the matrix does NOT assert them — CB-034-04's wording explicitly requires reasoning beyond compiler guarantees, and invariant class separation (A/B vs C/D) forces the distinction (compiler acceptance ≠ runtime reclamation correctness). The frozen taxonomy note ("Runtime diagnostics observe bounded executions") aligns with S2/S8. Verdict: the model encodes the correct epistemic position.

## 3. Construction audit

- CB-034-01/02: DIRECTLY_OBSERVABLE from written schedule analysis. Confounder: C-kernel RCU experience transfers fully (schedules are language-neutral) — appropriate for a concurrency competency, but see CM-007: whether the L3 artifact must be Rust is unpinned.
- CB-034-03: OBSERVABLE_WITH_INSTRUMENTATION (artifact review of guard type + ordering model). The Rust binding surface (`sync::rcu::Guard`, S6) is minimal and evolving — assessors must score the reasoning, not the exact API spelling (CM-006).
- CB-034-04: INFERENTIAL (written audit quality); distinguishable from L3 by whether KCSAN-type evidence is over-trusted — a genuine discriminator (Profile D fails here).
- CB-034-05: DIFFICULT_TO_OBSERVE under current protocol (no calibrated reviewers exist; engine calibration BLOCKED).

## 4. Boundary validity — see level-boundary-analysis.md for the full record

L1→L2 is the weakest boundary (both satisfiable by API familiarity; Profile D risk, CM-002). L2→L3 and L3→L4 are genuinely discriminative. L4→L5 conflates capability with governance maturity (CM-015).

## 5. Configuration/version sensitivity (CM-001, CM-006)

Primary sources: classic RCU forbids blocking in read-side critical sections; **CONFIG_PREEMPT_RT permits RCU read-side critical sections to be preempted and permits (sleeplockified) spinlocks to block within them**; SRCU permits sleeping locks outright (S2/S3). The frozen scope declares PREEMPT_RT=y while the catalog carries a context-free `prohibited_sleep` hard gate. Within RCU read-side contexts, "prohibited sleep" is therefore **configuration-dependent**, and the competency does not say which regime governs. This does not make the gate wrong (atomic-context sleep remains prohibited universally; voluntary sleep in a classic read-side critical section remains illegal), but an assessor applying the frozen gate to a PREEMPT_RT-scoped RCU case has an under-specified rule. Classification: SCOPE / VERSION_DEPENDENT — HIGH impact on C034 specifically because its own scope selects the regime where the ambiguity bites. Durable principle (correct): atomic-context sleeping prohibition; grace-period lifetime reasoning. Implementation detail (moving): exact Rust binding shapes (S6/S7).

## 6. Interpretation

C034 tests **actual concurrent reclamation reasoning** at L3–L4 and **API-plus-reasoning** at L1–L2; the transition is real but under-discriminated (CM-002/003). The competency's epistemic architecture (KCSAN-not-proof, class separation) is technically sound and unusually rigorous.

**C034 disposition: PARTIALLY_SUPPORTED → RETAIN_WITH_BOUNDARY_CLARIFICATION** (clarifications: flavor scoping per behavior; sleep-gate semantics under PREEMPT_RT; Rust-artifact requirement pinned per behavior; L4→L5 boundary justification). No competency-file modification in this audit.
