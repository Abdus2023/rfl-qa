# Adversarial Candidate Profiles (§14) — construct attacks, no scores assigned

Each profile is a conceptual engineer; the question is whether the behavior matrices classify them in a technically sensible way. No overall good/bad judgment; specific construct failures identified.

| Profile | Description | Predicted matrix behavior | Verdict |
|---|---|---|---|
| A | Rust-strong, Linux-concurrency-weak | C053: reaches L3–L4 (Pin fluency transfers); C034: fails early (cannot read reader/remove schedule sensibly); C047: L2–L3, fails L4 | SENSIBLE — concurrency competencies resist pure-Rust talent; good construct separation |
| B | Linux-concurrency-strong, Rust-weak | C034: schedules are language-neutral — reaches L4 reasoning except CB-034-03 requires "constructs a guard" (Rust-shaped); C047 similar at L2–L3; C053 blocked ≤L1 | PARTIALLY SENSIBLE — construct failure CM-007: the model never pins whether artifacts must be Rust; B's placement swings on an unpinned convention |
| C | C/FFI-strong, RfL-weak | Like B for C047 (L1–L2 natural in C terms); C053 blocked early | SENSIBLE for C053 (rejects C-only profile from pinned-Rust construct); AMBIGUOUS for C047 (CM-007) |
| D | API memorization, weak invariant reasoning | Passes C034 L1–L2 (CM-002), fails C034 L4 (KCSAN epistemics) and C047 L4 (drain admission); C053 L2 pass / L3–L4 fail | SENSIBLE — the L2→L3/L3→L4 boundaries do the intended work |
| E | Invariant reasoning strong, exact API unfamiliar | C034 L3–L4 reachable (reasoning over vocabulary); C047 L3–L4 reachable; C053 L3 penalized by machinery churn (CM-020) | MOSTLY SENSIBLE — C053 carries an API-churn confound the rubric must neutralize by scoring reasoning over macro fluency |
| F | Implementation-strong, explanation-weak | All matrices require recorded, evidence-linked explanation; F underplaced if explanations are weak | SENSIBLE BY DESIGN — explanation is part of auditable capability; recorded, not treated as defect |
| G | Review-strong, implementation-weak | Blocked at cumulative implementation behaviors (L2–L3) despite excellent L4-grade audits | CONSTRUCT RESTRICTION (CM-016): cumulative scale cannot represent auditor capability separately; documented rubric choice — retained with boundary note |
| H | Strong in one subsystem, weak transfer | Passes at full level within the single synthetic task scope; transfer never probed | SCOPE GAP (CM-017): transfer/generalization unmeasured — classification OPEN (acceptable for alpha scope, must be stated) |

## Specific construct failures identified

1. **CM-007 (language pinning):** B/C placements hinge on an unpinned convention (must artifacts be Rust?). Must be resolved before calibration design.
2. **CM-016 (cumulative single scale):** G is unrepresentable; accept and document, or split builder/auditor tracks at a future freeze.
3. **CM-002 + CM-013:** D passes too much in C034 L1–L2 and C053 L1 (C-generic layer) — prerequisite layers should be scored as prerequisite evidence, not kernel competence.
4. **CM-017 (transfer):** H exposes that the alpha case scope cannot support transfer claims; scope statements must forbid extrapolation (consistent with the frozen no-extrapolation rules).

No profile required inventing a new status; all verdicts use the frozen vocabulary. These are hypotheses for calibration design, not empirical placements.
