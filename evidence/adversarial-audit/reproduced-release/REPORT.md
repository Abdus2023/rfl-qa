# RFL-QA v1.1-alpha EXECUTION REPORT

Repository: `Abdus2023/rfl-qa`
Commit at execution: `33e4d95f835ecfd42830087dcd2772bb6cc8c216`
Source snapshot: `source-manifest.json` (SHA-256 `86f8b796a887f7f288e66dca4f537080bd094494ec72ba4169c40184c33bcaae`)

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
| CALIBRATION | **BLOCKED** | `calibration_automated.log`: synthetic comparison tests only; independent human run unavailable |
| REPRODUCIBILITY | **PASS** | `reproducibility.log` |

Tests: **119 passed**, 0 failed, 0 errors, 0 skipped. See `tests.log` and `pytest.xml`.

## Reproduction and records

The determinism test executed 100 full in-process derivations and two CLI derivations. Each of the three lab examples was derived and reported; canonical qualification records and readable reports are retained here. Input scopes and epistemic states remain unchanged.

The source manifest binds the actual executed files, independently of pre-existing unrelated worktree changes. Raw stdout/stderr and exit codes are retained, including valid rejected-decision tests. Logs demonstrate only their declared populations.

## Known limitations and OPEN findings

- **Human calibration BLOCKED:** only synthetic fixture assessors were available; no independent human measurements or adjudication were performed.
- **Remote CI NOT_RUN:** local commands have executed; workflow existence is not CI execution evidence.
- **No real kernel runs:** no Rust/compiler/sanitizer/hardware execution or actual candidate artifact review. Structured fixture results are not kernel safety proof.
- **Evidence authentication OPEN:** artifact/source-audit references and independence declarations are structurally checked, not authenticated.
- **Outcome attribution OPEN:** causal classifications require reviewed scope/confounder evidence; no downstream bug is automatically a false positive or validation.
- **Criterion validity OPEN:** no longitudinal upstream data. Hash consistency is not authenticity or empirical validity.
- See `GOVERNANCE.md` for recorded vocabulary/sample-code contradictions and their limited treatment.

## Release status: BLOCKED

No tag or release created. Mandatory independent calibration and remote CI evidence are missing. Machine checks do not certify the system itself.
