# RFL-QA v1.1-alpha — Adversarial Validation Audit

**Disposition: BLOCKED. The 119-test result reproduces, but the broader frozen assurance claims do not all hold.**

This audit inspected and attacked the existing implementation without modifying its source, schemas, competencies, fixtures, vocabulary, or previous execution evidence. All new artifacts are under `evidence/adversarial-audit/`. No release, tag, or human calibration was created. Recommendations below are not implemented policy changes.

## 1. Established repository and evidence state

| Item | Observed result |
|---|---|
| Local branch | `arena/01a0dfcc-rfl-qa` |
| Local HEAD during execution | `33e4d95f835ecfd42830087dcd2772bb6cc8c216` |
| Initial working tree | **Not clean**: modified README and untracked implementation, docs, and evidence files |
| Fetched remote branch | `e4f1611c245d5c001d29b5c4477dee088c3d7867` |
| Ancestry | Local HEAD is an ancestor of remote HEAD; remote HEAD is not an ancestor of local HEAD. This is a behind checkout plus uncommitted content, not two divergent committed tips. |
| Claimed source `993cf96` | Unresolvable after fetching full history; GitHub commit API returns HTTP 422 |
| Claimed evidence `50512a3` | Unresolvable after fetching full history; GitHub commit API returns HTTP 422 |
| Actual published evidence history | Evidence files first appear in `1bfcdf918e9b476a81ad3ed5960e56b107cbf9c3` |
| Remote/content comparison | All **112** files in the remote branch match the local pre-audit file bytes |
| Previous source manifest | All **74** listed source files match; manifest hash matches the ledger |
| Previous command logs | All **15** recorded log hashes match |
| Tags/releases | No remote tags returned; GitHub releases API returned an empty list |

Exact command observations and individual exit codes are retained in `commands.log` and `evidence-chain.json`. The initial clone was shallow; the missing commit checks were repeated after unshallowing and fetching the session branch. Neither a branch switch nor a source reset was performed.

The previous ledger is **self-authored, internally consistent historical evidence**, not independently authenticated historical command execution. Matching a log checksum proves content identity, not that its claimed command ran. Nevertheless, a new pinned-environment run reproduces the old test count and **all three stored qualification outputs byte-for-byte**, providing fresh execution support for those bounded results. Missing commit references do not establish that the old execution never happened; they leave its claimed commit chain unresolved (AUD-001).

## 2. Execution environment and first reproduction

- Python **3.11.2**, Linux x86_64; exact platform and relevant environment variables in `environment.yaml`.
- A fresh `.venv` was created and **every version in `requirements.txt` installed as pinned**. `pip check` returned 0.
- Core versions: jsonschema **4.23.0**, PyYAML **6.0.2**, pytest **8.3.5**, rfc3339-validator **0.1.4**, six **1.17.0**. The complete transitive version list is retained.
- First untouched-fixture command: `.venv/bin/pytest -q`.
- Actual result: **119 passed in 5.42 seconds**, exit **0**, no warnings reported in captured output. Measured whole-process duration: **5.811 seconds**.
- `tools/validate.py --all` returned **0**.
- The full original gate runner was executed with a **new output directory**, `reproduced-release/`, rather than overwriting old evidence. It again reported the six machine checks PASS, synthetic calibration tests PASS, human calibration BLOCKED, and returned **1**.

`rfc3339-validator` is genuinely used by jsonschema's registered date-time checker in this environment. The audit inspected the checker and executed valid-date, invalid-date, and impossible-date cases; only the valid value conformed. No other Python/dependency versions were tested, and no cross-version compatibility or dependency vulnerability certification is claimed.

## 3. Fresh release matrix

The middle column is the **reproduced legacy test result**, not the final assurance judgment. The final column incorporates the counterexamples below.

