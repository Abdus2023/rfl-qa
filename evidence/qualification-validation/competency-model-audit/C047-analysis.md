# C047 — Callback Teardown: Validity Audit

Construct under audit: "Scoped callback teardown behavior" (domain `c_ffi`), behaviors CB-047-01…05, oracle OR-CALLBACK with teardown schedule model, scope x86_64/CONFIG_RUST=y/PREEMPT_RT=y.

## 1. Definition

What is measured: designing and auditing the unregister→drain→callback→reference→free lifecycle for concurrently-registered callbacks across a C/Rust boundary.

- The taught pipeline — CREATE → REGISTER → ACTIVE → STOP → QUIESCE → CALLBACK DRAIN → REFERENCE DRAIN → DESTROY → FREE — is a **sufficient, workqueue-centric canonical model**, explicitly declared as a teardown state machine to be assessed, not asserted as the only valid one. Verdict: CORRECT as a scoped model; the model is a **context-specific approximation** (CM-009), which the competency does not explicitly say.
- Distinct competencies kept separate: FFI pointer-lifetime reasoning (ffi_lifetime gate), callback lifecycle design, concurrent race resolution. Not conflated. Title accurate.

## 2. Existence audit

| Behavior | Claim | Reality check (S3/S4/S7) | Class | verdict |
|---|---|---|---|---|
| CB-047-01 | Identify callback-after-free interleaving in C baseline | Canonical kernel bug class (work/timer/RCU callbacks dereferencing freed objects) | REAL AND CENTRAL | SUPPORTED both |
| CB-047-02 | Refcounted wrapper + registration owner recorded | Real: registration creates an ownership/lifetime obligation; owner recording is the standard defense | REAL AND CENTRAL | SUPPORTED; the obligation itself is implicit in the matrix (CM-012) |
| CB-047-03 | Lifetime guard + teardown state machine (unregister/callback/reference/free ordering) | Real: exactly the invariant class `cancel_work_sync` implements in Rust wrappers (S7 ScopedWork PinnedDrop→cancel_work_sync) | REAL AND CENTRAL | SUPPORTED both |
| CB-047-04 | Resolve concurrent remove/ioctl races with explicit drain synchronization + adversarial observations | Real and the hardest part of teardown design; documented caveat — cancel guarantees quiescence "as long as there are not racing enqueues" (S4) — proves drain ADMISSION gating (stop accepting registrations before draining) is genuinely necessary, not bureaucratic | REAL AND CENTRAL | SUPPORTED both; strongest boundary in the model (CM-010) |
| CB-047-05 | Reviewed subsystem-wide async callback lifecycle policy | Real activity; observability requires calibrated review infrastructure | REAL BUT SPECIALIZED | TECHNICAL SUPPORTED; CONSTRUCT PROVISIONAL (CM-015) |

## 3. Oracle-predicate audit (required attack)

- `alive(reference) ⇒ object_alive`: as an oracle this operationalizes "no dereference may follow free"; as a universal theorem it is circular/under-defined (what makes a reference "alive" if the object is gone?). Verdict: ASSESSMENT ORACLE — usable; NOT a kernel theorem.
- `callback_possible ⇒ callback_target_alive`: a real invariant for work/timer callbacks (a queued callback must not run against freed memory); kernel APIs (cancel_work_sync, del_timer_sync) exist precisely to establish it. Verdict: real invariant, but its ESTABLISHMENT is mechanism-specific (CM-009).
- `free(object) ⇒ no live ref ∧ no callback possible ∧ no RCU reader ∧ no registered owner`: a **sufficient-condition conjunction checklist for safe free in the modeled mechanism class**. It is NOT universal: (a) SLAB_TYPESAFE_BY_RCU and similar caches return objects with stale but non-garbage contents — dereference-after-free-but-before-realloc is semantically distinct; (b) refcounted release paths free objects *because* an owner dropped the last reference — "no registered owner" then means "no owner beyond the freeing path," which is a modeling convention; (c) cross-CPU stale pointers can persist. Verdict: ORACLE_MISMATCH risk if treated as universal — recommendation: the calibration harness and assessors must treat it as a scoped checklist (CM-008). The competency description ("Assessor oracle… NOT universal formal verification") already carries the correct disclaimer in the oracle files; the behavior matrix itself is silent — boundary clarification needed, not a defect.

## 4. Mechanism-dependence (CM-009)

Stage semantics change with mechanism: workqueue callbacks are cancellable and quiescible (S4); IRQ handlers are synchronized via free_irq rather than drained; timer callbacks via del_timer_sync; RCU callbacks execute in softirq/BH context (or offloaded kthreads under PREEMPT_RT/nocb configurations); tasklets are legacy with BH workqueues as the modern softirq interface (S4). Under PREEMPT_RT, most "atomic" contexts run in sleepable kernel threads, changing which context assumptions an engineer may rely on. The pipeline remains a valid *ordering skeleton*; an assessor must be permitted to accept mechanism-appropriate reorderings — the matrix's "covering unregister/callback/reference/free ordering" phrasing tolerates this, but nothing instructs the assessor on it (ASSESSOR_AMBIGUITY, folded into CM-009).

## 5. Construction audit

- CB-047-01/02: DIRECTLY_OBSERVABLE (artifact/trace). Confounders: prior workqueue experience; C background (Profile C) can satisfy L1–L2 conceptually — see CM-007 (language pinning ambiguity, shared with C034).
- CB-047-03: OBSERVABLE_WITH_INSTRUMENTATION (state machine review). 
- CB-047-04: DIRECTLY_OBSERVABLE through adversarial schedule resolution — the discriminating construct vs API knowledge (Profile D fails: memorized cancel APIs do not produce a drain-admission design).
- CB-047-05: DIFFICULT_TO_OBSERVE under current protocol (CM-015).

**C047 disposition: PARTIALLY_SUPPORTED → RETAIN_WITH_BOUNDARY_CLARIFICATION** (clarifications: oracle-predicate scoping statement; mechanism-tolerance instruction; release-callback context behavior; registration-obligation explicitness). No competency-file modification in this audit.
