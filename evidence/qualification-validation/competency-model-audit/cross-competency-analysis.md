# Cross-Competency Overlap Audit (C034 × C047 × C053)

## Overlap matrix

Concepts are scored for how strongly each competency's behavior matrix engages them: `—` none, `◦` supporting role, `●` central.

| Concept | C034 | C047 | C053 | Overlap verdict |
|---|---|---|---|---|
| Lifetime | ● (grace periods) | ● (teardown lifetime) | ● (pinned lifetime) | INTENTIONAL_COMPOSITION (different lifetime *mechanisms*: RCU vs drain vs pin) |
| Ownership | ● (ref vs grace) | ● (registration owner) | ◐ (allocator contract) | INTENTIONAL_COMPOSITION |
| Publication | ◦ | ● (registration publication) | ◐ **(missing — CM-014)** | MISSING BOUNDARY (see below) |
| Concurrency | ● | ● (remove/ioctl races) | ◦ | INTENTIONAL_COMPOSITION |
| Deferred work | ● (call_rcu family) | ● (work callbacks) | — | INTENTIONAL_COMPOSITION |
| Callback safety | ◐ (RCU callbacks) | ● | ◐ (callback publication at init) | INTENTIONAL_SHARED with one gap (CM-019) |
| Initialization | — | ◐ (create stage) | ● | INTENTIONAL_COMPOSITION (lifecycle endpoints) |
| Teardown | ◐ (grace as drain) | ● | ◐ (unwind paths) | INTENTIONAL_COMPOSITION |
| FFI | — | ● (C pointer validity) | ◐ (Opaque/FFI repr) | INTENTIONAL_COMPOSITION |
| Runtime invariants | ● | ● | ● | INTENTIONAL_SHARED (class C/D separation) — risk of scoring the same statement three times (CM-018b) |
| Rust type-system reasoning | ◐ | ◐ | ● | INTENTIONAL_COMPOSITION |

## Strong-overlap verdicts

1. **C034 × C047 — grace period as reference-drain mechanism: INTENTIONAL_COMPOSITION, sound.** A grace period is precisely a "reference drain" for RCU-readers in the C047 pipeline; the competencies require genuinely different reasoning (temporal reader accounting vs lifecycle state-machine design).
   - **Duplication risk (CM-018):** CB-034-03 ("models remove/grace-period/free ordering") and CB-047-03 ("unregister/callback/reference/free ordering") can be satisfied by one and the same ordering argument. Mitigation for calibration design: each must be evidenced against distinct artifacts/schedules (already partially the case: OR-RCU vs OR-CALLBACK schedules differ). Assessment guidance must forbid double-counting a single ordering argument across both competencies.
2. **C053 × C047 — lifecycle endpoints: INTENTIONAL_COMPOSITION with a MISSING BOUNDARY (CM-019).** Registration during initialization (callback published before init completes; partially-initialized object reachable by an already-registered callback) is owned by neither matrix: C053 owns init-unwind, C047 owns post-registration teardown. Classification: MISSING_BOUNDARY — record as construct hypothesis for the next freeze; do not patch now.
3. **C034 × C053 — weak coupling: CORRECT.** Pin/init machinery has minimal RCU interaction; no artificial duplication found.
4. **Runtime-invariant statements (class C/D) recur in all three: INTENTIONAL_SHARED, with a scoring hazard (CM-018b).** The invariant separation (A/B vs C/D with independent epistemic/strength fields) is the model's best anti-conflation device; the hazard is assessor-level: the same "runtime diagnostic ≠ proof" statement could satisfy invariant findings in all three competencies. Guidance: invariant findings must reference competency-local evidence.

## Structural conclusion

No accidental conflation of distinct competencies was found; the three competencies compose as lifecycle phases (construct → protect/operate → reclaim) with (a) one known duplication risk to manage at assessment time, (b) one unowned boundary (init-time registration), and (c) one construct-level omission (publication semantics in C053). All three are recorded in findings.yaml with recommended actions for the **next instrument freeze**, not executed now.
