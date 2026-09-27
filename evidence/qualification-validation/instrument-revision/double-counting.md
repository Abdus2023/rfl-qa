# Double-Counting Analysis (§11) — C034-03 × C047-03 and other overlaps

## Dependency graph (behavior → construct → invariant → oracle → evidence)

```
CB-034-03 (guard + remove/grace/free model)
  → construct: temporal reader-accounting (grace period as reference drain)
    → invariants: C01 (drain before release), D01 (external unregister/drain contracts)
      → oracle: OR-RCU schedule checks
        → evidence: RCU-flavored schedule artifacts

CB-047-03 (lifetime guard + teardown state machine)
  → construct: lifecycle state-machine design (unregister/callback/reference/free)
    → invariants: C01 (same drain-before-release), D01 (same external contracts)
      → oracle: OR-CALLBACK schedule checks
        → evidence: teardown-flavored schedule artifacts
```

The two behaviors **share the abstract invariant** (drain-before-release: C01/D01) but exercise **different mechanisms** (RCU reader accounting vs callback/lifecycle state design). One ordering argument can genuinely satisfy both if the artifact is single — that is DUPLICATE CREDIT for the shared abstraction while the mechanisms differ.

## Other overlap checks (from the audit's overlap matrix)

- C053-04 (init unwind) × C047 (teardown): different lifecycle stages (construction-failure vs post-registration teardown) — SHARED PREREQUISITE (correctness reasoning), not duplicate credit, provided evidence artifacts differ.
- Runtime-invariant statements (class C/D) recurring in all three: SHARED PREREQUISITE for the reasoning habit; must be evidenced per competency from competency-local artifacts (audit CM-018b hazard).
- OR-RCU schedule checks × OR-CALLBACK schedule checks: distinct oracle instances; no mechanical double-count.

## Classification & rule (→ CH-5)

- SHARED PREREQUISITE: allowed; appears in multiple competencies; no credit inflation by itself.
- INDEPENDENT COMPETENCE: mechanism-specific design/audit work — credited per competency from **artifact-distinct** evidence.
- DUPLICATE CREDIT: forbidden — one artifact/argument may support at most one of {CB-034-03, CB-047-03}; cross-competency reuse beyond the shared prerequisite requires explicitly different mechanisms and must be annotated in derived reports.

Encoded as a rubric scoring rule (CH-5) — mechanics change, conservative direction; regression RG-DUP-1 (a test dossier attempting single-artifact double-credit must derive with the reuse annotation and must not elevate both behaviors to DEMONSTRATED from that artifact alone).
