# Adversarial remediation report — RELEASE BLOCKED

**No evidence → no VERIFIED claim. Software consistency is not human reliability or criterion validity.**

Executed source/test revision: `b0582f61ae4fad99c02a262c9b27475330bd018e` on `arena/01a0dfcc-rfl-qa`. Implementation commit: `3651ffb`; baseline: `e4f1611`. Rules: **1.1-alpha.2**. Later evidence-only receipt commits do not assert a different source execution. Prior `evidence/adversarial-audit/` and `evidence/execution/` were preserved (97 files verified against the pre-remediation SHA256 snapshot).

## Outcome

- **564 passed, 0 failed, 0 skipped**: all **119 original tests unchanged**, plus **445 new regressions**. The unchanged baseline was 119/119 before patching. Original-only rerun: 119/119. Final fresh procedural runner independently reports 564/564 and release BLOCKED.
- Final schema/reference validation PASS. All three canonical dossiers derived and reported successfully. Sixteen final independent CLI executions produced identical bytes/hashes under varied hash seeds, directories, locale, timezone and concurrency. All remain synthetic qualifications, not human/kernel evidence.
- **Eight findings locally corrected, successful whole-workflow CI prerequisite outstanding** (`FIXED_LOCALLY_CI_PENDING`). **AUD-007 and AUD-008 remain OPEN**: consistent fabricated bindings and safe snapshots can coexist with unrelated or contradictory prose. The bounded evaluator is a partial correction, not artifact authentication.
- Actual final CI workflows both **FAIL** at the procedural release-gate step. Dependency, schema, automated tests, CLI and artifact-upload steps are **success** per GitHub job API. Logs/artifact download EOF prevents independent confirmation of remote procedural details; local human-calibration blockage is not substituted for the missing remote ledger.
- **No finding is FIXED_AND_RETESTED; no VERIFIED fix or release eligibility is claimed.** No release/tag was created.

## Baseline → reproduction → contract → patch

The original source/schema suite was executed unchanged. All 12 saved counterexample inputs (including injected bad catalog and forged report) reproduced acceptance before implementation changes; see `pre-fix-counterexamples.json` and command receipts. Seven contracts were written in `regression-contracts.md` before patching. Available published files were byte-checked before aligning the local index/HEAD to the already published e4f1611 history; no force push or reconstructed commits were used. Historical 993cf96/50512a3 remain UNRESOLVED_HISTORICAL_COMMIT.

Minimal production changes enforce authoritative criticality, complete scope, material support closure, method/strength compatibility, explicit observation/result provenance, fixed teardown predicates, qualification rederivation, standalone invariant rules and bounded strict parsing. Existing canonical/synthetic fixtures were explicitly migrated; arbitrary old inputs receive no defaults or repairs. Frozen axes, statuses, three labs/competencies and release gates remain unchanged. SPEC.md and CHANGELOG.md document the stricter alpha profile.

AUD-011 supplemental baseline reproduction was performed **after** implementation using the exact recorded baseline `tools/common.py` in an isolated temporary directory. Old JSON/YAML depth1500 raises RecursionError; patched CLI rejects cleanly. This is evidence about baseline-version behavior, not a falsely backdated command.

## Counterexample replay and positive controls

All 12 frozen old inputs now reject, mostly for missing required provenance. **That alone is not a semantic fix.** Current-schema replay adds explicitly synthetic template observations and bindings while retaining old fields; it is NOT a transcription/authentication of narrative source facts:

- Criticality downgrade; VERIFIED external invariant with OPEN support; not_tested-as-observation; and all three omitted environment attacks: reject at their intended semantic boundaries.
- Required oracle support with OPEN status and optional flag: accepts only as **PROVISIONAL / OPEN**, never VERIFIED. This is the expected conservative result, not an input-format rejection requirement.
- Unrelated external audit and contradictory teardown prose paired with safe fabricated snapshots: **still accepted**. These are retained as OPEN counterexamples, not hidden behind old-schema rejection.
- Explicitly transcribing the original `FREE(target)` with possible callback/live reference into the bounded trace causes **BLOCKED / REJECTED / signature BLOCKED**. Unsafe traces fail regardless of submitted PASS/BLOCKED; the same safe trace has the same derived result for both labels, while a submitted BLOCKED remains a separate conservative veto.
- Bad state-model catalog, standalone D VERIFIED/no support and current-format rehashed report contradiction reject in dedicated regressions.

Controls include all canonical derive/report pipelines, safe modeled trace → DERIVED_RESULT/PASS, exact/permuted scope, catalog-consistent criticality, compatible method/strength pairs, valid standalone records, and complete VERIFIED support closure. Tests never interpret these synthetic positive controls as real human qualifications.

## Regression matrix

