# RFL-QA v1.1-alpha — executable slice

**Status: release candidate implementation; NOT a validated measurement system.**
Only C047 (callback teardown), C053 (pin-init), C034 (RCU) and their three meta-labs are implemented. Existing design documents remain historical inputs, not evidence that software or calibration ran.

## Run

Python 3.11; no kernel, network service, GPU, database or Rust compiler required for these **measurement-fixture** tests.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/validate.py --all
python tools/derive.py dossiers/examples/003-callback-teardown.json > qualification.json
python tools/report.py qualification.json > qualification.md
pytest -q
python tools/release_gates.py
```

The last command writes actual local command evidence to `evidence/execution/` and exits nonzero while mandatory human calibration remains unavailable. CI machine checks are separate from release authorization; a green CI job cannot authorize a release without the procedural gate. Root-level output filenames above are optional scratch outputs, not required source artifacts.

## Frozen axes

| Axis | Values |
|---|---|
| Capability | L0–L5, from observable behaviors only |
| Evidence tier | E0–E5, from the recorded artifact assessment, never converted into L |
| Invariant class | A compiler / B API / C runtime / D external |
| Epistemic status | VERIFIED / PARTIALLY_VERIFIED / PROVISIONAL / OPEN / BLOCKED |
| Evidence strength | PROOF / OBSERVATION / COVERAGE / ABSENCE_OF_EVIDENCE |
| Hard gate | PASS / BLOCKED |
| Decision | PROVISIONAL / VERIFIED_WITHIN_SCOPE / REJECTED |

**No evidence → no verified claim. No scope → no extrapolation. No behavioral trail → no capability level. No oracle → no meaningful test. No explicit assumption → no trust boundary. No teardown model → no lifetime claim. Hard gates are non-compensable. No silent epistemic upgrade. No calibration → no system validity.**

## Input, validation, and derivation contract

The five JSON Schemas use Draft 2020-12 and fixed HTTPS `$id`s, resolved **locally**, without fetching URLs. `claim.schema.json` validates a complete dossier and has supporting definitions for independent assessment, outcome, calibration-case, and scope records. Oracle task and observation templates are definitions in `oracle.schema.json`; taxonomy is a definition in `invariant.schema.json`. `competency/_schema.yaml` is JSON Schema expressed in YAML.

`validate.py --all` checks normative catalog records, examples, templates and positive/calibration fixtures. Poisoned fixtures are intentionally excluded from this positive gate: the tests validate their explicit expected rejection, capping or veto. JSON/YAML duplicate keys, unknown fields, unknown references, invalid IDs, missing scopes, unsupported environments, missing behavior observations, duplicate assessor identities and incomplete oracle check coverage fail. YAML dates remain strings and must pass format validation. Required scopes have one competency in alpha; there is no cross-domain aggregation or extrapolation.

The engine preserves the demonstration and raw assessor records rather than using assessor labels as qualification results. Each assessment binds to the SHA-256 of the same raw dossier (everything except the assessments array). Assessors supply distinct identities, an explicit independence declaration, behavior observations with evidence references, evidence tier, invariant findings, and hard gates. These declarations do **not** prove human independence.

Capability computation cumulatively requires the behavior matrix entries from L1 through Lx. Failed required behaviors or missing supported observations cap the result. References to absent/OPEN/BLOCKED evidence cannot demonstrate behavior. Neither artifact tier nor the assessor's claimed level enters the level-selection function. A claimed L4 with only L2 behaviors produces L2, not an inferred L4.

For automatic qualification the two raw assessments must agree on claimed level, supported level, behavior findings, evidence tier, invariant findings and hard gates. Discrepancies with the shared dossier also halt automatic qualification. Raw evidence-reference lists need not be identical. There is no averaging. A disagreement record has `capability: null`, `AWAITING_ADJUDICATION`, an OPEN event and a PROVISIONAL decision unless a hard veto takes precedence. The initial `artifact_ambiguity` event describes conflicting records, not the cause; a human must establish cause under the review protocol. Automatic derivation never adjudicates.

The epistemic ceiling is the weakest required finding in this order (strongest first):
`VERIFIED > PARTIALLY_VERIFIED > PROVISIONAL > OPEN > BLOCKED`.
It includes required invariant statuses (including both assessors), explicit required evidence, evidence referenced by required invariants and behavioral evidence. Excluded NMI absence remains recorded but is not required. Counts, time, tier, and presentation cannot change this ceiling. New assessment findings are necessary for changes.

A VERIFIED Type-D invariant requires a nonempty, structured external-evidence record linked to a real record in the dossier: matching source-audit/documentation/contract/specification method, explicit description and participating assessor. Schema validation is not authentication of the referenced document or its scientific sufficiency. A critical Type-D assumption not VERIFIED vetoes qualification, including PROVISIONAL and OPEN assumptions.

Dynamic tools cannot use PROOF strength. Each strength has a distinct `establishes` value. Free-text statements and artifact URIs are preserved for assessors; the engine does not claim to establish the truth of prose or parse real sanitizer logs. Observed defects must be recorded in structured `detected_defects`/hard-gate findings; any such record vetoes the result even if the dossier summary mistakenly says PASS. All ten frozen defect types are recognized. Required oracle BLOCKED results veto; NOT_RUN results prevent a verified decision.

Decision precedence:
1. Any recorded/derived safety veto → hard gate BLOCKED, decision REJECTED, signature BLOCKED.
2. BLOCKED epistemic ceiling or E0 primary evidence → REJECTED (not a fabricated safety defect).
3. Any assessor divergence → halt automatic qualification; preserve an OPEN event.
4. Only a VERIFIED ceiling, supported non-L0 capability and completed oracles allow VERIFIED_WITHIN_SCOPE.
5. Otherwise → PROVISIONAL. Scope and exclusions are copied exactly into the decision.

A valid rejected decision is valid output (`derive.py` exits 0); malformed/inconsistent input exits 1. Release tests assert decision contents, not merely command success.

## Canonical record and hash

Canonical encoding is UTF-8 JSON with sorted object keys, compact separators, Unicode preserved and no NaN. Array order is significant. SHA-256 covers **every output field except `assessment_hash` itself**, including the explicit input timestamp, raw assessments, evidence, scope, limitations, decision, rules version and source digests for the input, rubric, invariant catalog and required oracles. No wall clock or random input participates. `report.py` checks schema and hash and never derives or upgrades findings.

Hashes provide content addressing and tamper detection against a retained hash. They are **not** digital signatures, authentication, immutable storage, or proof that an input was true. Retain original records; changes require a new digest and assessment record.

## Release boundary and evidence

Machine tests establish bounded coherence and deterministic fixture behavior only. The synthetic fixture pair was authored by the implementation agent; it is not two independent human assessments. No actual kernel sanitizer, Rust compiler, upstream study or candidate evaluation has run. Human calibration, independent assessor training, evidence authentication and longitudinal criterion-validity work remain OPEN. See `evidence/execution/REPORT.md` and `GOVERNANCE.md`.

All frozen seven gates must pass, including real independent calibration, before tagging `v1.1-alpha`. The implementation cannot self-certify and does not automatically issue Git tags/releases. CI run evidence, not workflow text, is execution authority for CI claims.
