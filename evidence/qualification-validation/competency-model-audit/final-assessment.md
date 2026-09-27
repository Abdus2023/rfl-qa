# Competency-Model Audit — Final Assessment (§22 structure)

Evidence classes per finding: PRIMARY_SOURCE (kernel.org/Rust-project docs), UPSTREAM_IMPLEMENTATION, UPSTREAM_REVIEW/DISCUSSION, SYNTHETIC_CASE (paper probes), EXPERT_JUDGMENT (audit reasoning — never PROOF), REPOSITORY_ASSERTION (frozen model text). No synthetic probe is presented as calibration; no upstream implementation is presented as candidate-competence evidence.

## A. Definition — what each competency actually measures

- **C034**: concurrent reclamation reasoning — reader-side protection, grace-period accounting, ordering models, and epistemically disciplined auditing of concurrency claims. Linux-generic concurrency instantiated in RfL; honestly labeled (`concurrency_lkmm`).
- **C047**: design and verification of callback lifecycle teardown across a C/Rust boundary — from hazard perception through concurrent drain design.
- **C053**: in-place pinned initialization — from address-stability fundamentals (generic layer) through kernel object construction (kernel-specific layer). Measures a deliberate mixture; requires rubric separation of layers (CM-013).

## B. Technical defensibility

All 15 behaviors correspond to real engineering concerns (13 REAL AND CENTRAL, 2 REAL BUT SPECIALIZED — the two L5 policy behaviors). No technically incorrect claim was found in any behavior statement. Statuses: 13 SUPPORTED (technical), 2 SUPPORTED-with-observability-provisional (L5s). The frequently-attested naive equivalences (`Rust lifetime ⇒ RCU safety`, `safe Rust ⇒ reclamation correctness`, `Pin = initialized`, `!Unpin = safe publication`) are **not asserted anywhere** in the matrices; C034-L4 and C053-L3 actively require reasoning beyond them.

## C. Construct validity

- **Supported constructs**: hazard perception (all three L1s); artifact construction (C047 L2–L3, C053 L2–L3); ordering/state-machine design; adversarial audit with epistemic discipline (C034 L4, C053 L4, C047 L4 — the strongest).
- **Degraded constructs** (PARTIALLY_SUPPORTED): C034 L1→L2 (API-familiarity confound, CM-002/003); C053 L1/L2 generic layer if scored as kernel competence (CM-013); oracle predicates if treated as theorems (CM-008).
- **Open constructs**: all three L5s (governance conflation, CM-015); init-time registration boundary (CM-019).
- Two REQUIRED_BUT_MISSING omissions weaken construct completeness: publication semantics (CM-014, HIGH) and release-callback context (CM-011).

## D. Level boundaries

Supported: C034 L0→L1, L2→L3, L3→L4; C047 L0→L1, L1→L2, L2→L3, L3→L4 (strongest); C053 L0→L1, L1→L2 (most objective), L3→L4.
Partially supported: C034 L1→L2; C053 L2→L3.
Open: **all three L4→L5 boundaries** — not discriminative under the frozen protocol until calibrated independent review exists (CM-015).

## E. Coverage

Represented well: hazard perception, lifetime/ownership reasoning, teardown design, adversarial audit, epistemic discipline, FFI lifetime, in-place initialization. Omitted within scope: publication semantics (CM-014), release-context discipline (CM-011), configuration sensitivity as an explicit skill, positive lock design. Correctly excluded by scope: DMA, NMI, ARM64, architecture sensitivity.

## F. Observability

DIRECTLY_OBSERVABLE: schedule analyses, wrapper/state-machine artifacts, compile-fail demos (the only machine-recheckable evidence in the catalog). OBSERVABLE_WITH_INSTRUMENTATION: guard/ordering artifacts, audits. INFERENTIAL: audit quality, epistemic discipline. NOT_OBSERVABLE_WITH_CURRENT_PROTOCOL: all three L5 policy behaviors (require calibrated reviewers — infrastructure BLOCKED). No behavior depends on unobservable mental states.

## G. Cross-competency structure

Intentional composition confirmed (lifecycle phases: construct → protect/operate → reclaim) with no accidental conflation of distinct competencies. Managed risks: ordering-argument double-counting between CB-034-03 and CB-047-03 (CM-018 — calibration-design rule required); one unowned boundary (init-time registration, CM-019); shared runtime-invariant statements must be evidenced locally per competency.

## H. Version stability