| Gate / boundary | Reproduced existing checks | Fresh audit disposition |
|---|---|---|
| Schema | PASS | **FAIL** — inconsistent evidence and standalone/output validation gaps |
| Derivation | PASS | **FAIL** — required-oracle evidence omitted from ceiling; unsupported observations credited |
| Invariant | PASS | **FAIL** — caller-controlled criticality and inconsistent external support |
| Oracle | PASS | **FAIL** — safety predicates are not evaluated against artifacts/traces |
| Hard-gate | PASS | **FAIL** — critical Type-D veto can be disabled |
| Calibration | Synthetic comparison PASS; human component blocked | **BLOCKED** |
| Reproducibility | PASS | **PASS**, within the tested fixed-source/pinned-environment scope |
| Remote CI | GitHub API inspected | **FAIL**, not NOT_RUN |
| Human calibration | No independent human run performed | **NOT_RUN** |
| Kernel/compiler/sanitizer execution | Not executed | **NOT_RUN** |
| Criterion validity | No longitudinal outcome study | **NOT_ESTABLISHED** |

**Release: BLOCKED.** NOT_RUN and NOT_ESTABLISHED are not converted into test failures. `gate-results.yaml` records CLAIMED → OBSERVED → REPRODUCED separately from VERIFIED_WITHIN_EXECUTION_SCOPE. A reproduced legacy PASS does not verify a broader assurance property refuted by a counterexample.

## 4. Adversarial results and smallest counterexamples

The additional engine probe program executed **150 cases**: **139 expected boundaries held**, and **11 acceptance/counterexample observations** exposed defects or evidence limitations. The 11 include three variants of the same scope problem; they are not 11 independent defect classes. Other parser, hashing, process, and static probes are recorded separately rather than inflated into a pytest count.

`findings.yaml` contains **15 findings: 7 HIGH, 5 MEDIUM, 1 LOW, 2 INFORMATIONAL**, with the requested ID, SEVERITY, STATUS, LOCATION, CLAIM, OBSERVATION, EVIDENCE, IMPACT, and RECOMMENDED_ACTION fields, plus classification. Finding status PROVED refers only to the bounded observed counterexample; it does not change the qualification engine's frozen VERIFIED vocabulary or claim universal formal proof.

### Release-blocking implementation and schema defects

1. **AUD-002 — Criticality downgrade bypass.** D01 is critical in the normative catalog. The same OPEN D01 returns BLOCKED/REJECTED when `critical: true`, but PASS/PROVISIONAL after the dossier changes only that flag to false (with its assessor dossier digests rebound). The validator checks class and requiredness, not authoritative criticality. This is a direct bypass of a non-compensable veto, not compensation by L or E.

2. **AUD-003 — Required oracle evidence escapes the ceiling.** A required teardown check references OPEN `TEST` evidence. Marking the evidence optional and removing its separate invariant reference excludes it from `required_refs`. The engine returns **VERIFIED_WITHIN_SCOPE / VERIFIED ceiling**, even though the required oracle still depends on OPEN evidence. This was reproduced through the public CLI as well as the function API.

3. **AUD-004 — Configuration scope can be erased.** Explicit ARM64/DMA/NMI/non-RT additions, different competencies/tasks, and missing scope fields are rejected. But `environments: [x86_64]`, `[PREEMPT_RT=y]`, and `[CONFIG_RUST=y]` are accepted as subsets. Deleting a conjunctive configuration/architecture restriction is not necessarily a narrower qualification. Output faithfully copies the submitted scope; the gap is incomplete input scope, not formatter expansion. The environment-list whitelist/conjunction interpretation needs resolution, not silent inference.

4. **AUD-005 — Untested evidence can masquerade as support.** `method: not_tested`, `coverage.executed: 0`, and a statement that no assessment occurred are accepted when labeled OBSERVATION/VERIFIED. The record supports behavioral L3 and a verified decision. Strength validation enforces absence semantics in one direction but does not reject this contradictory method/strength pairing.

5. **AUD-006 — Critical VERIFIED assertion survives OPEN support.** A critical D01 label remains VERIFIED while its only source-audit evidence is OPEN. The aggregate ceiling drops to OPEN, but hard gates remain PASS and qualification PROVISIONAL instead of vetoing the unresolved critical contract.

### Oracle and evidence limitations

