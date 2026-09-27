# RFL-QA v1.1-alpha EXECUTION REPORT

Repository: `Abdus2023/rfl-qa`
Commit at execution: `06053bfc03366912e9880eab5208ba13af3f5da8`
Source snapshot: `source-manifest.json` (SHA-256 `698d410d2beb1a114e85be15fa1040b0c0ab5ec6f90154e454caa362a1722ff6`)

Environment: `Linux-6.1.158+-x86_64-with-glibc2.36`
Python: `3.11.2`
Dependencies: pinned in `requirements.txt`; installed versions recorded in `ledger.yaml`.

| Gate | Status | Executed evidence |
|---|---|---|
| SCHEMA | **PASS** | `schema.log` |
| DERIVATION | **PASS** | `derivation.log` |
| INVARIANT | **PASS** | `invariant.log` |
| ORACLE | **PASS** | `oracle.log` |
| HARD_GATE | **PASS** | `hard_gate.log` |
| AUD_007_PROVENANCE | **PASS** | `aud_007_provenance.log` |
| AUD_008_PROSE_AUTHORITY | **PASS** | `aud_008_prose_authority.log` |
| CALIBRATION | **BLOCKED** | `calibration_automated.log`: synthetic comparison tests only; independent human run unavailable |
| REPRODUCIBILITY | **PASS** | `reproducibility.log` |

Tests: **653 passed**, 0 failed, 0 errors, 0 skipped. See `tests.log` and `pytest.xml`.

## Reproduction and records

The determinism test executed 100 full in-process derivations and two CLI derivations. Each of the three lab examples was derived and reported; canonical qualification records and readable reports are retained here. Input scopes and epistemic states remain unchanged.

The source manifest binds the actual executed files, independently of pre-existing unrelated worktree changes. Raw stdout/stderr and exit codes are retained, including valid rejected-decision tests. Logs demonstrate only their declared populations.

## Known limitations and OPEN findings

- **Human calibration BLOCKED:** only synthetic fixture assessors were available; no independent human measurements or adjudication were performed.
- **Remote CI NOT_RUN:** local commands have executed; workflow existence is not CI execution evidence.
- **No real kernel runs:** no Rust/compiler/sanitizer/hardware execution or actual candidate artifact review. Structured fixture results are not kernel safety proof.
- **External authenticity OPEN:** scoped content integrity and authorization are checked against the explicit registry; producer honesty, source-audit adequacy and actual human independence remain unestablished.
- **Outcome attribution OPEN:** causal classifications require reviewed scope/confounder evidence; no downstream bug is automatically a false positive or validation.
- **Criterion validity OPEN:** no longitudinal upstream data. Hash consistency is not authenticity or empirical validity.
- See `GOVERNANCE.md` for recorded vocabulary/sample-code contradictions and their limited treatment.

## Release status: BLOCKED

No tag or release created. Mandatory independent calibration and remote CI evidence are missing. Machine checks do not certify the system itself.
