# Static trust-boundary review

AST inspection of all production tools found no eval/exec, pickle loading, dynamic module imports, or shell=True. Literal strings naming attacks in tests do not execute candidate code. `trust-review.json` lists inspected filesystem/subprocess/YAML/environment sites and file digests.

| Conversion | Trust boundary |
|---|---|
| `tools.common.load` text → data | Strict JSON / SafeLoader subclass, duplicate keys and nonfinite floats rejected; existing 2 MB/depth64/node100000 bounds. Parsing grants no evidence authority. |
| `provenance.load_context` registry → source bytes | Explicit repository registry, schema-checked fixed basename paths, no file discovery, no network/cwd/env source selection. Symlinks rejected; bounded reads and aggregate 2 MB cap. Missing/unreadable source becomes unavailable, not a submitted-value fallback. Registry/code management is administrative authority. |
| `provenance.extract` text → fact | Exact authorized one-line selector and fixed JSON capsule grammar. Strict parser; no arbitrary expression, prose keyword or code execution. Only selected fields get authority; whole-file digest is integrity, not whole-document semantics. |
| `provenance.subjects` records → required facts | Closed projection of claim/scope/evidence/invariants/oracle observations/assessor structured findings/hard gates. Non-authoritative limitations and asserted positive oracle labels cannot create facts. |
| `provenance.evaluate/enforce` facts → admission | Exact canonical typed comparison, all dossier grants required, explicit contradictions and missing/invalid provenance. No source ordering, timestamps or voting; any failure prevents derivation. |
| `derive` admitted facts → qualification | Existing E/L separation, catalog criticality, material closure, method/strength constraints and bounded oracle evaluation remain. Provenance admission occurs before capability/qualification credit. No production issuance or source repair. |
| `report/validate_record` qualification → presentation | Retained input is rederived against independent registry; claimed source results cannot be smuggled in by rehashing output. |
| test-only `source_fixtures.issue` | Explicit controlled fixture preparation; production never imports it. Legacy tests isolate downstream behavior. Dedicated provenance tests freeze authority before mutation. No claim of independent humans. |

Existing release-runner subprocess invocations are fixed trusted pytest/CLI commands, not candidate code; they do not have an internal timeout. This pre-existing runner limitation is disclosed, not a new derivation execution path. Remediation recorder wraps commands with a timeout. Fixed `importlib.metadata` dependency-version inspection in the release runner is not dynamic candidate module loading. Existing environment reads only annotate CI receipts; no environment value selects source truth. The loader has no network retrieval, and qualification derivation introduces no writes. This bounded source review is **not** a security certification, OS isolation proof, cryptographic producer authentication, or measurement validation.
