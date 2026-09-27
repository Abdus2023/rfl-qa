# C034 L1→L2 Boundary Analysis (§8)

## Attack

Does the current boundary separate **RCU API familiarity** from **actual concurrent reclamation reasoning**? The audit (CM-002) found it weak: both levels are satisfiable by vocabulary plus C-kernel transfer. Difficulty alone must not be the discriminator (§8: do not use difficulty alone).

## Candidate discriminators (documented per §8 schema)

| Discriminator | knowledge required | reasoning required | observable artifact | likely confounders | expected failure mode |
|---|---|---|---|---|---|
| D1: "Which grace period covers this removal — and what may be freed after it elapses?" | flavor names | the invariant: readers in flight remain unreclaimed until grace period ends; consequences for the specific removal | written answer referencing the supplied schedule | memorized definitions without application | restates API docs; never binds to the schedule's removal |
| D2: "This reader holds a reference across the grace period — may the object be freed now?" | none beyond D1 | ownership-vs-grace separation: a refcounted reference outlives grace obligations; freeing requires BOTH conditions resolved | written yes/no + invariant justification | C-kernel training transfers (acceptable: it IS a concurrency competency) | answers from pattern-matching ("RCU ⇒ wait ⇒ free") without noticing the independent reference |
| D3: "Two candidate free points: after unlink, after grace period. Which is correct and why does the other fail?" | grace-period role | necessity ordering: unlink removes reachability for NEW readers; grace period protects EXISTING readers | written ordering argument | API recall | picks correct point with wrong (or absent) mechanism reasoning |

## Decision

D1–D3 share one property: the correct answer **must reference the specific schedule's invariant**, not vocabulary. This yields CH-3's rubric guidance (score CB-034-02 DEMONSTRATED only on invariant-bound reasoning). No behavior/oracle text changes; the boundary itself is retained; per §8/§13: practical discrimination remains **OPEN** — paper probes (P-C034-1/2 in construct-probes.md) support the guidance's discriminability hypothesis, but only real assessor rounds can establish actual discrimination. This is deliberately not forced to closure.

## What would make it CLOSE

A real two-assessor round in which one assessor applies vocabulary-only scoring and the guidance-constrained scoring diverge on ≥1 case, followed by adjudicated review — i.e., evidence from the BLOCKED calibration infrastructure.