| Contract | Finding | Result | Executed boundary |
|---|---|---|---|
| HG-01 | AUD-002 | PASS | Catalog true/false, upgrade/downgrade, missing metadata, identity and assessor downgrade |
| HG-02 | AUD-004 | PASS | Exact/reordered scope; omitted environment/task; unsupported additions/exclusions/duplicates |
| HG-03 | AUD-003 | PASS | Five epistemic states; oracle, behavioral and assessor closure independent of required flag |
| HG-04 | AUD-005 | PASS | 40 method/strength combinations; no not_tested observations; positive proof/coverage controls |
| HG-05 | AUD-003 | PASS | Every canonical check x remove/unrelated/OPEN/absence/changed-strength/BLOCKED |
| HG-06 | AUD-008 | FAIL | Structured result-label tests PASS; narrative artifact authenticity/provenance completeness remains unresolved |
| HG-07 | AUD-008 | PASS | Bounded safe/unsafe/empty/incomplete/duplicate/reordered lifecycle evaluations; no real kernel execution |

The suite additionally retains seven specified E/L pairs plus all 36 pairs, A/B/C/D × VERIFIED/OPEN, all ten hard-gate classes at L5/E5/VERIFIED and assessor agreement, schema/format/alias/numeric attacks and hash sensitivity/equivalence tests. Every generated test case is listed in `regression-results.yaml`; actual JUnit receipts are retained. No xfail, skip or original test weakening was used. Six additional exact-limit/over-limit parser controls (2 MB, depth 64, 100000 nodes) were executed locally by `verify_evidence.py`; they are recorded separately in `parser-boundary-results.json`, not included in the 564 pytest count or claimed as remote CI tests.

Earlier failed runs remain in the log: diagnostic-order mismatch (118/119), a no-op PROOF→PROOF mutation (522/523), and a new test reading the evidence list as a dict (554/564). Those test/diagnostic issues were corrected without weakening intended failure oracles, then full suites rerun. The final 564-test suite is green.

## Canonical outputs and determinism

| Dossier | Decision | Ceiling | Assessment hash |
|---|---|---|---|
| 001-pin-init | PROVISIONAL | PARTIALLY_VERIFIED | `1c456ffcd29ddbdc8573fa61e66a9a803a204d874f26f0f05b57ea42b1faf656` |
| 002-rcu | PROVISIONAL | OPEN | `8dafc33f049205c6679f75959e48fa81882e75d4feaed537e012ce17877d1961` |
| 003-callback-teardown | PROVISIONAL | PARTIALLY_VERIFIED | `56325b9a7164d73282aefe9bb8307593429bb927331cba5acc86ed9e9bceb6c8` |

RCU's required absence-classification evidence now participates in closure, changing its ceiling to OPEN; its decision remains PROVISIONAL. Other canonical ceilings remain PARTIALLY_VERIFIED. Provenance fields/rules intentionally change output hashes. Hashes bind recorded timestamps/limitations and array order; presentation indentation/key order do not. No wall-clock value participates in derivation. Final deterministic results are in `determinism-results.json`; three reports and records in `outputs/`. The fresh procedural ledger is `procedural-final/ledger.yaml`.

## CI authority

