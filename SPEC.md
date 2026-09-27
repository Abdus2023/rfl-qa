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

## Remediation execution contract — rules 1.1-alpha.2

This section records the explicit HG-01..HG-07 implementation requirements; it does not add competencies or change the frozen qualification axes. Earlier descriptions of weaker validation are superseded only at the boundaries listed here and in CHANGELOG.md.

- The catalog's criticality is immutable in a dossier; claiming either more or less criticality is invalid. Required external VERIFIED claims require VERIFIED external support and explicit invariant bindings. Reference/method matches still do not authenticate an external document or establish relevance from prose alone.
- Environment and task-class arrays denote the full alpha combination, not a menu. Both `required ⊆ claimed` and `claimed ⊆ supported` are enforced; exclusions remain a superset and disjoint from claims. Equivalent ordering is accepted, but duplicate entries reject.
- The closure includes evidence for every required check and its observation, in addition to required invariant, behavioral, primary and assessor evidence. Optional flags cannot remove referenced support. Consequently the RCU absence-classification check's OPEN NMI evidence now limits its ceiling to OPEN; no NMI proficiency is asserted. The RCU decision remains PROVISIONAL.
- Methods have compatible strength sets: not_tested → ABSENCE_OF_EVIDENCE; dynamic diagnostics → OBSERVATION/COVERAGE; rustc/formal → PROOF/OBSERVATION/COVERAGE; review/documentation → OBSERVATION/COVERAGE. No method implies an epistemic state.
- `oracle_results` are ASSERTED_RESULT and must link to an `oracle_observations` record bound to the candidate input and check-specific evidence. `oracle_evaluations` are DERIVED_RESULT, recomputed by the engine. Submitted PASS cannot provide the result; asserted BLOCKED remains an additional conservative veto and NOT_RUN prevents verification. Neither alters the independently computed evaluator outcome.
- Observations supply only one of three closed payloads: a bounded lifecycle trace, an invariant classification, or an evidence-strength classification. The lifecycle trace has at most nine snapshots, in the frozen sequence, with explicit object/reference/callback/RCU/registered-owner liveness fields. Undrained resources at destroy/free, a dead target with a possible callback, live reference to a dead object, and invalid/incomplete sequences fail. These are finite modeled observations, not execution of candidate Rust/C code.
- Output provenance binds the structured input, observation, evidence and oracle. `derivation_input` is retained so record validation can compare a recomputed result. The reporter validates, then presents without altering facts. Old output profiles are not silently upgraded; historical evidence remains interpretable under its recorded rules.
- The evaluator cannot prove supplied facts true. Real artifact authentication, independent assessors, source-audit adequacy and kernel execution remain external evidence requirements; no hash substitutes for them.
- Parsing limits: 2 MB per document, depth 64, 100,000 visited nodes; trace length ≤9. Counts must be integer representations, not float/non-finite values. YAML aliases are permitted only when they stay within the bounds and schema; duplicate keys and unsafe tags reject.

Regressions are in `tests/test_remediation.py`. The original 119 tests are retained unchanged. Independent human calibration is still absent, so the release workflow's procedural gate must remain blocked even if the machine regression steps succeed.

## Scoped source provenance — rules 1.1-alpha.3

`evidence/aud-007-008/provenance-contract.yaml` defines the bounded contract. These are new **provenance states**, not epistemic statuses: SUPPORTED, CONTRADICTED, UNBOUND, UNVERIFIABLE, INVALID_BINDING. Any non-SUPPORTED diagnostic prevents qualification derivation; it is not converted to OPEN, PROVISIONAL or a positive observation. The existing epistemic vocabulary and capability/evidence axes remain unchanged.

The CLI's authority root is the separately controlled `artifacts/registry.json`. It alone admits local source files, identities, SHA256 pins, dossier-specific subjects, exact one-line selectors, and the fixed `rfl-json-fact-v1` extraction rule. A dossier supplies bindings and observed values, never its own trusted registry. No file discovery, network, timestamps, filenames, environment variables or source ordering establish authority. The pure evaluator accepts an explicit authority snapshot from a trusted embedding caller; this administrative API is not an untrusted-dossier field. Registry/code administration remains a trusted deployment boundary.

Every authorized subject for this dossier must be accounted for, including facts whose corresponding record a submitter attempts to remove. Multiple authorized sources are all inspected. Any disagreement is explicit; no winner is selected. Binding identifiers form an unordered mapping; duplicate JSON/YAML keys reject. Overlapping/duplicated authorized selectors reject; line ranges must select exactly one line. Missing files/facts provide no support. Malformed grants/provenance reject; there is no recovery or implicit whole-document scope.

Only `RFL-QA-FACT {"subject": "...", "value": ...}` at an authorized line can yield a typed fact. Values use the existing dossier records; there is no general expression or NLP engine. The projection includes claim identity, scope, evidence (including explicitly bound statements), invariants, oracle observations, structured assessor findings, and hard gates. Assessor/dossier limitations and unrelated prose have no qualification authority. Positive oracle labels remain ASSERTED_RESULT; computed oracle outcomes remain DERIVED_RESULT. Source authentication does not bypass oracle execution or catalog-defined criticality.

Artifact digests use the existing canonical SHA256 mechanism on artifact ID, dossier ID and exact decoded UTF-8 content. Thus a renamed identity or any changed content invalidates stale pins. Scoped field authority is distinct from whole-file integrity. Unselected text does not acquire authority because its bytes were hashed. Source byte changes intentionally affect artifact identity; extracted value identity remains canonical and is insensitive to JSON object key order. Unregistered files have no effect at all; bound metadata retained in the complete qualification record remains hash-bound without gaining authority.

A stale pin plus a parseable mismatching source produces both INVALID_BINDING and CONTRADICTED diagnostics. The latter then denotes a syntactic difference, not authenticated source truth. Only intact integrity and exact grant/value agreement can yield SUPPORTED. This preserves both the digest-failure and source-mutation metamorphic oracles without silently resolving their difference.

All repository source fixtures are **synthetic**. Integrity/authorization of controlled content does not authenticate a human producer, honest kernel observation, adequate external audit, real assessor independence or criterion validity. The CLI does not issue new grants. Test-only fixture preparation explicitly issues controlled authority for the retained downstream regressions; new provenance tests freeze that independent snapshot before attacking it. No runtime repair/default or production self-signing facility is added.