- **AUD-008:** The nine teardown states and all five interleavings are present as text. The code validates IDs, references and selected strength labels, then consumes submitted PASS/BLOCKED/NOT_RUN results. It does not evaluate `alive(reference) ⇒ object_alive` or the final-free predicate against a trace. An explicitly contradictory free-with-live-callback statement with PASS labels still qualifies. Replacing the model with `[FREE, ACTIVE]` and `looks correct` in an isolated catalog copy is also accepted. This tests trusted-catalog validation; it is not an exploit that writes to trusted production files.
- **AUD-007:** Type-D Boolean/empty/malformed/dangling/wrong-method evidence is rejected, but an unrelated source audit passes if the reference and method match. Structural validity does not establish relevance, authenticity or truth. This is a documented human-review boundary, not a claim that the engine should understand arbitrary prose automatically.
- **AUD-012:** LAB-001 and LAB-002 have generic callback unregister/free text and `fixture://` labels, not a concrete self-referential initializer, RCU implementation/flavor contract, compiler output or actual external audit. They exercise the intended answer labels but do not establish independent classification of substantive artifacts. LAB-003's state strings do not themselves establish runtime safety.

### Additional validator/report/parser findings

- **AUD-009:** `report.py` does not mutate genuine input states. However, changing a PARTIALLY_VERIFIED result's decision/ceiling to VERIFIED_WITHIN_SCOPE/VERIFIED and recomputing the public checksum yields an accepted, internally contradictory report. This is a missing cross-field validation check; it is **not** evidence that a checksum was ever an authentication mechanism or that formatting itself upgrades a decision.
- **AUD-010:** Standalone D+VERIFIED invariants without any evidence pass `validate_record`; the equivalent dossier-contained record is rejected. The positive catalog gate uses the shallow path.
- **AUD-011:** 1500 nested JSON/YAML arrays produce an uncaught RecursionError and traceback. They emit no qualification, but parser depth/resource bounds are absent. No arbitrary code execution or service exploit was demonstrated.

### Minimal reproduction commands

After installing the pinned requirements:

```bash
# Existing suite still passes; this is not a regression-suite replacement.
.venv/bin/pytest -q

# Exits 1 because the audit deliberately finds violated boundaries.
.venv/bin/python evidence/adversarial-audit/probe_engine.py

# These currently exit 0 and emit the incorrect/insufficiently bounded result.
.venv/bin/python tools/derive.py evidence/adversarial-audit/counterexamples/critical-open-declared-noncritical.json
.venv/bin/python tools/derive.py evidence/adversarial-audit/counterexamples/oracle-open-evidence-not-in-ceiling.json
.venv/bin/python tools/derive.py evidence/adversarial-audit/counterexamples/not-tested-as-observation.json
```

The modified dossiers and observed result records are retained in `counterexamples/`. The authoritative source and original positive/poisoned fixtures were not modified. Remediation should target these exact boundaries and add regressions, not add competencies or change the qualification axes.

## 5. Boundaries that held in the executed population

### Evidence tier versus capability

The seven requested cases produced the independently supported levels:

| Input | Supported capability |
|---|---|
| E5 + no demonstrated behavior (explicit failed L1 observation) | L0 |
| E4 + L1 behaviors | L1 |
| E4 + L2 behaviors | L2 |
| E3 + L2 behaviors | L2 |
| E2 + L3 behaviors | L3 |
| E1 + L4 behaviors | L4 |
| E0 + L5 behaviors | L5, but decision REJECTED under the separate E0 eligibility rule |

An additional **36-case level/tier cross-product** held the behavioral level fixed while varying all six tiers. Full-path source review found no tier read in `capability()`. Tier participates in consistency/divergence checks and E0 eligibility, not supported-level computation. An inconsistent assessor tier can halt a qualification; that is not capability promotion.

Required behavior failures cap the corresponding level. Invented, cross-competency and duplicate behavior IDs were rejected at schema or semantic validation. Each alpha rubric has only one behavior per level, so incomplete L3 means the sole L3 behavior is not demonstrated; finer-grained partial completion is not machine-encoded. No unperformed partial-completion experiment is claimed.

