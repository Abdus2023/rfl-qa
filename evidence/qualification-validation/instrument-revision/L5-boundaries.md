# L4→L5 Boundary Redesign Analysis (§10) — result: NO boundary manufactured

## What is L5 supposed to measure?

Current text (all three competencies): "Produces a **reviewed** reusable subsystem policy …" — i.e., a governance-infused artifact. The audit (CM-015) showed this conflates technical capability with review access and governance maturity: a superb technical engineer without review access fails; a mediocre one with review access passes.

## Required separation (§10)

- **Technical capability**: what the engineer can design, audit, and generalize (observable from artifacts).
- **Organizational authority**: maintainer/reviewer roles — MUST NOT grant capability levels.
- **Governance maturity**: review infrastructure quality — MUST NOT be a candidate's burden.

## Can L5 be made observable here?

Candidate observable reformulations were considered: (a) "authors a policy artifact with explicit ABI/lifetime boundaries" (drop "reviewed") — attack: an unreviewed policy is exactly what CB-053-04-grade audits already cover; demoting L5 to "writes a long document" converts governance conflation into **task-size conflation**, the §7 forbidden substitution; (b) "cross-subsystem reasoning" — attack: not observable within the frozen single-subtask alpha scope (Profile H, CM-017); (c) "migration/leadership" — organizational by definition.

**Conclusion (§10 mandate): no observable, independently assessable L5 construct can be established in this environment without manufacturing a boundary.** L5 remains **OPEN / NOT_OBSERVABLE_WITH_CURRENT_PROTOCOL**. Non-change NC-1 adds only an assessment-mechanics clarification: L5 requirements are marked UNSATISFIED-BY-INFRASTRUCTURE (not failed-by-candidate) until calibrated independent review exists. L0–L4 boundaries are untouched. Ceiling epistemics preserved: qualification ceiling stays below L5 under the current protocol; VERIFIED ceiling remains blocked independently.