- [pull_request run 36282488859](https://github.com/Abdus2023/rfl-qa/actions/runs/36282488859), head `b0582f61ae4fad99c02a262c9b27475330bd018e`, completed **failure**; job 108516876827.
- [push run 36282486359](https://github.com/Abdus2023/rfl-qa/actions/runs/36282486359), head `b0582f61ae4fad99c02a262c9b27475330bd018e`, completed **failure**; job 108516870448.

The workflow was inspected and left unchanged; see `workflow-review.md` and `ci-results.json`. API success on automated steps is real execution evidence, but is not a successful whole-workflow conclusion. Raw logs and uploaded artifacts could not be downloaded (EOF; actual nonzero exits recorded, signed URLs redacted). No exact remote test count, kernel run or detailed remote procedural cause is asserted. The successful-CI prerequisite for a VERIFIED fix remains outstanding; the prescribed pending disposition is used conservatively even though the current attempt has completed FAIL.

## Finding dispositions

| Finding | Disposition | Observation |
|---|---|---|
| AUD-001 | OPEN | UNRESOLVED_HISTORICAL_COMMIT: 993cf96/50512a3 remain unavailable after fetch. New receipts use available commits and content hashes; historical claims are not repaired. |
| AUD-002 | FIXED_LOCALLY_CI_PENDING | Catalog criticality equality and authoritative derivation reject original false downgrade and inconsistent catalog metadata. |
| AUD-003 | FIXED_LOCALLY_CI_PENDING | Closure includes optional-flagged material oracle/observation/assessor/behavior support. Original OPEN oracle support now produces PROVISIONAL/OPEN, not VERIFIED. |
| AUD-004 | FIXED_LOCALLY_CI_PENDING | Complete environment/task combinations and required exclusions enforced; all three original omission variants reject. |
| AUD-005 | FIXED_LOCALLY_CI_PENDING | Method/strength compatibility rejects not_tested OBSERVATION; dynamic methods require a nonempty executed population. |
| AUD-006 | FIXED_LOCALLY_CI_PENDING | VERIFIED external invariants reject unresolved external support, with explicit binding requirements. This is not source-document authentication. |
| AUD-007 | OPEN | Unrelated audit prose remains accepted when all declared bindings are fabricated consistently. Record bindings cannot establish source relevance or adequacy. |
| AUD-008 | OPEN | Partial correction: fixed bounded evaluator and ASSERTED_RESULT/DERIVED_RESULT provenance work for supplied structured traces; unsafe explicit transcription blocks. Contradictory prose paired with fabricated safe snapshots remains accepted. Full finding is NOT closed. |
| AUD-009 | FIXED_LOCALLY_CI_PENDING | Report validation recomputes qualification from retained input and rejects a rehashed contradictory decision. |
| AUD-010 | FIXED_LOCALLY_CI_PENDING | Standalone invariant validation applies context-free required evidence rules; original D VERIFIED without support rejects. |
| AUD-011 | FIXED_LOCALLY_CI_PENDING | Bounded parser rejects deep/recursive/ambiguous data with controlled Invalid errors. Supplemental baseline replay used exact e4f1611 common.py in isolation after patching; its old behavior was reproduced, not assumed. |
| AUD-012 | OPEN | Structured synthetic fixtures are more executable as models, but substantive candidate/kernel artifacts for labs 001/002 remain unestablished. No real kernel/compiler/sanitizer execution was performed. |
| AUD-013 | SPECIFICATION_FAILURE | Outcome scope terminology conflict remains unresolved. No silent enum rename or expanded outcome interpretation was introduced. |
| AUD-014 | OPEN | No independent human calibration, actual kernel execution or upstream criterion evidence was supplied or generated. Synthetic agreement does not satisfy these gates. |
| AUD-015 | EXTERNAL_FAILURE | Actual final CI runs/jobs observed: software steps succeed, overall workflows fail at procedural gate. Raw logs and artifact downloads return EOF. Successful whole-workflow CI is still absent; remote detailed failure cause is not independently confirmed. |

## Final gate matrix

| Gate | Status | Scope / executed evidence |
|---|---|---|
| Schema | PASS | Final --all and positive/negative schema regressions |
| Derivation | PASS | 564-test suite; all 3 canonical CLI pipelines |
| E→L separation | PASS | 7 required pairs plus exhaustive 36-pair sweep |
| Invariant enforcement | PASS | Authoritative catalog and external support structure; document adequacy remains OPEN |
| Scope enforcement | PASS | Both containment directions, exclusions, duplicates, order controls |
| Epistemic closure | PASS | All referenced material supports included; weakening cannot verify |
| Evidence-strength separation | PASS | Compatibility matrix and independent epistemic states |
| Oracle integrity | FAIL | Executed adapted narrative cases still accept fabricated consistently bound source facts (AUD-007/008) |
| Hard-gate veto | PASS | All 10 classes at L5/E5/VERIFIED and agreement: BLOCKED/REJECTED/BLOCKED |
| Teardown evaluation | PASS | Finite structured model only, not external artifact authenticity |
| Canonical hashing | PASS | Full-record binding; serialization/key order stable; semantic changes differ |
| Original regression suite | PASS | 119 unchanged tests; separately rerun and included in final suite |
| Adversarial regression suite | PASS | 445 additional tests; no skipped/xfail tests |
| Determinism | PASS | 16 final independent CLI processes, varied seed/CWD/locale/TZ/concurrency; key-order tests |
| Remote CI | FAIL | Both final workflows completed failure; schema/tests/CLI steps success; logs/artifacts unavailable |
| Human calibration | BLOCKED | NOT_RUN: no real independent dual-assessor exercise |
| Kernel execution | NOT_RUN | No kernel/compiler/KASAN/KCSAN/lockdep run |
| Criterion validity | NOT_ESTABLISHED | No upstream outcome validation |
| Release | BLOCKED | Open authenticity/self-attestation gaps plus human/kernel/criterion/CI prerequisites |

## Evidence and next boundary

`environment.yaml` records exact Python/OS/architecture/dependencies, source commit/branch and an allowlisted environment; `commands.log` and `command-records.jsonl` contain command, stdout, stderr and actual exit information. `hash-manifest.yaml` covers remediation evidence and qualification outputs, plus relevant source files; it explicitly excludes itself to avoid recursive hashing. `preserved-evidence.json` is the original immutability snapshot. Source AST/boundary review is in `trust-boundary-review.json`; it is not a security certification. Repeatable harnesses write only remediation output, never frozen prior evidence.

Next work must establish authentic, relevant observation/source artifacts and reconcile contradictory facts; obtain independent human calibration and real scoped kernel/compiler/sanitizer observations; resolve outcome scope terminology and historical provenance; and establish upstream criterion validity. A general evaluator or an NLP heuristic is not silently added to pretend those gaps are solved. Release remains BLOCKED even though the executed bounded software regressions pass.

The execution ledger is sealed before the evidence-only publication commit. That later administrative commit/push is represented by Git history, not recursively embedded into its own manifest. GitHub execution evidence above is explicitly for the source/test revision, not for any later evidence-only receipt commit.