### Status and strength separation

A+PROVISIONAL, B+VERIFIED, C+PARTIALLY_VERIFIED and D+OPEN remain separately represented. Direct weakest-required-invariant cases yield the expected PROVISIONAL/OPEN ceilings. Under current `SPEC.md`, a noncritical B+OPEN finding yields PROVISIONAL, while an unresolved critical D assumption must veto. This audit did not invent a rule that every OPEN invariant must reject.

KCSAN represented as PROOF is rejected, even with a trillion declared executions. Legal OBSERVATION and COVERAGE labels remain distinct. All ten structured defect types vetoed maximal L5/E5 inputs, including UAF, double-free, race, deadlock, prohibited sleep, callback-after-free and required ABI break. **Those positive controls do not negate the criticality downgrade bypass.**

### Reporting and calibration

Genuine report records for every epistemic state remained byte-unchanged after presentation. Five separate assessor disagreements—capability, tier, invariant class, epistemic status, hard gate—were preserved and halted automatic qualification without averaging. Synthetic source fixtures and generated reports explicitly remain synthetic. Distinct IDs and `independent: true` cannot prove human independence; the release gate did not claim otherwise.

All seven frozen outcome classification values are preserved as explicit inputs. There is no automatic downstream-bug-to-false-positive classifier. `VALIDATED_WITHIN_SCOPE` remains potentially misleading when associated with an out-of-scope defect; AUD-013 records the existing governance issue without renaming it.

## 6. Determinism and canonical hashing

Beyond rerunning the existing 100-derivation test, this audit ran **16 new CLI processes**: eight variants spanning hash seeds `0`, `1`, `42`, `random`, repository/temporary working directories, locales `C`/`C.utf8`, and UTC/Tunis/Honolulu timezones, plus eight concurrent processes with distinct seeds. All exited 0 and produced byte-identical qualification JSON. JSON, ordinary YAML, reversed YAML mapping order and benign YAML anchors also produced identical hashes and bytes.

Capability, scope and epistemic changes alter the assessment hash. Explicit input timestamp and limitation-text changes also alter it, while leaving the decision/signature unchanged where appropriate. **This is intentional under the documented whole-record hash**, not a clock-dependent decision. There is no generated UUID/current-time read in derivation. Array order is significant, as documented; numeric encodings `1` and `1.0` also yield different record hashes despite schema integer compatibility. The encoding is sorted-key Python JSON, not a claim of universal semantic normalization or RFC canonicalization.

The hash covers all output fields except `assessment_hash`, including raw assessments, explicit timestamp, findings, scope, limitations and source digests. It is content addressing, not an authenticated signature. Dependency versions were held fixed; behavior under different versions is unknown.

## 7. YAML/JSON and trust-boundary audit

- Duplicate JSON/YAML keys are rejected.
- YAML Python-object tags are rejected by the SafeLoader-derived loader; the tested recursive alias is rejected, benign aliases are accepted.
- YAML dates remain strings. YAML 1.1 `ON` **does load as Boolean true**, but string/enum validation rejects it as an epistemic status; it does not silently enter derivation as a valid status. Nulls, wrong scalar types and unknown properties/enums were rejected in the tested records.
- Deep recursion remains an availability gap (AUD-011).
- Static review of `tools/` found no application `eval`, `exec`, `pickle`, `shell=True`, executable dynamic import, random/UUID source or derivation-time network call. Schema identifiers resolve through the local registry.
- Catalog/schema discovery uses sorted filesystem globs relative to the tool's source root. Reproduction therefore depends on the fixed catalog/source bundle, not the dossier alone. Those files are a trusted input boundary and are hashed in the evidence manifests.
- Subprocess execution is confined to the release runner with argument arrays and fixed commands. Wall time and GitHub environment metadata affect the execution ledger, not qualification derivation. The runner has no internal subprocess timeout; this audit's recorder applied timeouts.

