# CM-014 Change Analysis — C053 Publication Semantics

## The defect, precisely

C053's construct is "correct construction **and publication** of immovable kernel objects," but no behavior measures publication. A candidate can pass C053 while believing `!Unpin`/`Pin<T>` yields safe concurrent publication — the exact naive equivalences the audit attacked. Primary sources: `Pin` guarantees address stability via the type system and nothing about memory visibility or cross-CPU ordering (S1); `kernel::init` provides in-place constructors (S5) — construction machinery, not publication semantics.

## The missing distinction (§7 investigation)

`object initialized` ≠ `object safely published`. The chain the revised construct must make explicit:

1. **initialization completion** — all fields initialized in place; failure paths handled (already CB-053-04);
2. **ownership transfer** — who owns the object after init succeeds (allocator contract → caller → kernel registry);
3. **publication** — the act of making the object reachable by other execution contexts;
4. **visibility/synchronization** — publication requires release/acquire-style ordering or stronger; Rust's type system does NOT supply this automatically (S1); kernel primitives do;
5. **registration interaction** — registration-before-publication (object reachable by callback machinery while partially initialized → CM-019 boundary, absorbed here as ordering obligation), publication-before-registration (window where object is reachable but unregistered), and failure-during-registration unwinding;
6. **pinning vs initialization vs publication** — three distinct axes: Pin constrains movement; initialization is state; publication is a visibility event. None implies another.

Rejected equivalences (unless independently justified — they are not): `Pin<T> = fully initialized`, `!Unpin = safe publication`, `successful initialization = safe concurrent publication`.

## Proposed behavior (full §7 schema)

```yaml
behavior_id: CB-053-06
construct: publication correctness for initialized pinned kernel objects
engineering_situation: >
  An initialized pinned object must become reachable by other CPUs / kernel subsystems
  (device registration, callback registration, publish-through-pointer); incorrect
  publication yields stale-value or partially-observed-object bugs invisible to Pin.
candidate_action: >
  Design/audit the publication path: state the ownership transfer point, the required
  synchronization for visibility (e.g., kernel primitive with release semantics on
  publish / acquire on consume), and the ordering between publication and any callback
  registration; identify what remains a runtime kernel invariant beyond Rust guarantees.
observable_evidence: >
  Written publication/registration design or artifact review with explicit
  synchronization and ownership-transfer statements; adversarial question responses on
  publication-before-registration windows.
required_invariants: [B01, C01, D01]
oracle: OR-PIN-publication — PASS requires stated synchronization evidence + ownership
  transfer point + registration-ordering statement; BLOCKED if publication asserted with
  none of the three (assertion is not evidence).
confounders: [Rust Send/Sync fluency (must not substitute for kernel-context reasoning),
  API churn of init machinery (CM-020), prior driver publication experience]
level: L4
reason_for_level: >
  Requires adversarial audit-grade reasoning integrating ownership, synchronization, and
  lifecycle ordering — same class as CB-053-04; not constructible (L3) and not perceptible
  (L1/L2). Cumulative rule preserved: requires CB-053-01..05 first.
```

## What does NOT change

Existing CB-053-01..05 semantics; hard gates; E→L separation (new behavior is behavior-evidenced, never tier-inferred); the L4→L5 boundary (unchanged — NC-1); C047/C034 matrices. Oracle OR-PIN gains one check; OR-CALLBACK/OR-RCU untouched (their registration interactions already assessed via CB-047-02/03).

## Comparability

INCOMPARABLE for L4 results (requirement set changes). Historical alpha.3 records remain valid historical evidence under their own instrument identity. First real calibration round must occur under alpha.4 (calibration reset rule).
