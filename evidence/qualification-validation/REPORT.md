# RFL-QA v1.1-alpha — Qualification-System Validation & Calibration Phase Report

Baseline: `459ec8b9836339537d2cbd995e73af0a330d69ff` (remote tip; verified after sandbox rehydration; sealed packages byte-intact).
Scope: measurement-system validation **preparation and honest state recording**. No calibration, agreement, kernel-execution, or criterion-validity evidence exists; none is manufactured.

## 1. The three separate claims (maintained throughout)

| Claim | Question | State | Why |
|---|---|---|---|
| Internal consistency | Does the implementation deterministically enforce its declared contracts? | Substantially evidenced | 653/653 tests, schema/derivation/invariant/oracle/hard-gate gates, CI run 36304213414 software steps success, AUD-007/008 FIXED_AND_RETESTED (prior cycles) |
| Calibration reliability | Do independent assessors applying the frozen rubric produce consistent assessments? | **NOT_RUN / NOT_ESTABLISHED** | No independent human assessors exist in this environment; agent-generated assessments are prohibited (GOVERNANCE.md, F-005) |
| Criterion validity | Does RFL-QA assessment relate to independently defined external outcomes? | **NOT_ESTABLISHED** | No external outcome data collected; study protocol frozen before any collection |

Neither of the latter two is inferred from the first.

## 2. Instrument freeze (§3)

`instrument.yaml`: 32 frozen files at commit `459ec8b` — SPEC.md, GOVERNANCE.md, `assessors/rubric.md`, `assessors/review-protocol.md`, `calibration/inter-rater.md`, 6 schemas, 4 competency catalogs, invariant taxonomy + A01/B01/C01/D01, 3 oracles, 3 laboratory task/oracle/expected-observation sets. Directory manifest digest: `8fbf31d89f7e8391…` (method recorded in the file). Freeze rules and the mid-round defect procedure (freeze → record defect → new instrument version → restart affected cases) are recorded in the manifest. Freezing the instrument prepares measurement; it is not itself calibration evidence.

## 3. Calibration case set (§4–§5)

`calibration/cases.yaml`: **16 frozen cases** (CS-001…CS-016) over the three frozen competencies only, each with id, competency_id, task, evidence_package, assessor-blind `expected_boundary` (+ derivation rationale), applicable invariants (A01–D01), applicable oracles (OR-PIN/OR-RCU/OR-CALLBACK), hard-gate conditions, and scoring contract (cumulative levels, unexecuted checks never PASS, safety veto wins, exact agreement for automatic alpha qualification, no averaging).

Classes: positive ×3 (CS-001, CS-002, CS-015), negative ×2 (CS-003, CS-004), boundary ×3 (CS-005 L2/L3, CS-006 L3/L4, CS-007 L4/L5), hard-gate ×4 (CS-008 callback-after-free, CS-009 critical-external-assumption, CS-010 data-race epistemics, CS-016 deadlock), evidence-quality ×2 (CS-011 tier cannot raise level; CS-012 unexecuted oracle cannot PASS), provenance ×2 (CS-013 AUD-007 contradiction; CS-014 AUD-008 unbound prose). Levels exercised: L0–L5 boundaries. Remaining hard-gate conditions (uaf, double_free, prohibited_sleep, ffi_lifetime, required_abi_break) are exercised through the frozen lab oracle schedules; `dma_ownership` is exclusion-only under frozen scope. Assessor-facing views strip `expected_boundary`/`boundary_derivation`.

## 4. Assessor independence & round status (§6, §9, §10)

Round protocol state: `FREEZE INSTRUMENT ✓ → PREPARE CASES ✓ → BLIND ASSESSOR A ✗ (NOT_RUN)`. `assessor-a.yaml` / `assessor-b.yaml` are submission templates with `round_status: NOT_RUN`; independence declarations are left **null** for humans to declare — agent-filled values would be fabricated calibration. Two failure conditions verifiably hold (fewer than required assessors; raw submissions missing) → calibration remains **NOT_RUN / NOT_ESTABLISHED / BLOCKED**. No assessment exists anywhere in this package.

## 5. Inter-rater agreement (§7)

`agreement.yaml`: cases assessed 0/16; assessors 0/2; all agreement metrics null; statistic NOT_RUN (any post-hoc statistic selection is forbidden; a single pair would be STATISTICALLY_INSUFFICIENT for generalized reliability regardless). Decision threshold recorded from frozen governance: **exact agreement required for automatic alpha qualification** (review-protocol step 5); general reliability threshold NOT_SPECIFIED — none invented. `disagreements.yaml`: empty, with the frozen category taxonomy and preservation rules for future rounds.

## 6. Kernel laboratory execution (§11–§14)

`kernel/execution.yaml`: per-lab frozen requirements (x86_64, CONFIG_RUST=y, PREEMPT_RT=y; arm64/dma/nmi excluded) extracted from the frozen lab specs; compile / runtime / sanitizer / formal-proof recorded as four **distinct NOT_RUN epistemic classes** per lab; full §13 binding schema (command/command_digest/environment/input/output/artifact digests) mandated for any future result; §14 negative-fixture plan (intentional UAF, race, callback-after-free, prohibited sleep, lifetime violation) prepared with true_positive/false_negative recording rules — all NOT_RUN. `kernel/artifacts.yaml`: empty; no artifact may be synthesized to fill it. **No kernel, compiler, or sanitizer execution occurred; none is claimed.**