This is a bounded static/dynamic audit, not a security certification or dependency-vulnerability assessment. `static-review.json` retains reviewed imports, call sites, line locations, source hashes and all evidence-tier-related derivation sites.

## 8. Remote CI: observed execution, unavailable raw logs

GitHub reports two completed runs at `e4f1611`:

- https://github.com/Abdus2023/rfl-qa/actions/runs/36280520784
- https://github.com/Abdus2023/rfl-qa/actions/runs/36280518710

Both conclude **failure**. API step records show successful dependency installation, schema validation, automated tests and CLI derivation/reporting, followed by failure at the full procedural release gate and successful evidence upload. The workflow declares Python 3.11, installs the pinned requirements, runs those commands, then the gate runner; the latter includes the repeated-derivation tests and deliberately returns nonzero while human calibration is missing.

Full logs could not be downloaded: both the run-log and job-log endpoints ended with EOF. The API result is execution evidence, unlike mere workflow text, but it does not expose the exact remote test count, installed Python patch version or failure stdout here. Local reproduction corroborates a procedural block, not a remote pytest failure. Signed download URLs in the audit error logs are redacted; the command, exit status and EOF are retained. No authentication credentials were collected.

## 9. Answers to the required disposition questions

1. **Does it satisfy the frozen alpha specification?** Not fully: the reproduced counterexamples violate hard-gate, required-evidence, scope-completeness and oracle-evaluation claims.
2. **Are all seven gates executable?** Six machine gate commands run; the seventh includes an unperformed human procedure represented by a hardcoded BLOCKED status. Synthetic comparison is executable, human reliability is not demonstrated.
3. **Can capability leak from evidence tier?** No promotion found in the seven requested cases, 36-case sweep or full-path review. Other evidence-consistency weaknesses exist, but are not E→L mappings.
4. **Can scope leak?** Explicit expansion and missing whole fields reject; deletion of environment restrictions is accepted and can remove necessary bounds.
5. **Can epistemic status be silently upgraded?** Counts/time/report formatting did not upgrade genuine records. Omitting required oracle evidence from the ceiling can nevertheless allow an unjustified VERIFIED decision.
6. **Can hard gates be bypassed?** Yes: caller-controlled criticality bypasses the unresolved Type-D veto. Recorded defect enums still veto correctly.
7. **Can malformed evidence enter derivation?** Yes, semantically contradictory method/strength and critical-support records can pass. Ordinary structural corruption generally rejects.
8. **Is hashing deterministic?** Yes within the tested fixed-source, pinned-dependency and supported representation scope. It is neither authentication nor full semantic normalization.
9. **Are synthetic assessors distinguished?** Yes in the shipped fixtures/reports and procedural block. Actual independence is unverified and was not performed.
10. **Is old execution evidence reproducible?** The 119-test result and three exact outputs are freshly reproduced; historical commit linkage/authenticity remains unresolved.
11. **Does remote CI execute?** Yes; GitHub API records two failed completed runs. Raw logs were unavailable, so their detailed contents are not claimed.
12. **What remains unknown?** Real assessor reliability, real artifact adequacy/authenticity, kernel/compiler/sanitizer behavior, longitudinal criterion validity, other environments/versions, and the unavailable historical commit chain/remote raw logs.

## 10. Evidence files and preservation

Required deliverables: `REPORT.md`, `findings.yaml`, `environment.yaml`, `commands.log`, `gate-results.yaml`, and `hash-manifest.yaml`. Supporting evidence includes exact counterexample dossiers/results, seven requested tier fixtures, structured probe results, static review, original-chain inspection and a separate full-gate reproduction directory.

`commands.log` is newline-delimited JSON recording command arguments, working directory, relevant environment overrides, stdout/stderr, actual exit code, start time and duration. Selected signed log-download URLs are redacted. The manifest hashes the audit files (excluding itself to avoid self-reference), audited source files and preserved prior execution files. Hashes establish content identity only; this audit's own evidence is not self-authenticating or a substitute for independent human review.

**No implementation changes were made, so no implementation CHANGELOG entry was added. Previous evidence remains untouched. The release remains BLOCKED.**
