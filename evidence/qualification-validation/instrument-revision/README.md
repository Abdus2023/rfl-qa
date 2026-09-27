# Instrument Revision & Change-Control — Stage A Package (v1.1-alpha.4 proposal)

Stage: **A (Proposal) — COMPLETE. Stage B (Implementation): DEFERRED** — no explicit governing approval mechanism exists in this environment (no appointed governance body; GOVERNANCE.md reserves appointment for human maintainers), so per §17B: `IMPLEMENTATION = DEFERRED`, `NEW INSTRUMENT FREEZE = NOT_REACHED`. The authoritative instrument remains **1.1-alpha.3** (hash-frozen; aggregate digest byte-identical to the phase-1 freeze — zero drift proven). Nothing in competency/, schemas/, oracles/, assessors/, or invariants/ was modified in this stage.

## Required final report (§22, A–K)

**A. Current instrument identity** — Version `1.1-alpha.3` (unreleased); source commit `f1f4810058b58bcb4183e85d473f717823ae9792`; 32 instrument files; aggregate digest `8fbf31d89f7e8391…` (method and full per-file hashes in `current-instrument-manifest.yaml`; equality with the phase-1 freeze verified programmatically).

**B. Audit findings imported** — From `f1f4810` (unaltered; package hash-checked): CM-001 (HIGH, → CH-1), CM-014 (HIGH, → CH-2), CM-002/003 (C034 L1→L2, → CH-3), CM-008/009 (C047 oracle scope, → CH-4), CM-018 (double-counting, → CH-5), CM-015 (L4→L5 OPEN, → NC-1 retention); CM-011/CM-019 deferred (NC-2/NC-3). Audit statuses (PARTIALLY_SUPPORTED ×3) imported as-is — not converted to VERIFIED.

**C. Proposed changes** — Five exact-target deltas + three explicit non-changes, machine-readable in `change-proposal.yaml`: CH-1 ORACLE_REVISION (execution-context classification for the sleep gate; per-context predicates; PREEMPT_RT-correct), CH-2 BEHAVIOR_ADDITION (CB-053-06 publication semantics @ L4 + OR-PIN-publication), CH-3 RUBRIC_REVISION (C034 L1→L2 invariant-bound scoring guidance), CH-4 CLARIFICATION (oracle scope_metadata: scoped checklist ≠ theorem; exceptions list), CH-5 RUBRIC_REVISION (no-duplicate-credit rule + artifact-distinct evidence). NC-1: L5 retained OPEN/NOT_OBSERVABLE_WITH_CURRENT_PROTOCOL.

**D. Technical justification** — Primary sources S1–S5 (Pin semantics; RCU/PREEMPT_RT requirements docs; workqueue cancel guarantees with racing-enqueue caveat; kernel::init reality), audit findings, and the instrument's own wording gap ("in prohibited context" with no context definition). Evidence classes recorded per change; expert judgment never labeled PROOF.

**E. Construct justification** — CH-1 removes a configuration-induced false signal (same behavior judged differently than the frozen scope's own kernel semantics require); CH-2 closes the largest construct-vs-purpose gap (publication named but unmeasured); CH-3/CH-5 tighten scoring against known gaming profiles (D, H); CH-4 kills the checklist→theorem upgrade path. Each improves observability or reduces confounding — the §30 objective.

**F. Boundary analysis** — L0–L4 boundaries: unchanged except C034 L1→L2 scoring guidance (boundary retained; practical discrimination OPEN pending real assessors). L4→L5: all three retained OPEN; no boundary manufactured; L5 marked UNSATISFIED-BY-INFRASTRUCTURE in assessment mechanics.

**G. Oracle analysis** — Mechanically evaluated: gate firing per declared context (CH-1), OR-PIN-publication three-element predicate (CH-2), scope-metadata presence + semantic freeze of existing checks (CH-4), double-count annotation (CH-5). Contextual (assessor-judged): audit-quality behaviors, context boundary cases under RT (BH-off sections etc.), rubric-guidance application.

**H. Cross-competency effects** — C034×C047 shared invariant made explicit (drain-before-release) with duplicate-credit prohibition and artifact-distinctness rule; C053×C047 init-registration interaction absorbed into CB-053-06 with cross-reference (post-registration stays C047); shared prerequisite statements remain creditable only from competency-local evidence.

**I. Historical compatibility** — All prior evidence remains VALID HISTORICAL under 1.1-alpha.3 identity; CH-1/CH-2/CH-5 INCOMPARABLE going forward; CH-3/CH-4 COMPARABLE_HISTORICAL; old synthetic fixtures/case boundaries bound to alpha.3; an alpha.4 case-set review (16 expected-boundary re-checks) is a Stage-B precondition; no human calibration exists to invalidate; calibration reset rule recorded.

**J. Adversarial review** — 13 attack questions in `adversarial-review.md`; no blocking finding; R2/R3/R7 carry implementation-time requirements (artifact-binding wording; RT boundary-case table; per-freeze version re-anchoring); R12 records the inherent limit: a proposal can be well-specified, never empirically validated at proposal stage. Proposal status: PARTIALLY_SUPPORTED.

**K. Decision** — **REVISION_READY_FOR_IMPLEMENTATION** (as a proposal: exact targets, evidence-referenced, adversarially reviewed, regression-planned, comparability-declared). Simultaneously and without contradiction: `IMPLEMENTATION = DEFERRED`, `NEW INSTRUMENT FREEZE = NOT_REACHED` — Stage B requires explicit governing approval that no existing mechanism can grant. The revised instrument is NOT claimed valid; validity would require the new freeze, then a real calibration round under it, none of which can occur here.

## Stop conditions (§24) & anti-overclaim (§23)

No §24 condition triggered (verified item-by-item in adversarial-review.md). §23 checklist: all 25 items verified — see final message; highlights: current instrument frozen & hashed ✓; audit preserved unchanged ✓; no historical rewrite ✓; CM-001/CM-014 explicitly analyzed ✓; C034 L1→L2 attacked ✓; C047 oracle scope attacked ✓; all three L4→L5 attacked ✓; double-counting analyzed ✓; exact targets ✓; evidence refs ✓; technical ≠ construct validity ✓; probes ≠ calibration ✓; no reliability/criterion/measurement-validity claims ✓; E→L, hard-gate veto, provenance closure protected ✓; historical immutable ✓; material changes → calibration reset ✓; no competency file modified ✓; no force push ✓; no tag ✓; tree clean ✓.

## Core invariants preserved

CURRENT INSTRUMENT (1.1-alpha.3, authoritative) ≠ PROPOSED INSTRUMENT (alpha.4, unfrozen) ≠ CALIBRATED INSTRUMENT (none exists) ≠ VALIDATED MEASUREMENT (NOT_ESTABLISHED). FREEZE → FORMALIZE → ATTACK → REVIEW → FREEZE AGAIN → ONLY THEN IMPLEMENT → ONLY THEN RECALIBRATE: this package completes FORMALIZE/ATTACK/REVIEW for a proposal whose FREEZE AGAIN awaits an authority this environment does not have.

## Package contents

`current-instrument-manifest.yaml` · `change-proposal.yaml` · `CM-001-preempt-rt.md` · `CM-014-publication.md` · `C034-boundary.md` · `C047-oracle-scope.md` · `L5-boundaries.md` · `double-counting.md` · `backward-compatibility.md` · `regression-plan.md` · `construct-probes.md` · `adversarial-review.md` · this README.