Durable principles (stable across versions): grace-period lifetime reasoning, teardown ordering invariants (as scoped checklists), address stability before publication, in-place fallible init, epistemic limits of dynamic tools. Implementation-anchored (moving): Rust binding surfaces (`sync::rcu::Guard`), pin-init machinery (merged in `kernel::init`, split crate, 2026 upstream sync), workqueue lifetime wrappers (`ScopedWork`/cancel-in-drop). Configuration sensitivity is real (PREEMPT_RT changes RCU read-side and sleep semantics — S2/S3) and currently implicit (CM-001). Behaviors are phrased at the durable level (good); assessor examples must re-anchor per instrument freeze (CM-020).

## I. Required changes before real calibration (recommendations ONLY — no file modified in this audit)

1. Clarify `prohibited_sleep` gate semantics per execution context/configuration, explicitly for the PREEMPT_RT RCU case (CM-001).
2. Pin RCU flavor per L2 task and pin artifact-language expectations per behavior (CM-003, CM-007).
3. Add publication-semantics behavior to C053 and release-context behavior to C047 (CM-014, CM-011) — ADD_MISSING_BEHAVIOR.
4. Restate the C047 oracle conjunction as a scoped sufficient-condition checklist in assessor guidance; forbid universal-theorem upgrades (CM-008, CM-009).
5. Resolve the L4→L5 boundary: either bind L5 evidence to the (future) calibrated review infrastructure explicitly, or split a provisional "policy draft" level from "reviewed policy" (CM-015).
6. Calibration-design rules: forbid cross-competency evidence reuse (CM-018); score C053 L1/L2 as prerequisite evidence (CM-013); re-anchor API examples per freeze (CM-020).

All changes require a **new instrument freeze** under the frozen rules; none is executed here.

## J. Residual uncertainty (OPEN)

- Whether L5 constructs are valid capability boundaries at all (depends on real rounds with independent reviewers — CM-015/CM-004).
- Whether C034 L1→L2 discriminates in practice once assessors apply clarification guidance (CM-002) — resolvable only by actual inter-rater evidence.
- Init-time registration ownership (CM-019) — needs design evidence from real assessment cases.
- All construct-validity probes remain paper hypotheses; none has empirical weight.

## Competency dispositions (§19 decision classes)

| Competency | Status | Disposition |
|---|---|---|
| C034 | PARTIALLY_SUPPORTED | RETAIN_WITH_BOUNDARY_CLARIFICATION |
| C047 | PARTIALLY_SUPPORTED | RETAIN_WITH_BOUNDARY_CLARIFICATION |
| C053 | PARTIALLY_SUPPORTED | RETAIN_WITH_BOUNDARY_CLARIFICATION (+ deferred ADD_MISSING_BEHAVIOR recommendation) |
| Level boundaries | 9 SUPPORTED / 3 PARTIALLY_SUPPORTED / 3 OPEN (L4→L5 ×3) | REVISE_LEVEL_BOUNDARY candidates deferred to next freeze |

Severity counts: 4 HIGH, 11 MEDIUM, 4 LOW, 1 INFO across 20 findings (findings.yaml).

## Release implications (§23) — recomputed state

This audit improves evidence for **competency-model validity hypotheses only**. It changes nothing it cannot:

- `calibration = BLOCKED` (unchanged — no human assessors)
- `inter_rater_reliability = NOT_RUN` (unchanged)
- `criterion_validity = NOT_ESTABLISHED` (unchanged — no independent outcome dataset)
- `measurement_validity = NOT_ESTABLISHED` (unchanged — technical audit ≠ measurement validity)
- `kernel_execution = NOT_RUN`, `dynamic_analysis = NOT_RUN` (unchanged)
- `release = BLOCKED` (unchanged; the audit creates no qualifying evidence)

## Mandatory anti-overclaim verification (§24 checklist)

```
[ x ] No claim of assessor reliability without assessors
[ x ] No claim of criterion validity without independent criterion data
[ x ] No capability level inferred from technical plausibility
[ x ] No technical claim upgraded solely from repository prose
[ x ] No synthetic case presented as empirical calibration
[ x ] No universal theorem inferred from context-specific oracle
[ x ] No Rust type-system guarantee substituted for runtime kernel invariant
[ x ] No API familiarity treated as engineering competence without behavioral evidence
[ x ] No task difficulty substituted for capability level
[ x ] No version-specific behavior presented as timeless
[ x ] No historical evidence overwritten
[ x ] No force push
[ x ] No fabricated execution receipt
[ x ] No silent competency-file modification
```

Governing principle preserved: HONEST ENGINE ≠ VALID CONSTRUCT ≠ RELIABLE ASSESSMENT ≠ EXTERNAL VALIDITY. NO EVIDENCE → NO VERIFIED CLAIM.
