# L0–L5 Boundary Audit + Construct-Validity Probes

Rule under test: levels are cumulative; a level requires every behavior up to it and no failed required behavior (assessors/rubric.md). Distinguishing question per boundary: **CAPABILITY COMPLEXITY ≠ TASK COMPLEXITY**.

## Boundary-by-boundary record

### C034 (RCU grace periods)
| Boundary | New responsibility | Verdict |
|---|---|---|
| L0→L1 | hazard perception in a supplied schedule | SUPPORTED — clear, observable, minimal prerequisites |
| L1→L2 | active traversal + grace-period explanation | PARTIALLY_SUPPORTED — new API/model vocabulary, but both levels satisfiable by API familiarity (CM-002); discriminates Profile D weakly |
| L2→L3 | *construct* a guard + ordering model (from analyze to build) | SUPPORTED — genuinely new capability (construction vs analysis) |
| L3→L4 | memory-ordering audit + anti-KCSAN-overtrust epistemics | PARTIALLY_SUPPORTED — real step up; confounder: prior LKMM background inflates without RfL competence (SCOPE_ERROR risk in scoring, CM-007) |
| L4→L5 | reviewed reusable policy | OPEN — conflates capability with governance maturity + artifact production (CM-015); a superb L4 engineer without policy-writing practice fails; a mediocre one with review access passes — capability vs task/access complexity |

### C047 (callback teardown)
| Boundary | New responsibility | Verdict |
|---|---|---|
| L0→L1 | perceive callback-after-free | SUPPORTED |
| L1→L2 | build refcounted wrapper + record owner | SUPPORTED — artifact construction, directly checkable |
| L2→L3 | complete teardown state machine | SUPPORTED — ordering design is new capability |
| L3→L4 | concurrent remove/ioctl race resolution with drain admission | SUPPORTED — strongest boundary in the model: the documented cancel/racing-enqueue caveat (S4) makes admission gating genuinely necessary, so this cannot be gamed by API knowledge (CM-010) |
| L4→L5 | reviewed subsystem-wide policy | OPEN — same governance conflation (CM-015) |

### C053 (pin initialization)
| Boundary | New responsibility | Verdict |
|---|---|---|
| L0→L1 | perceive address-instability failure | SUPPORTED |
| L1→L2 | in-place init + machine-checkable compile-fail artifact | SUPPORTED — most objective boundary in the model |
| L2→L3 | safe-API encoding + teardown model | PROVISIONAL — real step, but "safe API" is ambiguous (contract-level vs kernel-invariant, CM-013) and the L2→L3 jump bundles API machinery + design in one step |
| L3→L4 | partial-init unwind + allocator-lifetime audit | SUPPORTED — expert discriminator, distinct capability |
| L4→L5 | reviewed policy with ABI boundaries | OPEN — same conflation (CM-015) |

**Pattern finding (CM-015):** all three L4→L5 boundaries share one defect class — L5 requires a *reviewed* artifact, making the boundary depend on review infrastructure and reviewer calibration that do not exist in the frozen protocol (assessor observability NOT_OBSERVABLE_WITH_CURRENT_PROTOCOL). The L5 construct may still be a real capability; its current boundary condition conflates capability with governance access. Classification: LEVEL_BOUNDARY / OPEN.

**Second pattern (CM-016):** the cumulative rule forces one scale over distinct capability dimensions (builder, auditor, policy author). Profile G (review-strong, implementation-weak) cannot be placed sensibly above the implementation behaviors it fails. This is a deliberate, documented rubric choice (single cumulative scale), retained — but the audit records the construct restriction.

## Construct-validity probes (§13) — paper probes, NOT calibration

| case_id | competency | boundary | intended distinction | lower-level solution | upper-level solution | confounders | oracle | result |
|---|---|---|---|---|---|---|---|---|
| P-C034-L1L2 | C034 | L1/L2 | hazard ID vs traversal+grace explanation | read schedule, name race | explain traversal + which grace period covers removal | API familiarity; C-kernel experience | written analysis | DISCRIMINATIVE_WEAK (CM-002) |
| P-C034-L2L3 | C034 | L2/L3 | explain vs construct guard+ordering | paraphrase list rules | working guard design + remove/grace/free model | Rust fluency | artifact review | DISCRIMINATIVE |
| P-C034-L3L4 | C034 | L3/L4 | design vs adversarial ordering audit | correct happy-path ordering | interleaving audit with LKMM reasoning; rejects KCSAN-as-proof | LKMM background | audit review | DISCRIMINATIVE |
| P-C034-L4L5 | C034 | L4/L5 | audit vs reviewed policy | correct audit | reviewed subsystem policy artifact | review access; writing skill | review artifact | BOUNDARY_NOT_DISCRIMINATIVE_WITHOUT_REVIEW_INFRASTRUCTURE |
| P-C047-L1L2 | C047 | L1/L2 | perceive vs wrapper construction | name interleaving | refcounted wrapper + owner record | C experience (Profile C) | artifact | DISCRIMINATIVE |
| P-C047-L2L3 | C047 | L2/L3 | owner record vs full ordering machine | registration owner noted | unregister/callback/reference/free machine | workqueue familiarity | artifact | DISCRIMINATIVE |
| P-C047-L3L4 | C047 | L3/L4 | sequential machine vs concurrent race resolution | correct single-threaded ordering | drain admission + ioctl race resolution | prior race-fix war stories | schedule resolution | DISCRIMINATIVE_STRONG (CM-010) |
| P-C047-L4L5 | C047 | L4/L5 | race resolution vs reviewed policy | correct concurrent design | reviewed lifecycle policy | review access | review artifact | BOUNDARY_NOT_DISCRIMINATIVE_WITHOUT_REVIEW_INFRASTRUCTURE |
| P-C053-L1L2 | C053 | L1/L2 | perceive vs in-place init demo | name address-change failure | in-place init + rustc-rejected move artifact | Rust fluency | artifact + re-runnable rustc | DISCRIMINATIVE_STRONG |
| P-C053-L2L3 | C053 | L2/L3 | local demo vs safe-API+teardown encoding | compile-fail demo | pinned-lifetime API + teardown model | API churn (CM-020) | artifact | DISCRIMINATIVE_MODERATE (ambiguity CM-013) |
| P-C053-L3L4 | C053 | L3/L4 | encoding vs unwind/allocator audit | correct happy-path init | partial-init unwind audit + allocator contract | init-machinery fluency | audit review | DISCRIMINATIVE |
| P-C053-L4L5 | C053 | L4/L5 | audit vs reviewed policy | correct audit | reviewed reusable policy | review access | review artifact | BOUNDARY_NOT_DISCRIMINATIVE_WITHOUT_REVIEW_INFRASTRUCTURE |

Probe verdicts: 8/12 boundaries clearly discriminative on paper; 3 weak-with-known-confounders; all three L4/L5 boundaries not currently discriminative **under the frozen protocol** because the distinguishing evidence (independent calibrated review) is unavailable. No empirical agreement percentage is claimed; these are construct hypotheses for calibration design.
