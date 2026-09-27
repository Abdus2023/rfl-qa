# AUD-007 / AUD-008 scoped provenance remediation — RELEASE BLOCKED

**NO EVIDENCE → NO VERIFIED CLAIM.** Source under test: `06053bfc03366912e9880eab5208ba13af3f5da8`. Frozen baseline: `b0582f6`; prior receipt: `92d3bba`. Rules: **1.1-alpha.3**. All current-source results below are **local**; current-source CI is **NOT_RUN / BLOCKED**.

## 1. Reproduction and frozen state

Before implementation, the unchanged suite executed **564 passed** and schema validation passed. Both saved attacks—contradictory teardown prose paired with safe observations, and unrelated external audit prose—again produced **VERIFIED_WITHIN_SCOPE**. `before.json`, `reproduce-open-findings` and baseline command receipts preserve this reproduction. Existing 16-process baseline and old CI conclusions are not reinterpreted.

All **183 previous evidence files** (including the earlier 97 and the complete remediation receipt) remain byte-identical; see `preservation-results.json`. All **11 prior test modules** are byte-identical. Only shared fixture preparation and controlled fixture data were adapted to supply explicit source grants; no old test body/oracle was weakened. The rehydrated checkout matched every published 92d3bba file before index/HEAD alignment; no force push was used.

The mission uses AUD-007 for contradiction and AUD-008 for prose authority, while the older audit used the reverse prose/combined-oracle association. Both old counterexamples and both boundaries are covered here; prior IDs/documents are not edited.

## 2. Formalized invariant before coding

`provenance-contract.yaml`, `contradiction-cases.yaml` and `prose-boundary-cases.yaml` were written before implementation changes. Every qualification-relevant record must match an explicitly authorized dossier/subject/source/digest/selector/rule binding. Unregistered prose contributes nothing. All authorized sources are inspected; a submitter cannot omit a conflicting grant or its target record.

SUPPORTED, CONTRADICTED, UNBOUND, UNVERIFIABLE and INVALID_BINDING are **provenance diagnostics**, not replacements for frozen epistemic states. Any non-SUPPORTED state prevents derivation; no contradiction becomes OPEN/PROVISIONAL/VERIFIED or positive capability credit. A stale pin yields INVALID_BINDING; a parseable difference also yields CONTRADICTED as a syntactic mismatch, not as authenticated truth. Reauthenticated changed content still contradicts the unchanged observation. This explicitly reconciles case E and M1 without dropping either oracle.

## 3. Minimal implementation

- Separate, repository-controlled `artifacts/registry.json` admits sources and grants. Dossiers cannot supply or extend this authority root. CLI source selection is independent of caller cwd, environment and filenames outside the registry.
- Reuse canonical SHA256 for artifact ID + dossier ID + exact content; changed bytes or falsely relabeled identity cannot reuse a pin.
- One fixed extraction rule, `rfl-json-fact-v1`, selects an explicit single line containing a strictly parsed JSON fact capsule. No general evaluator, arbitrary code, NLP inference, or keyword authentication.
- Validate source identity/scope/rule/value before qualification. Include deterministic binding/value/source identities in `source_authentication` and the complete qualification hash. Existing ASSERTED_RESULT versus DERIVED_RESULT and hard-gate logic remain intact.
- Exact bounds: ≤2 MB source collection, ≤1024 grants/artifacts, single-line selectors, existing structured depth/node bounds. No implicit whole-document scope.
- Explicit controlled fixture migration; production does not issue grants or repair input. The legacy run fixture prepares authorized synthetic inputs to isolate its pre-existing tests. Dedicated new provenance tests **never use that fixture** and freeze authority before mutation.

## 4. Regression and adversarial replay

The final committed procedural run executed **653 passed, 0 failed, 0 skipped, 0 errors**: **564 retained + 89 focused new regressions**. Required `pytest -q` and `python tools/validate.py --all` executed successfully; the procedural runner repeats the full suite and records the exact source commit.

- **C1–C15: 15/15 contracted cases passed.** Every case has an explicit machine-readable oracle and retained input/independent authority snapshot under `cases/`.
- **M1–M7:** source-only, observation-only, unrelated prose, missing source, digest, cross-dossier and scope mutations executed in dedicated parameterized tests.
- **P1–P10:** unrelated PASS/VERIFIED/calibration/competency/oracle/hard-gate text has no qualification authority, including assessor limitations and actual unrelated files.
- Source replacement and missing-file tests exercise the actual fixed-registry filesystem loader. Duplicate keys/scopes, invalid digest/algorithm/rule, invalid locations, type/enum changes, YAML aliases/scalars/null/timestamp, nonfinite values, unknown properties and bool-versus-integer comparison are covered.
- Conflict tests include withholding the conflicting binding, source order reversal and deleting an authorized evidence record; none yields support.
- Authenticated unsafe traces still trigger the bounded oracle/hard-gate veto even when submitted labels say PASS. Source authentication does not convert an asserted PASS into a derived one.

Post-fix replay isolates the **original** attacks: source controls restore only the attacked textual source identity/statement, while keeping the original VERIFIED statuses and safe trace payloads. Independent authority is then frozen before reintroducing the attacked fields. Both positive controls qualify synthetically; both original attacks reject with **CONTRADICTED** at the evidence subject. Rejection is not merely due to missing new schema fields. `replay-results.json` contains exact results.