## 7. Criterion validity (§15–§18)

`criterion/study-protocol.yaml`: frozen **before** any data collection — population, inclusion/exclusion, t0, 12-month outcome window, primary criterion (independent upstream acceptance ratio from public review records — never an RFL-QA-derived quantity), secondary criteria, 8 pre-identified confounders, missing-data policy, analysis plan (descriptive first; association only if N permits; no threshold fitting on the same dataset). `dataset-manifest.yaml`: NOT_COLLECTED, entry shape mandated. `analysis.yaml`: **NOT_ESTABLISHED / INSUFFICIENT_EVIDENCE**, with the forbidden-inference list recorded.

## 8. Reproducibility (§23)

Executed after all measurement preparation: **10 independent derivation+report processes** (PYTHONHASHSEED 0/1/2/7/random, TZ UTC and Asia/Tunis, LC_ALL C and C.UTF-8) across all three canonical pipelines. repetitions: 10 derivation+report process pairs (+1 report-only re-run); variations: hash seed / timezone / locale; **mismatches: 0**; result: **11/11 comparisons byte-identical** to the sealed `evidence/aud-007-008/procedural/` outputs. The measurement package is evidence-directory-only and cannot alter qualification outputs; `validate.py --all` re-run PASS. (A transient harness index-arithmetic error in the first comparison loop produced a false mismatch flag; it referenced nonexistent files and was redone cleanly — both invocations are preserved in commands.log.)

## 9. Release-gate status matrix (§21)

| Dimension | State |
|---|---|
| Software gates | PASS (653/653 local at 459ec8b; CI run 36304213414 software steps success) |
| Adversarial findings | AUD-007 FIXED_AND_RETESTED; AUD-008 FIXED_AND_RETESTED (not reopened; no new counterexample) |
| Current-source CI | EXECUTED / OBSERVED — software gates PASS; procedural gate BLOCKED by design; log+artifact content UNCONFIRMED (EOF) |
| Human calibration | **NOT_RUN / BLOCKED** |
| Inter-rater agreement | **NOT_RUN** (OBSERVED only after real submissions) |
| Kernel execution | **NOT_RUN** |
| Criterion validity | **NOT_ESTABLISHED** |
| Release | **BLOCKED** |

No dimension compensates for another. Release blockers (§22) holding: human calibration NOT_RUN; kernel execution NOT_RUN; criterion validity NOT_ESTABLISHED; CI evidence insufficient for release-grade claims (log/artifact content UNCONFIRMED). No v1.1-alpha tag or release artifact exists.

## 10. Final qualification matrix (§26)

| Claim | Status | Evidence |
|---|---|---|
| Contract implementation | VERIFIED (implementation level) | 653/653 tests at 459ec8b; CI 36304213414 software steps; sealed package |
| AUD-007 | FIXED_AND_RETESTED | sealed replay 15/15 + controls; 89 regressions; current-source CI |
| AUD-008 | FIXED_AND_RETESTED | sealed P1–P10 receipts; 89 regressions; current-source CI |
| Deterministic derivation | VERIFIED_WITHIN_SCOPE | 11/11 byte-identical processes this phase; sealed 16+16 experiment |
| Human calibration | NOT_RUN | assessor-a/b.yaml; failure conditions recorded |
| Inter-rater reliability | NOT_RUN | agreement.yaml |
| Kernel laboratory execution | NOT_RUN | kernel/execution.yaml (requirements frozen; no environment) |
| Dynamic-analysis observations | NOT_RUN (vocabulary frozen: OBSERVATION/COVERAGE/PROOF/ABSENCE_OF_EVIDENCE) | kernel/execution.yaml epistemic fields |
| Criterion validity | NOT_ESTABLISHED | criterion/analysis.yaml; protocol frozen, data absent |
| Measurement validity | NOT_ESTABLISHED | synthesis: requires calibration reliability + external validity evidence; internal consistency alone is insufficient |
| Release eligibility | **BLOCKED** | explicit release policy: multiple unresolved mandatory prerequisites |

The final row applies the explicit frozen release policy (GOVERNANCE.md review/release section; release_gates.py mandatory BLOCKED), not intuition over the rows above.

## 11. Integrity & publication (§24–§25)

- No historical evidence modified: `evidence/aud-007-008/` seal verify PASS at `459ec8b`; this phase writes only `evidence/qualification-validation/`.
- No hidden source changes: implementation untouched (evidence-directory-only delta).
- No test weakening, no release tag, no force push, no silent adjudication, no circular criterion, no fabricated calibration, no inferred kernel execution, no inferred validity.
- Commits: instrument+calibration freeze; kernel record; criterion protocol; phase report — pushed normally to `arena/01a0dfcc-rfl-qa`. Exact publication SHA recorded in the post-push publication note in the final cycle message (hash-manifest excludes itself).
- Working tree clean at publication.

## 12. Limitations

- Everything in this package is preparation: frozen instrument, designed cases, protocols, and honest NOT_RUN/NOT_ESTABLISHED states. It contains **zero** calibration, agreement, kernel-execution, or criterion evidence.
- Case expected boundaries are design-time derivations from the frozen catalogs; if a real round reveals a boundary defect, the §3 defect procedure applies (new instrument version; affected cases restarted).
- This receipt does not strengthen any prior CI claim; CI log/artifact content remains UNCONFIRMED (EOF) from earlier cycles.
