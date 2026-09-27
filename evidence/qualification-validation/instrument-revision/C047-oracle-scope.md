# C047 Oracle-Scoping Analysis (§9)

## Classification of the predicates

| Predicate | Classification | Grounds |
|---|---|---|
| `alive(reference) ⇒ object_alive` | context-specific oracle predicate | circular without a defined liveness source; operationalizes "no dereference follows free" for the modeled mechanism class |
| `callback_possible ⇒ callback_target_alive` | real kernel invariant, mechanism-specifically ESTABLISHED | cancel_work_sync/del_timer_sync/free_irq exist to establish it; guarantee holds only against the documented race envelope (S4: "as long as there aren't racing enqueues") |
| `free(object) ⇒ no live ref ∧ no callback possible ∧ no RCU reader ∧ no registered owner` | sufficient-condition assessment checklist for the modeled scope | NOT universal: SLAB_TYPESAFE_BY_RCU-class caches free objects whose contents remain valid until reuse (deref-after-free ≠ immediate garbage); refcounted-release paths free *because* the last owner dropped — "no registered owner" is a modeling convention of the checklist; cross-CPU stale-pointer windows persist |

## Exception inventory (§9 mandated investigations)

- **SLAB_TYPESAFE_BY_RCU / object reuse**: free ≠ memory invalid; distinct semantic stage — checklist still usable (the conjunction describes when free is SAFE), but "no access follows free" claims must not be reported as memory-unsafety proofs of past accesses.
- **RCU-protected reuse & delayed reclamation**: kfree_rcu/call_rcu shift the free point; checklist applies at the actual free point, after the grace window — assessors must not demand immediate post-unlink frees.
- **Workqueue semantics**: cancel guarantees quiescence only vs the documented race envelope (S4); drain-admission gating is therefore necessary, not decorative (CM-010 positive finding — preserved).
- **Cancellation races**: re-queue/self-re-queue work — cancel_work_sync covers it (S4); the checklist's "no callback possible" must be evaluated at the final free point, not mid-teardown.
- **Callback admission**: admission gating (stop accepting registrations before drain) is part of establishing the conjunction in concurrent settings — already assessed at CB-047-04.
- **Reference-counted ownership**: release-path freeing makes "no registered owner" true only in the beyond-last-owner sense — scope metadata must say so.
- **Configuration-dependent behavior**: PREEMPT_RT threading changes execution contexts (handled by CH-1, not here).

## Decision (§9: do not change an oracle merely for terminology)

Oracle semantics — checks, predicates, expected/failure conditions — are **unchanged** (CH-4 is metadata + rubric guidance only): a `scope_metadata` block (interpretation: scoped sufficient-condition checklist; not: universal theorem; exceptions list) on each oracle, plus a rubric rule forbidding theorem-upgrade phrasing in reports. This prevents the assessor failure mode (scoped checklist silently promoted to universal kernel theorem) without perturbing oracle mechanics, E→L separation, or historical comparability. Regression RG-C047O-1 asserts the metadata presence and that check semantics hash-unchanged for assessed fields.