Earlier failed test runs remain logged: the first fixture migration changed assessor digests for an unmigrated poisoned fixture (563/564); explicitly migrating that controlled fixture resolved the mismatch without changing the test. The first focused run had eight no-op attacks setting an already-false Boolean to false; mutations were corrected to actual inversions. A test-only shared location object was also copied so observation mutations cannot change authority by alias. Final suites/replays are green.

## 5. Hashing and determinism

Artifact identity binds ID, dossier and exact content; binding identity additionally binds subject, digest, extraction rule and selector. Value identity is the canonical typed value. Mapping key order/serialization indentation is presentation-only. Existing complete-record array ordering, timestamps and limitations remain hash-bound, but do not establish authority. Unregistered files do not even affect the qualification hash. An unselected line in a bound file still changes the integrity digest; explicit reauthentication may preserve semantic results, never silently reuse a stale pin.

All **three canonical derive/report pipelines** executed. **16 independent CLI derivations** and **16 independent contradiction-evaluation processes** were byte-identical within each population, varying hash seeds, cwd, locale, timezone and sequential/concurrent scheduling; source/grant/binding insertion order was reversed for conflicts. See `determinism-results.json`, `canonical-results.json`, `outputs/` and command receipts. These are synthetic model results, not kernel observations.

## 6. CI evidence — BLOCKED, not silently inferred

The workflow was inspected. It still requests Python 3.11, pinned dependencies, schema, full pytest, CLI derive/report, and the nonzero procedural release gate with always-uploaded evidence. The proposed workflow change only redirects new execution/artifact output to this task's directory, preserving old receipts; it does not skip a gate or turn failure into success.

**Push failed**: GitHub refuses a GitHub App workflow update without `workflows` permission. Remote branch remains `92d3bba`; **no CI run exists for `06053bfc03366912e9880eab5208ba13af3f5da8`**. Current run ID is null, jobs empty, logs/artifacts unavailable, failure detail UNCONFIRMED. We did not dispatch an old revision and call it remediation CI. Read-only GitHub observations confirm historical completed failed runs, not new-source execution. Old EOF log/artifact limitations remain frozen observations, not invented new retrieval failures.

The GitHub connection needs workflow-edit permission. Reconnect GitHub in Arena, then push only `arena/01a0dfcc-rfl-qa` and collect actual run/job/log/artifact receipts. Local PASS is not CI PASS. Both findings therefore remain **FIXED_LOCALLY_CI_PENDING**, with **no VERIFIED fix claim**.

## 7. Trust review and unresolved limits

`trust-boundary-review.md` and `trust-review.json` record the text→fact→evidence→qualification boundaries and prohibited-call search. No eval/exec, pickle trust, dynamic candidate import/execution, shell=True or network retrieval was added. Existing release-runner fixed subprocess calls lack an internal timeout; the audit recorder bounds its invocation. This review is not security certification.

The registry is a trusted administrative root, not proof of an honest human producer or a real kernel event. Changing the trusted registry/code can change authority; an untrusted dossier cannot. Only declared exact structured slices are machine-admissible; arbitrary narrative interpretation and source-audit adequacy remain outside this implementation. Full-file hashing does not authorize every sentence. All current sources are explicitly synthetic. **Human calibration NOT_RUN, kernel/compiler/sanitizer execution NOT_RUN, criterion validity NOT_ESTABLISHED.** Historical provenance/terminology issues outside this mission remain unchanged.

## 8. Disposition and final deterministic matrix

| Finding | Disposition | Evidence |
|---|---|---|
| AUD-007 | FIXED_LOCALLY_CI_PENDING | before.json → frozen contracts → 89 focused regressions/replay → deterministic results; CI permission blocker |
| AUD-008 | FIXED_LOCALLY_CI_PENDING | before.json → scoped-authority/negative-prose tests → deterministic results; CI permission blocker |

Gate PASS below means only the executed bounded local contract, not independent measurement validity or a verified finding closure.

| Gate | Status | Evidence |
|---|---|---|
| Schema | PASS | procedural/schema.log |
| Derivation | PASS | procedural/derivation.log; outputs/ |
| Invariant | PASS | procedural/invariant.log |
| Oracle | PASS | procedural/oracle.log; dedicated asserted-PASS tests |
| Hard-gate | PASS | procedural/hard_gate.log; C13 |
| AUD-007 | PASS | replay-results.json; procedural/aud_007_provenance.log (bounded local contract) |
| AUD-008 | PASS | procedural/aud_008_prose_authority.log; P1-P10 (bounded local contract) |
| Calibration | BLOCKED | procedural/ledger.yaml: independent human execution NOT_RUN |
| Reproducibility | PASS | determinism-results.json: 16 + 16 independent processes |
| CI | BLOCKED | ci.yaml: no current-source run ID; push rejected for workflows permission |
| Kernel execution | NOT_RUN | No kernel/compiler/sanitizer execution was performed |
| Criterion validity | NOT_ESTABLISHED | No upstream outcome validation |
| Release | BLOCKED | findings.yaml; CI, human/kernel/criterion prerequisites remain absent |

## Receipt handling

`environment.yaml` records exact local Python/OS/architecture/dependency versions and only allowlisted environment values. `commands.log` and `command-records.jsonl` retain actual commands/stdout/stderr/exit codes. `hash-manifest.yaml` seals evidence, qualification outputs and source files, excluding itself to avoid recursion. Administrative evidence-only commit metadata is represented by Git history, not recursively embedded into its own receipt.

The source commit and later evidence receipt are **local only** pending GitHub permission repair. No release or tag is created. Release remains **BLOCKED** throughout. The next action is real current-source CI execution after reconnecting—not declaring the remaining prerequisites satisfied.
