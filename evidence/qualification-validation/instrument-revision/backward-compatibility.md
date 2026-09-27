# Backward-Compatibility Analysis (§13)

Per-change answers to the six questions. Standing distinction: HISTORICAL EVIDENCE (valid under its own instrument identity, never rewritten) vs CURRENT INSTRUMENT EVIDENCE (only what alpha.4 would produce after an approved freeze).

| Question | CH-1 oracle/context revision | CH-2 behavior addition | CH-3 rubric guidance | CH-4 oracle scope metadata | CH-5 no-duplicate-credit |
|---|---|---|---|---|---|
| old evidence remains valid? | Yes, as historical (1.1-alpha.3) evidence — old gate applied as then-defined | Yes, historical; L4 assessments simply lack CB-053-06 | Yes | Yes | Yes |
| old evidence remains comparable? | **INCOMPARABLE** (gate semantics change) | **INCOMPARABLE** for L4 (requirement set changes); comparable for L0–L3 | COMPARABLE (interpretation tightened; construct unchanged) | COMPARABLE (semantics unchanged) | **INCOMPARABLE** (scoring mechanics change) |
| old capability results reproducible? | Yes under alpha.3 rules (frozen inputs + deterministic engine); not re-derivable as alpha.4 results | Yes, same rule | Yes | Yes | Yes under alpha.3 scoring |
| old calibration cases valid? | CS-001…016 remain structurally valid; expected boundaries for sleep-gate-adjacent cases (atomic-context ones) unchanged; **re-derivation of expected boundaries required for any case exercising RT-sleepable contexts** | CS cases unaffected except CS-007/CS-001-type L4 expectations gain CB-053-06 consideration → alpha.4 case-set review required before next round | valid | valid | alpha.4 round requires updated case guidance |
| old assessor submissions valid? | None exist (NOT_RUN) — n/a; first round runs under the then-frozen instrument only | n/a | n/a | n/a | n/a |
| old criterion study valid? | No criterion data exists — n/a; frozen protocol untouched | n/a | n/a | n/a | n/a |

## Rules applied

- VALID HISTORICAL EVIDENCE is preserved by identity: every prior receipt stays bound to 1.1-alpha.3 commits/digests; nothing is rewritten, re-derived, or re-labeled (§13 mandate).
- The synthetic fixture pairs and CS-001…016 expected boundaries remain bound to the 1.1-alpha.3 instrument; alpha.4 (if approved) requires its own case-set review (a small, bounded task: 16 expected-boundary re-checks) — recorded as a Stage-B precondition.
- Default INCOMPARABLE applied exactly where constructs/scoring materially change (§12).
